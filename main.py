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
    
    bad_chars = ['<', '>', ':', "\"", "/", "\\", "\|", "\?", "*"]
    
    while (True):
        video_request = youtube.playlistItems().list(part="contentDetails, snippet", playlistId=selected_playlist_id, pageToken=pageToken, maxResults=50)
        video_response = video_request.execute()
        
        for item in video_response["items"]:
            video_ids.append(item["contentDetails"]["videoId"])
            video_title = item["snippet"]["title"]
            
            for c in bad_chars:
                video_title = video_title.replace(c, '_')
            
            video_titles.append(video_title)
        
        if (video_response.get("nextPageToken") == None):
            break
        
        pageToken = video_response["nextPageToken"]
    
    youtube_prefix = "https://youtu.be/"
    
    video_urls = []
    
    for ids in video_ids:
        video_urls.append(youtube_prefix + ids)

    return (video_urls, video_titles)

def urlToMp3(youtube_urls, youtube_titles):    
    path = os.getcwd()
    
    if os.path.exists("download_folder"):
        shutil.rmtree("download_folder")
    os.mkdir("download_folder")
    
    if os.path.exists("mp3_folder"):
        shutil.rmtree("mp3_folder")
    os.mkdir("mp3_folder")

    download_path = os.path.join(path, "download_folder")
    mp3_path = os.path.join(path, "mp3_folder")
    
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": download_path}
    options.add_experimental_option("prefs", prefs)
    options.add_argument('--headless')
    options.add_argument('--log-level=3')
    
    
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://cobalt.tools/")
    driver.implicitly_wait(10)
    
    audio_mode = driver.find_element(By.ID, "audioMode-true")
    audio_mode.click()
    
    input = driver.find_element(By.ID, "url-input-area")
    
    download_regex = re.compile('.*crdownload$')
    mp3_prefix = ".mp3"
    
    
    files_downloaded = 0
    for url, title in zip(youtube_urls, youtube_titles):
        input.clear()
        input.send_keys(url)
        
        WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.ID, "download-button")))
        download_button = driver.find_element(By.ID, "download-button")
        download_button.click()
        
        if (len(driver.find_elements(By.XPATH, "//*[contains(@class, 'close-error switch') and text()='got it']")) > 0):
            try:
                driver.find_element(By.XPATH, "//*[contains(@class, 'close-error switch') and text()='got it']").click()
            except:
                pass
        
        time.sleep(5)
        
        while (True):
            download = os.listdir(download_path)[0]
            match = download_regex.match(download)

            if (not(match)):
                break
        
        files_downloaded += 1
        print(f"Finished downloading {files_downloaded}/{len(youtube_urls)} file")
        
        old_title = os.listdir(download_path)[0]
        
        old_file = os.path.join(download_path, old_title)
        new_file = os.path.join(mp3_path, title) + mp3_prefix
        os.rename(old_file, new_file)
        
        shutil.rmtree("download_folder")
        os.mkdir("download_folder")
        
    
    print("DONE!!!")
    return

if __name__ == "__main__":
    credentials = googleLogin()
    video_urls, video_titles = playlistVideosToUrl(credentials)
    urlToMp3(video_urls, video_titles)