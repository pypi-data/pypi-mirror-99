import glob
import shutil
import tempfile
from typing import Dict

import requests
from deepchainapps import log


def create_base_app(args):
    log.info("download base app")
    latest_release = fetch_latest_version()
    temp_dir = tempfile.mkdtemp()
    download_latest_version(latest_release, temp_dir)
    unpack_base_repository(args, latest_release, temp_dir)
    shutil.rmtree(temp_dir)


def fetch_latest_version() -> Dict:
    url = "https://api.github.com/repos/mmbeyrem/nothingTodoapps/releases"
    #url = "https://api.github.com/repos/instadeepai/deep-chain-apps/releases"
    r = requests.get(url)
    releases = r.json()
    latest_release = sorted(
        releases, key=lambda k: k['published_at'], reverse=True)[0]
    return latest_release


def download_latest_version(latest_release: Dict,
                            temp_dir: str):
    log.info(f'downloading release  from : {latest_release["tarball_url"]}')
    r = requests.get(latest_release['tarball_url'])
    with open(f"{temp_dir}/{latest_release['tag_name']}.tar", 'wb') as f:
        f.write(r.content)


def unpack_base_repository(args,
                           latest_release: Dict,
                           temp_dir: str):

    shutil.unpack_archive(f"{temp_dir}/{latest_release['tag_name']}.tar",
                          f"{temp_dir}/{latest_release['tag_name']}")
    for file in glob.glob(rf"{temp_dir}/{latest_release['tag_name']}/*/**", recursive=True):
        shutil.copytree(file, args.app_name)
        break


def scaffold_args_configuration(sub_parser):
    scaffold_parser = sub_parser.add_parser(
        name="create", help="scaffold new scorer app")
    scaffold_parser.add_argument(
        "app_name", action="store", help="this will be the app name in deep-chain")
    scaffold_parser.set_defaults(func=create_base_app)
