from django.conf.urls import url,include
from django.contrib import admin
from django.conf.urls import url
from ui import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'', include('ui.urls' )),
        url(r'^page', views.treneri, name='treneri'),
   ] 