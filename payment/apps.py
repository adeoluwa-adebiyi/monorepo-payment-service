from django.apps import AppConfig


class PaymentConfig(AppConfig):
    name = 'payment'

    def ready(self):
        import payment.job_handlers
