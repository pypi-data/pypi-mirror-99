# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gen2aclbundle',
 'gen2aclbundle.acl',
 'gen2aclbundle.acl.check',
 'gen2aclbundle.acl.export',
 'gen2aclbundle.acl.set',
 'gen2aclbundle.client']

package_data = \
{'': ['*'], 'gen2aclbundle': ['_config/*']}

install_requires = \
['azure-storage-file-datalake>=12.0,<13.0',
 'console-bundle>=0.4.0b1',
 'pandas>=0.25.0,<0.26.0',
 'pyfony-bundles>=0.4.0b1']

entry_points = \
{'pyfony.bundle': ['create = gen2aclbundle.Gen2AclBundle:Gen2AclBundle']}

setup_kwargs = {
    'name': 'gen2-acl-bundle',
    'version': '0.3.0a1',
    'description': 'Azure DataLake ACL setup bundle for the Pyfony Framework',
    'long_description': 'Azure DataLake ACL setup bundle for the Pyfony Framework\n',
    'author': 'Jiri Koutny',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/daipe-ai/gen2-acl-bundle',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
