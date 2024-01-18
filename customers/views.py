from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.urls import reverse_lazy
from .forms import UserSignUpForm, UserUpdateForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.views.generic import View
from transactions.models import TransactionModel
from transactions.constants import PENDING, COMPLETED
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from email_system.utils.email import send_transaction_emails
from .models import TokenModel
from django.contrib.auth.models import User

class UserSignUpView(FormView):
    template_name = "customers/signup.html"
    success_url = reverse_lazy("home")
    form_class = UserSignUpForm

    def form_valid(self, form):
        user = form.save()
   
        # login(self.request, user)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        TokenModel.objects.create(
            token = token,
            user = user
        )
        confirm_link = f"https://flower-sell.onrender.com/customers/activate/{uid}/{token}"
        send_transaction_emails({"first_name": user.first_name, "last_name": user.last_name},user.email, "Please verify your email to activate your account", f"Thanks for creating an account on our platform. click the below link to verify your account {confirm_link}")
        messages.success(self.request, "Please check your email and verify")
        return super().form_valid(form)


class UserSignInView(LoginView):
    template_name = "customers/signin.html"

    def get_success_url(self):
        messages.success(self.request, "Signed in successfully")
        return reverse_lazy("home")


# class UserLogoutView(LogoutView):
#     def get_success_url(self):
#         messages.success(self.request, "Logged out successfully")
#         return reverse_lazy("home")

def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("home")



class UserProfileView(LoginRequiredMixin, View):
    template_name = "customers/profile.html"

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        borrows = TransactionModel.objects.filter(customer=self.request.user.customer)
        return render(request, self.template_name, {"form": form, "borrows": borrows})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(self.request, "Profile updated Successfully")
            return redirect("profile")
        return render(request, self.template_name, {"form": form})



def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        find_token = TokenModel.objects.get(token=token)
        find_token.delete()


        return redirect("signin")
    
    else :
        return redirect("signup")