import json
import os
import requests
import sys
from typing import Optional

EXPECTED_TF_CONFIG_FILE_NAMES = ["tdfconfig.yml", "tdfconfig.yaml", "validate_configs.yaml", "commit_configs.yaml"]
TRANSFORM_API_URL = "web-api.prod.transformdata.io"
UPLOAD_MODE_VALIDATE = "validate"
UPLOAD_MODE_COMMIT = "commit"


def read_config_files(config_dir: str):
    """Read yaml files from config_dir. Returns (file name, file contents) per file in dir"""
    assert os.path.exists(config_dir), f"User-specified config dir ({config_dir}) does not exist"

    results = {}
    for path, _folders, filenames in os.walk(config_dir):
        for fname in filenames:
            if not (fname.endswith(".yml") or fname.endswith(".yaml")):
                continue

            # ignore transform config
            if fname in EXPECTED_TF_CONFIG_FILE_NAMES:
                continue

            with open(os.path.join(path, fname), "r") as f:
                results[fname] = f.read()

    return results


def upload_configs(  # noqa: D
    mode: str,
    api_key: str,
    repo: Optional[str] = None,
    branch: Optional[str] = None,
    commit: Optional[str] = None,
    config_dir: Optional[str] = None,
):
    yaml_files = read_config_files(config_dir or ".")
    results = {"yaml_files": yaml_files}
    print(f"Files to upload: {yaml_files.keys()}")
    headers = {"Content-Type": "application/json", "Authorization": f"X-Api-Key {api_key}"}

    add_files_url = f"https://{TRANSFORM_API_URL}/api/v1/model/{repo}/{branch}/{commit}/add_model_files"
    print(f"add_files_url: {add_files_url}")
    print("Uploading config files")
    r = requests.post(add_files_url, data=json.dumps(results).encode("utf-8"), headers=headers)
    print(r.text)
    assert r.status_code == 200, "Failed uploading config yaml files"

    if mode == UPLOAD_MODE_VALIDATE:
        validate_url = f"https://{TRANSFORM_API_URL}/api/v1/model/{repo}/{branch}/{commit}/validate_model"
        print(f"validate_url: {validate_url}")
        print("Checking that uploaded configs are valid and form a valid model")
        r = requests.post(validate_url, headers=headers)
        assert r.status_code == 200, f"Failed validating uploaded configs. Error response: {r.text}"
        print("Successfully validated configs")
    elif mode == UPLOAD_MODE_COMMIT:
        commit_url = f"https://{TRANSFORM_API_URL}/api/v1/model/{repo}/{branch}/{commit}/commit_model"
        print(f"commit_url: {commit_url}")
        print("Committing model")
        r = requests.post(commit_url, headers=headers)
        assert r.status_code == 200, f"Failed committing uploaded configs. Error response: {r.text}"
        print("Successfully committed configs")
    else:
        raise ValueError(f"Invalid upload mode ({mode}). Expected '{UPLOAD_MODE_VALIDATE}' or '{UPLOAD_MODE_COMMIT}'")


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode != UPLOAD_MODE_VALIDATE and mode != UPLOAD_MODE_COMMIT:
        raise ValueError(f"Invalid upload mode ({mode}) passed via args.")

    # Retrieve git info and API key from env
    REPO = os.getenv("REPO")
    # remove github org from repo
    if REPO:
        REPO = "/".join(REPO.split("/")[1:])

    if os.getenv("GITHUB_HEAD_REF") == "":
        BRANCH = os.getenv("GITHUB_REF").lstrip("/refs/heads/")
    else:
        BRANCH = os.getenv("GITHUB_HEAD_REF")

    COMMIT = os.getenv("GITHUB_SHA")
    TRANSFORM_CONFIG_DIR = os.getenv("TRANSFORM_CONFIG_DIR").rstrip()
    TRANSFORM_API_KEY = os.environ["TRANSFORM_API_KEY"].rstrip()  # fail if TRANSFORM_API_KEY not present

    upload_configs(mode, TRANSFORM_API_KEY, REPO, BRANCH, COMMIT, TRANSFORM_CONFIG_DIR)
