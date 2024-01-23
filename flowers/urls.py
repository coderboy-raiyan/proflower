from django.urls import path
from .views import BookDetailsView, BookReviewView, OurServicesView

urlpatterns = [
    path("our-services/", OurServicesView.as_view(), name="our_services"),
    path("book/<int:id>", BookDetailsView.as_view(), name="book_details"),
    path("review/<int:id>", BookReviewView.as_view(), name="review_book"),
]
