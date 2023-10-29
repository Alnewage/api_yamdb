from django.db.models import Avg
from django.utils import timezone
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CustomRelatedField(serializers.SlugRelatedField):
    """Кастомный сериализатор для моделей Genre и Category."""

    def __init__(self, model, *args, **kwargs):
        kwargs['slug_field'] = 'slug'
        self.model = model
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all()

    def to_representation(self, value):
        # Сериализация: из объекта в словарь
        return {'name': value.name, 'slug': value.slug}


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title."""

    # Применяем кастомную модель, так как данные поля имеют разные типы
    # при сериализации и десериализации.
    genre = CustomRelatedField(model=Genre, many=True)
    category = CustomRelatedField(model=Category)
    rating = serializers.FloatField(source='avg_rating', read_only=True,
                                    allow_null=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        read_only_field = ('id',)

    @staticmethod
    def validate_year(value):
        # Проверяем, что год произведения не больше текущего.
        if value > timezone.now().year:
            raise serializers.ValidationError(
                'Year must be less than current year.')
        return value

    def create(self, validated_data):
        genre_data = validated_data.pop('genre', [])
        title = super().create(validated_data)
        # Установка связей с жанрами (ManyToMany через промежуточную модель)
        title.genre.set(genre_data)
        return title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""

    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        # Проверяем, что метод запроса является POST
        if self.context['request'].method != 'POST':
            return data

        # Получаем автора и идентификатор произведения из контекста запроса
        author = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')

        # Проверяем, существует ли отзыв с таким автором и идентификатором
        # произведения.
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение')

        return data

    @staticmethod
    def validate_score(value):
        """Проверка, что оценка в диапазоне от 1 до 10."""
        if not 1 <= value <= 10:
            raise serializers.ValidationError('Score must be in range 1..10.')
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
