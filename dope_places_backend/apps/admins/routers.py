# apps/admins/routers.py
# Python imports


# Django imports


# Third party apps imports


# Local imports
from .viewsets import AdminViewSet

# Create your routers here.
admins = (
    (r'admin', AdminViewSet),
)
