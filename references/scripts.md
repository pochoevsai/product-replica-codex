# Deterministic helper formats

The bundled helpers use only Python's standard library and never access the network.

## `parity.py`

CSV columns: `id`, `capability`, `priority`, `status`, and optional `intentional_difference`. Priorities are weighted `must=3`, `should=2`, `could=1`; statuses score `done=1`, `partial=0.5`, and other in-scope values `0`. Rows marked `out-of-scope` or with a true `intentional_difference` are excluded. A missing `must` is a release warning; use `--strict` for a non-zero exit.

## `contrast.py`

The JSON may contain nested objects with `foreground` and `background` hex colors. It reports the ratio and WCAG AA/AAA results for normal and large text. It also accepts `--foreground` and `--background` for a one-off check.

## `imgdiff.py`

Accepts non-interlaced 8-bit RGB/RGBA PNGs. It compares dimensions and normalized pixel difference and writes a JSON report with changed-pixel ratio and mean error. Unsupported PNG variants fail clearly rather than producing a misleading score.

## `brand_sweep.py`

Scans common text/code files while ignoring `.git`, dependency directories, build outputs, and binary-looking files. It reports file, line, and matching term. Exit code is non-zero when a forbidden term is found.

## `listing.py`

Reads JSON fields such as `title`, `subtitle`, `description`, `keywords`, and `promotional_text`. It checks conservative App Store/Google Play length limits, ranking claims, and avoided target terms. Platform-specific limits still require confirmation against the current store documentation.
