# apps/countries/viewsets.py
# Python imports


# Django imports


# Third party apps imports
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly


# Local imports
from .models import Country
from .serializers import CountrySerializer


# Create your viewsets here.
class CountryViewSet(ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
