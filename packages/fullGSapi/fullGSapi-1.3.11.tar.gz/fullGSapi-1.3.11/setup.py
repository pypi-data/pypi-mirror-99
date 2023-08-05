from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()


setup(
    name="fullGSapi",
    version="1.3.11",
    author="ThaumicMekanism",
    author_email="thaumicmekanism@gmail.com",
    long_description=readme,
    long_description_content_type="text/markdown",
    licence="MIT",
    packages=find_packages(include=["fullGSapi.api", "fullGSapi.cli"]),
    entry_points={"console_scripts": ["gradescope=fullGSapi.cli.__main__:cli"]},
    python_requires=">=3.6",
    install_requires=["cryptography", "beautifulsoup4", "py-mini-racer", "requests", "pyyaml", "python-dateutil"],
    extras_require={
        "cli": ["click", "tqdm", "pytz"],
    },
)
