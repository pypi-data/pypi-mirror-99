# Copyright 2019 Catalyst Cloud Ltd.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import copy
import datetime
import operator

from ceilometerclient import client as ceiloclient
from oslo_log import log
from oslo_utils import timeutils

from aodh import evaluator
from aodh.evaluator import utils
from aodh.i18n import _
from aodh import keystone_client

LOG = log.getLogger(__name__)
COMPARATORS = {
    'gt': operator.gt,
    'lt': operator.lt,
    'ge': operator.ge,
    'le': operator.le,
    'eq': operator.eq,
    'ne': operator.ne,
}
TYPE = "threshold"


class InsufficientDataError(Exception):
    def __init__(self, reason, statistics):
        self.reason = reason
        self.statistics = statistics
        super(InsufficientDataError, self).__init__(reason)


class ThresholdEvaluator(evaluator.Evaluator):
    # the sliding evaluation window is extended to allow
    # the reporting/ingestion lag.
    look_back = 1

    def __init__(self, conf):
        super(ThresholdEvaluator, self).__init__(conf)
        self._cm_client = None

    @property
    def cm_client(self):
        if self._cm_client is None:
            auth_config = self.conf.service_credentials
            self._cm_client = ceiloclient.get_client(
                version=2,
                session=keystone_client.get_session(self.conf),
                region_name=auth_config.region_name,
                interface=auth_config.interface,
            )

        return self._cm_client

    def _bound_duration(self, rule):
        """Bound the duration of the statistics query."""
        now = timeutils.utcnow()

        # when exclusion of weak datapoints is enabled, we extend
        # the look-back period so as to allow a clearer sample count
        # trend to be established
        if rule.get('exclude_outliers'):
            look_back = rule['evaluation_periods']
        else:
            look_back = self.look_back

        window = rule['period'] * (rule['evaluation_periods'] + look_back)
        start = now - datetime.timedelta(seconds=window)

        return start.isoformat(), now.isoformat()

    @staticmethod
    def _sanitize(rule, statistics):
        """Sanitize statistics."""
        orig_count = len(statistics)

        if rule.get('exclude_outliers'):
            key = operator.attrgetter('count')
            mean = utils.mean(statistics, key)
            stddev = utils.stddev(statistics, key, mean)
            lower = mean - 2 * stddev
            upper = mean + 2 * stddev
            inliers, outliers = utils.anomalies(statistics, key, lower, upper)
            if outliers:
                LOG.debug('excluded weak datapoints with sample counts %s',
                          [s.count for s in outliers])
                statistics = inliers
            else:
                LOG.debug('no excluded weak datapoints')

        # in practice statistics are always sorted by period start, not
        # strictly required by the API though
        statistics = statistics[-rule['evaluation_periods']:]
        result_statistics = [getattr(stat, rule['statistic'])
                             for stat in statistics]

        LOG.debug('pruned statistics from %d to %d',
                  orig_count, len(statistics))

        return result_statistics

    def _statistics(self, rule, start, end):
        """Retrieve statistics over the current window."""
        after = dict(field='timestamp', op='ge', value=start)
        before = dict(field='timestamp', op='le', value=end)
        query = copy.copy(rule['query'])
        query.extend([before, after])

        LOG.info('statistics query for meter: %s, period: %s, query: %s',
                 rule['meter_name'], rule['period'], query)

        try:
            return self.cm_client.statistics.list(
                meter_name=rule['meter_name'], q=query,
                period=rule['period'])
        except Exception:
            LOG.exception(_('alarm stats retrieval failed'))
            return []

    @staticmethod
    def _reason_data(disposition, count, most_recent):
        """Create a reason data dictionary for this evaluator type."""
        return {'type': TYPE, 'disposition': disposition,
                'count': count, 'most_recent': most_recent}

    @classmethod
    def _reason(cls, alarm, statistics, state, count):
        """Fabricate reason string."""
        if state == evaluator.OK:
            disposition = 'inside'
            count = len(statistics) - count
        else:
            disposition = 'outside'

        last = statistics[-1] if statistics else None
        reason_data = cls._reason_data(disposition, count, last)

        transition = alarm.state != state
        if transition:
            return ('Transition to %(state)s due to %(count)d samples'
                    ' %(disposition)s threshold, most recent:'
                    ' %(most_recent)s' % dict(reason_data, state=state),
                    reason_data)
        return ('Remaining as %(state)s due to %(count)d samples'
                ' %(disposition)s threshold, most recent: %(most_recent)s'
                % dict(reason_data, state=state), reason_data)

    def evaluate_rule(self, alarm_rule):
        """Evaluate alarm rule.

        :returns: state, trending state and statistics.
        """
        start, end = self._bound_duration(alarm_rule)
        statistics = self._statistics(alarm_rule, start, end)
        statistics = self._sanitize(alarm_rule, statistics)

        sufficient = len(statistics) >= alarm_rule['evaluation_periods']
        if not sufficient:
            raise InsufficientDataError(
                '%d datapoints are unknown' % alarm_rule['evaluation_periods'],
                statistics)

        def _compare(value):
            op = COMPARATORS[alarm_rule['comparison_operator']]
            limit = alarm_rule['threshold']
            LOG.debug('comparing value %(value)s against threshold'
                      ' %(limit)s', {'value': value, 'limit': limit})
            return op(value, limit)

        compared = list(map(_compare, statistics))
        distilled = all(compared)
        unequivocal = distilled or not any(compared)
        number_outside = len([c for c in compared if c])

        if unequivocal:
            state = evaluator.ALARM if distilled else evaluator.OK
            return state, None, statistics, number_outside, None
        else:
            trending_state = evaluator.ALARM if compared[-1] else evaluator.OK
            return None, trending_state, statistics, number_outside, None

    def _transition_alarm(self, alarm, state, trending_state, statistics,
                          outside_count, unknown_reason):
        unknown = alarm.state == evaluator.UNKNOWN
        continuous = alarm.repeat_actions

        if trending_state:
            if unknown or continuous:
                state = trending_state if unknown else alarm.state
                reason, reason_data = self._reason(alarm, statistics, state,
                                                   outside_count)
                self._refresh(alarm, state, reason, reason_data)
                return

        if state == evaluator.UNKNOWN and not unknown:
            LOG.warning('Expecting %(expected)d datapoints but only get '
                        '%(actual)d'
                        % {'expected': alarm.rule['evaluation_periods'],
                           'actual': len(statistics)})
            # Reason is not same as log message because we want to keep
            # consistent since thirdparty software may depend on old format.
            last = None if not statistics else statistics[-1]
            reason_data = self._reason_data('unknown',
                                            alarm.rule['evaluation_periods'],
                                            last)
            self._refresh(alarm, state, unknown_reason, reason_data)

        elif state and (alarm.state != state or continuous):
            reason, reason_data = self._reason(alarm, statistics, state,
                                               outside_count)
            self._refresh(alarm, state, reason, reason_data)

    def evaluate(self, alarm):
        if not self.within_time_constraint(alarm):
            LOG.debug('Attempted to evaluate alarm %s, but it is not '
                      'within its time constraint.', alarm.alarm_id)
            return

        try:
            evaluation = self.evaluate_rule(alarm.rule)
        except InsufficientDataError as e:
            evaluation = (evaluator.UNKNOWN, None, e.statistics, 0,
                          e.reason)
        self._transition_alarm(alarm, *evaluation)
