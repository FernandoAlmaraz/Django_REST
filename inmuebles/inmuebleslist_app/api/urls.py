from django.urls import path, include
from rest_framework.routers import DefaultRouter


# from inmuebleslist_app.api.views import , inmueble_detalle
from inmuebleslist_app.api.views import (
    EdificacionListAV,
    EdificacionDetalleAV,
    EmpresaListAv,
    EmpresaDetalleAV,
    ComentarioList,
    ComentarioDetail,
    ComentarioCreate,
    EmpresaVS,
)

# urlpatterns = [
#     path("list/", inmueble_list, name="inmueble-list"),
#     path("select_id/<int:pk>", inmueble_detalle, name="inmueble-detalle"),
# ]
router = DefaultRouter()
router.register("empresa", EmpresaVS, basename="empresa")
urlpatterns = [
    ##edificacion
    path("edificacion/", EdificacionListAV.as_view(), name="inmueble-list"),
    path(
        "edificacion/<int:pk>", EdificacionDetalleAV.as_view(), name="inmueble-detail"
    ),
    ##empresa
    path("", include(router.urls)),
    path("empresa/", EmpresaListAv.as_view(), name="empresa-list"),
    path("empresa/<int:pk>", EmpresaDetalleAV.as_view(), name="empresa-detail"),
    ##comentarios
    path(
        "edificacion/<int:pk>/comentario-create/",
        ComentarioCreate.as_view(),
        name="comentario-create",
    ),
    path(
        "edificacion/<int:pk>/comentario/",
        ComentarioList.as_view(),
        name="comentario-list",
    ),
    path(
        "edificacion/comentario/<int:pk>",
        ComentarioDetail.as_view(),
        name="comentario-detail",
    ),
]
