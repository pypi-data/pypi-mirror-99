from setuptools import setup
import pathlib

plugin_dir = pathlib.Path(__file__).parent.absolute()

with open(f"{plugin_dir}/README.md", "r") as fh:
    long_description = fh.read()

setup(
    author="Tenzir",
    author_email="engineering@tenzir.com",
    classifiers=[
        # https://pypi.org/classifiers/
        "Development Status :: 3 - Alpha",
        "Environment :: Plugins",
        "License :: OSI Approved :: BSD License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
        "Topic :: Security",
        "Topic :: Software Development :: Object Brokering",
        "Topic :: System :: Distributed Computing",
    ],
    description="A plugin to enable threatbus communication with Zeek network monitor.",
    entry_points={"threatbus.app": ["zeek = threatbus_zeek.plugin"]},
    install_requires=[
        "stix2 >= 2.1",
        "threatbus >= 2021.3.25",
    ],
    keywords=[
        "Zeek",
        "intrusion detection",
        "IDS",
        "broker",
        "NSM",
        "network security monitoring",
        "threatbus",
        "Threat Bus",
        "threat intelligence",
        "TI",
        "TI dissemination",
    ],
    license="BSD 3-clause",
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="threatbus-zeek",
    packages=["threatbus_zeek"],
    python_requires=">=3.7",
    setup_requires=["setuptools", "wheel"],
    url="https://github.com/tenzir/threatbus",
    version="2021.03.25",
)
