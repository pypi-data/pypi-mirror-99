# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mirth_client']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.17.1,<0.18.0', 'pydantic>=1.8.1,<2.0.0', 'xmltodict>=0.12.0,<0.13.0']

extras_require = \
{'docs': ['Sphinx>=3.5.3,<4.0.0']}

setup_kwargs = {
    'name': 'mirth-client',
    'version': '0.1.1',
    'description': 'Basic Python interface for Mirth Connect',
    'long_description': '# python-mirth-client\n\nA basic async Python interface for Mirth Connect\n\n## Usage example\n\nAssuming running within IPython or as part of an async application with an event-loop set up.\n\n```python\nfrom mirth_client import MirthAPI\nfrom pprint import pprint\n\nasync with MirthAPI("https://mirth.ukrdc.nhs.uk/api") as api:\n    await api.login("****", "****")\n\n    # Check out list of channels\n    for channel in await api.get_channels():\n        print(f"ID: {channel.id}")\n        print(f"Name: {channel.name}")\n        print("")\n\n    # Get stats for a channel\n    s = await channels["3cdefad2-bf10-49ee-81c9-8ac6fd2fed67"].get_statistics()\n    pprint(s)\n\n    # Check channel for failed messages\n    e = await channels["3cdefad2-bf10-49ee-81c9-8ac6fd2fed67"].get_messages(status="error")\n    pprint(e)\n\n    # Get 10 most recent events\n    e = await api.get_events(10)\n    pprint(e)\n```\n',
    'author': 'Joel Collins',
    'author_email': 'joel.collins@renalregistry.nhs.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
