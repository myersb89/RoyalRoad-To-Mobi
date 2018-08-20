from kindlegenerator import *
from bs4 import BeautifulSoup

url = input("Please enter a URL: ")

if validate_url(url):
	#get chapters and title from url
	chapter_urls = get_chapter_urls(url)
	title = get_book_title(url)
	print(title)
	
	#create the html file
	print("compiling chapters...")
	html_file = title.replace(" ","") + '.html'
	mybook = init_html(html_file)
	html_from_chapters(mybook,chapter_urls[0:2])
	close_html(mybook)

	#generate mobi file
	print("generating...")
	mobi_file = generate_mobi("C:\\Users\\Bryan\\Documents\\Projects\\Python\\KindleGenerator\\" + html_file)

	#email to kindle?

	#cleanup
	print("moving kindle file to output destination...")
	book_storage = "C:\\Users\\Bryan\\Documents\\KindleBooks\\"
	cleanup_files(book_storage, html_file, mobi_file)