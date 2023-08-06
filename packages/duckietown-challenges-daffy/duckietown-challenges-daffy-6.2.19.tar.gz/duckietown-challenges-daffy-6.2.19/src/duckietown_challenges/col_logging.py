# coding=utf-8
import logging

import termcolor

__all__ = ["setup_logging_color", "setup_logging_format", "setup_logging"]


def get_FORMAT_datefmt():
    pre = "%(asctime)s|d|%(name)s|%(filename)s:%(lineno)s|%(funcName)s():\n"
    pre = termcolor.colored(pre, attrs=["dark"])
    FORMAT = pre + "%(message)s"
    datefmt = "%H:%M:%S"
    return FORMAT, datefmt


# noinspection PyUnresolvedReferences
def setup_logging_format():
    from logging import Logger, StreamHandler, Formatter
    import logging

    FORMAT, datefmt = get_FORMAT_datefmt()
    logging.basicConfig(format=FORMAT, datefmt=datefmt)

    root = Logger.root
    if root.handlers:
        for handler in root.handlers:
            if isinstance(handler, StreamHandler):
                formatter = Formatter(FORMAT, datefmt=datefmt)
                handler.setFormatter(formatter)
    else:
        logging.basicConfig(format=FORMAT, datefmt=datefmt)


def add_coloring_to_emit_ansi(fn):
    # add methods we need to the class
    def new(*args):
        levelno = args[1].levelno
        if levelno >= 50:
            color = "\x1b[31m"  # red
        elif levelno >= 40:
            color = "\x1b[31m"  # red
        elif levelno >= 30:
            color = "\x1b[33m"  # yellow
        elif levelno >= 20:
            color = "\x1b[32m"  # green
        elif levelno >= 10:
            color = "\x1b[35m"  # pink
        else:
            color = "\x1b[0m"  # normal

        msg = str(args[1].msg)

        lines = msg.split("\n")

        def color_line(l):
            return "%s%s%s" % (color, l, "\x1b[0m")  # normal

        lines = list(map(color_line, lines))

        args[1].msg = "\n".join(lines)
        return fn(*args)

    return new


def setup_logging_color():
    import platform

    if platform.system() != "Windows":
        emit2 = add_coloring_to_emit_ansi(logging.StreamHandler.emit)
        logging.StreamHandler.emit = emit2


def setup_logging():
    # logging.basicConfig()
    setup_logging_color()
    setup_logging_format()
