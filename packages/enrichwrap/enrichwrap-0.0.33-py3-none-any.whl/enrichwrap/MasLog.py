import os
from datetime import datetime


MASCmd_Logging = 0xc1


def get_env(key, default=None):
    try:
        val = os.environ[key]
        if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
            val = val[1:-1]
    except:
        val = default
    return val


def str2b(s):
    val = str(s)
    return val.lower() in ('yes','y','true','t','1')


class MasLog:
    ALL    = 1
    TRACE  = 2
    DEBUG  = 3
    INFO   = 4
    WARN   = 5
    ERROR  = 6
    FATAL  = 7
    OFF    = 8
    lvlStr = { ALL:'ALL', TRACE:'TRACE', DEBUG:'DEBUG', INFO:'INFO', WARN:'WARN', ERROR:'ERROR', FATAL:'FATAL', OFF:'OFF' }
    lvlInt = { 'ALL':ALL, 'TRACE':TRACE, 'DEBUG':DEBUG, 'INFO':INFO, 'WARN':WARN, 'ERROR':ERROR, 'FATAL':FATAL, 'OFF':OFF }

    def __init(self,level):
        self._mas = None
        self._logLevel = level
        self._logFile = None
        self._logPrefix = ''
        try:
            log_filename = get_env('MAS_PYLOG_FILE')
            if (log_filename):
                if log_filename[0] == '+':
                    fmode = 'a'
                    log_filename = log_filename[1:]
                else:
                    fmode = 'w'
                self._logFile = open(log_filename, fmode)
        except:
            self._logFile = None

    def __init__(self, level):
        self.__init(level)

    def __init__(self):
        lvl_name = get_env('MAS_PYLOG_LEVEL', 'WARN')
        lvl = self.levelInt(lvl_name)
        if lvl is None:
            lvl = self.WARN
        self.__init(lvl)

    def levelStr(self, i_level):
        try:
            val = self.lvlStr[i_level]
        except:
            val = None
        return val

    def levelInt(self, s_level):
        try:
            uc = s_level.upper()
            val = self.lvlInt[uc]
        except:
            val = None
        return val

    def log(self, level, *args, **kwargs):
        mas = True
        log = True
        for key, val in kwargs.items():
            key = key.lower()
            if key == 'mas':
                mas = str2b(val)
            elif key == 'log':
                log = str2b(val)
        msg_s = self._logPrefix
        for a in args:
            msg_s += str(a)
        if log and self._logFile:
            now = datetime.now()
            n = now.strftime('%Y-%m-%d %H:%M:%S') + '.' + str(now.microsecond)
            str_level = self.levelStr(level)
            self._logFile.write("    " + n + " " + str(str_level) + " " + msg_s + "\n")
            self._logFile.flush()
        if self._mas:
            ret_pack = self._mas.packReturnMsg(MASCmd_Logging, msg_s, level)
            self._mas.write(ret_pack)

    def all(self, *args, **kwargs):
        ml = self.ALL
        self.log(ml, *args, **kwargs)

    def trace(self, *args, **kwargs):
        ml = self.TRACE
        ll = self._logLevel
        if (ll == self.ALL) or (ml >= ll):
            self.log(ml, *args, **kwargs)

    def debug(self, *args, **kwargs):
        ml = self.DEBUG
        ll = self._logLevel
        if (ll == self.ALL) or (ml >= ll):
            self.log(ml, *args, **kwargs)

    def info(self, *args, **kwargs):
        ml = self.INFO
        ll = self._logLevel
        if (ll == self.ALL) or (ml >= ll):
            self.log(ml, *args, **kwargs)

    def warn(self, *args, **kwargs):
        ml = self.WARN
        ll = self._logLevel
        if (ll == self.ALL) or (ml >= ll):
            self.log(ml, *args, **kwargs)

    def error(self, *args, **kwargs):
        ml = self.ERROR
        ll = self._logLevel
        if (ll == self.ALL) or (ml >= ll):
            self.log(ml, *args, **kwargs)

    def fatal(self, *args, **kwargs):
        ml = self.FATAL
        ll = self._logLevel
        if (ll == self.ALL) or (ml >= ll):
            self.log(ml, *args, **kwargs)
