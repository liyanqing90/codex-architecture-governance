# Releasing

1. Update `CHANGELOG.md` and `.codex-plugin/plugin.json`.
2. Regenerate `requirements-runtime.lock` and `requirements-dev.lock` with
   `pip-compile --generate-hashes` when dependency ranges change.
3. Run the full gate from `AGENTS.md`, including `validate-knowledge`,
   `scripts/audit_licenses.py`, and `pip-audit`.
4. Confirm the selector-source and latest reviewed implementation commits are
   reachable from the release commit:

   ```bash
   python3 resources/scripts/architecture_tool.py validate-history-anchors .
   ```

   Merge source-anchored governance pull requests with **Merge Commit**.
   Squash or rebase merging discards the reviewed ancestry and will fail CI
   on `main` and the release workflow.
5. Validate all ten Markdown Knowledge Packs and confirm no entry is stale:

   ```bash
   python3 resources/scripts/validate_knowledge.py
   ```

6. Confirm the 45 routing cases and separate selection, decision,
   false-positive, and artifact-validity corpora parse and pass their
   deterministic tests.
7. Run the repository's architecture gate through `release`; preserve the
   trusted Review, accepted Decision, completed Plan, and passed provider
   evidence used by that result.
8. Confirm the archive contains only runtime files:

   ```bash
   unzip -l dist/hengmu-<version>.zip
   ```

9. Verify the checksum on any supported platform:

   ```bash
   python3 scripts/verify_checksum.py \
     dist/hengmu-<version>.zip.sha256
   ```

10. Generate and inspect the SPDX SBOM:

   ```bash
   python3 scripts/generate_sbom.py \
     --archive dist/hengmu-<version>.zip \
     --output dist/hengmu-<version>.spdx.json
   ```

11. Confirm every dependency package in the SPDX document has a declared
   license and exactly matches `resources/supply-chain/runtime-licenses.json`.
12. Complete one current Codex installation smoke test and record the surface,
   application version, operating system, and observed Skill routing.
13. If a behavioral quality claim is planned, preserve three trials per case
   from at least two identified models, with surface, exact plugin version, and
   scorer output.
14. Confirm migration evidence never preserves a legacy verified label as
    current 1.2 verification.
15. Create a signed or annotated `v<version>` tag.
16. Push the tag. The release workflow re-runs validation, tests, lint,
   formatting, dependency audit, deterministic packaging, checksum, and SBOM
   generation. It creates GitHub provenance and SBOM attestations before
   publishing the ZIP, checksum, and SBOM.

After publication, verify both artifact digest and attestation:

```bash
gh attestation verify \
  dist/hengmu-<version>.zip \
  --repo qingye-lab/hengmu
python3 scripts/verify_checksum.py \
  dist/hengmu-<version>.zip.sha256
```

Do not publish from an uncommitted working tree or manually replace a release
asset without issuing a new version. GitHub attestations establish build
provenance; they do not prove the source or workflow is vulnerability-free.
