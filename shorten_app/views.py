from django.http import HttpResponseRedirect
from django.shortcuts import render
from hashids import Hashids
# Create your views here.
from django.views.generic import View, CreateView
from django.core.urlresolvers import reverse
from shorten_app.forms import UrlForm
from shorten_app.models import Url

class IndexView(View):
    def get(self, request):
        url_form = UrlForm()
        return render(request, 'index.html', {"form": url_form})

    def post(self, request):
        hashids = Hashids()
        form_instance = UrlForm(request.POST)
        if form_instance.is_valid():
            url_object = form_instance.save()
            hashid = hashids.encode(url_object.id)

            url_object.short_version = hashid
            url_object.save()

        return HttpResponseRedirect(reverse("index"))

class AllClick(IndexView):
    pass

class UserClick(CreateView):
    pass


def redirect(request, pk):
    print(pk)
    redirect_url_object = Url.objects.get(short_version=pk)
    redirect_url = redirect_url_object.url
    return HttpResponseRedirect(redirect_url)
