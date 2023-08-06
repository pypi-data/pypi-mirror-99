__version__ = '0.1.0'


# module imports
from .detector_factory import DetectorFactory, PROFILES_DIRECTORY, detect, detect_langs
from .language import Language

__all__ = [
    "DetectorFactory",
    "PROFILES_DIRECTORY",
    "detect",
    "detect_langs",
    "Language"
]