from django import template
from django.db.models import Exists, OuterRef
from django_cte import CTE, with_cte

from ..models import Comment, CommentLike


register = template.Library()


@register.simple_tag(takes_context=True)
def get_all_replies(context, comment):
    base = Comment.objects.filter(pk=comment.pk).values('pk')

    cte = CTE.recursive(
        lambda cte: base.union(
            cte.join(Comment, parent=cte.col.pk).values('pk'), all=True
        )
    )
    qs = with_cte(
        cte,
        select=cte.join(
            Comment, pk=cte.col.pk
        ).exclude(pk=comment.pk).annotate(
            liked_by_user=Exists(
                CommentLike.objects.filter(
                    user=context.get('request').user.profile,
                    comment=OuterRef('pk')
                )
            )
        )
    )

    return qs
