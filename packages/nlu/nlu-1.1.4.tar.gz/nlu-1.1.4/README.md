
# NLU: The Power of Spark NLP, the Simplicity of Python
John Snow Labs' NLU is a Python library for applying state-of-the-art text mining, directly on any dataframe, with a single line of code.
As a facade of the award-winning Spark NLP library, it comes with hundreds of pretrained models in tens of languages - all production-grade, scalable, and trainable.

## Project's Website
Take a look at our official Spark NLU page: [https://nlu.johnsnowlabs.com/](https://nlu.johnsnowlabs.com/)  for user documentation and examples



## NLU in action 
<img src="http://ckl-it.de/wp-content/uploads/2020/08/My-Video6.gif" width="1800" height="500"/>

## Features
* Tokenization
* Trainable Word Segmentation
* Stop Words Removal
* Token Normalizer
* Document Normalizer
* Stemmer
* Lemmatizer
* NGrams
* Regex Matching
* Text Matching
* Chunking
* Date Matcher
* Sentence Detector
* Deep Sentence Detector (Deep learning)
* Dependency parsing (Labeled/unlabeled)
* Part-of-speech tagging
* Sentiment Detection (ML models)
* Spell Checker (ML and DL models)
* Word Embeddings (GloVe and Word2Vec)
* BERT Embeddings (TF Hub models)
* ELMO Embeddings (TF Hub models)
* ALBERT Embeddings (TF Hub models)
* XLNet Embeddings
* Universal Sentence Encoder (TF Hub models)
* BERT Sentence Embeddings (42 TF Hub models)
* Sentence Embeddings
* Chunk Embeddings
* Unsupervised keywords extraction
* Language Detection & Identification (up to 375 languages)
* Multi-class Sentiment analysis (Deep learning)
* Multi-label Sentiment analysis (Deep learning)
* Multi-class Text Classification (Deep learning)
* Neural Machine Translation
* Text-To-Text Transfer Transformer (Google T5)
* Named entity recognition (Deep learning)
* Easy TensorFlow integration
* GPU Support
* Full integration with Spark ML functions
* +710 pre-trained models in +192 languages!
* +450 pre-trained pipelines in +192 languages!
* Multi-lingual NER models: Arabic, Chinese, Danish, Dutch, English, Finnish, French, German, Hewbrew, Italian, Japanese, Korean, Norwegian, Persian, Polish, Portuguese, Russian, Spanish, Swedish, and Urdu.

## Getting Started with NLU 
To get your hands on the power of NLU, you just need to install it via pip and ensure Java 8 is installed and properly configured. Checkout [Quickstart for more infos](https://nlu.johnsnowlabs.com/docs/en/install)
```bash 
pip install nlu pyspark==2.4.7
``` 

## Loading and predict with any model in 1 line python 
```python
import nlu 
nlu.load('sentiment').predict('I love NLU! <3') 
``` 

## Loading and predict with multiple models in 1 line 

Get 6 different embeddings in 1 line and use them for downstream data science tasks! 

```python 
nlu.load('bert elmo albert xlnet glove use').predict('I love NLU! <3') 
``` 

## What kind of models does NLU provide? 
NLU provides everything a data scientist might want to wish for in one line of code!  
 - NLU provides everything a data scientist might want to wish for in one line of code!
 - 1000 + pre-trained models
 - 100+ of the latest NLP word embeddings ( BERT, ELMO, ALBERT, XLNET, GLOVE, BIOBERT, ELECTRA, COVIDBERT) and different variations of them
 - 50+ of the latest NLP sentence embeddings ( BERT, ELECTRA, USE) and different variations of them
 - 100+ Classifiers (NER, POS, Emotion, Sarcasm, Questions, Spam)
 - 300+ Supported Languages
- Summarize Text and Answer Questions with T5
- Labeled and Unlabeled Dependency parsing
 - Various Text Cleaning and Pre-Processing methods like Stemming, Lemmatizing, Normalizing, Filtering, Cleaning pipelines and more


## Classifiers trained on many different different datasets 
Choose the right tool for the right task! Whether you analyze movies or twitter, NLU has the right model for you! 

- trec6 classifier 
- trec10 classifier 
- spam classifier 
- fake news classifier 
- emotion classifier 
- cyberbullying classifier 
- sarcasm classifier 
- sentiment classifier for movies 
- IMDB Movie Sentiment classifier 
- Twitter sentiment classifier 
- NER pretrained on ONTO notes 
- NER trainer on CONLL 
- Language classifier for 20 languages on the wiki 20 lang dataset. 

## Utilities for the Data Science NLU applications 
Working with text data can sometimes be quite a dirty Job. NLU helps you keep your hands clean by providing lots of components that take away data engineering intensive tasks. 

- Datetime Matcher
- Pattern Matcher
- Chunk Matcher
- Phrases Matcher
- Stopword Cleaners
- Pattern Cleaners
- Slang Cleaner 

## Where can I see NLUs entire offer? 
Checkout the [NLU Namespace](https://nlu.johnsnowlabs.com/docs/en/namespace) for everything that NLU has to offer! 



## Supported Data Types
- Pandas DataFrame and Series
- Spark DataFrames
- Modin with Ray backend
- Modin with Dask backend
- Numpy arrays
- Strings and lists of strings 


Checkout the following notebooks for examples on how to work with NLU.


# NLU Demos on Datasets
- [Kaggle Twitter Airline Sentiment Analysis NLU demo](https://www.kaggle.com/kasimchristianloan/nlu-sentiment-airline-demo)
- [Kaggle Twitter Airline Emotion Analysis NLU demo](https://www.kaggle.com/kasimchristianloan/nlu-emotion-airline-demo)
- [Kaggle Twitter COVID Sentiment Analysis NLU demo](https://www.kaggle.com/kasimchristianloan/nlu-covid-sentiment-showcase)
- [Kaggle Twitter COVID Emotion Analysis nlu demo](https://www.kaggle.com/kasimchristianloan/nlu-covid-emotion-showcase)


# NLU component examples
Checkout the following notebooks for examples on how to work with NLU.


## NLU Training Examples
### Binary Class Text Classification training
- [2 class Finance News sentiment classifier training](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/Training/binary_text_classification/NLU_training_sentiment_classifier_demo_apple_twitter.ipynb)
- [2 class Reddit comment sentiment classifier training](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/Training/binary_text_classification/NLU_training_sentiment_classifier_demo_reddit.ipynb)
- [2 class Apple Tweets sentiment classifier training](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/Training/binary_text_classification/NLU_training_sentiment_classifier_demo_IMDB.ipynb)
- [2 class IMDB Movie sentiment classifier training](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/Training/binary_text_classification/NLU_training_sentiment_classifier_demo_IMDB.ipynb)
- [2 class twitter classifier training](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/Training/binary_text_classification/NLU_training_sentiment_classifier_demo_twitter.ipynb)

### Multi Class Text Classification training
- [5 class WineEnthusiast Wine review classifier training](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/Training/multi_class_text_classification/NLU_training_multi_class_text_classifier_demo_wine.ipynb)
- [3 class Amazon Phone review classifier training](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/Training/multi_class_text_classification/NLU_training_multi_class_text_classifier_demo_amazon.ipynb)
- [5 class Amazon Musical Instruments review classifier training](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/Training/multi_class_text_classification/NLU_training_multi_class_text_classifier_demo_musical_instruments.ipynb)
- [5 class Tripadvisor Hotel review classifier training](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/Training/multi_class_text_classification/NLU_training_multi_class_text_classifier_demo_hotel_reviews.ipynb)
- [5 class Phone review classifier training](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/Training/multi_class_text_classification/NLU_training_multi_class_text_classifier_demo_hotel_reviews.ipynb)

### Multi Label Text  Classification training
- [ Train Multi Label Classifier on E2E dataset Demo](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/Training/multi_label_text_classification/NLU_traing_multi_label_classifier_E2e.ipynb)
- [Train Multi Label  Classifier on Stack Overflow Question Tags dataset Demo](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/Training/multi_label_text_classification/NLU_training_multi_token_label_text_classifier_stackoverflow_tags.ipynb)

### Named Entity Recognition training (NER)
- [NER Training example](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/Training/named_entity_recognition/NLU_training_NER_demo.ipynb)

### Part of Speech tagger training (POS)
- [POS Training example](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/Training/part_of_speech/NLU_training_POS_demo.ipynb)

## NLU Applications Examples
- [Sentence Similarity with Multiple Sentence Embeddings](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/sentence_embeddings/sentence_similarirty_stack_overflow_questions.ipynb)
- [6 Wordembeddings in 1 line with T-SNE plotting](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/word_embeddings/NLU_multiple_word_embeddings_and_t-SNE_visualization_example.ipynb)

## NLU Demos on Datasets

- [Kaggle Twitter Airline Sentiment Analysis NLU demo](https://www.kaggle.com/kasimchristianloan/nlu-sentiment-airline-demo)
- [Kaggle Twitter Airline Emotion Analysis NLU demo](https://www.kaggle.com/kasimchristianloan/nlu-emotion-airline-demo)
- [Kaggle Twitter COVID Sentiment Analysis NLU demo](https://www.kaggle.com/kasimchristianloan/nlu-covid-sentiment-showcase)
- [Kaggle Twitter COVID Emotion Analysis nlu demo](https://www.kaggle.com/kasimchristianloan/nlu-covid-emotion-showcase)




## NLU examples grouped by component

The following are Collab examples which showcase each NLU component and some applications.

### Named Entity Recognition (NER)

- [NER pretrained on ONTO Notes](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/named_entity_recognition_(NER)/NLU_ner_ONTO_18class_example.ipynb)
- [NER pretrained on CONLL](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/named_entity_recognition_(NER)/NLU_ner_CONLL_2003_5class_example.ipynb)
- [Tokenize, extract POS and NER in Chinese](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/multilingual/chinese_ner_pos_and_tokenization.ipynb)
- [Tokenize, extract POS and NER in Korean](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/multilingual/korean_ner_pos_and_tokenization.ipynb)
- [Tokenize, extract POS and NER in Japanese](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/multilingual/japanese_ner_pos_and_tokenization.ipynb)
- [Aspect based sentiment NER sentiment for restaurants](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/named_entity_recognition_(NER)/aspect_based_ner_sentiment_restaurants.ipynb)


### Part of speech (POS)

- [POS pretrained on ANC dataset](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/part_of_speech(POS)/NLU_part_of_speech_ANC_example.ipynb)
- [Tokenize, extract POS and NER in Chinese](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/multilingual/chinese_ner_pos_and_tokenization.ipynb)
- [Tokenize, extract POS and NER in Korean](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/multilingual/korean_ner_pos_and_tokenization.ipynb)
- [Tokenize, extract POS and NER in Japanese](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/multilingual/japanese_ner_pos_and_tokenization.ipynb)

### Sequence2Sequence
- [Translate between 192+ languages with marian](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/sequence2sequence/translation_demo.ipynb)
- [Try out the 18 Tasks like Summarization Question Answering and more on T5](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/sequence2sequence/T5_tasks_summarize_question_answering_and_more)
- [T5 Open and Closed Book question answering tutorial](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/sequence2sequence/T5_question_answering.ipynb)



###  Classifiers
- [Unsupervised Keyword Extraction with YAKE](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/classifiers/unsupervised_keyword_extraction_with_YAKE.ipynb)
- [Toxic Text Classifier](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/classifiers/toxic_classification.ipynb)
- [Twitter Sentiment Classifier](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/classifiers/sentiment_classification.ipynb)
- [Movie Review Sentiment Classifier](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/classifiers/sentiment_classification_movies.ipynb)
- [Sarcasm Classifier](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/classifiers/sarcasm_classification.ipynb)
- [50 Class Questions Classifier](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/classifiers/question_classification.ipynb)
- [300 Class Languages Classifier](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/classifiers/NLU_language_classification.ipynb)
- [Fake News Classifier](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/classifiers/fake_news_classification.ipynb)
- [E2E Classifier](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/classifiers/E2E_classification.ipynb)
- [Cyberbullying Classifier](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/classifiers/cyberbullying_cassification_for_racism_and_sexism.ipynb)
- [Spam Classifier](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/classifiers/spam_classification.ipynb)
- [Emotion Classifier](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/classifiers/emotion_classification.ipynb)

### Word Embeddings
- [BERT, ALBERT, ELMO, ELECTRA, XLNET, GLOVE at once with t-SNE plotting](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/word_embeddings/NLU_multiple_word_embeddings_and_t-SNE_visualization_example.ipynb)
- [BERT Word Embeddings and t-SNE plotting](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/word_embeddings/NLU_BERT_word_embeddings_and_t-SNE_visualization_example.ipynb)
- [ALBERT Word Embeddings and t-SNE plotting](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/word_embeddings/NLU_ALBERT_word_embeddings_and_t-SNE_visualization_example.ipynb)
- [ELMO Word Embeddings and t-SNE plotting](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/word_embeddings/NLU_ELMo_word_embeddings_and_t-SNE_visualization_example.ipynb)
- [XLNET Word Embeddings and t-SNE plotting](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/word_embeddings/NLU_XLNET_word_embeddings_and_t-SNE_visualization_example.ipynb)
- [ELECTRA Word Embeddings and t-SNE plotting](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/word_embeddings/NLU_ELECTRA_word_embeddings_and_t-SNE_visualization_example.ipynb)
- [COVIDBERT Word Embeddings and t-SNE plotting](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/word_embeddings/NLU_COVIDBERT_word_embeddings_and_t-SNE_visualization_example.ipynb)
- [BIOBERT Word Embeddings and t-SNE plotting](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/word_embeddings/NLU_BIOBERT_word_embeddings_and_t-SNE_visualization_example.ipynb)
- [GLOVE Word Embeddings and t-SNE plotting](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/word_embeddings/NLU_GLOVE_word_embeddings_and_t-SNE_visualization_example.ipynb)

### Sentence Embeddings
- [BERT Sentence Embeddings and t-SNE plotting](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/sentence_embeddings/NLU_BERT_sentence_embeddings_and_t-SNE_visualization_Example.ipynb)
- [ELECTRA Sentence Embeddings and t-SNE plotting](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/sentence_embeddings/NLU_ELECTRA_sentence_embeddings_and_t-SNE_visualization_example.ipynb)
- [USE Sentence Embeddings and t-SNE plotting](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/sentence_embeddings/NLU_USE_sentence_embeddings_and_t-SNE_visualization_example.ipynb)

### Sentence Embeddings
- [BERT Sentence Embeddings and t-SNE plotting](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/sentence_embeddings/NLU_BERT_sentence_embeddings_and_t-SNE_visualization_Example.ipynb)
- [ELECTRA Sentence Embeddings and t-SNE plotting](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/sentence_embeddings/NLU_ELECTRA_sentence_embeddings_and_t-SNE_visualization_example.ipynb)
- [USE Sentence Embeddings and t-SNE plotting](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/sentence_embeddings/NLU_USE_sentence_embeddings_and_t-SNE_visualization_example.ipynb)


### Dependency Parsing
- [Untyped Dependency Parsing](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/dependency_parsing/NLU_untyped_dependency_parsing_example.ipynb)
- [Typed Dependency Parsing](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/dependency_parsing/NLU_typed_dependency_parsing_example.ipynb)


### Text Pre Processing and Cleaning
- [Tokenization](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/text_pre_processing_and_cleaning/NLU_tokenization_example.ipynb)
- [Stopwords removal](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/text_pre_processing_and_cleaning/NLU_stopwords_removal_example.ipynb)
- [Stemming](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/text_pre_processing_and_cleaning/NLU_stemmer_example.ipynb)
- [Lemmatization](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/text_pre_processing_and_cleaning/NLU_lemmatization.ipynb)
- [Normalizing](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/text_pre_processing_and_cleaning/NLU_normalizer_example.ipynb)
- [Spell checking](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/text_pre_processing_and_cleaning/NLU_spellchecking_example.ipynb)
- [Sentence Detecting](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/text_pre_processing_and_cleaning/NLU_sentence_detection_example.ipynb)
- [Normalize documents](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/text_pre_processing_and_cleaning/document_normalizer_demo.ipynb)


### Chunkers
- [N Gram](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/chunkers/NLU_n-gram.ipynb)
- [Entity Chunking](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/chunkers/NLU_chunking_example.ipynb)


### Matchers

- [Date Matcher](https://github.com/JohnSnowLabs/nlu/blob/master/examples/colab/component_examples/matchers/NLU_date_matching.ipynb)


# Need help? 
- [Ping us on Slack](https://spark-nlp.slack.com/archives/C0196BQCDPY) 
- [Post an issue on Github](https://github.com/JohnSnowLabs/nlu/issues)

# Simple NLU Demos
- [NLU different output levels Demo](https://colab.research.google.com/drive/1C4N3wpC17YzZf9fXHDNAJ5JvSmfbq7zT?usp=sharing)


