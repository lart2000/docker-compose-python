# apps/orders/viewsets.py
# Python imports


# Django imports
from django.db.models.query import QuerySet
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.paginator import Paginator


# Third party apps imports
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

# Local imports
from .models import Order, Comment
from .serializers import OrderSerializer, CommentSerializer, OrderHistorySerializer
from apps.customers.serializers import CustomerSerializer
from apps.proxies.serializers import ProxySerializer


# Create your viewsets here.
class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    filter_fields = ('status',)

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.none()
        if hasattr(user, 'customer'):
            queryset = Order.objects.filter(customer=user.customer)
        if hasattr(user, 'proxy'):
            queryset = Order.objects.filter(
                (Q(proxy=user.proxy) | Q(status=Order.POSTED))
                & Q(country=user.proxy.country)
                ).exclude(
                    status=Order.DRAFT)
        if hasattr(user, 'admin'):
            queryset = Order.objects.all()

        if isinstance(queryset, QuerySet):
            queryset = queryset.all()
        return queryset

    @action(detail=False, methods=['POST'])
    def history(self, request, *args, **kwargs):
        user = User.objects.get(auth_token=request.auth)
        queryset = Order.objects.none()

        page = request.data['pagination']['page']
        per_page = request.data['pagination']['per_page']

        if hasattr(user, 'proxy'):
            queryset = Order.objects.all().filter(Q(status=Order.DELIVERED)& Q(proxy=user.proxy))
        if hasattr(user, 'customer'):
            queryset = Order.objects.all().filter(Q(status=Order.DELIVERED) & Q(customer=user.customer))

        quantity = queryset.__len__()
        quantity_pages = int(quantity / per_page)
        paginator = Paginator(queryset.values(), quantity_pages)

        if page <= quantity_pages:
            result = paginator.page(page).object_list
        else:
            result = {}

        serializer = OrderHistorySerializer(result, many=True)

        if hasattr(user, 'proxy'):
            return Response({
                            "quantity": quantity,
                            "data": serializer.data,
                            "proxy": ProxySerializer(user.proxy).data
                            })
        elif hasattr(user, 'customer'):
            return Response({
                "quantity": quantity,
                "data": serializer.data,
                "customer": CustomerSerializer(user.customer).data
            })
        else:
            return Response({"error": "user has not profile"})


class CommentViewSet(ModelViewSet):

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    @action(detail=True)
    def show(self, request, pk=None):
        order_id = pk
        comments = Comment.objects.filter(order=order_id).order_by('-creation_date')
        comment_serializer = CommentSerializer(comments, many=True)

        order = Order.objects.get(id=order_id)
        customer = order.customer
        customer_serializer = CustomerSerializer(customer)
        proxy = order.proxy
        proxy_serializer = ProxySerializer(proxy)

        return Response({"customer": customer_serializer.data,
                         "proxy": proxy_serializer.data,
                         "comment": comment_serializer.data
                         })

    def create(self, request, *args, **kwargs):
        order_id = request.data['order_id']
        user = User.objects.get(auth_token=request.auth.key)
        order = Order.objects.get(pk=order_id)

        if user.id == order.customer.user.id or user.id == order.proxy.user.id:
            message = request.data['message']

            comment = Comment.objects.create(order=order, message=message, user=user)
            serializer = CommentSerializer(comment)
            return Response({"comment": serializer.data})
        else:
            return Response({"error": "User does not have privileges to modify this order"})
