# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geojson_rewind']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['rewind = geojson_rewind.rewind:main']}

setup_kwargs = {
    'name': 'geojson-rewind',
    'version': '1.0.1',
    'description': 'A Python library for enforcing polygon ring winding order in GeoJSON',
    'long_description': '# geojson-rewind\n\n![Run tests](https://github.com/chris48s/geojson-rewind/workflows/Run%20tests/badge.svg?branch=master)\n[![codecov](https://codecov.io/gh/chris48s/geojson-rewind/branch/master/graph/badge.svg?token=0WGM3W8ULH)](https://codecov.io/gh/chris48s/geojson-rewind)\n![PyPI Version](https://img.shields.io/pypi/v/geojson-rewind.svg)\n![License](https://img.shields.io/pypi/l/geojson-rewind.svg)\n![Python Compatibility](https://img.shields.io/badge/dynamic/json?query=info.requires_python&label=python&url=https%3A%2F%2Fpypi.org%2Fpypi%2Fgeojson-rewind%2Fjson)\n\nA Python library for enforcing polygon ring winding order in GeoJSON\n\nThe [GeoJSON](https://tools.ietf.org/html/rfc7946) spec mandates the [right hand rule](https://tools.ietf.org/html/rfc7946#section-3.1.6):\n\n> A linear ring MUST follow the right-hand rule with respect to the area it bounds, i.e., exterior rings are counterclockwise, and holes are clockwise.\n\nThis helps you generate compliant Polygon and MultiPolygon geometries.\n\nNote: Co-ordinates in the input data are assumed to be WGS84 with (lon, lat) ordering, [as per RFC 7946](https://tools.ietf.org/html/rfc7946#section-3.1.1). Input with co-ordinates using any other CRS may lead to unexpected results.\n\n## Installation\n\n```\npip install geojson-rewind\n```\n\n## Usage\n\n### As a Library\n\nEnforce RFC 7946 ring winding order (input/output is a GeoJSON string):\n\n```py\n>>> from geojson_rewind import rewind\n\n>>> input = """{\n...      "geometry": {   "coordinates": [   [   [100, 0],\n...                                             [100, 1],\n...                                             [101, 1],\n...                                             [101, 0],\n...                                             [100, 0]]],\n...                      "type": "Polygon"},\n...      "properties": {"foo": "bar"},\n...      "type": "Feature"}"""\n\n>>> output = rewind(input)\n\n>>> output\n\'{"geometry": {"coordinates": [[[100, 0], [101, 0], [101, 1], [100, 1], [100, 0]]], "type": "Polygon"}, "properties": {"foo": "bar"}, "type": "Feature"}\'\n\n>>> type(output)\n<class \'str\'>\n```\n\nEnforce RFC 7946 ring winding order (input/output is a python dict):\n\n```py\n>>> from geojson_rewind import rewind\n\n>>> input = {\n...     \'geometry\': {   \'coordinates\': [   [   [100, 0],\n...                                            [100, 1],\n...                                            [101, 1],\n...                                            [101, 0],\n...                                            [100, 0]]],\n...                     \'type\': \'Polygon\'},\n...     \'properties\': {\'foo\': \'bar\'},\n...     \'type\': \'Feature\'}\n\n>>> output = rewind(input)\n\n>>> output\n{\'geometry\': {\'coordinates\': [[[100, 0], [101, 0], [101, 1], [100, 1], [100, 0]]], \'type\': \'Polygon\'}, \'properties\': {\'foo\': \'bar\'}, \'type\': \'Feature\'}\n\n>>> type(output)\n<class \'dict\'>\n```\n\n## On the Console\n\n```sh\n# Enforce ring winding order on a GeoJSON file\n$ rewind in.geojson > out.geojson\n\n# fetch GeoJSON from the web and enforce ring winding order\n$ curl "https://myserver.com/in.geojson" | rewind\n```\n\n## Acknowledgements\n\n`geojson-rewind` is a python port of Mapbox\'s javascript [geojson-rewind](https://github.com/mapbox/geojson-rewind) package. Credit to [Tom MacWright](https://github.com/tmcw) and [contributors](https://github.com/mapbox/geojson-rewind/graphs/contributors).\n',
    'author': 'chris48s',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chris48s/geojson-rewind',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
