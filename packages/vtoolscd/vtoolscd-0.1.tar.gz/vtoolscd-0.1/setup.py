from setuptools import setup
import sys,os
from requests import get
setup(
      name='vtoolscd',
      version="0.1", # Lastest release
      description="vtools",
      long_description="Manage vitual machines, getting some informations (eg. OS).",
      long_description_content_type="text/markdown",
      url="https://github.com/repos/CastellaniDavide/vtools",
      author="DavideC03",
      author_email="help@castellanidavide.it",
      license='GNU',
      packages = ['src'],
      python_requires=">=3.6",
      platforms="linux_distibution",
      install_requires=["requests", "tabular-log>=2.5"],
      zip_safe=True,
      entry_points = {
        'console_scripts': [
            'vtools=src.vtools:laucher']
            },
      )
