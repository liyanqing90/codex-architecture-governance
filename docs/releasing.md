# Releasing

1. Update `CHANGELOG.md` and `.codex-plugin/plugin.json`.
2. Regenerate `requirements-runtime.lock` and `requirements-dev.lock` with
   `pip-compile --generate-hashes` when dependency ranges change.
3. Run the full gate from `AGENTS.md`, including `validate-knowledge`,
   `scripts/audit_licenses.py`, and `pip-audit`.
4. Confirm the archive contains only runtime files:

   ```bash
   unzip -l dist/codex-architecture-governance-<version>.zip
   ```

5. Verify the checksum on any supported platform:

   ```bash
   python3 scripts/verify_checksum.py \
     dist/codex-architecture-governance-<version>.zip.sha256
   ```

6. Generate and inspect the SPDX SBOM:

   ```bash
   python3 scripts/generate_sbom.py \
     --archive dist/codex-architecture-governance-<version>.zip \
     --output dist/codex-architecture-governance-<version>.spdx.json
   ```

7. Confirm every dependency package in the SPDX document has a declared
   license and exactly matches `resources/supply-chain/runtime-licenses.json`.
8. Complete one current Codex installation smoke test and record the surface,
   application version, operating system, and observed Skill routing.
9. If a behavioral quality claim is planned, preserve a repeated benchmark run
   with identified model, surface, exact plugin version, and scorer output.
10. Create a signed or annotated `v<version>` tag.
11. Push the tag. The release workflow re-runs validation, tests, lint,
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
