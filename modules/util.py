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
