import asyncio
import configparser
import logging
import argparse
import os.path
import typing

from smart_tv_telegram import Http, Mtproto, Config, Bot
from smart_tv_telegram.devices import FINDERS


def open_config(parser: argparse.ArgumentParser, arg: str) -> typing.Optional[Config]:
    if not os.path.exists(arg):
        parser.error(f"The file `{arg}` does not exist")

    elif not os.path.isfile(arg):
        parser.error(f"`{arg}` is not a file")

    try:
        return Config(arg)
    except ValueError as err:
        parser.error(str(err))
    except KeyError as err:
        parser.error(f"config key {str(err)} does not exists")
    except configparser.Error as err:
        parser.error(f"generic configparser error:\n{str(err)}")

    return None


async def async_main(config: Config):
    finders = [f() for f in FINDERS if f.is_enabled(config)]
    mtproto = Mtproto(config)
    http = Http(mtproto, config, finders)
    bot = Bot(mtproto, config, http, finders)
    http.set_on_stream_closed_handler(bot.get_on_stream_closed())
    bot.prepare()

    await mtproto.start()
    await http.start()


def main(config: Config):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_main(config))


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", type=lambda x: open_config(parser, x), default="config.ini")
    parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2], default=0)

    args = parser.parse_args()

    if args.verbosity == 0:
        logging.basicConfig(level=logging.ERROR)

    elif args.verbosity == 1:
        logging.basicConfig(level=logging.INFO)

    elif args.verbosity == 2:
        logging.basicConfig(level=logging.DEBUG)

    main(args.config)


if __name__ == "__main__":
    arg_parser()
