import click

import modules.util as util
from modules.extractor import extract_data


@click.command()
@click.option('--config', help= 'path of the config file')
def extract(config):
  configs = util.get_config(config)
  extract_data(configs)

@click.group()
def main():
  pass


if __name__ == '__main__':
  main.add_command(extract)
  main()