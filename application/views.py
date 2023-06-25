from django.shortcuts import render, get_object_or_404
from rest_framework import generics as rfg
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from .models import UserProfile, Mission
from .serializers import UpdatePositionSerializer, GetPointSerializer, UserProfileSerializer, UserProfileCreateSerializer, DetailMissionSerializer, MissionListSerializer, MissionSerializer
from math import sqrt
import string


    

class FindNearPostchiView(APIView):
    permission_classes = (IsAdminUser,)
    def post(self, request):   # show near postchi by distance
        serializer = GetPointSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        distances = claculate_distances(serializer.data["start_point_x"],serializer.data["start_point_y"])
        return Response(distances)


class RegisterView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = UserProfileCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# class RegisterView(rfg.CreateAPIView):
#     queryset = UserProfile.objects.all()
#     permission_classes = (AllowAny,)
#     serializer_class = UserProfileSerializer

class UserProfileView(rfg.ListAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.all()


class DetailMissionView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, name):
        print(str(request.user)==str(name))
        if(str(request.user) != str(name)):
            print("users not equal!!")
            raise APIException("you cant see other's mission!!!")
        else:
            id_user = return_id_by_name(name)
            print(id_user)
            mission = get_object_or_404(Mission,assigned_to=id_user)  
            print(mission)
            serializer = DetailMissionSerializer(mission)
            return Response(serializer.data)

def return_id_by_name(name):
    id = UserProfile.objects.filter(name=name).values('id').first()
    return id["id"]

class RegisterMissionView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = MissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # print("request assign",request.data["assigned_to"])
        if request.data["assigned_to"]:
            print("assigned by user!")
            if check_user_status(request.data["assigned_to"]):
                raise serializers.ValidationError({"end_date": "you cant assign to busy postchi"})
        else:
            if not request.data["assigned_to"]:
                if not claculate_distances(request.data["start_point_x"],request.data["start_point_y"]):
                    print("haven't free postchi")
                    raise serializers.ValidationError({"end_date": "there is no free postchi at currnt time!!!"})
                else:
                    appropriate_postchi = claculate_distances(request.data["start_point_x"],request.data["start_point_y"])[0][0]
                    print("appropriate_postchi",appropriate_postchi)
                    serializer.validated_data["assigned_to"] = UserProfile.objects.filter(name=appropriate_postchi).first()
        serializer.save()
        print(serializer.data["assigned_to"])
        update_status_user(serializer.data["assigned_to"])
        return Response(serializer.data, status=status.HTTP_201_CREATED)

def check_user_status(id):
    status_user_selected = UserProfile.objects.filter(id=id).values('is_in_mission').first()
    return status_user_selected["is_in_mission"]

def update_status_user(id):
    print("updating status user",id)
    UserProfile.objects.filter(id=id).update(is_in_mission=True)

# class RegisterMissionView(rfg.CreateAPIView):
#     queryset = Mission.objects.all()
#     permission_classes = (AllowAny,)
#     serializer_class = MissionSerializer

class ListMissionView(rfg.ListAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = MissionListSerializer

    def get_queryset(self):
        return Mission.objects.all()

class UpdatePositionView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
            serializer = UpdatePositionSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = get_object_or_404(UserProfile, name=request.data["name"]) 
            update_postion_user(request.data["name"], request.data["current_position_x"], request.data["current_position_y"], )
            return Response(serializer.data, status=status.HTTP_200_OK)



def update_postion_user(name, new_position_x, new_position_y):
        print("updating position ",name)
        UserProfile.objects.filter(name=name).update(current_position_x=new_position_x,current_position_y=new_position_y)
    

def claculate_distances(x,y):
    free_users = UserProfile.objects.filter(is_in_mission=False).all()
    lists = []
    if not free_users:
        return 0
    else:
        for user in free_users:
            if(user.is_superuser):
                pass
            else:
                name = user.name
                x1 = user.current_position_x
                y1 = user.current_position_y
                dist = sqrt( (x - x1)**2 + (y - y1)**2 )
                lists.append((name,dist))
        lists.sort(key=lambda a: a[1])
        return lists