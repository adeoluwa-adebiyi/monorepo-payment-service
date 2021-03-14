from rest_framework import serializers


class TrxJobSerializer(serializers.Serializer):
    cardno = serializers.CharField(required=True)
    cvv = serializers.CharField(required=True)
    expirymonth = serializers.CharField(required=True)
    expiryyear = serializers.CharField(required=True)
    amount = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    phonenumber = serializers.CharField(required=True)
    firstname = serializers.CharField(required=True)
    lastname = serializers.CharField(required=True)
    trxjob_id = serializers.IntegerField(required=True)


class OtpSerializer(serializers.Serializer):

    otp = serializers.CharField(required=True)
    trxjob_id = serializers.IntegerField(required=True)
