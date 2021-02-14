from kafka import KafkaConsumer, KafkaProducer, ConsumerRebalanceListener
from django.conf import settings
import multiprocessing


TOPIC_ID = getattr(settings, "KAFKA_TOPIC_ID", "5myef1xu-messages")

SERVERS = getattr(
    settings, 
    "KAFKA_SERVERS", 
    "rocket-01.srvs.cloudkafka.com:9094,rocket-02.srvs.cloudkafka.com:9094,rocket-03.srvs.cloudkafka.com:9094"
    ).split(",")



def startConsumers():

    print("Initializing Consumers:")
    consumer: KafkaConsumer = KafkaConsumer(
        bootstrap_servers=[
            *SERVERS
        ], 
        security_protocol="SASL_PLAINTEXT",
        sasl_mechanism="PLAIN",
        sasl_plain_username="5myef1xu",
        sasl_plain_password="p9XeeG6glskK4uuN3zWhwInjXHSPhrsE",
        api_version=(2,5,0),

    )

    for message in consumer:
        print(message)
    print("finished")

try:
    proc = multiprocessing.Process(target=startConsumers, args=[])
    proc.daemon = True
    proc.start()
except Exception as e:
    print(str(e))
