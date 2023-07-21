from django.urls import path, re_path


from .views import login_page, register_page, activate,accountSettings
from django.contrib.auth.views import LogoutView

app_name = "accounts"




urlpatterns = [
    path('account/', accountSettings, name="account"),
    path('login/', login_page, name="login"),
    path('register/', register_page, name="register"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('activate/<uidb64>/<token>', activate, name='activate'),





]