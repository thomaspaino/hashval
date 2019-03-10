# hashval
Quickly verify a file hash.

## Requirements
- python 3.4+

## Usage
After cloning the repository, copy/symlink the python file to your local bin directory, eg:
```sh
$ sudo ln -sv ~/github/hashval/hashval.py /usr/local/bin/hashval
```

The script only takes two arguments: **filename** and **hash**
```sh
$ hashval ~/isolinux/archlinux-2019.03.01-x86_64.iso e32acb5a7b7cfb2bdba10697cce48ab69e13c186
INFO  Hashing algorithm is SHA1
INFO  Computed SHA1 hash: e32acb5a7b7cfb2bdba10697cce48ab69e13c186
INFO  Hashes match: VALIDATED! :)
$
```
