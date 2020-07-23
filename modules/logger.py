import time
import datetime

from sys import exit as e

class Logger():
  def __init__(self, file_succpath, file_failpath):
    super(Logger).__init__()
    self.file_success = open(file_succpath, "a")
    self.file_success.seek(0, 0)
    self.file_success.truncate()

    self.file_failure = open(file_failpath, "a")
    self.file_failure.seek(0, 0)
    self.file_failure.truncate()

  def log_success(self, subject, typ, task = None):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    if typ == "videos":
      self.file_success.write(f"{st}: {subject}\n")
    elif typ == "frames":
      self.file_success.write(f"{st}: {subject} {task}\n")


  def log_failure(self, subject, typ, task = None, msg = None):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    if typ == "videos":
      self.file_failure.write(f"{st}: {subject}: {msg}\n")
    elif typ == "frames":
      self.file_failure.write(f"{st}: {subject}_{task}: {msg}\n")


