**Purpose**

    This is a python script that allows you to download all the videos from a youtube playlist into mp3 files

**Requirements (client_secret.json): Because this script uses Oauth for you to login to your Google account, you will need a client_secret.json file**
1. Go to https://console.cloud.google.com
2. Go to the APIs & Services section using the the drop-down menu
3. Create a project with any name (you don't need an org)
4. Configure consent screen (Corey Schafer can teach you how to do it in about 4 minutes https://youtu.be/vQQEaSnQ_bs?t=306)
5. Paste the file into the project folder and **you're done**

**Dependencies (pip install)**

    python-dotenv
    google-api-python-client
    google-auth-oauthlib
    selenium

**Details**
1. On the first run of the program, you will have to log in to google
2. The script will save the crendentials token for future runs (IT DOES NOT SAVE YOUR INFORMATION)
3. Playlists will be listed with numbers in the terminal
4. Enter the number corresponding to playlist in the terminal
5. Selenium will download the mp3s using https://cobalt.tools (terminal will show download progress)
6. Access mp3s in the mp3_folder


**Notes**

    If you want to convert a public playlist, just save it to your account and it will show up when you are prompted to select a playlist

**Next Steps**

    I guess the next step is to copy the mp3 folder into a place where you would want it. (but it seems hard to make it user-friendly)

**Goal**

    Gain experience with accessing APIs and using Python Selenium
