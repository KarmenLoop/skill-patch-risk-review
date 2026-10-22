# Patch Risk Review

English | [简体中文](README.zh-CN.md)

Find the parts of a Git diff that deserve a closer look. Get per-file line counts and review areas such as authentication before you open the full change in your normal review tool.

[Download v0.2.1](https://github.com/KarmenLoop/skill-patch-risk-review/releases/tag/v0.2.1) · [Tutorial](docs/tutorial.en.md) · [Input reference](docs/INPUT.md) · [Report an issue](https://github.com/KarmenLoop/skill-patch-risk-review/issues)

## What it does

The sample touches src/auth.py, adds two lines, removes one, and marks authentication for review.

Review areas are path-based hints, not a security audit. The helper does not apply patches, inspect runtime behavior, or approve a merge.

![Patch Risk Review sample JSON output from version 0.2.1](docs/images/example-output-v0.2.1.svg)

*Actual local output from v0.2.1, rendered as an image. [Complete result](examples/expected.json) · [Image provenance](docs/images/provenance.json).*

## Start here

Download `karmen-patch-risk-review-v0.2.1.zip` and its `.sha256` file from the release, verify the hash, then extract the ZIP. In the extracted directory, use Python 3.9 or later:

```sh
python3 scripts/run.py --version
python3 scripts/run.py --input examples/input.json
```

Expected version: `karmen-patch-risk-review 0.2.1`. The sample touches src/auth.py, adds two lines, removes one, and marks authentication for review.

To install the complete skill into a host that reads `~/.agents/skills`:

```sh
python3 install.py --host agents
```

The installer refuses an existing destination. Host discovery and invocation vary; see the [full setup and practice guide](docs/tutorial.en.md). You can run the helper directly without an AI host.

## Use it with your own work

Supply the complete Git-style unified diff as diff. Preserve headers and hunk counts; truncated or inconsistent hunks are rejected instead of guessed.

Review a change with quoted or space-containing paths, then compare the summary with git diff --stat. Inspect each flagged file and run the affected project’s own checks.

Read the [field contract](docs/INPUT.md) before preparing a new input. The helper runs locally with the Python standard library; it needs no model account, API key, or network connection. An AI host has its own data and permission settings.

## Questions

**Can this prove a patch is safe to merge?** No. Use it to choose where to look, then review the code, requirements, and actual test results.

**Where does the result go?** JSON is printed to stdout unless you request a new file with `--output`. Existing output files are preserved. The helper reads only the submitted records and any local paths documented in its input contract.

## Documentation and support

- [Download, install, configure, practice, upgrade, and remove](docs/tutorial.en.md)
- [Input/output contract](docs/INPUT.md) and [compatibility](docs/COMPATIBILITY.md)
- [Changelog](CHANGELOG.md), [contributing](CONTRIBUTING.md), [support](SUPPORT.md), and [security reports](SECURITY.md)

## License

[MIT](LICENSE). Keep the license and [notice](NOTICE.md) with redistributed copies. Maintained by [KarmenLoop](https://karmenloop.com).
