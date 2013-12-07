Hipikat.org
===========

Source code for Adam Wright's personal website at http:/hipikat.org/. 
I put this online as a portfolio, and in case you'd like to see how
anything is done or copy my work. Everything required to get the site
up is included in this repository, with the obvious exception of secret
keys and such. :smile_cat:

Main technology stack
---------------------

**Backend** • The site is based on the Django_ web framework, with
feinCMS_ and a `modified fork`_ of ElephantBlog_. I use django-hosts_
for managing links between sub-domains.

.. _Django: https://www.djangoproject.com
.. _feinCMS: http://www.feincms.org
.. _modified fork: https://github.com/hipikat/feincms-elephantblog
.. _ElephantBlog: https://feincms-elephantblog.readthedocs.org
.. _django-hosts: http://django-hosts.readthedocs.org

**Frontend** • Layout is implemented with the grid system from
`Zurb Foundation`_, and styles are compiled from Sass_, using Compass_'s
typographic components.

.. _`Zurb Foundation`: http://foundation.zurb.com
.. _Sass: http://sass-lang.com
.. _Compass: http://compass-style.org

Personal projects in the mix
----------------------------

More than anything, having a personal site gives me a low-risk (but
production) area to experiment with my own packages. Currently approaching
beta, `django-cinch`_ is a package for writing modular, class-based
settings in Django projects - take a look at `this site's settings module`_,
to get a quick idea of what it does.

.. _django-cinch: https://github.com/hipikat/django-cinch
.. _this site's settings module: https://github.com/hipikat/hipikat.org/blob/develop/src/hipikat/settings/__init__.py

Besides that, I'm working on a lightweight deployment suite called scow_,
for projects targetting uWSGI_ + `DigitalOcean`_ + Ubuntu_ + Nginx_,
which wraps Fabric_. Several other potential projects live in
`django-revkom`_, which is basically my personal in vitro development
package.

.. _scow: https://github.com/hipikat/scow
.. _uWSGI: http://projects.unbit.it/uwsgi/
.. _DigitalOcean: http://digitalocean.com
.. _Ubuntu: http://www.ubuntu.com
.. _Nginx: http://nginx.org
.. _Fabric: http://fabfile.org
.. _django-revkom: https://github.com/hipikat/django-revkom
