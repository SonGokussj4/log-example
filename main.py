# main.py
import sys
import logging

import cli
from utils.utils import multiply


# https://github.com/borntyping/python-colorlog


log = logging.getLogger(__name__)

# log = logging.getLogger(__name__)
def add(a, b):
    log.info(f"W Adding {a}+{b}={a+b}")
    log.info(f"W Adding {a}+{b}={a+b}")
    return a + b

def main():
    parser = cli.get_parser()
    args = parser.parse_args()
    print(f">>> args: {args}")

    # console = logging.StreamHandler(sys.stdout)
    # if args.v == 4:
    #     console.setLevel(logging.TRACE)
    #     fmt = ColorFormatter('[%(levelname)s]: %(message)s (%(filename)s:%(lineno)s)')
    # elif args.v == 3:
    #     console.setLevel(logging.DEBUG)
    #     fmt = ColorFormatter('[%(levelname)s]: %(message)s (%(filename)s:%(lineno)s)')
    # elif args.v == 2:
    #     console.setLevel(logging.INFO)
    #     fmt = ColorFormatter('[%(levelname)s]: %(message)s')
    # elif args.v == 1:
    #     console.setLevel(logging.WARNING)
    #     fmt = ColorFormatter('[%(levelname)s]: %(message)s')
    # else:
    #     console.setLevel(logging.ERROR)
    #     fmt = ColorFormatter('[%(levelname)s]: %(message)s')
    # console.setFormatter(fmt)
    # logging.getLogger().addHandler(console)  # add to root logger

    # log.info(f"E MAIN Log level: {logging.root.level}")

    add_result = add(2, 3)
    log.debug(f"D MAIN add_result: {add_result}")

    multiply_result = multiply(2, 3)
    log.info(f"I MAIN multiply_result: {multiply_result}")

if __name__ == '__main__':
    main()
