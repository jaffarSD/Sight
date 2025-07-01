from django import views
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from seen.views import RegisterView, ContactCreateView, VerifyEmailView,LoginView,LogoutView,UserProfileView, index




urlpatterns = [

   path('', index, name='sgbd'),
   
   path("register/", RegisterView.as_view(), name="register"),
   path("verify_email/", VerifyEmailView.as_view(), name="verify-email"),
   path("login/", LoginView.as_view(), name="login"),
   path("logout/", LogoutView.as_view(), name="logout"),
   path("profile/", UserProfileView.as_view(), name="profile"),
   path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
   path('api/Contact_us/', ContactCreateView.as_view(), name='Contact_us'),

]