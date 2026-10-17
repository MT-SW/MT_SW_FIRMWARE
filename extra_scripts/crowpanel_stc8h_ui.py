#!/usr/bin/env python3
# trunk-ignore-all(ruff/F821)
# trunk-ignore-all(flake8/F821): For SConstruct imports
import glob
import shutil
from filecmp import cmp
from os.path import join

Import("env")

# ---------------------------------------------------------------------------
# CrowPanel Advance 4.3" / 5.0" / 7.0", HW rev 1.4 / 1.5 (STC8H1K28 at I2C 0x30).
#
# The pinned meshtastic/device-ui only knows the older boards with a TCA9534 I/O
# expander at 0x18 (spams I2C error 259 and never drives the backlight on newer
# boards). The display driver header is therefore replaced - in this environment's
# private libdeps copy only - by variants/esp32s3/elecrow_panel/stc8h/LGFX_ELECROW70.h
# (device-ui PR #307: probes 0x18, otherwise drives backlight via the STC8H1K28).
#
# device-ui includes the header by its own relative path, so it cannot be shadowed
# through -I; the file has to be replaced in the library. libdeps are per
# environment, so no other environment is affected. Remove this script once the
# pinned device-ui contains PR #307.
# ---------------------------------------------------------------------------

SRC = join(
    env.subst("$PROJECT_DIR"),
    "variants",
    "esp32s3",
    "elecrow_panel",
    "stc8h",
    "LGFX_ELECROW70.h",
)
PATTERN = join(
    env.subst("$PROJECT_LIBDEPS_DIR"),
    env["PIOENV"],
    "*",
    "include",
    "graphics",
    "LGFX",
    "LGFX_ELECROW70.h",
)

targets = glob.glob(PATTERN)
if not targets:
    print("crowpanel_stc8h_ui: device-ui LGFX_ELECROW70.h not found at " + PATTERN)
    env.Exit(1)

for target in targets:
    if not cmp(SRC, target, shallow=False):
        shutil.copyfile(SRC, target)
        print("crowpanel_stc8h_ui: patched " + target)
