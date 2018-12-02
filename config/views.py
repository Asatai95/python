from django.http import HttpResponse
from django.views.generic import CreateView, ListView
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse
from django.contrib.auth.decorators import login_required

class IndexView(View):

	def get(self, request, *args, **kwargs):

		return render(request, 'index.html')

Index = IndexView.as_view()
