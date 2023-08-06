import getpass
import json
from pathlib import Path


def login_args_configuration(sub_parser):
    login_parser = sub_parser.add_parser(
        name="login", help="login to deepchain")
    login_parser.set_defaults(func=login)


def login(_):
    path = Path.home().joinpath(".deep-chain").joinpath("config")
    data = {}
    with open(path, "w+") as config_file:
        try:
            data = json.load(config_file)
        except:
            pass
        data["pat"] = getpass.getpass("PAT:")
        json.dump(data, config_file)
