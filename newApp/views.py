from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views import View
from .forms import BlogForm
from .models import BlogModel
import datetime
# Create your views here.

def hello(request):
    return HttpResponse("Hello world!")

def test(request):
    return HttpResponse("Testing testing!")

def show_all_data(request):
    try:
        blogs = BlogModel.objects.all()
    except Exception:
        return HttpResponse("Not found")
    return render(request, "show.html", {"blogs": blogs})

class EditBlogView(View):
    def get(self, request, id):
        b = get_object_or_404(BlogModel, id=id)
        return render(request, "edit.html", {"blog": b})

    def post(self, request, id):
        b = get_object_or_404(BlogModel, id=id)
        # b.title = request.POST["title"]
        # b.body = request.POST["body"]
        b.save()
        return render(request, "show.html", {"blogs": blogs})

class Blog(View):
    def get(self, request):
        form = BlogForm()
        return render(request, "forms.html", {"form": form})

    def post(self, request):
        form = BlogForm(request.POST)
        if(form.is_valid()):
            cd = form.cleaned_data
            blog_t = cd['title']
            blog_b = cd['body']
            print(blog_t)
            blog = BlogModel(title=blog_t, timestamp=datetime.datetime.now(), body=blog_b)
            blog.save()
            return HttpResponse('Added')
