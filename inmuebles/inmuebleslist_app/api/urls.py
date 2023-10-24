from django.urls import path

# from inmuebleslist_app.api.views import , inmueble_detalle
from inmuebleslist_app.api.views import (
    InmueblesListAV,
    InmuebleDetalleAV,
    EmrpesaListAv,
)

# urlpatterns = [
#     path("list/", inmueble_list, name="inmueble-list"),
#     path("select_id/<int:pk>", inmueble_detalle, name="inmueble-detalle"),
# ]
urlpatterns = [
    path("list/", InmueblesListAV.as_view(), name="inmueble-list"),
    path("select_id/<int:pk>", InmuebleDetalleAV.as_view(), name="inmueble-detalle"),
    path("empresa/", EmrpesaListAv.as_view(), name="empresa-list"),
]
