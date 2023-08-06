__version__ = '1.1.3'

import sys


def check_pyspark_install():
    try :
        from pyspark.sql import SparkSession
        try :
            import sparknlp
            v = sparknlp.start().version
            spark_major = int(v.split('.')[0])
            if spark_major >= 3 :
                raise Exception()
        except :
            print(f"Detected pyspark version={v} Which is >=3.X\nPlease run '!pip install pyspark==2.4.7' or install any pyspark>=2.4.0 and pyspark<3")
            # print(f"Or set nlu.load(version_checks=False). We disadvise from doing so, until Pyspark >=3 is officially supported in 2021.")
            return False
    except :
        print("No Pyspark installed!\nPlease run '!pip install pyspark==2.4.7' or install any pyspark>=2.4.0 with pyspark<3")
        return False
    return True

def check_python_version():
    if float(sys.version[:3]) >= 3.8:
        print("Please use a Python version with version number SMALLER than 3.8")
        print("Python versions equal or higher 3.8 are currently NOT SUPPORTED by NLU")
        return False
    return True


# if not check_pyspark_install(): raise Exception()
if not check_python_version(): raise Exception()



import nlu
import logging
from nlu.namespace import NameSpace
import warnings

warnings.filterwarnings("ignore")

logger = logging.getLogger('nlu')
# logger.setLevel(logging.INFO)
logger.setLevel(logging.CRITICAL)
ch = logging.StreamHandler()
ch.setLevel(logging.CRITICAL)

logger.addHandler(ch)

import gc
from nlu.pipeline import *

from nlu import info
from nlu.info import ComponentInfo
from nlu.components import tokenizer, stemmer, spell_checker, normalizer, lemmatizer, embeddings, chunker, \
    embeddings_chunker
# Main components
from nlu.components.classifier import Classifier
from nlu.components.lemmatizer import Lemmatizer
from nlu.components.spell_checker import SpellChecker
from nlu.components.labeled_dependency_parser import LabeledDependencyParser as LabledDepParser
from nlu.components.unlabeled_dependency_parser import UnlabeledDependencyParser as UnlabledDepParser
from nlu.components.sentence_detector import NLUSentenceDetector

from nlu.components.dependency_untypeds.unlabeled_dependency_parser.unlabeled_dependency_parser import \
    UnlabeledDependencyParser
from nlu.components.dependency_typeds.labeled_dependency_parser.labeled_dependency_parser import \
    LabeledDependencyParser

# 0 Base internal Spark NLP structure required for all JSL components
from nlu.components.utils.document_assembler.spark_nlp_document_assembler import SparkNlpDocumentAssembler
from nlu.components.utils.ner_to_chunk_converter.ner_to_chunk_converter import NerToChunkConverter

# we cant call the embdding file "embeddings" because namespacing wont let us import the Embeddings class inside of it then
from nlu.components.embedding import Embeddings
from nlu.components.util import Util
from nlu.components.utils.ner_to_chunk_converter import ner_to_chunk_converter
from nlu.components.utils.sentence_embeddings.spark_nlp_sentence_embedding import SparkNLPSentenceEmbeddings

# sentence
from nlu.components.sentence_detectors.pragmatic_sentence_detector.sentence_detector import PragmaticSentenceDetector
from nlu.components.sentence_detectors.deep_sentence_detector.deep_sentence_detector import SentenceDetectorDeep
# Embeddings
from nlu.components.embeddings.albert.spark_nlp_albert import SparkNLPAlbert
from nlu.components.embeddings.sentence_bert.BertSentenceEmbedding import BertSentence

from nlu.components.embeddings.bert.spark_nlp_bert import SparkNLPBert
from nlu.components.embeddings.elmo.spark_nlp_elmo import SparkNLPElmo
from nlu.components.embeddings.xlnet.spark_nlp_xlnet import SparkNLPXlnet
from nlu.components.embeddings.use.spark_nlp_use import SparkNLPUse
from nlu.components.embeddings.glove.glove import Glove

# classifiers
from nlu.components.classifiers.classifier_dl.classifier_dl import ClassifierDl
from nlu.components.classifiers.multi_classifier.multi_classifier import MultiClassifier
from nlu.components.classifiers.yake.yake import Yake
from nlu.components.classifiers.language_detector.language_detector import LanguageDetector
from nlu.components.classifiers.named_entity_recognizer_crf.ner_crf import NERDLCRF
from nlu.components.classifiers.ner.ner_dl import NERDL
from nlu.components.classifiers.sentiment_dl.sentiment_dl import SentimentDl
from nlu.components.classifiers.vivekn_sentiment.vivekn_sentiment_detector import ViveknSentiment
from nlu.components.classifiers.pos.part_of_speech_jsl import PartOfSpeechJsl

# matchers
from nlu.components.matchers.date_matcher.date_matcher import DateMatcher
from nlu.components.matchers.regex_matcher.regex_matcher import RegexMatcher
from nlu.components.matchers.text_matcher.text_matcher import TextMatcher

from nlu.components.matcher import Matcher

# token level operators
from nlu.components.tokenizer import Tokenizer
from nlu.components.lemmatizer import Lemmatizer
from nlu.components.stemmer import Stemmer
from nlu.components.normalizer import Normalizer
from nlu.components.stopwordscleaner import StopWordsCleaner
from nlu.components.stemmers.stemmer.spark_nlp_stemmer import SparkNLPStemmer
from nlu.components.normalizers.normalizer.spark_nlp_normalizer import SparkNLPNormalizer
from nlu.components.normalizers.document_normalizer.spark_nlp_normalizer import SparkNLPDocumentNormalizer

from nlu.components.lemmatizers.lemmatizer.spark_nlp_lemmatizer import SparkNLPLemmatizer
from nlu.components.stopwordscleaners.stopwordcleaner.nlustopwordcleaner import NLUStopWordcleaner
from nlu.components.stopwordscleaner import StopWordsCleaner
## spell
from nlu.components.spell_checkers.norvig_spell.norvig_spell_checker import NorvigSpellChecker
from nlu.components.spell_checkers.context_spell.context_spell_checker import ContextSpellChecker
from nlu.components.spell_checkers.symmetric_spell.symmetric_spell_checker import SymmetricSpellChecker
from nlu.components.tokenizers.default_tokenizer.default_tokenizer import DefaultTokenizer
from nlu.components.tokenizers.word_segmenter.word_segmenter import WordSegmenter

from nlu.components.chunkers.default_chunker.default_chunker import DefaultChunker
from nlu.components.embeddings_chunks.chunk_embedder.chunk_embedder import ChunkEmbedder
from nlu.components.chunkers.ngram.ngram import NGram

# sentence
from nlu.components.utils.sentence_detector.sentence_detector import SparkNLPSentenceDetector
from nlu.components.sentence_detector import NLUSentenceDetector

#seq2seq
from nlu.components.seq2seqs.marian.marian import Marian
from nlu.components.seq2seqs.t5.t5 import T5
from nlu.components.sequence2sequence import Seq2Seq

from nlu.pipeline_logic import PipelineQueryVerifier

global spark_started, spark, active_pipes, all_components_info, nlu_package_location

nlu_package_location = nlu.__file__[:-11]

active_pipes = []
spark_started = False
spark = None

from nlu.info import AllComponentsInfo
from nlu.discovery import Discoverer
all_components_info = nlu.AllComponentsInfo()
discoverer = nlu.Discoverer()

import os
import sparknlp

def read_nlu_info(path):
    f = open(os.path.join(path,'nlu_info.txt'), "r")
    nlu_ref = f.readline()
    f.close()
    return nlu_ref


def is_running_in_databricks():
    #Check if the currently running Python Process is running in Databricks or not
    # If any Enviroment Variable name contains 'DATABRICKS' this will return True, otherwise False
    for k in os.environ.keys() :
        if 'DATABRICKS' in k :
            return True
    return False

def load_nlu_pipe_from_hdd(pipe_path):
    pipe = NLUPipeline()
    if nlu.is_running_in_databricks() :
        if pipe_path.startswith('/dbfs/') or pipe_path.startswith('dbfs/'):
            nlu_path = pipe_path
            if pipe_path.startswith('/dbfs/'):
                nlp_path =  pipe_path.replace('/dbfs','')
            else :
                nlp_path =  pipe_path.replace('dbfs','')

        else :
            nlu_path = 'dbfs/' + pipe_path
            if pipe_path.startswith('/') : nlp_path = pipe_path
            else : nlp_path = '/' + pipe_path

        nlu_ref = read_nlu_info(nlu_path)
        if os.path.exists(pipe_path):
            # if os.path.exists(info_path):
            pipe_components = construct_component_from_pipe_identifier(nlu_ref,nlu_ref,'hdd',path=nlp_path)
            # pipe_components = construct_component_from_pipe_identifier('nlu_ref','nlu_ref','hdd',path=pipe_path)

            for c in pipe_components: pipe.add(c, nlu_ref, pretrained_pipe_component=True)

            return pipe
            # else:
            #     print(f'Could not find nlu_info.json file in  {pipe_path}')
            #     return NluError
        else :
            print(f'Could not find nlu pipe folder in {pipe_path}')
            return NluError


    nlu_ref = read_nlu_info(pipe_path)
    if os.path.exists(pipe_path):
        # if os.path.exists(info_path):
        pipe_components = construct_component_from_pipe_identifier(nlu_ref,'nlu_ref','hdd',path=pipe_path)
        for c in pipe_components: pipe.add(c, nlu_ref, pretrained_pipe_component=True)

        return pipe
        # else:
        #     print(f'Could not find nlu_info.json file in  {pipe_path}')
        #     return NluError
    else :
        print(f'Could not find nlu pipe folder in {pipe_path}')
        return NluError
def enable_verbose():
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    logger.addHandler(ch)

def is_spark_23_installed():
    version = pyspark.version.__version__
    if '2.3' == version[:3]: return True
    return False
def load(request ='from_disk', path=None,verbose=False,version_checks=True):
    '''
    Load either a prebuild pipeline or a set of components identified by a whitespace seperated list of components
    :param verbose:
    :param path: If path is not None, the model/pipe for the NLU reference will be loaded from the path. Useful for offline mode. Currently only loading entire NLU pipelines is supported, but not loading singular pipes
    :param request: A NLU model/pipeline/component reference
    :param version_checks: Wether to check if Pyspark is properly installed and if the Pyspark version is correct for the NLU version. If set to False, these tests will be skipped
    :return: returns a non fitted nlu pipeline object
    '''
    gc.collect()
    # if version_checks : check_pyspark_install()

    spark = sparknlp.start(spark23=is_spark_23_installed())
    spark.catalog.clearCache()
    spark_started = True
    if verbose:
        enable_verbose()

    try:

        if path != None :
            logger.info(f'Trying to load nlu pipeline from local hard drive, located at {path}')
            pipe = load_nlu_pipe_from_hdd(path)
            return pipe
        components_requested = request.split(' ')
        pipe = NLUPipeline()
        language = parse_language_from_nlu_ref(request)
        pipe.lang=language
        pipe.nlu_ref = request
        for nlu_ref in components_requested:
            nlu_ref.replace(' ', '')
            # component = component.lower()
            if nlu_ref == '': continue
            nlu_component = parse_component_data_from_name_query(nlu_ref)
            # if we get a list of components, then the NLU reference is a pipeline, we do not need to check order
            if type(nlu_component) == type([]):
                # lists are parsed down to multiple components
                for c in nlu_component: pipe.add(c, nlu_ref, pretrained_pipe_component=True)
            else:
                pipe.add(nlu_component, nlu_ref)
                pipe = PipelineQueryVerifier.check_and_fix_nlu_pipeline(pipe)

    except:
        import sys
        e = sys.exc_info()
        print(e[0])
        print(e[1])

        print(
            "Something went wrong during loading and fitting the pipe. Check the other prints for more information and also verbose mode. Did you use a correct model reference?")

        return NluError()
    # active_pipes.append(pipe)
    return pipe


def parse_language_from_nlu_ref(nlu_ref):

    infos = nlu_ref.split('.')
    for split in infos:
        if split in nlu.AllComponentsInfo().all_languages:
            logger.info(f'Parsed Nlu_ref={nlu_ref} as lang={split}')
            return split
    logger.info(f'Parsed Nlu_ref={nlu_ref} as lang=en')
    return 'en'

def resolve_multi_lang_embed(language,sparknlp_reference):
    if language == 'ar' and 'glove' in sparknlp_reference : return 'arabic_w2v_cc_300d'
    if language == 'ur' : return 'urduvec_140M_300d'
    else : return sparknlp_reference



def get_default_component_of_type(missing_component_type,language='en'):
    '''
    This function returns a default component for a missing component type.
    It is used to auto complete pipelines, which are missng required components.
    These represents defaults for many applications and should be set wisely.
    :param missing_component_type: String which is either just the component type or componenttype@spark_nlp_reference which stems from a models storageref and refers to some pretrained embeddings or model
    :return: a NLU component which is a either the default if there is no '@' in the @param missing_component_type or a default component for that particualar type
    '''

    logger.info('Getting default for missing_component_type=%s', missing_component_type)
    if not '@' in missing_component_type:
        # get default models if there is no @ in the model name included
        if missing_component_type == 'document': return Util('document_assembler')
        if missing_component_type == 'sentence': return Util('sentence_detector')
        if missing_component_type == 'sentence_embeddings': return Embeddings('use')
        if 'token' in missing_component_type: return nlu.components.tokenizer.Tokenizer("default_tokenizer", language=language)
        if missing_component_type == 'word_embeddings': return Embeddings(nlu_ref='glove')
        if missing_component_type == 'pos':   return Classifier(nlu_ref='pos')
        if missing_component_type == 'ner':   return Classifier(nlu_ref='ner')
        if missing_component_type == 'ner_converter':   return Util('ner_converter')
        if missing_component_type == 'chunk': return nlu.chunker.Chunker()
        if missing_component_type == 'ngram': return nlu.chunker.Chunker(nlu_ref='ngram')
        if missing_component_type == 'chunk_embeddings': return embeddings_chunker.EmbeddingsChunker()
        if missing_component_type == 'unlabeled_dependency': return UnlabledDepParser()
        if missing_component_type == 'labled_dependency': return LabledDepParser('dep')
        if missing_component_type == 'date': return nlu.Matcher('date')
        if missing_component_type == 'ner_converter': return Util('ner_converter')

    else:
        multi_lang =['ar','ur']
        # if there is an @ in the name, we must get some specific pretrained model from the sparknlp reference that should follow after the @
        missing_component_type, sparknlp_reference = missing_component_type.split('@')
        if 'embed' in missing_component_type:

            if language in multi_lang : sparknlp_reference = resolve_multi_lang_embed(language,sparknlp_reference)
            return construct_component_from_identifier(language=language, component_type='embed',
                                                       nlp_ref=sparknlp_reference)
        if 'pos' in missing_component_type or 'ner' in missing_component_type:
            return construct_component_from_identifier(language=language, component_type='classifier',
                                                       nlp_ref=sparknlp_reference)
        if 'chunk_embeddings' in missing_component_type:
            return embeddings_chunker.EmbeddingsChunker()
        if 'unlabeled_dependency' in missing_component_type or 'dep.untyped' in missing_component_type:
            return UnlabledDepParser('dep.untyped')
        if 'labled_dependency' in missing_component_type or 'dep.typed' in missing_component_type:
            return LabledDepParser('dep.typed')
        if 'date' in missing_component_type:
            return None

        logger.exception("Could not resolve default component type for missing type=%s", missing_component_type)


def parse_component_data_from_name_query(nlu_reference, detect_lang=False):
    '''
    This method implements the main namespace for all component names. It parses the input request and passes the data to a resolver method which searches the namespace for a Component for the input request
    It returns a list of NLU.component objects or just one NLU.component object alone if just one component was specified.
    It maps a correctly namespaced name to a corresponding component for pipeline
    If no lang is provided, default language eng is assumed.
    General format  <lang>.<class>.<dataset>.<embeddings>
    For embedding format : <lang>.<class>.<variant>
    This method will parse <language>.<NLU_action>
        Additional data about dataset and variant will be resolved by corrosponding action classes

    If train prefix is part of the nlu_reference ,the trainable namespace will e searched

    if 'translate_to' or 'marian' is inside of the nlu_reference, 'xx' will be prefixed to the ref and set as lang if it is not already
    Since all translate models are xx lang
    :param nlu_reference: User request (should be a NLU reference)
    :param detect_lang: Wether to automatically  detect language
    :return: Pipeline or component for the NLU reference.
    '''

    infos = nlu_reference.split('.')

    if len(infos) < 0:
        logger.exception("EXCEPTION: Could not create a component for nlu reference=%s", nlu_reference)
        return NluError()
    language = ''
    component_type = ''
    dataset = ''
    component_embeddings = ''
    trainable = False
    resolved_component = None
    # 1. Check if either a default cmponent or one specific pretrained component or pipe  or alias of them is is requested without more sepcificatin about lang,dataset or embeding.
    # I.e. 'explain_ml' , 'explain; 'albert_xlarge_uncased' or ' tokenize'  or 'sentiment' s requested. in this case, every possible annotator must be checked.
    # format <class> or <nlu identifier>
    # type parsing via checking parts in nlu action <>


    if len(infos) == 0:
        logger.exception("Split  on query is 0.")
    # Query of format <class>, no embeds,lang or dataset specified
    elif 'train' in infos :
        trainable = True
        component_type = infos[1]
    elif 'translate_to' in nlu_reference and not 't5' in nlu_reference:
        language = 'xx'
        if nlu_reference[0:3] != 'xx.':
            nlu_reference = 'xx.' + nlu_reference
        logger.info(f'Setting lang as xx for nlu_ref={nlu_reference}')
        component_type = 'translate_to'
    elif len(infos) == 1:
        # if we only have 1 split result, it must a a NLU action reference or an alias
        logger.info('Setting default lang to english')
        language = 'en'
        if infos[0] in all_components_info.all_components or all_components_info.all_nlu_actions:
            component_type = infos[0]
    #  check if it is any query of style #<lang>.<class>.<dataset>.<embeddings>
    elif infos[0] in all_components_info.all_languages:
        language = infos[0]
        component_type = infos[1]
        logger.info(f"Got request for trainable model {component_type}")
        if len(infos) == 3:  # dataset specified
            dataset = infos[2]
        if len(infos) == 4:  # embeddings specified
            component_embeddings = infos[3]

    # passing embed_sentence can have format embed_sentence.lang.embedding or embed_sentence.embedding
    # i.e. embed_sentence.bert
    # fr.embed_sentence.bert will automatically select french bert thus no embed_sentence.en.bert or simmilar is required
    # embed_sentence.bert or en.embed_sentence.bert
    # name does not start with a language
    # so query has format <class>.<dataset>
    elif len(infos) == 2:
        logger.info('Setting default lang to english')
        language = 'en'
        component_type = infos[0]
        dataset = infos[1]
    # query has format <class>.<dataset>.<embeddings>
    elif len(infos) == 3:
        logger.info('Setting default lang to english')
        language = 'en'
        component_type = infos[0]
        dataset = infos[1]
        component_embeddings = infos[1]


    logger.info(
        'For input nlu_ref %s detected : \n lang: %s  , component type: %s , component dataset: %s , component embeddings  %s  ',
        nlu_reference, language, component_type, dataset, component_embeddings)
    resolved_component = resolve_component_from_parsed_query_data(language, component_type, dataset,component_embeddings, nlu_reference, trainable)
    if resolved_component is None:
        logger.exception("EXCEPTION: Could not create a component for nlu reference=%s", nlu_reference)
        return NluError()
    return resolved_component


def resolve_component_from_parsed_query_data(language, component_type, dataset, component_embeddings, nlu_ref,trainable=False,path=None):
    '''
    Searches the NLU name spaces for a matching NLU reference. From that NLU reference, a SparkNLP reference will be aquired which resolved to a SparkNLP pretrained model or pipeline
    :param nlu_ref: Full request which was passed to nlu.load()
    :param language: parsed language, may never be  '' and should be default 'en'
    :param component_type: parsed component type. may never be ''
    :param dataset: parsed dataset, can be ''
    :param component_embeddings: parsed embeddigns used for the component, can be ''
    :return: returns the nlu.Component class that corrosponds to this component. If it is a pretrained pipeline, it will return a list of components(?)
    '''
    component_kind = ''  # either model or pipe or auto_pipe
    nlp_ref = ''
    logger.info('Searching local Namespaces for SparkNLP reference.. ')
    resolved = False

    # 0. check trainable references
    if trainable == True :
        if nlu_ref in NameSpace.trainable_models.keys():
            component_kind = 'trainable_model'
            nlp_ref = NameSpace.trainable_models[nlu_ref]
            logger.info(f'Found Spark NLP reference in trainable models namespace = {nlp_ref}')
            resolved = True

    # 1. check if pipeline references for resolution
    if resolved == False and language in NameSpace.pretrained_pipe_references.keys():
        if nlu_ref in NameSpace.pretrained_pipe_references[language].keys():
            component_kind = 'pipe'
            nlp_ref = NameSpace.pretrained_pipe_references[language][nlu_ref]
            logger.info(f'Found Spark NLP reference in pretrained pipelines namespace = {nlp_ref}')
            resolved = True

    # 2. check if model references for resolution
    if resolved == False and language in NameSpace.pretrained_models_references.keys():
        if nlu_ref in NameSpace.pretrained_models_references[language].keys():
            component_kind = 'model'
            nlp_ref = NameSpace.pretrained_models_references[language][nlu_ref]
            logger.info(f'Found Spark NLP reference in pretrained models namespace = {nlp_ref}')
            resolved = True

    # 2. check if alias/default references for resolution
    if resolved == False and nlu_ref in NameSpace.component_alias_references.keys():
        sparknlp_data = NameSpace.component_alias_references[nlu_ref]
        component_kind = sparknlp_data[1]
        nlp_ref = sparknlp_data[0]
        logger.info('Found Spark NLP reference in language free aliases namespace')
        resolved = True

        if len(sparknlp_data) > 2 :
            dataset=sparknlp_data[2]
        if len(sparknlp_data) > 3 :
            # special case overwrite for T5
            nlu_ref=sparknlp_data[3]

    # 3. If reference is none of the Namespaces, it must be a component like tokenizer or YAKE or Chunker etc....
    # If it is not, then it does not exist and will be caught later
    if not resolved:
        resolved = True
        component_kind = 'component'
        logger.info('Could not find reference in NLU namespace. Assuming it is a component that is an ragmatic NLP annotator with NO model to download behind it.')

    # Convert references into NLU Component object which embelishes NLP annotators
    if component_kind == 'pipe':
        constructed_components = construct_component_from_pipe_identifier(language, nlp_ref, nlu_ref)
        logger.info(f'Inferred Spark reference nlp_ref={nlp_ref} and nlu_ref={nlu_ref}  to NLP Annotator Class {constructed_components}')
        if constructed_components is None:
            logger.exception(
                f'EXCEPTION : Could not create NLU component for nlp_ref={nlp_ref} and nlu_ref={nlu_ref}  to NLP Annotator Classes {constructed_components}')
            return NluError
        else:
            return constructed_components
    elif component_kind in ['model', 'component']:
        constructed_component = construct_component_from_identifier(language, component_type, dataset,
                                                                    component_embeddings, nlu_ref,
                                                                    nlp_ref)

        logger.info(f'Inferred Spark reference nlp_ref={nlp_ref} and nlu_ref={nlu_ref}  to NLP Annotator Class {constructed_component}')

        if constructed_component is None:
            logger.exception(f'EXCEPTION : Could not create NLU component for nlp_ref={nlp_ref} and nlu_ref={nlu_ref}')
            return NluError
        else:
            return constructed_component
    elif component_kind == 'trainable_model':
        constructed_component = construct_trainable_component_from_identifier(nlu_ref,nlp_ref)
        if constructed_component is None:
            logger.exception(f'EXCEPTION : Could not create NLU component for nlp_ref={nlp_ref} and nlu_ref={nlu_ref}')
            return NluError
        else:
            constructed_component.component_info.is_untrained = True
            return constructed_component
    else:
        logger.exception(
            "EXCEPTION : Could not resolve query=%s for kind=%s and reference=%s in any of NLU's namespaces ", nlu_ref,
            component_kind,
            nlp_ref)
        return NluError

def construct_trainable_component_from_identifier(nlu_ref,nlp_ref):
    '''
    This method returns a Spark NLP annotator Approach class embelished by a NLU component
    :param nlu_ref: nlu ref to the trainable model
    :param nlp_ref: nlp ref to the trainable model
    :return: trainable model as a NLU component
    '''

    logger.info(f'Creating trainable NLU component for nlu_ref = {nlu_ref} and nlp_ref = {nlp_ref}')
    try:
        if nlu_ref in ['train.deep_sentence_detector','train.sentence_detector']:
            #no label col but trainable?
            return  nlu.NLUSentenceDetector(annotator_class = 'deep_sentence_detector', trainable='True')
        if nlu_ref in ['train.context_spell','train.spell'] :
            pass
        if nlu_ref in ['train.symmetric_spell'] :
            pass
        if nlu_ref in ['train.norvig_spell'] :
            pass
        if nlu_ref in ['train.unlabeled_dependency_parser'] :
            pass
        if nlu_ref in ['train.labeled_dependency_parser'] :
            pass
        if nlu_ref in ['train.classifier_dl','train.classifier'] :
            return nlu.Classifier(annotator_class = 'classifier_dl', trainable=True)
        if nlu_ref in ['train.ner','train.named_entity_recognizer_dl'] :
            return nlu.Classifier(annotator_class = 'ner', trainable=True)
        if nlu_ref in ['train.sentiment_dl','train.sentiment'] :
            return nlu.Classifier(annotator_class = 'sentiment_dl', trainable=True)
        if nlu_ref in ['train.vivekn_sentiment'] :
            pass
        if nlu_ref in ['train.pos'] :
            return nlu.Classifier(annotator_class = 'pos', trainable=True)
        if nlu_ref in ['train.multi_classifier'] :
            return nlu.Classifier(annotator_class = 'multi_classifier', trainable=True)
        if nlu_ref in ['train.word_seg','train.word_segmenter'] :
            return nlu.Tokenizer(annotator_class = 'word_segmenter', trainable=True)


    except:  # if reference is not in namespace and not a component it will cause a unrecoverable crash
        logger.exception(f'EXCEPTION: Could not create trainable NLU component for nlu_ref = {nlu_ref} and nlp_ref = {nlp_ref}')
        return None

def construct_component_from_pipe_identifier(language, nlp_ref, nlu_ref,path=None):
    '''
    # creates a list of components from a Spark NLP Pipeline reference
    # 1. download pipeline
    # 2. unpack pipeline to annotators and create list of nlu components
    # 3. return list of nlu components
    :param nlu_ref:
    :param language: language of the pipeline
    :param nlp_ref: Reference to a spark nlp petrained pipeline
    :param path: Load pipe from HDD
    :return: Each element of the SaprkNLP pipeline wrapped as a NLU componed inside of a list
    '''
    logger.info("Starting Spark NLP to NLU pipeline conversion process")
    from sparknlp.pretrained import PretrainedPipeline, LightPipeline
    if 'language' in nlp_ref: language = 'xx'  # special edge case for lang detectors
    if path == None :
        pipe = PretrainedPipeline(nlp_ref, lang=language)
        iterable_stages = pipe.light_model.pipeline_model.stages
    else :
        pipe = LightPipeline(PipelineModel.load(path=path))
        iterable_stages = pipe.pipeline_model.stages
    constructed_components = []

    # for component in pipe.light_model.pipeline_model.stages:
    for component in iterable_stages:

        logger.info("Extracting model from Spark NLP pipeline: %s and creating Component", component)
        parsed = str(component).split('_')[0].lower()
        logger.info("Parsed Component for : %s", parsed)
        c_name = component.__class__.__name__
        if isinstance(component, NerConverter):
            constructed_components.append(Util(annotator_class='ner_converter', model=component))
        elif parsed in NameSpace.word_embeddings + NameSpace.sentence_embeddings:
            constructed_components.append(nlu.Embeddings(model=component))
        elif parsed in NameSpace.classifiers:
            constructed_components.append(nlu.Classifier(model=component))
        elif isinstance(component, MultiClassifierDLModel):
            constructed_components.append(nlu.Classifier(model=component, nlp_ref='multiclassifierdl'))
        elif isinstance(component, PerceptronModel):
            constructed_components.append(nlu.Classifier(nlp_ref='classifierdl', model=component))
        elif isinstance(component, (ClassifierDl,ClassifierDLModel)):
            constructed_components.append(nlu.Classifier(nlp_ref='classifierdl', model=component))
        elif isinstance(component, UniversalSentenceEncoder):
            constructed_components.append(nlu.Embeddings(model=component, nlp_ref='use'))
        elif isinstance(component, BertEmbeddings):
            constructed_components.append(nlu.Embeddings(model=component, nlp_ref='bert'))
        elif isinstance(component, AlbertEmbeddings):
            constructed_components.append(nlu.Embeddings(model=component, nlp_ref='albert'))
        elif isinstance(component, XlnetEmbeddings):
            constructed_components.append(nlu.Embeddings(model=component, nlp_ref='xlnet'))
        elif isinstance(component, WordEmbeddingsModel):
            constructed_components.append(nlu.Embeddings(model=component, nlp_ref='glove'))
        elif isinstance(component, ElmoEmbeddings):
            constructed_components.append(nlu.Embeddings(model=component, nlp_ref='elmo'))
        elif isinstance(component, BertSentenceEmbeddings):
            constructed_components.append(nlu.Embeddings(model=component, nlp_ref='bert_sentence'))
        elif isinstance(component, UniversalSentenceEncoder):
            constructed_components.append(nlu.Embeddings(model=component, nlu_ref='use'))
        elif isinstance(component, TokenizerModel) and parsed != 'regex':
            constructed_components.append(nlu.Tokenizer(model=component))
        elif isinstance(component, TokenizerModel) and parsed == 'regex' :
            constructed_components.append(nlu.Tokenizer(model=component, annotator_class='regex_tokenizer'))
        elif isinstance(component, DocumentAssembler):
            constructed_components.append(nlu.Util(model=component))
        elif isinstance(component, SentenceDetectorDLModel):
            constructed_components.append(NLUSentenceDetector(annotator_class='deep_sentence_detector', model=component))
        elif isinstance(component, (SentenceDetectorDLModel, SentenceDetector)):
            constructed_components.append(NLUSentenceDetector(annotator_class='pragmatic_sentence_detector', model=component))
        elif isinstance(component, RegexMatcherModel) or parsed == 'match':
            constructed_components.append(nlu.Matcher(model=component, annotator_class='regex'))
        elif isinstance(component, TextMatcherModel):
            constructed_components.append(nlu.Matcher(model=component, annotator_class='text'))
        elif isinstance(component, DateMatcher):
            constructed_components.append(nlu.Matcher(model=component, annotator_class='date'))
        elif isinstance(component, ContextSpellCheckerModel):
            constructed_components.append(nlu.SpellChecker(model=component, annotator_class='context'))
        elif isinstance(component, SymmetricDeleteModel):
            constructed_components.append(nlu.SpellChecker(model=component, annotator_class='symmetric'))
        elif isinstance(component, NorvigSweetingModel):
            constructed_components.append(nlu.SpellChecker(model=component, annotator_class='norvig'))
        elif isinstance(component, LemmatizerModel):
            constructed_components.append(nlu.lemmatizer.Lemmatizer(model=component))
        elif isinstance(component, NormalizerModel):
            constructed_components.append(nlu.normalizer.Normalizer(model=component))
        elif isinstance(component, Stemmer):
            constructed_components.append(nlu.stemmer.Stemmer(model=component))
        elif isinstance(component, (NerDLModel, NerCrfModel)):
            component.setIncludeConfidence(True) # Pipes dont always extrat confidences, so here we enable all pipes to extract confidences manually
            constructed_components.append(nlu.Classifier(model=component, annotator_class='ner'))
        elif isinstance(component, LanguageDetectorDL):
            constructed_components.append(nlu.Classifier(model=component, annotator_class='language_detector'))

        elif isinstance(component, DependencyParserModel):
            constructed_components.append(UnlabledDepParser(model=component))
        elif isinstance(component, TypedDependencyParserModel):
            constructed_components.append(LabledDepParser(model=component))
        elif isinstance(component, MultiClassifierDLModel):
            constructed_components.append(nlu.Classifier(model=component, nlp_ref='multiclassifierdl'))
        elif isinstance(component, (SentimentDetectorModel,SentimentDLModel)):
            constructed_components.append(nlu.Classifier(model=component, nlp_ref='sentimentdl'))
        elif isinstance(component, (SentimentDetectorModel,ViveknSentimentModel)):
            constructed_components.append(nlu.Classifier(model=component, nlp_ref='vivekn'))
        elif isinstance(component, Chunker):
            constructed_components.append(nlu.chunker.Chunker(model=component))
        elif isinstance(component, NGram):
            constructed_components.append(nlu.chunker.Chunker(model=component))
        elif isinstance(component, ChunkEmbeddings):
            constructed_components.append(embeddings_chunker.EmbeddingsChunker(model=component))
        elif isinstance(component, StopWordsCleaner):
            constructed_components.append(nlu.StopWordsCleaner(model=component))
        elif isinstance(component, (TextMatcherModel, RegexMatcherModel, DateMatcher,MultiDateMatcher)) or parsed == 'match':
            constructed_components.append(nlu.Matcher(model=component))
        elif isinstance(component,(T5Transformer)):
            constructed_components.append(nlu.Seq2Seq(annotator_class='t5', model=component))
        elif isinstance(component,(MarianTransformer)):
            constructed_components.append(nlu.Seq2Seq(annotator_class='marian', model=component))
        else:
            logger.exception(
                f"EXCEPTION: Could not infer component type for lang={language} and nlp_ref={nlp_ref} and model {component} during pipeline conversion,")
            logger.info("USING DEFAULT ANNOTATOR TYPE Lemmatizer to fix issue")
            constructed_components.append(nlu.normalizer.Normalizer(model=component))

        logger.info(f"Extracted into NLU Component type : {parsed}", )
        if None in constructed_components:
            logger.exception(
                f"EXCEPTION: Could not infer component type for lang={language} and nlp_ref={nlp_ref} during pipeline conversion,")
            return None
    return constructed_components


def construct_component_from_identifier(language, component_type='', dataset='', component_embeddings='', nlu_ref='',
                                        nlp_ref=''):
    '''
    Creates a NLU component from a pretrained SparkNLP model reference or Class reference.
    Class references will return default pretrained models
    :param language: Language of the sparknlp model reference
    :param component_type: Class which will be used to instantiate the model
    :param dataset: Dataset that the model was trained on
    :param component_embeddings: Embedded that the models was traiend on (if any)
    :param nlu_ref: Full user request
    :param nlp_ref: Full Spark NLP reference
    :return: Returns a NLU component which embelished the Spark NLP pretrained model and class for that model
    '''
    logger.info('Creating singular NLU component for type=%s sparknlp_ref=%s , dataset=%s, language=%s , nlu_ref=%s ',
                component_type, nlp_ref, dataset, language, nlu_ref)
    try:

        if any(
            x in NameSpace.seq2seq for x in [nlp_ref, nlu_ref, dataset, component_type, ]):
            return Seq2Seq(annotator_class=component_type, language=language, get_default=False, nlp_ref=nlp_ref,configs=dataset)

        # if any([component_type in NameSpace.word_embeddings,dataset in NameSpace.word_embeddings, nlu_ref in NameSpace.word_embeddings, nlp_ref in NameSpace.word_embeddings]):
        elif any(x in NameSpace.word_embeddings and not x in NameSpace.classifiers for x in
               [nlp_ref, nlu_ref, dataset, component_type, ] + dataset.split('_')):
            return Embeddings(get_default=False, nlp_ref=nlp_ref, nlu_ref=nlu_ref, language=language)

        # elif any([component_type in NameSpace.sentence_embeddings,dataset in NameSpace.sentence_embeddings, nlu_ref in NameSpace.sentence_embeddings, nlp_ref in NameSpace.sentence_embeddings]):
        if any(x in NameSpace.sentence_embeddings and not x in NameSpace.classifiers for x in
               [nlp_ref, nlu_ref, dataset, component_type, ] + dataset.split('_')):
            return Embeddings(get_default=False, nlp_ref=nlp_ref, nlu_ref=nlu_ref, language=language)

        elif any(
                x in NameSpace.classifiers for x in [nlp_ref, nlu_ref, dataset, component_type, ] + dataset.split('_')):
            return Classifier(get_default=False, nlp_ref=nlp_ref, nlu_ref=nlu_ref, language=language)



        elif any('spell' in x for x in [nlp_ref, nlu_ref, dataset, component_type]):
            return SpellChecker(annotator_class=component_type, language=language, get_default=True, nlp_ref=nlp_ref,
                                dataset=dataset)

        elif any('dep' in x and not 'untyped' in x for x in [nlp_ref, nlu_ref, dataset, component_type]):
            return LabledDepParser()

        elif any('dep.untyped' in x or 'untyped' in x for x in [nlp_ref, nlu_ref, dataset, component_type]):
            return UnlabledDepParser()

        elif any('lemma' in x for x in [nlp_ref, nlu_ref, dataset, component_type]):
            return nlu.lemmatizer.Lemmatizer(language=language, nlp_ref=nlp_ref)

        elif any('norm' in x for x in [nlp_ref, nlu_ref, dataset, component_type]):
            return nlu.normalizer.Normalizer(nlp_ref=nlp_ref, nlu_ref=nlu_ref)
        elif any('clean' in x or 'stopword' in x for x in [nlp_ref, nlu_ref, dataset, component_type]):
            return nlu.StopWordsCleaner(language=language, get_default=False, nlp_ref=nlp_ref)
        elif any('sentence_detector' in x for x in [nlp_ref, nlu_ref, dataset, component_type]):
            return NLUSentenceDetector(nlu_ref=nlu_ref, nlp_ref=nlp_ref, language=language)

        elif any('match' in x for x in [nlp_ref, nlu_ref, dataset, component_type]):
            return Matcher(nlu_ref=nlu_ref, nlp_ref=nlp_ref)

# THIS NEEDS TO CAPTURE THE WORD SEGMNETER!!!
        elif any('tokenize' in x or 'segment_words' in x for x in [nlp_ref, nlu_ref, dataset, component_type]):
            return nlu.tokenizer.Tokenizer(nlp_ref=nlp_ref, nlu_ref=nlu_ref, language=language,get_default=False)

        elif any('stem' in x for x in [nlp_ref, nlu_ref, dataset, component_type]):
            return Stemmer()

        # supported in future version with auto embed generation
        # elif any('embed_chunk' in x for x in [nlp_ref, nlu_ref, dataset, component_type] ):
        #     return embeddings_chunker.EmbeddingsChunker()

        elif any('chunk' in x for x in [nlp_ref, nlu_ref, dataset, component_type]):
            return nlu.chunker.Chunker()
        elif component_type == 'ngram':
            return nlu.chunker.Chunker('ngram')

        logger.exception('EXCEPTION: Could not resolve singular Component for type=%s and nlp_ref=%s and nlu_ref=%s',
                         component_type, nlp_ref, nlu_ref)
        return None
    except:  # if reference is not in namespace and not a component it will cause a unrecoverable crash
        logger.exception('EXCEPTION: Could not resolve singular Component for type=%s and nlp_ref=%s and nlu_ref=%s',
                         component_type, nlp_ref, nlu_ref)
        return None


def extract_classifier_metadata_from_nlu_ref(nlu_ref):
    '''
    Extract classifier and metadataname from nlu reference which is handy for deciding what output column names should be
    Strips lang and action from nlu_ref and returns a list of remaining identifiers, i.e [<classifier_name>,<classifier_dataset>, <additional_classifier_meta>
    :param nlu_ref: nlu reference from which to extra model meta data
    :return: [<modelname>, <dataset>, <more_meta>,]  . For pure actions this will return []
    '''
    model_infos = []
    for e in nlu_ref.split('.'):
        if e in nlu.all_components_info.all_languages or e in nlu.namespace.NameSpace.actions: continue
        model_infos.append(e)
    return model_infos


class NluError:
    def __init__(self):
        self.has_trainable_components = False
    @staticmethod
    def predict(text, output_level='error', positions='error', metadata='error', drop_irrelevant_cols=False):
        print('The NLU components could not be properly created. Please check previous print messages and Verbose mode for further info')
    @staticmethod
    def print_info(): print("Sorry something went wrong when building the pipeline. Please check verbose mode and your NLU reference.")



#Discovery
def print_all_languages():
    ''' Print all languages which are available in NLU Spark NLP pointer '''
    discoverer.print_all_languages()
def print_all_nlu_components_for_lang(lang='en', c_type='classifier'):
    '''Print all NLU components available for a language Spark NLP pointer'''
    discoverer.print_all_nlu_components_for_lang(lang, c_type)
def print_all_nlu_components_for_lang(lang='en'):
    '''Print all NLU components available for a language Spark NLP pointer'''
    discoverer.print_all_nlu_components_for_lang(lang)
def print_components(lang='', action=''):
    '''Print every single NLU reference for models and pipeliens and their Spark NLP pointer
    :param lang: Language requirements for the components filterd. See nlu.languages() for supported languages
    :param action: Components that will be filterd.'''
    discoverer.print_components(lang,action)
def print_component_types():
    ''' Prints all unique component types in NLU'''
    discoverer.print_component_types()
def print_all_model_kinds_for_action(action):
    discoverer.print_all_model_kinds_for_action(action)
def print_all_model_kinds_for_action_and_lang(lang, action):
    discoverer.print_all_model_kinds_for_action_and_lang(lang,action)
def print_trainable_components():
    '''Print every trainable Algorithm/Model'''
    discoverer.print_trainable_components()
