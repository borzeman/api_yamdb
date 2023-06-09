from django.db.models import Avg
from rest_framework import serializers

from artworks.models import Category, Genre, Title
from reviews.models import Comment, Review
from users.models import ConfirmCode, CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.SlugRelatedField(
        slug_field='username',
        queryset=CustomUser.objects.all())

    class Meta:
        model = ConfirmCode
        fields = ('username', 'confirmation_code')


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role')

    def validate_role(self, value):
        user = self.context.get("request").user
        if user.role == 'admin':
            return value
        return user.role


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'category', 'genre', 'year', 'description',
                  'rating',)
        read_only_fields = ['id', ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = {
            'name': instance.category.name,
            'slug': instance.category.slug
        }
        representation['genre'] = [
            {
                'name': genre.name,
                'slug': genre.slug
            }
            for genre in instance.genre.all()
        ]
        return representation

    def get_rating(self, obj):
        rating = (
            obj.reviews.filter(title=obj)
            .aggregate(Avg('score'))
            ['score__avg']
        )
        if rating:
            return int(rating)
        else:
            return None


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, attrs):
        if self.context['request'].method == 'POST':
            if Review.objects.filter(
                title_id=self.context['view'].kwargs.get('title_id'),
                author=self.context['request'].user,
            ).exists():
                raise serializers.ValidationError(
                    'Попытка оставить повторный отзыв',
                )
        return attrs
