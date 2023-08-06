#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os

from typing import List

from git import Repo as GitRepo

from polyaxon import settings
from polyaxon.client import RunClient
from polyaxon.env_vars.keys import (
    POLYAXON_KEYS_GIT_CREDENTIALS,
    POLYAXON_KEYS_SSH_PATH,
    POLYAXON_KEYS_SSH_PRIVATE_KEY,
)
from polyaxon.exceptions import PolyaxonClientException, PolyaxonContainerException
from polyaxon.polyboard.artifacts import V1ArtifactKind, V1RunArtifact
from polyaxon.utils.code_reference import (
    add_remote,
    checkout_revision,
    get_code_reference,
    git_fetch,
    git_init,
    set_remote,
)
from polyaxon.utils.path_utils import check_or_create_path

_logger = logging.getLogger("polyaxon.repos.git")


def has_cred_access() -> bool:
    return os.environ.get(POLYAXON_KEYS_GIT_CREDENTIALS) is not None


def has_ssh_access() -> bool:
    ssh_path = os.environ.get(POLYAXON_KEYS_SSH_PATH)
    return bool(ssh_path and os.path.exists(ssh_path))


def get_ssh_cmd():
    ssh_path = os.environ.get(POLYAXON_KEYS_SSH_PATH)
    ssh_key_name = os.environ.get(POLYAXON_KEYS_SSH_PRIVATE_KEY, "id_rsa")
    return "ssh -i {}/{} -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no".format(
        ssh_path, ssh_key_name
    )


def get_clone_url(url: str) -> str:
    if not url:
        raise ValueError(
            "Git initializer requires a valid url, received {}".format(url)
        )

    if has_cred_access():
        if "https" in url:
            _url = url.split("https://")[1]
        else:
            _url = url
        creds = os.environ.get(POLYAXON_KEYS_GIT_CREDENTIALS)
        # Add user:pass to the git url
        return "https://{}@{}".format(creds, _url)
    if has_ssh_access() and "http" in url:
        if "https" in url:
            _url = url.split("https://")[1]
        elif "http" in url:
            _url = url.split("http://")[1]
        else:
            _url = url
        parts = _url.split("/")
        _url = "{}:{}".format(parts[0], "/".join(parts[1:]))
        _url = _url.split(".git")[0]
        _url = "git@{}.git".format(_url)
        return _url

    return url


def clone_git_repo(repo_path: str, url: str, flags: List[str] = None) -> str:
    if has_ssh_access():
        return GitRepo.clone_from(
            url=url,
            to_path=repo_path,
            multi_options=flags,
            env={"GIT_SSH_COMMAND": get_ssh_cmd()},
        )
    return GitRepo.clone_from(url=url, to_path=repo_path, multi_options=flags)


def clone_and_checkout_git_repo(
    repo_path: str,
    clone_url: str,
    revision: str,
    flags: List[str] = None,
):
    clone_git_repo(repo_path=repo_path, url=clone_url, flags=flags)
    if revision:
        checkout_revision(repo_path=repo_path, revision=revision)


def fetch_git_repo(
    repo_path: str,
    clone_url: str,
    revision: str,
    flags: List[str] = None,
):
    check_or_create_path(repo_path, is_dir=True)
    git_init(repo_path)
    add_remote(repo_path, clone_url)
    env = None
    if has_ssh_access():
        env = {"GIT_SSH_COMMAND": get_ssh_cmd()}
    git_fetch(repo_path=repo_path, revision=revision, flags=flags, env=env)


def create_code_repo(
    repo_path: str,
    url: str,
    revision: str,
    connection: str = None,
    flags: List[str] = None,
):
    try:
        clone_url = get_clone_url(url)
    except Exception as e:
        raise PolyaxonContainerException("Error parsing url: {}.".format(url)) from e

    if flags and "--experimental-fetch" in flags:
        flags.remove("--experimental-fetch")
        fetch_git_repo(
            repo_path=repo_path, clone_url=clone_url, revision=revision, flags=flags
        )
    else:
        clone_and_checkout_git_repo(
            repo_path=repo_path, clone_url=clone_url, revision=revision, flags=flags
        )
    # Update remote
    set_remote(repo_path=repo_path, url=url)

    if settings.CLIENT_CONFIG.no_api:
        return

    try:
        run_client = RunClient()
    except PolyaxonClientException as e:
        raise PolyaxonContainerException(e)

    code_ref = get_code_reference(path=repo_path, url=url)
    artifact_run = V1RunArtifact(
        name=code_ref.get("commit"),
        kind=V1ArtifactKind.CODEREF,
        connection=connection,
        summary=code_ref,
        is_input=True,
    )
    run_client.log_artifact_lineage(artifact_run)
