from nlu.pipe_components import SparkNLUComponent, NLUComponent
import nlu
class Tokenizer(SparkNLUComponent):

    def __init__(self, annotator_class='default_tokenizer', language='en', component_type='tokenizer', get_default = True, nlp_ref='', nlu_ref='', model=None):

        if 'segment_words' in nlu_ref : annotator_class = 'word_segmenter'
        elif 'token' in annotator_class and  language in nlu.AllComponentsInfo().all_right_to_left_langs_with_pretrained_tokenizer : annotator_class = 'word_segmenter'
        elif 'token' in annotator_class and not 'regex'  in annotator_class: annotator_class = 'default_tokenizer'


        if model != None : self.model = model
        elif annotator_class == 'default_tokenizer':
            from nlu import DefaultTokenizer
            if get_default : self.model =  DefaultTokenizer.get_default_model()
            else : self.model =  DefaultTokenizer.get_default_model()  # there are no pretrained tokenizrs, only default 1
        elif annotator_class == 'word_segmenter':
            from nlu import WordSegmenter
            if get_default  and language =='': self.model =  WordSegmenter.get_default_model()
            elif get_default  and language !='': self.model =  WordSegmenter.get_default_model_for_lang(language)
            else : self.model =  WordSegmenter.get_pretrained_model(nlp_ref,language)  # there are no pretrained tokenizrs, only default 1



        SparkNLUComponent.__init__(self, annotator_class, component_type)
