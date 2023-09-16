from bs4 import *
from pathlib import PurePath
import requests
import sys
import os

class bcolors:
    OK = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    RESET = "\033[0m"

def get_links(url, url_links, dominio):
    try:
        response = requests.get(url)
    except:
        print(bcolors.FAIL + "Error: invalid URL" + bcolors.RESET)
        exit()
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.findAll('a')
    for tag in links:
        cut = tag.get('href')
        if cut != None:
            if dominio in cut:
                url_links.append(cut)
            elif cut.startswith('/') == True:
                cut = "https://" + dominio + cut
                url_links.append(cut)
    return (url_links)
    
def get_images(url_links, dominio):
    url_images = []
    for link in url_links:
        try:
            response = requests.get(link)
        except:
            print(bcolors.FAIL + "Error: invalid URsL " + link +bcolors.RESET)
            exit()
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.findAll('img')
        for tag in images:
            cut = tag.get('src')
            if cut != None and len(cut) > 0:
                if cut.endswith(".png") or cut.endswith(".gif") or cut.endswith(".bmp") or cut.endswith(".jpg" or cut.endswith(".jpeg")):
                    if cut.startswith('//') == True:
                        cut = cut[2:]
                    if dominio in cut:
                        if cut.startswith("https") == False:
                            cut = "https://" + cut
                        url_images.append(cut)
                    elif cut.startswith('/') and ".com" != cut:
                        cut = "https://" + dominio + cut
                        url_images.append(cut)
        return url_images

def check(rec):
    opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
    url_images = []
    url_links = []
    
    if (len(sys.argv) == 1):
        print(bcolors.FAIL + "Error: please insert a URL" + bcolors.RESET)
        exit()
    elif "-r" != opts:
        url = sys.argv[len(sys.argv) - 1]
        if url.endswith("/") == False:
            url = url + '/'
        if url.startswith("http") == False:
            url = "https://" + url

        dominio = url[url.index('/') + 2:-1]
        
        if rec != 0 and len(url_links) < int(rec):
            x = 0
            url_links = get_links(url, url_links, dominio)
            while len(url_links) < int(rec):
                url_links = get_links(url_links[x], url_links, dominio)
                x += x
            result = []
            for link in url_links:
                if link not in result:
                    result.append(link)
            if len(result) < int(rec):
                print(bcolors.WARNING + "Warning: has requested recursion " + str(rec) + " but only " + str(len(result)) + " urls with the supplied domain are valid" + bcolors.RESET)
            url_links = result
        else:
            url_links.append(url)
        url_images = get_images(url_links, dominio)
        return url_images

def clean_folder(path, content):
    for file in content:
        os.remove(path + '/' + file)

def download_image(folder, url, name):
    path = os.getcwd() + '/'+ folder
    if os.path.exists(path) == False:
        os.mkdir(folder)
    name = folder + '/' + name
    f = open(name,'wb')
    try:
        response = requests.get(url)
        f.write(response.content)
    except:
        print(bcolors.WARNING + "Invalid URL ", url + bcolors.RESET)
        return 0
    f.close()
    return 1

def main():
    opts = [opt for opt in sys.argv[1:]]
    if "-p" in opts:
        try:
            folder = opts[opts.index("-p") + 1]
        except:
            print(bcolors.FAIL + "Error: invalid folder" + bcolors.RESET)
            exit()
        if folder.startswith("-"):
            print(bcolors.FAIL + "Error: invalid name for folder" + bcolors.RESET)
            exit()
    else:
        folder = "data"

    if "-l" in opts:
        if "-r" not in opts:
            print(bcolors.FAIL + "Error: \"-l\" specified but no recursivity \"-r\"" + bcolors.RESET)
            exit()
        else:
            try:
                rec = opts[opts.index("-l") + 1]
            except:
                print(bcolors.FAIL + "Error: invalid argument for \"-l\"" + bcolors.RESET)
                exit()
            if rec.isnumeric() == False:
                print(bcolors.FAIL + "Error: invalid argument for \"-l\"" + bcolors.RESET)
                exit()
    elif "-r" in opts:
        rec = 5
    else:
        rec = 0

    url_images = check(rec)
    if url_images == None:
        exit()
    else:
        x = 0
        path = os.getcwd() + '/' + folder
        if os.path.exists(path) == True:
            content = os.listdir(path)
            clean_folder(path,  content)
        for image in url_images:
            extension = image[image.rfind('.'):len(image)]
            if ".jpeg" in extension:
                extension = ".jpeg"
            else:
                extension = extension[0:4]
            x += download_image(folder, url_images[x], "image" + str(x) + extension)
            if x == rec:
                break
        print(bcolors.OK + str(x) + bcolors.RESET + " images downloaded successfully")

if __name__ == '__main__':
    main()