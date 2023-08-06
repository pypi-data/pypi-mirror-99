==========
 Overview
==========


What is zope.app.tree?
======================

ZopeTree is a port of Philipp's Zope2 product ZopeTree. ZopeTree was
meant to be a light-weight and easy-to-use static tree implementation,
mainly designed for use in ZPTs. It was originally written because
Zope2's ``ZTUtils.Tree`` was found to be too complicated and inflexible.

The ``ZTUtils`` package has not been ported to Zope3. Parts of it, like
batching, have found their way into Zope3, though. Only support for
static tree generation is not in the core.


How to use it
=============

Using the skin
--------------

ZopeTree comes with a pre-defined skin, :class:`StaticTree
<zope.app.tree.browser.IStaticTreeSkin>`. It looks just like Zope3's
default skin, :class:`zope.app.rotterdam.Rotterdam`, except that it
displays a static tree in the navigation box instead of the
Javascript/XML based dynamic tree.

Using predefined views on objects
---------------------------------

ZopeTree comes with several predefined views:

:meth:`cookie_tree <zope.app.tree.browser.cookie.CookieTreeView.cookieTree>`
  simple view using cookies for tree state storage.

:meth:`folder_cookie_tree <zope.app.tree.browser.cookie.CookieTreeView.folderTree>`
  same as above, however only showing folders.

:meth:`site_cookie_tree <zope.app.tree.browser.cookie.CookieTreeView.siteTree>`
  same as above, with the nearest site as root node.

:meth:`root_cookie_tree <zope.app.tree.browser.cookie.CookieTreeView.rootTree>`
  same as above, with the traversal root container as root node.

:meth:`virtualhost_cookie_tree <zope.app.tree.browser.cookie.CookieTreeView.virtualHostTree>`
  same as above, but using the request's virtual host root instead of
  the traversal root.

The example page template(s) in the browser package give an idea how
to use these views for HTML templating.

Customization
=============

The best way to customize ZopeTree is to define your own view for
objects (usually '*'). If you want to use the cookie functionality,
simply extend the cookie browser view::

  >>> from zope.app.tree.filters import OnlyInterfacesFilter
  >>> from zope.app.tree.browser.cookie import CookieTreeView

  >>> class BendableStaticTreeView(CookieTreeView):
  ...
  ...  def bendablesTree(self):
  ...        # tree with only IBendables, but also show the folder
  ...        # they're in
  ...        filter = OnlyInterfacesFilter(IBendable, IFolder)
  ...        return self.cookieTree(filter)

You can also write your own filters. All you have to do is implement
the IObjectFindFilter interface (which is trivial)::

  >>> from zope.interface import implementer
  >>> from zope.container.interfaces import IObjectFindFilter

  >>> @implementer(IObjectFindFilter)
  ... class BendableFilter(object):
  ...
  ...    def matches(self, obj):
  ...        # only allow bendable objects
  ...        return obj.isBendable()


License and Copyright
=====================

This product is released under the terms of the `Zope Public License
(ZPL) v2.1`__.

Copyright (c) 2003 Philipp "philiKON" von Weitershausen
Copyright (c) 2004 Zope Corporation and Contributors

.. __: http://www.zope.org/Resources/ZPL/ZPL-2.1


Credits
=======

Thanks to ZopeMag (http://zopemag.com) for sponsoring development of
the original ZopeTree product.

Thanks to Runyaga LLC (http://runyaga.com) for sponsoring the Zope3
port.
