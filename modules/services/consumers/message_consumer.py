from kafka import KafkaProducer, KafkaConsumer
from typing import Callable
from multiprocessing import Process

class IMessageConsumer:

    def run() -> None:
        pass


class KafkaMessageConsumer(IMessageConsumer):

    def __init__(self, kafkaClient, job_handler=None):
        super().__init__()
        self.kafkaClient = kafkaClient
        self.job_handler = job_handler

    def run(self) -> None:
        for message in self.kafkaClient.poll():
            if self.job_handler is not None:
                process = Process(target=self.job_handler, args=[message])
                process.run()
            else:
                raise Exception("job_handler cannot be None")

