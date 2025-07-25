"""
forms.py

Defines all Django forms for the blog app:
- User registration and login
- Blog post creation/editing
- Password reset and forgot password forms
"""

from django import forms
from django.contrib.auth.models import User
from .models import Category, Post
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator

class RegisterForm(forms.ModelForm):
    """Form for user registration."""

    username = forms.CharField(
        label='Username',
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    email = forms.EmailField(
        label='Email',
        max_length=100,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    password = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        validators=[MinLengthValidator(8, message="Password must be at least 8 characters long.")]
    )

    confirm_password = forms.CharField(
        label='Confirm Password',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        validators=[MinLengthValidator(8, message="Password must be at least 8 characters long.")]
    )

    class Meta:
        model = User 
        fields = ['username', "email", 'password']

    def save(self):
        """Save user with hashed password."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user

    def clean(self):
        """Validate password and confirm_password match."""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")

class LoginForm(forms.Form):
    """Form for user login."""

    username = forms.CharField(
        label='Username',
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    password = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        validators=[MinLengthValidator(8, message="Password must be at least 8 characters long.")]
    )

class PostForm(forms.ModelForm):
    """Form for creating and editing blog posts."""

    title = forms.CharField(
        label='Title',
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[MinLengthValidator(8, message="Title must be at least 8 characters long.")]
    )

    content = forms.CharField(
        label='Content',
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 50}),
        validators=[MinLengthValidator(20, message="Content must be at least 20 characters long.")]
    )

    category = forms.ModelChoiceField(
        label='Category',
        required=True,
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select Category",
    )

    img_url = forms.ImageField(
        label='Image',
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'img_url']

    def save(self, commit=True):
        """Save post and set default image if not provided."""
        post = super().save(commit=False)
        cleaned_data = super().clean()
        if cleaned_data.get('img_url'):
            post.img_url = cleaned_data['img_url']
        else:
            post.img_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/2048px-No_image_available.svg.png"
        if commit:
            post.save()
        return post

class forgetPasswordForm(forms.Form):
    """Form for requesting password reset email."""

    email = forms.EmailField(
        label='Email',
        max_length=100,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        """Validate that email exists in the database."""
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError("No account found with this email address.")

class resetForm(forms.Form):
    """Form for resetting user password."""

    password = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        validators=[MinLengthValidator(8, message="Password must be at least 8 characters long.")]
    )

    confirm_password = forms.CharField(
        label='Confirm Password',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        validators=[MinLengthValidator(8, message="Password must be at least 8 characters long.")]
    )

    def clean(self):
        """Validate password and confirm_password match."""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")