import os
import subprocess
from tqdm import tqdm
import cv2
import glob
from sys import exit as e

import modules.util as util

FNULL = open(os.devnull, 'w')
def sh(cmd):
  return subprocess.call(cmd, stdout=FNULL, stderr=subprocess.STDOUT)


def get_folder(configs):
  dirs = []
  d = configs['paths']['input']
  num_dirs = configs['params']['subfolders']
  for dir, subdir, files in os.walk(d):
    if not subdir:
      if configs['params']['type'] == 'frames':
        dirs.append(dir)
      elif configs['params']['type'] == 'videos':
        for file in files:
          if os.path.splitext(file)[-1] == configs['params']['ext']:
            dirs.append(os.path.join(dir, file))
  return dirs


def extract_data(configs):
  input_path = configs['paths']['input']
  output_path = configs['paths']['output']
  docker_img = configs['docker']['img']
  work_dir = configs['docker']['work_dir']
  cmd = configs['docker']['cmd']

  data_type = configs['params']['type']
  fresh_output = configs['params']['fresh_output']
  docker_dst = f"{docker_img}:{work_dir}"

  dir_lst = get_folder(configs)

  for file_inpath in tqdm(dir_lst):
    file = file_inpath.split('/')[-1]

    output_path_main = os.path.abspath(os.path.join(os.path.join(output_path, os.path.relpath(file_inpath, input_path)), os.pardir))
    if not os.path.isdir(output_path_main):
      os.makedirs(output_path_main)
    output_path_aligned = os.path.join(output_path_main, "aligned")
    if not os.path.isdir(output_path_aligned):
      os.mkdir(output_path_aligned)
    output_path_openface = os.path.join(output_path_main, "openface")
    if not os.path.isdir(output_path_openface):
      os.mkdir(output_path_openface)

    op_file = f"{os.path.splitext(file)[0]}.csv" if data_type == "videos" else f"{os.path.splitext(file)[0]}"
    op_folder = f"{os.path.splitext(file)[0]}_aligned"

    copy_to = sh(['docker', 'cp', file_inpath, docker_dst])
    if copy_to != 0:
      print(f"Could not copy the file {file} to docker")
      continue

    if data_type == "videos":
      exec_status = sh(['docker', 'exec', docker_img, cmd, '-f', file])
    elif data_type == "frames":
      exec_status = sh(['docker', 'exec', docker_img, cmd, '-fdir', file])
    else:
      exec_status = -1
    if exec_status != 0:
      print(f"Openface could not extract the details for {file}")
      continue

    copy_from = sh(['docker', 'cp', f"{docker_dst}/processed/{op_file}", f'{output_path_openface}'])
    copy_from_face = sh(['docker', 'cp', f"{docker_dst}/processed/{op_folder}", f"{output_path_aligned}"])
    if copy_from != 0:
      print(f"Could not copy the file {op_file} from docker")
      continue
    if copy_from_face != 0:
      print(f"Could not copy the file {op_folder} from docker")
      continue

  sh(['docker', 'exec', docker_img, 'rm', '-r', 'processed'])
  sh(['docker', 'exec', docker_img, 'rm', file])
