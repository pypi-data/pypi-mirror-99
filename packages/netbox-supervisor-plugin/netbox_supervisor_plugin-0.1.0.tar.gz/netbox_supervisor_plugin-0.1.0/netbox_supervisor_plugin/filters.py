import django_filters
from django.db.models import Q

from utilities.filters import NameSlugSearchFilterSet

from .models import Supervisor


class SupervisorFilter(NameSlugSearchFilterSet):
    q = django_filters.CharFilter(
        method="search",
        label="Поиск",
    )

    class Meta:
        model = Supervisor
        fields = [
            'status',
            'email',
            'comments',
        ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset

        qs_filter = (
            Q(sid__icontains=value)
            | Q(name__icontains=value)
            | Q(status__icontains=value)
            | Q(comments__icontains=value)
            | Q(email__icontains=value)
            | Q(phone__icontains=value)
        )

        return queryset.filter(qs_filter)