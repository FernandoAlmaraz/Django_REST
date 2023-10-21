from django.urls import path
from inmuebleslist_app.views import inmueble_list

urlpatterns = [path("list/", inmueble_list, name="inmueble-list")]
