'''
    aggregator
    ~~~~~~~~~~

    Aggregates multiple posts into single pages.

    :copyright: Copyright 2011 by Vlad Riscutia.
    :license: FreeBSD, see LICENSE file
'''
import copy
from tinkerer.ext import patch



def make_aggregated_pages(app):
    '''
    Generates aggregated pages.
    '''
    env = app.builder.env

    # get post groups
    groups = [env.blog_posts[i:i+10] for i in range(0, len(env.blog_posts), 10)]

    # for each group
    for i, posts in enumerate(groups):
        # initialize context
        context = { 
            "prev": {},
            "next": {},
            "posts": []
        }

        # add posts to context
        for post in posts:
            # deepcopy metadata and patch links
            metadata = copy.deepcopy(env.blog_metadata[post])
            metadata.body = patch.patch_links(metadata.body, post[:11])
            context["posts"].append(metadata)

            # hyperlink title
            context["posts"][-1].body = context["posts"][-1].hyperlink_title(post)

        # handle navigation
        if i == 0:
            # first page doesn't have prev link and its title is "Home"
            pagename = "index"
            context["prev"] = None
            context["title"] = "Home"
        else:
            # following pages prev-link to previous page (titled as "Newer")
            pagename = "page%d" % i
            context["prev"]["title"] = "Newer"
            context["prev"]["link"] = "index.html" if i == 1 else "page%d.html" % (i - 1)
            context["title"] = "Page %d" % (i + 1)

        if i == len(groups) - 1:
            # last page doesn't have next link
            context["next"] = None
        else:
            # other pages next-link to following page (titled as "Older")
            context["next"]["title"] = "Older"
            context["next"]["link"] = "page%d.html" % (i + 1)

        yield (pagename, context, "aggregated.html")

