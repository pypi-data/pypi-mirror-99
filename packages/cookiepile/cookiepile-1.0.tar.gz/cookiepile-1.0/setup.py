from setuptools import setup
__project__ = "cookiepile"
__version__ = "1.0"
__description__ = "Cookiepile is a new compiler program. It supports compiling almost anything. You can run python and shell commands, have a ToS page, an intro, and outro. Wiki page coming soon."
__packages__ = ["cookiepile"]
__author__ = "EnderC00kiez"
__author_email__ = "EnderC00kiez@pm.me"
__classifiers__ = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3",
]
__keywords__ = ["Installer", "Compiler"]
setup(
    name = __project__,
    version = __version__,
    description = __description__,
    packages = __packages__,
    author = __author__,
    author_email = __author_email__,
    classifiers = __classifiers__,
    keywords = __keywords__,
)