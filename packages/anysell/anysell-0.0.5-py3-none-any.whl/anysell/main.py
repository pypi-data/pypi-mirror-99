import logging
import sys
import os
from typing import List

import yaml
import click
import glob

from anysell.config import load_config
from anysell.sellers.item import Item
from anysell.sellers import BazosSeller


logging.basicConfig(level=logging.INFO)


@click.group()
def cli():
    pass


@cli.command()
@click.option("--config-path", default="~/.config/anysell/.cfg", type=click.Path())
def sell(config_path):
    cfg = load_config(config_path)

    with open(cfg["item_config_path"], "r") as f:
        items_config = yaml.safe_load(f)

    sellers = [
        BazosSeller(),
    ]
    items: List[Item] = []

    # deserialize and validate items config input
    for name, itemdict in items_config.items():
        click.echo(f"Loading {name}.")
        try:
            items.append(Item.deserialize(itemdict))
        except KeyError as e:
            click.echo(f"\n You're missing key - '{e.args[0]}' in {name}'")
            sys.exit(1)

    # create posts for each item in each platform (e.g. bazos, fb)
    for item in items:
        for seller in sellers:
            try:
                seller.create_post(item)
            except Exception as e:
                click.echo("Error occurred.")
                click.echo(e.args[0])
                sys.exit(1)

    click.echo("All done.")


@cli.command()
@click.option("--config-path", default="~/.config/anysell/.cfg", type=click.Path())
@click.option("--overwrite", type=bool, default=False, is_flag=True)
def generate_cfg(config_path, overwrite):
    cfg = load_config(config_path)
    if "item_config_path" not in cfg:
        click.echo(
            "Missing 'item_config_path' key to determine where items config should be."
        )
        sys.exit(1)

    item_config_path = cfg["item_config_path"]
    if os.path.exists(item_config_path) and not overwrite:
        click.echo("File already exists, if you want to overwrite pass '--overwrite'.")
        sys.exit(1)

    click.echo(f"Generating config to '{item_config_path}'.")

    item_cfg = {}

    keys = list(Item.__dataclass_fields__.keys())
    keys.remove("filepaths")

    if not os.path.exists(cfg["img_path"]):
        click.echo(f"Path with images '{cfg['image_path']}' doesn't exists.")
        sys.exit(1)

    for dirname in os.listdir(cfg["img_path"]):
        if dirname.startswith("."):
            continue

        item_cfg[dirname] = {k: "" for k in keys}
        item_cfg[dirname]["filepaths"] = glob.glob(f"{os.path.join(cfg['img_path'], dirname)}/*.jpg")

    with open(item_config_path, "w") as f:
        yaml.dump(item_cfg, f, allow_unicode=True)
