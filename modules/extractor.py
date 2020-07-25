import os
import subprocess
from tqdm import tqdm
import cv2
import glob
import time
import datetime
from sys import exit as e

import modules.util as util
from modules.logger import Logger


FNULL = open(os.devnull, 'w')
def sh(cmd):
  return subprocess.call(cmd, stdout=FNULL, stderr=subprocess.STDOUT)



def extract_data(configs, file_inpath):
  input_path = configs['paths']['input']
  output_path = configs['paths']['output']
  docker_img = configs['docker']['img']
  work_dir = configs['docker']['work_dir']
  cmd = configs['docker']['cmd']

  data_type = configs['params']['type']
  docker_dst = f"{docker_img}:{work_dir}"

  # file_inpath = get_folder(configs)

  file = file_inpath.split('/')[-1]
  if data_type == "videos":
    subject = file
  elif data_type == "frames":
    subject = file_inpath.split('/')[-2]

  op_file = f"{os.path.splitext(file)[0]}.csv"
  op_folder = f"{os.path.splitext(file)[0]}_aligned"


  output_path_main = os.path.abspath(os.path.join(os.path.join(output_path, os.path.relpath(file_inpath, input_path)), os.pardir))
  if not os.path.isdir(output_path_main):
    os.makedirs(output_path_main)
  output_path_aligned = os.path.join(output_path_main, "aligned")
  if not os.path.isdir(output_path_aligned):
    os.mkdir(output_path_aligned)
  output_path_openface = os.path.join(output_path_main, "openface")
  if not os.path.isdir(output_path_openface):
    os.mkdir(output_path_openface)


  copy_to = sh(['docker', 'cp', file_inpath, docker_dst])
  if copy_to != 0:
    msg = f"Could not copy the file {file} to docker"
    return -1, msg

  if data_type == "videos":
    exec_status = sh(['docker', 'exec', docker_img, cmd, '-f', file])
  elif data_type == "frames":
    exec_status = sh(['docker', 'exec', docker_img, cmd, '-fdir', file])
  else:
    exec_status = -1
  if exec_status != 0:
    msg = f"Openface could not extract the details for {file}"
    return -1, msg

  copy_from = sh(['docker', 'cp', f"{docker_dst}/processed/{op_file}", f'{output_path_openface}'])
  copy_from_face = sh(['docker', 'cp', f"{docker_dst}/processed/{op_folder}", f"{output_path_aligned}"])
  if copy_from != 0:
    msg = f"Could not copy the file {op_file} from docker"
    return -1, msg
  if copy_from_face != 0:
    msg = f"Could not copy the file {op_folder} from docker"
    return -1, msg

  stat1 = sh(['docker', 'exec', docker_img, 'rm', '-r', 'processed'])
  if stat1 != 0:
    print(f"could not remove the processed file in docker")

  stat = sh(['docker', 'exec', docker_img, 'rm', '-r', file])
  if stat != 0:
    print(f"could not remove the file {file} in docker")

  return None, None


def run_openface(configs, dataset):
  text_file = open("./logs/bp4d_failure_20200724193802.txt", "r")
  lines = text_file.readlines()
  lines = [i.split(':')[3].strip(' ') for i in lines]

  ts = time.time()
  st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
  d = configs['paths']['input']
  logger = Logger(f'./logs/{dataset}_success_{st}.txt', f'./logs/{dataset}_failure_{st}.txt')
  for dir, subdir, files in os.walk(d):
    if not subdir:
      if configs['params']['type'] == 'frames':
        subject = dir.split('/')[-2]
        task = dir.split('/')[-1]
        fname = f"{subject}_{task}"
        if fname in lines:
          print(f" extracting for Subject {dir.split('/')[-2]} task {dir.split('/')[-1]}...")
          status, msg = extract_data(configs, dir)
          if status == -1:
            logger.log_failure(dir.split('/')[-2], 'frames', dir.split('/')[-1], msg)
            print("failed!")
          else:
            logger.log_success(dir.split('/')[-2], 'frames', dir.split('/')[-1])
            print("done!")
        else:
          continue
      elif configs['params']['type'] == 'videos':
        for file in files:
          if os.path.splitext(file)[-1] == configs['params']['ext']:
            subject = os.path.join(dir, file)
            print(f"extracting for Subject {subject.split('/')[-1]}....")
            status, msg = extract_data(configs, subject)
            if status == -1:
              logger.log_failure(dir.split('/')[-1], 'videos', msg)
              print("failed!")
            else:
              logger.log_success(dir.split('/')[-1], 'videos')
              print("done!")
  print("openface extraction complete!")

