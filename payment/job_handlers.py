from kafka import KafkaProducer
from django.conf import settings
import multiprocessing
from redis import Redis
from .serializers import TrxJobSerializer, OtpSerializer
import json

from multiprocessing import Process
from modules.services.payment.flutterwave import FlutterwavePaymentProvider
from .models import Transaction, OrderTransaction


TOPIC_ID = getattr(settings, "KAFKA_TOPIC_ID", "5myef1xu-messages")

# SERVERS = getattr(
#     settings, 
#     "KAFKA_SERVERS", 
#     "rocket-01.srvs.cloudkafka.com:9094,rocket-02.srvs.cloudkafka.com:9094,rocket-03.srvs.cloudkafka.com:9094"
#     ).split(",")

PAYMENT_SERVICE_REDIS_PORT = getattr(settings, "PAYMENT_SERVICE_REDIS_PORT")
PAYMENT_SERVICE_REDIS_HOST = getattr(settings, "PAYMENT_SERVICE_REDIS_HOST")
PAYMENT_SERVICE_REDIS_PASSWORD = getattr(settings, "PAYMENT_SERVICE_REDIS_PASSWORD")


# producer: KafkaProducer = KafkaProducer(
#         bootstrap_servers=[
#             *SERVERS
#         ], 
#         security_protocol="SASL_PLAINTEXT",
#         sasl_mechanism="PLAIN",
#         sasl_plain_username="5myef1xu",
#         sasl_plain_password="p9XeeG6glskK4uuN3zWhwInjXHSPhrsE",
#         api_version=(2,5,0),
# )

def create_trx_job():

    redis: Redis = Redis(
        host=PAYMENT_SERVICE_REDIS_HOST, 
        port=PAYMENT_SERVICE_REDIS_PORT,
        password=PAYMENT_SERVICE_REDIS_PASSWORD
    )

    pubsub  = redis.pubsub()

    pubsub.subscribe("payment_request")


    for message in pubsub.listen():

        if message.get("type") == "message":

            trx_job = TrxJobSerializer(data=json.loads(message.get("data")))

            if trx_job.is_valid(raise_exception=True):

                trx = OrderTransaction.objects.create(trxjob_id=trx_job.validated_data["trxjob_id"], amount=trx_job.validated_data["amount"])
                trxjob_id = trx_job.validated_data.pop("trxjob_id")
                trx_finished, response = FlutterwavePaymentProvider().charge_card(
                    card_num=trx_job.validated_data["cardno"], 
                    exp_month=trx_job.validated_data["expirymonth"], 
                    amount=trx_job.validated_data["amount"], 
                    exp_year=trx_job.validated_data["expiryyear"], 
                    cvv=trx_job.validated_data["cvv"], email=trx_job.validated_data["email"], 
                    phone=trx_job.validated_data["phonenumber"], 
                    firstname=trx_job.validated_data["firstname"], 
                    lastname=trx_job.validated_data["lastname"], txn_id=trx.id
                )
                trx.charge_response = response
                trx.save()

                if not trx_finished:
                    # if response["validationRequired"]:
                    redis.publish(f"payment_otp#{trxjob_id}", "")


def authorize_trx_job():

    redis: Redis = Redis(
        host=PAYMENT_SERVICE_REDIS_HOST, 
        port=PAYMENT_SERVICE_REDIS_PORT,
        password=PAYMENT_SERVICE_REDIS_PASSWORD
    )

    pubsub  = redis.pubsub()

    pubsub.subscribe("payment_authorized")

    for message in pubsub.listen():

        if message.get("type") == "message":

            otp_data = OtpSerializer(data=json.loads(message.get("data")))

            if otp_data.is_valid(raise_exception=True):

                trx = OrderTransaction.objects.get(trxjob_id=otp_data.validated_data["trxjob_id"])
                status,response = FlutterwavePaymentProvider().validate_otp(trx.charge_response,otp_data.validated_data["otp"])
                trx.validate_response = response
                response = {**response,"success":False}

                if status == True:
                    response["success"] = True
                else:
                    response["success"] = False

                trx.save()

                redis.publish(f"payment_status#{otp_data.validated_data['trxjob_id']}",json.dumps(response))
            
# Create Transaction job process
create_trx_job_process = Process(target=create_trx_job, args=[], group=None)
create_trx_job_process.daemon = True
create_trx_job_process.start()

# Authorize Transaction job process
authorize_trx_job_process = Process(target=authorize_trx_job, args=[], group=None)
authorize_trx_job_process.daemon = True
authorize_trx_job_process.start()
