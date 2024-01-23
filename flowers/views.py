from typing import Any
from django.views.generic import DetailView, CreateView, View, TemplateView
from .models import FlowerModel, ReviewModel
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ReviewForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from .models import ReviewModel

# Create your views here.


class BookDetailsView(DetailView):
    template_name = "books/book_details.html"
    model = FlowerModel
    pk_url_kwarg = "id"
    context_object_name = "flower"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs['id']
        flower = FlowerModel.objects.get(pk=id)
        reviews = ReviewModel.objects.filter(flower=flower)
        context.update({
            'reviews': reviews
        })
        return context

# def returnBook(request, id) :
#     transaction = TransactionModel.objects.get(pk=id)


class BookReviewView(LoginRequiredMixin, CreateView):
    template_name = "books/book_review.html"
    model = ReviewModel
    form_class = ReviewForm
    success_url = reverse_lazy("profile")

    def get_initial(self):
        id = self.kwargs['id']
        flower = FlowerModel.objects.get(pk=id)
        initial = {'flower': flower, 'user': self.request.user}
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs['id']
        flower = FlowerModel.objects.get(pk=id)
        context.update({
            'flower': FlowerModel
        })
        return context

    def form_valid(self, form):
        id = self.kwargs['id']
        flower = FlowerModel.objects.get(pk=id)
        isAlreadyReviewed = ReviewModel.objects.filter(
            flower=flower, user=self.request.user).count()
        if isAlreadyReviewed >= 1:
            messages.info(self.request, "You have already reviewed this book.")
            return redirect("profile")
        else:
            messages.success(self.request, "Thanks for your valuable Reviews")
        return super().form_valid(form)



services = [
    {
        "title"  : "Sympathy",
        "image" : "https://images.ctfassets.net/ztm44xofsurz/6EYaJiXQeeQqPzE0emv8HS/fd75531be1f5e25f78ead017b07bbac3/4492_PF_Summer23_June_Sympathy_CategoryTile.jpg?w=384&fm=webp&q=70",
    },
    {
        "title"  : "Birthday",
        "image" : "https://images.ctfassets.net/ztm44xofsurz/1i5dX5yARLOPyL4I9vPm1q/53f8e6f1f72a334d1aeff0adf864f502/4492_PF_Summer23_June_Baby_CategoryTile.jpg?w=384&fm=webp&q=70",
    },
    {
        "title"  : "Get Well",
        "image" : "https://images.ctfassets.net/ztm44xofsurz/4SWUq35GNDKsjpe0lNhHQu/557e3bb7bbb781bd4df06a7a1706c422/4492_PF_Summer23_June_ThinkingOfYou_CategoryTile.jpg?w=384&fm=webp&q=70",
    },
    {
        "title"  : "Just because",
        "image" : "https://images.ctfassets.net/ztm44xofsurz/4OPuA4FYgCg3gDkVWLujq0/3599c5376ff23c3b5d9e5dca70bd1ffb/4492_PF_Summer23_June_Birthday_CategoryTile.jpg?w=384&fm=webp&q=70",
    },
]

class OurServicesView(TemplateView):
    template_name = "books/services.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'services': services
        })
        return context