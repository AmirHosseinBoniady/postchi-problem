from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import UserProfile, Mission, Point

class UserProfileSerializer(serializers.ModelSerializer):

    #missions = MissionSerializer()
    class Meta:
        model = UserProfile
        fields = (
            'name','email', 'address' ,'is_in_mission', 'current_position_x', 'current_position_y'
        )

class UserProfileCreateSerializer(serializers.ModelSerializer):

    #missions = MissionSerializer()
    class Meta:
        model = UserProfile
        fields = (
            'name','password','email', 'address' ,'is_in_mission', 'current_position_x', 'current_position_y'
        )

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        
        # Adding the below line made it work for me.
        instance.is_active = True
        if password is not None:
            # Set password does the hash, so you don't need to call make_password 
            instance.set_password(password)
        instance.save()
        return instance

class MissionSerializer(serializers.ModelSerializer):

    #assigned_to = UserProfileSerializer_name()

    class Meta:
        model = Mission
        fields = (
            'title','start_point_x', 'start_point_y', 'end_point_x', 'end_point_y', 'assigned_to', 'is_finished'  
        )

class DetailMissionSerializer(serializers.ModelSerializer):

    # missions = MissionSerializer()
    class Meta:
        model = Mission
        fields = (
            'title','start_point_x', 'start_point_y', 'end_point_x', 'end_point_y','is_finished'  
        )

   
User = get_user_model()


class MissionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Mission
        fields = (
            'title','start_point_x', 'start_point_y', 'end_point_x', 'end_point_y', 'assigned_to', 'is_finished'  
        )

    
class MissionListSerializer(serializers.ModelSerializer):

    assigned_to = UserProfileSerializer()

    class Meta:
        model = Mission
        fields = (
            'title','start_point_x', 'start_point_y', 'end_point_x', 'end_point_y', 'assigned_to', 'is_finished'  
        )

class GetPointSerializer(serializers.ModelSerializer):

    class Meta:
        model = Point
        fields = (
            'start_point_x','start_point_y'
        )
class UpdatePositionSerializer(serializers.Serializer):
    name = serializers.CharField()
    current_position_x = serializers.IntegerField()
    current_position_y = serializers.IntegerField()