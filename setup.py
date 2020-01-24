from setuptools import setup, find_packages


with open("README.md") as fd:
    readme = fd.read()

setup(
    name="aiotraceroute",
    version="0.1.1",
    description="Asynchronous traceroute in python",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Nicolas Adrian",
    author_email="nicolasadrian3@gmail.com",
    url="https://github.com/NicoAdrian/aiotraceroute",
    license="MIT",
    keywords=["traceroute", "async", "asyncio"],
    packages=find_packages(),
    install_requires=["aiodns"]
)
