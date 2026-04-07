import json
import sys
import time
from functools import partial
from threading import Thread
from typing import Callable
from pydantic import BaseModel

from TwitchChannelPointsMiner import TwitchChannelPointsMiner


class Config(BaseModel):
    usernames: list[str] = []
    streamers: list[str] = []



def loadConfig() -> Config:
    try:
        with open("config.json", "r") as file:
            config = json.load(file)

    except FileNotFoundError:
        print("No config.json file found!")
        sys.exit(1)

    return Config(**config)


def mine(minerFactory: Callable[[], partial[TwitchChannelPointsMiner]]):
    config = loadConfig()

    threads: list[Thread] = []

    for username in config.usernames:
        miner = minerFactory()(username=username, password="")

        threads.append(
            Thread(
                target=partial(miner.mine, streamers=config.streamers),
                daemon=True
            )
        )

    for thread in threads:
        thread.start()

    time.sleep(100_000_000)