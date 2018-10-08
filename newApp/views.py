from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views import View
from .forms import BlogForm, CopyOfForm, UserCreationForm
from .models import BlogModel, User
from django.contrib import messages
import datetime
# Create your views here.

def hello(request):
    return HttpResponse("Hello world!")


def show_all_data(request):
    try:
        blogs = BlogModel.objects.order_by('-timestamp')
    except Exception:
        return HttpResponse("Lopeta heti paikalla")
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
        return HttpResponse('Error')


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
            form = CopyOfForm({"c_title": blog_t, "c_body": blog_b})
            return render(request, "confirmation.html", {"form": form})
            #Sessions:
            # request.session('blog_t') = blog_t
            # request.session('blog_b') = blog_b


def saveBlog(request):
    option = request.POST.get('option', 'no')
    if option == 'yes':
        title = request.POST.get('c_title', '')
        body = request.POST.get('c_body', '')
        blog = BlogModel(title=title, timestamp=datetime.datetime.now(), body=body)
        blog.save()
        return HttpResponseRedirect(reverse("home"))
    else:
        messages.add_message(request, messages.INFO, "Whatever")
        return HttpResponseRedirect(reverse("save_form"))


class registerUser(View):
    def get(self, request):
        form= UserCreationForm()
        return render(request, "registration.html", {"form": form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if(form.is_valid()):
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.clean_password2['password']
            new_user = User(username= username,email= email, password = password, timestamp = datetime.datetime.now())
            new_user.save()
            messages.add_message(request, messages.INFO, "New user created")
            return HttpResponseRedirect(reverse("home"))
        else:
            form = UserCreationForm(request.POST)
            return render(request, "registration.html", {"form": form})
