# apps/customers/viewsets.py
# Python imports


# Django imports
from django.contrib.auth.models import User

# Third party apps imports
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response


# Local imports
from .models import Customer
from .serializers import CustomerSerializer
from apps.countries.models import Country


# Create your viewsets here.
class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny, ]
        return [permission() for permission in self.permission_classes]


class CustomerSocialUserViewSet(ModelViewSet):
    def create(self, request, *args, **validated_data):
        user_id = request.data.get('user_id')
        user = User.objects.get(pk=user_id)
        if not hasattr(user, "customer") and not hasattr(user, "proxy") :
            country = Country.objects.get(id=request.data.get('country'))
            paypal_email = request.data.get("paypal_email")

            try:
                customer = Customer.objects.create(user=user, country=country, paypal_email=paypal_email)
                serializer = CustomerSerializer(customer)
                return Response({"customer": serializer.data})
            except Exception:
                return Response({"error": "Incorrect customer fields"})

        else:
            return Response({"error:": "This user already has a profile"})
