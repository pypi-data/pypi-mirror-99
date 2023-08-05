from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="nameko-apscheduler",
    version="0.0.4",
    author="Pony Ma",
    author_email="mtf201013@gmail.com",
    description="nameko apscheduler dependency.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ma-pony/nameko-apscheduler",
    install_requires=[
        "marshmallow>=3.6.0",
        "nameko>=3.0.0-rc8",
        "kombu>=4.6.8",
        "APScheduler>=3.6.3",
    ],
    zip_safe=True,
)
