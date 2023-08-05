# backwork-backup-consul

Adds support for Consul backups to [`backwork`](https://github.com/IBM/backwork).

## Requirements
This plug-in is build on top of [`consul`](https://www.consul.io/commands),
so you will need to have [`consul`](https://learn.hashicorp.com/tutorials/consul/get-started-install)
installed.

If not, you can install the `consul` cli following the [installation instructions](https://learn.hashicorp.com/tutorials/consul/get-started-install).

## Installing
You can use `pip` to install this plug-in:
```sh
$ pip install backwork-backup-consul
```

## Using
After installing the plug-in you will be able to use the `backup consul` and `restore consul` commands
on `backwork`.


#### `backwork backup consul`

```sh
$ backwork backup consul --help
usage: backwork backup consul [-h] [file]

Backup a Consul cluster. It uses `consul` so it's required to have it installed and added to the system's PATH. You can use any of the arguments supported by `consul snapshot
save`. Use `consul snapshot save --help` for more information.

positional arguments:
  file        output snapshot file name (optional)

optional arguments:
  -h, --help  show this help message and exit
```

You can pass any option that you would normally use on `consul snapshot save`, e.g.:

```sh
$ backwork backup consul -http-addr=http://127.0.0.1:8500
```

The only exception is `-h` which is reserved for the help/usage message.

#### `backwork restore consul`

```sh
$ backwork restore consul --help
usage: backwork restore consul [-h] file

Restore a Consul cluster. Restore a Consul cluster. It uses `consul` so it's required to have it installed and added to the system's PATH. You can use any of the arguments
supported by `consul snapshot restore`. Use `consul snapshot restore --help` for more information.

positional arguments:
  file        input snapshot file name

optional arguments:
  -h, --help  show this help message and exit
```

You can pass any option that you would normally use on `consul snapshot restore`, e.g.:

```sh
$ backwork restore consul --http-addr=http://127.0.0.1:8500
```

The only exception is `-h` which is reserved for the help/usage message.
