import os
import sys
import logging
import argparse
import importlib
# from utils.log import get_logger
import logging.config
# from logs import default_log_config

def get_parser(args=None):
    scriptname = os.path.basename(__file__)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument('-v', action='count', default=None, help='Verbal')

    parser = argparse.ArgumentParser(parents=[common])
    levels = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
    parser.add_argument('--log-level', default='INFO', choices=levels)
    subparsers = parser.add_subparsers(dest='command',
                                       help='Available commands:')
    start_cmd = subparsers.add_parser('start', help='Start a service')
    start_cmd.add_argument('name', metavar='NAME',
                           help='Name of service to start')
    stop_cmd = subparsers.add_parser('stop',
                                     help='Stop one or more services')
    stop_cmd.add_argument('names', metavar='NAME', nargs='+',
                          help='Name of service to stop')
    restart_cmd = subparsers.add_parser('restart',
                                        help='Restart one or more services')
    restart_cmd.add_argument('names', metavar='NAME', nargs='+',
                             help='Name of service to restart')
    options = parser.parse_args()
    # the code to dispatch commands could all be in this file. For the purposes
    # of illustration only, we implement each command in a separate module.
    # try:
    #     mod = importlib.import_module(options.command)
    #     cmd = getattr(mod, 'command')
    # except (ImportError, AttributeError):
    #     print('Unable to find the code for command \'%s\'' % options.command)
    #     return 1
    # Could get fancy here and load configuration from file or dictionary
    # cmd(options)
    # logging.config.dictConfig(
    #     {
    #         'version': 1,
    #         'disable_existing_loggers': False,
    #         'formatters': {
    #             'standard': {
    #                 'format': '%(asctime)s - [%(levelname)s] %(name)s [%(module)s.%(funcName)s:%(lineno)d]: %(message)s',
    #                 'datefmt': '%Y-%m-%d %H:%M:%S',
    #             }
    #         },
    #        'handlers' : {
    #             'default': {
    #                 'level': 'DEBUG',
    #                 'class': 'logging.StreamHandler',
    #                 'formatter': 'standard',
    #             }
    #        },
    #        'loggers': {
    #             # '__main__': { # logging from this module will be logged in VERBOSE level
    #             #     'handlers' : ['default'],
    #             #     'level': 'DEBUG',
    #             #     'propagate': False,
    #             # },
    #             # 'utils.utils': { # logging from this module will be logged in VERBOSE level
    #             #     'handlers' : ['default'],
    #             #     'level': 'INFO',
    #             #     'propagate': False,
    #             # },
    #        },
    #        'root': {
    #             'level': 'DEBUG',
    #             'handlers': ['default']
    #        },
    #     }
    # )
    return parser

if __name__ == '__main__':
    sys.exit(main())