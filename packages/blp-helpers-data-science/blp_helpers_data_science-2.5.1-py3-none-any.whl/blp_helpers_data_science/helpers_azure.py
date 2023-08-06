from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import logging
import pandas as pd
import ast


def get_text_analytics_client(azure_key, azure_endpoint):
    ta_credential = AzureKeyCredential(azure_key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=azure_endpoint,
            credential=ta_credential)
    return text_analytics_client


def get_entities(documents, client):
    """
    :param documents: should look like this: text = ['This sentence talks about iPhones and Sushi.']
    :param client:
    :return:
    """
    try:
        result = client.recognize_entities(documents=documents)[0]
        entities = result.entities
        return entities
    except Exception as err:
        print("Encountered exception. {}".format(err))


def get_entities_for_category(entities_base, entity_category):
    """
    :param entity_category: could be for instance 'Organization'
    :param entities_base: entities as returned from azure, has all entities, from which entity_category will be filtered
    :return: entities_filtered

    Example:

    entity_category = 'Product'
    entities_base = [CategorizedEntity(text=Buches, category=Product, subcategory=None, confidence_score=0.86),
                     CategorizedEntity(text=Mädelsabend, category=Event, subcategory=None, confidence_score=0.81)]
    entities_filtered = '['Buches']'
    """
    entities_filtered = ''
    try:
        entities_filtered = [entity.text for entity in entities_base if entity.category == entity_category]
    except:
        pass
    return entities_filtered


def get_sentiment(client, documents, show_documents_stats=False, documents_language='de'):
    """
    :param client: TextAnalyticsClient
    :param documents: for instance ["this is the text", "this is another doc"]
    :param show_documents_stats: see official doc
    :param documents_language: see official doc
    :return: sentiment_overall_all_docs, sentiment_sentences_all_docs
    pandas data frames for the overall doc and each sentence in each doc

    """
    def _get_confidence_score_from_dict(response_dict):
        return str(response_dict.get('confidence_scores'))

    def _get_individual_sentiments(data_frame, tgt_column_prefix, src_column):
        individual_sentiments = [
            'positive'
            , 'neutral'
            , 'negative'
        ]

        for suffix in individual_sentiments:
            data_frame[tgt_column_prefix + '_' + suffix] = data_frame.apply(
                lambda x: ast.literal_eval(x[src_column]).get(suffix), axis=1)

        return data_frame

    logger = logging.getLogger("azure.core.pipeline.policies.http_logging_policy")
    logger.setLevel(logging.WARNING)
    response_set = client.analyze_sentiment(
        documents=documents
        , show_stats=show_documents_stats
        , language=documents_language
    )

    sentiment_sentences_all_docs = pd.DataFrame()
    sentiment_overall_all_docs = pd.DataFrame()

    for doc_idx, response in enumerate(response_set):
        df_idx = sentiment_overall_all_docs.shape[0]
        overall__id = response.get('id')

        sentiment_overall_all_docs.loc[df_idx, 'overall__sentiment'] = response.get('sentiment')
        sentiment_overall_all_docs.loc[df_idx, 'overall__id'] = overall__id
        sentiment_overall_all_docs.loc[df_idx, 'doc_text'] = documents[doc_idx]
        sentiment_overall_all_docs.loc[df_idx, 'overall__confidence_scores'] = _get_confidence_score_from_dict(response)

        # do stuff on sentence level
        sentences = response.get('sentences')
        if not sentences:
            continue

        for sentence in sentences:
            df_idx = sentiment_sentences_all_docs.shape[0]

            sentiment_sentences_all_docs.loc[df_idx, 'sentence__text'] = sentence.get('text')
            sentiment_sentences_all_docs.loc[df_idx, 'sentence__sentiment'] = sentence.get('sentiment')
            sentiment_sentences_all_docs.loc[df_idx, 'sentence__confidence_scores'] = _get_confidence_score_from_dict(
                sentence)
            sentiment_sentences_all_docs.loc[df_idx, 'sentence__overall__id'] = overall__id

    sentiment_overall_all_docs = _get_individual_sentiments(
        sentiment_overall_all_docs
        , 'overall__confidence_score'
        , 'overall__confidence_scores'

    )
    sentiment_sentences_all_docs = _get_individual_sentiments(
        sentiment_sentences_all_docs
        , 'sentence__confidence_score'
        , 'sentence__confidence_scores'
    )

    return sentiment_overall_all_docs, sentiment_sentences_all_docs
