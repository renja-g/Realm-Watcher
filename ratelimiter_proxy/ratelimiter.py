from pulsefire.ratelimiters import RiotAPIRateLimiter
import logging
import sys


logging.basicConfig(
    level=logging.DEBUG,
    handlers=[
        logging.StreamHandler(stream=sys.stdout)
    ]
)



if __name__ == "__main__":
    RiotAPIRateLimiter().serve(host="0.0.0.0", port=12227)
