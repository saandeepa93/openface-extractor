import os
from natsort import natsorted
from shutil import copyfile

copy_path  = './input/BP4D/'
dest_path = '/Users/saandeep/Projects/de-expression/deep_fake/input/BP4D/'
task_lst = ["T1", "T3", "T4", "T5", "T6", "T7", "T8", "T9"]
for subject in natsorted(os.listdir(copy_path)):
  if subject in ["F003", "F008"]:
    continue
  sub_path = os.path.join(copy_path, subject)
  if os.path.isdir(sub_path):
    for tsk in task_lst:
      task_path = os.path.join(sub_path, tsk)
      file = natsorted(os.listdir(task_path))[0]
      file_path = os.path.join(task_path, file)
      file_name = f"{subject}_{tsk}.png"
      out_path = os.path.join(dest_path, file_name)
      copyfile(file_path, out_path)
