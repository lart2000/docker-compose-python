# apps/core/routers.py

# Python imports


# Django imports


# Third party apps imports
from rest_framework.routers import DefaultRouter


# Local imports
from apps.countries.routers import countries
from apps.customers.routers import customers
from apps.items.routers import items
from apps.orders.routers import orders
from apps.proxies.routers import proxies
from apps.admins.routers import admins


# Create your routers here.
routers_tuples = (countries, customers, items, orders, proxies, admins)
routers_lists = sum(
    [list(router_tuple) for router_tuple in routers_tuples], [])

router = DefaultRouter()

for router_list in sorted(routers_lists):
    router.register(router_list[0], router_list[1], base_name=router_list[0])
