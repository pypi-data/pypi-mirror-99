# -*- coding: utf-8 -*-

import os
import os.path
import inspect
import json

from pathlib import Path

import argparse
import configparser

class Config:

    def __init__(self, argparser = None):
        self.argparser = argparser if argparser is not None else argparse.ArgumentParser()
        self.parser = configparser.ConfigParser()
        self.err = []
        
    def parse(self, config_path = None):
        self.args = self.argparser.parse_args()
        self.args_dict = {v[0]:v[1] for v in inspect.getmembers(self.args) if not (callable(v[0]) or v[0].startswith('_'))}
        self.config_path = []
        
        if hasattr(self.args, 'config') and self.args.config:
            for p in self.args.config.split(os.pathsep):
                self.config_path.append(p.format(**self.args_dict))

        if hasattr(self.args, 'current_dir') and self.args.current_dir:
            if self.args.current_dir != '.':
                os.chdir(self.args.current_dir)

        if config_path:
            if type(config_path) != str and hasattr(config_path, '__iter__'):
                for p in config_path:
                    self.config_path.append(p.format(**self.args_dict))
            else:
                self.config_path.append(config_path)

        lp = configparser.ConfigParser()
        for p in reversed(self.config_path):
            if os.path.exists(p):
                try:
                    with open(p, "r") as f:
                        lp.read_file(f)
                except Exception as e:
                    pass
            else:
                pass
        if lp.has_section('ifconf'):
            for path in [v[1] for v in sorted(lp['ifconf'].items(), key=lambda x: x[0]) if v[0].startswith('config_path')]:
                if path not in self.config_path:
                    self.config_path.append(path)
                
        for p in reversed(self.config_path):
            if os.path.exists(p):
                try:
                    with open(p, "r") as f:
                        self.parser.read_file(f)
                except Exception as e:
                    self.err.append('Failed to load configuration file(s) [{}]. Error: {}'.format(p, e))
            else:
                self.err.append('Configuration file(s) [{}] are not found.'.format(p))

    def get_attr(self, section, option, default='', required=False):
        if required or self.parser.has_option(section, option):
            return self.parser.get(section, option)
        else:
            return default

    def get_attr_boolean(self, section, option, default=False, required=False):
        if required or self.parser.has_option(section, option):
            return self.parser.getboolean(section, option)
        else:
            return default
        
    def get_attr_int(self, section, option, default=0, required=False):
        if required or self.parser.has_option(section, option):
            return self.parser.getint(section, option)
        else:
            return default

    def get_attr_float(self, section, option, default=0.0, required=False):
        if required or self.parser.has_option(section, option):
            return self.parser.getfloat(section, option)
        else:
            return default

    def get_attr_dict(self, section, option, default={}, required=False):
        return self.get_attr_json(section, option, default, required)
        
    def get_attr_list(self, section, option, default=[], required=False):
        return self.get_attr_json(section, option, default, required)
        
    def get_attr_json(self, section, option, default, required):
            if required or self.parser.has_option(section, option):
                value_string = self.parser.get(section, option)
                try:
                    return json.loads(value_string)
                except Exception as e:
                    raise ValueError('Invalid Data Format [{}]. [{}][{}][{}]'.format(e, section, option, value_string), e)
            else:
                return default

    def get_attr_path(self, section, option, default, required):
        if required or self.parser.has_option(section, option):
            return Path(self.parser.get(section, option))
        else:
            return default if type(default) == Path else Path(default)
        
