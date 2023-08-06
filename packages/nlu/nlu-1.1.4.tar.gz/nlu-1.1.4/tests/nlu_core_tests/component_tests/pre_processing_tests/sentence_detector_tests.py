import unittest
from tests.test_utils import get_sample_pdf_with_labels, get_sample_pdf, get_sample_sdf, get_sample_pdf_with_extra_cols, get_sample_pdf_with_no_text_col ,get_sample_spark_dataframe
from nlu import *

class TestSentenceDetector(unittest.TestCase):

    def test_sentence_detector(self):
        pipe = nlu.load('sentence_detector', verbose=True , )
        df = pipe.predict('I like my sentences detected. Some like their sentences warm. Warm is also good.', output_level='sentence')
        print(df.columns)
        print(df['sentence'])


    def test_sentence_detector_multi_lang(self):
        pipe = nlu.load('xx.sentence_detector', verbose=True , )
        df = pipe.predict('I like my sentences detected. Some like their sentences warm. Warm is also good.', output_level='sentence')
        print(df.columns)
        print(df['sentence'])

    def test_sentence_detector_pragmatic(self):
        pipe = nlu.load('sentence_detector.pragmatic', verbose=True , )
        df = pipe.predict('I like my sentences detected. Some like their sentences warm. Warm is also good.', output_level='sentence')
        print(df.columns)
        print(df['sentence'])

if __name__ == '__main__':
    unittest.main()

