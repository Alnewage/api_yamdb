from datetime import datetime

from rest_framework import serializers

from reviews.models import Category, Genre, GenreTitle, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre

    # def to_internal_value(self, data):
    #     if isinstance(data, str):
    #         if not Genre.objects.filter(slug=data).exists():
    #             raise serializers.ValidationError(
    #                 'There is no such genre.'
    #             )
    #         return Genre.objects.get(slug=data)
    #     return super().to_internal_value(data)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category

    # def to_internal_value(self, data):
    #     if isinstance(data, str):
    #         if not Category.objects.filter(slug=data).exists():
    #             raise serializers.ValidationError(
    #                 'There is no such category.'
    #             )
    #         return Category.objects.get(slug=data)
    #     return super().to_internal_value(data)


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all(),
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'category', 'genre')
        model = Title
        read_only_field = ('id', 'rating')

    def get_rating(self, obj):
        titles = Genre.objects.all()
        x = 0
        for object in titles:
            x += object.id
        x = x / titles.count()
        return x

    def validate(self, data):
        if not 1888 < data['year'] < datetime.now().year:
            raise serializers.ValidationError(
                'Year must be greater than 1888.'
            )
        return data

    def create(self, validated_data):
        genre_data = validated_data.pop('genre', [])

        if not isinstance(genre_data, list):
            raise serializers.ValidationError(
                'Genre must be a list.'
            )

        title = Title.objects.create(**validated_data)

        for genre in genre_data:
            GenreTitle.objects.create(
                genre=genre, title=title)
        return title
