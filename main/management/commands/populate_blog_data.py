from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from main.models import BlogPost
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Populate the database with dummy blog posts and news articles'

    def handle(self, *args, **options):
        # Delete existing blog posts
        BlogPost.objects.all().delete()
        self.stdout.write(self.style.WARNING('Deleted all existing blog posts'))

        # Get or create a default author
        author, created = User.objects.get_or_create(
            username='ajif_admin',
            defaults={
                'first_name': 'AJIF',
                'last_name': 'Team',
                'email': 'admin@ajif.org'
            }
        )
        if created:
            author.set_password('admin123')
            author.save()
            self.stdout.write(self.style.SUCCESS(f'Created default author: {author.username}'))

        # Blog Posts Data with all required fields
        blog_posts_data = [
            {'slug': 'empowering-communities-through-education', 'title': 'Empowering Communities Through Education', 'category': 'blog', 'excerpt': 'Discover how our foundation is transforming lives through educational initiatives across Pakistan.', 'content': 'Education is the cornerstone of development and progress. Our foundation has been working tirelessly to provide quality education to underprivileged children across Pakistan.', 'published_date': timezone.now()},
            {'slug': 'healthcare-services-expand-rural-areas', 'title': 'Healthcare Services Expand to Rural Areas', 'category': 'blog', 'excerpt': 'Learn about our healthcare programs providing essential medical services to those in need.', 'content': 'Access to healthcare is a fundamental right, yet millions in rural Pakistan lack basic medical services. Our mobile health clinics are changing this reality.', 'published_date': timezone.now() - timedelta(days=2)},
            {'slug': 'building-hope-new-community-center-opens', 'title': 'Building Hope: New Community Center Opens', 'category': 'impact', 'excerpt': 'A new community center opens its doors in rural Punjab.', 'content': 'We are thrilled to announce the opening of our latest community center in rural Punjab. This facility provides a safe space for education and community events.', 'published_date': timezone.now() - timedelta(days=5)},
            {'slug': 'youth-sports-program-launches', 'title': 'Youth Sports Program Launches', 'category': 'blog', 'excerpt': 'Our new youth sports initiative brings athletics to underprivileged communities.', 'content': 'Sports have the power to transform lives. Our new youth sports program brings these benefits to underprivileged communities across Pakistan.', 'published_date': timezone.now() - timedelta(days=7)},
            {'slug': 'scholarship-recipients-share-stories', 'title': 'Scholarship Recipients Share Their Stories', 'category': 'impact', 'excerpt': 'Meet the inspiring students whose lives have been changed through our scholarship program.', 'content': 'Behind every scholarship is a story of hope, determination, and transformation. Today, we share inspiring journeys of students.', 'published_date': timezone.now() - timedelta(days=9)},
            {'slug': 'clean-water-initiative-reaches-10000-families', 'title': 'Clean Water Initiative Reaches 10,000 Families', 'category': 'impact', 'excerpt': 'Our clean water project has successfully provided access to safe drinking water.', 'content': 'Clean water is essential for health and dignity. Our clean water initiative has reached a major milestone.', 'published_date': timezone.now() - timedelta(days=12)},
            {'slug': 'legal-aid-support-services', 'title': 'Legal Aid and Support Services', 'category': 'blog', 'excerpt': 'Explore our legal aid initiatives helping families navigate legal challenges.', 'content': 'Justice should be accessible to all. Our legal aid program provides free legal consultation and representation.', 'published_date': timezone.now() - timedelta(days=14)},
            {'slug': 'vocational-training-creates-opportunities', 'title': 'Vocational Training Creates New Opportunities', 'category': 'blog', 'excerpt': 'Our vocational training programs equip workers with valuable skills.', 'content': 'Economic empowerment begins with employable skills. Our programs provide practical skills training in high-demand trades.', 'published_date': timezone.now() - timedelta(days=19)},
            {'slug': 'partnership-local-organizations', 'title': 'Partnership with Local Organizations', 'category': 'update', 'excerpt': 'Learn how we collaborate with local NGOs to maximize our impact.', 'content': 'Collaboration multiplies impact. We work closely with local NGOs and community organizations.', 'published_date': timezone.now() - timedelta(days=22)},
            {'slug': 'women-empowerment-literacy-programs', 'title': 'Women Empowerment Through Literacy Programs', 'category': 'blog', 'excerpt': 'Our women literacy programs are breaking barriers and empowering females across rural Pakistan.', 'content': 'Education empowers women to transform their lives. Over 500 women have graduated from our literacy courses this year.', 'published_date': timezone.now() - timedelta(days=25)},
        ]

        # News Articles Data
        news_posts_data = [
            {'slug': 'education-initiative-launches-rural-punjab', 'title': 'Education Initiative Launches in Rural Punjab', 'category': 'news', 'excerpt': 'Government announces major education reforms for rural areas.', 'content': 'The government has announced a comprehensive education initiative targeting rural areas of Punjab.', 'published_date': timezone.now()},
            {'slug': 'healthcare-services-expand-sindh', 'title': 'Healthcare Services Expand Across Sindh', 'category': 'news', 'excerpt': 'New mobile health units deployed to remote communities.', 'content': 'The Sindh Health Department has deployed new mobile health units to serve remote communities.', 'published_date': timezone.now() - timedelta(days=1)},
            {'slug': 'infrastructure-development-balochistan', 'title': 'Infrastructure Development in Balochistan', 'category': 'news', 'excerpt': 'Major road construction projects underway in rural regions.', 'content': 'Major infrastructure development projects are underway in Balochistan.', 'published_date': timezone.now() - timedelta(days=2)},
            {'slug': 'national-sports-initiative-youth', 'title': 'National Sports Initiative for Youth', 'category': 'news', 'excerpt': 'Government launches nationwide youth sports program.', 'content': 'A nationwide youth sports initiative has been launched to promote healthy lifestyles.', 'published_date': timezone.now() - timedelta(days=3)},
            {'slug': 'clean-water-projects-benefit-thousands', 'title': 'Clean Water Projects Benefit Thousands', 'category': 'news', 'excerpt': 'New water purification plants operational in 10 districts.', 'content': 'New water purification plants have become operational across Pakistan.', 'published_date': timezone.now() - timedelta(days=4)},
            {'slug': 'job-creation-program-shows-results', 'title': 'Job Creation Program Shows Results', 'category': 'news', 'excerpt': 'Skills training initiative helps 5000 find employment.', 'content': 'A government-sponsored skills training program has achieved remarkable success.', 'published_date': timezone.now() - timedelta(days=5)},
            {'slug': 'digital-literacy-program-reaches-villages', 'title': 'Digital Literacy Program Reaches Villages', 'category': 'news', 'excerpt': 'Free computer training provided to rural youth.', 'content': 'A digital literacy program has been launched in rural areas to equip youth with computer skills.', 'published_date': timezone.now() - timedelta(days=6)},
            {'slug': 'legal-rights-awareness-campaign', 'title': 'Legal Rights Awareness Campaign', 'category': 'news', 'excerpt': 'Citizens educated about fundamental rights.', 'content': 'A nationwide legal rights awareness campaign is educating citizens.', 'published_date': timezone.now() - timedelta(days=7)},
            {'slug': 'new-universities-open-remote-areas', 'title': 'New Universities Open in Remote Areas', 'category': 'news', 'excerpt': 'Higher education facilities inaugurated in underserved regions.', 'content': 'New university campuses have been inaugurated in remote regions of Pakistan.', 'published_date': timezone.now() - timedelta(days=8)},
            {'slug': 'housing-project-low-income-families', 'title': 'Housing Project for Low-Income Families', 'category': 'news', 'excerpt': 'Government launches affordable housing scheme.', 'content': 'An affordable housing scheme has been launched to provide decent housing.', 'published_date': timezone.now() - timedelta(days=9)},
        ]

        # Create blog posts
        blog_count = 0
        for data in blog_posts_data:
            post = BlogPost.objects.create(author=author, status='published', **data)
            blog_count += 1
            self.stdout.write(self.style.SUCCESS(f'Created: {post.title}'))

        # Create news articles
        news_count = 0
        for data in news_posts_data:
            post = BlogPost.objects.create(author=author, status='published', **data)
            news_count += 1
            self.stdout.write(self.style.SUCCESS(f'Created: {post.title}'))

        self.stdout.write(self.style.SUCCESS(f'\nTotal: {blog_count} blogs + {news_count} news = {blog_count + news_count} posts created!'))
