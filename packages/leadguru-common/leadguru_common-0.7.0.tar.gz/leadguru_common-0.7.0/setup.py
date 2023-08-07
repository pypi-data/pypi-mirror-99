import json
from urllib import request
from pkg_resources import parse_version
from setuptools import setup

package_name = "leadguru_common"

def versions():
    url = f'https://pypi.python.org/pypi/{package_name}/json'
    releases = json.loads(request.urlopen(url).read())['releases']
    return sorted(releases, key=parse_version, reverse=True)


version_parts = versions()[0].split(".")
version_parts[1] = f'{float(version_parts[1]) + 1}'
#last_version = ".".join(version_parts[0:-1])
last_version = "0.7.0"

setup(name=package_name,
      version=f'{last_version}',
      description='LGT common builds',
      packages=['lgt'],
      include_package_data=True,
      install_requires=[
          'wheel',
          'google-cloud-pubsub',
          'google-cloud-storage',
          'requests',
          'aiohttp',
          'websockets',
          'loguru',
          'leadguru-data',
          'pydantic==1.8.1'
      ],
      author_email='developer@leadguru.co',
      zip_safe=False)
