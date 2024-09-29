from django.contrib import admin
from django.template.context_processors import static
from django.urls import path, include
from django.conf.urls.i18n import set_language
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
