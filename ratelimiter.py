from pulsefire.ratelimiters import RiotAPIRateLimiter
import logging


logging.basicConfig(level=logging.DEBUG)


if __name__ == "__main__":
    RiotAPIRateLimiter().serve()
