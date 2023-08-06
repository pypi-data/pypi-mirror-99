Threat Bus CIFv3 Plugin
======================

<h4 align="center">

[![PyPI Status][pypi-badge]][pypi-url]
[![Build Status][ci-badge]][ci-url]
[![License][license-badge]][license-url]

</h4>

A Threat Bus plugin to push indicators from Threat Bus to
[Collective Intelligence Framework v3](https://github.com/csirtgadgets/bearded-avenger).

The plugin uses the [cifsdk (v3.x)](https://pypi.org/project/cifsdk/) Python
client to submit indicators received from Threat Bus into a CIFv3 instance.

The plugin breaks with the pub/sub architecture of Threat Bus, because CIF does
not subscribe itself to the bus. Instead, the plugin actively contacts a CIF
endpoint.

## Installation

```sh
pip install threatbus-cif3
```

## Configuration

Configure this plugin by adding a section to Threat Bus' `config.yaml` file, as
follows:

```yaml
...
plugins:
  cif3:
    api:
      host: http://cif.host.tld:5000
      ssl: false
      token: CIF_TOKEN
    group: everyone
    confidence: 7.5
    tlp: amber
    tags:
      - test
      - malicious
...
```

## Development Setup

The following guides describe how to set up local, dockerized instances of CIF.

### Dockerized CIFv3

Use [dockerized CIFv3](https://github.com/sfinlon/cif-docker) to set
up a local CIFv3 environment:

*Setup a CIFv3 docker container*

```sh
git clone https://github.com/sfinlon/cif-docker.git
cd cif-docker
docker-compose build
```

*Edit the docker-compose.yml*

```sh
vim docker-compose.yml
```
Find the section `cif` in the configuration and edit the following as
appropriate to bind port 5000 to your localhost:

```yaml
cif:
    ...
    ports:
      - "5000:5000"
    ...
```


*Start the container*

```sh
docker-compose up -d
# Get an interactive shell in the container:
docker-compose exec cif /bin/bash
# Become the cif user:
su cif
# check to see if access tokens were successfully created. Copy the `admin`
# token to the CIF config section:
cif-tokens
# Ping the router to ensure connectivity:
cif --ping
```

## License

Threat Bus comes with a [3-clause BSD license][license-url].

[pypi-badge]: https://img.shields.io/pypi/v/threatbus-cif3.svg
[pypi-url]: https://pypi.org/project/threatbus-cif3
[ci-url]: https://github.com/tenzir/threatbus/actions?query=branch%3Amaster
[ci-badge]: https://github.com/tenzir/threatbus/workflows/Python%20Egg/badge.svg?branch=master
[license-badge]: https://img.shields.io/badge/license-BSD-blue.svg
[license-url]: https://github.com/tenzir/threatbus/blob/master/COPYING
