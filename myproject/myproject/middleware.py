"""
middleware.py

Custom middleware for user redirection and access control:
- Redirects authenticated users away from login/register pages
- Restricts unauthenticated users to allowed paths
"""

from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages

class UserRedirectMiddleware:
    # Middleware to manage user access and redirects.

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Redirect authenticated users away from login/register
        if request.user.is_authenticated:
            path_to_redirect = [reverse('blog:register'), reverse('blog:login')]
            if request.path in path_to_redirect:
                return redirect('blog:dashboard')
        else:
            # Allow unauthenticated users only on certain paths
            allowed_paths = [
                reverse('blog:index'),
                reverse('blog:about'),
                reverse('blog:login'),
                reverse('blog:register'),
                reverse('blog:forget_password'),
                reverse('blog:reset_password', kwargs={'uidb64': 'dummy_uid', 'token': 'dummy_token'})
            ]
            # Allow access to static files and admin
            if request.path.startswith('/media/') or request.path.startswith('/admin') or request.path.startswith('/reset_password'):
                return self.get_response(request)
            # Redirect if not allowed
            if request.path not in allowed_paths:
                messages.error(request, 'You must be logged in to access this page.')
                return redirect('blog:login')
            
        return self.get_response(request)