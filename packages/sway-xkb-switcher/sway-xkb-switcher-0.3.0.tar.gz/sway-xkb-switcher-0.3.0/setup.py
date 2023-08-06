# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['emacs_sway_xkb', 'sway_xkb_switcher']

package_data = \
{'': ['*']}

install_requires = \
['i3ipc>=2.1.1,<3.0.0']

entry_points = \
{'console_scripts': ['emacs-sway-xkb = emacs_sway_xkb.emacs_sway_xkb:main',
                     'sway-xkb-switcher = sway_xkb_switcher.switcher:main']}

setup_kwargs = {
    'name': 'sway-xkb-switcher',
    'version': '0.3.0',
    'description': 'Keyboard layout switcher for sway windows',
    'long_description': 'sway-xkb-switcher\n===============\n\n## Description\n\nsway-xkb-switcher records keyboard layout for a sway windows when you leave them.\nAnd when you come back it is restore keyboard layout.\n\nThis project is forked from https://github.com/inn0kenty/i3-xkb-switcher\nand adapted to work with sway window manager.\n\nThere is also helper switcher for emacs.\n\nOn layout switch event emacs-sway-xkb tool checks\nif focused window is emacs window.\nIn case of emacs window it switches emacs input method.\n\nIn case of non-emacs window,\nemacs-sway-xkb switches wayland keyboard layout.\n\nNOTE: emacs-sway-xkb is able to only detect emacs native window.\nIf you open emacs frame in terminal,\nit will not detect it.\n\n## Install\n\n```bash\n$ pip install sway-xkb-switcher\n```\n\nAlso you can download compiled binary from [release page](https://github.com/nmukhachev/sway-xkb-switcher/releases).\n\n## Usage\n\n### sway-xkb-switcher\n\n```bash\n$ sway-xkb-switcher\n```\n\nThis will track the layout of all your keyboards.\n\n#### Default layout for new windows\n\nIf you like all your new windows start with default layout,\nyou can specify it with parameter `--default-lang` (`-D`).\n\n```bash\n$ sway-xkb-switcher --default-lang "English (US)"\n```\n\nYou can obtain list of available layout names from running the following `swaymsg` command.\n\n```bash\n$ swaymsg -t get_inputs | grep -A 2 xkb_layout_names\n```\n\nNOTE: Layout names are not literally the same as in sway configuration file.\n\n#### Debugging / logging\n\nTo enable debug mode run with `--debug` key.\n\nBy default it writes logs to stdout. You can specify path by `--log-path` option.\n\n### emacs-sway-xkb\n\nIf you are using emacs you can\nkeep emacs with its own state of input method.\n\nBind some key to switch keyboard layout and\ncompletely disable xkb native switching option\nin your sway config file.\n\n```\ninput "1:1:AT_Translated_Set_2_keyboard" {\n  xkb_layout us,ru\n#  xkb_options grp:alts_toggle,shift:both_capslock\n}\n\nbindsym --to-code $mod+n exec emacs-sway-xkb\n```\n',
    'author': 'Innokenty Lebedev',
    'author_email': None,
    'maintainer': 'Nikolay Mukhachev',
    'maintainer_email': None,
    'url': 'https://github.com/nmukhachev/sway-xkb-switcher',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
