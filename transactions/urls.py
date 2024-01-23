from django.urls import path
from .views import DepositView, BorrowView, ReturnBookView, OrderHistoryView

urlpatterns = [
    path("order-history/", OrderHistoryView.as_view(), name="order_history"),
    path("deposit/", DepositView.as_view(), name="deposit"),
    path("borrow/<int:id>", BorrowView.as_view(), name="borrow"),
    path("return/<int:id>", ReturnBookView.as_view(), name="return")
]
