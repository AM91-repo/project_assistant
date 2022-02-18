from django.urls import path

import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.login, name='login'),
    path('logout/', authapp.logout, name='logout'),
    path('user/register/', authapp.register, name='register'),
    path('user/edit/', authapp.edit, name='edit'),
    path('user/friends/', authapp.list_friends, name='friends'),
    path('user/friandrequest/', authapp.friend_request, name='friendrequest'),
    path('user/request/', authapp.FriendRequestList.as_view(), name='request'),
    path('user/request/delete/<int:pk>/', authapp.FriendRequestDelete.as_view(),
         name='request_delete'),
    path('user/request/accepte/<int:pk>/',
         authapp.accept_friend_request, name='request_accepte')
    # path('user/friandrequest',
    #      authapp.FriendRequestCreate.as_view(), name='friendrequest'),
    # path('user/verify/<str:email>/<str:activate_code>/',
    #      authapp.verify, name='verify'),
]
