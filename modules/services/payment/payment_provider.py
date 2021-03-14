class PaymentProvider(object):

    def charge_card(self, card_num:int, exp_month:str, amount:float, exp_year:str, 
                        cvv:str, email:str, phone:str, firstname:str, 
                        lastname: str, txn_id:str, ip:str="") -> tuple :
        pass

    def validate_otp(self, flutterwaveRef:str, otp:str) -> tuple:
        pass

