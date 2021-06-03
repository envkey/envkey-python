from __future__ import print_function
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
  p = platform.platform()

  if "arm64" in p or "aarch64" in p:
    return "arm64"

  is_64 = sys.maxsize > 2**32

  if not is_64:
    raise RuntimeError("As of 1.3.0, envkey-python only supports 64-bit systems. Please use an earlier version for 32-bit support.")

  return "amd64"

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

  try:
    res = subprocess.check_output(args).decode(encoding="utf-8").rstrip()
  except subprocess.CalledProcessError as err:
    print("envkey-fetch " + err.output.decode(encoding="utf-8"), file=sys.stderr)
    raise ValueError("ENVKEY invalid. Couldn't load vars.")

  if res.startswith("error: "):
    raise ValueError("ENVKEY invalid. Couldn't load vars.")

  return json.loads(res)