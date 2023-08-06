import json
from urllib import request
from pkg_resources import parse_version
from setuptools import setup

package_name = "leadguru_common"

def versions():
    url = f'https://pypi.python.org/pypi/{package_name}/json'
    releases = json.loads(request.urlopen(url).read())['releases']
    return sorted(releases, key=parse_version, reverse=True)


try:
    last_version = round(float(versions()[0]) + 0.1, 1) if versions() else "0.1.0"
except:
    last_version = "0.1.0"

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
          'leadguru-data'
      ],
      author_email='developer@leadguru.co',
      zip_safe=False)
