from setuptools import setup, find_packages

VERSION = '1.0.2'
DESCRIPTION = 'Athena Utility'
LONG_DESCRIPTION = 'AWS Athena client based on PyAthena'

# Setting up
setup(
    name="athenautility",
    version=VERSION,
    author="KnowledgeLens",
    author_email="karthik.madhamanchi@knowledgelens.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pyathena', 'pandas'],
    python_requires=">=3.6"
)

