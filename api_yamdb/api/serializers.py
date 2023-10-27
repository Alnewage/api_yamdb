from rest_framework import serializers

from reviews.models import Category, Genre, TitleGenre, Title, Review, Comment


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
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'category', 'genre')
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


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""

    author = serializers.StringRelatedField(read_only=True)
    title = serializers.SlugRelatedField(
        slug_field='id',
        many=False,
        read_only=True,
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
            'title',
        )

    def validate(self, data):
        """Запрещает пользователям оставлять повторные отзывы"""
        if not self.context.get('request').method == 'POST':
            return data
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение',
            )
        return data

    def validate_score(self, value):
        """Проверка, что оценка в диапазоне от 1 до 10."""
        if not 1 <= value <= 10:
            raise serializers.ValidationError('Оценка может быть от 1 до 10!')
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
    )

    class Meta:
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )
        model = Comment
