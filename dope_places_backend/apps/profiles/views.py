# apps/profiles/views.py
# Python imports


# Django imports
from django.conf import settings


# Third party apps imports
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from requests.exceptions import HTTPError

from social_django.utils import psa


# Local imports
from .serializers import ProfileSerializer


# Create your viewsets here.
class ProfileAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        serializer = ProfileSerializer(request.user)
        if serializer.data['role'] == 'Not profile asigned':
            return Response(
                serializer.data, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.data)


class SocialSerializer(serializers.Serializer):
    access_token = serializers.CharField(
        allow_blank=False,
        trim_whitespace=True,
    )


@api_view(http_method_names=['POST'])
@permission_classes([AllowAny])
@psa()
def exchange_token(request, backend):
    serializer = SocialSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        try:
            nfe = settings.NON_FIELD_ERRORS_KEY
        except AttributeError:
            nfe = 'non_field_errors'

        try:
            user = request.backend.do_auth(serializer.validated_data['access_token'])
        except HTTPError as e:
            return Response(
                {'errors': {
                        'token': 'Invalid token',
                        'detail': str(e),
                     }},
                status=status.HTTP_400_BAD_REQUEST
            )

        if user:
            if user.is_active:
                profile = False

                if hasattr(user, 'customer') or hasattr(user, 'proxy'):
                    profile = True

                token, _ = Token.objects.get_or_create(user=user)
                return Response({
                    "token": token.key,
                    "user_id": user.pk,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "profile": profile
                    })

            else:
                return Response(
                    {'errors': {nfe: 'This user account is inactive'}},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {'errors': {nfe: 'Authentication Failed'}},
                status=status.HTTP_400_BAD_REQUEST,
            )
