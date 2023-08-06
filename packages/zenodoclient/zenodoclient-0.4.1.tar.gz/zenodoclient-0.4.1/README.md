# zenodoclient

[![Build Status](https://github.com/shh-dlce/zenodoclient/workflows/tests/badge.svg)](https://github.com/shh-dlce/zenodoclient/actions?query=workflow%3Atests)
[![PyPI](https://img.shields.io/pypi/v/zenodoclient.svg)](https://pypi.org/project/zenodoclient)

Python package to access the Zenodo API ([REST](http://developers.zenodo.org/) and
[OAI-PMH](http://developers.zenodo.org/#oai-pmh)) programmatically and from the command line.


# Install

To install from pypi
```shell
pip install zenodoclient
```

Instructions for a development installation can be found in 
[`CONTRIBUTING.md`](CONTRIBUTING.md).


# Curating deposits

To curate deposits on Zenodo, you need an [access token](https://zenodo.org/account/settings/applications/tokens/new/).
Then you can use the CLI:
```
zenodo --access-token $YOURTOKEN ls
```


# Accessing OAI-PMH feeds

Zenodo disseminates the metadata for communities via OAI-PMH. This metadata
can be accessed programmatically from python as folows:
```python
>>> from zenodoclient.oai import Records
>>> recs = Records('dictionaria')
>>> len(recs)
18
```
We can list the latest version for each Dictionaria dictionary:
```python
>>> import itertools
>>> for d, records in itertools.groupby(sorted(recs, key=lambda r: (r.repos.repos, r.version), reverse=True), lambda r: r.repos.repos):
...     print(d, next(records).tag)
...     
wersing v1.0
tseltal v1.0.1
teop v1.0
sidaama v1.0
sanzhi v1.0
palula v1.0
nen v1.1
medialengua v1.0
kalamang v1.0
hdi v1.1
guarayu v1.0
diidxaza v1.0
daakaka v1.1.1
```
and look at metadata:
```python
>>> recs[0].doi
'10.5281/zenodo.3066952'
>>> recs[0].citation
'Henrik Liljegren. (2019). dictionaria/palula: Palula Dictionary (Version v1.0) [Data set]. Zenodo. http://doi.org/10.5281/zenodo.3066952'
```