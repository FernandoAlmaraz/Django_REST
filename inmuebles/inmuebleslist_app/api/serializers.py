from rest_framework import serializers
from inmuebleslist_app.models import Edificacion, Empresa, Comentario


class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        exclude = ["edificaion"]
        ##fields = "__all__"


class EdificacionSerializer(serializers.ModelSerializer):
    comentarios = ComentarioSerializer(many=True, read_only=True)

    class Meta:
        model = Edificacion
        fields = "__all__"


class EmpresaSerializer(serializers.HyperlinkedModelSerializer):
    edificacionList = EdificacionSerializer(many=True, read_only=True)
    # todos los valores

    # edificacionList = serializers.StringRelatedField(
    #     many=True,
    # ) solo el metodo string del modelo
    # edificacionList = serializers.PrimaryKeyRelatedField(many=True, read_only=True) solo id
    # edificacionList = serializers.HyperlinkedIdentityField(
    #     many=True,
    #     read_only=True,
    #     view_name="inmueble-detalle",
    # )
    class Meta:
        model = Empresa
        fields = "__all__"

        # fields = ["id", "pais"]
        # exclude = ["id"]

        # def validate(self, data):
        #     if data["direccion"] == data["pais"]:
        #         raise serializers.ValidationError(
        #             "La direccion y el pais deben ser diferentes"
        #         )
        #     else:
        #         return data

        # def validate_image(self, data):
        #     if len(data) < 2:
        #         raise serializers.ValidationError("La url es muy corta")
        #     else:
        #         return data


# def column_longitud(value):
#     if len(value) < 2:
#         raise serializers.ValidationError("La direccion es muy corta")


# class InmuebleSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     direccion = serializers.CharField(validators=[column_longitud])
#     pais = serializers.CharField()
#     descripcion = serializers.CharField()
#     image = serializers.CharField()
#     active = serializers.BooleanField()

#     def create(self, validate_data):
#         return Inmueble.objects.create(**validate_data)

#     def update(self, instance, validated_data):
#         instance.direccion = validated_data.get("direccion", instance.direccion)
#         instance.pais = validated_data.get("pais", instance.pais)
#         instance.descripcion = validated_data.get("descripcion", instance.descripcion)
#         instance.image = validated_data.get("image", instance.image)
#         instance.active = validated_data.get("active", instance.active)
#         instance.save()
#         return instance
