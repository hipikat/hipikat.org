
from django.conf import settings
from django.views.generic import TemplateView

from hipikat.models import Post


class MainLandingView(TemplateView):
    template_name = 'landing-main.html'

    def get_context_data(self, **kwargs):
        recent_count = settings.SITE_RECENT_POST_COUNT
        context = super(FrontPageView, self).get_context_data(**kwargs)
        recent_posts = Post.objects.filter(published=True).order_by("updated_date")
        try:
            context['posts'] = recent_posts[recent_count]
        except IndexError:
            context['posts'] = list(recent_posts)
        return context
main_landing_view = MainLandingView.as_view
