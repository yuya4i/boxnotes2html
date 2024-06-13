# convBoxNotes

It is difficult to search "Box notes documents" quickly.`convBoxNotes` is a tool to convert "Box notes documents" to html, markdown bulk process with `boxnotes2html` OSS.

## Installation

This tool is available for both MAC and Windows with WSL1 or WSL2. If you use it on Windows, you need to install WSL1 or WSL2 in order to use shell(bash).

0. Python 3 is required.
1. Move to ```boxnote2converter```. (This souce code using alexwennerberg's [boxnotes2html](https://github.com/alexwennerberg/boxnotes2html))
2. Setup the repo using poetry:
```shell
python3 -m pip install poetry
poetry install
```


## Usage

```Shell
./convBoxNotes.sh <-h|-x>  <directory path where *.boxnotes are stored>
```

automatically saved in ```<directory path where *.boxnotes are stored>/output/```