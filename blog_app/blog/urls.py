
from django.conf.urls import url
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers

from blog import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'articles', views.ArticleViewSet)
router.register(r'article-ratings', views.ArticleRatingViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'comment-ratings', views.ArticleRatingViewSet)
router.register(r'images', views.ImageViewSet)

urlpatterns = [
    path('articles/ok/<uuid:id>', views.censor_article),
    path('comments/ok/<uuid:id>', views.censor_comment),
    url(r'^', include(router.urls)),

]