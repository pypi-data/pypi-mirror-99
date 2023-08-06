"""rio_stac.scripts.cli."""

import datetime
import json

import click
from pystac import MediaType
from pystac.utils import datetime_to_str, str_to_datetime
from rasterio.rio import options

from rio_stac import create_stac_item


def _cb_key_val(ctx, param, value):
    if not value:
        return {}
    else:
        out = {}
        for pair in value:
            if "=" not in pair:
                raise click.BadParameter(
                    "Invalid syntax for KEY=VAL arg: {}".format(pair)
                )
            else:
                k, v = pair.split("=", 1)
                out[k] = v
        return out


@click.command()
@options.file_in_arg
@click.option(
    "--datetime",
    "-d",
    "input_datetime",
    type=str,
    help="The date and time of the assets, in UTC (e.g 2020-01-01, 2020-01-01T01:01:01).",
)
@click.option(
    "--extension",
    "-e",
    type=str,
    default=["proj"],
    multiple=True,
    help="STAC extension the Item implements.",
)
@click.option(
    "--collection", "-c", type=str, help="The Collection ID that this item belongs to."
)
@click.option(
    "--property",
    "-p",
    metavar="NAME=VALUE",
    multiple=True,
    callback=_cb_key_val,
    help="Additional property to add.",
)
@click.option("--id", type=str, help="Item id.")
@click.option("--asset-name", "-n", type=str, default="asset", help="Asset name.")
@click.option("--asset-href", type=str, default="asset", help="Overwrite asset href.")
@click.option(
    "--asset-mediatype",
    type=click.Choice([it.name for it in MediaType] + ["auto"]),
    help="Asset media-type.",
)
@click.option("--output", "-o", type=click.Path(exists=False), help="Output file name")
def stac(
    input,
    input_datetime,
    extension,
    collection,
    property,
    id,
    asset_name,
    asset_href,
    asset_mediatype,
    output,
):
    """Rasterio stac cli."""
    property = property or {}

    if not input_datetime:
        input_datetime = datetime.datetime.utcnow()
    else:
        if "/" in input_datetime:
            start_datetime, end_datetime = input_datetime.split("/")
            property["start_datetime"] = datetime_to_str(
                str_to_datetime(start_datetime)
            )
            property["end_datetime"] = datetime_to_str(str_to_datetime(end_datetime))
            input_datetime = None
        else:
            input_datetime = str_to_datetime(input_datetime)

    if asset_mediatype and asset_mediatype != "auto":
        asset_mediatype = MediaType[asset_mediatype]

    extensions = [e for e in extension if e]

    item = create_stac_item(
        input,
        input_datetime=input_datetime,
        extensions=extensions,
        collection=collection,
        properties=property,
        id=id,
        asset_name=asset_name,
        asset_href=asset_href,
        asset_media_type=asset_mediatype,
    )

    if output:
        with open(output, "w") as f:
            f.write(json.dumps(item.to_dict(), separators=(",", ":")))
    else:
        click.echo(json.dumps(item.to_dict(), separators=(",", ":")))
