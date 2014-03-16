
from django.views.generic import TemplateView
#from elephantblog.models import Entry


class NotConfiguredView(TemplateView):
    template_name = '404.html'
not_configured_view = NotConfiguredView.as_view()


#class ActivityItem(object):
#    """
#    Object representing a "thing that's happened on the site". Each item
#    returns at most one event for being published, updated and created.
#    """
#    #only returns one "most recent thing that's happened", so, for example,
#    #a feed won't contain a 'published' and an 'updated' activity for
#    ACTIVITY_TYPES = {
#        'blog_update': "updated a blog post",
#        'blog_publish': "published a blog post",
#        'blog_draft_update': "updated a draft blog post",
#        'blog_draft_create': "wrote a draft blog post",
#        'random_update': "updated some writing",
#        'random_publish': "wrote something",
#        'random_draft_update': "changed a draft",
#        'random_draft_create': "wrote a draft",
#    }
#
#    def __init__(self, item, *args, **kwargs):
#        self.item = item
#
#    @property
#    def activities(self):
#        """
#        Return a list of `(timedate, activity_type)` tuples, with at most
#        one (the most recent) activity being returned for each of publish,
#        update and create.
#        """
#        item = self.item
#        activities = []
#        if isinstance(item, Entry):
#            entry_type = item.entry_type
#            # TODO: Remove check for not modification_date when pre-migration-4 fixtures are gone.
#            if item.modification_date and\
#                    item.is_final and item.modification_date > item.published_on:
#                activities.append((item.modification_date, entry_type + '_update'))
#            if item.is_final:
#                activities.append((item.published_on, entry_type + '_publish'))
#            else:
#                # TODO: as above
#                if item.modification_date and item.creation_date and\
#                        item.modification_date > item.creation_date:
#                    activities.append((item.modification_date, entry_type + '_draft_update'))
#                # TODO: as above
#                if item.creation_date:
#                    activities.append((item.creation_date, entry_type + '_draft_create'))
#        else:
#            raise NotImplementedError
#        return activities
#
#
## TODO: Implement max_items...
#def get_activity_items(max_items=None):
#    activity_events = []
#    activity_items = [ActivityItem(entry) for entry in Entry.objects.filter(is_active=True)]
#    for activity_item in activity_items:
#        for activity in activity_item.activities:
#            activity_events.append(list(activity) + [activity_item.item])
#    activity_feed = [dict(time=act[0],
#                          activity_type=ActivityItem.ACTIVITY_TYPES[act[1]],
#                          item=act[2])
#                     for act in sorted(activity_events, key=lambda act: act[0], reverse=True)]
#    return activity_feed
