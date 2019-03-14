# apps/orders/routers.py
# Python imports


# Django imports


# Third party apps imports


# Local imports
from .viewsets import OrderViewSet, CommentViewSet


# Create your routers here.
orders = (
    (r'order', OrderViewSet),
    (r'comment', CommentViewSet),
)
