from django.contrib import messages
from invitations.adapters import get_invitations_adapter
from invitations.app_settings import app_settings as invitations_settings
from invitations.signals import invite_accepted
from xlibrary.viewsets import ModelViewset as xViewSet
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import (action,api_view,
                                       permission_classes)
from rest_framework.permissions import AllowAny, IsAuthenticated
from accountinginfo.models import Ledger
from rest_framework.response import Response
from .models import GuestInvitation as InvitationModel, GroupOptions, User
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
# from .serializers import InvitationReadSerializer,InvitationBulkWriteSerializer,InvitationWriteSerializer,UserSerializer, GroupSerializer, PermissionSerializer,ContenttypeSerializer,GroupOptionsSerializer,CUserSerializer, CGroupSerializer,CGroupOptionsSerializer
from .serializers import InvitationReadSerializer,InvitationBulkWriteSerializer,InvitationWriteSerializer,UserSerializer, GroupSerializer, PermissionSerializer,ContenttypeSerializer,GroupOptionsSerializer,CUserSerializer, CGroupSerializer
from rest_auth.views import LoginView as RestAuthLoginView
from django.conf import settings

def getVisiblePermissions():
    ct = ContentType.objects.all()
    myNameList = []
    for c in ct:
        class_name = c.model_class()
        if hasattr(class_name, "xtrmMeta"):
            myNameList.append(class_name.__name__.lower())
    return myNameList


def jwt_response_payload_handler(token, user=None, request=None):
    myNameList = getVisiblePermissions()
    perms = user.groups.first()
    rtn = []
    if perms:
        for perm in perms.permissions.all().filter(content_type__model__in=myNameList):
            pm = {
                "name": perm.name,
                "codename": perm.codename,
                "app_label": perm.content_type.app_label,
                "model": perm.content_type.model
            }
            rtn.append(pm)

    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data,
        'permissions': rtn
    }


class LoginView(RestAuthLoginView):
    """
    Overriden LoginView

    get_response serializes the response according to the default serializer (as you already know)
    which in turn, uses the default UserDetailsSeriazlizer (which we don't want)

    What we can do is use our custom jwt_response_payload_handler as our serializer and return in directly
    in the response
    """

    def get_response(self):
        serializers_class = self.get_response_serializer()

        if getattr(settings, 'REST_USE_JWT', False):

            # Use jwt_response_payload_handler since we already have the token, user (optional) and the request (optional)
            data = jwt_response_payload_handler(
                self.token, self.user, self.request)

            return Response(data, status=status.HTTP_200_OK)
        else:
            serializer = serializers_class(instance=self.token, context={
                                           'resquest': self.request})

            return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(xViewSet):
    http_method_names = [m for m in viewsets.ModelViewSet.http_method_names if m not in [m for m in viewsets.ModelViewSet.http_method_names if m not in ['get']]]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    reporttitle = 'Users'
	#orientation='landscape'
    options = {'canAdd': 1, 'canPrint': 1}
    filters = [
        {'title': 'User Name', 'name': 'filter{username}', 'url': 'v1/rights/users/'},
        {'title': 'Email', 'name': 'filter{email}'},
        {"title": "Group", "name": "filter{groups.name}", "url": "v1/rights/groups/"}
    ]
    columns = [
        {'title': 'Id', 'name': 'id', 'type': 'numeric',
            'searchable': False, 'sortable': False, 'visible': False},
        {'title': 'User Name', 'name': 'username', 'width': '20%'},
        {'title': 'First Name', 'name': 'first_name', 'width': '20%'},
        {'title': 'Last Name', 'name': 'last_name', 'width': '20%'},
        {'title': 'Email', 'name': 'email'}
    ]


class GroupViewSet(xViewSet):
    http_method_names = [m for m in viewsets.ModelViewSet.http_method_names if m not in [m for m in viewsets.ModelViewSet.http_method_names if m not in ['get']]]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    reporttitle = 'Groups'
    #orientation='landscape'
    options = {'canAdd': 1, 'canPrint': 1}
    filters = [
        {'title': 'name', 'name': 'filter{name}', 'url': 'v1/rights/groups/'}
    ]
    columns = [
        {'title': 'Id', 'name': 'id', 'alignment': 'right', 'type': 'numeric',
            'searchable': False, 'sortable': False, 'visible': False},
        {'title': 'Name', 'name': 'name'}
    ]


class PermissionViewSet(xViewSet):
    http_method_names = [m for m in viewsets.ModelViewSet.http_method_names if m not in [m for m in viewsets.ModelViewSet.http_method_names if m not in ['get']]]
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    reporttitle = 'Permissions'
    #orientation='landscape'
    options = {'canAdd': 1, 'canPrint': 1}
    filters = [
        {'title': 'Name', 'name': 'filter{name}', 'url': 'v1/rights/permissions/'}
    ]
    columns = [
        {'title': 'Id', 'name': 'id', 'alignment': 'right', 'type': 'numeric',
            'searchable': False, 'sortable': False, 'visible': False},
        {'title': 'Name', 'name': 'name'},
        {'title': 'Code Name', 'name': 'codename'}
    ]

    def get_queryset(self):
        myNameList = getVisiblePermissions()
        return Permission.objects.all().filter(content_type__model__in=myNameList)


class ContenttypeViewSet(xViewSet):
    http_method_names = [m for m in viewsets.ModelViewSet.http_method_names if m not in [m for m in viewsets.ModelViewSet.http_method_names if m not in ['get']]]
    queryset = ContentType.objects.all()
    serializer_class = ContenttypeSerializer
    reporttitle = 'Content Types'
    #orientation='landscape'
    options = {'canAdd': 1, 'canPrint': 1}
    filters = [
        {'title': 'App Label', 'name': 'filter{app_label}',
            'url': 'v1/rights/contenttypes/'}
    ]
    columns = [
        {'title': 'Id', 'name': 'id', 'alignment': 'right', 'type': 'numeric',
            'searchable': False, 'sortable': False, 'visible': False},
        {'title': 'App Label', 'name': 'app_label'},
        {'title': 'Model', 'name': 'model'}
    ]


class GroupOptionsViewSet(xViewSet):
    http_method_names = [m for m in viewsets.ModelViewSet.http_method_names if m not in [m for m in viewsets.ModelViewSet.http_method_names if m not in ['get']]]
    queryset = GroupOptions.objects.all()
    serializer_class = GroupOptionsSerializer


class CUserViewSet(viewsets.ModelViewSet):
    http_method_names = [m for m in viewsets.ModelViewSet.http_method_names if m not in ['get']]
    queryset = User.objects.all()
    serializer_class = CUserSerializer

    # def get_permissions(self):
    #     permission_classes = [IsAdminUser]
    #     return [permission() for permission in permission_classes]


class CGroupViewSet(viewsets.ModelViewSet):
    http_method_names = ['post', 'put', 'patch']
    queryset = Group.objects.all()
    serializer_class = CGroupSerializer


# class CGroupOptionsViewSet(viewsets.ModelViewSet):
#     queryset = GroupOptions.objects.all()
#     serializer_class = CGroupOptionsSerializer

class InvitationViewSet(viewsets.ModelViewSet):
    queryset = InvitationModel.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return InvitationReadSerializer
        elif self.action == 'send_multiple':
            return InvitationBulkWriteSerializer
        return InvitationWriteSerializer

    def _prepare_and_send(self, invitation, request):
        invitation.inviter = request.user
        invitation.save()
        invitation.send_invitation(request)

    # @detail_route(
    #     methods=['post'], permission_classes=[IsAuthenticated],
    #     url_path=SEND_URL
    # )
    # def send(self, request, pk=None):
    #     invitation = self.get_object()
    #     self._prepare_and_send(invitation, request)
    #     content = {'detail': 'Invite sent'}
    #     return Response(content, status=status.HTTP_200_OK)

    # @list_route(
    #     methods=['post'], permission_classes=[IsAuthenticated],
    #     url_path=CREATE_AND_SEND_URL
    # )
    @action(
        methods=['post'],detail=False
    )
    def send(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        authorentity = Ledger.objects.get(pk=serializer.data['authorentity'])
        invitation = InvitationModel.create(email=email,authorentity=authorentity, inviter=request.user)
        self._prepare_and_send(invitation, request)
        content = {'detail': 'Invite sent'}
        return Response(content, status=status.HTTP_200_OK)

    # @list_route(
    #     methods=['post'], permission_classes=[IsAuthenticated],
    #     url_path=SEND_MULTIPLE_URL
    # )
    @action(
        methods=['post'], detail=False
    )
    def sendmultiple(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        inviter = request.user
        authorentity = Ledger.objects.get(pk=serializer.data['authorentity'])
        for email in serializer.data['email']:
            invitation = InvitationModel.create(
                email=email, authorentity=authorentity, inviter=inviter)
            self._prepare_and_send(invitation, request)
        content = {'detail': 'Invite(s) sent'}
        return Response(content, status=status.HTTP_200_OK)


@api_view(('POST', 'GET'))
@permission_classes((AllowAny,))
def accept_invitation(request, key):
    def get_object():
        try:
            return InvitationModel.objects.get(key=key.lower())
        except InvitationModel.DoesNotExist:
            return None

    invitation = get_object()

    login_data = {
        # 'LOGIN_REDIRECT': invitations_settings.LOGIN_REDIRECT
    }
    signup_data = {
        # 'SIGNUP_REDIRECT': invitations_settings.SIGNUP_REDIRECT
    }

    if invitations_settings.GONE_ON_ACCEPT_ERROR and \
        (not invitation or
         (invitation and (invitation.accepted or
                          invitation.key_expired()))):
        return Response(status=status.HTTP_410_GONE)

    if not invitation:
        get_invitations_adapter().add_message(
            request,
            messages.ERROR,
            'invitations/messages/invite_invalid.txt'
        )
        return Response(login_data, status=status.HTTP_200_OK)

    if invitation.accepted:
        get_invitations_adapter().add_message(
            request,
            messages.ERROR,
            'invitations/messages/invite_already_accepted.txt',
            {
                'email': invitation.email
            }
        )
        return Response(login_data, status=status.HTTP_200_OK)

    if invitation.key_expired():
        get_invitations_adapter().add_message(
            request,
            messages.ERROR,
            'invitations/messages/invite_expired.txt',
            {
                'email': invitation.email
            }
        )
        return Response(signup_data, status=status.HTTP_200_OK)

    if not invitations_settings.ACCEPT_INVITE_AFTER_SIGNUP:
        invitation.accepted = True
        invitation.save()
        invite_accepted.send(sender=None, email=invitation.email)
        get_invitations_adapter().add_message(
            request,
            messages.SUCCESS,
            'invitations/messages/invite_accepted.txt',
            {
                'email': invitation.email,
                'author':invitation.authorentity.pk
            }
        )
        signup_data.update(
            {
                'account_verified_email': invitation.email,
                'account_verified_author': invitation.authorentity.pk
            }
        )
    return Response(
        signup_data,
        status=status.HTTP_200_OK
    )
