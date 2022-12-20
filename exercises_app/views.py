from rest_framework import status
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response

import json

from .models import Equipments, Excercises
from .serializer import EquipmentsSerializer, ExcercisesSerializer, ReportSerializer

# Create your views here.
class registerEquipment(APIView):
    "Register Equipments of Gym"
    def post(self, request):
        serializer_obj = EquipmentsSerializer(data=request.data)
        if serializer_obj.is_valid():
            serializer_obj.save()
            return Response({
                'error': False, 
                'message':'Equipment Registered', 
                'data':[]},
                status=status.HTTP_201_CREATED)
        return Response({
                'error': True, 
                'message':'Entered Data is Incorrect', 
                'data':[serializer_obj.errors]},
                status=status.HTTP_400_BAD_REQUEST)

class recordExercise(APIView):
    "Record Excercises"
    def post(self, request):
        request_data = request.data
        equipment_obj = Equipments.objects.filter(name=request_data.get('equipment'))
        if equipment_obj:
            del request_data['equipment']
            serializer_obj = ExcercisesSerializer(data=request_data)
            if serializer_obj.is_valid():
                serializer_obj.save(athlete=request.user, equipment=equipment_obj.first())
                return Response({
                    'error': False, 
                    'message':'Excercise Recorded Successfully', 
                    'data':[]},
                    status=status.HTTP_201_CREATED)
            return Response({
                    'error': True, 
                    'message':'Entered Data is Incorrect', 
                    'data':[serializer_obj.errors]},
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'error': True, 
                'message':'Equipment not found', 
                'data':[{'equipment':f'{request_data.get("equipment")} not found'}]},
                status=status.HTTP_400_BAD_REQUEST)

class exerciseReport(APIView):
    "Generating Reports for Excercises Performed by User"
    def get(self, request):
        print('yahan tak okay')
        print(request.body)
        serializer_obj = ReportSerializer(data=json.loads(request.body))
        if serializer_obj.is_valid():
            user_obj = request.user
            excercises_obj = Excercises.objects.filter(
                athlete=user_obj,
                recorded_at__gte = serializer_obj.validated_data.get('start'),
                recorded_at__lte = serializer_obj.validated_data.get('end')
                ).aggregate(
                    total_calories_burnt=Sum('calories_burnt'), 
                    total_duration=Sum('duration'))
            return Response({
                    'error': False, 
                    'message':'Excercise Report', 
                    'data':excercises_obj},
                    status=status.HTTP_200_OK)
        return Response({
                'error': True, 
                'message':'Entered Data is Incorrect', 
                'data':[serializer_obj.errors]},
                status=status.HTTP_400_BAD_REQUEST)
