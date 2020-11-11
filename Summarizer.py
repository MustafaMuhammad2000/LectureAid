import math

from nltk import sent_tokenize, word_tokenize, PorterStemmer
from nltk.corpus import stopwords


def create_frequency_matrix(sentences):
    frequency_matrix = {}
    stopWords = set(stopwords.words("english"))
    ps = PorterStemmer()

    for sent in sentences:
        freq_table = {}
        words = word_tokenize(sent)
        for word in words:
            word = word.lower()
            word = ps.stem(word)
            if word in stopWords:
                continue
            if word in freq_table:
                freq_table[word] += 1
            else:
                freq_table[word] = 1

        frequency_matrix[sent[:15]] = freq_table

    return frequency_matrix


def create_tf_matrix(freq_matrix):
    tf_matrix = {}

    for sent, f_table in freq_matrix.items():
        tf_table = {}

        count_words_in_sentence = len(f_table)
        for word, count in f_table.items():
            tf_table[word] = count / count_words_in_sentence

        tf_matrix[sent] = tf_table

    return tf_matrix


def create_documents_per_words(freq_matrix):
    word_per_doc_table = {}

    for sent, f_table in freq_matrix.items():
        for word, count in f_table.items():
            if word in word_per_doc_table:
                word_per_doc_table[word] += 1
            else:
                word_per_doc_table[word] = 1

    return word_per_doc_table


def create_idf_matrix(freq_matrix, count_doc_per_words, total_documents):
    idf_matrix = {}

    for sent, f_table in freq_matrix.items():
        idf_table = {}

        for word in f_table.keys():
            idf_table[word] = math.log10(total_documents / float(count_doc_per_words[word]))

        idf_matrix[sent] = idf_table

    return idf_matrix


def create_tf_idf_matrix(tf_matrix, idf_matrix):
    tf_idf_matrix = {}

    for (sent1, f_table1), (sent2, f_table2) in zip(tf_matrix.items(), idf_matrix.items()):

        tf_idf_table = {}

        for (word1, value1), (word2, value2) in zip(f_table1.items(),
                                                    f_table2.items()):  # here, keys are the same in both the table
            tf_idf_table[word1] = float(value1 * value2)

        tf_idf_matrix[sent1] = tf_idf_table

    return tf_idf_matrix


def score_sentences(tf_idf_matrix) -> dict:
    """
    score a sentence by its word's TF
    Basic algorithm: adding the TF frequency of every non-stop word in a sentence divided by total no of words in a sentence.
    :rtype: dict
    """

    sentenceValue = {}

    for sent, f_table in tf_idf_matrix.items():
        total_score_per_sentence = 0

        count_words_in_sentence = len(f_table)
        for word, score in f_table.items():
            total_score_per_sentence += score

        sentenceValue[sent] = total_score_per_sentence / count_words_in_sentence

    return sentenceValue


def find_top_sentences(sentenceValue) -> int:
    """
    Find the average score from the sentence value dictionary
    :rtype: int
    """

    values = list(sentenceValue.values())
    index = 0.6*(len(values)-1)
    index = round(index)
    print(values[index])

    return values[index]

def generate_summary(sentences, sentenceValue, threshold):
    sentence_count = 0
    summary = ''

    i = 0
    for sentence in sentences:
        i += 1
        if sentence[:15] in sentenceValue and sentenceValue[sentence[:15]] >= (threshold):
            if i%5 == 0:
                summary += " " + sentence+"\n"
                sentence_count += 1
            else:
                summary += " " + sentence
                sentence_count += 1

    return summary


class Summarizer:
    def __init__(self, text):
        self.text = text

    def summarize(self):
        # 1 Sentence Tokenize
        sentences = sent_tokenize(self.text)
        total_documents = len(sentences)
        # print(sentences)

        # 2 Create the Frequency matrix of the words in each sentence.
        freq_matrix = create_frequency_matrix(sentences)
        # print(freq_matrix)

        '''
        Term frequency (TF) is how often a word appears in a document, divided by how many words are there in a document.
        '''
        # 3 Calculate TermFrequency and generate a matrix
        tf_matrix = create_tf_matrix(freq_matrix)
        # print(tf_matrix)

        # 4 creating table for documents per words
        count_doc_per_words = create_documents_per_words(freq_matrix)
        # print(count_doc_per_words)

        '''
        Inverse document frequency (IDF) is how unique or rare a word is.
        '''
        # 5 Calculate IDF and generate a matrix
        idf_matrix = create_idf_matrix(freq_matrix, count_doc_per_words, total_documents)
        # print(idf_matrix)

        # 6 Calculate TF-IDF and generate a matrix
        tf_idf_matrix = create_tf_idf_matrix(tf_matrix, idf_matrix)
        # print(tf_idf_matrix)

        # 7 Important Algorithm: score the sentences
        sentence_scores = score_sentences(tf_idf_matrix)
        # print(sentence_scores)

        # 8 Find the threshold
        threshold = find_top_sentences(sentence_scores)
        # print(threshold)

        # 9 Important Algorithm: Generate the summary
        summary = generate_summary(sentences, sentence_scores, threshold)
        print("Summary is here:")
        print(summary)
        summary = "Summary: \n"+summary
        return summary
