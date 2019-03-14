# apps/orders/serializers.py
# Python imports


# Django imports


# Third party apps imports
from rest_framework import serializers


# Local imports
from .models import Order, Comment
from apps.countries.fields import CountryField
from apps.customers.fields import CustomerField
from apps.proxies.fields import ProxyField
from apps.items.models import Item
from apps.items.serializers import ItemSerializer


# Create your serializers here.

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    country = CountryField()
    customer = CustomerField(required=False)
    items = ItemSerializer(many=True)
    proxy = ProxyField(required=False)
    comments = CommentSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = (
            'id', 'country', 'customer', 'items', 'name', 'notes', 'proxy',
            'status', 'total_price', 'shipping_company', 'tracking_number', 'delivery_date',
            'total_price_proxy', 'fee_dope_places', 'final_price', 'comments')

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(
            customer=self.context['request'].user.customer, **validated_data)
        for item_data in items_data:
            Item.objects.create(order=order, **item_data)
        return order

    def update(self, instance, validated_data):
        if instance.status == Order.POSTED:
            if len(validated_data) == 0:
                try:
                    proxy = self.context['request'].user.proxy
                except Exception:
                    proxy = None
                if proxy:
                    instance.proxy = proxy
                    instance.status = Order.MATCHED
        if instance.status == Order.DRAFT:
            if 'items' in validated_data:
                items_from_request = []
                for item_data in validated_data.pop('items'):
                    item_data['order'] = instance
                    item, created = Item.objects.get_or_create(**item_data)
                    items_from_request.append(item)
                for item in instance.items:
                    if item not in items_from_request:
                        Item.objects.get(id=item.id).delete()
        if instance.status == Order.DELIVERY:
            if self.context['request'].user.proxy:
                msg_error = {}
                if "shipping_company" not in validated_data:
                    msg_error["shipping_company"] = "parameter is required "
                if "tracking_number" not in validated_data:
                    msg_error["tracking_number"] = "parameter is required"
                if "delivery_date" not in validated_data:
                    msg_error["delivery_date"] = "parameter is required"
                if msg_error:
                    data = {"Message": msg_error}
                    raise serializers.ValidationError(data, code="Not valid request")
                instance.shipping_company = validated_data['shipping_company']
                instance.tracking_number = validated_data['tracking_number']
                instance.delivery_date = validated_data['delivery_date']
                instance.status = Order.DELIVERED
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class OrderHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('id', 'total_price_proxy', 'shipping_company', 'tracking_number', 'delivery_date')
