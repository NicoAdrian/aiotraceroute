from setuptools import setup, find_packages


with open("README.md") as fda, open("LICENSE") as fdb:
    readme = fda.read()
    license = fdb.read()

setup(
    name="aiotraceroute",
    version="0.1.0",
    description="Asynchronous traceroute in python",
    long_description=readme,
    author="Nicolas Adrian",
    author_email="nicolasadrian3@gmail.com",
    url="https://github.com/NicoAdrian/aiotraceroute",
    license=license,
    keywords=["traceroute", "async", "asyncio"],
    packages=find_packages(exclude=("tests",)),
)
