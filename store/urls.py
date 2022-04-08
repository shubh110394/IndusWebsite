from django.urls import path
from .views import Index,Login,SignUp,logout,Cart

urlpatterns = [
    path("",Index.as_view(),name='homepage'),
    path("signup/",SignUp.as_view(),name="signup"),
    path("login/",Login.as_view(),name="login"),
    path("logout/",logout,name="logout"),
    path("cart/",Cart.as_view(),name="cart")

]