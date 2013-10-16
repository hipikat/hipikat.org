
from django.conf import settings
from django.views.generic import TemplateView

from hipikat.models import Post


__all__ = ['MainLandingView', 'main_landing_view',]


class MainLandingView(TemplateView):
    template_name = 'landing-main.html'

    def get_context_data(self, **kwargs):
        recent_count = settings.SITE_RECENT_POST_COUNT
        context = super(MainLandingView, self).get_context_data(**kwargs)
        recent_posts = Post.objects.filter(published=True).order_by("updated_date")
        try:
            context['posts'] = recent_posts[recent_count]
        except IndexError:
            context['posts'] = list(recent_posts)
        return context

    #def dispatch(self, request, *args, **kwargs):
    #    import pdb; pdb.set_trace()
    #    return super(MainLandingView, self).dispatch(request, *args, **kwargs)

    def render_to_response(self, *args, **kwargs):
        response = super(MainLandingView, self).render_to_response(*args, **kwargs)
        import pdb; pdb.set_trace()
        return response

main_landing_view = MainLandingView.as_view
