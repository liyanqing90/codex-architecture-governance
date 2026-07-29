# Releasing

1. Update `CHANGELOG.md` and `.codex-plugin/plugin.json`.
2. Regenerate `requirements-runtime.lock` and `requirements-dev.lock` with
   `pip-compile --generate-hashes` when dependency ranges change.
3. Run the full gate from `AGENTS.md`, including `validate-knowledge`,
   `scripts/audit_licenses.py`, and `pip-audit`.
4. Validate all ten Markdown Knowledge Packs and confirm no entry is stale:

   ```bash
   python3 resources/scripts/validate_knowledge.py
   ```

5. Confirm the 40 routing cases and separate selection, decision,
   false-positive, and artifact-validity corpora parse and pass their
   deterministic tests.
6. Run the repository's architecture gate through `release`; preserve the
   trusted Review, accepted Decision, completed Plan, and passed provider
   evidence used by that result.
7. Confirm the archive contains only runtime files:

   ```bash
   unzip -l dist/codex-architecture-governance-<version>.zip
   ```

8. Verify the checksum on any supported platform:

   ```bash
   python3 scripts/verify_checksum.py \
     dist/codex-architecture-governance-<version>.zip.sha256
   ```

9. Generate and inspect the SPDX SBOM:

   ```bash
   python3 scripts/generate_sbom.py \
     --archive dist/codex-architecture-governance-<version>.zip \
     --output dist/codex-architecture-governance-<version>.spdx.json
   ```

10. Confirm every dependency package in the SPDX document has a declared
   license and exactly matches `resources/supply-chain/runtime-licenses.json`.
11. Complete one current Codex installation smoke test and record the surface,
   application version, operating system, and observed Skill routing.
12. If a behavioral quality claim is planned, preserve three trials per case
   from at least two identified models, with surface, exact plugin version, and
   scorer output.
13. Confirm migration evidence never preserves a legacy verified label as
    current 1.2 verification.
14. Create a signed or annotated `v<version>` tag.
15. Push the tag. The release workflow re-runs validation, tests, lint,
   formatting, dependency audit, deterministic packaging, checksum, and SBOM
   generation. It creates GitHub provenance and SBOM attestations before
   publishing the ZIP, checksum, and SBOM.

After publication, verify both artifact digest and attestation:

```bash
gh attestation verify \
  dist/codex-architecture-governance-<version>.zip \
  --repo liyanqing90/codex-architecture-governance
python3 scripts/verify_checksum.py \
  dist/codex-architecture-governance-<version>.zip.sha256
```

Do not publish from an uncommitted working tree or manually replace a release
asset without issuing a new version. GitHub attestations establish build
provenance; they do not prove the source or workflow is vulnerability-free.
