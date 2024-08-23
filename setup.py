from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="liqpay-async",
    version="0.0.1",
    description="LiqPay Async Python3 SDK",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/SpaceIgor/liqpay-async",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "aiohttp>=3.10.5"
    ],
)
