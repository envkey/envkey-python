import sys
import platform
import subprocess
import os.path
import pkg_resources
import json
from .constants import ENVKEY_FETCH_VERSION

def __lib_extension():
  return ".exe" if platform.system() == "Windows" else ""

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
  root = os.path.abspath(os.path.dirname(__file__))
  return os.path.join(root, 'ext',__lib_dir(), __lib_file_name())

def fetch_env(key, cache_enabled=False):
  path = __lib_path()
  args = [path, key, "--client-name", "envkey-python", "--client-version", pkg_resources.get_distribution("envkey").version]
  if cache_enabled:
    args.append("--cache")

  res = subprocess.check_output(args).decode().rstrip()

  if res.startswith("error: "):
    raise ValueError("ENVKEY invalid. Couldn't load vars.")

  return json.loads(res)