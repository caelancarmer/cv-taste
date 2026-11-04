"""Public Camel M33 guidance contract: privacy and fail-closed structure (stdlib only)."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / ".camel"
REQUIRED = {
    "read-live-state", "inspect-domain-evidence", "verify-exact-head",
    "stop-on-unknown", "save-durable-handoff",
}

class PublicCamelM33Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((DATA / "manifest.json").read_text(encoding="utf-8"))
        cls.habits = json.loads((DATA / "habits.json").read_text(encoding="utf-8"))
        cls.policy = json.loads((DATA / "policy.json").read_text(encoding="utf-8"))

    def test_not_private_bundle(self):
        self.assertEqual(self.manifest["kernel"]["version"], "m33-public-guidance")
        self.assertIs(self.manifest["review_only"], True)
        self.assertIs(self.manifest["trajectory"]["host_attestation_verified"], False)
        self.assertIs(self.manifest["trajectory"]["outcome_auto_certification"], False)
        self.assertIs(self.manifest["private_camel_source_bundled"], False)
        self.assertIs(self.manifest["kernel"]["private_source_bundled"], False)
        self.assertEqual(self.manifest["distribution"]["source_modules"], 0)
        self.assertEqual(self.manifest["distribution"]["kind"], "guidance-only")
        self.assertFalse((DATA / "camel-resident.mjs").exists())

    def test_private_candidate_and_external_effects_are_disabled(self):
        for field in ("automatic_merge", "automatic_publication",
                      "automatic_job_application", "private_candidate_data_in_git"):
            self.assertIs(self.policy[field], False)
        self.assertEqual(self.policy["no_new_spend_usd"], 0)
        self.assertIs(self.policy["external_effects_require_explicit_owner_grant"], True)

    def test_domain_habits_are_present_and_scoped(self):
        h = self.habits
        self.assertEqual(h["schema_version"], 1)
        self.assertEqual(h["repository"], "caelancarmer/cv-taste")
        self.assertRegex(h["source_sha"], r"^[0-9a-f]{40}$")
        self.assertEqual(len(h["habits"]), 8)
        self.assertEqual(len({x["id"] for x in h["habits"]}), 8)
        self.assertTrue(REQUIRED.issubset({x["id"] for x in h["habits"]}))
        for x in h["habits"]:
            self.assertRegex(x["id"], r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
            for k in ("trigger", "action", "acceptance"):
                self.assertGreater(len(x[k].strip()), 7)

    def test_outcome_bounds_and_clear_skill(self):
        self.assertEqual(self.manifest["trajectory"]["max_outcomes"], 5)
        self.assertEqual(self.manifest["trajectory"]["max_sub_trajectories_per_outcome"], 12)
        self.assertFalse(self.manifest["autonomous_host_installed"])
        text = (ROOT / ".agents/skills/trajectory-orchestrator/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("candidate", text.lower())
        self.assertIn("not five arbitrary", text.lower())

if __name__ == "__main__":
    unittest.main()
