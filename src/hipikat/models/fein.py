
#from django.utils.translation import ugettext_lazy as _
from feincms.module.page.models import Page
from feincms.content.application.models import ApplicationContent
from feincms.content.raw.models import RawContent
from feincms.content.richtext.models import RichTextContent
from feincms.content.medialibrary.models import MediaFileContent
#import feincms_cleanse
#from elephantblog.models import Entry as BlogPost
#from elephantblog.models import Entry as ElephantblogEntry
from elephantblog.models import Entry


#class Entry(ElephantblogEntry):
#    class Meta:
#        proxy = True
#
#    def get_absolute_url(self):
#        print("F*F*F*F*F*")
#        return super(Entry, self).get_absolute_url()

#from feincms.content.application.models import retrieve_page_information
#Page.register_request_processor(retrieve_page_information)
#Entry.register_request_processor(retrieve_page_information)


# feinCMS core page type
Page.register_extensions(
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
Page.create_content_type(RichTextContent)
Page.create_content_type(RawContent)
Page.create_content_type(MediaFileContent, TYPE_CHOICES=(
    ('default', 'default'),
))
Page.create_content_type(ApplicationContent, APPLICATIONS=(
#    ('elephantblog', 'Blog', {'urls': 'elephantblog.urls'}),
    ('elephantblog.urls', 'Blog'),
))

# Elephantblog
Entry.register_extensions(
    #'feincms.module.extensions.changedate',            # Creation and modification dates
    #'feincms.module.extensions.ct_tracker',            # Content type cache
    #'feincms.module.extensions.datepublisher',         # Date-based publishing
    #'feincms.module.extensions.featured',              # Simple featured flag for a page
    'feincms.module.extensions.seo',                    # Search engine optimsation
    #'feincms.module.extensions.translations',          # Page translations
    #'feincms.module.page.extensions.excerpt',          # Page summary
    #'feincms.module.page.extensions.navigation',       # Navigation extensions
    'feincms.module.page.extensions.relatedpages',      # Links related content
    #'feincms.module.page.extensions.sites',            # Limit pages to sites
    #'feincms.module.page.extensions.symlinks',         # Symlinked content extension
    #'feincms.module.page.extensions.titles',           # Additional titles
    'elephantblog.extensions.blogping',
)
Entry.register_regions(
    ('main', 'Main content area'),
)
Entry.create_content_type(RichTextContent)
Entry.create_content_type(RawContent)
Entry.create_content_type(MediaFileContent, TYPE_CHOICES=(
    ('default', 'default'),
))
