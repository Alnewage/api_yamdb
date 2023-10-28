from reviews.models import Title, Category, Genre
from rest_framework import serializers
from datetime import date


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    # category = serializers.SlugRelatedField(
    #     slug_field='slug', queryset=Category.objects.all()
    # )
    # genre = serializers.SlugRelatedField(
    #     slug_field='slug', queryset=Genre.objects.all(), many=True
    # )
    category = CategorySerializer(read_only=True,)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')
        model = Title
        read_only_field = ('rating', 'id',)
    
    def validate(self, data):
        if data['year'] > date.today().year:
            raise serializers.ValidationError('wrong year')
        return data

    def get_rating(self, obj):
        titles = Genre.objects.all()
        x = 0
        for object in titles:
            x += object.id
        x = x / titles.count()
        return None



# class TitleReadSerializer(serializers.ModelSerializer):
#     category = serializers.SlugRelatedField(
#         slug_field='name', queryset=Category.objects.all()
#     )
#     genre = serializers.SlugRelatedField(
#         slug_field='name', queryset=Genre.objects.all(), many=True
#     )
#     rating = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         fields = ('name', 'year', 'rating', 'description', 'category', 'genre')
#         model = Title
#         read_only_field = 'rating'
    
#     def validate(self, data):
#         if data['year'] > date.today().year:
#             raise serializers.ValidationError('wrong year')
#         return data

#     def get_rating(self, obj):
#         titles = Genre.objects.all()
#         x = 0
#         for object in titles:
#             x += object.id
#         x = x / titles.count()
#         return x