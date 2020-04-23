import os
import pytest

from sys import version_info
if version_info[0] < 3:
    pass # Python 2 has built in reload
elif version_info[0] == 3 and version_info[1] <= 4:
    from imp import reload # Python 3.0 - 3.4
else:
    from importlib import reload # Python 3.5+

VALID_ENVKEY = "wYv78UmHsfEu6jSqMZrU-3w1kwyF35nRYwsAJ-env-staging.envkey.com"
INVALID_ENVKEYS = (
 "Emzt4BE7C23QtsC7gb1z-3NvfNiG1Boy6XH2oinvalid-env-staging.envkey.com",
 "Emzt4BE7C23QtsC7gb1zinvalid-3NvfNiG1Boy6XH2o-env-staging.envkey.com",
 "Emzt4BE7C23QtsC7gb1zinvalid-3NvfNiG1Boy6XH2o-localhost:387946",
 "invalid",
)

os.environ["ENVKEY"] = VALID_ENVKEY
import envkey

def test_valid():
  os.environ.clear()
  os.environ["ENVKEY"] = VALID_ENVKEY
  reload(envkey)
  assert(os.environ["TEST"] == "it")
  assert(os.environ["TEST_2"] == "works!")

def test_no_overwrite():
  os.environ.clear()
  os.environ["TEST"] = "otherthing"
  os.environ["ENVKEY"] = VALID_ENVKEY
  reload(envkey)
  assert(os.environ["TEST"] == "otherthing")
  assert(os.environ["TEST_2"] == "works!")

def test_invalid():
  os.environ.clear()
  for key in INVALID_ENVKEYS:
    os.environ["ENVKEY"] = key
    with pytest.raises(ValueError):
      reload(envkey)

def test_no_envkey():
  os.environ.clear()
  with pytest.raises(ValueError):
    reload(envkey)

def test_autoload_disabled():
  os.environ.clear()
  os.environ["ENVKEY"] = VALID_ENVKEY

  # ensure import doesn't autload when disabled via env var
  os.environ["ENVKEY_DISABLE_AUTOLOAD"] = "1"

  reload(envkey)
  assert(os.environ.get("TEST") == None)

  # test calling fetch directly
  assert(envkey.fetch_env(VALID_ENVKEY)['TEST'] == "it")

  # test calling load directly
  envkey.load()
  assert(os.environ["TEST"] == "it")
  assert(os.environ["TEST_2"] == "works!")