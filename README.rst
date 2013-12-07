Hipikat.org
===========

Source code for Adam Wright's personal website at http:/hipikat.org/. 
I put this online as a portfolio, and in case you'd like to see how
anything is done or copy my work. Everything required to get the site
up is included in this repository, with the obvious exception of secret
keys and such. 😊

Technology stack
----------------

**Backend** • The site is based on the Django_ web framework, with feinCMS_
and a `modified fork`_ of ElephantBlog_. I use django-hosts_
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

My projects
-----------

More than anything, having a personal site gives me a low-risk, production
area to experiment with my own packages.

- django-revkom_ - My library for in vitro, generic, not-yet-packaged code
- django-cinch_ - An app for class-based Django settings
- django-slater_ - A small suite of debugging tools for Django.

.. _django-revkom: https://github.com/hipikat/django-revkom
.. _django-cinch: https://github.com/hipikat/django-cinch
.. _django-slater: https://github.com/hipikat/django-slater

Other tools involved in the creation of the site include PostgreSQL_,
Git_, Vim_, and and 11-inch, Mid 2011 MacBook Air.

.. _PostgreSQL: http://www.postgresql.org
.. _Git: http://git-scm.com
.. _Vim: http://www.vim.org

TODO: Get deployment working with Salt Stack? Maybe with Vagrant?
More tests.
