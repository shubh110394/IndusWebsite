from django.urls import path
from .views import Index,Login,SignUp

urlpatterns = [
    path("",Index.as_view(),name='homepage'),
    path("signup/",SignUp.as_view(),name="signup"),
    path("login/",Login.as_view(),name="login"),
]