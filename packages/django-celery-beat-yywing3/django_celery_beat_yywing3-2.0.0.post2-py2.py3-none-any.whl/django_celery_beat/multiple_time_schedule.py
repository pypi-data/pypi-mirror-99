"""multiple time schedule Implementation."""

from datetime import timedelta
from celery import schedules
from .utils import NEVER_CHECK_TIMEOUT, replace_datetime_time


class multipletime(schedules.BaseSchedule):
    """multiple time schedule."""

    def __init__(self, timezone, times, model=None, nowfun=None, app=None):
        """Initialize multiple time.

        :type times: List[time]"""
        self.timezone = timezone
        self.times = sorted(times)
        super(multipletime, self).__init__(nowfun=nowfun, app=app)

    def get_next_datetime(self, last_run_at):
        """
        Get next run time for given last_run_at
        :type last_run_at: datetime
        """
        last_run_time = last_run_at.time()
        if last_run_time >= self.times[-1]:
            return replace_datetime_time(last_run_at, self.times[0]) + timedelta(days=1)
        for time in self.times:
            if last_run_time < time:
                return replace_datetime_time(last_run_at, time)

    def now_with_tz(self):
        return self.now().astimezone(self.timezone)

    def remaining_estimate(self, last_run_at):
        next_datetime = self.get_next_datetime(last_run_at)
        now_datetime = self.now_with_tz()
        r = next_datetime - now_datetime
        return r

    def is_due(self, last_run_at):
        if len(self.times) == 0:
            return schedules.schedstate(is_due=False, next=NEVER_CHECK_TIMEOUT)

        last_run_at = last_run_at.astimezone(self.timezone)
        # will update self._next_time
        rem_delta = self.remaining_estimate(last_run_at)
        remaining_s = max(rem_delta.total_seconds(), 0)
        if remaining_s == 0:
            return schedules.schedstate(
                is_due=True,
                next=self.remaining_estimate(
                    self.now_with_tz()
                ).total_seconds(),
            )
        return schedules.schedstate(is_due=False, next=remaining_s)

    def __repr__(self):
        return "<multipletime: {} {}>".format(self.timezone, self.times)

    def __eq__(self, other):
        if isinstance(other, multipletime):
            return self.times == other.times and self.timezone == other.timezone
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __reduce__(self):
        return self.__class__, (self.timezone, self.times)
