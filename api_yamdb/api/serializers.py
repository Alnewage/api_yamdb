from django.db.models import Avg
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


class CustomFieldMixin:
    """Миксин для десериализации и сериализации."""

    def get_queryset(self):
        """Метод должен быть переопределен в подклассах."""
        raise NotImplementedError(
            'Subclasses must implement get_queryset method.')

    def to_internal_value(self, data):
        # Десериализация: из строки в объект
        if isinstance(data, str):
            try:
                return self.get_queryset().get(slug=data)
            except self.get_queryset().model.DoesNotExist:
                raise serializers.ValidationError('Object not found.')
        return super().to_internal_value(data)

    def to_representation(self, value):
        # Сериализация: из объекта в словарь
        return {'name': value.name, 'slug': value.slug}


class CustomCategoryField(CustomFieldMixin, serializers.RelatedField):
    def get_queryset(self):
        return Category.objects.all()


class CustomGenreField(CustomFieldMixin, serializers.RelatedField):
    def get_queryset(self):
        return Genre.objects.all()


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title."""

    # Применяем кастомные модели, так как данные поля имеют разные типы
    # при сериализации и десериализации.
    genre = CustomGenreField(many=True)
    category = CustomCategoryField()

    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'category', 'genre')
        read_only_field = ('id', 'rating')

    @staticmethod
    def get_rating(obj):
        """Получение рейтинга."""
        if obj.reviews.exists():
            return obj.reviews.aggregate(Avg('score'))['score__avg']
        return None

    def create(self, validated_data):
        genre_data = validated_data.pop('genre', [])
        title = Title.objects.create(**validated_data)
        # Создание связей с жанрами (ManyToMany через промежуточную модель).
        for genre in genre_data:
            TitleGenre.objects.create(
                genre=genre, title=title)
        return title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""

    author = serializers.StringRelatedField(read_only=True)
    title = serializers.SlugRelatedField(slug_field='id',
                                         many=False,
                                         read_only=True, )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')

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
