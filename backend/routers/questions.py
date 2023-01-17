import sys
sys.path.append("..")

from auth.oauth2 import get_current_user
from fastapi import APIRouter, Depends, status, UploadFile, File
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from database import db_question
from routers.schemas import UserAuth
import pickle
from routers.similar_questions import get_similar_questions
import os

router = APIRouter(prefix='/question', tags=['question'])


@router.get('/{topic}')
def get_question(topic: str, db: Session = Depends(get_db)):
    questions_list = db_question.get_question_by_topic(db, topic)

    answer_path = './temp_files/answer_string.txt'
    if not os.path.exists(answer_path):
        return 'Please introduce yourself'

    file = open(answer_path)
    answer = file.readlines()
    file.close()

    question, questions_list = get_similar_questions(answer, questions_list)

    file_path = './temp_files/questions_dict.pkl'
    with open(file_path, 'wb') as f:
        pickle.dump(questions_list, f)
    f.close()

    return question
