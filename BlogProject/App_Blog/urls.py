from django.urls import path
from . import views
app_name = 'App_Blog'
urlpatterns = [
    path('',views.BlogList.as_view(), name='BlogList'),
    path('write/',views.CreateBlog.as_view(),name='create_blog'),
    path('details/<int:pk>/',views.blog_details,name='details_blog'),
    path('liked/<int:pk>/',views.liked,name='like_post'),
    path('like/<int:pk>/',views.unLiked,name='unlike_post'),
    path('my_blog/',views.MyBlog.as_view(),name='my_blog'),
    path('edit_blog/<int:pk>',views.UpdateBlog.as_view(),name='edit_blog'),

    
]
