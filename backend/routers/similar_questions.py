import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('bert-base-nli-mean-tokens')


def sent_cleaning(sent):
    sent = sent.replace('\t',' ')
    sent = sent.replace('\n', ' ')
    sent = sent.replace('•', ' ')
    return sent


def get_similar_questions(answer, questions_list):
    print('--------------------- Inside get_similar_questions ----------------------')
    df = pd.DataFrame.from_records(questions_list)
    print(df.head())
    df['combined'] = df['question'] + ' ' + df['answer']
    df['combined'] = df['combined'].apply(sent_cleaning)
    sentences = list(df['combined'])
    sentence_embeddings = model.encode(sentences)

    try:
        new_sent_embedding = model.encode([answer[0]])
    except (IndexError, Exception) as e:
        print(e)
        new_sent_embedding = model.encode([' '])

    dist = cosine_similarity(
        [new_sent_embedding[0]],
        sentence_embeddings
    )
    question = df['question'][np.argmax(dist)]
    del questions_list[np.argmax(dist)]

    return question, questions_list
