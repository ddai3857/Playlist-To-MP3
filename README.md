**Purpose**

    This is a python script that downloads all the videos of a youtube playlist into mp3 files

**Requirements (API key): Because this script accesses Youtube's database, you will need obtain an API key from Google**

    Corey Schafer has a great video on how to obtain an API key (https://www.youtube.com/watch?v=th5_9woFJmk&t=1083s&ab_channel=CoreySchafer)

**Dependencies (pip install)**

    python-dotenv (You don't have to create a python environment if you really don't want to)
    google-api-python-client
    google-auth-oauthlib
    selenium

**Details**
1. Every playlist on YouTube has a playlist id. You can find it by locating the random combination of letters, numbers, and symbols after the "=" sign in the url of the playlist. (Make sure the playlist is public)
2. The python script will collect all the videos from the playlist and grab their urls.
3. A webscraper (Selenium) is then used to download the audio from the videos as mp3 files using https://cobalt.tools (terminal will show download progress)
4. Access mp3s in the mp3_folder


**Notes**

    If you want to convert a public playlist, just save it to your account
    It will show up when you are prompted to select a playlist

**Goal**

    Gain experience with APIs and using Python Selenium
