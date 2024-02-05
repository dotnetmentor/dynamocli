from setuptools import setup, find_packages

with open("README", "r", encoding="utf-8") as fhand:
    long_description = fhand.read()

setup(
    name='dynamocli',
    author='Viktor Blidh',
    author_email='viktor.blidh@gmail.com',
    version='0.0.11',
    description='Command line interface for interacting with a DynamoDB instance',
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'boto3',
        'rich',
        'appdirs'
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "dynamocli = src.dyno:main"
        ]
    }
)
