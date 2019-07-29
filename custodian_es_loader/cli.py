import click
import custodian_es_loader.core as core
from pathlib import Path


@click.command()
@click.option("-r",
              "--resources",
              type=click.Path(),
              help="Path to resources.json file")
@click.option("-m",
              "--metadata",
              type=click.Path(),
              help="Path to metadata.json file")
@click.option("-f",
              "--folder",
              type=click.Path(),
              help="Folder to recursively load policies results from")
def main(resources, metadata, folder):
    if folder:
        metadata_files = Path(folder).glob('**/metadata.json*')
        resources_filename_template = "resources.json"

        for metadata_file in metadata_files:
            if metadata_file.suffix == '.gz':
                resources_filename = resources_filename_template + ".gz"
            else:
                resources_filename = resources_filename_template

            resources_file = metadata_file.parent.joinpath(resources_filename)

            if not resources_file.exists() or not resources_file.is_file():
                print(
                    "Unable to find file {}. Skipping.".format(resources_file))
                continue

            metadata = core.load_metadata(metadata_file)
            resources = core.load_resources(resources_file)
            core.process_resources(resources, metadata)
    else:
        metadata = core.load_metadata(metadata)
        resources = core.load_resources(resources)
        core.process_resources(resources, metadata)
