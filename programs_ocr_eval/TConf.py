import sys
import io
import glob
import matplotlib.pyplot as plt
import tools
from bs4 import BeautifulSoup

def get_confidences__page_level(soup):
	confidences_sum, tot = 0, 0
	for span in soup.find_all('span'): # tokens are in: <span class="ocrx_word">
		if span.get('class') == ['ocrx_word']:
			txt = span.get_text()
			t = span.get('title')
			# Confidences are given character per character. So we are storing confidences for each character in the page
			confidences = t.split(';')[1].split(' ') # ['', 'x_confs', '0.5362149']
			confidences = confidences[2:]
			for c in confidences:
				confidences_sum += float(c)
				tot += 1
	return (confidences_sum, tot)

def get_confidences__line_level(soup):
	confidences_per_line = {}
	cpt = 0 # line counter
	for span in soup.find_all('span'):  
		if span.get('class') == ['ocr_line']: # each line
			confidences_sum, tot = 0, 0
			for elm in span.find_all('span'):
				if elm.get('class') == ['ocrx_word']: # each token
					txt = elm.get_text()
					t = elm.get('title')
					confidences = t.split(';')[1].split(' ') # ['', 'x_confs', '0.5362149']
					confidences = confidences[2:]
					for c in confidences:
						confidences_sum += float(c)
						tot += 1
			mean = confidences_sum / tot if tot != 0 else 0
			confidences_per_line[cpt] = mean
			cpt += 1

	return confidences_per_line



if __name__ == '__main__':
	# Options parser
	options = tools.get_args()
	dir_path = options.data_dir
	level = options.level
	# For each file in the html directory
	for file in glob.glob(dir_path + '*.html'):
		# Parsing
		inFile = io.open(file, mode='r', encoding='utf-8')
		html = inFile.read()
		soup = BeautifulSoup(html, 'lxml') # parsing
		if level == 'page': 
			doc_name = file.split('/')[-1]
			sum_, tot = get_confidences__page_level(soup)
			mean = sum_ / tot if tot != 0 else 0
			print(doc_name + '\t' + str(mean))
		elif level == 'line':
			doc_name = file.split('/')[-1]
			confidences_per_line = get_confidences__line_level(soup)
			for cpt, mean in confidences_per_line.items():
				print(doc_name + '_' + str(cpt) + '\t' + str(mean))
		else:
			print('ERROR: Please enter "page" or "line" for the --level argument.')
			break