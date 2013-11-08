
from feincms.module.page.models import Page
from feincms.content.richtext.models import RichTextContent
from feincms.content.medialibrary.models import MediaFileContent

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
})

Page.create_content_type(RichTextContent)
Page.create_content_type(MediaFileContent, TYPE_CHOICES=(
    ('default', 'default'),
    ('lightbox', 'lightbox'),
))
