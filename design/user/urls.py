from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('user',views.authorized, name="user"),
    path('get_user',views.UserView.as_view(), name="get_user"),
    path('get_cus',views.CusView.as_view(),name="get_cus"),
    path('get_cus/myfollow',views.CusFollow.as_view(),name="cusfollow"),
    path('get_cus/newcus',views.NewCus.as_view(),name="newcus"),
    path('get_cus/waitcus',views.WaitCus.as_view(),name="waitcus"),
]