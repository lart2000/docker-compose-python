# apps/payments/viewsets.py
# Python imports


# Django imports
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie, csrf_exempt

# Third party apps imports
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny

from config.paypal_config import PayPalClient
from paypalcheckoutsdk.orders import OrdersCreateRequest
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment



# Local imports
from .models import Payment
from .serializers import PaymentSerializer
from apps.orders.models import Order
import sys


# Create your viewsets here.

class CreateOrder(PayPalClient):

    def create_order(self, order, debug=False):
        request = OrdersCreateRequest()
        request.prefer('return=representation')

        request.request_body(self.build_request_body(order))
        response = self.client.execute(request)
        if debug:
            print('Status Code: ', response.status_code)
            print('Status: ', response.result.status)
            print('Order ID: ', response.result.id)
            print('Intent: ', response.result.intent)
            print('Links:')

            for link in response.result.links:
                print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))

            print('Total Amount: {} {}'.format(response.result.purchase_units[0].amount.currency_code,
                    response.result.purchase_units[0].amount.value))
        return response

    def build_request_body(self, order):

        request = {
                "intent": "CAPTURE",
                "application_context": {
                    "brand_name": "EXAMPLE INC",
                    "landing_page": "BILLING",
                    "shipping_preference": "GET_FROM_FILE",
                    "user_action": "CONTINUE"
                },
                "purchase_units": [
                    {
                        "reference_id": order.id,
                        "description": "Dope Places",

                        "amount": {
                            "currency_code": order.country.currency,
                            "value": str(order.final_price),
                            "breakdown": {
                                "item_total": {
                                    "currency_code": order.country.currency,
                                    "value": str(order.total_price_proxy)
                                },
                                "handling": {
                                    "currency_code": order.country.currency,
                                    "value": str(order.fee_dope_places)
                                }
                            }

                        },
                        "items": self.list_items_oreder(order)

                    }
                ]
            }
        return request

    def list_items_oreder(self, order):
        items = []
        for item in order.items:
            items.append({
                "name": item.name,
                "sku": str(item.id),
                "unit_amount": {
                    "currency_code": order.country.currency,
                    "value": str(item.price_proxy)},
                "quantity": 1,
            })
        return items


@api_view()
def setup_transaction(request, id):
    paypal_order = CreateOrder()
    order = Order.objects.get(id=id)
    paypal_response = paypal_order.create_order(order, debug=True)

    links = []
    for link in paypal_response.result.links:
        links.append({
            "relation": link.rel,
            "link": link.href,
            "method": link.method
        })

    response = {
        "status_code": paypal_response.status_code,
        "status": paypal_response.result.status,
        "order_id": paypal_response.result.id,
        "intent": paypal_response.result.intent,
        "links": links
    }
    return Response(response)

