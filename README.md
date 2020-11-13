# node-t-checker

![Build](https://github.com/alastria/node-t-checker/workflows/Build/badge.svg)

Application to automatically validate a node in the Alastria T network

## Install and run

```bash
docker-compose up
```

## Launch the tests

``` bash
docker-compose run --rm validator poetry run python -m pytest --cov=validator
```
