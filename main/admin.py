from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from django.utils.html import format_html
from .models import (
    Partner, BlogPost, Testimonial, ContactMessage,
    Donation, NewsletterSubscriber, Gallery, SiteSettings
)


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'is_active', 'display_order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'email', 'description']
    list_editable = ['display_order', 'is_active']
    ordering = ['display_order', 'name']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'mission_statement', 'logo')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'website')
        }),
        ('Social Media', {
            'fields': ('facebook', 'twitter', 'instagram', 'youtube'),
            'classes': ('collapse',)
        }),
        ('Images', {
            'fields': ('featured_image', 'gallery_image_1', 'gallery_image_2', 'gallery_image_3'),
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': ('is_active', 'display_order')
        }),
    )


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'is_featured', 'published_date', 'view_count']
    list_filter = ['status', 'category', 'is_featured', 'published_date', 'created_at']
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status', 'is_featured']
    date_hierarchy = 'published_date'
    ordering = ['-published_date', '-created_at']

    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'author', 'category', 'excerpt', 'content', 'featured_image')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Publishing', {
            'fields': ('status', 'is_featured', 'published_date')
        }),
        ('Statistics', {
            'fields': ('view_count',),
            'classes': ('collapse',)
        }),
    )

    actions = ['make_published', 'make_draft', 'make_featured']

    def make_published(self, request, queryset):
        queryset.update(status='published')
        self.message_user(request, f"{queryset.count()} posts published successfully.")
    make_published.short_description = "Publish selected posts"

    def make_draft(self, request, queryset):
        queryset.update(status='draft')
        self.message_user(request, f"{queryset.count()} posts moved to draft.")
    make_draft.short_description = "Move to draft"

    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f"{queryset.count()} posts marked as featured.")
    make_featured.short_description = "Mark as featured"


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'testimonial_type', 'is_approved', 'is_featured', 'created_at']
    list_filter = ['testimonial_type', 'is_approved', 'is_featured', 'created_at']
    search_fields = ['name', 'organization', 'content']
    list_editable = ['is_approved', 'is_featured']
    ordering = ['display_order', '-created_at']

    fieldsets = (
        ('Testimonial Information', {
            'fields': ('name', 'organization', 'testimonial_type', 'content', 'image')
        }),
        ('Display Settings', {
            'fields': ('is_approved', 'is_featured', 'display_order')
        }),
    )

    actions = ['approve_testimonials', 'reject_testimonials']

    def approve_testimonials(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f"{queryset.count()} testimonials approved.")
    approve_testimonials.short_description = "Approve selected testimonials"

    def reject_testimonials(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f"{queryset.count()} testimonials rejected.")
    reject_testimonials.short_description = "Reject selected testimonials"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'inquiry_type', 'subject', 'is_read', 'is_responded', 'created_at']
    list_filter = ['inquiry_type', 'is_read', 'is_responded', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['is_read', 'is_responded']
    ordering = ['-created_at']
    readonly_fields = ['created_at']

    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'inquiry_type')
        }),
        ('Message', {
            'fields': ('subject', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'is_responded', 'response_notes')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_as_read', 'mark_as_responded']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f"{queryset.count()} messages marked as read.")
    mark_as_read.short_description = "Mark as read"

    def mark_as_responded(self, request, queryset):
        queryset.update(is_responded=True)
        self.message_user(request, f"{queryset.count()} messages marked as responded.")
    mark_as_responded.short_description = "Mark as responded"


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['donor_name', 'amount_display', 'payment_method', 'payment_status', 'purpose', 'created_at']
    list_filter = ['payment_status', 'payment_method', 'is_recurring', 'is_anonymous', 'created_at']
    search_fields = ['donor_name', 'donor_email', 'transaction_id', 'receipt_number']
    list_editable = ['payment_status']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'completed_at', 'receipt_number']

    fieldsets = (
        ('Donor Information', {
            'fields': ('donor_name', 'donor_email', 'donor_phone', 'is_anonymous')
        }),
        ('Donation Details', {
            'fields': ('amount', 'currency', 'purpose', 'partner', 'is_recurring')
        }),
        ('Payment Information', {
            'fields': ('payment_method', 'payment_status', 'transaction_id', 'receipt_number')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )

    def amount_display(self, obj):
        return f"{obj.currency} {obj.amount:,.2f}"
    amount_display.short_description = 'Amount'

    actions = ['mark_as_completed', 'mark_as_failed']

    def mark_as_completed(self, request, queryset):
        queryset.update(payment_status='completed')
        self.message_user(request, f"{queryset.count()} donations marked as completed.")
    mark_as_completed.short_description = "Mark as completed"

    def mark_as_failed(self, request, queryset):
        queryset.update(payment_status='failed')
        self.message_user(request, f"{queryset.count()} donations marked as failed.")
    mark_as_failed.short_description = "Mark as failed"


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'is_active', 'subscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email', 'name']
    list_editable = ['is_active']
    ordering = ['-subscribed_at']
    readonly_fields = ['subscribed_at', 'unsubscribed_at']

    actions = ['activate_subscribers', 'deactivate_subscribers']

    def activate_subscribers(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f"{queryset.count()} subscribers activated.")
    activate_subscribers.short_description = "Activate selected subscribers"

    def deactivate_subscribers(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"{queryset.count()} subscribers deactivated.")
    deactivate_subscribers.short_description = "Deactivate selected subscribers"


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_featured', 'display_order', 'created_at']
    list_filter = ['category', 'is_featured', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_featured', 'display_order']
    ordering = ['display_order', '-created_at']

    fieldsets = (
        ('Gallery Item', {
            'fields': ('title', 'description', 'image', 'category')
        }),
        ('Related Content', {
            'fields': ('partner', 'blog_post'),
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'display_order')
        }),
    )


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Site Information', {
            'fields': ('site_name', 'site_tagline')
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_phone', 'contact_address')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'youtube_url')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords', 'google_analytics_id')
        }),
        ('Footer', {
            'fields': ('footer_text',)
        }),
    )

    def has_add_permission(self, request):
        # Prevent adding more than one instance
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion
        return False


# Custom User Admin for easy Blog Manager creation
class CustomUserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_blog_manager', 'is_superuser']
    list_filter = ['is_staff', 'is_superuser', 'groups']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'description': '<strong>Blog Manager Setup:</strong> To create a Blog Manager user, check "Staff status" and add them to the "Blog Manager" group below. Blog Managers can create/edit blog posts but cannot publish them.'
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'is_staff', 'groups'),
            'description': '<div style="background: #fef3c7; padding: 15px; margin: 10px 0; border-left: 4px solid #f59e0b;"><strong>Creating a Blog Manager:</strong><br/>1. Enter username and password<br/>2. Check "Staff status" box<br/>3. Select "Blog Manager" from Groups (below)<br/>4. Save<br/><br/><strong>Note:</strong> Blog Managers can only create/edit blog posts as drafts. You (Super Admin) must publish their posts from the BlogPost section.</div>'
        }),
    )

    actions = ['make_blog_manager', 'remove_blog_manager']

    def is_blog_manager(self, obj):
        """Display if user is a Blog Manager"""
        blog_manager_group = Group.objects.filter(name='Blog Manager').first()
        if blog_manager_group and obj.groups.filter(id=blog_manager_group.id).exists():
            return format_html('<span style="color: green; font-weight: bold;">✓ Blog Manager</span>')
        return format_html('<span style="color: gray;">—</span>')
    is_blog_manager.short_description = 'Blog Manager Role'

    def make_blog_manager(self, request, queryset):
        """Convert selected users to Blog Managers"""
        blog_manager_group, created = Group.objects.get_or_create(name='Blog Manager')
        count = 0
        for user in queryset:
            if not user.is_superuser:  # Don't convert superusers
                user.is_staff = True
                user.save()
                user.groups.add(blog_manager_group)
                count += 1
        self.message_user(request, f"{count} user(s) converted to Blog Manager successfully.")
    make_blog_manager.short_description = "Convert to Blog Manager"

    def remove_blog_manager(self, request, queryset):
        """Remove Blog Manager role from selected users"""
        blog_manager_group = Group.objects.filter(name='Blog Manager').first()
        if blog_manager_group:
            count = 0
            for user in queryset:
                if user.groups.filter(id=blog_manager_group.id).exists():
                    user.groups.remove(blog_manager_group)
                    count += 1
            self.message_user(request, f"Blog Manager role removed from {count} user(s).")
    remove_blog_manager.short_description = "Remove Blog Manager role"


# Unregister default User admin and register custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# Customize admin site header and title
admin.site.site_header = "Anila & Jawad Iqbal Foundation Admin"
admin.site.site_title = "AJIF Admin Portal"
admin.site.index_title = "Welcome to AJIF Administration"
