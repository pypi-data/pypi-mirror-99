import time


class TimerSyncHour:
    """ Utility class for facilitating fixed intervals synchronized with the top of the hour """
    def __init__(self, triggersperhour: int = 3600):
        """
        Constructor for hourly time synchronizer

        Args:
            triggersperhour (int): number of triggers per hour - will be truncated to `int`
        """
        self.seconds_per_trigger = 3600.0 / int(triggersperhour)
        t_seconds = time.time()
        self.interval = int(t_seconds / self.seconds_per_trigger)

    def nextinterval(self):
        """ Returns True if we are in a later interval than last time we called this method """
        t_seconds = time.time()
        present_interval = int(t_seconds / self.seconds_per_trigger)
        if present_interval != self.interval:
            self.interval = present_interval
            return True
        return False

    def intervalselapsed(self, t_seconds=None):
        """ Returns the number of intervals that have elapsed since last time we called this method """
        if t_seconds is None:
            t_seconds = time.time()
        present_interval = int(t_seconds / self.seconds_per_trigger)
        intervals_elapsed = present_interval - self.interval
        self.interval = present_interval
        return intervals_elapsed

    def triggercallback(self, callbackfunction=None, n=-1, **kwargs):
        """
        Nonblocking method that calls callbackfunction whenever the next interval starts.
        Args:
            callbackfunction: method to call
            n (int): if specified, represents the number of triggers to perform
            kwargs (dict): dict of keyword arguments to callback function
        """
        while n != 0:
            t_seconds = time.time()
            time_to_next_interval = self.seconds_per_trigger - (t_seconds % self.seconds_per_trigger)
            time.sleep(time_to_next_interval)
            callbackfunction(**kwargs)
            if n > 0:
                n = n - 1

