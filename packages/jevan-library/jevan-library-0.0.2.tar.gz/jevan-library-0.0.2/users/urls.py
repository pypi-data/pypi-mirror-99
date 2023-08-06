# from rest_framework import routers
from .views import InvitationViewSet, accept_invitation, UserViewSet, GroupViewSet, PermissionViewSet, ContenttypeViewSet, GroupOptionsViewSet, CUserViewSet, CGroupViewSet
from django.conf.urls import include, url
from xtrm_drest.routers import DynamicRouter

# router = routers.SimpleRouter()
router = DynamicRouter()
router.register('users', UserViewSet)
router.register('edit/user', CUserViewSet)
router.register('groups', GroupViewSet)
router.register('edit/group', CGroupViewSet)
router.register('permissions', PermissionViewSet)
router.register('contenttypes', ContenttypeViewSet)
router.register('groupoptions', GroupOptionsViewSet)
router.register('invitations', InvitationViewSet)
invitations_patterns = (
    [
        url(
            r'^{0}/{1}/(?P<key>\w+)/?$'.format(
                'invitations','accept-invite'
            ),
            accept_invitation,
            name='accept-invite'
        ),
    ],
    'invitations'
)

urlpatterns = router.urls + [
    url(r'^', include(invitations_patterns)),
]
