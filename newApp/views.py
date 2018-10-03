from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views import View
from .forms import BlogForm
from .models import BlogModel
from django.contrib import messages
import datetime
# Create your views here.

def hello(request):
    return HttpResponse("Hello world!")

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
        # This will return an array of one blog or none
        blog = BlogModel.objects.get(id=id)
        form = BlogForm(request.POST, instance = blog)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, "Blog updated")
            return HttpResponseRedirect(reverse("home"))
        return HttpResponse('Pieleen meni')
        # blogs = BlogModel.objects.filter(id=id)
        # if len(blogs) > 0:
        #     blog = blogs[0]
        # else:
        #     messages.add_message(request, messages.INFO, "Invalid blog id")
        #     return HttpResponseRedirect(reverse("home"))
        # body = request.POST.get("body")
        # title = request.POST.get("title")
        # blog.title = title
        # blog.body = body
        # blog.save()


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
            blog = BlogModel(title=blog_t, timestamp=datetime.datetime.now(), body=blog_b)
            blog.save()
            return HttpResponse('Added ')
