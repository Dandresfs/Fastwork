from rest_framework.serializers import ModelSerializer
from hv.models import Experiencia, Formacion

class ExperienciaSerializer(ModelSerializer):
    class Meta:
        model = Experiencia
        fields = ('id','user','empresa','departamento','sector','cargo','area','periodo','funciones_logros','meses')

class FormacionSerializer(ModelSerializer):
    class Meta:
        model = Formacion
        fields = ('id','user','institucion','nivel','area','estado','periodo')