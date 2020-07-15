import os
import subprocess
from tqdm import tqdm
import cv2
from sys import exit as e

import modules.util as util

FNULL = open(os.devnull, 'w')


def sh(cmd):
  return subprocess.call(cmd, stdout=FNULL, stderr=subprocess.STDOUT)


def extract_data(configs):
  input_path = configs['paths']['input']
  output_path = configs['paths']['output']
  docker_img = configs['docker']['img']
  work_dir = configs['docker']['work_dir']
  cmd = configs['docker']['cmd']

  data_type = configs['params']['type']
  fresh_output = configs['params']['fresh_output']
  docker_dst = f"{docker_img}:{work_dir}"

  for file in tqdm(os.listdir(input_path)):
    file_inpath = os.path.abspath(os.path.join(input_path, file))

    if os.path.splitext(file_inpath)[-1] != configs['params']['ext']:
      op_file = f"{os.path.splitext(file)[0]}.csv"
      file_opath = os.path.join(output_path, op_file)
      copy_to = sh(['docker', 'cp', file_inpath, docker_dst])
      if copy_to != 0:
        print(f"Could not copy the file {file} to docker")
        continue
      exec_status = sh(['docker', 'exec', docker_img, cmd, '-f', file])
      if exec_status != 0:
        print(f"Openface could not extract the details for {file}")
        continue
      copy_from = sh(['docker', 'cp', f"{docker_dst}/processed/{op_file}", f'{file_opath}'])
      if copy_from != 0:
        print(f"Could not copy the file {op_file} from docker")
        continue


    sh(['docker', 'exec', docker_img, 'rm', '-r', 'processed'])
    sh(['docker', 'exec', docker_img, 'rm', file])
