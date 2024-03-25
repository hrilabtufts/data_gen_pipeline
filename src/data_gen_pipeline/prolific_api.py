import requests
import json
from enum import Enum


class DEVICES(Enum):
    DESKTOP = [1]
    TABLET = [2]
    MOBILE = [3]
    ALL = [DESKTOP, TABLET, MOBILE]


class ProlificAPI:
    def __init__(self, api_token, researcher_id):
        self.api_token = api_token
        self.researcher_id = researcher_id

    def request(self, method, endpoint, json_body=None):
        headers = {
            "Content-Type": "application/json",
            "PROLIFIC_AUTH_TOKEN": self.api_token,
        }
        response = requests.request(
            method,
            "https://api.prolific.co" + endpoint,
            headers=headers,
            json=json_body,
        )
        if response.status_code != 200:
            print(response.text)
            raise Exception("Error in request: " + response.text)
        return response.json()

    def create_draft_study(
        self,
        name,
        internal_name,
        description,
        external_study_url,
        prolific_id_option,
        completion_option,
        completion_codes,
        total_available_places,
        estimated_completion_time,
        reward,
        eligability_requirements,
        maximum_allowed_time=None,
        device_compatability=DEVICES.ALL,
        peripheral_requirements=[],
        naivety_distribution_rate=None,
        project=None,
        submissions_config=None,
        metadata=None,
    ):
        # construct the json body
        json_body = {
            "name": name,
            "internal_name": internal_name,
            "description": description,
            "external_study_url": external_study_url,
            "prolific_id_option": prolific_id_option,
            "completion_option": completion_option,
            "completion_codes": completion_codes,
            "total_available_places": total_available_places,
            "estimated_completion_time": estimated_completion_time,
            "reward": reward,
            "eligibility_requirements": eligability_requirements,
            "device_compatability": device_compatability,
        }
        if maximum_allowed_time:
            json_body["maximum_allowed_time"] = maximum_allowed_time
        if len(peripheral_requirements) > 0:
            json_body["peripheral_requirements"] = peripheral_requirements
        if naivety_distribution_rate:
            json_body["naivety_distribution_rate"] = naivety_distribution_rate
        if project:
            json_body["project"] = project
        if submissions_config:
            json_body["submissions_config"] = submissions_config
        if metadata:
            json_body["metadata"] = metadata

        self.request("POST", "/studies/drafts/", json_body)

    def publish_draft_study(self,
                            id_,
                            action: str = "PUBLISH",
                            ):
        json_body = {
            "action": action,
        }
        self.request("POST", "/studies/drafts/" + id_ + "/actions/", json_body)


