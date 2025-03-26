#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import logging.handlers
import os
import time
import inspect
import yaml

LOG_DIR = "log"
global VERBOSE
VERBOSE = 5
global TEST
TEST = 45

levels = [('CRITICAL' , logging.CRITICAL),
          ('ERROR' , logging.ERROR),
          ('WARNING' , logging.WARNING),
          ('INFO' , logging.INFO),
          ('DEBUG' , logging.DEBUG),
          ('VERBOSE' , VERBOSE)]


logging.captureWarnings(True)
logging.getLogger("py.warnings").setLevel(logging.ERROR)


def get_default_config_filename():
    """ Determine the filename and path to the logging configuration file. """
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), 'logging.yaml'))


def configure_logging(config_file=None):
    """ Configure MRSv logging. Fall back to defaults if there's an error."""
    cfg_filename = config_file if config_file else get_default_config_filename()
    try:
        with open(cfg_filename, "r", encoding="utf-8") as logcfg:
            cfg = yaml.load(logcfg, Loader=yaml.FullLoader)
        logging.config.dictConfig(cfg)
        logging.debug("Logging configuration loaded from %s", cfg_filename)
    except Exception:
        logging.basicConfig(level=logging.INFO)
        logging.info(
            "Could not load logging configuration from '%s'; using defaults.",
            cfg_filename)
        logging.exception("Exception when loading logging configuration:")
    logging.info('PID=%d', os.getpid())


def get_logger(module_name, obj=None):
    """
    Proxies to logging.getLogger to get a logger object.
    The name of the logger is constructed based on the module name, and the
    optional object's class.
    If the functionality of --verbose is needed, this can transform all logger
    objects to be verbose before returning them.
    """
    postfix = str.format(".{0.__class__.__name__}", obj) if obj else ''
    logger_name = str.format('{}{}', module_name, postfix)
    return logging.getLogger(logger_name)


def start_file_logging(file_name, log_file_path):
    """
    Starts logging to a specific file.
    """
    if not os.path.exists(log_file_path):
        os.makedirs(log_file_path)
    logfile = f"{log_file_path}/{file_name}.log"
    master_log = logging.getLogger('')
    master_log.setLevel(VERBOSE)
    master_handler = logging.FileHandler(logfile)
    formatter = logging.Formatter('%(asctime)s %(name)-35s %(levelname)-8s %(message)s')
    master_handler.setFormatter(formatter)
    logging.getLogger('').addHandler(master_handler)
    add_custom_log_level()


def start_console_logging(loglevel=3):
    """
    Starts logging to the console.
    """
    master_log = logging.getLogger('')
    master_log.setLevel(VERBOSE)
    console = logging.StreamHandler()
    console.setLevel(levels[loglevel][1])
    formatter = logging.Formatter("%(name)-35s: %(levelname)-8s %(message)s")
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logger = logging.getLogger(os.path.basename(__file__))
    logger.debug("Logging configuration: Console[%s]", levels[loglevel][0])
    add_custom_log_level()


def stop_file_logging(file_name):
    """
    Stop logging to the file file_name, by
    removing the filehandler.
    """
    for handler in logging.root.handlers[:]:
        if isinstance(handler, logging.FileHandler ):
            if os.path.basename(handler.baseFilename) == file_name:
                logging.root.removeHandler(handler)
                return


def stop_logging():
    """
    Stop all logging, by removing all handlers
    """
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)


def start_logging(
        log_file_path=LOG_DIR, debug=True, loglevel=3,
        log_file_name="", module_name=None, rotating=False
):
    """
    Start logging
    """
    if loglevel < 0 or loglevel > 5 :
        loglevel = 4
    if log_file_path != "":
        if not os.path.exists(log_file_path):
            os.makedirs(log_file_path)
        if not log_file_name:
            log_file_name = get_caller_name()
        if not rotating:
            str_time = time.strftime(r"%Y-%m-%d_%H%M%S", time.gmtime())
            logfile = f"{log_file_path}{os.sep}{log_file_name}_{str_time}.log"
            # set up logging to file
            logging.basicConfig(level=VERBOSE,
                                format='%(asctime)s %(name)-35s %(levelname)-8s %(message)s',
                                datefmt='%m-%d %H:%M',
                                filename=logfile,
                                filemode='w')
        else:
            master_log = logging.getLogger('')
            master_log.setLevel(VERBOSE)
            logfile = f"{log_file_path}{os.sep}{log_file_name}.log"
            master_handler = logging.handlers.RotatingFileHandler(logfile,
                                            maxBytes=10000000, backupCount=3)
            formatter = logging.Formatter('%(asctime)s %(name)-35s %(levelname)-8s %(message)s')
            master_handler.setFormatter(formatter)
            logging.getLogger('').addHandler(master_handler)
    add_custom_log_level()
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(levels[loglevel][1])
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-35s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)
    if module_name:
        logger = logging.getLogger(module_name)
    else:
        logger = logging.getLogger(os.path.basename(__file__))
    logger.info(
        "Logging configuration: Console[%s] File[VERBOSE] Logfile[%s]",
        levels[loglevel][0],
        logfile
    )


def get_console_loglevel():
    """
    Get the current loglevel in console.
    """
    for handler in logging.root.handlers[:]:
        if isinstance(handler, logging.FileHandler ):
            continue
        if isinstance(handler, logging.handlers.SocketHandler):
            continue
        configured_level = handler.level
        index = 0
        for level in levels:
            if level[1] == configured_level:
                return index
            index +=1
    return configured_level


def change_loglevel(loglevel, module_name=None):
    """
    Change the loglevel in console.
    Stop all console logging and then start it again with the new loglevel.
    Logging to file and via tcp is kept.
    """
    for handler in logging.root.handlers[:]:
        if isinstance(handler, logging.FileHandler ): # dont change filelogging
            continue
        elif isinstance(handler, logging.handlers.SocketHandler): # dont change streamlogging
            continue
        else:
            logging.root.removeHandler(handler)
    console = logging.StreamHandler()
    console.setLevel(levels[loglevel][1])
    formatter = logging.Formatter('%(name)-35s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)
    if module_name:
        logger = logging.getLogger(module_name)
    else:
        logger = logging.getLogger(os.path.basename(__file__))
    logger.debug("Changing console loglevel to %s", levels[loglevel][0])


def add_custom_log_level():
    """
    Adds new custom loglevels VERBOSE and TEST.
    """
    logging.addLevelName(VERBOSE, "VERBOSE")
    logging.Logger.verbose = \
        lambda inst, msg, *args, **kwargs: inst.log(VERBOSE, msg, *args, **kwargs)
    logging.addLevelName(TEST, "TEST")
    logging.Logger.test = \
        lambda inst, msg, *args, **kwargs: inst.log(TEST, msg, *args, **kwargs)


def get_caller_name():
    """
    Returns the filename of the calling module.
    """
    _, filename, _, _, _, _ = inspect.getouterframes(inspect.currentframe())[2]
    log_file_name = os.path.splitext(os.path.basename(filename))[0]
    return log_file_name
