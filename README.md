## MEMO

> SOS: Repository under development

# python Version
Raspberry pi: Python 3.9.2
python3 --version

# Install
sudo apt install python3-virtualenv

# Git clone etc
TODO

# Inside the repository
virtualenv -p python3 .venv

# Get inside the invironment
if Windows:   .venv\Scripts\activate.bat
if Raspberry:  source .venv/bin/activate

# Update pip
python -m pip install --upgrade pip

# Install requirements.txt
pip install -r requirements.txt

# Run it
Receiver: python main.py -d
Transmitter: python main.py --bar <path to an image>
