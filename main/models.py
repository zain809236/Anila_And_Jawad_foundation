from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone


class Partner(models.Model):
    """Partner organizations"""
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='partners/', null=True, blank=True)
    description = models.TextField()
    mission_statement = models.TextField(blank=True)
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)

    # Social media links
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    youtube = models.URLField(blank=True)

    # Images
    featured_image = models.ImageField(upload_to='partners/featured/', null=True, blank=True)
    gallery_image_1 = models.ImageField(upload_to='partners/gallery/', null=True, blank=True)
    gallery_image_2 = models.ImageField(upload_to='partners/gallery/', null=True, blank=True)
    gallery_image_3 = models.ImageField(upload_to='partners/gallery/', null=True, blank=True)

    # Meta
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    """Blog posts and news articles"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    CATEGORY_CHOICES = [
        ('news', 'News'),
        ('blog', 'Blog'),
        ('event', 'Event'),
        ('update', 'Update'),
        ('impact', 'Impact Story'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='blog_posts')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='blog')

    # Content
    excerpt = models.TextField(max_length=500, blank=True, help_text="Short description for previews")
    content = models.TextField()
    featured_image = models.ImageField(upload_to='blog/', null=True, blank=True)

    # SEO
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(max_length=300, blank=True)

    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False, help_text="Display on homepage")

    # Timestamps
    published_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Statistics
    view_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-published_date', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == 'published' and not self.published_date:
            self.published_date = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f'/blogpost/{self.slug}/'


class Testimonial(models.Model):
    """Testimonials from community members, partners, donors"""
    TESTIMONIAL_TYPE_CHOICES = [
        ('personal', 'Personal'),
        ('partner', 'Partner Organization'),
        ('donor', 'Donor'),
        ('beneficiary', 'Beneficiary'),
    ]

    name = models.CharField(max_length=200)
    organization = models.CharField(max_length=200, blank=True)
    testimonial_type = models.CharField(max_length=20, choices=TESTIMONIAL_TYPE_CHOICES, default='personal')
    content = models.TextField()
    image = models.ImageField(upload_to='testimonials/', null=True, blank=True)

    # Status
    is_approved = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return f"{self.name} - {self.testimonial_type}"


class ContactMessage(models.Model):
    """Contact form submissions"""
    INQUIRY_TYPE_CHOICES = [
        ('general', 'General Inquiry'),
        ('volunteer', 'Volunteer'),
        ('partnership', 'Partnership'),
        ('donation', 'Donation Query'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPE_CHOICES, default='general')
    subject = models.CharField(max_length=200)
    message = models.TextField()

    # Status
    is_read = models.BooleanField(default=False)
    is_responded = models.BooleanField(default=False)
    response_notes = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"


class Donation(models.Model):
    """Track donations"""
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('jazzcash', 'JazzCash'),
        ('easypaisa', 'EasyPaisa'),
        ('bank', 'Bank Transfer'),
        ('credit_card', 'Credit Card'),
        ('other', 'Other'),
    ]

    # Donor information
    donor_name = models.CharField(max_length=200)
    donor_email = models.EmailField()
    donor_phone = models.CharField(max_length=20, blank=True)

    # Donation details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='PKR')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')

    # Purpose
    purpose = models.CharField(max_length=200, blank=True, help_text="What is this donation for?")
    partner = models.ForeignKey(Partner, on_delete=models.SET_NULL, null=True, blank=True, related_name='donations')

    # Payment details
    transaction_id = models.CharField(max_length=200, blank=True)
    receipt_number = models.CharField(max_length=100, blank=True, unique=True)

    # Recurring
    is_recurring = models.BooleanField(default=False)

    # Anonymous
    is_anonymous = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.donor_name} - {self.amount} {self.currency}"

    def save(self, *args, **kwargs):
        if not self.receipt_number:
            # Generate receipt number
            self.receipt_number = f"AJIF-{timezone.now().strftime('%Y%m%d')}-{self.pk or '0000'}"
        if self.payment_status == 'completed' and not self.completed_at:
            self.completed_at = timezone.now()
        super().save(*args, **kwargs)


class NewsletterSubscriber(models.Model):
    """Newsletter email subscriptions"""
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email


class Gallery(models.Model):
    """Image gallery for events and activities"""
    GALLERY_CATEGORY_CHOICES = [
        ('event', 'Event'),
        ('activity', 'Activity'),
        ('team', 'Team'),
        ('impact', 'Impact'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='gallery/')
    category = models.CharField(max_length=20, choices=GALLERY_CATEGORY_CHOICES, default='event')

    # Related content
    partner = models.ForeignKey(Partner, on_delete=models.SET_NULL, null=True, blank=True, related_name='gallery_images')
    blog_post = models.ForeignKey(BlogPost, on_delete=models.SET_NULL, null=True, blank=True, related_name='gallery_images')

    # Display
    is_featured = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', '-created_at']
        verbose_name_plural = "Galleries"

    def __str__(self):
        return self.title


class SiteSettings(models.Model):
    """Global site settings"""
    site_name = models.CharField(max_length=200, default="Anila & Jawad Iqbal Foundation")
    site_tagline = models.CharField(max_length=300, blank=True)

    # Contact information
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_address = models.TextField(blank=True)

    # Social media
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)

    # SEO
    meta_description = models.TextField(max_length=300, blank=True)
    meta_keywords = models.CharField(max_length=500, blank=True)
    google_analytics_id = models.CharField(max_length=50, blank=True)

    # Footer
    footer_text = models.TextField(blank=True)

    # Timestamps
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
