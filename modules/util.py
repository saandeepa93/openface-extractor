import matplotlib.pyplot as plt
import cv2
import yaml


def show(img):
    plt.imshow(img)
    plt.show()

def cvshow(img):
  cv2.imshow("img", img)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

def get_config(config_path):
  with open(config_path) as file:
    configs = yaml.load(file, Loader = yaml.FullLoader)
  return configs

def get_2d_lms():
  lms_cols = []
  for i in ('x', 'y'):
    for j in range(68):
      lms_cols.append(i+'_'+str(j))
  return lms_cols
