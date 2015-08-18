
from collections import defaultdict
import os
import re
from os import path
from django.conf import settings
from django.views.generic import TemplateView


class TemplateDetail(TemplateView):
    """ 
    Render a template specified by `template_name`.
    """
    def get_template_names(self):
        return [self.kwargs['template_name']]


class TemplateList(TemplateView):
    """ 
    TODO: RE-EVERYTHING
    List HTML files under each directory in ``settings.TEMPLATE_DIRS``,
    with links to the named URL ``debug_template_detail``. Passes the
    (relative) template path as the keyword ``template_name``.
    
    Templates are listed if they match a pattern in ``include_patterns``,
    and do not match any patterns in ``exclude_patterns``; these can be
    set with keyword arguments during class instantiation.
    """
    template_name = 'develop/template_list.html'

    def get_context_data(self, **kwargs):
        """ 
        Add ``template_dirs_names`` to the context; a dictionary with keys from
        ``settings.TEMPLATE_DIRS``, whose values are lists of template names
        with valid patterns.
        """
        template_dirs_names = defaultdict(list)
        for template_dir in settings.TEMPLATE_DIRS:
            for dir_path, dir_names, file_names in os.walk(template_dir):
                for file_name in file_names:
                    template_name = path.join(dir_path, file_name)[len(template_dir)+1:]
                    if self._valid_template(template_name):
                        template_dirs_names[template_dir].append(template_name)
        kwargs.update({ 
            'template_dirs_names': dict(template_dirs_names),
            'include_patterns': self.include_patterns,
            'exclude_patterns': self.exclude_patterns,
        })  
        return super(DebugTemplateListView, self).get_context_data(**kwargs)
        
    def _valid_template(self, template_name):
        """
        Return True if a ``template_name`` matches any pattern in
        ``self.include_patterns`` and does not match any patterns in
        ``self.exclude_patterns``, otherwise return False.
        """
        for pattern in self.exclude_patterns:
            if re.search(pattern, template_name) != None:
                return False
        for pattern in self.include_patterns:
            if re.search(pattern, template_name) != None:
                return True
        return False
