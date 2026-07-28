from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = ROOT / "scripts" / "validate_repository.py"
SPEC = importlib.util.spec_from_file_location("validate_repository", SCRIPT_PATH)
assert SPEC and SPEC.loader
validate_repository = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_repository)


class RepositoryContractTests(unittest.TestCase):
    def test_repository_contract(self) -> None:
        errors = validate_repository.validate_repository(ROOT)
        self.assertEqual(errors, [], "\n".join(errors))


if __name__ == "__main__":
    unittest.main()
