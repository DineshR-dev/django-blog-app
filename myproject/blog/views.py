"""
views.py

Main view logic for the blog app:
- Handles user authentication (register, login, logout, password reset)
- Manages blog post CRUD operations
- Renders dashboard and other pages
"""

from django.shortcuts import render,get_object_or_404
from .models import Post
from .forms import RegisterForm,LoginForm,PostForm,forgetPasswordForm,resetForm
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.core.paginator import Paginator
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User,Group

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail

def index(request):
    # Display published blog posts with pagination.
    post = Post.objects.filter(is_published=True)
    items_per_page = 5
    page_num = request.GET.get("page")
    paginator_obj = Paginator(post,items_per_page)
    post = paginator_obj.get_page(page_num) 
    page_data = {
        'post_list' : post 
    }
    return render(request,'blog/index.html',page_data)

@permission_required('blog.view_post', raise_exception=True)
def details(request,slug):
    # Display full blog post
    post = Post.objects.get(slug=slug)
    releted_post = Post.objects.filter(category=post.category,is_published=True).exclude(pk=post.id)[:3]
    page_data = {
        'post' : post,
        'releted_post' : releted_post 
    }
    return render(request, "blog/details.html",page_data)

def about(request):
    # Render the About page.
    return render(request, "blog/about.html")
    
def register(request):
    # Handle user registration.
    form = RegisterForm()
    if request.method=='POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # set default permission(Readers) for new user
            reader,created = Group.objects.get_or_create(name="Readers")
            user.groups.add(reader)
            messages.success(request, "Registration successfull! Please log in.")
            return redirect('blog:login')
        
    page_data = {
        'form' : form,
    }
    return render(request, "blog/register.html",page_data)

def login(request):
    # Authenticate and log in a user.
    form = LoginForm()
    if request.method=="POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            if user:
                auth_login(request,user)
                messages.success(request, "Login Successfully.")
                return redirect('blog:dashboard')
            else:
                messages.error(request, "Invalid username or password.")
    
    page_data = {
        'form' : form,
    }
    return render(request, "blog/login.html",page_data)

def forget_password(request):
    # Send password reset email to user.
    form = forgetPasswordForm()
    if request.method=="POST":
        form = forgetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            domain = current_site.domain
            subject = "Reset Password Request"
            
            # Render email template with reset link
            message = render_to_string("blog/reset_password_email.html",{
                'domain':domain,
                'uid':uid,
                'token':token,
            })
            # Send email with reset link
            send_mail(subject,message,'noreply@example.com',[email])
            messages.success(request, "Email has been sent")
        else:
            messages.error(request, "Email not found")
            
    page_data = {
        'form' : form,
    }
    return render(request, "blog/forget_password.html",page_data)

def reset_password(request,uidb64,token):
    # Reset user password using token from email.
    form = resetForm()
    if request.method=="POST":
        form = resetForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['password']
            try:
                uid = urlsafe_base64_decode(uidb64).decode()
                user = User.objects.get(pk=uid)
            except Exception as E:
                user= None
            if user and default_token_generator.check_token(user,token):
                user.set_password(new_password)
                user.save()
                messages.success(request,"Reset Password Successfully")
                return redirect("blog:login")
            else:
                messages.error(request,"Password Reset link is invalid")
                return redirect("blog:login")
            
    page_data = {
        'form' : form,
    }
    return render(request, "blog/reset_password.html",page_data)

@permission_required('blog.add_post', raise_exception=True)
def dashboard(request):
    # Show dashboard with user's posts or all posts if permitted.

    # Editors can see all posts, while authors see their own.
    if request.user.has_perm('blog.can_publish'):
        post = Post.objects.all()
    else:
        post = Post.objects.filter(user=request.user)

    items_per_page = 5
    page_num = request.GET.get("page")
    paginator_obj = Paginator(post,items_per_page)
    post = paginator_obj.get_page(page_num) 
    page_data = {
        'post_list' : post,
    }
    return render(request, "blog/dashboard.html",page_data)

def logout(request):
    # Log out the current user.
    auth_logout(request)
    return redirect("blog:index")

@permission_required('blog.add_post', raise_exception=True)
def new_post(request):
    # Create a new blog post.
    form = PostForm()
    if request.method=="POST":
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "Post Added Successfully.")
            return redirect("blog:dashboard")
        
    page_data = {
        'form' : form,
    }
    return render(request, "blog/new_post.html",page_data)

@permission_required('blog.change_post', raise_exception=True)
def edit_post(request,post_id):
    # Edit an existing blog post.
    post = get_object_or_404(Post,id=post_id)

    # Authors can only edit their own posts, editors can edit any post
    if not request.user.groups.filter(name='Editors').exists():
        if request.user != post.user:
            messages.error(request, "Author can't modify other posts.")
            return redirect("blog:dashboard")
        
    form = PostForm(instance=post)
    if request.method=="POST":
        form = PostForm(request.POST,request.FILES,instance=post)
        if form.is_valid():
            form.save()
            messages.success(request,"Post Updated Successfully")
            return redirect("blog:dashboard")
    
    page_data = {
        'form' : form,
    }
    return render(request, "blog/edit_post.html",page_data)

@permission_required('blog.delete_post', raise_exception=True)
def delete_post(request,post_id):
    # Delete a blog post.
    post = get_object_or_404(Post,id=post_id)
    if not request.user.groups.filter(name='Editors').exists():
        if request.user != post.user:
            messages.error(request, "Author can't modify other posts.")
            return redirect("blog:dashboard")
        
    post.delete()
    messages.success(request,"Post Deleted successfully")
    return redirect('blog:dashboard')

@permission_required('blog.can_publish', raise_exception=True)
def publish_post(request,post_id):
    # Toggle publish status of a blog post. 
    post = get_object_or_404(Post,id=post_id)
    new_status = not post.is_published
    post.is_published = new_status
    post.save()
    if new_status:
        messages.success(request, "Blog Published successfully")
    else:
        messages.success(request, "Blog hidden successfully")
        
    return redirect('blog:dashboard')