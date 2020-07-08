from rest_framework import routers
from main.views import *

router = routers.DefaultRouter()
router.register('facturas', FacturaViewSet, 'facturas')
router.register('items', ItemViewSet, 'items')
router.register('cajas', CajaViewSet, 'cajas')
urlpatterns = router.urls