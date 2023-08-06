import logging
import os
import pathlib
from typing import Dict

_config = None


def load_config(path):
    global _config
    if _config:
        return _config

    logging.info(f"Reading cfg from `{path}`")
    with open(path, "r") as f:
        _config = {row.split("=")[0]: row.split("=")[1] for row in f.read().split("\n")}

    return _config


def config() -> Dict[str, str]:
    global _config
    if _config:
        return _config

    raise AttributeError("Load config first.")


# todo - refactor for Path usage everywhere
def storage_path():
    path = os.path.expanduser("~/.config/anysell")

    if not os.path.exists(path):
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)

    return os.path.join(path, ".internal.cfg")
