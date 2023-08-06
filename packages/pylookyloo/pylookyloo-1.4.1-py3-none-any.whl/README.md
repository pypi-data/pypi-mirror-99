[![Documentation Status](https://readthedocs.org/projects/pylookyloo/badge/?version=latest)](https://pylookyloo.readthedocs.io/en/latest/?badge=latest)

# PyLookyloo

This is the client API for [Lookyloo](https://www.lookyloo.eu).

## Installation

```bash
pip install pylookyloo
```

## Usage

### Command line

You can use the `lookyloo` command to enqueue a URL.

```bash
usage: lookyloo [-h] [--url URL] --query QUERY

Enqueue a URL on Lookyloo.

optional arguments:
  -h, --help     show this help message and exit
  --url URL      URL of the instance (defaults to https://lookyloo.circl.lu/,
                 the public instance).
  --query QUERY  URL to enqueue.
  --listing      Should the report be publicly listed.
  --redirects    Get redirects for a given capture.

The response is the permanent URL where you can see the result of the capture.
```

### Library

See [API Reference](https://pylookyloo.readthedocs.io/en/latest/api_reference.html)
