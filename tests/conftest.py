"""Shared test setup: headless, isolated matplotlib."""

import os
import tempfile

os.environ["MPLBACKEND"] = "Agg"
os.environ["MPLCONFIGDIR"] = tempfile.mkdtemp(prefix="introai-mpl-")
