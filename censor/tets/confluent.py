import requests
from confluent_kafka import Producer, Consumer
from profanity_filter import ProfanityFilter
import json
import os
import uuid
#This is confluent.py file!!! just a test for interactive.
def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False

class Object(object):
    pass

print('KOTEK PIJE MLEKO A JA ROBIE SOBIE TEST')
producer = Producer({'bootstrap.servers': os.getenv('KAFKA_HOST', "localhost:9092")})

consumerComment = Consumer({
    'bootstrap.servers': os.getenv('KAFKA_HOST', "localhost:9092"),
    'group.id': 'censor',
    'auto.offset.reset': 'earliest'})
consumerArticle = Consumer({
    'bootstrap.servers': os.getenv('KAFKA_HOST', "localhost:9092"),
    'group.id': 'censor',
    'auto.offset.reset': 'earliest'})

consumerComment.subscribe(['commentSaved'])
consumerArticle.subscribe(['articleSaved'])
pf = ProfanityFilter()

while True:
    msgComment = consumerComment.poll(1.0)
    msgArticle = consumerArticle.poll(1.0)
    if msgArticle is not None and is_valid_uuid(msgArticle.value().decode("utf-8").strip('"')):
        articleCensored = False
        r = requests.get(
            os.getenv('BLOG_HOST', "http://localhost:8001/api") + "/articles/" + msgArticle.value().decode(
                "utf-8").strip('"') + "/")
        response = json.loads(r.text)
        description = response.get("description")

        if description and not pf.is_clean(description):
            articleCensored = True
            description = pf.censor(description)
        title = response.get("title")

        if title and not pf.is_clean(title):
            articleCensored = True
            title = pf.censor(title)

        if articleCensored:
            requests.put(
                os.getenv('BLOG_HOST', "http://localhost:8001/api") + "/articles/ok/" + msgArticle.value().decode(
                    "utf-8").strip('"'),
                data={'title': title,
                      'description': description})
            producer.produce('articleCensored', json.dumps({
                "service": "censor",
                "value": "Article:" + msgArticle.value().decode("utf-8").strip(
                    '"') + " has been censored due to detected profanities."
            }))  # .encode("utf-8")
            print(json.dumps({
                "service": "censor",
                "value": "Article:" + msgArticle.value().decode("utf-8").strip(
                    '"') + " has been censored due to detected profanities."
            }))
        else:
            print(
                requests.post(
                    os.getenv('BLOG_HOST', "http://localhost:8001/api") + '/articles/ok/' + msgArticle.value().decode(
                        "utf-8").strip('"')))
            producer.produce('articleApproved', json.dumps({
                "service": "censor",
                "value": "Article:" + msgArticle.value().decode(
                    "utf-8") + " has been censored due to detected profanities."
            }))  # .encode("utf-8")
    if msgComment is not None and is_valid_uuid(msgArticle.value().decode("utf-8").strip('"')):
        commentCensored = False
        r = requests.get(
            os.getenv('BLOG_HOST', "http://localhost:8001/api") + "/comments/" + msgComment.value().decode(
                "utf-8").strip('"') + "/")

        response = json.loads(r.text)
        value = response.get("value")

        if value and not pf.is_clean(value):
            articleCensored = True
            value = pf.censor(value)

        if articleCensored:
            requests.put(
                os.getenv('BLOG_HOST', "http://localhost:8001/api") + "/comments/ok/" + msgComment.value().decode(
                    "utf-8").strip('"') + "/",
                data={"value": value})
            producer.produce('commentCensored', json.dumps({
                "service": "censor",
                "value": "Comment:" + msgComment.value().decode(
                    "utf-8") + " has been censored due to detected profanities."
            }))  # .encode("utf-8"))

        else:
            requests.post(
                os.getenv('BLOG_HOST', "http://localhost:8001/api") + '/comments/ok/' + msgComment.value().decode(
                    "utf-8").strip('"') + "/")
            producer.produce('commentApproved', json.dumps({
                "service": "censor",
                "value": "Comment:" + msgComment.value().decode("utf-8") + " has been approved!"
            }))  # .encode("utf-8"))

c.close()
