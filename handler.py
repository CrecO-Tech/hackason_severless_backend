import json
import logging
from pydantic import BaseModel
import asyncio
from utils import get_image_from_firebase
from utils import get_subject_image_path
from utils import get_percent_from_theme, peaple_and_developer_score, get_face_score

class Question(BaseModel):
    imageUrl: str  # URL of the image taken by the user
    themeNumber: int  # Theme number: 1-5 for 1 person, 6-10 for 2 persons, 11-15 for 3-4 persons

def question1(event, context):
    try:
        num_of_questions = 1
         # JSON データを解析し、Pydantic モデルに変換
        question = Question(**json.loads(event['body']))
        print("Parsed question:", question)
        
        # Firebaseから画像をダウンロード
        image =  asyncio.run(get_image_from_firebase(question.imageUrl))
        if image is None:
            return {
                "statusCode": 500,
                "body": {"detail": "Failed to decode image"}
            }

  
        max_people_score = 15
        people_score, original_score_ratio = peaple_and_developer_score(image, question.themeNumber, max_people_score)
        original_score = original_score_ratio * 15
     

        theme_image_path = get_subject_image_path(num_of_questions, question.themeNumber)
        exclude_ratio, include_ratio = get_percent_from_theme(image, theme_image_path)
        include_score = include_ratio * 35
        exclude_score = exclude_ratio * 35

     

        # Prepare response
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "includeScore": int(include_score),
                "excludeScore": int(exclude_score),
                "peopleScore": int(people_score),
                "originalScore": int(original_score)
            })
        }

    except Exception as e:
        # Handle exceptions
        logging.error(f"Error processing the request: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"detail": "Server error"})
        }

def question2(event, context):
    # ここでスコアデータを処理します
    # 開発者の主観15点満点
    # 人数 15点満点
    # はみ出しているか35点満点
    # 枠がどれだけ埋まっているか35点満点
    question = Question(**json.loads(event['body']))
    num_of_questions = 2
    # Firebase Storageから画像をダウンロード
    image = asyncio.run(get_image_from_firebase(question.imageUrl))
    if image is None:
        return {
                "statusCode": 500,
                "body": {"detail": "Failed to decode image"}
            }
    
    # 人数によるスコアを取得
    max_peaple_score = 15
    peaple_score, original_score_raito = peaple_and_developer_score(image, question.themeNumber, max_peaple_score)

    print(f'peaple_score: {peaple_score}')

    # 開発者の主観スコア
    original_score = original_score_raito * 15
    # お題の画像を取得
    theme_image_path = get_subject_image_path(num_of_questions, question.themeNumber)

    # はみ出している割合と含まれている割合を計算
    exclude_ratio, include_ratio = get_percent_from_theme(image, theme_image_path)

    include_score = include_ratio * 35
    exclude_score = exclude_ratio * 35

    exclude_score = 0 if exclude_score < 0 else exclude_score

    logging.info(f"include_ratio: {include_ratio}, hamidashi_ratio: {exclude_ratio}")
   
    return {"includeScore": int(include_score) , "excludeScore": int(exclude_score), "peopleScore": int(peaple_score), "originalScore": int(original_score)}
# Additional functions used within the handler, such as image processing, need to be defined here or imported.


def question3(event, context):
    # ここでスコアデータを処理します
    # 開発者の主観 20点
    # 人数 20点
    # はみ出しているか 45点
    # 枠がどれだけ埋まっているか 45点
    # 表情: 20
    question = Question(**json.loads(event['body']))

    num_of_questions = 3
    # Firebase Storageから画像をダウンロード
    image = asyncio.run(get_image_from_firebase(question.imageUrl))
    if image is None:
        return {
                "statusCode": 500,
                "body": {"detail": "Failed to decode image"}
            }

    print(f'num_of_questions: {num_of_questions}')
   # 人数によるスコアを取得
    max_peaple_score = 20
    peaple_score, original_score_raito = peaple_and_developer_score(image, question.themeNumber, max_peaple_score)

    print(f'peaple_score: {peaple_score}')

    # 開発者の主観スコア
    original_score = original_score_raito * 20

    # お題の画像を取得
    theme_image_path = get_subject_image_path(num_of_questions, question.themeNumber)
    
    # はみ出している割合と含まれている割合を計算
    exclude_ratio, include_ratio = get_percent_from_theme(image, theme_image_path)

    include_score = include_ratio * 45
    exclude_score = exclude_ratio * 45

    logging.info(f"include_ratio: {include_ratio}, hamidashi_ratio: {exclude_ratio}")

    # 表情のスコアを取得
    emotional_ratio = get_face_score(image, num_of_questions, question.themeNumber)
    emotion_score = emotional_ratio * 20

    return {"includeScore": int(include_score) , "excludeScore": int(exclude_score), "peopleScore": int(peaple_score), "originalScore": int(original_score), "faceScore": int(emotion_score)}

def question4(event, context):
    # ここでスコアデータを処理します
    # 開発者の主観 20点
    # 人数 20点
    # はみ出しているか 45点
    # 枠がどれだけ埋まっているか 45点
    # 表情: 20
    question = Question(**json.loads(event['body']))

    num_of_questions = 4
    # Firebase Storageから画像をダウンロード
    image =  asyncio.run(get_image_from_firebase(question.imageUrl))
    if image is None:
        return {
                "statusCode": 500,
                "body": {"detail": "Failed to decode image"}
            }

    # 人数によるスコアを取得
    max_peaple_score = 20
    peaple_score, original_score_raito = peaple_and_developer_score(image, question.themeNumber, max_peaple_score)

    print(f'peaple_score: {peaple_score}')

    # 開発者の主観スコア
    original_score = original_score_raito * 20

    # お題の画像を取得
    theme_image_path = get_subject_image_path(num_of_questions, question.themeNumber)
    
    # はみ出している割合と含まれている割合を計算
    exclude_ratio, include_ratio = get_percent_from_theme(image, theme_image_path)

    include_score = include_ratio * 45
    exclude_score = exclude_ratio * 45

    logging.info(f"include_ratio: {include_ratio}, hamidashi_ratio: {exclude_ratio}")

    # 表情のスコアを取得
    emotional_ratio =  get_face_score(image, num_of_questions, question.themeNumber)
    emotion_score = emotional_ratio * 20


    return {"includeScore": int(include_score) , "excludeScore": int(exclude_score), "peopleScore": int(peaple_score), "originalScore": int(original_score), "faceScore": int(emotion_score)}
