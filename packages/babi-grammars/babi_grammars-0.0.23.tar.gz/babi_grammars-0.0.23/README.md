[![Build Status](https://dev.azure.com/asottile/asottile/_apis/build/status/asottile.babi-grammars?branchName=master)](https://dev.azure.com/asottile/asottile/_build/latest?definitionId=63&branchName=master)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/asottile/babi-grammars/master.svg)](https://results.pre-commit.ci/latest/github/asottile/babi-grammars/master)

babi-grammars
=============

grammars for babi

## installation

`pip install babi-grammars`

### licenses

the licenses for the individual grammars are included in the `licenses`
directory.  the license for this repository is available in the `LICENSE` file


### (internal/contributing instructions)

to add a grammar:
- add it to the `REPOS` list in `./bin/download-syntax`
    - if you want the latest, use `version='HEAD'` and then run
      `./bin/download-syntax update --only repo/name` to freeze it
- run `./bin/download-syntax download --only repo/name`

to update all the grammars
- run `./bin/download-syntax update`
- then run `./bin/download-syntax download`
