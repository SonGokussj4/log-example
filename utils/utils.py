# utils.py
import logging
log = logging.getLogger(__name__)

def multiply(a, b):
    log.debug(f"D UTILS Multiplying {a}*{b}={a*b}")
    log.info(f"I UTILS Multiplying {a}*{b}={a*b}")
    log.warning(f"W UTILS Multiplying {a}*{b}={a*b}")
    log.error(f"E UTILS Multiplying {a}*{b}={a*b}")
    log.critical(f"C UTILS Multiplying {a}*{b}={a*b}")
    log.success(f"S UTILS Multiplying {a}*{b}={a*b}")
    return a * b
