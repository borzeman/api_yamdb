from rest_framework import serializers

from .models import CustomUser, ConfirmCode

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class TokenSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=CustomUser.objects.all())
    class Meta:
        model = ConfirmCode
        fields = ('user', 'confirmation_code')


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')

    def validate_role(self, value):
        user = self.context.get("request").user
        if user.role == 'admin':
            return value
        return user.role


