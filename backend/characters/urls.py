from rest_framework.routers import SimpleRouter

from .views import CharacterViewSet


router = SimpleRouter()
router.register("", CharacterViewSet, basename="character")

urlpatterns = router.urls
