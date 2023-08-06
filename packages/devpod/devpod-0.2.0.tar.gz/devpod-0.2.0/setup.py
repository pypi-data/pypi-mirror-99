# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['devpod']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['devpod = devpod.console:cli']}

setup_kwargs = {
    'name': 'devpod',
    'version': '0.2.0',
    'description': '',
    'long_description': "# DevPod: Rootless, FOSS .DevContainer Tooling\n\nA support framework for using `.devcontainer` on Linux desktops. Let's start\nwith Buildah + Podman + Builder, but the project is open to contributions for\nother IDE integrations.\n\n## Basic Setup and Usage\n\n### Setup\n\n**These instructions should work out of the box on Fedora Silverblue 33+.** \n\n1. Install GNOME Builder (example uses Flatpak, but a normal package works, too):\n\n       flatpak install flathub org.gnome.Builder\n\n1. Install this utility (choosing an alternative to `pip` like `pipx` if you like):\n\n       pip install devpod\n\n### Usage\n\n1. In the CLI, change to the parent directory of `.devcontainer` for your project.\n1. Run the utility (which will *delete* any container with the same name as your project directory):\n\n       devpod launch\n\n1. The `launch` command should list any open ports at the end of the process,\n   but you can also list them using Podman directly:\n   \n       podman port --latest\n\n1. Connect using a Web browser. For example, if the output of `port` is\n   `80/tcp -> 0.0.0.0:12345`, then open a browser to `http://localhost:12345/`.\n\n## Developing DevPod Itself\n\n### Installing the CLI Tool from Local Builds\n\n**These instructions have been tested on Fedora Silverblue 33 but are probably adaptable to other setups.**\n\n1. Install Python package tooling (using a [Toolbox](https://docs.fedoraproject.org/en-US/fedora-silverblue/toolbox/) if desired):\n\n       sudo dnf install poetry pipx\n\n1. Clone the DevPod code and make it your working directory.\n1. Build and (re)install the utility for global use:\n\n       rm -rf dist/ && poetry build && pipx install --force dist/devpod-*.tar.gz\n\n1. The `devpod` command should now be globally available to your user, even\n   outside of any Toolbox.\n\n## Resources\n\n* [.devcontainer Reference Documentation](https://code.visualstudio.com/docs/remote/devcontainerjson-reference)\n* [Podman Commands Documentation](http://docs.podman.io/en/latest/Commands.html)\n* Rootless Podman\n    * [Shortcomings of Rootless Podman](https://github.com/containers/podman/blob/master/rootless.md)\n    * [Volumes and Rootless Podman](https://blog.christophersmart.com/2021/01/31/volumes-and-rootless-podman/)\n    * [User Namespaces, SELinux, and Rootless Containers](https://www.redhat.com/sysadmin/user-namespaces-selinux-rootless-containers)\n",
    'author': 'David Strauss',
    'author_email': 'david@davidstrauss.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/davidstrauss/devpod',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
