from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from flowers.models import FlowerModel, CategoryModel
# Create your views here.


class Home(ListView):
    template_name = "home.html"
    context_object_name = "flowers"
    model = FlowerModel

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.kwargs:
            slug = self.kwargs['flower_slug']
            category = CategoryModel.objects.get(slug=slug)
            queryset = super().get_queryset().filter(categories=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = CategoryModel.objects.all()
        context.update({
            "categories": categories
        })

        return context
