from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response

from .models import ( 
  ProductCategory, 
  Data, 
  DataSettings, 
  AirtimeSettings,
  CableSettings,
  Cable,
  Electricity,
  ElectricitySettings
  )
from .serializers import (
  ProductCategorySerializer, 
  NetworkSerializer, 
  DataSerializer, 
  PlanTypeSerializer, 
  AirtimeTypeSerializer,
  CableCategorySerializer,
  CablePlansSerializer,
  ElectricitySerializer,
  ElectricitySettingsSerializer
  )



# class ProductCategoryView(APIView):
#   def get(self, request):
#     data = ProductCategory.objects.all()
#     serializer = ProductCategorySerializer(data, many=True)
#     return Response(serializer.data)



#######################################################################################
####### DATA #####################################################################


# class DataNetworkView(APIView):
#   def get(self, request):
#       networks = DataSettings.objects.values('network', 'network_id').distinct()
#       serializer = NetworkSerializer(networks, many=True)
#       return Response(serializer.data)

class DataPlansView(generics.ListAPIView):
  serializer_class = DataSerializer

  def get_queryset(self):
    network_type = self.kwargs['network_type']
    data_plan_type = self.kwargs['data_plan_type']
    return Data.objects.filter(network=network_type, plan_type=data_plan_type, is_active=True)

class PlanTypeView(generics.ListAPIView):
  serializer_class = PlanTypeSerializer
  def get_queryset(self):
    network_type = self.kwargs['network_type']
    return DataSettings.objects.filter(network=network_type)



#######################################################################################
####### AIRTIME #####################################################################

# class AirtimeNetworkView(APIView):
#   def get(self, request):
#       networks = AirtimeSettings.objects.values('network', 'network_id').distinct()
#       serializer = NetworkSerializer(networks, many=True)
#       return Response(serializer.data)

class AirtimeTypeView(generics.ListAPIView):
  serializer_class = AirtimeTypeSerializer
  def get_queryset(self):
    network_type = self.kwargs['network_type']
    return AirtimeSettings.objects.filter(network=network_type)


########################################################################################
##########CABLE SUBSCRIPTION##############################################

# class CableCategoryView(APIView):
#   def get(self, request):
#     cable_category = CableSettings.objects.all()
#     serializer = CableCategorySerializer(cable_category, many=True)
#     return Response(serializer.data)

class CablePlansView(generics.ListAPIView):
  serializer_class = CablePlansSerializer
  
  def get_queryset(self):
    cable_plans = self.kwargs['cable_category']
    return Cable.objects.filter(cable_name=cable_plans)


#########################################################################################
###################ELECTRICITY BILL############################

class ElectricityView(APIView):
  def get(self, request):
    electricity = Electricity.objects.all()
    serializer = ElectricitySerializer(electricity, many=True)
    return Response(serializer.data)

class ElectricitySettingsView(APIView):
  def get(self, request):
    settings = ElectricitySettings.objects.all()
    serializer = ElectricitySettingsSerializer(settings, many=True)
    return Response(serializer.data)


class CombinedDataView(APIView):
    def get(self, request):
        # Fetch data for each category
        product_data = ProductCategory.objects.all()
        electricity = Electricity.objects.all()
        data_networks = DataSettings.objects.values('network', 'network_id').distinct()
        airtime_networks = AirtimeSettings.objects.values('network', 'network_id').distinct()
        cable_categories = CableSettings.objects.all()
        electricity_settings = ElectricitySettings.objects.all()


        # Serialize the data
        product_data_serialized = ProductCategorySerializer(product_data, many=True).data
        data_networks_serialized = NetworkSerializer(data_networks, many=True).data
        airtime_networks_serialized = NetworkSerializer(airtime_networks, many=True).data
        cable_categories_serialized = CableCategorySerializer(cable_categories, many=True).data
     



        # Combine into a single response
        combined_data = {
            'productData': product_data_serialized,
            'dataNetworks': data_networks_serialized,
            'airtimeNetworks': airtime_networks_serialized,
            'cableCategories': cable_categories_serialized,
        }
        
        return Response(combined_data, status=status.HTTP_200_OK)