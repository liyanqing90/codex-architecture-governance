from __future__ import annotations

import copy
import json
import re
import sys
import tempfile
import unittest
from datetime import UTC, date, datetime
from pathlib import Path

import yaml

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
SCRIPT_ROOT = ROOT / "resources" / "scripts"
sys.path.insert(0, str(SCRIPT_ROOT))

from inspect_repository import InspectionError, inspect_repository  # noqa: E402
from knowledge_model import (  # noqa: E402
    KnowledgeError,
    validate_knowledge_tree,
    validate_markdown_entry,
)
from select_knowledge import select_knowledge  # noqa: E402


class TargetArchitectureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name).resolve()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_inspector_collects_only_bounded_observations(self) -> None:
        (self.root / "app.py").write_text(
            "from fastapi import FastAPI\napp = FastAPI()\n",
            encoding="utf-8",
        )
        (self.root / "requirements.txt").write_text(
            "fastapi==1.0\npsycopg==3.0\n",
            encoding="utf-8",
        )
        facts = inspect_repository(
            self.root,
            scanned_at=datetime(2026, 7, 29, tzinfo=UTC),
        )

        self.assertEqual(
            {item["id"] for item in facts["frameworks"]},
            {"fastapi"},
        )
        self.assertEqual(
            {item["id"] for item in facts["storage"]},
            {"postgresql"},
        )
        serialized = json.dumps(facts, sort_keys=True).lower()
        self.assertNotIn("recommendation", serialized)
        self.assertNotIn("finding", serialized)
        self.assertNotIn("severity", serialized)

    def test_inspector_rejects_scope_escape(self) -> None:
        with self.assertRaisesRegex(InspectionError, "escapes repository root"):
            inspect_repository(self.root, scope_values=["../outside"])

    def test_selector_uses_facts_and_respects_negative_scope(self) -> None:
        (self.root / "package.json").write_text(
            json.dumps(
                {
                    "dependencies": {
                        "react": "1.0.0",
                        "vite": "1.0.0",
                    }
                }
            ),
            encoding="utf-8",
        )
        (self.root / "requirements.txt").write_text(
            "fastapi==1.0\npsycopg==3.0\n",
            encoding="utf-8",
        )
        facts = inspect_repository(
            self.root,
            scanned_at=datetime(2026, 7, 29, tzinfo=UTC),
        )
        facts_path = self.root / "repository-facts.yaml"
        facts_path.write_text(
            yaml.safe_dump(facts, sort_keys=False),
            encoding="utf-8",
        )

        selection = select_knowledge(
            facts_path,
            profile_path=None,
            task=(
                "Review React, FastAPI, and PostgreSQL boundaries without "
                "Kafka, Kubernetes, iOS, Event Sourcing, or multi-agent design."
            ),
            skill="project-architecture-audit",
            maximum_entries=24,
        )
        selected = {item["id"] for item in selection["selection"]}

        self.assertTrue(
            {
                "technology.react",
                "technology.fastapi",
                "technology.postgresql",
                "domain.web-frontend",
                "domain.backend-api",
            }.issubset(selected)
        )
        self.assertTrue(
            {
                "technology.apache-kafka",
                "technology.kubernetes",
                "domain.mobile",
                "decision.single-agent-vs-multi-agent",
                "pattern.cqrs-event-sourcing",
            }.isdisjoint(selected)
        )
        self.assertEqual(
            len(selection["selection"]) + len(selection["excluded"]),
            205,
        )

    def test_knowledge_tree_has_all_target_packs_and_entries(self) -> None:
        manifest, entries = validate_knowledge_tree(
            ROOT / "resources" / "knowledge",
            schema_root=ROOT / "resources" / "schemas",
            today=date(2026, 7, 29),
        )

        self.assertEqual(len(manifest["packs"]), 10)
        self.assertEqual(len(entries), 205)
        self.assertTrue(all(manifest["_validated_counts"].values()))

    def test_knowledge_validator_rejects_shallow_and_stale_entries(self) -> None:
        source = (
            ROOT / "resources" / "knowledge" / "foundations" / "quality-attributes.md"
        )
        shallow = self.root / "shallow.md"
        shallow.write_text(
            re.sub(
                r"(?ms)^## Mechanism\n.*?(?=^## )",
                "## Mechanism\n\nx\n\n",
                source.read_text(encoding="utf-8"),
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(KnowledgeError, "too shallow"):
            validate_markdown_entry(
                shallow,
                schema_root=ROOT / "resources" / "schemas",
                expected_kind="foundation",
                today=date(2026, 7, 29),
            )

        stale = self.root / "stale.md"
        stale.write_text(
            source.read_text(encoding="utf-8").replace(
                "last_reviewed: '2026-07-28'",
                "last_reviewed: '2020-01-01'",
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(KnowledgeError, "is stale"):
            validate_markdown_entry(
                stale,
                schema_root=ROOT / "resources" / "schemas",
                expected_kind="foundation",
                today=date(2026, 7, 29),
            )

    def test_knowledge_tree_rejects_unknown_relations(self) -> None:
        knowledge_root = self.root / "knowledge"
        manifest = yaml.safe_load(
            (ROOT / "resources" / "knowledge" / "manifest.yaml").read_text(
                encoding="utf-8"
            )
        )
        for pack in manifest["packs"]:
            pack["required"] = pack["id"] == "foundations"
            (knowledge_root / pack["path"]).mkdir(parents=True)
        (knowledge_root / "manifest.yaml").write_text(
            yaml.safe_dump(manifest, sort_keys=False),
            encoding="utf-8",
        )
        source = (
            ROOT / "resources" / "knowledge" / "foundations" / "quality-attributes.md"
        )
        entry = source.read_text(encoding="utf-8").replace(
            "related: []",
            "related:\n- foundation.does-not-exist",
        )
        (knowledge_root / "foundations" / "quality-attributes.md").write_text(
            entry,
            encoding="utf-8",
        )

        with self.assertRaisesRegex(KnowledgeError, "unknown related IDs"):
            validate_knowledge_tree(
                knowledge_root,
                schema_root=ROOT / "resources" / "schemas",
                today=date(2026, 7, 29),
            )

    def test_decision_snapshot_rejects_stale_knowledge_hash(self) -> None:
        import architecture_tool

        _, entries = validate_knowledge_tree(
            ROOT / "resources" / "knowledge",
            schema_root=ROOT / "resources" / "schemas",
            today=date(2026, 7, 29),
        )
        decision = architecture_tool.load_yaml(
            ROOT / "resources" / "templates" / "architecture-decision.yaml"
        )
        decision["knowledge_snapshot"] = [
            {
                "id": entry_id,
                "version": entries[entry_id].metadata["version"],
                "sha256": entries[entry_id].sha256,
            }
            for entry_id in (
                "style.modular-monolith",
                "pattern.feature-flag",
                "technology.import-linter",
                "migration.layered-monolith-to-modular",
            )
        ]
        decision_path = self.root / "decision.yaml"
        decision_path.write_text(
            yaml.safe_dump(decision, sort_keys=False),
            encoding="utf-8",
        )
        architecture_tool.validate_decision(decision_path)

        tampered = copy.deepcopy(decision)
        tampered["knowledge_snapshot"][0]["sha256"] = "0" * 64
        decision_path.write_text(
            yaml.safe_dump(tampered, sort_keys=False),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(
            architecture_tool.ArchitectureError,
            "hash is stale",
        ):
            architecture_tool.validate_decision(decision_path)


if __name__ == "__main__":
    unittest.main()
