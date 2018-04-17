import bz2
from bs4 import BeautifulSoup
import sys


class CorpusExtractor:
    """
    Extracting the test corpus
    """

    def __init__(self, english_file, french_file, german_file, spanish_file):
        """
        Initialize a corpus extractor
        :param bzipfile:
        """
        self.__english_file = bz2.BZ2File(english_file, "w")
        self.__french_file = bz2.BZ2File(french_file, "w")
        self.__german_file = bz2.BZ2File(german_file, "w")
        self.__spanish_file = bz2.BZ2File(spanish_file, "w")

    def __append_corpus(self, language, paragraphs):
        """
        Appends the provided paragraphs to the corpus file for the language
        :param language: language
        :param paragraphs: paragraphs to append
        :return:
        """
        if language == "en":
            self.__english_file.writelines(["en|" + p + '\n' for p in paragraphs])
        elif language == "fr":
            self.__french_file.writelines(["fr|" + p + '\n' for p in paragraphs])
        elif language == "de":
            self.__german_file.writelines(["de|" + p + '\n' for p in paragraphs])
        elif language == "es":
            self.__spanish_file.writelines(["es|" + p + '\n' for p in paragraphs])

    def __get_language(self, article):
        """
        Parse out the language from an article
        :param article:
        :return: language
        """
        return BeautifulSoup(article, 'xml').article['lang']

    def __get_paragraphs(self, article):
        """
        Retrieve the interesting paragraphs from the article.  Interesting is defined as:
        - having primarily free text
        - being of a certain minimum length
        :param article:
        :return: a list of paragraphs
        """
        paragraphs = BeautifulSoup(article, 'xml').content.find_all('p')
        parsed = []
        for p in paragraphs:
            if '\n' in str(p):
                continue
            elif len(str(p)) < 1000:
                continue
            else:
                parsed.append(p.get_text())

        return parsed

    def __get_next_article(self, source_file):
        """
        Returns the lines between the <article></article> tags
        :return:
        """
        # Get to the next article or bail
        while True:
            line = source_file.readline()

            # EOF
            if not line:
                return None

            # Found an article to parse out
            if "<article lang" in line:
                article = line
                # Get remainder of article and return
                while True:
                    line = source_file.readline()
                    if "</article" not in line:
                        article += line
                    else:
                        article += line
                        return article

    def extract(self, source_file, num_articles=100000):
        """
        Extract corpus from the given bzipfile
        :param source_file: the bzip compressed file
        :param num_articles: number of articles to evaluate
        :return:
        """
        source_file = bz2.BZ2File(source_file, "r")

        articles_extracted = 0
        while articles_extracted < num_articles:
            article = self.__get_next_article(source_file)
            lang = self.__get_language(article)
            paragraphs = self.__get_paragraphs(article)
            if len(paragraphs) > 0:
                self.__append_corpus(lang, paragraphs)
            articles_extracted +=1
            if articles_extracted % 20 == 0:
                print "Reviewed {0} articles".format(articles_extracted)

        print "Extraction done"


if __name__ == "__main__":
    if __name__ == "__main__":
        reload(sys)
        sys.setdefaultencoding("utf-8")

    files = [
        "../data/wikicomp-2014_dees.xml.bz2",
        "../data/wikicomp-2014_enfr.xml.bz2"
    ]
    ec = CorpusExtractor(english_file="../data/english_corpus.bz2",
                         french_file="../data/french_corpus.bz2",
                         german_file="../data/german_corpus.bz2",
                         spanish_file="../data/spanish_corpus.bz2")

    for f in files:
        ec.extract(f, num_articles=500000)




