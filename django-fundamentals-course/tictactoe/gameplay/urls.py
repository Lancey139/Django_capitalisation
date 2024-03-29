from django.conf.urls import url

from .views import game_detail, make_move, AllGameList

urlpatterns = [
    url(r'detail/(?P<id>\d+)/$',
        game_detail,
        name="gameplay_detail"),
    url(r'make_move/(?P<id>\d+)/$',
        make_move,
        name="gameplay_make_move"
        ),
    url(r'all$', AllGameList.as_view())
    ]