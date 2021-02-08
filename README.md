# targetd-client

targetd-client is a client library for the targetd API.

## Usage

targetd-client is available on PyPI:

```
$ python -m pip install targetd-client
```

Using the library is pretty simple:

```
>>> from targetd_client import TargetdClient
>>> targetd = TargetdClient("https://example.com:18700", "username", "password")
>>> pool_list = targetd.pool_list()
>>> vol_list = targetd.vol_list(pool_list[0]["name"])
>>> ...
```

## `targetdctl`

This projects also ships with the `targetdctl` CLI utility. To use it, you must
first install its dependencies:

```
$ pip install targetd-client[cli]
```

Use `targetdctl --help` to get the list of command lines arguments.

## Contributing

This library is [Free Software](LICENCE) and every contributions are welcome.

Please note that this project is released with a [Contributor Code of
Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to
abide by its terms.
