import bz2
from bs4 import BeautifulSoup
import os
import sys


class SklearnCorpusExtractor:
    """
    Extracting a old_corpus per Sklearn's format expectations
    """

    def __init__(self, source_file, corpus_dir, language, num_samples, min_length, max_length):
        """
        Setup the old_corpus extractor.
        :param source_file: file to extract from
        :param corpus_dir: old_corpus directory to place samples in
        :param language: language to extract for
        :param num_samples: number of samples to extract
        :param min_length: minimum paragraph length
        :param max_length: maximum paragraph length
        """

        # Source file to pull from
        self.__source_file = bz2.BZ2File(source_file, "r")

        # Check for old_corpus dir
        self.__corpus_dir = corpus_dir
        if not os.path.exists(corpus_dir):
            os.mkdir(corpus_dir)

        # Make language dir
        self.__language = language
        self.__language_dir = corpus_dir + "/" + language
        if not os.path.exists(self.__language_dir):
            os.mkdir(self.__language_dir)

        # sample counter
        self.__num_samples = num_samples
        self.__sample_counter = 0

        # min & max paragraph lengths
        self.__min_length = min_length
        self.__max_length = max_length

    def __create_samples(self, paragraphs):
        """
        Creates a language sample file for each paragraph
        :param paragraphs: paragraph to place in the file
        :return:
        """
        for p in paragraphs:
            filename = self.__language_dir + "/" + self.__language + str(self.__sample_counter) + ".txt"
            sample_file = open(filename, "w")
            sample_file.writelines([p + '\n'])
            sample_file.close()
            self.__sample_counter += 1

            # break if we have enough samples
            if self.__sample_counter > (self.__num_samples-1):
                print "Acquired {0} samples.".format(self.__num_samples)
                break

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

            text_p = p.get_text()
            if len(text_p) < self.__min_length or len(text_p) > self.__max_length:
                continue
            else:
                parsed.append(text_p)

        return parsed

    def __get_next_article(self):
        """
        Returns the lines between the <article></article> tags
        :return:
        """
        # Get to the next article or bail
        while True:
            line = self.__source_file.readline()

            # EOF
            if not line:
                return None

            # Found an article to parse out
            if "<article lang" in line:
                article = line
                # Get remainder of article and return
                while True:
                    line = self.__source_file.readline()
                    if "</article" not in line:
                        article += line
                    else:
                        article += line
                        return article

    def extract(self):
        """
        Extract test old_corpus from source file
        :param source_file: source file
        :param language: language to extract samples for
        :param num_samples: number of samples to extract
        :return:
        """

        last_count = 0
        while self.__sample_counter <= (self.__num_samples-1):
            article = self.__get_next_article()
            article_language = self.__get_language(article)
            if article_language == self.__language:
                paragraphs = self.__get_paragraphs(article)
                if len(paragraphs) > 0:
                    self.__create_samples(paragraphs)

            # Tracking progress in 50 sample increments
            if self.__sample_counter > last_count + 50:
                print "Extracted {0} samples".format(self.__sample_counter)
                last_count = self.__sample_counter

        print "Extraction done"


if __name__ == "__main__":
    if __name__ == "__main__":
        reload(sys)
        sys.setdefaultencoding("utf-8")

    corpus_dir = "../data/corpus"
    num_samples = 1000
    min_length = 100
    max_length = 2000

    # English and French
    #en_fr_file = '../data/wikicomp-2014_enfr.xml.bz2'
    #for lan in ['en', 'fr']:
    #    ec = SklearnCorpusExtractor(source_file=en_fr_file, corpus_dir=corpus_dir, language=lan,
    #                                num_samples=num_samples, min_length=min_length, max_length=max_length)
    #    ec.extract()

    # German and Spanish
    #de_es_file = '../data/wikicomp-2014_dees.xml.bz2'
    #for lan in ['de', 'es']:
    #    ec = SklearnCorpusExtractor(source_file=de_es_file, corpus_dir=corpus_dir, language=lan,
    #                                num_samples=num_samples, min_length=min_length, max_length=max_length)
    #    ec.extract()

    # Italian and Portuguese
    it_pt_file = '../data/wikicomp-2014_itpt.xml.bz2'
    for lan in ['it', 'pt']:
        ec = SklearnCorpusExtractor(source_file=it_pt_file, corpus_dir='../data/lexical', language=lan,
                                    num_samples=num_samples, min_length=min_length, max_length=max_length)
        ec.extract()





