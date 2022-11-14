from django.urls import path
from . import apiREST

urlpatterns = [
    path('ping/', apiREST.Ping.as_view()),
    path('pingAuth/', apiREST.PingAuth.as_view()),
    path('account/', apiREST.get_account_list),
]