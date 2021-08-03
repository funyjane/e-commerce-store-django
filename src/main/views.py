from django.shortcuts import render
from django.views.generic import TemplateView
from constance import config


class IndexPageView(TemplateView):
    template_name = "pages/index.html"
    turn_on_block = config.MAINTENANCE_MODE
    extra_context = {"maintenance": turn_on_block}
