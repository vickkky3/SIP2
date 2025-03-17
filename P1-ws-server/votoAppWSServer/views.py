from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Censo, Voto
from .serializers import CensoSerializer, VotoSerializer


class CensoView(APIView):
    def post(self, request):
        dni = request.data.get("numeroDNI")
        if Censo.objects.filter(numeroDNI=dni).exists():
            return Response({'message': 'Datos encontrados en Censo.'}, status=status.HTTP_200_OK)
        return Response({'message': 'Datos no encontrados en Censo.'}, status=status.HTTP_404_NOT_FOUND)


class VotoView(APIView):
    """
    API endpoint to collect voto information,
    and save it in the database.
    """
    def post(self, request):
        cens = request.data.get("censo_id")

        if not Censo.objects.filter(numeroDNI=cens).exists():
            return Response({'message': 'Votante no encontrado en el censo.'}, status=status.HTTP_404_NOT_FOUND)
        
        censo_obj = Censo.objects.get(numeroDNI=cens)

        data = request.data.copy()
        data["censo"] = censo_obj.numeroDNI  
        data.pop("censo_id", None)  

        # Serializar y guardar
        serializer = VotoSerializer(data=data)

        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id_voto):
        voto = get_object_or_404(Voto, id=id_voto)
        voto.delete()
        return Response({'message': 'Voto eliminado correctamente.'}, status=status.HTTP_200_OK)


class ProcesoElectoralView(APIView):
    def get(self, request, idProcesoElectoral):
        votos = Voto.objects.filter(idProcesoElectoral=idProcesoElectoral)
        if not votos.exists():
            return Response({'message': 'No hay votos para este proceso electoral.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = VotoSerializer(votos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TestBDView(APIView):
    def get(self, request):
        return Response({'message': 'La conexión a la base de datos funciona correctamente.'}, status=status.HTTP_200_OK)
