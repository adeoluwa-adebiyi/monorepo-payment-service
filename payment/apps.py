from django.apps import AppConfig
import os
import time


class PaymentConfig(AppConfig):
    name = 'payment'

    def ready(self):
        from .job_handlers import start_services
        start_services()
