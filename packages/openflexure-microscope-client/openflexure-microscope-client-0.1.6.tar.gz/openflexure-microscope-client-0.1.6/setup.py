# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openflexure_microscope_client']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=7.0,<8.0',
 'numpy>=1.17,<2.0',
 'requests>=2.22,<3.0',
 'zeroconf>=0.25,<0.26']

setup_kwargs = {
    'name': 'openflexure-microscope-client',
    'version': '0.1.6',
    'description': 'Python client code for the OpenFlexure Microscope',
    'long_description': '# A Python client for the OpenFlexure Microscope.  \n\nThe [OpenFlexure Microscope] is most often controlled by two pieces of software - the [OpenFlexure Microscope Server], which is written in Python and runs on the embedded Raspberry Pi, and [OpenFlexure Connect][Connect] which is a graphical interface written in Electron, that can be run either on the Raspberry Pi, or on another computer via a network connection.  However, if you want to write your own scripts to perform particular experiments or protocols, it\'s useful not to have to embed these into the the [OpenFlexure Microscope Server] or package them up as plugins.  This library exists to make it easy to control your microscope from a simple Python script that can run either on the Raspberry Pi, or over the network.  I particularly like to use it from a [Jupyter] notebook on my laptop, because it allows me to plot graphs and display images as I go.\n\n## Installation\n\nThis module can be installed with ``pip install openflexure-microscope-client``, or by cloning the repository and running ``poetry install``.\n\n## Usage\n\n### Connect to your microscope\nYou can connect to the microscope either by specifying a hostname or IP address, or using mDNS.  If your network is relatively simple, and if you can see your microscope in the "nearby devices" section of [Connect], then mDNS is a zero-faff way of connecting to your microscope:\n```python\nimport openflexure_microscope_client as ofm_client\nmicroscope = ofm_client.find_first_microscope()\n```\nIf your network is more complicated, or you know the address of your microscope, you can connect using the hostname or IP address.  By default, your microscope will declare itself as ``microscope.local`` though this also relies on mDNS so if the method above doesn\'t work, ``microscope.local`` may also not work.  \n```python\nmicroscope = ofm_client.MicroscopeClient("example.host.name")\n```\n\n### Check the connection\nUsually, I run a few commands to check my microscope is working properly:\n```python\npos = microscope.position\nstarting_pos = pos.copy()\npos[\'x\'] += 100\nmicroscope.move(pos)\nassert microscope.position == pos\npos[\'x\'] -= 100\nmicroscope.move(pos)\nassert microscope.position == starting_pos\n\n# Check the microscope will autofocus\nret = microscope.autofocus()\n\n# Acquire an image for sanity-checking too\nimage = microscope.grab_image()\nf, ax = plt.subplots(1,1)\nax.imshow(np.array(image))\n#print(image.metadata)\nprint("Active microscope extensions")\nfor k in microscope.extensions.keys():\n    print(k)\n```\nAfter running this block, you should see a list of extensions that are currently active, and a picture taken by the microscope.  Given that we just autofocused, this image should be nice and sharp!\n\n### Basic commands\nThere are a few basic commands built in as methods of the ``MicroscopeClient`` object:\n  * ``position`` is a property that returns a dictionary with ``\'x\'``, ``\'y\'``, and ``\'z\'`` components, giving the position of the stage.\n  * ``get_position_array()`` returns a 3-element ``numpy`` array with the same position in it.\n  * ``move(position)`` accepts either a 3-element array or a dictionary as returned by ``position``, and performs an absolute move\n  * ``move_rel(displacement)`` performs a relative move (i.e. supplying 0 will not move that axis)\n  * ``capture_image()`` will take a new image from the camera and return it as a ``PIL`` image object\n  * ``grab_image()`` will return the next image the camera sends in its MJPEG preview stream (i.e. it\'s quicker but lower quality than ``capture_image()``)\n  * ``grab_image_array()`` returns the image as a ``numpy`` array.\n  * ``autofocus()`` runs the fast autofocus routine, just like clicking the "autofocus" button in [Connect]\n\n### Extensions\nTo run methods provided by the microscope extensions, you can use the ``extensions`` dictionary, to make ``get`` or ``post`` requests:\n```python\nmicroscope.extensions["your.extension.name"]["link_name"].get()\nmicroscope.extensions["your.extension.name"]["link_name"].post_json({"key":"value"})\n```\n\n## Development\n### Installation\nThe dependencies are managed using poetry, so once you have cloned the repository, you can set up a virtual environment with ``poetry install``.\n\n### Tests\nThere are some basic tests that can be run using ``pytest``.  This needs to be within the environment installed above, so use ``poetry run pytest``.  These mostly need to connect to a microscope; the easiest way to test this automatically is to build ``openflexure-microscope-server`` and run it locally - this will create a local dummy microscope server.  Some tests will be skipped because they need microscope hardware, but it should at least verify most of the URLs.  Running the tests requires you to have started that server already - it will not be started automatically.\n\n[OpenFlexure Microscope]: https://openflexure.org/projects/microscope/\n[Connect]: https://gitlab.com/openflexure/openflexure-connect\n[OpenFlexure Microscope Server]: https://gitlab.com/openflexure/openflexure-microscope-server/\n[Jupyter]: https://jupyter.org/',
    'author': 'Richard Bowman',
    'author_email': 'richard.bowman@cantab.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/openflexure/openflexure-microscope-pyclient/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
