#! python3

import requests, sys, webbrowser, bs4, re, socket

# define variables
years = [2015, 2016]
base_url = 'http://malware-traffic-analysis.net/'

ip_list = []

for year in years:

	# for every years
	url = base_url + str(year) + '/index.html'
	
	res_year = requests.get(url)
	res_year.raise_for_status()

	soup_year = bs4.BeautifulSoup(res_year.text, 'html.parser')
	
	# select only the link to article
	linkElems = soup_year.select('.list_header')

	numOpen = len(linkElems)
	# numOpen = min(5, len(linkElems))

	for i in range(numOpen):

		# for every page
		url_art = 'http://malware-traffic-analysis.net/' + str(year) + '/' + linkElems[i].get('href')

		res_art = requests.get(url_art)
		res_art.raise_for_status()
		soup_art = bs4.BeautifulSoup(res_art.text, 'html.parser')
		
		ipElems = soup_art.select('ul li')
		
		# find IP 
		for i in range(len(ipElems)):
			ip = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ipElems[i].get_text())
			if ip:
				ip_list.append(ip.group())


# remove duplicate ip
ip_list = list(set(ip_list))

# result
print('Trovati ' + str(len(ip_list)) + ' IP unici')

# write list to file
bad_ip = open('bad_ip.txt', 'w')
for ip in ip_list:
	try:
		socket.inet_aton(ip)	
		bad_ip.write("%s\n" % ip)
	except socket.error:
		print(str(ip) + ' non valido')
