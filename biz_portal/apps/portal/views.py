from django.views import generic
from . import models


class BusinessView(generic.DetailView):
    model = models.Business
    template_name = 'portal/business.html'
