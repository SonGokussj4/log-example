# main.py
import sys
import logging
from utils.utils import multiply
import cli
import coloredlogs
import colorama
LOG_COLORS = {
    logging.ERROR: colorama.Fore.RED,
    logging.WARNING: colorama.Fore.YELLOW
}
class ColorFormatter(logging.Formatter):
    def format(self, record, *args, **kwargs):
        # if the corresponding logger has children, they may receive modified
        # record, so we want to keep it intact
        new_record = copy.copy(record)
        if new_record.levelno in LOG_COLORS:
            # we want levelname to be in different color, so let's modify it
            new_record.levelname = "{color_begin}{level}{color_end}".format(
                level=new_record.levelname,
                color_begin=LOG_COLORS[new_record.levelno],
                color_end=colorama.Style.RESET_ALL,
            )
        # now we can let standart formatting take care of the rest
        return super(ColorFormatter, self).format(new_record, *args, **kwargs)


# log = get_logger(__name__)
log = logging.getLogger(__name__)
fh = logging.FileHandler('lol.log', 'w')
logging.root.setLevel(logging.NOTSET)
fh.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(levelname)-8s | %(message)s (%(filename)s:%(lineno)s)')
formatter = logging.Formatter('%(asctime)s [%(levelname)-8s]: %(message)-150s [%(filename)s:%(funcName)s:%(lineno)d]')
# formatter = ColorFormatter('[%(levelname)-8s]: %(message)-150s')
fh.setFormatter(formatter)
logging.root.addHandler(fh)


from colorama import init, Fore, Back, Style
RCol = Style.RESET_ALL
Red, BRed = Fore.RED, f'{Fore.RED}{Style.BRIGHT}'
Blu, BBlu = Fore.BLUE, f'{Fore.BLUE}{Style.BRIGHT}'
Gre, BGre = Fore.GREEN, f'{Fore.GREEN}{Style.BRIGHT}'
Bla, BBla = Fore.BLACK, f'{Fore.BLACK}{Style.BRIGHT}'
Whi, BWhi = Fore.WHITE, f'{Fore.WHITE}{Style.BRIGHT}'
Yel, BYel = Fore.YELLOW, f'{Fore.YELLOW}{Style.BRIGHT}'
Mag, BMag = Fore.MAGENTA, f'{Fore.MAGENTA}{Style.BRIGHT}'
Cya, BCya = Fore.CYAN, f'{Fore.CYAN}{Style.BRIGHT}'


# from logging.config import dictConfig
# dictConfig({
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'standard': {
#             'format': '%(asctime)s - [%(levelname)s] %(name)s [%(module)s.%(funcName)s:%(lineno)d]: %(message)s',
#             'datefmt': '%Y-%m-%d %H:%M:%S',
#         }
#     },
#    'handlers' : {
#         'default': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'standard',
#         }
#    },
#    'loggers': {
#         # '__main__': { # logging from this module will be logged in VERBOSE level
#         #     'handlers' : ['default'],
#         #     'level': 'DEBUG',
#         #     'propagate': False,
#         # },
#         # 'utils.utils': { # logging from this module will be logged in VERBOSE level
#         #     'handlers' : ['default'],
#         #     'level': 'INFO',
#         #     'propagate': False,
#         # },
#    },
#    'root': {
#         'level': 'DEBUG',
#         'handlers': ['default']
#    },
# })


def addLogLevel(levelName, color, level, bold=True):
    """
    Add a new log level.

    :param levelName: name for the new level
    :param color:     related message color
    :param level:     integer defining the level
    :param bold:      whether the related messages should be displayed in bold
    """
    PY3 = sys.version[0] == "3"
    n, N = levelName, levelName.upper()
    if hasattr(logging, N):
        raise ValueError("Cannot overwrite log level '{}'".format(n))
    setattr(logging, N, level)
    setattr(logging, N + "_COLOR", color)
    logging.addLevelName(level, N)
    def display(self, message, *args, **kwargs):
        if self.isEnabledFor(level):
            self._log(level, message, args, **kwargs)
    display.__name__ = n
    setattr(logging.Logger, n, display)
    attrs = {'color': color}
    if bold:
        # compatibility fix due to a change in coloredlogs from version 14.0
        # see: https://github.com/xolox/python-coloredlogs/issues/82
        try:
            attrs['bold'] = coloredlogs.CAN_USE_BOLD_FONT
        except AttributeError:
            # in coloredlogs from v14, CAN_USE_BOLD_FONT is not present anymore
            #  and its flag is set to True everywhere it appears
            attrs['bold'] = True
    coloredlogs.DEFAULT_LEVEL_STYLES[n] = attrs
    if PY3:
        logging._levelToName[level] = N
        logging._nameToLevel[N] = level
    else:
        logging._levelNames[level] = N
    logging.addLogLevel = addLogLevel



def add(a, b):
    log.warning(f"W Adding {a}+{b}={a+b}")
    return a + b

def main():
    parser = cli.get_parser()
    args = parser.parse_args()
    print(f">>> args: {args}")
    addLogLevel('success', 'green', 100, True)
    level_styles = {
        'critical': {'bold': True, 'color': 'red'},
        'debug': {'bold': True, 'color': 'black'},
        'error': {'color': 'red'},
        'info': {},
        'notice': {'color': 'magenta'},
        'spam': {'color': 'green', 'faint': True},
        'success': {'bold': True, 'color': 'green'},
        'verbose': {'color': 'blue'},
        'warning': {'color': 'yellow'}
    }
    field_styles = {
        'asctime': {'color': 'green'},
        'hostname': {'color': 'magenta'},
        'levelname': {'bold': True, 'color': 'black'},
        'name': {'color': 'blue'},
        'programname': {'color': 'cyan'},
        'username': {'color': 'yellow'}
    }

    if args.v == 3:
        # logging.root.setLevel(logging.DEBUG)
        coloredlogs.install(
            level='DEBUG',
            fmt="%(levelname)-8s | %(message)s (%(filename)s:%(lineno)s)",
            level_styles=level_styles, field_styles=field_styles)
    elif args.v == 2:
        # logging.root.setLevel(logging.INFO)
        coloredlogs.install(
            level='INFO',
            fmt="%(levelname)-8s | %(message)s",
            level_styles=level_styles, field_styles=field_styles)
    elif args.v == 1:
        # logging.root.setLevel(logging.WARNING)
        coloredlogs.install(
            level='WARNING',
            fmt="%(levelname)-8s | %(message)s",
            level_styles=level_styles, field_styles=field_styles)
    else:
        # logging.root.setLevel(logging.ERROR)
        coloredlogs.install(
            level='ERROR',
            fmt="%(levelname)-8s | %(message)s",
            level_styles=level_styles, field_styles=field_styles)

    log.error(f"E MAIN Log level: {logging.root.level}")
    add_result = add(2, 3)
    log.debug(f"D MAIN add_result: {add_result}")
    multiply_result = multiply(2, 3)
    log.info(f"I MAIN multiply_result: {multiply_result}")
    # log.success(f"A co je toto :D")

if __name__ == '__main__':
    main()
