from django.urls import path
from .views import ViewPayment


urlpatterns = [
    path("view/<int:id>", ViewPayment.as_view())
]