from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_text
from django_comments.managers import CommentManager


class MoloCommentManager(CommentManager):

    def for_model(self, model):
        """
        QuerySet for all comments for a particular model (either an instance or
        a class).
        """
        ct = ContentType.objects.get_for_model(model)
        qs = self.get_queryset().filter(content_type=ct)
        if isinstance(model, models.Model):
            qs = qs.filter(object_pk=force_text(model._get_pk_val()))
        return qs
