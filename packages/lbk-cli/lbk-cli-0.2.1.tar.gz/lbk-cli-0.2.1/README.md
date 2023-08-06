# Logbook CLI

A command line interface for Logbook.

## Development setup

```shell
python3 -m venv venv
pip install < requirements.txt
```

## Publish

### Test PyPi

```shell
python setup.py sdist upload -r testpypi
```

### Official PyPi

```shell
python setup.py sdist upload -r pypi
```
