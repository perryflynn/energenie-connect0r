from setuptools import find_packages
import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="energenieconnector",
    version="1.0.0",
    author="perryflynn",
    author_email="christian@anysrc.net",
    description="Control your Energenie EG-PMS-LAN with Python.",
    long_description=long_description,
    license="MIT License",
    long_description_content_type="text/markdown",
    url="https://github.com/perryflynn/energenie-connect0r",
    project_urls={
        "Bug Tracker": "https://github.com/perryflynn/energenie-connect0r/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'geniecli = energenieconnector.geniecli:cli',
            'geniemassstatus = energenieconnector.geniemassstatus:cli',
        ],
    }
)
