from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from .models import CustomUser
from .forms import UserRegisterForm, UserProfileForm

# IMPORTA IL MODELLO ORDER DAL MAGAzzINO
from store.models import Order

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Benvenuto, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Credenziali non valide.')
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'Hai effettuato il logout.')
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.role = 'customer'
            user.save()
            login(request, user)
            messages.success(request, 'Registrazione completata!')
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Class-Based View (CBV) per l'aggiornamento del profilo utente.
    Soddisfa il requisito ministeriale di avere almeno una CBV nel progetto.
    """
    model = CustomUser
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        # Garantisce che l'utente possa modificare solo ed esclusivamente il PROPRIO profilo
        return self.request.user

    # --- NUOVA FUNZIONE AGGIUNTA PER PASSARE GLI ORDINI AL TEMPLATE ---
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Recupera tutti gli ordini dell'utente dal più recente al più vecchio
        context['orders'] = Order.objects.filter(customer=self.request.user).order_by('-created_at')
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Profilo aggiornato!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Errore nella compilazione del modulo.')
        return super().form_invalid(form)