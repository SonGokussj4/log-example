# main.py
import sys
import logging
import logging.handlers
from utils.utils import multiply
import cli
import copy
# import coloredlogs
import colorama


from colorama import init, Fore, Back, Style
RCol = Style.RESET_ALL
Red, BRed = Fore.RED, Fore.RED + Style.BRIGHT
Blu, BBlu = Fore.BLUE, Fore.BLUE + Style.BRIGHT
Gre, BGre = Fore.GREEN, Fore.GREEN + Style.BRIGHT
Bla, LBla, BBla = Fore.BLACK, Fore.LIGHTBLACK_EX, Fore.BLACK + Style.BRIGHT
Whi, BWhi = Fore.WHITE, Fore.WHITE + Style.BRIGHT
Yel, BYel = Fore.YELLOW, Fore.YELLOW + Style.BRIGHT
Mag, BMag = Fore.MAGENTA, Fore.MAGENTA + Style.BRIGHT
Cya, BCya = Fore.CYAN, Fore.CYAN + Style.BRIGHT

# def addLogLevel(levelName, color, level, bold=True):
#     """
#     Add a new log level.

#     :param levelName: name for the new level
#     :param color:     related message color
#     :param level:     integer defining the level
#     :param bold:      whether the related messages should be displayed in bold
#     """
#     PY3 = sys.version[0] == "3"
#     n, N = levelName, levelName.upper()
#     if hasattr(logging, N):
#         raise ValueError("Cannot overwrite log level '{}'".format(n))
#     setattr(logging, N, level)
#     setattr(logging, N + "_COLOR", color)
#     logging.addLevelName(level, N)
#     def display(self, message, *args, **kwargs):
#         if self.isEnabledFor(level):
#             self._log(level, message, args, **kwargs)
#     display.__name__ = n
#     setattr(logging.Logger, n, display)
#     attrs = {'color': color}
#     if bold:
#         # compatibility fix due to a change in coloredlogs from version 14.0
#         # see: https://github.com/xolox/python-coloredlogs/issues/82
#         try:
#             attrs['bold'] = coloredlogs.CAN_USE_BOLD_FONT
#         except AttributeError:
#             # in coloredlogs from v14, CAN_USE_BOLD_FONT is not present anymore
#             #  and its flag is set to True everywhere it appears
#             attrs['bold'] = True
#     coloredlogs.DEFAULT_LEVEL_STYLES[n] = attrs
#     if PY3:
#         logging._levelToName[level] = N
#         logging._nameToLevel[N] = level
#     else:
#         logging._levelNames[level] = N
#     logging.addLogLevel = addLogLevel


# addLogLevel('success', 'green', 100, True)
# addLogLevel('ok', 'greeb', 31, True)
# addLogLevel('trace', 'red', 1, True)

LOG_COLORS = {
    # logging.TRACE: BBla,
    logging.DEBUG: Fore.LIGHTBLACK_EX,
    logging.INFO: Style.RESET_ALL,
    logging.WARNING: Fore.YELLOW,
    logging.ERROR: Fore.RED,
    logging.CRITICAL: Fore.RED + Style.BRIGHT,
    # logging.SUCCESS: BGre,
    # logging.OK: BGre,
}


class ColorFormatter(logging.Formatter):
    def format(self, record, *args, **kwargs):
        # if the corresponding logger has children, they may receive modified
        # record, so we want to keep it intact
        new_record = copy.copy(record)
        if new_record.levelno in LOG_COLORS:
            # we want levelname to be in different color, so let's modify it
            new_record.levelname = "{color_begin}{level: <8}{color_end}".format(
                level=new_record.levelname,
                color_begin=LOG_COLORS[new_record.levelno],
                color_end=colorama.Style.RESET_ALL,
            )
            new_record.lineno = "{color_begin}{lineno}{color_end}".format(
                lineno=new_record.lineno,
                color_begin=LOG_COLORS[new_record.levelno],
                color_end=colorama.Style.RESET_ALL,
            )
            if new_record.levelno == 10:  # DEBUG - Even MSG colored
                new_record.msg = "{color_begin}{msg}{color_end}".format(
                    msg=new_record.msg,
                    color_begin=LOG_COLORS[new_record.levelno],
                    color_end=colorama.Style.RESET_ALL,
                )
        # now we can let standart formatting take care of the rest
        return super(ColorFormatter, self).format(new_record, *args, **kwargs)


logging.getLogger().setLevel(logging.NOTSET)
log = logging.getLogger()
# logging.root.setLevel(logging.NOTSET)

# Specify FILE HANDLER
fhandler = logging.FileHandler('lol.log', 'w')
formatter = logging.Formatter(
    fmt='%(asctime)s - %(levelname)-8s | %(message)s [%(filename)s:%(funcName)s:%(lineno)s]',
    datefmt='%Y-%m-%d %H:%M:%S')
fhandler.setLevel(logging.NOTSET)
fhandler.setFormatter(formatter)
logging.root.addHandler(fhandler)

# Add file rotating handler, with level DEBUG
rotatingHandler = logging.handlers.RotatingFileHandler(filename='rotating.log', maxBytes=1000000, backupCount=5)
rotatingHandler.setLevel(logging.NOTSET)
formatter = logging.Formatter(
    fmt='%(asctime)s - %(levelname)-8s | %(message)s [%(filename)s:%(funcName)s:%(lineno)s]',
    datefmt='%Y-%m-%d %H:%M:%S')
rotatingHandler.setFormatter(formatter)
# logging.root.addHandler(fhandler)
logging.getLogger().addHandler(rotatingHandler)

# Add file rotating handler, with level DEBUG
timedRotatingHandler = logging.handlers.TimedRotatingFileHandler(filename='timedRotating.log', when='midnight', backupCount=10)
timedRotatingHandler.setLevel(logging.NOTSET)
formatter = logging.Formatter(
    fmt='%(asctime)s - %(levelname)-8s | %(message)s [%(filename)s:%(funcName)s:%(lineno)s]',
    datefmt='%Y-%m-%d %H:%M:%S')
timedRotatingHandler.setFormatter(formatter)
# logging.root.addHandler(fhandler)
logging.getLogger().addHandler(timedRotatingHandler)


def add(a, b):
    log.info(f"W Adding {a}+{b}={a+b}")
    return a + b


def main():
    parser = cli.get_parser()
    args = parser.parse_args()
    print(f">>> args: {args}")

    console = logging.StreamHandler(sys.stdout)
    if args.v == 4:
        console.setLevel(logging.TRACE)
        fmt = ColorFormatter('[%(levelname)s]: %(message)s (%(filename)s:%(lineno)s)')
    elif args.v == 3:
        console.setLevel(logging.DEBUG)
        fmt = ColorFormatter('[%(levelname)s]: %(message)s (%(filename)s:%(lineno)s)')
    elif args.v == 2:
        console.setLevel(logging.INFO)
        fmt = ColorFormatter('[%(levelname)s]: %(message)s')
    elif args.v == 1:
        console.setLevel(logging.WARNING)
        fmt = ColorFormatter('[%(levelname)s]: %(message)s')
    else:
        console.setLevel(logging.ERROR)
        fmt = ColorFormatter('[%(levelname)s]: %(message)s')
    console.setFormatter(fmt)
    logging.getLogger().addHandler(console)  # add to root logger

    # # Create STREAM HANDLER
    # console = logging.StreamHandler(sys.stdout)
    # console.setFormatter(fmt)
    # logging.getLogger().addHandler(console)  # add to root logger

    # log.trace(f"T MAIN Totally detailed message")
    log.info(f"E MAIN Log level: {logging.root.level}")

    add_result = add(2, 3)
    log.debug(f"D MAIN add_result: {add_result}")

    multiply_result = multiply(2, 3)
    log.info(f"I MAIN multiply_result: {multiply_result}")

    # log.success(f"S MAIN Successful message")
    # log.ok(f"O MAIN This opration was {BGre}[ OK ]{RCol}")


if __name__ == '__main__':
    main()
