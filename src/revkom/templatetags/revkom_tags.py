
import logging
from functools import wraps

from django.template import Library, TemplateSyntaxError, Variable, Node


register = Library()


def split_token(tag_func):
    """
    Decorator for template tag callables which splits the passed token
    (an instance of django.template.Token) with its own split_contents()
    function, and passes the result to the callable as *args.
    """
    @wraps(tag_func)
    def wrapper(parser, token):
        try:
            return tag_func(*token.split_contents())
        except TypeError:
            raise TemplateSyntaxError('Bad arguments for tag "%s"' %
                                               token.split_contents()[0])
    return wrapper


class TemplateTag(object):
    pass


class URLResolverWithGET(TemplateTag):
    """
    {% url_update_GET 'login' next=this_url dynarg='foo' %}
    {% url_with_GET 'login' next=this_url dynarg='foo' %}
    {% url_GET_string next=this_url dynarg='foo' %}
    """
    def __init__(self, token, *args, **kwargs):
        self.token = token

    def as_tag(update, *args, **kwargs):
        pass
        # TODO

#register.tag(name="url_update_GET", URLResolverWithGet.as_tag(update=True))


class AppendGetNode(Node):
    def __init__(self, dict):
        self.dict_pairs = {}
        for pair in dict.split(','):
            pair = pair.split('=')
            self.dict_pairs[pair[0]] = Variable(pair[1])

    def render(self, context):
        get = context['request'].GET.copy()
        for key in self.dict_pairs:
            get[key] = self.dict_pairs[key].resolve(context)
        path = context['request'].META['PATH_INFO']
        if len(get):
            path += "?%s" % "&".join(["%s=%s" %
                    (key, value) for (key, value) in get.items() if value]
            )
        return path


@register.tag()
@split_token
def append_to_get(_tag_name, dict):
    return AppendGetNode(dict)

