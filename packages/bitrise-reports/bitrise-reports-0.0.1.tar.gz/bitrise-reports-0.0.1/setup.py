# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bitrise_reports']

package_data = \
{'': ['*']}

install_requires = \
['bandit==1.7.0',
 'black==20.8b1',
 'click==7.1.2',
 'flake8==3.9.0',
 'openpyxl==3.0.7',
 'python-dateutil==2.8.1',
 'requests==2.25.1',
 'rich==9.13.0']

entry_points = \
{'console_scripts': ['bitrise-reports = bitrise_reports:main']}

setup_kwargs = {
    'name': 'bitrise-reports',
    'version': '0.0.1',
    'description': 'The missing tool to extract reports about projects you build on Bitrise',
    'long_description': '# Bitrise Reports\n\n> _Complete blog post to come. Stay tuned!_\n\n## Context\n\nMain features:\n\n- Backed by [Bitrise REST API](https://api-docs.bitrise.io/) under the hood\n- Computes minutes for queued, building and total execution, for all builds in given a time frame\n- Breakdown numbers per machine type (aka Bitrise Build Stack) and also per Workflow\n- Supports emulation of consumed [Bitrise Velocity credits](https://www.bitrise.io/velocity-plan) (for Enterprise customers)\n- Report types : CLI (stdout), JSON and Excel spreadsheet\n\n## Installing\n\nThis tool requires Python, supporting versions 3.8.x and 3.9.x.\n\nInstall `bitrise-reports` with [pip](https://pypi.org/project/pip/)\n\n```bash\n→ pip install bitrise-reports\n```\n\n## Using\n\nLet\'s say you want see analyse numbers for the project `my-app`, learning from\nthe builds that ran during February of 2021. You\'ll firstly need a\n[Bitrise Personal Access Token](https://devcenter.bitrise.io/api/authentication/) for\nthat. Note you must be a member in the project you want to analyse.\n\nBy running\n\n```bash\n→ bitrise-reports \\\n    --token=$BITRISE_PAT_TOKEN \\\n    --app=my-app \\\n    --starting=2021-02-01 \\\n    --ending=2021-02-28\n```\n\nyou should get something like that on your CLI\n\n![](.github/assets/showcase-cli.png)\n\nThe full list CLI options :\n\n| Option   | Details                                    | Required  |\n|----------|--------------------------------------------|-----------|\n| token    | Personal access token for Bitrise API      | Yes       |\n| app      | The title of your app in Bitrise           | Yes       |\n| starting | Starting date in the target time frame     | Yes       |\n| ending   | Ending date in the target time frame       | Yes       |\n| report   | The style of report you want               | No        |\n| velocity | Estimate Bitrise Velocity credits consumed | No        |\n\nwhere\n\n- `starting` and `ending` follows **YYYY-MM-DD** convention\n- `report` accepts **stdout** (default), **json** and **excel**\n- `velocity`is a CLI flag\n\nFor instance, if you want an Excel spreadsheet instead of the fancy CLI UI from the previous example\nwhile also estimating Velocity usage for the builds, you can run\n\n```bash\n→ bitrise-reports \\\n    --token=$BITRISE_PAT_TOKEN \\\n    --app=my-app \\\n    --starting=2021-02-01 \\\n    --ending=2021-02-28 \\\n    --report=excel \\\n    --velocity\n```\n\nand the output file `bitrise-reports.xlsx` will be available in the same folder.\n\n![](.github/assets/showcase-excel.png)\n\n## Contributing\n\nIf you want to contribute with this project\n\n- Check the [contribution guidelines](https://github.com/dotanuki-labs/.github/blob/main/CONTRIBUTING.md)\n- Ensure you have Python 3.8.x or newer installed\n- Ensure you have [Poetry](https://python-poetry.org/) installed\n- Ensure you have [Flake8](https://pypi.org/project/flake8/) installed\n- Ensure you have [Black](https://github.com/psf/black) installed\n- Prepare your environment\n\n```bash\n→ make setup\n```\n\n- Code you changes\n- Make sure you have a green build\n\n```bash\n→  make inspect && make test\n```\n\n- Submit your PR 🔥\n\n## Author\n\n- Coded by Ubiratan Soares (follow me on [Twitter](https://twitter.com/ubiratanfsoares))\n\n## License\n\n```\nThe MIT License (MIT)\n\nCopyright (c) 2021 Dotanuki Labs\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of\nthis software and associated documentation files (the "Software"), to deal in\nthe Software without restriction, including without limitation the rights to\nuse, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of\nthe Software, and to permit persons to whom the Software is furnished to do so,\nsubject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS\nFOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR\nCOPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER\nIN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN\nCONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n```\n',
    'author': 'Ubiratan Soares',
    'author_email': 'ubiratanfsoares@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dotanuki-labs/bitrise-reports',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
