from rest_framework import serializers
from artworks.models import Category, Genre, Title, Review, Comment
from users.models import CustomUser, ConfirmCode


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
        if user.is_staff:
            return value
        return user.role


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')

class GenreSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    class Meta:
        model = Genre
        fields = ('id', 'name', 'genre')

class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer()

    class Meta:
        model = Title
        fields = ('id', 'name', 'category', 'genre', 'year')

class ReviewSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer()
    title = TitleSerializer()

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'pub_date', 'title', 'score')

class CommentSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer()
    review = ReviewSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date', 'review')