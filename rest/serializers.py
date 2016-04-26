from rest_framework.serializers import ModelSerializer, SlugRelatedField
from hv.models import Experiencia, Formacion
from ofertas.models import Oferta, Categoria
from empresa.models import Empresa

class ExperienciaSerializer(ModelSerializer):
    class Meta:
        model = Experiencia
        fields = ('id','user','empresa','departamento','sector','cargo','area','periodo','funciones_logros','meses')

class FormacionSerializer(ModelSerializer):
    class Meta:
        model = Formacion
        fields = ('id','user','institucion','nivel','area','estado','periodo')

class EmpresaSerializer(ModelSerializer):
    class Meta:
        model = Empresa
        fields = ('nombre_comercial','razon_social','verificada')


class CategoriaSerializer(ModelSerializer):
    class Meta:
        model = Categoria
        fields = ('nombre',)


class OfertaSerializer(ModelSerializer):
    empresa = EmpresaSerializer()
    categoria = CategoriaSerializer()

    class Meta:
        model = Oferta
        fields = ('id','empresa','categoria','titulo','descripcion','fecha_contratacion','vacantes','departamento','municipio',
                  'salario','educacion','experiencia','viajar','residencia','publicacion','actualizacion','cierre')