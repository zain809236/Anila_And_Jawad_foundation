from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('our-mission/', views.our_mission, name='our_mission'),
    path('about/', views.about, name='about'),
    path('our-partners/', views.our_partners, name='our_partners'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('testimonials/submit/', views.submit_testimonial, name='submit_testimonial'),

    # Blog
    path('blogs/', views.blogs, name='blogs'),
    path('blogpost/', views.blogpost, name='blogpost'),  # Default blog post
    path('blogpost/<slug:slug>/', views.blogpost, name='blogpost_detail'),  # Blog post with slug

    # Admin
    path('admin-login/', views.adminlogin, name='adminlogin'),
    path('admin-controls/', views.admincontrols, name='admincontrols'),

    # Blog Management System
    path('blog-manager/login/', views.blog_manager_login, name='blog_manager_login'),
    path('blog-manager/logout/', views.blog_manager_logout, name='blog_manager_logout'),
    path('blog-management/', views.blogmanagement, name='blogmanagement'),
    path('blog-management/create/', views.blog_create, name='blog_create'),
    path('blog-management/edit/<int:pk>/', views.blog_edit, name='blog_edit'),
    path('blog-management/delete/<int:pk>/', views.blog_delete, name='blog_delete'),

    # Forms and actions
    path('contact/', views.contact, name='contact'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('donate/', views.donate, name='donate'),
]
