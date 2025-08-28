from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexTemplateView(
    LoginRequiredMixin,
    TemplateView
):
    template_name = 'home_template/pages/base.html'
