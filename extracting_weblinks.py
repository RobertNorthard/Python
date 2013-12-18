#!/usr/bin/env python
"""
Extracing web links and creating an index

Created by Robert alongside Udacity online CS101 Computer Science Course
"""

import sys,os,re,urllib,time

def get_page(url):
	try:
		return urllib.urlopen(url).read()
	except:
		pass
	

def get_next_link(page):
	'''Returns next weblink and position of last link'''
	start_link = page.find('<a href=')
	
	if start_link == -1:
		return None, 0
	
	start_quote = page.find('"',start_link)
	end_quote = page.find('"',start_quote + 1)
	
	url = page[start_quote + 1:end_quote]
	
	return url, end_quote

def get_all_links(page):
	'''Get all links associated with page'''
	links = []
	while True:
		url, endpos = get_next_link(page)
		if url:
			links.append(url)
			page = page[endpos:]
		else:
			break
	return links
	
def add_to_index(index, url, keyword):
	'''Add URL to index'''
	for entry in index:
		if entry[0] == keyword:
			if url not in entry[1]:
				entry[1].append(url)
				return
			
	index.append([keyword, [url]])
			
def add_page_index(index, url, content):
	'''Add page to index'''
	tagStrip = re.compile('<[^>]*>')
	tagsStripped =  tagStrip.sub('', content)
	keywords = tagsStripped.split()
	for word in keywords:
		add_to_index(index, url, word)
		
def index_lookup(index, keywords):
	for entry in index:
		if entry[0] == item:
			return entry[1]
	return None
	
def union(a, b):
	for e in b:
		if e not in a:
			a.append(e)

def webcrawl(seed, max_depth):
	'''limited depth first search web crawl'''
	index = []
	tocrawl = [seed]
	crawled = []
	depth = []
	current_depth = 0
	
	while tocrawl and current_depth <= max_depth:
		url = tocrawl.pop()
		
		if url not in crawled:
			content = get_page(url)
			add_page_index(index, url, content)
			union(depth, get_all_links(content))
			crawled.append(url)
			
		if not tocrawl:
			tocrawl = depth
			depth = []
			current_depth+=1
			
	return index
	
data_set = webcrawl('http://www.reddit.com',0)
keywords = ['account', 'game', 'news', 'reddit']
print data_set
print '-------------------------Search-Results for %s-----------' % (keywords)
t0 = time.time()
for item in keywords:
	print index_lookup(data_set, item)

