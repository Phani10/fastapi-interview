import sys
sys.path.append("..")

from fastapi import HTTPException, status
from database.models import DbQuestion
from routers.schemas import  UserBase
from sqlalchemy.orm.session import Session
from database.hashing import Hash
import os
import pickle


def get_question_by_topic(db: Session, topic: str):
    file_path = './temp_files/questions_dict.pkl'
    if os.path.exists(file_path):
        print('------------- questions dict exists - db_questions -------------------')
        with open(file_path, 'rb') as f:
            questions_list = pickle.load(f)
        f.close()
        return questions_list

    print('-------------Retrieving questions dict - db_questions -------------------')
    questions_list = []
    data = db.query(DbQuestion).filter(DbQuestion.topic == topic).all()
    for row in data:
        temp_dict = {
            'answer': row.answer,
            'topic': row.topic,
            'id': row.id,
            'question': row.question
        }
        questions_list.append(temp_dict)
    print(questions_list)
    print('-------------Retrieved questions dict - db_questions -------------------')

    if not questions_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No questions for topic {topic} found in database')
    return questions_list
