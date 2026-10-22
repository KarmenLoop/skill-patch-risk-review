# Input and output

English | [简体中文](input.zh-CN.md)

Supply a UTF-8 JSON object (maximum 10 MiB). Use `--input PATH` for a file or `--input -` for standard input. Run `--version` to inspect the installed helper version. Duplicate JSON keys and non-finite JSON constants are rejected. Arrays are required unless documented as optional. IDs must be stable and unique. Dates use ISO 8601; timestamps require an explicit UTC offset.

| Field | Contract |
| --- | --- |
| diff | Git-style unified diff string; empty diff is allowed. Space-containing and Git-quoted UTF-8 paths are supported. Truncated or inconsistent hunk counts are input errors. |

## Example

```json
{
  "diff": "diff --git a/src/auth.py b/src/auth.py\n--- a/src/auth.py\n+++ b/src/auth.py\n@@ -1,1 +1,2 @@\n-old_check()\n+new_check()\n+log_result()\n"
}
```

## Result

files with additions, deletions, and review_areas; totals for all parsed hunks.

See [the complete sample result](../examples/expected.json). Exit 0 means processing completed, not that all reported findings passed.

## Errors and side effects

The helper makes no network requests and executes no submitted commands. It reads the input and explicitly documented local paths. It writes only a requested new output file; stdout is the default. Invalid input exits 2. Existing output is preserved. An output write failure can leave a partial new file; remove that file before retrying. Installation is a separate explicit action.
