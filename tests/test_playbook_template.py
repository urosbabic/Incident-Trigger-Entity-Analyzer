"""Validate the static structure of the Sentinel playbook ARM template."""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = REPOSITORY_ROOT / "azuredeploy.json"


def load_template() -> dict[str, Any]:
    """Load the deployment template as JSON."""
    with TEMPLATE_PATH.open(encoding="utf-8") as template_file:
        return json.load(template_file)


class PlaybookTemplateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.template = load_template()
        cls.resources = cls.template["resources"]
        workflows = [
            resource
            for resource in cls.resources
            if resource.get("type") == "Microsoft.Logic/workflows"
        ]
        if len(workflows) != 1:
            raise AssertionError(f"Expected one Logic App workflow, found {len(workflows)}")
        cls.workflow = workflows[0]
        cls.definition = cls.workflow["properties"]["definition"]

    def test_arm_template_metadata_and_parameters(self) -> None:
        self.assertEqual(
            self.template["$schema"],
            "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
        )
        self.assertIn("PlaybookName", self.template["parameters"])
        self.assertIn("lookBackDays", self.template["parameters"])

    def test_incident_creation_trigger_is_configured(self) -> None:
        trigger = self.definition["triggers"]["Microsoft_Sentinel_incident"]
        self.assertEqual(trigger["type"], "ApiConnectionWebhook")
        self.assertEqual(trigger["inputs"]["path"], "/incident-creation")

    def test_url_and_user_analysis_paths_are_present(self) -> None:
        actions = self.definition["actions"]
        url_actions = actions["For_each_URL"]["actions"]
        self.assertIn("URL_Analyzer", url_actions)
        self.assertIn("Add_Url_comment_to_incident", url_actions)

        user_actions = actions["For_each_User"]["actions"]
        identifier_check = user_actions["Condition_-_Check_Valid_User_Identifier"]
        self.assertIn("User_Analyzer", identifier_check["actions"])
        self.assertIn(
            "Add_Skip_comment_to_incident",
            identifier_check["else"]["actions"],
        )

    def test_sentinel_and_sentinel_mcp_connections_are_declared(self) -> None:
        connection_api_ids = {
            resource["properties"]["api"]["id"]
            for resource in self.resources
            if resource.get("type") == "Microsoft.Web/connections"
        }
        self.assertTrue(any("/managedApis/azuresentinel" in api_id for api_id in connection_api_ids))
        self.assertTrue(any("/managedApis/sentinelmcp" in api_id for api_id in connection_api_ids))


if __name__ == "__main__":
    unittest.main()