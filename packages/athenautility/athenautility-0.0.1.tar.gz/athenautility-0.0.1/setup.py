from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Athena Utility'
LONG_DESCRIPTION = 'AWS Athena utility based on PyAthena'

# Setting up
setup(
    name="athenautility",
    version=VERSION,
    author="KnowledgeLens",
    author_email="karthik.madhamanchi@knowledgelens.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pyathena'],
)

