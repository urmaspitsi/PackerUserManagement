import os
from typing import Dict
import yaml

# If running locally, then populate environment variables.
def load_from_yaml() -> Dict:
  # source: https://stackoverflow.com/questions/1773805/how-can-i-parse-a-yaml-file-in-python
  with open("env_variables.yaml") as f:
      env_dict = yaml.safe_load(f)
  
  return env_dict["env_variables"]

def get_env_variable(key: str) -> str:
  # localhost or gcloud appengine environment
  USE_LOCALHOST = False if os.environ.get("GAE_ENV") == "standard" else True

  if USE_LOCALHOST:
    dict = load_from_yaml()
    return dict[key]
  else:
    return os.environ.get(key)

