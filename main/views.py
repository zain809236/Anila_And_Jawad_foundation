from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q, Count, Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import (
    BlogPost, Partner, Testimonial, ContactMessage,
    Donation, NewsletterSubscriber, Gallery, SiteSettings
)
from .forms import ContactForm, NewsletterForm, TestimonialForm, DonationForm


def home(request):
    """Homepage with featured content"""
    featured_posts = BlogPost.objects.filter(status='published', is_featured=True)[:3]
    partners = Partner.objects.filter(is_active=True)[:4]
    testimonials = Testimonial.objects.filter(is_approved=True, is_featured=True)[:3]

    context = {
        'featured_posts': featured_posts,
        'partners': partners,
        'testimonials': testimonials,
    }
    return render(request, 'home.html', context)


def our_mission(request):
    """Our mission page"""
    testimonials = Testimonial.objects.filter(is_approved=True, testimonial_type='personal')[:2]
    gallery_images = Gallery.objects.filter(is_featured=True, category='impact')[:3]

    context = {
        'testimonials': testimonials,
        'gallery_images': gallery_images,
    }
    return render(request, 'Our Mission.html', context)


def about(request):
    """About page"""
    partners = Partner.objects.filter(is_active=True)
    gallery_images = Gallery.objects.filter(category='event')[:6]

    context = {
        'partners': partners,
        'gallery_images': gallery_images,
    }
    return render(request, 'about.html', context)


def our_partners(request):
    """Partners page with all partner details"""
    partners = Partner.objects.filter(is_active=True)

    context = {
        'partners': partners,
    }
    return render(request, 'our partners.html', context)


def testimonials(request):
    """Testimonials page - display only"""
    all_testimonials = Testimonial.objects.filter(is_approved=True)

    context = {
        'testimonials': all_testimonials,
    }
    return render(request, 'testimonials.html', context)


def submit_testimonial(request):
    """Submit testimonial page with form"""
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.is_approved = False  # Needs admin approval
            testimonial.save()
            messages.success(request, 'Thank you for your testimonial! It will be reviewed by our team.')
            return redirect('testimonials')
    else:
        form = TestimonialForm()

    context = {
        'form': form,
    }
    return render(request, 'submit_testimonial.html', context)


def blogs(request):
    """Blog listing page with search and filtering"""
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')

    # Get published blog posts from database
    db_posts = BlogPost.objects.filter(status='published')

    # Apply search filter
    if query:
        db_posts = db_posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(excerpt__icontains=query)
        )

    # Apply category filter
    if category:
        db_posts = db_posts.filter(category=category)

    # Use database posts if available; otherwise use dummy data
    if db_posts.exists():
        # Separate blog posts and news posts from database
        db_blog_posts = db_posts.exclude(category='news')[:10]  # Blog, impact, update, event
        db_news_posts = db_posts.filter(category='news')[:10]  # News only

        # Available images to cycle through
        blog_images = ['assets/uni.jpg', 'assets/water.jpg', 'assets/construction.jpg', 'assets/hockey.jpg', 'assets/student.jpg', 'assets/river.jpg', 'assets/darbar.jpg', 'assets/labour.jpg', 'assets/mission-preview.jpg']
        news_images = ['assets/uni.jpg', 'assets/water.jpg', 'assets/construction.jpg', 'assets/hockey.jpg', 'assets/river.jpg', 'assets/labour.jpg', 'assets/student.jpg', 'assets/darbar.jpg', 'assets/mission-preview.jpg']

        # Convert database blog posts to template-friendly format
        blog_posts = []
        for idx, post in enumerate(db_blog_posts):
            blog_posts.append({
                'slug': post.slug,
                'image': f'assets/{post.featured_image.name.split("/")[-1]}' if post.featured_image else blog_images[idx % len(blog_images)],
                'title': post.title,
                'category': post.get_category_display(),
                'date': post.created_at.strftime('%b %d, %Y'),
                'excerpt': post.excerpt or post.content[:150] + '...',
            })

        # Convert database news posts to template-friendly format
        news_posts = []
        for idx, post in enumerate(db_news_posts):
            news_posts.append({
                'slug': post.slug,
                'image': f'assets/{post.featured_image.name.split("/")[-1]}' if post.featured_image else news_images[idx % len(news_images)],
                'title': post.title,
                'category': post.get_category_display(),
                'date': post.created_at.strftime('%b %d, %Y'),
                'excerpt': post.excerpt or post.content[:150] + '...',
            })
    else:
        # Dummy blog data with existing static images - 10 blog posts
        blog_posts = [
            {
                'id': 1,
                'slug': 'empowering-communities-through-education',
                'image': 'assets/uni.jpg',
                'title': 'Empowering Communities Through Education',
                'category': 'Education',
                'date': 'Dec 17, 2025',
                'author': 'Dr. Sarah Ahmed',
                'excerpt': 'Discover how our foundation is transforming lives through educational initiatives across Pakistan. We provide scholarships, school supplies, and mentorship programs to help children reach their full potential.',
                'content': 'Education is the cornerstone of development and progress. Our foundation has been working tirelessly to provide quality education to underprivileged children across Pakistan. Through our scholarship program, we have supported over 2,000 students in pursuing their dreams.\n\nWe believe that every child deserves access to quality education, regardless of their economic background. Our programs include providing school supplies, building libraries, training teachers, and offering mentorship opportunities. The impact has been tremendous - our students are now pursuing higher education and giving back to their communities.\n\nOur approach is holistic, focusing not just on academic excellence but also on character development, critical thinking, and leadership skills. We work closely with local communities to ensure our programs are culturally sensitive and sustainable.',
                'type': 'blog'
            },
            {
                'id': 2,
                'slug': 'healthcare-services-expand-rural-areas',
                'image': 'assets/water.jpg',
                'title': 'Healthcare Services Expand to Rural Areas',
                'category': 'Healthcare',
                'date': 'Dec 15, 2025',
                'author': 'Dr. Hassan Malik',
                'excerpt': 'Learn about our healthcare programs providing essential medical services to those in need. Our mobile clinics bring doctors and medicines to remote villages that lack basic healthcare infrastructure.',
                'content': 'Access to healthcare is a fundamental right, yet millions in rural Pakistan lack basic medical services. Our mobile health clinics are changing this reality by bringing doctors, nurses, and essential medicines directly to remote communities.\n\nThese mobile units are equipped with diagnostic equipment and staffed by qualified medical professionals. They provide free consultations, vaccinations, maternal health services, and treatment for common ailments. Since launching this initiative, we have served over 50,000 patients.\n\nWe also conduct health awareness campaigns, teaching communities about hygiene, nutrition, and disease prevention. This preventive approach is key to building healthier communities in the long term.',
                'type': 'blog'
            },
            {
                'id': 3,
                'slug': 'building-hope-new-community-center-opens',
                'image': 'assets/construction.jpg',
                'title': 'Building Hope: New Community Center Opens',
                'category': 'Infrastructure',
                'date': 'Dec 12, 2025',
                'author': 'Amina Rashid',
                'excerpt': 'A new community center opens its doors in rural Punjab, providing a safe space for education, healthcare, and community gatherings. This marks our 5th community center built this year.',
                'content': 'We are thrilled to announce the opening of our latest community center in rural Punjab. This state-of-the-art facility provides a safe and welcoming space for education, healthcare services, vocational training, and community events.\n\nThe center features classrooms, a computer lab, a health clinic, a library, and multipurpose halls. It was built with input from local community members to ensure it meets their specific needs. The construction created jobs for local workers and used locally-sourced materials wherever possible.\n\nThis is our fifth community center this year, and we plan to build many more. These centers serve as hubs of hope, opportunity, and positive change in underserved communities.',
                'type': 'blog'
            },
            {
                'id': 4,
                'slug': 'youth-sports-program-launches',
                'image': 'assets/hockey.jpg',
                'title': 'Youth Sports Program Launches',
                'category': 'Community',
                'date': 'Dec 10, 2025',
                'author': 'Coach Ahmed Khan',
                'excerpt': 'Our new youth sports initiative brings athletics and teamwork training to underprivileged communities. Sports help build confidence, discipline, and leadership skills in young people.',
                'content': 'Sports have the power to transform lives, teaching discipline, teamwork, and resilience. Our new youth sports program brings these benefits to underprivileged communities across Pakistan.\n\nWe offer training in cricket, football, hockey, and athletics, led by experienced coaches. The program is free and open to all children aged 8-18. Beyond sports skills, we focus on character development, teaching values like sportsmanship, respect, and perseverance.\n\nEarly results have been amazing - participants show improved confidence, better school attendance, and stronger community bonds. Several talented athletes have already been identified for advanced training programs.',
                'type': 'blog'
            },
            {
                'id': 5,
                'slug': 'scholarship-recipients-share-stories',
                'image': 'assets/student.jpg',
                'title': 'Scholarship Recipients Share Their Stories',
                'category': 'Education',
                'date': 'Dec 8, 2025',
                'author': 'Fatima Noor',
                'excerpt': 'Meet the inspiring students whose lives have been changed through our scholarship program. Their success stories demonstrate the power of education in breaking the cycle of poverty.',
                'content': 'Behind every scholarship is a story of hope, determination, and transformation. Today, we share the inspiring journeys of students whose lives have been changed through our scholarship program.\n\nMeet Aisha, who dreamed of becoming a doctor but could not afford school fees. Through our scholarship, she completed her education and is now studying medicine. Then there is Hassan, the first in his family to attend university, now pursuing engineering.\n\nThese success stories motivate us to expand our scholarship program and reach more deserving students. Education truly is the key to breaking the cycle of poverty and creating a brighter future.',
                'type': 'blog'
            },
            {
                'id': 6,
                'slug': 'clean-water-initiative-reaches-10000-families',
                'image': 'assets/river.jpg',
                'title': 'Clean Water Initiative Reaches 10,000 Families',
                'category': 'Infrastructure',
                'date': 'Dec 5, 2025',
                'author': 'Engineer Bilal Hussain',
                'excerpt': 'Our clean water project has successfully provided access to safe drinking water for over 10,000 families. We install water filtration systems and teach communities about water safety and hygiene.',
                'content': 'Clean water is essential for health and dignity. Our clean water initiative has reached a major milestone - providing safe drinking water to over 10,000 families in rural Pakistan.\n\nWe install water filtration systems, dig wells, and repair existing water infrastructure. But our work goes beyond infrastructure - we also educate communities about water conservation, hygiene practices, and water-borne disease prevention.\n\nThe impact has been remarkable. Communities report significant reductions in waterborne illnesses, children spend less time fetching water and more time in school, and overall quality of life has improved dramatically.',
                'type': 'blog'
            },
            {
                'id': 7,
                'slug': 'legal-aid-support-services',
                'image': 'assets/darbar.jpg',
                'title': 'Legal Aid and Support Services',
                'category': 'Legal Aid',
                'date': 'Dec 3, 2025',
                'author': 'Advocate Zainab Ali',
                'excerpt': 'Explore our legal aid initiatives helping families navigate complex legal challenges. We provide free legal consultation and representation for those who cannot afford it.',
                'content': 'Justice should be accessible to all, regardless of economic status. Our legal aid program provides free legal consultation and representation to those who cannot afford it.\n\nOur team of volunteer lawyers helps with a range of issues including family law, property disputes, labor rights, and human rights cases. We have successfully resolved hundreds of cases, bringing justice and peace of mind to vulnerable families.\n\nWe also conduct legal awareness workshops, teaching communities about their rights and how to access the legal system. Empowering people with legal knowledge is crucial for creating a just society.',
                'type': 'blog'
            },
            {
                'id': 8,
                'slug': 'vocational-training-creates-opportunities',
                'image': 'assets/labour.jpg',
                'title': 'Vocational Training Creates New Opportunities',
                'category': 'Employment',
                'date': 'Nov 28, 2025',
                'author': 'Muhammad Tariq',
                'excerpt': 'Our vocational training programs equip workers with valuable skills for sustainable employment. We offer courses in carpentry, sewing, electrical work, and other trades.',
                'content': 'Economic empowerment begins with employable skills. Our vocational training programs provide practical skills training in high-demand trades, opening doors to sustainable employment.\n\nWe offer courses in carpentry, tailoring, electrical work, plumbing, mobile repair, and computer skills. Training is hands-on and industry-aligned, ensuring graduates are job-ready. Many of our graduates have started their own businesses or secured stable employment.\n\nThe program particularly focuses on women and youth, providing them with skills to become economically independent. We also offer business training to help graduates start and manage their own enterprises.',
                'type': 'blog'
            },
            {
                'id': 9,
                'slug': 'partnership-local-organizations',
                'image': 'assets/water.jpg',
                'title': 'Partnership with Local Organizations',
                'category': 'Community',
                'date': 'Nov 25, 2025',
                'author': 'Nadia Iqbal',
                'excerpt': 'Learn how we collaborate with local NGOs and community organizations to maximize our impact. Together, we can reach more people and create lasting positive change.',
                'content': 'Collaboration multiplies impact. We work closely with local NGOs, community organizations, and government agencies to maximize our reach and effectiveness.\n\nThese partnerships allow us to leverage local knowledge, avoid duplication of efforts, and ensure our programs are culturally appropriate and sustainable. Together, we have implemented projects in education, healthcare, infrastructure, and economic development.\n\nOur collaborative approach recognizes that lasting change requires collective effort. By working together, we can reach more people and create more meaningful, sustainable impact in communities across Pakistan.',
                'type': 'blog'
            },
            {
                'id': 10,
                'slug': 'women-empowerment-literacy-programs',
                'image': 'assets/uni.jpg',
                'title': 'Women Empowerment Through Literacy Programs',
                'category': 'Education',
                'date': 'Nov 22, 2025',
                'author': 'Dr. Sana Mahmood',
                'excerpt': 'Our women literacy programs are breaking barriers and empowering females across rural Pakistan. Over 500 women have graduated from our basic literacy courses this year, opening doors to new opportunities.',
                'content': 'Education empowers women to transform their lives and communities. Our women literacy programs are breaking barriers and creating opportunities for females across rural Pakistan.\n\nOver 500 women have graduated from our basic literacy courses this year. Many have gone on to pursue further education, start small businesses, or become community leaders. The program covers reading, writing, basic math, and life skills.\n\nWe create safe, supportive learning environments where women can learn without fear or judgment. Classes are scheduled to accommodate household responsibilities, and childcare is provided. The transformation we witness in these women - in confidence, agency, and aspirations - is truly inspiring.',
                'type': 'blog'
            },
        ]

        # Dummy news data for "Current News in Pakistan" section - 10 news items
        news_posts = [
        {
            'id': 11,
            'slug': 'education-initiative-launches-rural-punjab',
            'image': 'assets/uni.jpg',
            'title': 'Education Initiative Launches in Rural Punjab',
            'category': 'News',
            'date': 'Dec 17, 2025',
            'author': 'News Desk',
            'excerpt': 'Government announces major education reforms for rural areas.',
            'content': 'The government has announced a comprehensive education initiative targeting rural areas of Punjab. The program aims to improve literacy rates and provide better educational infrastructure in underserved communities.\n\nKey components include building 100 new schools, training 5,000 teachers, and providing free textbooks to students. The initiative will also focus on increasing girls\' enrollment in schools through awareness campaigns and incentive programs.\n\nEducation Minister stated that this is part of a broader vision to ensure quality education reaches every child in Pakistan, regardless of their geographic location or economic background.',
            'type': 'news'
        },
        {
            'id': 12,
            'slug': 'healthcare-services-expand-sindh',
            'image': 'assets/water.jpg',
            'title': 'Healthcare Services Expand Across Sindh',
            'category': 'News',
            'date': 'Dec 16, 2025',
            'author': 'News Desk',
            'excerpt': 'New mobile health units deployed to remote communities.',
            'content': 'The Sindh Health Department has deployed new mobile health units to serve remote communities across the province. These units are equipped with modern medical equipment and staffed by qualified healthcare professionals.\n\nThe mobile clinics will provide free consultations, basic diagnostic services, vaccinations, and maternal health services. They will visit each designated area on a fixed schedule, ensuring regular healthcare access for rural populations.\n\nThis initiative is expected to benefit over 2 million people in remote areas who previously had limited access to healthcare facilities.',
            'type': 'news'
        },
        {
            'id': 13,
            'slug': 'infrastructure-development-balochistan',
            'image': 'assets/construction.jpg',
            'title': 'Infrastructure Development in Balochistan',
            'category': 'News',
            'date': 'Dec 15, 2025',
            'author': 'News Desk',
            'excerpt': 'Major road construction projects underway in rural regions.',
            'content': 'Major infrastructure development projects are underway in Balochistan, focusing on improving road connectivity in rural areas. The projects include construction of highways, farm-to-market roads, and bridges.\n\nThese developments are expected to boost economic activity by improving access to markets, schools, and healthcare facilities. The projects are also creating thousands of jobs for local workers.\n\nOfficials stated that improved infrastructure is crucial for the socio-economic development of the region and will help reduce the isolation of remote communities.',
            'type': 'news'
        },
        {
            'id': 14,
            'slug': 'national-sports-initiative-youth',
            'image': 'assets/hockey.jpg',
            'title': 'National Sports Initiative for Youth',
            'category': 'News',
            'date': 'Dec 14, 2025',
            'author': 'News Desk',
            'excerpt': 'Government launches nationwide youth sports program.',
            'content': 'A nationwide youth sports initiative has been launched to promote healthy lifestyles and identify sporting talent across Pakistan. The program covers cricket, football, hockey, athletics, and other sports.\n\nSports facilities are being upgraded in schools and communities, and professional coaches are being hired to train young athletes. The program is free and open to all youth aged 10-20.\n\nThis initiative aims to create a pipeline of talented athletes for national teams while also promoting physical fitness and teamwork among the youth.',
            'type': 'news'
        },
        {
            'id': 15,
            'slug': 'clean-water-projects-benefit-thousands',
            'image': 'assets/river.jpg',
            'title': 'Clean Water Projects Benefit Thousands',
            'category': 'News',
            'date': 'Dec 13, 2025',
            'author': 'News Desk',
            'excerpt': 'New water purification plants operational in 10 districts.',
            'content': 'New water purification plants have become operational in 10 districts across Pakistan, providing clean drinking water to thousands of families. These plants use modern filtration technology to ensure water safety.\n\nThe projects are part of a larger clean water initiative aimed at reducing waterborne diseases and improving public health. Each plant has the capacity to serve 50,000-100,000 people.\n\nCommunity members have expressed gratitude for access to clean water, noting significant improvements in their families\' health and quality of life.',
            'type': 'news'
        },
        {
            'id': 16,
            'slug': 'job-creation-program-shows-results',
            'image': 'assets/labour.jpg',
            'title': 'Job Creation Program Shows Results',
            'category': 'News',
            'date': 'Dec 12, 2025',
            'author': 'News Desk',
            'excerpt': 'Skills training initiative helps 5000 find employment.',
            'content': 'A government-sponsored skills training and job creation program has achieved remarkable success, helping over 5,000 people find employment in various sectors.\n\nThe program provides free vocational training in high-demand fields such as construction, IT, hospitality, and manufacturing. Graduates receive certification and job placement assistance.\n\nThe initiative has been particularly beneficial for youth and women, providing them with skills and opportunities for economic independence and upward mobility.',
            'type': 'news'
        },
        {
            'id': 17,
            'slug': 'digital-literacy-program-reaches-villages',
            'image': 'assets/student.jpg',
            'title': 'Digital Literacy Program Reaches Villages',
            'category': 'News',
            'date': 'Dec 11, 2025',
            'author': 'News Desk',
            'excerpt': 'Free computer training provided to rural youth across Pakistan.',
            'content': 'A digital literacy program has been launched in rural areas to equip youth with essential computer and internet skills. Mobile computer labs are visiting villages to provide free training.\n\nThe program covers basic computer operations, internet usage, email, word processing, and digital safety. Upon completion, participants receive certificates that can help them in job searches.\n\nThis initiative aims to bridge the digital divide and ensure rural youth are not left behind in the digital age.',
            'type': 'news'
        },
        {
            'id': 18,
            'slug': 'legal-rights-awareness-campaign',
            'image': 'assets/darbar.jpg',
            'title': 'Legal Rights Awareness Campaign',
            'category': 'News',
            'date': 'Dec 10, 2025',
            'author': 'News Desk',
            'excerpt': 'Citizens educated about fundamental rights and legal procedures.',
            'content': 'A nationwide legal rights awareness campaign is educating citizens about their fundamental rights and legal procedures. Lawyers and legal experts are conducting workshops in communities.\n\nThe campaign covers topics such as constitutional rights, family law, property rights, labor laws, and how to access the legal system. Free legal consultation services are also being provided.\n\nThis initiative aims to empower citizens with legal knowledge and ensure they can effectively exercise their rights and seek justice when needed.',
            'type': 'news'
        },
        {
            'id': 19,
            'slug': 'new-universities-open-remote-areas',
            'image': 'assets/uni.jpg',
            'title': 'New Universities Open in Remote Areas',
            'category': 'News',
            'date': 'Dec 9, 2025',
            'author': 'News Desk',
            'excerpt': 'Higher education facilities inaugurated in underserved regions.',
            'content': 'New university campuses have been inaugurated in remote and underserved regions of Pakistan, bringing higher education closer to students who previously had limited access.\n\nThese universities offer programs in sciences, humanities, business, and technology. Scholarship programs are available for deserving students, and residential facilities ensure students from far-flung areas can attend.\n\nThe establishment of these institutions is expected to significantly increase higher education enrollment from rural areas and contribute to regional development.',
            'type': 'news'
        },
        {
            'id': 20,
            'slug': 'housing-project-low-income-families',
            'image': 'assets/construction.jpg',
            'title': 'Housing Project for Low-Income Families',
            'category': 'News',
            'date': 'Dec 8, 2025',
            'author': 'News Desk',
            'excerpt': 'Government launches affordable housing scheme for poor families.',
            'content': 'An affordable housing scheme has been launched to provide decent housing to low-income families across Pakistan. The project aims to construct 100,000 housing units over the next two years.\n\nEligible families can acquire homes through easy installment plans with subsidized interest rates. The houses are equipped with basic amenities including electricity, water, and sanitation facilities.\n\nThis initiative addresses the critical housing shortage faced by low-income families and aims to improve their living standards and quality of life.',
            'type': 'news'
        },
    ]

    # Calculate total pages (3 posts per page)
    import math
    total_pages = math.ceil(len(blog_posts) / 3)

    context = {
        'blog_posts': blog_posts,
        'news_posts': news_posts,
        'query': query,
        'category': category,
        'total_pages': total_pages,
    }
    return render(request, 'blogs.html', context)


def blogpost(request, slug=None):
    """Individual blog post detail page - works with both database posts and dummy data"""

    # Check if we have database posts or should use dummy data
    db_posts = BlogPost.objects.filter(status='published')

    # Use database posts if available; otherwise use dummy data
    if db_posts.exists():
        # Use database posts
        if slug:
            post = get_object_or_404(BlogPost, slug=slug, status='published')
            # Increment view count
            post.view_count += 1
            post.save(update_fields=['view_count'])
        else:
            # If no slug, show the latest post
            post = db_posts.first()

        # Get related posts
        related_posts = BlogPost.objects.filter(
            status='published',
            category=post.category if post else 'blog'
        ).exclude(id=post.id if post else None)[:3]

        # Assign default images based on post slug (for posts without featured_image)
        image_map = {
            'empowering-communities-through-education': 'assets/uni.jpg',
            'healthcare-services-expand-rural-areas': 'assets/water.jpg',
            'building-hope-new-community-center-opens': 'assets/construction.jpg',
            'youth-sports-program-launches': 'assets/hockey.jpg',
            'scholarship-recipients-share-stories': 'assets/student.jpg',
            'clean-water-initiative-reaches-10000-families': 'assets/river.jpg',
            'legal-aid-support-services': 'assets/darbar.jpg',
            'vocational-training-creates-opportunities': 'assets/labour.jpg',
            'partnership-local-organizations': 'assets/water.jpg',
            'women-empowerment-literacy-programs': 'assets/uni.jpg',
            'education-initiative-launches-rural-punjab': 'assets/uni.jpg',
            'healthcare-services-expand-sindh': 'assets/water.jpg',
            'infrastructure-development-balochistan': 'assets/construction.jpg',
            'national-sports-initiative-youth': 'assets/hockey.jpg',
            'clean-water-projects-benefit-thousands': 'assets/river.jpg',
            'job-creation-program-shows-results': 'assets/labour.jpg',
            'digital-literacy-program-reaches-villages': 'assets/student.jpg',
            'legal-rights-awareness-campaign': 'assets/darbar.jpg',
            'new-universities-open-remote-areas': 'assets/uni.jpg',
            'housing-project-low-income-families': 'assets/construction.jpg',
        }

        # Add image attribute to post if it doesn't have featured_image
        if post and not post.featured_image:
            post.image = image_map.get(post.slug, 'assets/water.jpg')

        # Add images to related posts
        for related in related_posts:
            if not related.featured_image:
                related.image = image_map.get(related.slug, 'assets/water.jpg')
    else:
        # Use dummy data - same data as in blogs view
        # Dummy blog data
        blog_posts = [
            {'id': 1, 'slug': 'empowering-communities-through-education', 'image': 'assets/uni.jpg', 'title': 'Empowering Communities Through Education', 'category': 'Education', 'date': 'Dec 17, 2025', 'author': 'Dr. Sarah Ahmed', 'excerpt': 'Discover how our foundation is transforming lives through educational initiatives across Pakistan. We provide scholarships, school supplies, and mentorship programs to help children reach their full potential.', 'content': 'Education is the cornerstone of development and progress. Our foundation has been working tirelessly to provide quality education to underprivileged children across Pakistan. Through our scholarship program, we have supported over 2,000 students in pursuing their dreams.\n\nWe believe that every child deserves access to quality education, regardless of their economic background. Our programs include providing school supplies, building libraries, training teachers, and offering mentorship opportunities. The impact has been tremendous - our students are now pursuing higher education and giving back to their communities.\n\nOur approach is holistic, focusing not just on academic excellence but also on character development, critical thinking, and leadership skills. We work closely with local communities to ensure our programs are culturally sensitive and sustainable.', 'type': 'blog'},
            {'id': 2, 'slug': 'healthcare-services-expand-rural-areas', 'image': 'assets/water.jpg', 'title': 'Healthcare Services Expand to Rural Areas', 'category': 'Healthcare', 'date': 'Dec 15, 2025', 'author': 'Dr. Hassan Malik', 'excerpt': 'Learn about our healthcare programs providing essential medical services to those in need. Our mobile clinics bring doctors and medicines to remote villages that lack basic healthcare infrastructure.', 'content': 'Access to healthcare is a fundamental right, yet millions in rural Pakistan lack basic medical services. Our mobile health clinics are changing this reality by bringing doctors, nurses, and essential medicines directly to remote communities.\n\nThese mobile units are equipped with diagnostic equipment and staffed by qualified medical professionals. They provide free consultations, vaccinations, maternal health services, and treatment for common ailments. Since launching this initiative, we have served over 50,000 patients.\n\nWe also conduct health awareness campaigns, teaching communities about hygiene, nutrition, and disease prevention. This preventive approach is key to building healthier communities in the long term.', 'type': 'blog'},
            {'id': 3, 'slug': 'building-hope-new-community-center-opens', 'image': 'assets/construction.jpg', 'title': 'Building Hope: New Community Center Opens', 'category': 'Infrastructure', 'date': 'Dec 12, 2025', 'author': 'Amina Rashid', 'excerpt': 'A new community center opens its doors in rural Punjab, providing a safe space for education, healthcare, and community gatherings. This marks our 5th community center built this year.', 'content': 'We are thrilled to announce the opening of our latest community center in rural Punjab. This state-of-the-art facility provides a safe and welcoming space for education, healthcare services, vocational training, and community events.\n\nThe center features classrooms, a computer lab, a health clinic, a library, and multipurpose halls. It was built with input from local community members to ensure it meets their specific needs. The construction created jobs for local workers and used locally-sourced materials wherever possible.\n\nThis is our fifth community center this year, and we plan to build many more. These centers serve as hubs of hope, opportunity, and positive change in underserved communities.', 'type': 'blog'},
            {'id': 4, 'slug': 'youth-sports-program-launches', 'image': 'assets/hockey.jpg', 'title': 'Youth Sports Program Launches', 'category': 'Community', 'date': 'Dec 10, 2025', 'author': 'Coach Ahmed Khan', 'excerpt': 'Our new youth sports initiative brings athletics and teamwork training to underprivileged communities. Sports help build confidence, discipline, and leadership skills in young people.', 'content': 'Sports have the power to transform lives, teaching discipline, teamwork, and resilience. Our new youth sports program brings these benefits to underprivileged communities across Pakistan.\n\nWe offer training in cricket, football, hockey, and athletics, led by experienced coaches. The program is free and open to all children aged 8-18. Beyond sports skills, we focus on character development, teaching values like sportsmanship, respect, and perseverance.\n\nEarly results have been amazing - participants show improved confidence, better school attendance, and stronger community bonds. Several talented athletes have already been identified for advanced training programs.', 'type': 'blog'},
            {'id': 5, 'slug': 'scholarship-recipients-share-stories', 'image': 'assets/student.jpg', 'title': 'Scholarship Recipients Share Their Stories', 'category': 'Education', 'date': 'Dec 8, 2025', 'author': 'Fatima Noor', 'excerpt': 'Meet the inspiring students whose lives have been changed through our scholarship program. Their success stories demonstrate the power of education in breaking the cycle of poverty.', 'content': 'Behind every scholarship is a story of hope, determination, and transformation. Today, we share the inspiring journeys of students whose lives have been changed through our scholarship program.\n\nMeet Aisha, who dreamed of becoming a doctor but could not afford school fees. Through our scholarship, she completed her education and is now studying medicine. Then there is Hassan, the first in his family to attend university, now pursuing engineering.\n\nThese success stories motivate us to expand our scholarship program and reach more deserving students. Education truly is the key to breaking the cycle of poverty and creating a brighter future.', 'type': 'blog'},
            {'id': 6, 'slug': 'clean-water-initiative-reaches-10000-families', 'image': 'assets/river.jpg', 'title': 'Clean Water Initiative Reaches 10,000 Families', 'category': 'Infrastructure', 'date': 'Dec 5, 2025', 'author': 'Engineer Bilal Hussain', 'excerpt': 'Our clean water project has successfully provided access to safe drinking water for over 10,000 families. We install water filtration systems and teach communities about water safety and hygiene.', 'content': 'Clean water is essential for health and dignity. Our clean water initiative has reached a major milestone - providing safe drinking water to over 10,000 families in rural Pakistan.\n\nWe install water filtration systems, dig wells, and repair existing water infrastructure. But our work goes beyond infrastructure - we also educate communities about water conservation, hygiene practices, and water-borne disease prevention.\n\nThe impact has been remarkable. Communities report significant reductions in waterborne illnesses, children spend less time fetching water and more time in school, and overall quality of life has improved dramatically.', 'type': 'blog'},
            {'id': 7, 'slug': 'legal-aid-support-services', 'image': 'assets/darbar.jpg', 'title': 'Legal Aid and Support Services', 'category': 'Legal Aid', 'date': 'Dec 3, 2025', 'author': 'Advocate Zainab Ali', 'excerpt': 'Explore our legal aid initiatives helping families navigate complex legal challenges. We provide free legal consultation and representation for those who cannot afford it.', 'content': 'Justice should be accessible to all, regardless of economic status. Our legal aid program provides free legal consultation and representation to those who cannot afford it.\n\nOur team of volunteer lawyers helps with a range of issues including family law, property disputes, labor rights, and human rights cases. We have successfully resolved hundreds of cases, bringing justice and peace of mind to vulnerable families.\n\nWe also conduct legal awareness workshops, teaching communities about their rights and how to access the legal system. Empowering people with legal knowledge is crucial for creating a just society.', 'type': 'blog'},
            {'id': 8, 'slug': 'vocational-training-creates-opportunities', 'image': 'assets/labour.jpg', 'title': 'Vocational Training Creates New Opportunities', 'category': 'Employment', 'date': 'Nov 28, 2025', 'author': 'Muhammad Tariq', 'excerpt': 'Our vocational training programs equip workers with valuable skills for sustainable employment. We offer courses in carpentry, sewing, electrical work, and other trades.', 'content': 'Economic empowerment begins with employable skills. Our vocational training programs provide practical skills training in high-demand trades, opening doors to sustainable employment.\n\nWe offer courses in carpentry, tailoring, electrical work, plumbing, mobile repair, and computer skills. Training is hands-on and industry-aligned, ensuring graduates are job-ready. Many of our graduates have started their own businesses or secured stable employment.\n\nThe program particularly focuses on women and youth, providing them with skills to become economically independent. We also offer business training to help graduates start and manage their own enterprises.', 'type': 'blog'},
            {'id': 9, 'slug': 'partnership-local-organizations', 'image': 'assets/water.jpg', 'title': 'Partnership with Local Organizations', 'category': 'Community', 'date': 'Nov 25, 2025', 'author': 'Nadia Iqbal', 'excerpt': 'Learn how we collaborate with local NGOs and community organizations to maximize our impact. Together, we can reach more people and create lasting positive change.', 'content': 'Collaboration multiplies impact. We work closely with local NGOs, community organizations, and government agencies to maximize our reach and effectiveness.\n\nThese partnerships allow us to leverage local knowledge, avoid duplication of efforts, and ensure our programs are culturally appropriate and sustainable. Together, we have implemented projects in education, healthcare, infrastructure, and economic development.\n\nOur collaborative approach recognizes that lasting change requires collective effort. By working together, we can reach more people and create more meaningful, sustainable impact in communities across Pakistan.', 'type': 'blog'},
            {'id': 10, 'slug': 'women-empowerment-literacy-programs', 'image': 'assets/uni.jpg', 'title': 'Women Empowerment Through Literacy Programs', 'category': 'Education', 'date': 'Nov 22, 2025', 'author': 'Dr. Sana Mahmood', 'excerpt': 'Our women literacy programs are breaking barriers and empowering females across rural Pakistan. Over 500 women have graduated from our basic literacy courses this year, opening doors to new opportunities.', 'content': 'Education empowers women to transform their lives and communities. Our women literacy programs are breaking barriers and creating opportunities for females across rural Pakistan.\n\nOver 500 women have graduated from our basic literacy courses this year. Many have gone on to pursue further education, start small businesses, or become community leaders. The program covers reading, writing, basic math, and life skills.\n\nWe create safe, supportive learning environments where women can learn without fear or judgment. Classes are scheduled to accommodate household responsibilities, and childcare is provided. The transformation we witness in these women - in confidence, agency, and aspirations - is truly inspiring.', 'type': 'blog'},
        ]

        # Dummy news data
        news_posts = [
            {'id': 11, 'slug': 'education-initiative-launches-rural-punjab', 'image': 'assets/uni.jpg', 'title': 'Education Initiative Launches in Rural Punjab', 'category': 'News', 'date': 'Dec 17, 2025', 'author': 'News Desk', 'excerpt': 'Government announces major education reforms for rural areas.', 'content': 'The government has announced a comprehensive education initiative targeting rural areas of Punjab. The program aims to improve literacy rates and provide better educational infrastructure in underserved communities.\n\nKey components include building 100 new schools, training 5,000 teachers, and providing free textbooks to students. The initiative will also focus on increasing girls\' enrollment in schools through awareness campaigns and incentive programs.\n\nEducation Minister stated that this is part of a broader vision to ensure quality education reaches every child in Pakistan, regardless of their geographic location or economic background.', 'type': 'news'},
            {'id': 12, 'slug': 'healthcare-services-expand-sindh', 'image': 'assets/water.jpg', 'title': 'Healthcare Services Expand Across Sindh', 'category': 'News', 'date': 'Dec 16, 2025', 'author': 'News Desk', 'excerpt': 'New mobile health units deployed to remote communities.', 'content': 'The Sindh Health Department has deployed new mobile health units to serve remote communities across the province. These units are equipped with modern medical equipment and staffed by qualified healthcare professionals.\n\nThe mobile clinics will provide free consultations, basic diagnostic services, vaccinations, and maternal health services. They will visit each designated area on a fixed schedule, ensuring regular healthcare access for rural populations.\n\nThis initiative is expected to benefit over 2 million people in remote areas who previously had limited access to healthcare facilities.', 'type': 'news'},
            {'id': 13, 'slug': 'infrastructure-development-balochistan', 'image': 'assets/construction.jpg', 'title': 'Infrastructure Development in Balochistan', 'category': 'News', 'date': 'Dec 15, 2025', 'author': 'News Desk', 'excerpt': 'Major road construction projects underway in rural regions.', 'content': 'Major infrastructure development projects are underway in Balochistan, focusing on improving road connectivity in rural areas. The projects include construction of highways, farm-to-market roads, and bridges.\n\nThese developments are expected to boost economic activity by improving access to markets, schools, and healthcare facilities. The projects are also creating thousands of jobs for local workers.\n\nOfficials stated that improved infrastructure is crucial for the socio-economic development of the region and will help reduce the isolation of remote communities.', 'type': 'news'},
            {'id': 14, 'slug': 'national-sports-initiative-youth', 'image': 'assets/hockey.jpg', 'title': 'National Sports Initiative for Youth', 'category': 'News', 'date': 'Dec 14, 2025', 'author': 'News Desk', 'excerpt': 'Government launches nationwide youth sports program.', 'content': 'A nationwide youth sports initiative has been launched to promote healthy lifestyles and identify sporting talent across Pakistan. The program covers cricket, football, hockey, athletics, and other sports.\n\nSports facilities are being upgraded in schools and communities, and professional coaches are being hired to train young athletes. The program is free and open to all youth aged 10-20.\n\nThis initiative aims to create a pipeline of talented athletes for national teams while also promoting physical fitness and teamwork among the youth.', 'type': 'news'},
            {'id': 15, 'slug': 'clean-water-projects-benefit-thousands', 'image': 'assets/river.jpg', 'title': 'Clean Water Projects Benefit Thousands', 'category': 'News', 'date': 'Dec 13, 2025', 'author': 'News Desk', 'excerpt': 'New water purification plants operational in 10 districts.', 'content': 'New water purification plants have become operational in 10 districts across Pakistan, providing clean drinking water to thousands of families. These plants use modern filtration technology to ensure water safety.\n\nThe projects are part of a larger clean water initiative aimed at reducing waterborne diseases and improving public health. Each plant has the capacity to serve 50,000-100,000 people.\n\nCommunity members have expressed gratitude for access to clean water, noting significant improvements in their families\' health and quality of life.', 'type': 'news'},
            {'id': 16, 'slug': 'job-creation-program-shows-results', 'image': 'assets/labour.jpg', 'title': 'Job Creation Program Shows Results', 'category': 'News', 'date': 'Dec 12, 2025', 'author': 'News Desk', 'excerpt': 'Skills training initiative helps 5000 find employment.', 'content': 'A government-sponsored skills training and job creation program has achieved remarkable success, helping over 5,000 people find employment in various sectors.\n\nThe program provides free vocational training in high-demand fields such as construction, IT, hospitality, and manufacturing. Graduates receive certification and job placement assistance.\n\nThe initiative has been particularly beneficial for youth and women, providing them with skills and opportunities for economic independence and upward mobility.', 'type': 'news'},
            {'id': 17, 'slug': 'digital-literacy-program-reaches-villages', 'image': 'assets/student.jpg', 'title': 'Digital Literacy Program Reaches Villages', 'category': 'News', 'date': 'Dec 11, 2025', 'author': 'News Desk', 'excerpt': 'Free computer training provided to rural youth across Pakistan.', 'content': 'A digital literacy program has been launched in rural areas to equip youth with essential computer and internet skills. Mobile computer labs are visiting villages to provide free training.\n\nThe program covers basic computer operations, internet usage, email, word processing, and digital safety. Upon completion, participants receive certificates that can help them in job searches.\n\nThis initiative aims to bridge the digital divide and ensure rural youth are not left behind in the digital age.', 'type': 'news'},
            {'id': 18, 'slug': 'legal-rights-awareness-campaign', 'image': 'assets/darbar.jpg', 'title': 'Legal Rights Awareness Campaign', 'category': 'News', 'date': 'Dec 10, 2025', 'author': 'News Desk', 'excerpt': 'Citizens educated about fundamental rights and legal procedures.', 'content': 'A nationwide legal rights awareness campaign is educating citizens about their fundamental rights and legal procedures. Lawyers and legal experts are conducting workshops in communities.\n\nThe campaign covers topics such as constitutional rights, family law, property rights, labor laws, and how to access the legal system. Free legal consultation services are also being provided.\n\nThis initiative aims to empower citizens with legal knowledge and ensure they can effectively exercise their rights and seek justice when needed.', 'type': 'news'},
            {'id': 19, 'slug': 'new-universities-open-remote-areas', 'image': 'assets/uni.jpg', 'title': 'New Universities Open in Remote Areas', 'category': 'News', 'date': 'Dec 9, 2025', 'author': 'News Desk', 'excerpt': 'Higher education facilities inaugurated in underserved regions.', 'content': 'New university campuses have been inaugurated in remote and underserved regions of Pakistan, bringing higher education closer to students who previously had limited access.\n\nThese universities offer programs in sciences, humanities, business, and technology. Scholarship programs are available for deserving students, and residential facilities ensure students from far-flung areas can attend.\n\nThe establishment of these institutions is expected to significantly increase higher education enrollment from rural areas and contribute to regional development.', 'type': 'news'},
            {'id': 20, 'slug': 'housing-project-low-income-families', 'image': 'assets/construction.jpg', 'title': 'Housing Project for Low-Income Families', 'category': 'News', 'date': 'Dec 8, 2025', 'author': 'News Desk', 'excerpt': 'Government launches affordable housing scheme for poor families.', 'content': 'An affordable housing scheme has been launched to provide decent housing to low-income families across Pakistan. The project aims to construct 100,000 housing units over the next two years.\n\nEligible families can acquire homes through easy installment plans with subsidized interest rates. The houses are equipped with basic amenities including electricity, water, and sanitation facilities.\n\nThis initiative addresses the critical housing shortage faced by low-income families and aims to improve their living standards and quality of life.', 'type': 'news'},
        ]

        # Combine both lists to search
        all_posts = blog_posts + news_posts

        # Find the post by slug
        post = None
        if slug:
            for p in all_posts:
                if p['slug'] == slug:
                    post = p
                    break

        if not post:
            # If slug not found or not provided, use first blog post
            post = blog_posts[0] if blog_posts else None

        # Get related posts (same category, excluding current post)
        if post:
            related_posts = [p for p in all_posts if p.get('category') == post.get('category') and p['id'] != post['id']][:3]
        else:
            related_posts = []

    context = {
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'blogpost.html', context)


def adminlogin(request):
    """Admin login page - redirects to Django admin"""
    return redirect('/admin/')


def blog_manager_login(request):
    """Login page for Blog Managers"""
    if request.user.is_authenticated:
        return redirect('blogmanagement')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Check if user is a Blog Manager or Super Admin
            is_blog_manager = user.groups.filter(name='Blog Manager').exists()
            is_superuser = user.is_superuser

            if is_blog_manager or is_superuser:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('blogmanagement')
            else:
                messages.error(request, 'You do not have permission to access the blog management system.')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'blog_manager_login.html')


def blog_manager_logout(request):
    """Logout for Blog Managers"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def admincontrols(request):
    """Admin controls dashboard"""
    # Statistics
    total_donations = Donation.objects.filter(payment_status='completed').aggregate(
        total=Sum('amount')
    )['total'] or 0

    total_blog_posts = BlogPost.objects.count()
    pending_testimonials = Testimonial.objects.filter(is_approved=False).count()
    unread_messages = ContactMessage.objects.filter(is_read=False).count()
    total_partners = Partner.objects.filter(is_active=True).count()
    newsletter_subscribers = NewsletterSubscriber.objects.filter(is_active=True).count()

    # Recent activity
    recent_donations = Donation.objects.all()[:5]
    recent_messages = ContactMessage.objects.all()[:5]
    recent_posts = BlogPost.objects.all()[:5]

    context = {
        'total_donations': total_donations,
        'total_blog_posts': total_blog_posts,
        'pending_testimonials': pending_testimonials,
        'unread_messages': unread_messages,
        'total_partners': total_partners,
        'newsletter_subscribers': newsletter_subscribers,
        'recent_donations': recent_donations,
        'recent_messages': recent_messages,
        'recent_posts': recent_posts,
    }
    return render(request, 'admincontrols.html', context)


@login_required
def blogmanagement(request):
    """Blog management page - Dashboard for Blog Managers"""
    # Get all posts created by the current user or all posts if superuser
    if request.user.is_superuser:
        all_posts = BlogPost.objects.all()
    else:
        all_posts = BlogPost.objects.filter(author=request.user)

    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        all_posts = all_posts.filter(status=status_filter)

    # Order by most recent
    all_posts = all_posts.order_by('-created_at')

    context = {
        'posts': all_posts,
        'status_filter': status_filter,
        'is_blog_manager': request.user.groups.filter(name='Blog Manager').exists(),
        'is_superuser': request.user.is_superuser,
    }
    return render(request, 'blogmanagement.html', context)


@login_required
def blog_create(request):
    """Create a new blog post - Blog Managers can create drafts only"""
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        excerpt = request.POST.get('excerpt', '')
        category = request.POST.get('category', 'blog')
        meta_title = request.POST.get('meta_title', '')
        meta_description = request.POST.get('meta_description', '')
        featured_image = request.FILES.get('featured_image')

        # Create blog post
        post = BlogPost.objects.create(
            title=title,
            content=content,
            excerpt=excerpt,
            category=category,
            meta_title=meta_title,
            meta_description=meta_description,
            featured_image=featured_image,
            author=request.user,
            status='draft'  # Always create as draft
        )

        messages.success(request, f'Blog post "{post.title}" created successfully! Status: Draft (pending Super Admin approval)')
        return redirect('blogmanagement')

    context = {
        'is_blog_manager': request.user.groups.filter(name='Blog Manager').exists(),
        'categories': BlogPost.CATEGORY_CHOICES,
    }
    return render(request, 'blog_form.html', context)


@login_required
def blog_edit(request, pk):
    """Edit a blog post - Blog Managers cannot change status to published"""
    post = get_object_or_404(BlogPost, pk=pk)

    # Check permissions
    if not request.user.is_superuser and post.author != request.user:
        messages.error(request, 'You do not have permission to edit this post.')
        return redirect('blogmanagement')

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.excerpt = request.POST.get('excerpt', '')
        post.category = request.POST.get('category', 'blog')
        post.meta_title = request.POST.get('meta_title', '')
        post.meta_description = request.POST.get('meta_description', '')

        if request.FILES.get('featured_image'):
            post.featured_image = request.FILES.get('featured_image')

        # Only superuser can change status
        if request.user.is_superuser:
            post.status = request.POST.get('status', 'draft')
            if request.POST.get('is_featured'):
                post.is_featured = True
            else:
                post.is_featured = False

        post.save()
        messages.success(request, f'Blog post "{post.title}" updated successfully!')
        return redirect('blogmanagement')

    context = {
        'post': post,
        'is_editing': True,
        'is_blog_manager': request.user.groups.filter(name='Blog Manager').exists(),
        'is_superuser': request.user.is_superuser,
        'categories': BlogPost.CATEGORY_CHOICES,
        'statuses': BlogPost.STATUS_CHOICES,
    }
    return render(request, 'blog_form.html', context)


@login_required
def blog_delete(request, pk):
    """Delete a blog post - Only superuser can delete"""
    if not request.user.is_superuser:
        messages.error(request, 'Only Super Admin can delete blog posts.')
        return redirect('blogmanagement')

    post = get_object_or_404(BlogPost, pk=pk)

    if request.method == 'POST':
        title = post.title
        post.delete()
        messages.success(request, f'Blog post "{title}" deleted successfully!')
        return redirect('blogmanagement')

    context = {'post': post}
    return render(request, 'blog_delete_confirm.html', context)


def contact(request):
    """Contact form page"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()

    context = {
        'form': form,
    }
    return render(request, 'contact.html', context)


def newsletter_subscribe(request):
    """Newsletter subscription handler"""
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Successfully subscribed to our newsletter!')
            except:
                messages.info(request, 'You are already subscribed to our newsletter.')
            return redirect(request.META.get('HTTP_REFERER', 'home'))

    return redirect('home')


def donate(request):
    """Donation form page"""
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.payment_status = 'pending'
            donation.save()
            messages.success(request, 'Thank you for your donation! You will receive payment instructions via email.')
            return redirect('home')
    else:
        form = DonationForm()

    partners = Partner.objects.filter(is_active=True)

    context = {
        'form': form,
        'partners': partners,
    }
    return render(request, 'donate.html', context)
