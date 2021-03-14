from django.shortcuts import render
from django.views.generic import View
from django.http.response import HttpResponse

# Create your views here.


class ViewPayment(View):

    def get(self, request, id:int):
        return HttpResponse("")