from import_export import resources
from import_export.fields import Field

from molo.commenting.models import MoloComment


class MoloCommentsResource(resources.ModelResource):
    # see dehydrate_ functions below
    article_title = Field()
    article_subtitle = Field()
    article_full_url = Field()
    parent_id = Field()
    country = Field()

    class Meta:
        model = MoloComment

        exclude = ('site', 'comment_ptr', 'content_type', 'object_pk',
                   'user', 'user_url', 'lft', 'rght',
                   'tree_id', 'level', 'ip_address', )

        export_order = (
            'country', 'submit_date', 'user_name', 'user_email', 'comment',
            'id', 'parent_id', 'article_title', 'article_subtitle',
            'article_full_url', 'is_public', 'is_removed')

    def dehydrate_country(self, comment):
        dehydrated_country = ''

        if comment.content_object:
            site = comment.content_object.get_site()
            dehydrated_country = site.root_page.title

        return dehydrated_country

    def dehydrate_article_title(self, comment):
        if not comment.content_object or not \
                hasattr(comment.content_object, 'title'):
            return ''

        return comment.content_object.title

    def dehydrate_article_subtitle(self, comment):
        if not comment.content_object or not \
                hasattr(comment.content_object, 'subtitle'):
            return ''

        return comment.content_object.subtitle

    def dehydrate_article_full_url(self, comment):
        if not comment.content_object or not \
                hasattr(comment.content_object, 'full_url'):
            return ''

        return comment.content_object.full_url

    def dehydrate_parent_id(self, comment):
        if comment.parent:
            return comment.parent.id

        return ''
