from typing import List

import setuptools
from setuptools import setup


def get_version() -> str:
    with open('version') as version_file:
        return version_file.read()


def get_requirements() -> List[str]:
    with open('requirements.txt') as requirements_file:
        return [dependency.strip() for dependency in requirements_file if dependency.strip()]


setup(name='usf-auth-service-client',
      version=get_version(),
      author="Ukuspeed",
      author_email="info@ukuspeed.gmail.com",
      description="Auth service client",
      url="https://github.com/ukuspeed/usf-auth-service",
      packages=setuptools.find_packages(),
      python_requires='>=3.6',
      install_requires=get_requirements()
      )
