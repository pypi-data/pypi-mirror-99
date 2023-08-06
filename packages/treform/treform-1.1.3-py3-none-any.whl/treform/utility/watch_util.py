import time

from treform.utility.date_util import DateUtil


class StopWatch:
    def __init__(self):
        self.Elapsed = 0.
        self.LastStart = None

    def start(self):
        assert self.LastStart is None
        self.LastStart = time.time()
        return self

    def stop(self):
        assert self.LastStart is not None
        self.Elapsed = time.time() - self.LastStart
        self.LastStart = None
        return self

    def elapsed(self):
        if self.LastStart is None:  # stopped
            return self.Elapsed
        else:
            return time.time() - self.LastStart


class WatchUtil(object):
    """
    - wrapper of 'pytools.stopwatch.StopWatch`
    - support multiple watches.
    """
    DEFAULT_WATCH_NAME = ''

    def __init__(self, auto_stop=True):
        """
        :param auto_stop: auto_stop=True이면, elapsed() 또는 elapsed_string() 호출시 자동으로 stop() 호출됨.
        """
        self.__watches = {}
        self.__cnt = {}
        self.auto_stop = auto_stop

    def __get(self, name=DEFAULT_WATCH_NAME) -> StopWatch:
        if name not in self.__watches:
            self.__watches[name] = StopWatch()
            self.__cnt[name] = 0
        return self.__watches[name]

    def del_watch(self, name=DEFAULT_WATCH_NAME) -> bool:
        if name in self.__watches:
            del self.__watches[name]
            return True
        else:
            return False

    def start(self, name=DEFAULT_WATCH_NAME) -> StopWatch:
        try:
            self.__get(name).stop()
        except:
            pass
        self.__get(name).start()
        self.__cnt[name] += 1
        return self.__get(name)

    def stop(self, name=DEFAULT_WATCH_NAME) -> StopWatch:
        return self.__get(name).stop()

    def elapsed(self, name=DEFAULT_WATCH_NAME) -> int:
        if self.auto_stop:
            try:
                self.__get(name).stop()  # must call start() later.
            except AssertionError:
                pass
        return self.__get(name).elapsed()

    def elapsed_string(self, name=DEFAULT_WATCH_NAME) -> str:
        return DateUtil.secs_to_string(self.elapsed(name))

    def summary(self, prefix='', include_total_time=False) -> str:
        import operator
        li = [(name, self.__watches[name].elapsed()) for name in self.__watches]
        li = sorted(li, key=operator.itemgetter(1), reverse=True)
        s = ''
        # for name, total_milli_secs in li:
        #     s += 'total [%s] %s\n' % (DateUtil.millisecs_to_string(total_milli_secs), name)
        if include_total_time:
            for name, total_milli_secs in li:
                if self.__cnt[name] > 0:
                    if len(prefix) > 0:
                        s += '%s total [%s] %s\n' % (
                            prefix, DateUtil.millisecs_to_string(float(total_milli_secs)), name)
                    else:
                        s += 'total [%s] %s\n' % (
                            DateUtil.millisecs_to_string(float(total_milli_secs)), name)

        for name, total_milli_secs in li:
            if self.__cnt[name] > 0:
                print(total_milli_secs)
                if len(prefix) > 0:
                    s += '%s average [%s] %s\n' % (
                        prefix, DateUtil.millisecs_to_string(float(total_milli_secs) / float(self.__cnt[name])), name)
                else:
                    s += 'average [%s] %s\n' % (
                        DateUtil.millisecs_to_string(float(total_milli_secs) / float(self.__cnt[name])), name)
        return s


if __name__ == '__main__':
    watches = WatchUtil(auto_stop=False)

    # watches.start('A')
    # time.sleep(1)
    # print(watches.elapsed_string('A'))
    # watches.del_watch('A')

    watches.start()
    time.sleep(3)
    print(watches.elapsed_string())

    watches.start()
    time.sleep(1)
    print(watches.elapsed_string())
    print(watches.elapsed_string())

    watches.start()
    time.sleep(3)
    print(watches.elapsed_string())

    print(watches.summary())