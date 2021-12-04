from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.generic import ListView, UpdateView, DetailView, CreateView, FormView, TemplateView, RedirectView
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from authentication.forms import RegistrationForm, UserProfileForm, InvoiceForm
from authentication.models import Invoice, Item
from django.urls import reverse, reverse_lazy

from django.contrib.auth import get_user_model

from authentication.utils import send_email

User = get_user_model()

class SignUpView(FormView):
    form_class = RegistrationForm
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        user = form.save(False)
        user.set_password(form.cleaned_data.get('password1'))
        user.is_active = True
        user.save()

        user = authenticate(username=user.email, password=form.data['password1'])
        login(self.request, user)
        return HttpResponseRedirect(reverse('authentication:home'))

class ProfileView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):

        return render(request, 'registration/profile.html')


class EditUserProfileView(LoginRequiredMixin, UpdateView): #Note that we are using UpdateView and not FormView
    model = User
    form_class = UserProfileForm
    template_name = "registration/profile.html"

    def get_object(self, *args, **kwargs):

        user = get_object_or_404(User, pk=self.request.user.pk)

        # We can also get user object using self.request.user  but that doesnt work
        # for other models.

        return user

    def get_success_url(self, *args, **kwargs):
        return reverse("authentication:profile")


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'deshboard.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.user.is_manager:
            data['invoices_count'] = Invoice.objects.all().count()
        else:   
            data['invoices_count'] = Invoice.objects.filter(user=self.request.user).count()
        return data


class InvoiceView(LoginRequiredMixin, CreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'authentication/invoice_create.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            invoice = form.save(False)
            invoice.user = request.user
            invoice.save()

            #Send invoice detail with manager
            context = {}
            context['agent_email'] = invoice.user.email
            context['invoice_id'] = invoice.id
            context['invoice_number'] = invoice.invoice_number

            for manager in User.objects.filter(is_manager=True, is_active=True):
                context['manager_name'] = manager.get_full_name()
                send_email(context, 'email/invoice_detail_email.html', 'email/invoice_detail_email.txt', "New invoice Notification", manager.email)

            # return HttpResponseRedirect(reverse_lazy('authentication:invoice_detail', args=[invoce.id]))
            return HttpResponseRedirect(reverse_lazy('authentication:invoice_list'))

        return render(request, 'authentication/invoice_create.html', {'form': form})

class InvoiceListView(LoginRequiredMixin, ListView):
    queryset = Invoice.objects.all()
    model = Invoice
    template_name = 'authentication/invoice_list.html'

    def get_queryset(self):
        """
        Return the list of items for this view.
        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        if self.request.user.is_manager:
            """If user is manager then return all invoices"""
            return self.queryset 
        else:
            """If user is agent then return only our invoices"""
            self.queryset = self.queryset.filter(user = self.request.user)
            return self.queryset


class InvoiceDetailView(LoginRequiredMixin, DetailView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'authentication/invoice_detail.html'