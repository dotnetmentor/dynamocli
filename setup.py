from setuptools import setup

with open("README", "r", encoding="utf-8") as fhand:
    long_description = fhand.read()

setup(
    name='dynamocli',
    author='Viktor Blidh',
    author_email='viktor.blidh@gmail.com',
    version='0.0.8',
    description='Command line interface for interacting with a DynamoDB instance',
    long_description_content_type="text/markdown",
    long_description=long_description,
    install_requires=[
        'boto3',
        'rich',
        'appdirs'
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "dynamocli = dynocli.dyno:main"
        ]
    }
)
