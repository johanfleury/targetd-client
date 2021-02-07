# targetd-client

targetd-client is a client library for the targetd API.

## Usage

Using this library is pretty simple:

```
from targetd_client import TargetdClient

targetd = TargetdClient("https://example.com:18700", "username", "password")
print(targetd.vol_list())
```

## Contributing

This library is [Free Software](LICENCE) and every contributions are welcome.

Please note that this project is released with a [Contributor Code of
Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to
abide by its terms.
