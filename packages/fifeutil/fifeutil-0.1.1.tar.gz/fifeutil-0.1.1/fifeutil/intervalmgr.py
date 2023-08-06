from fifeutil.sqlite_data_store import SqliteDeviceDataStore, StoreTSResult
from fifeutil.intervalaccumulator import intervalaccumulatorfactory
import logging

log = logging.getLogger(__name__)


class IntervalMgr:
    """
    Class for maintaining accumulated interval data which is timestamped at the beginning of the interval (BoI).
    Supports a callback function when intervals are complete.
    Rules:
        1. Records must arrive in sequential order (ts must be monotonically increasing) or are rejected
        2. Interval values will be calculated by interval accumulator functions provided on a field-by-field basis
        3. All previous intervals (if any) will be closed out when any measurement is received for a later interval
        4. The minimum number of measurements required to complete an interval can be given on a field-by-field basis
        5. Timestamps marking the beginning of each interval (BoI)
    Three pandas dataframes are stored in the data store in the following tables:
        1. interval - records that are accumulated at intervals_per_hour based on interval_types_map
        3. now - latest record received
    """

    def __init__(self, data_store, interval_types, callbackfunction, intervals_per_hour=4,
                 close_interval_threshold=0.1):
        """
        Constructor for interval mananager.

        Args:
            data_store (SqliteDeviceDataStore): data store
            intervals_per_hour (int): number of samples per hour for interval data accumulation
            callbackfunction: method to call with new complete interval record.  Takes args ts0, dt, field dict.
            interval_types (dict): dict of lists of IntervalAccumulator objects specifying accumulation behavior
            close_interval_threshold (dict):
        """
        self.data_store = data_store
        self.intervals_per_hour = intervals_per_hour
        self.callbackfunction = callbackfunction
        self.ts_index_workingon = 0
        self.ts_last = 0
        self.seconds_per_interval = int(3600 / intervals_per_hour)
        self.intervalaccumulatordict = self.intervalaccumulatorlisttodict(interval_types)

    def process(self, ts_sec, payload_dict):
        """ Process one data record and take action as needed.
        Args:
            ts_sec (int): timestamp in seconds since epoch in UNIX time (i.e. ignoring leap seconds)
            payload_dict (dict): dict containing the data record to store
        """
        ts_index = int(ts_sec / self.seconds_per_interval)
        log.debug("New Data Record: ts: {}, ts_index: {}, data: {}".format(ts_sec, ts_index, payload_dict))
        if ts_sec < self.ts_last:
            log.error(f"Received a record timestamped later than the previous one. Previous: {self.ts_last} "
                      f"Present one: {ts_sec}")
        payload_dict_with_ts = payload_dict.copy()
        payload_dict_with_ts["ts"] = ts_sec
        self.data_store.store_new_kvdata("now", payload_dict_with_ts)
        if ts_index >= self.ts_index_workingon:
            if ts_index > self.ts_index_workingon:
                if self.ts_index_workingon != 0:
                    # new interval - save the previous interval values and reset the accumulators
                    interval_payload_dict = self.getaccumulatedvalues()
                    ts_completed_interval = int(self.ts_index_workingon * self.seconds_per_interval)
                    ts_next_interval = int((self.ts_index_workingon+1) * self.seconds_per_interval)
                    log.info(
                        f"Storing interval: ts_index {self.ts_index_workingon} "
                        f"from {ts_completed_interval} "
                        f"to {ts_next_interval} "
                        f"data: {interval_payload_dict}")
                    result = self.data_store.store_new_tsdata("interval", ts_completed_interval, interval_payload_dict)
                    if result != StoreTSResult.SUCCESS:
                        log.error(f"Problem storing interval: ts_index {self.ts_index_workingon} "
                                  f"from {ts_completed_interval} "
                                  f"to {ts_next_interval}. "
                                  f"result: {result}")
                    self.reset_accumulators()
                    self.callbackfunction(ts_completed_interval, interval_payload_dict)
                self.ts_index_workingon = ts_index
            self.accumulate_interval_data(payload_dict)
        else:
            log.error(f"Working on ts_index {self.ts_index_workingon}. Received record for old interval: ts_index {ts_index} "
                      f"from {ts_index * self.seconds_per_interval} "
                      f"to {(ts_index+1)* self.seconds_per_interval} ")

    def getaccumulatedvalues(self):
        """ 
        Loop through all of the accumulators to see if any are not None.  If they are, add that accumulator's
        accumulated value to a dict representing a data record

        Returns:
            An interval record as a dict of fields and accumulated values
        """
        interval_value_dict = dict()
        for key, accumulatordict in self.intervalaccumulatordict.items():
            for accumulatorname, accumulator in accumulatordict.items():
                val = accumulator.val()
                if val is not None:
                    interval_value_dict[key + "_" + accumulatorname] = val
        return interval_value_dict

    def reset_accumulators(self):
        """ Reset all interval accumulators """
        for key, accumulatordict in self.intervalaccumulatordict.items():
            for accumulatorname, accumulator in accumulatordict.items():
                accumulator.reset()

    def accumulate_interval_data(self, data_dict):
        # loop through the field names and if there is an accumulator associated with it, accumulate the new value
        for key in data_dict:
            if key in self.intervalaccumulatordict:
                for accumulatorname, accumulator in self.intervalaccumulatordict[key].items():
                    accumulator.accum(data_dict[key])

    @staticmethod
    def intervalaccumulatorlisttodict(intervalaccumulatorlist):
        """ Create a dict of dict of interval accumulators for each possible field and type of accumulator that is specified 
        in a dictionary of lists of accumulator names
    
        Args:
            intervalaccumulatorlist (dict): a dictionary keyed by field name of lists of interval accumulator names
            
        Returns:
            A dict[field name] of dicts[accumulator name] of interval accumulator instances
        """
        intervalaccumulatordict = dict()
        for key, accumulatorlist in intervalaccumulatorlist.items():
            intervalaccumulatordict[key] = dict()
            for accumulatorname in list(accumulatorlist):
                intervalaccumulatordict[key][accumulatorname] \
                    = intervalaccumulatorfactory.get_intervalaccumulator(accumulatorname)
        return intervalaccumulatordict
