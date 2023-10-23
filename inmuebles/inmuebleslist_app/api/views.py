from inmuebleslist_app.models import Inmueble
from inmuebleslist_app.api.serializers import InmuebleSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


@api_view(["GET", "POST"])
def inmueble_list(request):
    if request.method == "GET":
        inmuebles = Inmueble.objects.all()
        serializer = InmuebleSerializer(inmuebles, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        de_serializer = InmuebleSerializer(data=request.data)
        if de_serializer.is_valid():
            de_serializer.save()
            return Response(de_serializer.data, status=200)
        else:
            return Response(de_serializer.errors, status=404)


@api_view(["GET", "PUT", "DELETE"])
def inmueble_detalle(request, pk):
    if request.method == "GET":
        try:
            inmueble = Inmueble.objects.get(pk=pk)
            serializer = InmuebleSerializer(inmueble)
            return Response(serializer.data)
        except Inmueble.DoesNotExist:
            return Response(
                {"Error": "El inmueble no existe."}, status=status.HTTP_404_NOT_FOUND
            )

    if request.method == "PUT":
        recordDB = Inmueble.objects.get(pk=pk)
        de_serializer = InmuebleSerializer(recordDB, data=request.data)
        if de_serializer.is_valid():
            de_serializer.save()
            return Response(de_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(de_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "DELETE":
        try:
            recordDB = Inmueble.objects.get(pk=pk)
            recordDB.delete()
        except Inmueble.DoesNotExist:
            return Response(
                {"Error": "EL Inmueble no existe."}, status=status.HTTP_204_NO_CONTENT
            )
