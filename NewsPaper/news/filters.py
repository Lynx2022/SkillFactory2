from django_filters import FilterSet, ModelChoiceFilter, DateTimeFilter, CharFilter
from .models import Post, Category
from django.forms import DateTimeInput


class NewsFilter(FilterSet):
    added_after = DateTimeFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        label='Новость не ранее',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    categoryType = ModelChoiceFilter(
        field_name='categoryType',
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='все',
    )

    title_filter = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Заголовок содержит',
    )