from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import subprocess
import os
import shutil

def generate_mobi(htmlfile):
	path_to_kindlegen = "C:\\Users\\Bryan\\Documents\\KindleGen\\kindlegen.exe"
	args = path_to_kindlegen + ' ' + htmlfile
	FNULL = open(os.devnull, 'w')
	subprocess.call(args, stdout=FNULL, stderr=FNULL, shell=False)
	return htmlfile.replace(".html",".mobi")
	

def init_html(filename):
	file = open(filename, 'w+', encoding='utf-8')
	title = filename.strip(".html")
	file.write('<!doctype html>\r\n<html>\r\n<head>\n<title>' + title +'</title>\n<meta http-equiv="content-type" content="text/html; charset=utf-8">\n<link rel="stylesheet" href="style.css">\n</head>\r\n')
	return file


def html_from_chapters(file, chapters):
	file.write('<body>\n')
	chap_num = 1
	for chap in chapters:
		file.write('<h1>Chapter ' + str(chap_num) + '</h1>\n')
		html_soup = BeautifulSoup(simple_get(chap), 'html.parser')
			
		#chapter contents are contained in a css class called "chapter-content". Extract each paragraph from the content
		contents = html_soup.find(class_="chapter-content")
		for paragraph in contents.find_all("p"):
			file.write(str(paragraph) + '\r\n')
		chap_num += 1
	file.write("\n</body>\r\n")

def close_html(file):
	file.write('</html>')
	file.close()
	
#Check that the URL is the TOC for a Royal Road book
def validate_url(url):
	if 'royalroad' not in url:
		print('Enter a Royal Road URL')
		return False	
	else:
		html_soup = BeautifulSoup(simple_get(url), 'html.parser')
		if 'Table of Contents' not in html_soup.get_text():
			print('Enter URL to Table of Contents page')
			return False
		else:
			return True
			
#input the URL to a Royal road table of contents page and get a list of URLs for each chapter back
def get_chapter_urls(url):
	html_soup = BeautifulSoup(simple_get(url), 'html.parser')
	chapter_urls = []
	for row in html_soup.find_all('tr'):
		if 'data-url' in row.attrs:
			chapter_urls.append('https://www.royalroad.com/' + row['data-url'])
	return chapter_urls
	
def get_book_title(url):
	sections = url.split("/")
	title = ''
	for word in sections[-1].split("-"):
		new = word[0].upper() + word[1:]
		title += new + " "
	return title[:-1]
	
#simple get request with some error handling
def simple_get(url):
	try:
		with closing(get(url, stream=True)) as resp:
			if is_good_response(resp):
				return resp.content
			else:
				return None
	except Exception as e:
		log_error('Error during requests to {0} : {1}'.format(url, str(e)))
		return None
		
#check if the response is successful and valid html 
def is_good_response(resp):
	content_type = resp.headers['Content-Type'].lower()
	return(resp.status_code == 200 and content_type is not None and content_type.find('html') > -1)
	
def log_error(e):
	print(e)
	
def cleanup_files(storage,html,mobi):
	mobi_filename = mobi.split("\\")[-1]
	shutil.move(mobi, storage + mobi_filename)
	os.remove(html)
	