from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, View
from .models import TransactionModel
from .forms import DepositForm, BorrowForm
from .constants import DEPOSIT, RETURN, PENDING, COMPLETED
from django.contrib import messages
from django.urls import reverse_lazy
from flowers.models import FlowerModel
from django.shortcuts import render, redirect
from email_system.utils.email import send_transaction_emails
from django.db.models import Q

# Create your views here.


class TransactionViewMixin(LoginRequiredMixin, CreateView):
    template_name = "transactions/transaction_form.html"
    success_url = reverse_lazy("home")

    model = TransactionModel
    title = ""

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'customer': self.request.user.customer
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title
        })
        return context


class DepositView(TransactionViewMixin):
    form_class = DepositForm
    title = "Deposit"

    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        customer = self.request.user.customer

        customer.balance += amount

        customer.save(
            update_fields=['balance']
        )

        send_transaction_emails(
            self.request.user,
            self.request.user.email,
            f"Balance Deposited Customer ID : {customer.customer_id}",
            f"""Your deposit request for ${amount} has successfully completed. After deposit your total amount is {customer.balance}""")

        messages.success(self.request, f"""{"{:,.2f}".format(
            float(amount))}$ was deposited to your account successfully""")

        return super().form_valid(form)


class BorrowView(TransactionViewMixin):
    form_class = BorrowForm
    title = "Buy flower"

    def get_initial(self):
        id = self.kwargs['id']
        flower = FlowerModel.objects.get(id=id)
        initial = {'transaction_type': PENDING,
                   'flower': flower, 'amount': flower.borrowing_price}
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs['id']
        flower = FlowerModel.objects.get(id=id)
        context.update({
            'flower': flower,
            'isBookView': True
        })
        return context

    def form_valid(self, form):
        customer = self.request.user.customer
        id = self.kwargs['id']
        flower = FlowerModel.objects.get(id=id)
        # Get the amount from the form
        if flower.quantity <= 0:
            messages.error(self.request, "Sorry this flower is not available")
            return redirect("profile")
        
        amount = flower.borrowing_price
        flower.quantity = flower.quantity - 1
        flower.save(update_fields=['quantity'])

        
        if customer.balance < amount:
            messages.error(self.request, "You don't have sufficient money")
            return redirect("profile")

        customer.balance -= amount

        customer.save(
            update_fields=['balance']
        )

        send_transaction_emails(
            self.request.user,
            self.request.user.email,
            f"One flower has been borrowed by Customer : {customer.customer_id}",
            f"""You have successfully borrowed this flower : ({flower.title}) cost of : ${amount}""")

        messages.success(self.request, f""" flower has been borrowed and your current balance is ${
                         customer.balance} """)

        return super().form_valid(form)


class ReturnBookView(LoginRequiredMixin, View):
    def get(self, request, id):
        transaction = get_object_or_404(TransactionModel, pk=id)

        transaction.transaction_type = RETURN
        customer = self.request.user.customer
        customer.balance += transaction.amount
        customer.save()
        transaction.save()

        messages.success(
            self.request,
            f"""The flower {transaction.flower.title} has been returned,and your balance has been refunded by ${transaction.amount}."""
        )

        send_transaction_emails(
            self.request.user,
            self.request.user.email,
            f"""Thanks for returning the flower by Customer ID : {
                customer.customer_id}""",
            f"""Your flower amount ${transaction.amount} has been refunded""")

        return redirect("profile")



class OrderHistoryView(LoginRequiredMixin, View):
    template_name = "transactions/order_history.html"

    def get(self, request):
        borrows = TransactionModel.objects.filter(
            Q(customer=self.request.user.customer, transaction_type=PENDING) |
            Q(customer=self.request.user.customer, transaction_type=COMPLETED)
        )
        return render(request, self.template_name, {"borrows": borrows})

  