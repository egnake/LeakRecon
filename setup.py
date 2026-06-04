"""
LeakRecon – High-Performance Asynchronous OSINT & Dark Web Intelligence Framework.

Packaging configuration for pip-installable distribution.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read long description from README
this_directory = Path(__file__).parent
long_description = ""
readme_path = this_directory / "README.md"
if readme_path.exists():
    long_description = readme_path.read_text(encoding="utf-8")

# Read requirements
requirements = []
req_path = this_directory / "requirements.txt"
if req_path.exists():
    requirements = [
        line.strip()
        for line in req_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="leakrecon",
    version="2.0.0",
    author="Egnake",
    author_email="egnake@proton.me",
    description="High-Performance Asynchronous OSINT & Dark Web Intelligence Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/egnake/LeakRecon",
    project_urls={
        "Bug Tracker": "https://github.com/egnake/LeakRecon/issues",
        "Source Code": "https://github.com/egnake/LeakRecon",
        "Documentation": "https://github.com/egnake/LeakRecon#readme",
    },
    license="MIT",
    packages=find_packages(exclude=["tests", "tests.*", "img", "reports"]),
    py_modules=["main", "config"],
    include_package_data=True,
    python_requires=">=3.10",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=8.2.2",
            "pytest-asyncio>=0.23.7",
        ],
    },
    entry_points={
        "console_scripts": [
            "leakrecon=main:cli_entry",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Security",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: System :: Networking",
    ],
    keywords="osint darkweb tor recon intelligence leak security cybersecurity",
)
