
import random
from django.contrib.auth import get_user_model
import factory
from factory import LazyAttribute
from faker import Faker
#from django.utils.translation import ugettext_lazy as _
from feincms.module.page.models import Page
from feincms.content.application.models import ApplicationContent
from feincms.content.raw.models import RawContent
from feincms.content.richtext.models import RichTextContent
from feincms.content.medialibrary.models import MediaFileContent
from elephantblog.models import Entry


#from feincms.content.application.models import retrieve_page_information
#Page.register_request_processor(retrieve_page_information)
#Writing.register_request_processor(retrieve_page_information)


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
    #('elephantblog', 'Blog', {'urls': 'elephantblog.urls'}),
    ('elephantblog.urls', 'Blog'),
))

# Elephantblog

#class Writing(Entry):
#
#    objects = EntryManager()
#
#    class Meta:
#        app_label = 'hipikat'
#        get_latest_by = 'published_on'
#        ordering = ['-published_on']
#        verbose_name = 'writing'
#        verbose_name_plural = 'writings'
#
#    #def get_absolute_url(self):
#    #    print("F*F*F*F*F*")
#    #    return super(Writing, self).get_absolute_url()
#
#
#class WritingAdmin(EntryAdmin):
#    pass
#
#Writing.register_extensions(
#    #'feincms.module.extensions.changedate',            # Creation and modification dates
#    #'feincms.module.extensions.ct_tracker',            # Content type cache
#    #'feincms.module.extensions.datepublisher',         # Date-based publishing
#    #'feincms.module.extensions.featured',              # Simple featured flag for a page
#    'feincms.module.extensions.seo',                    # Search engine optimsation
#    #'feincms.module.extensions.translations',          # Page translations
#    'feincms.module.page.extensions.excerpt',          # Page summary
#    #'feincms.module.page.extensions.navigation',       # Navigation extensions
#    'feincms.module.page.extensions.relatedpages',      # Links related content
#    #'feincms.module.page.extensions.sites',            # Limit pages to sites
#    #'feincms.module.page.extensions.symlinks',         # Symlinked content extension
#    #'feincms.module.page.extensions.titles',           # Additional titles
#    'elephantblog.extensions.blogping',
#)
#Writing.register_regions(
#    ('main', 'Main content area'),
#)
#Writing.create_content_type(RichTextContent)
#Writing.create_content_type(RawContent)
#Writing.create_content_type(MediaFileContent, TYPE_CHOICES=(
#    ('default', 'default'),
#))
#
#
#class WritingFactory(factory.Factory):
#    """
#    Just starting to play with factory_boy; not used anywhere in code yet.
#    """
#    FACTORY_FOR = Writing
#
#    is_active = True
#    is_featured = True


#################################

# Elephantblog
Entry.register_extensions(
    'feincms.module.extensions.changedate',            # Creation and modification dates
    #'feincms.module.extensions.ct_tracker',            # Content type cache
    #'feincms.module.extensions.datepublisher',         # Date-based publishing
    #'feincms.module.extensions.featured',              # Simple featured flag for a page
    'feincms.module.extensions.seo',                    # Search engine optimsation
    #'feincms.module.extensions.translations',          # Page translations
    'feincms.module.page.extensions.excerpt',          # Page summary
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


# Fake model generation
MIN_TITLE_LENGTH, MAX_TITLE_LENGTH = 10, 70
MIN_PARAGRAPHS, MAX_PARAGRAPHS = 1, 10
fake = Faker()


class EntryFactory(factory.Factory):
    """
    Just starting to play with factory_boy; not used anywhere in code yet.
    """
    FACTORY_FOR = Entry

    is_final = LazyAttribute(lambda obj: random.choice((True, False)))
    is_active = LazyAttribute(lambda obj: random.choice((True, False)))
    is_featured = LazyAttribute(lambda obj: random.choice((True, False)))
    entry_type = LazyAttribute(lambda obj: random.choice(Entry.ENTRY_TYPES.keys()))

    @classmethod
    def _get_title(cls, obj):
        title_parts = fake.text(random.randrange(MIN_TITLE_LENGTH, MAX_TITLE_LENGTH)).split()
        info_parts = []
        for part in ('entry_type', 'is_final', 'is_active', 'is_featured'):
            info_parts.append('{}={}'.format(part, getattr(obj, part)))
        title_parts[1:4] = info_parts
        title = ' '.join(title_parts)
        while len(title) > 100:
            title_parts.pop()
            title = ' '.join(title_parts)
        return ' '.join(title_parts)

    title = LazyAttribute(lambda obj: EntryFactory._get_title(obj))
    slug = LazyAttribute(lambda obj: fake.slug(' '.join(obj.title.split()[0:5])))
    author = get_user_model().objects.all()[0]
    excerpt = LazyAttribute(lambda obj: '<p>{}</p>'.format('</p><p>'.join(
                            fake.paragraphs(random.randrange(1, 3)))))
