import sys
import io
import glob
import tools
from bs4 import BeautifulSoup

def tokens_in_lex__page_level(soup, lex):
	nb_tokens, nb_in_voc = 0, 0
	for span in soup.find_all('span'):  # tokens are in: <span class="ocrx_word">
		if span.get('class') == ['ocrx_word']:
			txt = span.get_text()
			if txt.lower() in lex:
				nb_in_voc += 1
			nb_tokens += 1
	return nb_tokens, nb_in_voc

def get_confidences__line_level(soup, lex):
	tl_per_line = {}
	cpt = 0 # line counter
	for span in soup.find_all('span'):  
		if span.get('class') == ['ocr_line']: # each line
			nb_tokens, nb_in_voc = 0, 0
			for elm in span.find_all('span'):
				if elm.get('class') == ['ocrx_word']: # each token
					txt = elm.get_text()
					if txt.lower() in lex:
						nb_in_voc += 1
					nb_tokens += 1
			rate = nb_in_voc / nb_tokens if nb_tokens != 0 else 0
			tl_per_line[cpt] = rate
			cpt += 1
	return tl_per_line

if __name__ == '__main__':
	# Options parser
	options = tools.get_args()
	dir_path = options.data_dir
	level = options.level
	lex_path = options.vocabulary
	# Lexicon 
	lex_file = io.open(lex_path, mode='r', encoding='utf-8')
	lex = set([w.strip() for w in lex_file.readlines()])

	# For each file in the html directory
	for file in glob.glob(dir_path + '*.html'):
		# Parsing
		inFile = io.open(file, mode='r', encoding='utf-8')
		html = inFile.read()
		soup = BeautifulSoup(html, 'lxml') # parsing
		if level == 'page':
			doc_name = file.split('/')[-1]
			nb_tokens, nb_in_voc = tokens_in_lex__page_level(soup, lex)
			rate = nb_in_voc / nb_tokens if nb_tokens != 0 else 0
			print(doc_name + '\t' + str(rate))
		elif level == 'line':
			doc_name = file.split('/')[-1]
			tl_per_line = get_confidences__line_level(soup, lex)
			for cpt, tl in tl_per_line.items():
				print(doc_name + '_' + str(cpt) + '\t' + str(tl))
		else:
			print('ERROR: Please enter "page" or "line" for the --level argument.')
			break
		