from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from .views import ScenarioViewSet, ScenarioAreaViewSet, ScenarioTypeViewSet, CommentViewSet, RatingoViewSet, TestCaseViewSet, UserViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('scenarios', ScenarioViewSet)
router.register('cases', TestCaseViewSet)
router.register('ratings', RatingoViewSet)
router.register('comments', CommentViewSet)
router.register('areas', ScenarioAreaViewSet)
router.register('types', ScenarioTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
