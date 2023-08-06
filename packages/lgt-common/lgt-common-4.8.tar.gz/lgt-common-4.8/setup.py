import json
from urllib import request
from pkg_resources import parse_version
from setuptools import setup


def versions():
    url = f'https://pypi.python.org/pypi/lgt-common/json'
    releases = json.loads(request.urlopen(url).read())['releases']
    return sorted(releases, key=parse_version, reverse=True)


last_version = round(float(versions()[0]) + 0.1, 1) if versions() else 0.0

setup(name='lgt-common',
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
          'lgt_data'
      ],
      author_email='developer@leadguru.co',
      zip_safe=False)
