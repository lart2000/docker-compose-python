# apps/items/routers.py
# Python imports


# Django imports


# Third party apps imports


# Local imports
from .viewsets import ItemViewSet, UpdateItems, CreatePhotos


# Create your routers here.
items = (
    (r'item', ItemViewSet),
    (r'update_items', UpdateItems),
    (r'create_photos', CreatePhotos),
)
