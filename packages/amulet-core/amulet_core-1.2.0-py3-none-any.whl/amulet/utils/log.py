import logging
import sys
import os

log = logging.getLogger("amulet_core")
log.setLevel(logging.INFO)

_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

os.makedirs("./logs", exist_ok=True)
_log_file = logging.FileHandler("./logs/amulet_core.log", "w", encoding="utf-8")
if "amulet-debug" in sys.argv:
    _log_file.setLevel(logging.DEBUG)
    log.setLevel(logging.DEBUG)
else:
    _log_file.setLevel(logging.INFO)
_log_file.setFormatter(_formatter)
log.addHandler(_log_file)

_log_console = logging.StreamHandler()
_log_console.setLevel(logging.INFO)
_log_console.setFormatter(_formatter)
log.addHandler(_log_console)
