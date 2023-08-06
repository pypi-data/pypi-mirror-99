from typing import List

from setuptools import find_packages, setup

from deepchainapps.version import VERSION


def catch_requirements():
    with open("deepchainapps/requirements.txt") as reqs:
        req_list: List[str] = []
        for req in reqs.readlines():
            req = req.replace("\n", "")
            req = req.replace("==", ">=")
            if req.__contains__("esm"):
                req = "git+https://github.com/facebookresearch/esm.git"
            req_list.append(req)

    return req_list


def install():

    setup_fn = setup(
        name="deepchain-apps",
        version=VERSION,
        description="Define a personnal scorer for the user of DeepChain.bio",
        author="Instadeep",
        author_email="a.delfosse@instadeep.com",
        packages=find_packages(),
        entry_points={
            "console_scripts": [
                'deepchain=deepchainapps.cli.deepchain:main'
            ],
        },

        install_required=catch_requirements(),
        include_package_data=True,
        zip_safe=False,
        python_requires=">=3.7",
    )

    return setup_fn


if __name__ == "__main__":
    install()
