""" Habits URLs """

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import habits as habits_views
from .views import recurrences as recurrences_views

router = DefaultRouter()
router.register(
    r'(?P<username>[-a-zA-Z0-0_]+)/habits',
    habits_views.HabitViewSet,
    basename='habit'
)
router.register(
    r'(?P<username>[-a-zA-Z0-0_]+)/recurrence',
    recurrences_views.RecurrencesViewSet,
    basename='recurrences'
)

urlpatterns = [
    path('', include(router.urls))
]
