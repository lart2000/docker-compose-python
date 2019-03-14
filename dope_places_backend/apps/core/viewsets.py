# apps/core/viewsets.py
# Python imports
import time
import json

# Django imports
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.encoding import force_text, force_bytes
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

# Third party apps imports


# Local imports
from apps.customers.models import PasswordToken


# Create your viewsets here.
@csrf_exempt
def change_password(request, token):
    try:
        token_decrypt = urlsafe_base64_decode(token).decode()

        if not len(token_decrypt.split(':')) == 2:
            return JsonResponse({'result': False, 'msg': 'The link is invalid'})

        email, timestamp = token_decrypt.split(':')

        # valid email
        if not User.objects.filter(username=email).exists():
            return JsonResponse({'result': False, 'msg': 'Error: The email not exists.'})

        user = User.objects.get(username=email)

        # valid if token has expired
        if not PasswordToken.objects.filter(user=user).exists():
            return JsonResponse({'result': False, 'msg': 'Error: The link has expired'})

        password_token = PasswordToken.objects.get(user=user)

        if not password_token.token_password == token:
            return JsonResponse({'result': False, 'msg': 'Error: The token is invalid.'})

        # valid creation time of token
        if time.time() - float(timestamp) > 900000:
            return JsonResponse({'result': False, 'msg': 'Error: The link has expired.'})

        if request.method == 'POST':
            password = json.loads(request.body.decode('utf-8'))['password']

            # update user
            user = User.objects.get(username=email)
            user.set_password(password)
            user.save()

            return JsonResponse({'result': True, 'msg': 'Success: Your password has been changed'})
        else:
            return JsonResponse({'result': True, 'msg': 'Success: Token is valid.'})

    except Exception as exp:
        return JsonResponse({'result': False, 'msg': 'Internal Error'})


def get_request_change_password_token(request):
    try:
        # create token
        email = request.GET.get('email')
        timestamp = time.time()
        token = urlsafe_base64_encode(force_bytes("%s:%s" %(email, timestamp))).decode()

        # valid email
        if not User.objects.filter(username=email).exists():
            return JsonResponse({'result': False, 'msg': 'The email not exists.'})

        # update extra details with new token
        user = User.objects.get(username=email)

        password_token, created = PasswordToken.objects.get_or_create(user=user)

        password_token.token_password = token
        password_token.save()

        # send email with token
        subject = "change password"
        url = settings.WEB_HOSTNAME + '/reset_password/' + token
        content = "Change your password in %s" % url
        send_mail(
            subject,
            content,
            'from@example.com',
            [user.username],
            fail_silently=True,
        )

        return JsonResponse(
            {
                'result': True,
                'token': token,
                'msg': 'We send a email with your token to reset password.'
            }
        )
    except Exception as exp:
        return JsonResponse({'result': False, 'msg': 'Internal Error'})
