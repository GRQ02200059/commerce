from django.urls import path

from . import views

urlpatterns = [

    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories",views.categories,name="categories"),
    path("create_list",views.create_list,name="create_list"),
    path("watchlist/<user>",views.watchlist,name="watchlist"),
    path("after_create",views.after_create,name="after_create"),
    path("listings/<name>",views.detail,name="detail"),
    path("categories/<category>",views.the_category,name="category"),
    path("comments",views.after_comments,name="comments"),
    path("bids",views.after_bids,name="bids"),
    path("wl",views.wl,name="wl"),
    path("close",views.close,name="close"),
path('data_fresh/', views.data_fresh, name="data_fresh")
]
