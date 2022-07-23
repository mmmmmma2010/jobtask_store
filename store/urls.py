from rest_framework_nested import routers
from .views import item_views,order_views,customer_view

router = routers.DefaultRouter()
router.register('items', item_views.ItemViewSet, basename='items')
router.register('categorys', item_views.CategoryViewSet)
router.register('carts', item_views.CartViewSet)
router.register('customers', customer_view.CustomerViewSet)
router.register('orders', order_views.OrderViewSet, basename='orders')

items_router = routers.NestedDefaultRouter(
    router, 'items', lookup='item')


carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', item_views.CartItemViewSet, basename='cart-items')

# URLConf
urlpatterns = router.urls + items_router.urls + carts_router.urls
