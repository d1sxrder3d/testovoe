from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic import DetailView

from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView

from django.shortcuts import redirect, render
from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.urls import reverse_lazy

from .models import Ad, ExchangeProposal
from .forms import RegisterForm, AdForm, ExchangeProposalForm

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

class AdListView(ListView):
    model = Ad
    template_name = 'ads/ad_list.html'
    context_object_name = 'ads'
    paginate_by = 10

class MyAdsView(LoginRequiredMixin, ListView):
    template_name = 'ads/my_ads.html'
    context_object_name = 'ads'
    
    def get_queryset(self):
        return Ad.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        queryset = self.get_queryset()
        context = super().get_context_data(object_list=queryset, **kwargs)
        context['ads'] = queryset  # Добавляем 'ads' в контекст
        context['form'] = AdForm()
        return context
    
    def get_template_names(self):
        return ['ads/my_ads.html']

    def post(self, request, *args, **kwargs):
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('ad_list')
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)
    


class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad
    fields = ['title', 'description', 'image_url', 'category', 'condition']
    template_name = 'ads/ad_form.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class AdDetailView(DetailView):
    model = Ad
    template_name = 'ads/ad_detail.html'
    context_object_name = 'ad'



class AdUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ad
    form_class = AdForm  
    template_name = 'ads/ad_form.html'
    
    def test_func(self):
        ad = self.get_object()
        return self.request.user == ad.user

class AdDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ad
    template_name = 'ads/ad_confirm_delete.html'
    success_url = reverse_lazy('my_ads')
    
    def test_func(self):
        ad = self.get_object()
        return self.request.user == ad.user

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

class MyExchangesView(LoginRequiredMixin, ListView):
    template_name = 'ads/my_exchanges.html'
    
    def get_queryset(self):
        return ExchangeProposal.objects.filter(
            Q(sender=self.request.user) | Q(receiver=self.request.user)
        )
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sent_proposals'] = ExchangeProposal.objects.filter(sender=self.request.user)
        context['received_proposals'] = ExchangeProposal.objects.filter(receiver=self.request.user)
        return context

class CreateExchangeView(LoginRequiredMixin, CreateView):
    model = ExchangeProposal
    form_class = ExchangeProposalForm
    template_name = 'ads/create_exchange.html'
    
    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.instance.sender_ad = Ad.objects.get(id=self.kwargs['ad_id'])
        form.instance.receiver = form.instance.receiver_ad.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('my_exchanges')

class AcceptExchangeView(LoginRequiredMixin, UpdateView):
    model = ExchangeProposal
    fields = []
    template_name = 'ads/confirm_exchange.html'
    
    def form_valid(self, form):
        if self.object.receiver == self.request.user:
            self.object.status = 'accepted'
            self.object.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('my_exchanges')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('ad_list')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('ad_list')