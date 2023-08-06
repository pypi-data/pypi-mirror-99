"""sbmlsim package."""
from pathlib import Path

__author__ = "Matthias Koenig"
__version__ = "0.2.0"


from sbmlsim.utils import show_versions

BASE_PATH = Path(__file__).parent
RESOURCES_DIR = BASE_PATH / "resources"
