# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['summarytools']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'summarytools',
    'version': '0.1.3',
    'description': 'This is a port of the summarytools library in R. It provides a simple exploratory data analysis report of a pandas dataframe.',
    'long_description': "# DataFrame Summary Tools in Jupyter Notebook\n\nThis is python version of `summarytools`, which is used to generate standardized and comprehensive summary of dataframe in Jupyter Notebooks.\n\nThe idea is originated from the `summarytools` R package (https://github.com/dcomtois/summarytools).\n\nSee Github repo for more info: https://github.com/6chaoran/jupyter-summarytools\n\n* Only `dfSummary` function is made available for now\n* Added two html widgets to avoid displaying lengthy content\n    + [collapsible summary](#collapsible-summary) \n    + [tabbed summary](#tabbed-summary)\n\n## Dependencies\n1. python 3.6+\n2. packages in [requirements.txt](./requirements.txt)\n\n# Quick Start\n\nthe quick-start notebook is available in [here](quick-start.ipynb)\n\nout-of-box `dfSummary` function will generate a HTML based data frame summary.\n\n```py\nimport pandas as pd\nfrom summarytools import dfSummary\ntitanic = pd.read_csv('./data/titanic.csv')\ndfSummary(titanic)\n```\n![](images/dfSummary.png)\n\n## collapsible summary\n\n```py\nimport pandas as pd\nfrom summarytools import dfSummary\ntitanic = pd.read_csv('./data/titanic.csv')\ndfSummary(titanic, is_collapsible = True)\n```\n\n![](images/collapsible.gif)\n\n## tabbed summary\n\n```py\nimport pandas as pd\nfrom summarytools import dfSummary, tabset\ntitanic = pd.read_csv('./data/titanic.csv')\nvaccine = pd.read_csv('./data/country_vaccinations.csv')\nvaccine['date'] = pd.to_datetime(vaccine['date'])\n\ntabset({\n    'titanic': dfSummary(titanic).render(),\n    'vaccine': dfSummary(vaccine).render()})\n```\n\n![](images/tabbed.gif)\n\n# Export notebook as HTML\n\nwhen export jupyter notebook to HTML, make sure `Export Embedded HTML\n` extension is installed and enabled.\n\n![](images/embedded_html.png)\n\nUsing the following bash command to retain the data frame summary in exported HTML.\n```bash\njupyter nbconvert --to html_embed path/of/your/notebook.ipynb\n```\n",
    'author': '6chaoran',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/6chaoran/jupyter-summarytools',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
