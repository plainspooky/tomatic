from distutils.core import setup
from tomatic import __version__ as version

setup(
    name="tomatic",
    packages=["tomatic"],
    version=version,
    license="gpl-3.0",
    description="Tomatic is a library that helps to enable automatic configuration for python programas.",
    long_description=open("README.rst").read(),
    author="Giovanni Nunes",
    author_email="giovanni.nunes@gmail.com",
    url="https://github.com/plainspooky/tomatic",
    keywords=["configuration", "django", "settings", "setup"],
    install_requires=[],
    project_urls={
        "Documentation": "https://plainspooky.github.io/tomatic/index.html",
        "Source Code": "https://github.com/plainspooky/tomatic",
    },
    classifiers=[
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
