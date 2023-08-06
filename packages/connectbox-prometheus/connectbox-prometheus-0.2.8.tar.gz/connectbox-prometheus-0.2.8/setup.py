from pathlib import Path
from setuptools import find_packages, setup

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")


RESOURCES_ROOT = Path(__file__).parent / "resources"
REQUIREMENTS_ROOT = RESOURCES_ROOT / "requirements"
PRODUCTION_REQUIREMENTS = REQUIREMENTS_ROOT / "production.txt"

with PRODUCTION_REQUIREMENTS.open() as f:
    install_requires = [s.strip() for s in f.readlines()]

setup(
    name="connectbox-prometheus",
    version="0.2.8",
    author="Michael Bugert",
    author_email="git@mbugert.de",
    description='Prometheus exporter for Compal CH7465LG cable modems, commonly sold as "Connect Box"',
    long_description=long_descr,
    long_description_content_type="text/markdown",
    url="https://github.com/mbugert/connectbox-prometheus",
    entry_points={
        "console_scripts": [
            "connectbox_exporter = connectbox_exporter.connectbox_exporter:main"
        ]
    },
    include_package_data=True,
    packages=find_packages(exclude=["tests"]),
    install_requires=install_requires,
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: System :: Networking :: Monitoring",
    ],
)
