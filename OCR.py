import os
import pytesseract
import requests
from zipfile import ZipFile
from bs4 import BeautifulSoup
from PIL import Image

def generate_manga_url():
    # Prompt the user for manga name and chapter number
    manga_name = input("Enter the name of the manga: ")
    chapter_number = input("Enter the chapter number: ")
    
    # Define the base URL
    base_url = "https://rawkuma.com/"
    
    # Format the manga name and chapter number
    formatted_manga_name = manga_name.lower().replace(" ", "-")
    formatted_chapter_number = chapter_number.lower().replace(" ", "-")
    
    # Create the complete manga URL
    return f"{base_url}{formatted_manga_name}-chapter-{formatted_chapter_number}/"

def download_images(url):
    # Send an HTTP GET request to the provided URL
    response = requests.get(url)
    
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all anchor tags
        anchor_tags = soup.find_all('a')
        global link # Initialize link outside of the loop
        
        # Search for the download link
        for tag in anchor_tags:
            link = tag.get('href')
            if link and link.startswith('https://dl.rawkuma.com'):
                print(f"\nPage URL: {url}\nStatus Code: {response.status_code}\nDownload Link: {link}\n")
                break
        else:
            print(f"Download link not found on the page. Status Code: {response.status_code}")
    else:
        print(f"Failed to fetch the webpage. Status Code: {response.status_code}")

    zip_file =  '/mnt/c/Users/user/Desktop/PROJECTS/Translator/manga.zip'

    if link: # noqa: F821
        response = requests.get(link)
        
        if response.status_code == 200:
            with open("manga.zip",'wb') as file:
                file.write(response.content)
                print(f"File Downloaded and saved as '{zip_file}'.")
        else:
            print(f"Failed to download the file. Status code: {response.status_code}")
    else:
        print("No valid download link found.")

def extracted():
    print("Extracting Files")
    with ZipFile("/mnt/c/Users/user/Desktop/PROJECTS/Translator/manga.zip") as unzipped:
        unzipped.extractall("/mnt/c/Users/user/Desktop/PROJECTS/Translator/images")
        print("Extraction completed and saved as images")

def optical_recognition():

    files = os.listdir("/mnt/c/Users/user/Desktop/PROJECTS/Translator/images")

    for file in files:
        if os.path.isfile(os.path.join("/mnt/c/Users/user/Desktop/PROJECTS/Translator/images",file)):
            print(file)
            image = Image.open(f"/mnt/c/Users/user/Desktop/PROJECTS/Translator/images/{file}")
            text = pytesseract.image_to_string(image)
            print(text)
if __name__ == "__main__":
    url = generate_manga_url()
    download_images(url)
    extracted()
    optical_recognition()
