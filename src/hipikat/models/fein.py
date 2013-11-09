
from feincms.module.page.models import Page
from feincms.content.application.models import ApplicationContent
from feincms.content.richtext.models import RichTextContent
from feincms.content.medialibrary.models import MediaFileContent
#import feincms_cleanse
#from elephantblog.models import Entry as BlogPost
from elephantblog.models import Entry

# Templates and regions
Page.register_templates({
    'title': 'Standard page',
    'path': 'layouts/standard.html',
    'regions': (
        ('main', 'Main content area'),
    ),
}, {
    'title': 'Front page',
    'path': 'layouts/front_page.html',
    'regions': (
        ('vanity-links', 'Vanity links'),
        ('epic-hello', 'Epic hello'),
    ),
})
Entry.register_regions(
    ('main', 'Main content area'),
)
for post_class in (Page, Entry):
    post_class.create_content_type(RichTextContent)
    post_class.create_content_type(MediaFileContent, TYPE_CHOICES=(
        ('default', 'default'),
        ('lightbox', 'lightbox'),
    ))

# Page extensions
#for post_class in (Page, BlogPost):
for post_class in (Page,):
    post_class.register_extensions(
        'feincms.module.extensions.changedate',             # Creation and modification dates
        #'feincms.module.extensions.ct_tracker',            # Content type cache
        'feincms.module.extensions.datepublisher',          # Date-based publishing
        #'feincms.module.extensions.featured',              # Simple featured flag for a page
        'feincms.module.extensions.seo',                    # Search engine optimsation
        #'feincms.module.extensions.translations',          # Page translations
        'feincms.module.page.extensions.excerpt',           # Page summary
        'feincms.module.page.extensions.navigation',        # Navigation extensions
        'feincms.module.page.extensions.relatedpages',      # Links related content
        #'feincms.module.page.extensions.sites',            # Limit pages to sites
        'feincms.module.page.extensions.symlinks',          # Symlinked content extension
        'feincms.module.page.extensions.titles',            # Additional titles
    )


# Integrate ElephantBlog as a feinCMS content type
Page.create_content_type(ApplicationContent, APPLICATIONS=(
    ('elephantblog.urls', 'Blog post'),
))
