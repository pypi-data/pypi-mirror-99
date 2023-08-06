# myb-coinbase-api
 An API client for the Coinbase API

## Installation

The package is availble via PyPi and can be installed with the following command:
```
pip3 install myb-coinbase-api
```

To install it from the repo, clone the repo and cd into the directory:

```
git clone https://github.com/mine-your-business/myb-coinbase-api.git
cd myb-coinbase-api
```

You can install this library with `pip`:

```
pip3 install .
```

## Testing

This project makes use of the [Coinbase API](https://developers.coinbase.com/api/v2) for tests. Unfortunately there does not appear to be a "Sandbox" API at this time for testing endpoints that require authentication. As such, this project does not have tests for those endpoints.

> When tests requiring authentication are implemented, before tests can be run a `local_env_vars.py` file needs to be created in the [`tests`](tests) folder. You can use the [`local_env_vars_example.py`](tests/local_env_vars_example.py) file as an example for the content - just be sure to fill out the API Key data with actual secrets for API keys created on the Coinbase site.

To run tests, simply run the following command:

```
pytest --verbose
```

## Releases

Releases should follow a [Semantic Versioning](https://semver.org/) scheme. 

When changes have been made that warrant a new release that should be published, modify the `__version__` in [`setup.py`](setup.py) 

After the change is merged to the `main` branch, go to [releases](https://github.com/mine-your-business/myb-coinbase-api/releases) and `Draft a new release`. The `Tag version` should follow the pattern `v1.0.0` and should `Target` the `main` branch. 

The `Release title` should not include the `v` from the tag and should have a reasonably detailed description of the new release's changes (or put these details in the description and simply have the version in the title). 

Once the release has been published, the [`.github/workflows/python-publish.yml`](.github/workflows/python-publish.yml) GitHub Actions Workflow should trigger and automatically upload the new version to [PyPi](https://pypi.org/) using GitHub secrets credentials stored with the [Mine Your Business GitHub Organization](https://github.com/mine-your-business).

