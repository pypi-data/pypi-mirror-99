# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['motioneye_client']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0', 'pytest-cov>=2.11.1,<3.0.0']

setup_kwargs = {
    'name': 'motioneye-client',
    'version': '0.2.0',
    'description': 'motionEye client library Python Package',
    'long_description': '[![PyPi](https://img.shields.io/pypi/v/motioneye-client.svg)](https://pypi.org/project/motioneye-client/)\n[![PyPi](https://img.shields.io/pypi/pyversions/motioneye-client.svg)](https://pypi.org/project/motioneye-client/)\n[![Build Status](https://travis-ci.com/dermotduffy/motioneye-client.svg?branch=master)](https://travis-ci.com/dermotduffy/motioneye-client)\n[![Coverage](https://img.shields.io/codecov/c/github/dermotduffy/motioneye-client)](https://codecov.io/gh/dermotduffy/motioneye-client)\n\n# motionEye Client\n\nA simple async API client for motionEye.\n\n## Constructor arguments\n\nThe following arguments may be passed to the `MotionEyeClient` constructor:\n\n|Argument|Type|Default|Description|\n|--------|----|-------|-----------|\n|host    |`str`||Host or IP to connect to|\n|port    |`int`|8765|Port to connect to|\n|admin_username|`str`|admin|The motionEye admin username|\n|admin_password|`str`|""|The motionEye admin password\n|surveillance_username|`str`|user|The motionEye surveillance username|\n|surveillance_password|`str`|""|The motionEye surveillance password|\n\nThis client needs both `admin` and `surveillance` passwords in order to interact with\nthe API (which generally require the `admin` user), as well as prepare the URLs for\ndata streaming (which require the `surveillance` user).\n\n## Primary Client Methods\n\nAll async calls start with `async_`, and return the JSON response from the server (if any).\n\n### async_client_login\n\nLogin to the motionEye server. Not actually necessary, but useful for verifying credentials.\n### async_client_close\n\nClose the client session. Always returns True.\n\n### async_get_manifest\n\nGet the motionEye server manifest (e.g. server version number).\n\n### async_get_server_config\n\nGet the main motionEye server config.\n\n### async_get_cameras\n\nGet the listing of all cameras.\n\n### async_get_camera\n\nGet the configuration of a single camera. Takes an integer `camera_id` argument.\n\n### async_set_camera\n\nSet the configuration of a single camera. Takes an integer `camera_id` argument, and a\ndictionary of the same format as returned by `async_get_camera`.\n\n## Convenience Methods\n\n### is_camera_streaming\n\nConvenience method to take a camera dictionary (returned by `async_get_camera` or\n`async_get_cameras`) and return True if the camera has video stream enabled.\n\n### get_camera_steam_url\n\nConvenience method to take a camera dictionary (returned by `async_get_camera` or\n`async_get_cameras`) and return the string URL of the streamed content (which can be\nopened separately).\n\n### get_camera_snapshot_url\n\nConvenience method to take a camera dictionary (returned by `async_get_camera` or\n`async_get_cameras`) and return the string URL of a single still frame.\n\n## Context Manager\n\nThe client may be used in as a context manager, which will automatically close the\nsession.\n\n```python\nasync with client.MotionEyeClient("localhost", ) as mec:\n    if not mec:\n        return\n    ...\n````\n\n## Exceptions / Errors \n\n### MotionEyeClientError\n\nA generic base class -- all motionEye client exceptions inherit from this.\n\n### MotionEyeClientInvalidAuth\n\nInvalid authentication detected during a request.\n\n### MotionEyeClientConnectionFailure\n\nConnected failed to given host and port.\n\n### MotionEyeClientRequestFailed\n\nA request failed in some other undefined way.\n\n## Simple Example\n\n```python\n#!/usr/bin/env python\n"""Client test for motionEye."""\nimport asyncio\nimport logging\n\nfrom motioneye_client.client import MotionEyeClient\n\nasync def query_motioneye_server():\n  async with MotionEyeClient("localhost", 8765) as client:\n      if not client:\n        return\n\n      manifest = await client.async_get_manifest()\n      print ("Manifest: %s" % manifest)\n\n      camera_list = await client.async_get_cameras()\n      print ("Cameras: %s" % camera_list)\n\nasyncio.get_event_loop().run_until_complete(query_motioneye_server())\n```',
    'author': 'Dermot Duffy',
    'author_email': 'dermot.duffy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dermotduffy/motioneye-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
