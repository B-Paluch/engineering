import json
import os
import requests
from kafka import KafkaProducer, KafkaConsumer
from profanity_filter import ProfanityFilter

producer = KafkaProducer(bootstrap_servers=os.getenv('KAFKA_HOST', "localhost:9092"),
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))
consumer = KafkaConsumer('commentSaved', group_id='censor', bootstrap_servers=os.getenv('KAFKA_HOST', "localhost:9092"),
                         auto_offset_reset='earliest')
pf = ProfanityFilter()

for msg in consumer:
    commentCensored = False
    r = requests.get(
        os.getenv('BLOG_HOST', "http://localhost:8001/api") + "/comments/" + msg.value.decode("utf-8").strip('"') + "/")

    response = json.loads(r.text)
    value = response.get("value")

    if value and not pf.is_clean(value):
        articleCensored = True
        value = pf.censor(value)

    if articleCensored:
        requests.put(
            os.getenv('BLOG_HOST', "http://localhost:8001/api") + "/comments/ok/" + msg.value.decode("utf-8").strip(
                '"') + "/", data={"value": value})
        producer.send('commentCensored', {
            "service": "censor",
            "value": "Comment:" + msg.value.decode("utf-8") + " has been censored due to detected profanities."
        })

    else:
        requests.post(
            os.getenv('BLOG_HOST', "http://localhost:8001/api") + '/comments/ok/' + msg.value.decode("utf-8").strip(
                '"') + "/")
        producer.send('commentApproved', {
            "service": "censor",
            "value": "Comment:" + msg.value.decode("utf-8") + " has been approved!"
        })
