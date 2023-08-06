"""
This module contains classes for performing interval accumulation calculations.

These interval accumulator classes all conform to a specific interface.
If no data is received during the interval, the interval accumulator should return None.

Author: J. M. Fife
"""


class IntervalAccumulatorAverage:
    """" Class for calculating average value during an interval regardless of position in the interval """

    def __init__(self):
        self.n_samples = 0
        self.sum = 0.0

    def val(self):
        if self.n_samples:
            return self.sum/self.n_samples
        else:
            return None

    def reset(self):
        self.n_samples = 0
        self.sum = 0.0

    def accum(self, sample):
        if self.n_samples:
            self.sum = self.sum + sample
        else:
            self.sum = sample
        self.n_samples = self.n_samples + 1


class IntervalAccumulatorMin():
    """ Class for calculating the minimum value observed during an interval """

    def __init__(self):
        self.min = None

    def val(self):
        return self.min

    def reset(self):
        self.min = None

    def accum(self, sample):
        if self.min is not None:
            if sample < self.min:
                self.min = sample
        else:
            self.min = sample


class IntervalAccumulatorMax():
    """ Class for calculating the minimum value observed during an interval """

    def __init__(self):
        self.max = None

    def val(self):
        return self.max

    def reset(self):
        self.max = None

    def accum(self, sample):
        if self.max is not None:
            if sample > self.max:
                self.max = sample
        else:
            self.max = sample


class IntervalAccumulatorOn:
    """" Derived class for calculating whether an ON/OFF string was ever ON during an interval """

    def __init__(self):
        self.on_off = None

    def val(self):
        return self.on_off

    def reset(self):
        self.on_off = None

    def accum(self, sample):
        if self.on_off is None:
            self.on_off = "OFF"
        if sample == "ON":
            self.on_off = "ON"


class IntervalAccumulatorOr:
    """" Class for calculating AND of a bitmap during an interval """

    def __init__(self):
        self.samples_or = None

    def val(self):
        return self.samples_or

    def reset(self):
        self.samples_or = None

    def accum(self, sample):
        if self.samples_or is None:
            self.samples_or = 0
        self.samples_or = self.samples_or | sample


class IntervalAccumulatorFirst:
    """ Class for simply recording the first value in chronological order during an interval """

    def __init__(self):
        self.first = None

    def val(self):
        return self.first

    def reset(self):
        self.first = None

    def accum(self, sample):
        if self.first is None:
            self.first = sample


class IntervalAccumulatorLast:
    """ Class for simply recording the last value in chronological order during an interval """

    def __init__(self):
        self.last = None

    def val(self):
        return self.last

    def reset(self):
        self.last = None

    def accum(self, sample):
        self.last = sample


class IntervalAccumulatorLastNonzero:
    """ Class for simply remembering the last nonzero value during an interval ot 0 if no nonzero values """

    def __init__(self):
        self.last = None

    def val(self):
        return self.last

    def reset(self):
        self.last = None

    def accum(self, sample):
        if self.last is None:
            self.last = 0
        if sample:
            self.last = sample


class IntervalAccumulatorFactory:

    def __init__(self):
        self._registry = {}

    def register(self, name, intervalaccumulator):
        self._registry[name] = intervalaccumulator

    def get_intervalaccumulator(self, name):
        intervalaccumulator = self._registry.get(name)
        if not intervalaccumulator:
            raise ValueError(name)
        return intervalaccumulator()


intervalaccumulatorfactory = IntervalAccumulatorFactory()
intervalaccumulatorfactory.register('avg', IntervalAccumulatorAverage)
intervalaccumulatorfactory.register('min', IntervalAccumulatorMin)
intervalaccumulatorfactory.register('max', IntervalAccumulatorMax)
intervalaccumulatorfactory.register('on', IntervalAccumulatorOn)
intervalaccumulatorfactory.register('or', IntervalAccumulatorOr)
intervalaccumulatorfactory.register('first', IntervalAccumulatorFirst)
intervalaccumulatorfactory.register('last', IntervalAccumulatorLast)
intervalaccumulatorfactory.register('lastnonzero', IntervalAccumulatorLastNonzero)

