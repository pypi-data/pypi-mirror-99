# -*- coding: utf-8 -*-

import logging
import logging.config
from logging.handlers import RotatingFileHandler

logging.NOTICE = 25
logging.NOTICE_LEVEL_NAME = "NOTICE"

logging.addLevelName(logging.NOTICE, logging.NOTICE_LEVEL_NAME)

def notice(self, message, *args, **kws):
    self._log(logging.NOTICE, message, args, **kws)
    
logging.Logger.notice = notice



def configure_logging(conf
                      , log_level=logging.INFO
                      , log_file=""
                      , log_max_bytes = 1024*1024*16
                      , log_backup_count = 99
                      , log_encoding = 'UTF-8'
                      , fmt = '%(asctime)s [%(name)s] [%(levelname)s] %(message)s'):
    conf.verbose = conf.args.verbose if hasattr(conf.args, 'verbose') else False
    conf.log_level = log_level
    conf.log_level_name = logging.getLevelName(log_level)
    conf.log_file = log_file
    conf.log_max_bytes = log_max_bytes
    conf.log_backup_count = log_backup_count
    conf.log_encoding = log_encoding
    conf.formatter = logging.Formatter(fmt)

    if [s for s in ('loggers', 'handlers', 'formatters') if conf.parser.has_section(s)]:
        logging.config.fileConfig(conf.parser, disable_existing_loggers=False)
        conf.logger = logging.getLogger()
    elif conf.parser.has_option('ifconf', 'logging') and conf.parser.getboolean('ifconf', 'logging'):
        logging.config.dictConfig({'version': 1, 'disable_existing_loggers' : False})
        section = conf.parser['ifconf']
        conf.verbose = section.get('verbose', conf.verbose)
        conf.log_level_name = section.get('log_level', 'INFO')
        conf.log_level = getattr(logging, conf.log_level_name.upper(), conf.log_level)
        conf.log_file = section.get('log_file', conf.log_file)
        conf.err_file = section.get('err_file', '')
        conf.log_encoding = section.get('log_encoding', conf.log_encoding)
        bytes_str = section.get("log_max_bytes", '').replace('(','').replace(')','').replace('=','')
        conf.log_max_bytes = eval(bytes_str) if bytes_str else conf.log_max_bytes
        conf.log_backup_count = int(section.get('log_backup_count', conf.log_backup_count))
        conf.logger = load_logging(conf)
    else:
        conf.logger = load_logging(conf)


def load_logging(conf, name=None):
    if name:
        logger = logging.getLogger(name)
    else:
        logger = logging.getLogger()
    logger.setLevel(conf.log_level)


    if hasattr(conf, 'debug') and conf.debug:
        handler = logging.StreamHandler()
        handler.setFormatter(conf.formatter)
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
            
    if hasattr(conf, 'debug_file') and conf.debug_file:
        try:
            handler = FileHandler(conf.debug_file, encoding = conf.log_encoding)
            handler.setFormatter(conf.formatter)
            handler.setLevel(logging.DEBUG)
            logger.addHandler(handler)
            logger.setLevel(logging.DEBUG)
        except Exception as e:
            conf.err.append('Failed to set DEBUG file. File: [{}] Error: [{}]'.format(conf.debug_file, e))
    if hasattr(conf, 'log_file') and conf.log_file:
        try:
            #handler = RotatingFileHandler(conf.log_file, maxBytes = conf.log_max_bytes, backupCount = conf.log_backup_count, encoding = conf.log_encoding)
            handler = FileHandler(conf.log_file, encoding = conf.log_encoding)
            handler.setFormatter(conf.formatter)
            logger.addHandler(handler)
        except Exception as e:
            conf.err.append('Failed to set LOG file. File: [{}] Error: [{}]'.format(conf.log_file, e))
    if hasattr(conf, 'err_file') and conf.err_file and conf.err_file != conf.log_file:
        try:
            #handler = RotatingFileHandler(conf.err_file, maxBytes = conf.log_max_bytes, backupCount = conf.log_backup_count, encoding = conf.log_encoding)
            handler = FileHandler(conf.err_file, encoding = conf.log_encoding)
            handler.setFormatter(conf.formatter)
            handler.setLevel(logging.ERROR)
            logger.addHandler(handler)
        except Exception as e:
            conf.err.append('Failed to set ERROR file. File: [{}] Error: [{}]'.format(conf.err_file, e))
    if len(logger.handlers) == 0:
        handler = logging.StreamHandler()
        handler.setFormatter(conf.formatter)
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        logger.warning("Set output logging as stderr output.")
        
    if conf.verbose:
        logger.setLevel(logging.DEBUG)

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("Enabled DEBUG mode.")
    elif logger.isEnabledFor(logging.INFO):
        logger.info("Enabled logging. Printing INFO logs.")
    elif logger.isEnabledFor(logging.NOTICE):
        logger.notice("Enabled logging. Printing NOTICE logs.")
    elif logger.isEnabledFor(logging.WARN):
        logger.warning("Enabled logging. Printing WARNING logs.")
        
    return logger


