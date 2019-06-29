from . import views
from posts.views import *
from django.conf import settings # new
from django.urls import path,  include
from django.conf.urls import url


urlpatterns = [
        path('comment/<int:pk>', views.add_comment_to_post, name='post_comment'),
        path('post/', views.add_post , name = 'add_post'),
        path('post/<int:pk>', views.get_post, name='get_post')

]
