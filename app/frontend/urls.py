from django.urls import path
from frontend.views import RegisterView, SuccessView

urlpatterns = [
    path('', RegisterView.as_view(), name='index'),
    path("success", SuccessView.as_view(), name='success'),
]