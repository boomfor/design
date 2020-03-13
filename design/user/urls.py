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
    path('get_cus/infochange',views.CusInfoChange.as_view(),name="infochange"),
    path('get_cus/allcus',views.AllCus.as_view(),name="allcus"),
    path('get_cus/mysign',views.SignCus.as_view(),name="mysign"),
    path('get_cus/search',views.SearchCus.as_view(),name="search"),
    path('get_follow',views.FollowView.as_view(),name="get_follow"),
    path('get_warn',views.WarnView.as_view(),name="get_warn"),
    path('sign',views.SignView.as_view(),name="sign")
]