# apps/items/viewsets.py
# Python imports


# Django imports

# Third party apps imports
from rest_framework import viewsets, status
from rest_framework.response import Response


# Local imports
from .models import Item, Photo
from .serializers import ItemSerializer, PhotoSerializer
from apps.orders.models import Order
from apps.orders.serializers import OrderSerializer


# Create your viewsets here.
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class UpdateItems(viewsets.ModelViewSet):
    def update(self, request, *args, **kwargs):
        try:
            proxy = request.user.proxy
        except Exception:
            proxy = None

        if proxy:
            id_order = kwargs.get('pk')
            items_post = request.data['items']
            order = Order.objects.get(id=id_order)
            if order.status == Order.MATCHED:
                sum_prices = 0
                for item in items_post:
                    item_db = Item.objects.get(id=item.get("id"))
                    item_db.price_proxy = item.get("price_proxy")
                    item_db.notes_proxy = item.get("notes_proxy")
                    if item_db.price_proxy:
                        try:
                            sum_prices += float(item.get("price_proxy"))
                        except Exception:
                            return Response({"Error": "The prices must be numbers"})
                    else:
                        return Response({"Error": "All item must have a proxy user's price"})
                    item_db.save()
                order.total_price_proxy = sum_prices
                order.fee_dope_places = 0.1 * order.total_price_proxy
                order.final_price = order.total_price_proxy + order.fee_dope_places

                order.status = Order.CONFIRM_AND_PAY
                order.save()
                serializer = OrderSerializer(order)
                return Response({'order': serializer.data})
            else:
                content = {'Error': 'Status matched of order is required'}
                return Response(content, status=status.HTTP_401_UNAUTHORIZED)
        else:
            content = {'Unauthorized access': 'You are not a profile'}
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)


class CreatePhotos(viewsets.ModelViewSet):

    def create(self, request, *args, **kwargs):
        try:
            proxy = request.user.proxy
        except Exception:
            proxy = None

        if proxy:
            data = request.POST
            id_order = data.get('id_order')
            order = Order.objects.get(id=id_order)

            if order.status == Order.SHOPPING:
                photo = Photo.objects.create(item_id=data.get('id_item'),
                                             image=self.request.FILES['image'])

                return Response(PhotoSerializer(photo).data)
            else:
                return Response({'Error': 'Order status is not Shopping'})
        else:
            return Response({'Error': "User is not a proxy"})
    pass
