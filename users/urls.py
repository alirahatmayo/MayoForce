from . import views
from django.conf import settings # new
from django.urls import path,  include
from django.conf.urls import url

from django.conf.urls.static import static # new
from posts.views import user_posts
#
# urlpatterns = [
#     path('signup/', views.SignUp.as_view(), name='signup'),
# ]
from django.conf.urls.static import static # new


urlpatterns = [
    # path('info/', views.info, name='info'),
    # path('profile/', views.profile, name='profile'),
    # path('profile/edit/', views.edit_profile, name='edit_profile'),
    #
    # path('education/', views.education, name='education'),
    # # path('education/add/', views.add_education, name='add_education'),
    # path('education/edit/<int:pk>', views.edit_education, name='edit_education'),
    # path('education/delete/<int:pk>', views.delete_education, name='delete_education'),
    #
    # path('family/', views.family, name='family'),
    # # path('family/add/', views.add_family, name='add_family'),
    # path('family/edit/<int:pk>', views.edit_family, name='edit_family'),
    # path('family/delete/<int:pk>', views.delete_family, name='delete_family'),
    #
    # path('testing', views.testing, name='testing'),

    path('', views.home, name= 'home'),
    path('timeline/<int:pk>', views.timeline, name='timeline'),
    path('basic/edit/', views.edit_basic_info, name='edit_basic'),
    path('education/add/', views.edu_work, name='add_edu_work'),
    path('family/add/', views.add_family, name='add_family'),
    path('about/<int:pk>', views.about, name='about'),
    path('followers/<int:pk>', views.get_followers, name='followers'),
    path('following/<int:pk>', views.get_following, name='following'),
    path('follow-friend/<int:pk>', views.follow, name='follow'),
    path('unfollow-friend/<int:pk>', views.unfollow, name='unfollow'),

    # url(r'^connect/(?P<operation>.+)/(?P<pk>\d+)/$', views.change_connection, name='change_connection'),



]

if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)