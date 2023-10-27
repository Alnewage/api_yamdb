import django_filters


class TitleFilter(django_filters.FilterSet):
    """
    Фильтр для модели Title.
        Вынесли в отдельный класс, так как фильтрование по полю genre связанной
        модели с ManyToMany не поддерживается атрибутом filterset_fields.
    """
    genre = django_filters.CharFilter(field_name='genre__slug')
    category = django_filters.CharFilter(field_name='category__slug')
    name = django_filters.CharFilter(field_name='name')
    year = django_filters.NumberFilter(field_name='year')
