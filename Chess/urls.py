from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration$', views.registration),
    url(r'^create_user$', views.createuser),
    url(r'^login$', views.login_page),
    url(r'^log$', views.log),
    url(r'^logout$', views.logout_view),
    url(r'^profile$', views.profile_view),
    url(r'^game$', views.board),

]
