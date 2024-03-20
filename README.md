**Requirements (API key): Because this script accesses Youtube's database, you will need obtain an API key from Google**

    Corey Schafer has a great video on how to obtain an API key (it's the first 4 minutes)
    [https://www.youtube.com/watch?v=th5_9woFJmk&t=1083s&ab_channel=CoreySchafer]

    When you open the main.py file, there will be a comment on where to paste in your api key

**Dependencies (pip install)**

    google-api-python-client
    google-auth-oauthlib
    selenium

**Details**
1. You will be prompted to enter the url of the playlist you want to use (MAKE SURE YOUR PLAYLIST IS PUBLIC)
2. The python script will collect all the videos from the playlist and grab their urls
3. A webscraper (Selenium) is then used to download the audio from the videos as mp3 files using https://cobalt.tools (terminal will show download progress)
4. Access the new mp3 files in the mp3_folder
