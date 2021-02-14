import asyncio
from rave_python import Rave, RaveExceptions, Misc
from django.conf import settings
from modules.services.payment.payment_provider import PaymentProvider


FL_PUBLIC = getattr(settings, "FLUTTER_WAVE_API_KEY", None)

FL_SECRET = getattr(settings, "FLUTTER_WAVE_API_SECRET_KEY", None)

class FlutterwavePaymentProvider(PaymentProvider):

    def __init__(self):
        self.rave = Rave(FL_PUBLIC, FL_SECRET, production=False, usingEnv=False)


    def charge_card(self, card_num:int, exp_month:str, amount:float, exp_year:str, 
                        cvv:str, email:str, phone:str, firstname:str, 
                        lastname: str, txn_id:str, ip:str = "") -> tuple :
        payload = {
            "cardno": card_num,
            "cvv": cvv,
            "expirymonth": exp_month,
            "expiryyear": exp_year,
            "amount": amount,
            "email": email,
            "phonenumber": phone,
            "firstname": firstname ,
            "lastname": lastname,
            "IP": ip,
            "txRef": txn_id
        }

        try:
            res = self.rave.Card.charge(cardDetails=payload)

            if res["suggestedAuth"]:
                arg = Misc.getTypeOfArgsRequired(res["suggestedAuth"])

                if arg == "pin":
                    Misc.updatePayload(res["suggestedAuth"], payload, pin="3310")
                if arg == "address":
                    Misc.updatePayload(res["suggestedAuth"], payload, address= {"billingzip": "07205", "billingcity": "Hillside", "billingaddress": "470 Mundet PI", "billingstate": "NJ", "billingcountry": "US"})
                
                res = self.rave.Card.charge(payload)

            res = self.rave.Card.verify(res["txRef"])
            print(res)
            print(res["transactionComplete"])
            return res["transactionComplete"], res

        except RaveExceptions.CardChargeError as e:
            print(e.err["errMsg"])
            print(e.err["flwRef"])

        except RaveExceptions.TransactionValidationError as e:
            print(e.err)
            print(e.err["flwRef"])

        except RaveExceptions.TransactionVerificationError as e:
            print(e.err["errMsg"])
            print(e.err["txRef"])

    # if res["validationRequired"]:
    def validate_otp(self, response:str, otp:str) -> tuple:
        chargeStatus = self.rave.Card.validate(response["flwRef"], otp)
        print(chargeStatus["error"])
        return chargeStatus["error"]==False,chargeStatus
        
if __name__ == "__main__":
    provider = FlutterwavePaymentProvider()
    provider.charge_card(
        card_num="5531886652142950",
        exp_month="09",
        amount="40000",
        exp_year="32",
        cvv="564",
        email="akuybe@gmail.com",
        phone="+2348162814641",
        firstname="Phil",
        lastname="Jacob",
        txn_id="7836",
    )