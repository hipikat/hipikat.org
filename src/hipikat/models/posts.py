
from django.db import models
from django.utils.translation import ugettext as _
from revkom.models import ProjectModel, ProjectManager


class PostManager(ProjectManager):
    pass


class Post(ProjectModel):
    published = models.BooleanField(default=False,
        help_text=_("Published posts may be displayed."))
    updated_date = models.DateTimeField(auto_now=True,
        help_text=_("Last updated date and time."))
