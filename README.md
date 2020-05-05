## Four Souls Card Downloader

This script fetches and downloads The Binding of Isaac Four Souls card art from http://pop-life.com/foursouls. In order to download a card, the script requires a JSON file which contains all card links. This file is committed (`cards.json`) and used by default, but this file can be fetched manually using the `fetch` command (or alternatively, a different filename can be passed using the `--file` flag).
To download a card use the `download` command, you can either pass `--all` to download all cards defined within `cards.json`, or pass one/multiple `--card` arguments to the command, with the desired card name.

### Usage

```bash
$ ./main.py --help
usage: main.py [-h] [-j FILE] [-s START] [-e END] {fetch,download} ...

Binding of Isaac Four Souls card downloader

positional arguments:
  {fetch,download}
    fetch               fetch card data (do not download)
    download            download cards

optional arguments:
  -h, --help            show this help message and exit
  -j FILE, --file FILE  JSON file to dump data to
  -s START, --start START
                        ID of first card in range
  -e END, --end END     ID of last card in range
```

#### fetch

```bash
$ ./main.py fetch --help
usage: main.py fetch [-h] [-f]

Fetch card data and dump it to a file. This file needs to exist before
downloading cards is possible

optional arguments:
  -h, --help   show this help message and exit
  -f, --force  ignore existing json file file (default: False)
```

#### download
```bash
$ ./main.py download --help
usage: main.py download [-h] (-a | -c CARD [CARD ...])

Download card art, specify either '--all', or multiple '--card' arguments

optional arguments:
  -h, --help            show this help message and exit
  -a, --all             download all available cards
  -c CARD [CARD ...], --card CARD [CARD ...]
                        name of card to download
```

### Examples:

```bash
# force fetch all cards
$ ./main.py fetch -f
```

```bash
# fetch only ids 200-300 to an alternative file
$ ./main.py -s 200 -e 300 --file new.json fetch
```

```bash
# download all cards
$ ./main.py download --all
```

```bash
# download cards matching 'cent' and all cards matching 'mom'
$ ./main.py download -c cent -c mom
```
