from datetime import datetime

from rest_framework import serializers

from reviews.models import Category, Genre, TitleGenre, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CustomCategoryField(serializers.RelatedField):
    queryset = Category.objects.all()

    def to_internal_value(self, data):
        # Десериализация: из строки в объект
        if isinstance(data, str):
            try:
                return self.get_queryset().get(slug=data)
            except Category.DoesNotExist:
                raise serializers.ValidationError('Category not found.')
        return super().to_internal_value(data)

    def to_representation(self, value):
        # Сериализация: из объекта в словарь
        return {
            'name': value.name,
            'slug': value.slug,
        }


class CustomGenreField(serializers.RelatedField):
    queryset = Genre.objects.all()

    def to_internal_value(self, data):
        # Десериализация: из строки в объект
        if isinstance(data, str):
            try:
                return self.get_queryset().get(slug=data)
            except Genre.DoesNotExist:
                raise serializers.ValidationError('Genre not found.')
        return super().to_internal_value(data)

    def to_representation(self, value):
        # Сериализация: из объекта в словарь
        return {
            'name': value.name,
            'slug': value.slug,
        }


class TitleSerializer(serializers.ModelSerializer):
    genre = CustomGenreField(many=True)
    category = CustomCategoryField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
        'id', 'name', 'year', 'rating', 'description', 'category', 'genre')
        read_only_field = ('id', 'rating')

    def get_rating(self, obj):
        return None

    def create(self, validated_data):
        genre_data = validated_data.pop('genre', [])

        if not isinstance(genre_data, list):
            raise serializers.ValidationError(
                'Genre must be a list.'
            )

        title = Title.objects.create(**validated_data)

        for genre in genre_data:
            TitleGenre.objects.create(
                genre=genre, title=title)
        return title
