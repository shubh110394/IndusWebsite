from unicodedata import name
from django.urls import path
from .views import Index,Login,SignUp,logout,Cart,Orders,Payment,History,Search,razorInte,success,ViewPdf
from store.middlewares.auth import auth_middleware

urlpatterns = [
    path("",Index.as_view(),name='homepage'),
    path("signup/",SignUp.as_view(),name="signup"),
    path("login/",Login.as_view(),name="login"),
    path("logout/",logout,name="logout"),
    path("razorInte/",razorInte,name="razorInte"),
    path("cart/",Cart.as_view(),name="cart"),
    # path("check-out",CheckOut.as_view(),name="checkout"),
    path("orders",auth_middleware(Orders.as_view()),name="orders"),
    path("payment",Payment.as_view(),name="payment"),
    path("history",History.as_view(),name="history"),
    path("search/",Search.as_view(),name='search'),
    path('success/',success,name='success'),
    path('pdf_view/',ViewPdf.as_view(),name='pdf_view')



]