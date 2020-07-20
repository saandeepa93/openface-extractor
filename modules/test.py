import os
import random
import glob
import cv2
import pandas as pd
from sys import exit as e
import numpy as np
from numpy import genfromtxt

import modules.util as util


def add_lms(frame, in_fpath, cnt, lm_cols, op_fpath, arr):
  for i in zip(arr[cnt, :68], arr[cnt, 68:]):
    cv2.circle(frame, (i[0], i[1]), 2, (0, 255, 0), 2)
  util.show(frame)
  e()

def test_extracts(configs):
  input_path = configs['paths']['input']
  output_path = os.path.join(configs['paths']['output'], "openface")
  ext = configs['params']['ext']
  typ = configs['params']['type']
  lm_cols = util.get_2d_lms()

  tot_files = len(glob.glob(os.path.join(input_path, "*"+ext)))
  randint = random.randint(0, tot_files - 1)
  filename = os.listdir(input_path)[randint]

  in_fpath = os.path.join(input_path, filename)
  op_fname = os.path.splitext(filename)[0]+".csv"
  op_fpath = os.path.join(output_path, op_fname)

  arr = pd.read_csv(op_fpath, usecols = lm_cols, skipinitialspace = True).to_numpy().astype(np.int)

  if typ == 'videos':
    cap = cv2.VideoCapture(in_fpath)
    cnt = 0
    while True:
      ret, frame = cap.read()
      if ret == 0:
        break
      add_lms(frame, in_fpath, cnt, lm_cols, op_fpath, arr)
      cnt+=1
      if cv2.waitKey(1) & 0xFF == ord('e'):
        break
    cap.release()
    cv2.destroyAllWindows()

  elif typ == 'frame':
    pass
