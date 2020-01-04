from django.shortcuts import render, HttpResponse, redirect,get_object_or_404, reverse
from .forms import ArticleForm,FormNologin
from .models import Article, Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# from ckeditor.fields import RichTextField
from django import forms


# Create your views here.

def articles(request):
    keyword = request.GET.get("keyword")

    if keyword:
        articles = Article.objects.filter(title__contains = keyword)
        return render(request, "articles.html", {"articles":articles})

    articles = Article.objects.all()

    return render(request, "articles.html", {"articles": articles})


def index(request):
    form = ArticleForm(request.POST or None, request.FILES or None)
    
    if request.user.is_authenticated:
        notes = Article.objects.filter(author = request.user)
        # articles = get_object_or_404(Article,author=request.user)  

        # count = User.objects.count()
        context = {
            "notes": notes,
            # "count": count,
            "form" : form
        }
        return render(request,"index.html", context)
    else:
        context = {
            # "count": count,
            "form" : form
        }
        return render(request,"index.html", context)


def about(request):
    return render(request, "about.html")

@login_required(login_url = "user:login")        # user disinda birinin linklere girmesiyle yonlendirilecek sayfa icin
def dashboard(request):
    articles = Article.objects.filter(author = request.user)
    context = {
        "articles": articles
    }
    return render(request, "dashboard.html", context)

@login_required(login_url = "user:login")
def addarticle(request):
    form = ArticleForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user

        article.save()

        messages.success(request, "Article successfully created.")
        return redirect("/")

    return render(request, "addarticle.html", {"form": form})

def detail(request, id):
    #article = Article.objects.filter(id = id).first()
    article = get_object_or_404(Article,id=id)
    
    comments = article.comments.all()
    return render(request, "detail.html", {"article": article, "comments":comments})

@login_required(login_url = "user:login")
def updateArticle(request, id):
    article = get_object_or_404(Article, id= id)
    form = ArticleForm(request.POST or None, request.FILES or None, instance=article)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()

        messages.success(request, "Article successfully updated.")
        return redirect("/")            # article altindaki dashboard url sine git demek istiyoruz

    return render(request, "update.html", {"form":form})

@login_required(login_url = "user:login")
def deleteArticle(request, id):
    article = get_object_or_404(Article, id= id)

    article.delete()

    messages.success(request, "Article successfully deleted.")

    return redirect("/")            # article altindaki dashboard url sine git demek istiyoruz


def addComment(request, id):
    article = get_object_or_404(Article, id=id)

    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")

        newComment = Comment(comment_author= comment_author, comment_content= comment_content)

        newComment.article = article
        newComment.save()

    return redirect(reverse("article:detail",kwargs={"id":id}))


def nologin(request):

    form = ArticleForm(request.POST or None, request.FILES or None)
    
    if form.is_valid():
        title = form.cleaned_data['title']
        content =form.cleaned_data['content'] 
        article_image = form.cleaned_data['article_image']              
        args ={"title":title, "content":content, "form": form,"article_image":article_image}                
        return render(request,"index.html", {"args":args})
        # return redirect("/", {"args":args})
    
    # return render(request,"index.html",{"form": form})
    return redirect("/")
        


