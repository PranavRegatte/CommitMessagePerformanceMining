import os, sys, stat
import errno
from git import Repo
import shutil

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = "=" * filled_len + "-" * (bar_len - filled_len)

    sys.stdout.write("[%s] %s%%%s\r" % (bar, percents, status))
    sys.stdout.flush()
    
    

def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)
