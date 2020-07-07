""" Recurrences URLs """

# Django
from django.urls import path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import recurrences as recurrences_views

router = DefaultRouter()

urlpatterns = [
    path('recurrences/<int:id>/', recurrences_views.list_recurrences),
    path('recurrences/<int:id>/today/', recurrences_views.retrieve_today_recurrence),
    path('recurrences/<int:id>/list/', recurrences_views.list_habit_recurrences),
    path('recurrences/<int:id>/today/<int:r_id>/', recurrences_views.retrieve_today_recurrence_by_id),
    path('recurrences/<int:id>/<int:r_id>/', recurrences_views.update_recurrent_instance),
]
