import os
import urllib.request

import requests
from bs4 import BeautifulSoup
from win10toast import ToastNotifier


def rootDirectoryCreator(name):
    newpath = r'E:\\'+name
    if not os.path.exists(newpath):
        os.makedirs(newpath)
        print('\n New directory named '+str.upper(name)+' was created...')
        return newpath
    else:
        print('New Directory could not be created...')
        return str(0)

def download_web_image(imageUrl,imageName,path):
    if path == '0':
        print('Image could not be downloaded, because there already exists a directory with same name. Try with a different name.')
    else:
        fullName = path+'\\'+imageName+ '.png'
        urllib.request.urlretrieve(imageUrl, fullName)
        print(imageName+' was downloaded')
    
def browse_spider(max_pages,start_page,checkdir,startImage=1):
    page = int(start_page)
    while page <= max_pages:
        count = 1
        lists = []
        print('\n\n Getting Page '+str(page)+' contents...')
        url = 'http://simpledesktops.com/browse/' + str(page)
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text)
        for link in soup.findAll('img',attrs={'width':'295px','height':'184px'}):
            name = link.get('title')
            href = link.get('src')
            if count >= int(startImage):
                lists.append(href[:-17])
                download_web_image(href[:-17],str(page)+'-'+str(count),checkdir)
                count +=1
            else:
                count +=1
                continue
        # print(lists)
        page +=1


print('--- Minimal Wallpapers Downloader ---')
print('\n Enter the name of the folder you want to create : ')
folder = input()
folderCreationCheck = rootDirectoryCreator(folder)
print('Enter the page you want to resume downloading wallpapers from : ')
resume = input()
print('Enter the image you want to resume downloading from the selected page : ')
imageNo = input()
print('\n\n Enter the number of pages you want to go through : ')
pages = input()
browse_spider(int(pages),resume,folderCreationCheck,imageNo)
images = os.listdir(folderCreationCheck)

toaster = ToastNotifier()
toaster.show_toast('Wallpapers Downloaded!', str(len(images)) +' wallpapers were successfully downloaded.', \
	duration=5)
#print('\n All the wallpapers were downloaded succesfully.')
