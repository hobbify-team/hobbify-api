""" Habits URLs """

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import habits as habits_views

router = DefaultRouter()
router.register(
    r'(?P<username>[-a-zA-Z0-0_]+)/habits',
    habits_views.HabitViewSet,
    basename='habit'
)

urlpatterns = [
    path('', include(router.urls))
]
