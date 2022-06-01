from django.shortcuts import render
from rest_framework import viewsets
from user.models import User
from .serializers import UserSerializer
import user
from rest_framework.response import Response

# Create your views here.


class UserViewset(viewsets.ModelViewSet):
    queryset =User.objects.all()
    serializer_class = UserSerializer

   
    # def get_queryset(self):
    #     Users = User.objects.all()
    #     return Users
    
    # def create(self, request, *args, **kwargs):
    #     car_data = request.data

    #     # new_car = User.objects.create(first_Name = car_data['first_Name'] , 
    #     # Last_Name = car_data['Last_Name'],
    #     # Email_id = car_data['Email_id'],
    #     # Mobile_Number = car_data['Mobile_Number'],
    #     # Password = car_data['Password'] )

    #     # new_car.save()

    #     # serializer = UserSerializer(new_car)

    #     return Response('hello')

    # def retrieve(self, request, *args, **kwargs):
    #     params = kwargs
    #     print(params['pk'])
    #     params_list = params['pk'].split('-')
    #     cars = CarSpecs.objects.filter(
    #         car_brand=params_list[0], car_model=params_list[1])
    #     serializer = CarSpecsSerializer(cars, many=True)
    #     return Response(serializer.data)