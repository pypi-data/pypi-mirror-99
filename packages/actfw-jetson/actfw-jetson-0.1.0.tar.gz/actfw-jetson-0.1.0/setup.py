# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['actfw_jetson', 'actfw_jetson.test']

package_data = \
{'': ['*']}

install_requires = \
['actfw-gstreamer']

setup_kwargs = {
    'name': 'actfw-jetson',
    'version': '0.1.0',
    'description': "actfw's additional components for Jetson series",
    'long_description': '# actfw-jetson\n\nactfw\'s components for Jetson series.\nactfw is a framework for Actcast Application written in Python.\n\n## Installation\n\n```console\nsudo apt-get update\nsudo apt-get install -y python3-pip python3-pil \n\n# Install GStreamer dependencies (some components in actfw-jetson uses GStreamer in implementation)\nsudo apt-get install -y libgstreamer1.0-dev libgirepository1.0-dev ibgstreamer-plugins-base1.0-dev libglib2.0-dev libcairo2-dev\n\npip3 install actfw-jetson\n```\n\n## Document\n\n- [API References](https://idein.github.io/actfw-jetson/latest/)\n\n## Usage\n\nSee [actfw-core](https://github.com/Idein/actfw-core) for basic usage.\n\nSince actfw-jetson uses GStreamer to implement some components, an application using actfw-jetson may have to initialize GStreamer library before using actfw-jetson\'s components.\n\n```python\nif __name__ == \'__main__\':\n    import gi\n    gi.require_version(\'Gst\', \'1.0\')\n    from gi.repository import Gst\n    Gst.init(None)\n\n    main()\n```\n\nactfw-jetson provides:\n\n- `actfw_jetson.Display` : Display using `nvoverlaysink` element in [NVIDIA\'s Accelerated GStreamer](https://docs.nvidia.com/jetson/l4t/index.html#page/Tegra%20Linux%20Driver%20Package%20Development%20Guide/accelerated_gstreamer.html).\n\n## Example\n\n- `example/hello_jetson` : The simplest application example for Jetson\n  - Use HDMI display as 1280x720 area\n  - Generate 1280x720 single-colored image\n  - Draw "Hello, Actcast!" text\n  - Display it as 1280x720 image\n  - Notice message for each frame\n  - Support application heartbeat\n  - Support "Take Photo" command\n  - Depends: fonts-dejavu-core\n\n## Development Guide\n\n### Installation of dev requirements\n\n```console\ncurl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -\npoetry install\n```\n\n### Running tests\n\n```console\npoetry run nose2 -v\n```\n\n### Running examples\n\n#### hello_jetson\n\nDisplays a red rectangle and greeting text on it on HDMI display.\n\nRun on a Jetson Nano connected to HDMI display:\n\n```console\napt-get install fonts-dejavu-core\npoetry run python example/hello_jetson\n```\n\n#### camera_display\n\nDisplays camera input on HDMI display.\n\nRun on a Jetson Nano with CSI camera and HDMI display:\n\n```console\npoetry run python example/camera_display\n```\n\n### Releasing package & API doc\n\nCI will automatically do.\nFollow the following branch/tag rules.\n\n1. Make changes for next version in `master` branch (via pull-requests).\n2. Update `version` field in `pyproject.toml` with new version in `master` branch.\n3. Create Git tag from `master` branch\'s HEAD named `release-<New version>`. E.g. `release-1.4.0`.\n4. Then CI will build/upload package to PyPI & API doc to GitHub Pages.\n',
    'author': 'Idein Inc.',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Idein/actfw-jetson',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
