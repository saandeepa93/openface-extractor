import click

import modules.util as util
from modules.extractor import run_openface
from modules.test import test_extracts

from sys import exit as e


@click.command()
@click.option('--config', help= 'path of the config file')
def extract(config):
  dataset = config.split('/')[-1].split('.')[0]
  configs = util.get_config(config)
  run_openface(configs, dataset)

@click.command()
@click.option('--config', help = 'path of the config file you want to test')
def test(config):
  configs = util.get_config(config)
  test_extracts(configs)


@click.group()
def main():
  pass


if __name__ == '__main__':
  main.add_command(extract)
  main.add_command(test)
  main()