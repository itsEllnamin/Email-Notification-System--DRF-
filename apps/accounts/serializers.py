from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
import re



class UserSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(max_length=60, write_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "re_password",
        )
        extra_kwargs = {"email": {"required": True}, "password": {"write_only": True}}

    def create(self, validated_data):
        del validated_data["re_password"]

        # We must hash the password before creating the user
        password = validated_data["password"]
        validated_data["password"] = make_password(password)

        return super().create(validated_data)

    def validate(self, data):
        if data["re_password"] != data["password"]:
            raise serializers.ValidationError(
                "Password and its repetition are not the same"
            )
        return data

    def validate_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if re.match(pattern, email):
            return email
        raise serializers.ValidationError("Email is invalid")


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )

            if not user:
                msg = "Unable to log in with provided credentials."
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code="authorization")

        data["user"] = user
        return data
