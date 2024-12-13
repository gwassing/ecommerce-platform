from django.views.generic import CreateView
from django.contrib.auth import login
from accounts.forms import CustomUserCreationForm
from django.urls import reverse_lazy


class RegistrationView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("index")
    template_name = "registration/registration.html"

    def form_valid(self, form):
        if form.is_valid():
            response = super().form_valid(form)
            login(self.request, self.object)
            return response
