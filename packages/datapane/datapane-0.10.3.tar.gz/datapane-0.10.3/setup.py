# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['datapane',
 'datapane.client',
 'datapane.client.api',
 'datapane.client.api.report',
 'datapane.client.scripts',
 'datapane.common',
 'datapane.resources',
 'datapane.resources.local_report',
 'datapane.resources.report_def',
 'datapane.resources.templates',
 'datapane.resources.templates.report_py',
 'datapane.resources.templates.script',
 'datapane.runner']

package_data = \
{'': ['*'], 'datapane.resources.templates': ['report_ipynb/*']}

install_requires = \
['PyYAML>=5.1.0,<6.0.0',
 'altair>=4.0.0,<5.0.0',
 'bleach>=3.0.2,<4.0.0',
 'boltons>=20.0.0,<21.0.0',
 'click-spinner>=0.1.8,<0.2.0',
 'click>=7.0.0,<8.0.0',
 'colorlog>=4.0.2,<5.0.0',
 'dacite>=1.0.2,<2.0.0',
 'dominate>=2.4.0,<3.0.0',
 'flit-core>=3.0.0,<3.1.0',
 'furl>=2.0.0,<3.0.0',
 'glom>=20.5.0,<21.0.0',
 'importlib_resources>=5.0.0,<6.0.0',
 'jinja2>=2.10.0,<3.0.0',
 'jsonschema>=3.0.0,<4.0.0',
 'lxml>=4.0.0,<5.0.0',
 'micawber>=0.5.0',
 'munch>=2.3.0,<3.0.0',
 'nbconvert>=6.0.0,<7.0.0',
 'numpy>=1.16.5,<2.0.0',
 'packaging>=20.0.0,<21.0.0',
 'pandas>=1.0.1,<2.0.0',
 'pyarrow>=3.0.0,<4.0.0',
 'requests-toolbelt>=0.9.1,<0.10.0',
 'requests>=2.19.0,<3.0.0',
 'stringcase>=1.2.0,<2.0.0',
 'tabulate>=0.8.0,<0.9.0',
 'toolz>=0.11.0,<0.12.0',
 'validators>=0.17.1']

extras_require = \
{'plotting': ['matplotlib>=3.0.0,<4.0.0',
              'plotly>=4.0.0,<5.0.0',
              'bokeh>=2.2.0,<2.3.0',
              'folium>=0.12.0,<0.13.0']}

entry_points = \
{'console_scripts': ['datapane = datapane.client.__main__:main',
                     'dp-runner = datapane.runner.__main__:main']}

setup_kwargs = {
    'name': 'datapane',
    'version': '0.10.3',
    'description': 'Datapane client library and CLI tool',
    'long_description': '<p align="center">\n  <a href="https://datapane.com">\n    <img src="https://datapane.com/static/datapane-logo-dark.png" width="250px" alt="Datapane" />\n  </a>\n</p>\n<p align="center">\n    <a href="https://datapane.com">Datapane.com</a> |\n    <a href="https://datapane.com/enterprise">Datapane Enterprise</a> |\n    <a href="https://docs.datapane.com">Documentation</a> |\n    <a href="https://datapane.github.io/datapane/">API Docs</a> |\n    <a href="https://twitter.com/datapaneapp">Twitter</a> |\n    <a href="https://blog.datapane.com">Blog</a>\n    <br /><br />\n    <a href="https://pypi.org/project/datapane/">\n        <img src="https://img.shields.io/pypi/dm/datapane?label=pip%20downloads" alt="Pip Downloads" />\n    </a>\n    <a href="https://pypi.org/project/datapane/">\n        <img src="https://img.shields.io/pypi/v/datapane?color=blue" alt="Latest release" />\n    </a>\n    <a href="https://anaconda.org/conda-forge/datapane">\n        <img alt="Conda (channel only)" src="https://img.shields.io/conda/vn/conda-forge/datapane">\n    </a>\n</p>\n\nDatapane is a Python library which makes it simple to build reports from the common objects in your data analysis, such as pandas DataFrames, plots from Python visualisation libraries, and Markdown.\n\nReports can be exported as standalone HTML documents, with rich components which allow data to be explored and visualisations to be used interactively.\n\nFor example, if you wanted to create a report with a table viewer and an interactive plot:\n\n```python\nimport pandas as pd\nimport altair as alt\nimport datapane as dp\n\ndf = pd.read_csv(\'https://covid.ourworldindata.org/data/vaccinations/vaccinations-by-manufacturer.csv\', parse_dates=[\'date\'])\ndf = df.groupby([\'vaccine\', \'date\'])[\'total_vaccinations\'].sum().reset_index()\n\nplot = alt.Chart(df).mark_area(opacity=0.4, stroke=\'black\').encode(\n    x=\'date:T\',\n    y=alt.Y(\'total_vaccinations:Q\'),\n    color=alt.Color(\'vaccine:N\', scale=alt.Scale(scheme=\'set1\')),\n    tooltip=\'vaccine:N\'\n).interactive().properties(width=\'container\')\n\ntotal_df = df[df["date"] == df["date"].max()].sort_values("total_vaccinations", ascending=False).reset_index(drop=True)\ntotal_styled = total_df.style.bar(subset=["total_vaccinations"], color=\'#5fba7d\', vmax=total_df["total_vaccinations"].sum())\n\ndp.Report("## Vaccination Report",\n    dp.Plot(plot, caption="Vaccinations by manufacturer over time"),\n    dp.Table(total_styled, caption="Current vaccination totals by manufacturer")\n).save(path=\'report.html\', open=True)\n```\n\nThis would package a standalone HTML report such as the following, with a searchable DataTable and Plot component.\n\n![Report Example](https://imgur.com/PTiSCM0.png)\n\n# Getting Started\n\n## Install\n\n- `pip3 install datapane` OR\n- `conda install -c conda-forge "datapane>=0.10.0"`\n\n## Next Steps\n\n- [Read the documentation](https://docs.datapane.com)\n- [Browse the API docs](https://datapane.github.io/datapane/)\n- [Browse samples and demos](https://github.com/datapane/gallery/)\n- [View featured reports](https://datapane.com/explore/?tab=featured)\n\n# Datapane.com\n\nIn addition to saving reports locally, [Datapane](datapane.com) provides a free hosted platform and social network at https://datapane.com, including the following features:\n\n- published reports can kept private and securely shared,\n- reports can be shared publicly and become a part of the wider data stories community,\n- report embedding within your blogs, CMSs, and elsewhere (see [here](https://docs.datapane.com/reports/embedding-reports-in-social-platforms)),\n- explorations and integrations, e.g. additional DataTable analysis features and [GitHub action](https://github.com/datapane/build-action) integration.\n\nIt\'s super simple, just login (see [here](https://docs.datapane.com/tut-getting-started#authentication)) and call the `publish` function on your report,\n\n```python\nr = dp.Report(dp.DataTable(df), dp.Plot(chart))\nr.publish(name="2020 Stock Portfolio", open=True)\n```\n\n# Enterprise\n\n[Datapane Enterprise](https://datapane.com/enterprise/) provides automation and secure sharing of reports within in your organization.\n\n- Private report sharing within your organization and within groups, including external clients\n- Deploy Notebooks and scripts as automated, parameterised reports that can be run by your team interactively\n- Schedule reports to be generated and shared\n- Runs managed or on-prem\n- [and more](<(https://datapane.com/enterprise/)>)\n\n# Joining the community\n\nLooking to get answers to questions or engage with us and the wider community? Check out our [GitHub Discussions](https://github.com/datapane/datapane/discussions) board.\n\nSubmit requests, issues, and bug reports on this GitHub repo.\n\nWe look forward to building an amazing open source community with you!\n',
    'author': 'Datapane Team',
    'author_email': 'dev@datapane.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.datapane.com',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
