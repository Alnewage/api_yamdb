from reviews.models import Title, Category, Genre
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre

class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='name', queryset=Genre.objects.all(), many=True
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ('name', 'year', 'rating', 'description', 'category', 'genre')
        model = Title
        read_only_field = 'rating'

    def get_rating(self, obj):
        titles = Genre.objects.all()
        x = 0
        for object in titles:
            x += object.id
        x = x / titles.count()
        return x
