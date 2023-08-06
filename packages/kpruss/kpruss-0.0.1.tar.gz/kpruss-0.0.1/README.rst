Keith's Website Theme
=====================

This package is the Sphinx_ theme for use by my projects and website.
The base design started from the `Jekyll Now`_ them I started with, but
I've modified some of the base styling, structural names, updated the
link images in the footer (based on the usage details for each website),
and adapted it to work with Sphinx_.

Theme Options
-------------

The theme aims to be light weight and only has a few options.  These are
focused on my wants for my website.  These include:

``author``
    The author of the website (me).  This is placed in the masthead of
    each page with the project name beneath and is a link to the main
    page.  If this is not give, the project name is used as the main
    link.

``avatar``
    The URL to the author's Gravatar_.  This logo is placed in the
    masthead to the left of the author (or project).

``email``
    An email address to use for the email link in the footer.

``github``
    The author's Github handle (creates a link to the profile using the
    Github logo in the footer).

``linkedin``
    The author's LinkedIn handle (creates a link to the profile using
    the LinkedIn logo in the footer).

``stackoverflow``
    The author's Stack Overflow user ID (creates a link to the profile
    using the Stack Overflow logo in the footer).

Customization
-------------

The theme relies primarily on CSS to manage the customization.  The new
classes it defines are “abstract” and “by-line” for the post layout (see
below).  It uses the following CSS variables to set the basic colors:

``--foreground``
    The color of the main text.

``--background``
    The background color of the websites.

``--headers``
    The color of the headers.

``--quotes``
    The color of block quotes and level four headers.

``--links``
    The color of links.

``--footer``
    The background color of the footer, the border below the
    masthead, and the admonitions.

``--main-font``
    The list of fonts to use for the main text.

``--code-font``
    The list of fonts to use for code blocks.

To override these values (or redefine any other settings), create a
“custom.html” and place it on the html_static_path_.  To see the default
settings, use ``python -m kpruss {base,variables}``.

The theme defines an additional page for blog posts.  This is just a
normal page, but it defines an “abstract” class that should be the first
paragraph to summarize the post.  It will also typeset the author and
date from the metadata as a by-line after the post.  To create a post,
add the following metadata before the title of a post::

    :author: A. Nonymous
    :date: 2021-03-21
    :template: post.html

    Post Title
    ==========

    .. container:: abstract

        The abstract of the post.

    The content of the post.

The key metadata value is the ``:template:``.  The page.html template
will use this template to generate the page.  To add a custom template,
place it on the html_static_path_.  This template should extend the
basic page.html template.

This theme defines the template block ``headernav`` within the masthead
in the layout.  This placed at the end of the ``<header>`` and is
designed for the “Blog” and “About” navigation buttons from the original
`Jekyll Now`_ template.  The following custom ``layout.html`` would add
the links these to the header (mind the version skew regarding
root_doc_)::

    {%- extends !layout.html %}
    {%- block headernav %}
    <nav>
      <a href="{{ pathto(root_doc) }}/blog">Blog</a>
      <a href="{{ pathto(root_doc) }}/about">About</a>
    </nav>
    {{ super() }}
    {%- endblock %}

Contributing
------------

Thank you for you interest in improving my Sphinx_ theme.  It is open
sourced under the `BSD 2-Clause License`_ like `Jekyll Now`_, and I
welcome feedback via bug reports, feature requests, and pull requests.
Please report all bug reports or request a feature by submitting an
issue on the Github_ project page.

.. _Sphinx: https://sphinx-doc.org
.. _Jekyll Now: https://github.com/barryclark/jekyll-now
.. _Gravatar: https://en.gravatar.com
.. _root_doc: https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-root_doc
.. _html_static_path: https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_static_path
.. _BSD 2-Clause License: https://opensource.org/licenses/BSD-2-Clause
.. _Github: https://github.com/kprussing/kpruss
