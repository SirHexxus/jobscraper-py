#!/usr/bin/env bash

# create a file named products.json if it doesn't exist
if [ ! -f products.json ]; then
    echo '[]' > products.json
fi

# create a .env file if it doesn't exist, and put empty values in it
if [ ! -f .env ]; then
    echo 'SENDER=' > .env
    echo 'PASS=' >> .env
    echo 'API_KEY=' >> .env
fi

# use pip3 to install python-dotenv, requests, clipboard, pyperclip, lxml, and bs4
pip3 install python-dotenv requests clipboard pyperclip lxml bs4

# set all .py files to executable
chmod +x *.py