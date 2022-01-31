#!/usr/bin/env python3

import requests
import platform
import pwd
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
FILENAME = 'nasa_pic.png'
url = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}"


def get_filename():
    username = pwd.getpwuid(os.getuid()).pw_name
    if platform.system() == 'Linux':
        directory = f"/home/{username}/Downloads"
    elif platform.system() == 'Windows':
        directory = f"C:\\Users\\{username}\\Downloads"
    elif platform.system() == "Darwin":
        directory = "/Users/" + username + "/Downloads/"

    return os.path.join(directory, FILENAME)


def download_pic():
    r = requests.get(url)

    if r.status_code != 200:
        print('error: {}'.format(r.status_code))
        print(r.text)
        return

    picture_url = r.json()['hdurl']
    if "jpg" not in picture_url:
        print("No image for today, must be a video")
    else:
        pic = requests.get(picture_url, allow_redirects=True)
        filename = get_filename()

        open(filename, 'wb').write(pic.content)

        print(f"saved picture of the day to {filename}!")


if __name__ == '__main__':
    download_pic()

    filename = get_filename()

    if platform.system() == 'Linux':
        cmd = "gsettings set org.gnome.desktop.background picture-uri file://" + filename
    elif platform.system() == 'Windows':
        cmd = f"start ms-settings:backgroundimagefile={filename}"
    elif platform.system() == "Darwin":
        cmd = "osascript -e 'tell application \"Finder\" to set desktop picture to POSIX file \"" + filename + "\"'"

    os.system(cmd)
    print("set desktop background to {}".format(filename))
