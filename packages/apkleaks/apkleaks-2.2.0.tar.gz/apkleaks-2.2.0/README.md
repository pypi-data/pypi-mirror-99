# APKLeaks
[![version](https://badge.fury.io/gh/dwisiswant0%2fapkleaks.svg)](https://badge.fury.io/gh/dwisiswant0%2fapkleaks.svg)
[![contributions](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/dwisiswant0/apkleaks/issues)

Scanning APK file for URIs, endpoints & secrets.

<img src="https://user-images.githubusercontent.com/25837540/111854909-73eb7100-8954-11eb-8caf-d00d9f0b68f6.png" alt="APKLeaks" height="400">

---

- [Installation](#installation)
- [Usage](#usage)
- [Version](#version)
- [Legal](#legal)
- [Acknowledments](#acknowledments)

---

## Installation

It's fairly simple to install **APKLeaks**:

### from PyPi

```bash
$ pip3 install git+https://github.com/dwisiswant0/apkleaks
```

### from Source

Clone repository and install requirements:

```bash
$ git clone https://github.com/dwisiswant0/apkleaks
$ cd apkleaks/
$ pip3 install -r requirements.txt
```

### from Docker

Pull the Docker image by running:

```bash
$ docker pull dwisiswant0/apkleaks:latest
```

### Dependencies

APKLeaks using [jadx](https://github.com/skylot/jadx) disassembler to decompile APK file. If it doesn't exist in your environment, it'll ask you to download or nah.

## Usage

Simply,

```bash
$ apkleaks -f ~/path/to/file.apk
# from Source
$ python3 apkleaks.py -f ~/path/to/file.apk
# or with Docker
$ docker run -it --rm -v /tmp:/tmp apkleaks:latest -f /tmp/diva.apk
```

### Options

```console
$ apkleaks -h
usage: apkleaks [-h] -f FILE [-o OUTPUT] [-p PATTERN] [--json]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  APK file to scanning
  -o OUTPUT, --output OUTPUT
                        Write to file results (random if not set)
  -p PATTERN, --pattern PATTERN
                        Path to custom patterns JSON
  --json                Save as JSON format
```

In general, if you don't provide `-o` argument, then it will generate results file automatically.

Custom patterns can be added with the following flag `--pattern /path/to/rules.json` to provide sensitive _search rules_ in the JSON file format. If not set, it'll use default patterns from [regexes.json](https://github.com/dwisiswant0/apkleaks/blob/master/config/regexes.json) file.

Example patterns file:

```json
// rules.json
{
  "Amazon AWS Access Key ID": "AKIA[0-9A-Z]{16}",
  ...
}
```

```
$ apkleaks -f /path/to/file.apk -p rules.json -o ~/Documents/apkleaks-results.txt
```

## Known Bugs

- Empty results on Windows ([#24](https://github.com/dwisiswant0/apkleaks/issues/24)).

## Legal

`apkleaks` is distributed under Apache 2.

## Acknowledments

Since this tool includes some contributions, and I'm not an asshole, I'll publically thank the following users for their helps and resources:

- [@ndelphit](https://github.com/ndelphit) - for his inspiring `apkurlgrep`, that's why this tool was made.
- [@dxa4481](https://github.com/dxa4481) and y'all who contribute to `truffleHogRegexes`.
- [@GerbenJavado](https://github.com/GerbenJavado) & [@Bankde](https://github.com/Bankde) - for awesome pattern to discover URLs, endpoints & their parameters from `LinkFinder`.
- [@tomnomnom](https://github.com/tomnomnom/gf) - a `gf` patterns.
- [@pxb1988](https://github.com/pxb1988) - for awesome APK dissambler `dex2jar`.
- [@subho007](https://github.com/ph4r05) for standalone APK parser.
- `SHA2048#4361` _(Discord user)_ that help me porting code to Python3.
- [@Ry0taK](https://github.com/Ry0taK) because he had reported an [OS command injection bug](https://github.com/dwisiswant0/apkleaks/security/advisories/GHSA-8434-v7xw-8m9x).
- [All contributors](https://github.com/dwisiswant0/apkleaks/graphs/contributors).