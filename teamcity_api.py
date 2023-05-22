import json
import os
from urllib.request import HTTPBasicAuthHandler, HTTPPasswordMgr

import requests


class TeamCityApi:
    def __init__(self, rest_url: str, username: str, password: str):
        self._rest_url = rest_url
        self._auth = requests.auth.HTTPBasicAuth(username, password)

    def call_api(self, endpoint: str):
        """Call the TeamCity API and return the JSON response."""
        url = self._rest_url + endpoint
        log_file = f"./apilog/{endpoint.replace('/', '_').replace(':', '_')}.txt"

        if os.path.exists(log_file):
            with open(log_file, "rt") as file:
                return json.load(file)

        response = requests.get(url,
                                auth=self._auth,
                                headers={"accept": "application/json"})
        response.raise_for_status()

        if not os.path.exists("./apilog"):
            os.mkdir("./apilog")
        with open(log_file, "wt" if os.path.exists(log_file) else "xt") as file:
            json.dump(response.text, log_file)

        return response.json()

    def get_project(self, project_id):
        """Get the details of a project from TeamCity."""
        return self.call_api(f"/app/rest/projects/id:{project_id}")

    def get_build_configurations(self, project_id):
        """Get the build configurations for a project from TeamCity."""
        return self.call_api(f"/app/rest/projects/id:{project_id}/buildTypes")

    def get_build_configuration_details(self, build_type_id):
        """Get the details of a build configuration from TeamCity."""
        build_config = self.call_api(f"/app/rest/buildTypes/id:{build_type_id}")
        build_config["triggers"] = self.call_api(f"/app/rest/buildTypes/id:{build_type_id}/triggers")
        build_config["dependencies"] = self.call_api(f"/app/rest/buildTypes/id:{build_type_id}/snapshot-dependencies")
        return self.get_build_configurations()
