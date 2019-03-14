# apps/proxies/routers.py
# Python imports


# Django imports


# Third party apps imports


# Local imports
from .viewsets import ProxyViewSet, ProxySocialUserViewSet


# Create your routers here.
proxies = (
    (r'proxy', ProxyViewSet),
    (r'socialproxy', ProxySocialUserViewSet)
)
