import json

import requests
import setuptools


def increment_version():
    resp = requests.get('https://pypi.python.org/pypi/lumibot/json')
    j = json.loads(resp.content)
    last_version = j["info"]["version"]
    version_numbers = last_version.split(".")
    version_numbers[-1] = str(int(version_numbers[-1]) + 1)
    new_version = ".".join(version_numbers)
    return new_version

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lumibot",
    version=increment_version(),
    author="Slim Beji",
    author_email="mslimbeji@gmail.com",
    description="Trading Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Lumiwealth/lumibot",
    packages=setuptools.find_packages(),
    install_requires=[
        'alpaca_trade_api',
        'alpha_vantage',
        'yfinance',
        'pandas',
        'pandas_datareader',
        'redis'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
