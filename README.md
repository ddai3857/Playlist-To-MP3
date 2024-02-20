Goal:
- Gain experience with accessing APIs and using Python Selenium

Purpose:
- This is a python script that takes a youtube playlist and creates a folder named "mp3_folder" that has all the videos in the playlist converted to mp3s.

Details:
- The script will first ask you to login as a new_user. This is because if you have logged in before already, the script will save a token to your previous login (it does not know your username or password so don't worry)
- Then it will list out all the playlists on your account and number them starting from #1. You will have to input a number corresponding to the playlists. (Inputting an invalid number will force you to pick another one)
- The script will then find all the video urls. Selenium will open a chrome tab and go to https://cobalt.tools/ in order to convert the urls to mp3s
- The newly downloaded mp3s can be found in the folder called "mp3_folder" in the same directory

Notes:
- If a video is too long (like over an hour), it may end up crashing

Next Steps:
- I guess the next step is to copy the mp3 folder into a place where you would want it. (but it seems hard to make it user-friendly)
