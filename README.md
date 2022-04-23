# MEMO

*Repository is under development*

> Application that will run on a raspberry pi SBC to help with Memories in art


## Setup

This project works with python 3.9.x.
You can check your python version with the following command:

```sh
python3 --version
```

#### if on GNU/Linux

```sh
sudo apt install python3.9
```

#### if on Windows

Get it from https://www.python.org/downloads/ .


### Install virtualenv

```sh
sudo apt install python3-virtualenv
```

### Fetch the repository with git clone

Create a new directory for the project and enter it.

```sh
mkdir -p ~/proj/
cd ~/proj/memo/
```

Get the repository with git.

```sh
git clone https://github.com/tiandti/MEMO.git
cd memo
```

### Create a virtual environment

```sh
virtualenv -p python3.9 .venv
```

### Get inside the invironment

#### if on GNU/Linux
```sh
source .venv/bin/activate
```

#### if on windows
```sh
.venv\Scripts\activate.bat
```

### Update pip
```sh
python -m pip install --upgrade pip
```

### Install requirements.txt
```sh
pip install -r requirements.txt
```

## Run it

### Receiver

```sh
python main.py -d -f
```

### Transmitter

```sh
python main.py
```
