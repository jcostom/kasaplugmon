#!/usr/bin/env python3

import asyncio
import logging
import os
from time import sleep
from kasa import SmartPlug

# --- To be passed in to container ---
# Mandatory vars
PLUG_IP = os.getenv('PLUG_IP')
TZ = os.getenv('TZ', 'America/New_York')
INTERVAL = os.getenv('INTERVAL', 300)

# Optional Vars
DEBUG = int(os.getenv('DEBUG', 0))

# Other Globals
VER = "0.3.3"
USER_AGENT = f"kasaplugmon/{VER}"

# Setup logger
LOG_LEVEL = 'DEBUG' if DEBUG else 'INFO'
logging.basicConfig(level=LOG_LEVEL,
                    format='[%(levelname)s] %(asctime)s %(message)s',
                    datefmt='[%d %b %Y %H:%M:%S %Z]')
logger = logging.getLogger()


async def is_plug_on(ip: str) -> bool:
    p = SmartPlug(ip)
    await p.update()
    is_it_on = p.is_on
    return is_it_on


async def plug_on(ip: str) -> None:
    p = SmartPlug(ip)
    await p.update()
    await p.turn_on()
    logger.info("Plug turned on.")


def main() -> None:
    logger.info(f"Initiated: {USER_AGENT}")
    while True:
        hey_is_this_thing_on = asyncio.run(is_plug_on(PLUG_IP))
        if hey_is_this_thing_on:
            DEBUG and logger.debug("Plug state was on.")
        else:
            logger.info("Plug state was off.")
            asyncio.run(plug_on(PLUG_IP))
        sleep(INTERVAL)


if __name__ == "__main__":
    main()
