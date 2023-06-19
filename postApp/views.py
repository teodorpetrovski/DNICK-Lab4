from django.shortcuts import render, redirect
from postApp.forms import PostForm, FileForm
from postApp.models import BlockedUser, Post, Author, Interest, Skill


# Create your views here.

def posts(request):
    blocked_from=BlockedUser.objects.filter(blocking_user__user=request.user).values_list("blocked_user__user",flat=True)
    postSet=Post.objects.exclude(author__user__in = blocked_from).exclude(author__user=request.user).all()

    return render(request,"posts.html",{"posts":postSet})

def add(request):
    if request.method == "POST":
        form_data_post=PostForm(data=request.POST,files=request.FILES)
        form_data_files=FileForm(data=request.POST,files=request.FILES)
        if form_data_post.is_valid() and form_data_files.is_valid():
            post=form_data_post.save(commit=False)
            post.author=Author.objects.get(user=request.user)
            file=form_data_files.save(commit=False)
            file.post=post
            post.save()
            file.save()

            return redirect("posts")


    return render(request,"add.html",{"formPost":PostForm,"formFile":FileForm})

def profile(request):
    author=Author.objects.get(user=request.user)
    posts=Post.objects.filter(author=author).all()
    interests=Interest.objects.filter(author=author).all()
    skills=Skill.objects.filter(author=author).all()
    return render(request,"profile.html",{"author":author,"posts":posts,"interests":interests,"skills":skills})

def blocked(request):
    blocked_list=BlockedUser.objects.filter(blocking_user__user=request.user).all()
    excludeUsers=BlockedUser.objects.filter(blocking_user__user=request.user).values_list("blocked_user__user",flat=True)
    authors=Author.objects.exclude(user__in=excludeUsers).exclude(user=request.user)
    if request.method == "POST":
        blockedUser=Author.objects.get(user__username=request.POST["username"])
        author=Author.objects.get(user=request.user)
        block=BlockedUser(
            blocked_user=blockedUser,
            blocking_user=author
        )
        block.save()
        return redirect('blocked')
    return render(request,"blockList.html",{"blocked_list":blocked_list,"authors":authors})
