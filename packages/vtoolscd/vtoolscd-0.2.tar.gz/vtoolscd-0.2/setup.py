from setuptools import setup, find_packages
from requests import get

setup(
      name='vtoolscd',
      version=get("https://api.github.com/repos/CastellaniDavide/vtools/tags").json()[0]['name'].replace("v", ""), # Lastest release
      description=get("https://api.github.com/repos/CastellaniDavide/vtools").json()['description'],
      long_description=get("https://raw.githubusercontent.com/CastellaniDavide/vtools/master/docs/README.md").text,
      long_description_content_type="text/markdown",
      url=get("https://api.github.com/repos/CastellaniDavide/vtools").json()['html_url'],
      author=get("https://api.github.com/repos/CastellaniDavide/vtools").json()['owner']['login'],
      author_email=get(f"https://api.github.com/users/{get('https://api.github.com/repos/CastellaniDavide/vtools').json()['owner']['login']}").json()['email'],
      license='GNU',
      packages=find_packages(),
      python_requires=">=3.6",
      platforms="linux_distibution",
      install_requires=[i for i in get("https://raw.githubusercontent.com/CastellaniDavide/vtools/master/requirements/requirements.txt").text.split("\n") if not "#" in i and i != ''],
      zip_safe=True
      )

"""
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
"""
