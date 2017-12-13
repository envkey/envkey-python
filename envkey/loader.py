import os
import json
from dotenv import load_dotenv
from .fetch import fetch_env

def load():
  dot_env_res = load_dotenv(os.path.join(os.getcwd(), ".env"))
  key = os.environ.get("ENVKEY")

  if key == None:
    raise ValueError("ENVKEY missing - must be set as an environment variable or in a gitignored .env file in the root of your project. Go to https://www.envkey.com if you don't know what an ENVKEY is.")

  fetch_res = fetch_env(key, is_dev=(dot_env_res == True))

  if fetch_res.startswith("error: "):
    raise ValueError("ENVKEY invalid. Couldn't load vars.")

  parsed = json.loads(fetch_res)
  vars_set = dict()

  for k in parsed:
    if os.environ.get(k) == None:
      os.environ[k] = parsed[k]
      vars_set[k] = parsed[k]

  return vars_set