from inmuebleslist_app.models import Edificacion, Empresa, Comentario
from inmuebleslist_app.api.serializers import (
    EdificacionSerializer,
    EmpresaSerializer,
    ComentarioSerializer,
)
from rest_framework.response import Response
from rest_framework import mixins, generics
from rest_framework.exceptions import ValidationError
from inmuebleslist_app.api.permissions import AdminOrReadOnly, CometarioUserOrReadOnly

# from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated


class ComentarioCreate(generics.CreateAPIView):
    serializer_class = ComentarioSerializer

    def get_queryset(self):
        return Comentario.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get("pk")
        edificaion = Edificacion.objects.get(pk=pk)
        user = self.request.user
        comentario_queryset = Comentario.objects.filter(
            edificaion=edificaion, comentario_user=user
        )
        if comentario_queryset.exists():
            raise ValidationError(
                "El usuario ya añadio un comentario para este inmueble."
            )
        if edificaion.number_calificacion == 0:
            edificaion.avg_calificacion = serializer.validated_data["calificacion"]
        else:
            edificaion.avg_calificacion = (
                serializer.validated_data["calificacion"] + edificaion.avg_calificacion
            ) / 2
        edificaion.number_calificacion = edificaion.number_calificacion + 1
        edificaion.save()

        serializer.save(edificaion=edificaion, comentario_user=user)


class ComentarioList(generics.ListCreateAPIView):
    # queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Comentario.objects.filter(edificaion=pk)


class ComentarioDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
    permission_classes = [CometarioUserOrReadOnly]


# class ComentarioList(
#     mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
# ):
#     queryset = Comentario.objects.all()
#     serializer_class = ComentarioSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class ComentarioDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Comentario.objects.all()
#     serializer_class = ComentarioSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)


class EmpresaVS(viewsets.ModelViewSet):
    ##permission_classes = [IsAuthenticated]
    permission_classes = [AdminOrReadOnly]
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer


# class EmpresaVS(viewsets.ViewSet):
#     def list(self, request):
#         queryset = Empresa.objects.all()
#         serialzer = EmpresaSerializer(queryset, many=True)
#         return Response(serialzer.data)

#     def retrieve(self, request, pk=None):
#         queryset = Empresa.objects.all()
#         edificacionList = get_object_or_404(queryset, pk=pk)
#         serializer = EmpresaSerializer(edificacionList)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = EmpresaSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)

#     def update(self, request, pk):
#         try:
#             empresa = Empresa.objects.get(pk=pk)
#         except Empresa.DoesNotExist:
#             return Response(
#                 {"error": "empresa no encontrada"}, status=status.HTTP_400_BAD_REQUEST
#             )
#         serializer = EmpresaSerializer(empresa, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def distroy(self, requesy, pk):
#         try:
#             empresa = Empresa.objects.get(pk=pk)
#         except Empresa.DoesNotExist:
#             return Response(
#                 {"error": "empresa no encontrada"}, status=status.HTTP_400_BAD_REQUEST
#             )
#         empresa.delete()
#         return Response(status=status.HTTP_400_BAD_REQUEST)


class EmpresaListAv(APIView):
    def get(self, request):
        empresas = Empresa.objects.all()
        serializer = EmpresaSerializer(
            empresas, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = EmpresaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmpresaDetalleAV(APIView):
    def get(self, request, pk):
        try:
            empresa = Empresa.objects.get(pk=pk)
        except Empresa.DoesNotExist:
            return Response(
                {"error": "Empresa no encontrada"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = EmpresaSerializer(empresa, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            empresa = Empresa.objects.get(pk=pk)
        except Empresa.DoesNotExist:
            return Response(
                {"error": "Empresa no encontrada"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = EmpresaSerializer(
            empresa, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            empresa = Empresa.objects.get(pk=pk)
        except Empresa.DoesNotExist:
            return Response(
                {"Error": "la empresa no existe."}, status=status.HTTP_404_NOT_FOUND
            )
        empresa.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EdificacionListAV(APIView):
    def get(self, request):
        edificacion = Edificacion.objects.all()
        serializer = EdificacionSerializer(edificacion, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        de_serializer = EdificacionSerializer(data=request.data)
        if de_serializer.is_valid():
            de_serializer.save()
            return Response(de_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(de_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EdificacionDetalleAV(APIView):
    def get(self, request, pk):
        try:
            edificacion = Edificacion.objects.get(pk=pk)
        except Edificacion.DoesNotExist:
            return Response(
                {"Error": "El inmueble no existe."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = EdificacionSerializer(edificacion)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            edificacion = Edificacion.objects.get(pk=pk)
        except Edificacion.DoesNotExist:
            return Response(
                {"Error": "El inmueble no se puede actualizar"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = EdificacionSerializer(edificacion, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            edificacion = Edificacion.objects.get(pk=pk)
        except Edificacion.DoesNotExist:
            return Response(
                {"Error": "El inmueble no existe."}, status=status.HTTP_404_NOT_FOUND
            )
        edificacion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(["GET", "POST"])
# def inmueble_list(request):
#     if request.method == "GET":
#         inmuebles = Inmueble.objects.all()
#         serializer = InmuebleSerializer(inmuebles, many=True)
#         return Response(serializer.data)

#     if request.method == "POST":
#         de_serializer = InmuebleSerializer(data=request.data)
#         if de_serializer.is_valid():
#             de_serializer.save()
#             return Response(de_serializer.data, status=200)
#         else:
#             return Response(de_serializer.errors, status=404)


# @api_view(["GET", "PUT", "DELETE"])
# def inmueble_detalle(request, pk):
#     if request.method == "GET":
#         try:
#             inmueble = Inmueble.objects.get(pk=pk)
#             serializer = InmuebleSerializer(inmueble)
#             return Response(serializer.data)
#         except Inmueble.DoesNotExist:
#             return Response(
#                 {"Error": "El inmueble no existe."}, status=status.HTTP_404_NOT_FOUND
#             )

#     if request.method == "PUT":
#         recordDB = Inmueble.objects.get(pk=pk)
#         de_serializer = InmuebleSerializer(recordDB, data=request.data)
#         if de_serializer.is_valid():
#             de_serializer.save()
#             return Response(de_serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(de_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     if request.method == "DELETE":
#         try:
#             recordDB = Inmueble.objects.get(pk=pk)
#             recordDB.delete()
#         except Inmueble.DoesNotExist:
#             return Response(
#                 {"Error": "EL Inmueble no existe."}, status=status.HTTP_204_NO_CONTENT
#             )
