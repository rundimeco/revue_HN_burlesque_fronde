from optparse import OptionParser

def get_args():
	parser = OptionParser()
	parser.add_option("-d", "--data_dir", help="path to htmls files to evaluate")
	parser.add_option("-l", "--level", help="'page' or 'line")
	parser.add_option("-v", "--vocabulary", help="path to lexicon to use")
	(options, args) = parser.parse_args()
	return options
