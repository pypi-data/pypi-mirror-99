"""
Copyright © 2017-present, Encode OSS Ltd. All rights reserved.

Original Code:
    https://github.com/encode/uvicorn/blob/master/uvicorn/logging.py
"""

import logging
import sys
from copy import copy

import click

TRACE_LOG_LEVEL = 5


class ColourizedFormatter(logging.Formatter):
    """
    A custom log formatter class that:

    * Outputs the LOG_LEVEL with an appropriate color.
    * If a log call includes an `extras={"color_message": ...}` it will be used
      for formatting the output, instead of the plain text message.
    """

    level_name_colors = {
        TRACE_LOG_LEVEL: lambda level_name: click.style(
            str(level_name), fg="blue"
        ),
        logging.DEBUG: lambda level_name: click.style(
            str(level_name), fg="cyan"
        ),
        logging.INFO: lambda level_name: click.style(
            str(level_name), fg="green"
        ),
        logging.WARNING: lambda level_name: click.style(
            str(level_name), fg="yellow"
        ),
        logging.ERROR: lambda level_name: click.style(
            str(level_name), fg="red"
        ),
        logging.CRITICAL: lambda level_name: click.style(
            str(level_name), fg="bright_red"
        ),
    }

    def __init__(self, fmt=None, datefmt=None, style="%", use_colors=None):
        if use_colors in (True, False):
            self.use_colors = use_colors
        else:
            self.use_colors = sys.stdout.isatty()
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)

    def color_level_name(self, level_name, level_no):
        def default(level_name):
            return str(level_name)

        func = self.level_name_colors.get(level_no, default)
        return func(level_name)

    def should_use_colors(self):
        return True

    def formatMessage(self, record):
        recordcopy = copy(record)
        levelname = recordcopy.levelname
        seperator = " " * (8 - len(recordcopy.levelname))
        if self.use_colors:
            levelname = self.color_level_name(levelname, recordcopy.levelno)
            if "color_message" in recordcopy.__dict__:
                recordcopy.msg = recordcopy.__dict__["color_message"]
                recordcopy.__dict__["message"] = recordcopy.getMessage()
        recordcopy.__dict__["levelprefix"] = levelname + ":" + seperator
        return super().formatMessage(recordcopy)


class DefaultFormatter(ColourizedFormatter):
    def should_use_colors(self):
        return sys.stderr.isatty()
