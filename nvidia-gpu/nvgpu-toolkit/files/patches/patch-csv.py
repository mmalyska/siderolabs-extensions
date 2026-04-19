#!/usr/bin/env python3
"""
Patch internal/modifier/csv.go to honour cfg.DisableRequire in CSV mode.

image.HasDisableRequire() checks the container env var NVIDIA_DISABLE_REQUIRE,
not the toolkit config file's disable-require field. The config field is only
propagated to the image object in the hook (legacy) path. This patch makes the
CSV modifier also skip requirement checks when cfg.DisableRequire is true,
which is needed on Tegra where /proc/driver/nvidia/version does not exist.
"""
import sys

path = "/container-toolkit/internal/modifier/csv.go"

old = (
    "\tif err := checkRequirements(f.logger, f.image); err != nil {\n"
    "\t\treturn nil, fmt.Errorf(\"requirements not met: %v\", err)\n"
    "\t}"
)
new = (
    "\tif disableRequire := f.cfg != nil && f.cfg.DisableRequire; !disableRequire {\n"
    "\t\tif err := checkRequirements(f.logger, f.image); err != nil {\n"
    "\t\t\treturn nil, fmt.Errorf(\"requirements not met: %v\", err)\n"
    "\t\t}\n"
    "\t}"
)

content = open(path).read()
if old not in content:
    print(f"ERROR: patch target not found in {path}", file=sys.stderr)
    sys.exit(1)
patched = content.replace(old, new, 1)
open(path, "w").write(patched)
print("csv.go patched OK")
