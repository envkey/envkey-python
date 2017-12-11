from pkg_resources import resource_filename, Requirement
import sys
import platform
import subprocess
import os.path
from .constants import ENVKEY_FETCH_VERSION

def __lib_extension():
  return ".exe" if sys.platform == "win32" else ""

def __lib_file_name():
  return "envkey-fetch" + __lib_extension()

def __lib_arch_part():
  is_64 = sys.maxsize > 2**32
  return "amd64" if is_64 else "386"

def __lib_platform_part():
  name = platform.system()

  if name == "Darwin":
    return "darwin"
  elif name == "Windows":
    return "windows"
  elif name == "FreeBSD":
    return "freebsd"
  else:
    return "linux"

def __lib_dir():
  return "_".join(("envkey-fetch", ENVKEY_FETCH_VERSION, __lib_platform_part(), __lib_arch_part()))

def __lib_path():
  path = "/".join(("ext", __lib_dir(), __lib_file_name()))
  return resource_filename(Requirement.parse("envkey"), path)

def fetch_env(key, is_dev=False):
  path = __lib_path()
  args = [path, key]
  if is_dev:
    args.append("--cache")

  return subprocess.check_output(args).decode().rstrip()