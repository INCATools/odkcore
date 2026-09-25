# odkcore - Ontology Development Kit Core
# Copyright © 2026 ODK Developers
#
# This file is part of the ODK Core project and distributed under the
# terms of a 3-clause BSD license. See the LICENSE file in that project
# for the detailed conditions.

from time import sleep
from typing import Any, Dict, Set, Tuple

import requests
from requests.exceptions import RequestException

from .download import RETRIABLE_HTTP_ERRORS


class GitHubHelper(object):
    """Helper class to interact with the GitHub API.

    For now, the only purpose of this class is to automatically obtain
    the commit ID of the latest release of a GitHub Action. It may be
    expanded for other purposes in the future.
    """

    cache: Dict[str, Tuple[str, str]]
    failure_cache: Set[str]

    def __init__(self):
        self.cache = {}
        self.failure_cache = set()

    def get_latest_release_sha(self, name: str, default: str) -> str:
        """Gets the commit ID for the latest release of a GitHub project.

        :param name: The name of a GitHub project, in `owner/repo` form.
        :param default: The default tag to fallback to if we can't get the
            required information from GitHub.
        :returns: A string of the form `XXXX # TAG`, where `XXXX` is the
            commit ID of the latest release and `TAG` is the
            corresponding tag name; or just the value of the `default`
            parameter if the latest commit ID could not be obtained.
        """
        latest = self.get_latest_release(name)
        if latest:
            return f"{latest[1]} # {latest[0]}"
        return default

    def get_latest_release(self, name: str) -> Tuple[str, str] | None:
        """Gets the tag name and commit ID for the latest release of a GitHub project.

        :param name: The name of a GitHub project, in `owner/repo` form.
        :returns: A tuple (TAG,XXXX), where `TAG` is the tag of the
            latest release and `XXXX` is the corresponding commit ID; or
            None if we could not obtain the information from GitHub.
        """
        cached = self.cache.get(name)
        if cached or name in self.failure_cache:
            return cached

        try:
            latest_release = self._query_github_api(f"repos/{name}/releases/latest")
            tagname = latest_release["tag_name"]

            release_ref = self._query_github_api(f"repos/{name}/git/ref/tags/{tagname}")
            sha = release_ref["object"]["sha"]
            if release_ref["object"]["type"] != "commit":
                release_tag = self._query_github_api(f"repos/{name}/git/tags/{sha}")
                sha = release_tag["object"]["sha"]

            self.cache[name] = (tagname, sha)
            return (tagname, sha)
        except (KeyError, RequestException):
            # We don't really care about what went wrong exactly (e.g.
            # network issue or unexpected JSON content).
            self.failure_cache.add(name)
            return None

    def _query_github_api(self, endpoint: str, max_retry: int = 4) -> Dict[str, Any]:
        """Sends a query to the GitHub API and returns the JSON response."""
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2026-03-10",
        }
        n_try = 0
        while True:
            response = requests.get(
                f"https://api.github.com/{endpoint}", timeout=5, headers=headers
            )
            if response.status_code == 200:
                return response.json()
            elif response.status_code in RETRIABLE_HTTP_ERRORS and n_try < max_retry:
                n_try += 1
                sleep(1)
            else:
                response.raise_for_status()
                # We could get there upon receiving a non-error HTTP
                # status (e.g. 203, 204)
                raise RequestException(f"Unexpected status: {response.status_code}")
