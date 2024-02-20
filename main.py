import os
import shutil
import pickle
from dotenv import load_dotenv
import re

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import time

def googleLogin():
    credentials = None
    
    while (True):
        new_user = input("Do u want to sign in as a new user? (y/n): ")
        if (new_user == "y"):
            if (os.path.exists("token.pickle")):
                os.remove("token.pickle")
            break
        if (new_user == "n"):
            break
        print("Invalid input")
        print()
        
        

    if os.path.exists("token.pickle"):
        print("Loading Credentials From File...")
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)
            
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print("Refreshing Access Token...")
            credentials.refresh(Request())
        else:
            print("Fetching New Tokens...")
            flow = InstalledAppFlow.from_client_secrets_file("client_secret.json",
                                                    scopes=scopes)
            
            flow.run_local_server(port=8080, prompt="consent", authorization_prompt_message="")
            credentials = flow.credentials
            
            with open("token.pickle", "wb") as f:
                print("saving Credentuials for Future Use...")
                pickle.dump(credentials, f)
    
    return credentials

def playlistVideosToUrl(credentials):
    youtube = build("youtube", "v3", credentials=credentials)

    request = youtube.playlists().list(part="snippet", mine=True, maxResults = 50)

    response = request.execute()
    
    playlist_ids = []
    playlist_titles = []
    
    print()

    for i, item in enumerate(response["items"]):
        playlist_ids.append(item["id"])
        
        playlist_titles.append(item["snippet"]["title"])
    
    print("PLAYLISTS")
    print("---------")
    for i, title in enumerate(playlist_titles):
        print(f"{i + 1}. {title}")   

    while (True):
        print()
        selected_playlist_idx = input("Type in the number associated with the playlist you want to convert to mp3s: ")
        print()
        
        if (not(selected_playlist_idx.isdigit()) or int(selected_playlist_idx) < 1 or int(selected_playlist_idx) > len(playlist_titles)):
            print("Invalid Number")
            continue

        selected_playlist_idx = int(selected_playlist_idx) - 1
        break
    
    selected_playlist_id = playlist_ids[selected_playlist_idx]
    
    video_ids = []
    video_titles = []
    pageToken = None
    while (True):
        vid_request = youtube.playlistItems().list(part="contentDetails, snippet", playlistId=selected_playlist_id, pageToken=pageToken, maxResults=50)
        vid_response = vid_request.execute()
        
        for item in vid_response["items"]:
            video_ids.append(item["contentDetails"]["videoId"])
            video_titles.append(item["snippet"]["title"])
        
        if (vid_response.get("nextPageToken") == None):
            break
        
        pageToken = vid_response["nextPageToken"]
    
    youtube_prefix = "https://youtu.be/"
    
    video_urls = []
    
    for ids in video_ids:
        video_urls.append(youtube_prefix + ids)

    return (video_urls, video_titles)

def urlToMp3(youtube_urls, youtube_titles):    
    path = os.getcwd()
    
    if os.path.exists("mp3_folder"):
        shutil.rmtree("mp3_folder")
    os.mkdir("mp3_folder")

    download_path = os.path.join(path, "mp3_folder")
    
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": download_path}
    options.add_experimental_option("prefs", prefs)
    
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://cobalt.tools/")
    driver.implicitly_wait(10)
    
    audio_mode = driver.find_element(By.ID, "audioMode-true")
    audio_mode.click()
    
    input = driver.find_element(By.ID, "url-input-area")
    
    download_regex = re.compile('.*crdownload$')
    mp3_prefix = ".mp3"
    
    for url, title in zip(youtube_urls, youtube_titles):
        input.clear()
        input.send_keys(url)
        
        WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.ID, "download-button")))
        download_button = driver.find_element(By.ID, "download-button")
        download_button.click()
        
        time.sleep(2)
        
        while (True):
            download = os.listdir(download_path)[-1]
            match = download_regex.match(download)

            if (not(match)):
                break
                
        
        print("finished 1 file")
        
        old_title = os.listdir(download_path)[-1]
        
        old_file = os.path.join(download_path, old_title)
        new_file = os.path.join(download_path, title) + mp3_prefix
        os.rename(old_file, new_file)
    
    return

if __name__ == "__main__":
    credentials = googleLogin()
    video_urls, video_titles = playlistVideosToUrl(credentials)
    urlToMp3(video_urls, video_titles)