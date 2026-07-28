# Releasing

1. Update `CHANGELOG.md` and `.codex-plugin/plugin.json`.
2. Run the full gate from `AGENTS.md`.
3. Confirm the archive contains only runtime files:

   ```bash
   unzip -l dist/codex-architecture-governance-<version>.zip
   ```

4. Verify the checksum:

   ```bash
   (cd dist && shasum -a 256 -c codex-architecture-governance-<version>.zip.sha256)
   ```

5. Create a signed or annotated `v<version>` tag.
6. Push the tag. The release workflow re-runs validation, tests, lint,
   formatting, and deterministic packaging before creating the GitHub release.

Do not publish from an uncommitted working tree or manually replace a release
asset without issuing a new version.
