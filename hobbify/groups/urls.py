""" Users URLs """

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import groups as groups_views
from .views import memberships as membership_views

router = DefaultRouter()
router.register(r'groups', groups_views.GroupViewSet, basename='group')
router.register(
    r'groups/(?P<slug_name>[-a-zA-Z0-0_]+)/members',
    membership_views.MembershipViewSet,
    basename='membership'
)

urlpatterns = [
    path('', include(router.urls))
]
