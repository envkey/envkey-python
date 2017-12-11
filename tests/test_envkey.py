import os
import pytest
from importlib import reload

VALID_ENVKEY = "Emzt4BE7C23QtsC7gb1z-3NvfNiG1Boy6XH2o-env-staging.envkey.com"
INVALID_ENVKEYS = (
 "Emzt4BE7C23QtsC7gb1z-3NvfNiG1Boy6XH2oinvalid-env-staging.envkey.com",
 "Emzt4BE7C23QtsC7gb1zinvalid-3NvfNiG1Boy6XH2o-env-staging.envkey.com",
 "Emzt4BE7C23QtsC7gb1zinvalid-3NvfNiG1Boy6XH2o-localhost:387946",
 "invalid",
)

os.environ["ENVKEY"] = VALID_ENVKEY
import envkey

def test_valid():
  os.environ["ENVKEY"] = VALID_ENVKEY
  reload(envkey)
  assert(os.environ["TEST"] == "it")
  assert(os.environ["TEST_2"] == "works!")

def test_no_overwrite():
  os.environ["TEST"] = "otherthing"
  reload(envkey)
  assert(os.environ["TEST"] == "otherthing")
  assert(os.environ["TEST_2"] == "works!")

def test_invalid():
  for key in INVALID_ENVKEYS:
    os.environ["ENVKEY"] = key
    with pytest.raises(ValueError):
      reload(envkey)

def test_no_envkey():
  del os.environ["ENVKEY"]
  with pytest.raises(ValueError):
    reload(envkey)