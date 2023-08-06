import configparser
import json
import os
import shutil
from pathlib import Path

import requests
from deepchainapps import log


def deploy_args_configuration(sub_parser):
    login_parser = sub_parser.add_parser(
        name="deploy", help="deploy your app to deepchain")
    login_parser.add_argument("app_name", action="store", help="app name")
    login_parser.add_argument("--checkpoints", action="store")
    login_parser.set_defaults(func=deploy)


def deploy(args):
    config = configparser.ConfigParser()
    config.read('config.ini')
    url = config['APP']['DEEP_CHAIN_URL']
    pat = get_pat()
    r = upload_code(args, pat, url)

    if r.status_code != 200:
        log.warning(f'api return {r.status_code} stopping operation')
        return

    if args.checkpoints is None:
        return
    upload_checkpoint(args, pat, url)


def upload_code(args, pat, url):
    archive = shutil.make_archive(args.app_name, "zip", args.app_name)
    r = requests.post(url=url + args.app_name,
                      headers={'authorisation': pat},
                      files={"code": ("code.zip", open(archive, "rb"))})
    os.remove(archive)
    return r


def get_pat() -> str:
    path = Path.home().joinpath(".deep-chain").joinpath("config")
    with open(path, "r") as config_file:
        data = json.load(config_file)
    return data["pat"]


def upload_checkpoint(args, pat, url):
    signed_url = get_object_storage_url(args, pat, url)

    archive = shutil.make_archive(
        args.checkpoints, "zip", ".", args.checkpoints)
    requests.put(signed_url, files={f"checkpoints": (
        "checkpoints.zip", open(archive, "rb"))})
    os.remove(archive)


def get_object_storage_url(args, pat, url):
    r = requests.post(url=url + args.app_name + "/checkpointUrl",
                      headers={'authorisation': pat})
    signed_url = r.json()
    return signed_url
