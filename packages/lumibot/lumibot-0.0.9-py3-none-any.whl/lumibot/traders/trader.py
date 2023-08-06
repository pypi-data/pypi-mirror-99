import logging
import os
import signal
from concurrent.futures import ThreadPoolExecutor, as_completed


class Trader:
    def __init__(self, logfile="logs/test.log", debug=False, strategies=None):
        # Setting debug and _logfile parameters and setting global log format
        self.debug = debug
        self.log_format = logging.Formatter("%(asctime)s: %(levelname)s: %(message)s")
        self.logfile = logfile

        # Setting the list of strategies if defined
        self._strategies = strategies if strategies else []
        self._pool = []

    @property
    def is_backtest(self):
        result = False
        if any([s.broker.IS_BACKTESTING_BROKER for s in self._strategies]):
            result = True
        return result

    def add_strategy(self, strategy):
        """Adds a strategy to the trader"""
        self._strategies.append(strategy)

    def run_all(self):
        """run all strategies"""
        if self.is_backtest:
            if len(self._strategies) > 1:
                raise Exception(
                    "Received %d strategies for backtesting."
                    "You can backtest only once at a time." % len(self._strategies)
                )

            logging.info("Backtesting starting...")

        signal.signal(signal.SIGINT, self._stop_pool)
        self._set_logger()
        self._init_pool()
        self._start_pool()
        self._join_pool()
        result = self._collect_analysis()
        return result

    def _set_logger(self):
        """Setting Logging to both console and a file if logfile is specified"""
        logging.getLogger("urllib3").setLevel(logging.ERROR)
        logging.getLogger("requests").setLevel(logging.ERROR)

        logger = logging.getLogger()
        if not logger.handlers:
            logger.addHandler(logging.StreamHandler())
        if self.debug:
            logger.setLevel(logging.DEBUG)
        elif self.is_backtest:
            logger.setLevel(logging.ERROR)
        else:
            logger.setLevel(logging.INFO)

        # Setting file logging
        if self.logfile:
            dir = os.path.dirname(os.path.abspath(self.logfile))
            if not os.path.exists(dir):
                os.mkdir(dir)
            fileHandler = logging.FileHandler(self.logfile, mode="w")
            logger.addHandler(fileHandler)

        for handler in logger.handlers:
            handler.setFormatter(self.log_format)

        logger.propagate = True

    def _init_pool(self):
        self._pool = [strategy._executor for strategy in self._strategies]

    def _start_pool(self):
        for strategy_thread in self._pool:
            strategy_thread.start()

    def _join_pool(self):
        for strategy_thread in self._pool:
            strategy_thread.join()

    def _stop_pool(self, sig, frame):
        """Run all strategies on_abrupt_closing
        lifecycle method. python signal handlers
        needs two positional arguments, the signal
        and the frame"""
        logging.debug("Received signal number %d." % sig)
        logging.debug("Closing Trader in %s frame." % frame)
        for strategy_thread in self._pool:
            strategy_thread.stop()
        logging.info("Trading finished")

    def _collect_analysis(self):
        result = {}
        for strategy_thread in self._pool:
            result[strategy_thread.name] = strategy_thread.result
        return result
