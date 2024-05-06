import json
import os

import requests
from kafka import KafkaProducer, KafkaConsumer
from profanity_filter import ProfanityFilter

producer = KafkaProducer(bootstrap_servers=os.getenv('KAFKA_HOST', "localhost:9092"),
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))  # os.environ['KAFKA_BOOTSTRAP']
consumer = KafkaConsumer('articleSaved', group_id='censor', bootstrap_servers=os.getenv('KAFKA_HOST', "localhost:9092"),
                         auto_offset_reset='earliest')
pf = ProfanityFilter()

for msg in consumer:
    articleCensored = False
    r = requests.get(
        os.getenv('BLOG_HOST', "http://localhost:8001/api") + "/articles/" + msg.value.decode("utf-8").strip('"') + "/")

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
            os.getenv('BLOG_HOST', "http://localhost:8001/api") + "/articles/ok/" + msg.value.decode("utf-8").strip(
                '"'),
            data={'title': title,
                  'description': description})
        producer.send('articleCensored', {
            "service": "censor",
            "value": "Article:" + msg.value.decode("utf-8").strip(
                '"') + " has been censored due to detected profanities."
        })

    else:
        requests.post(
            os.getenv('BLOG_HOST', "http://localhost:8001/api") + '/articles/ok/' + msg.value.decode("utf-8").strip(
                '"'))
        producer.send('articleApproved', {
            "service": "censor",
            "value": "Article:" + msg.value.decode("utf-8") + " has been censored due to detected profanities."
        })
