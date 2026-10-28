from django.core.management.base import BaseCommand
from apps.accounts.management.commands.createuser import Command as UserCreateCommand
from apps.accounts.management.commands.follow import Command as FollowCreateCommand
from apps.blog.management.commands.createpost import Command as PostCreateCommand
from apps.blog.management.commands.postlike import Command as PostLikeCreateCommand
from apps.blog.management.commands.postview import Command as PostViewCreateCommand
from apps.comment.management.commands.comment import Command as CommentCreateCommand
from apps.comment.management.commands.reply import Command as ReplyCreateCommand
from apps.comment.management.commands.comment_like import Command as CommentLikeCreateCommand
from apps.accounts.models import Profile
import math
import random


class Command(BaseCommand):
    """
    A command for generating multiple posts with different user objects
    (as author) using "handle_post_create" method from create_post command.
    """
    help = 'Generates multiple posts with different users using create_post command'

    def add_arguments(self, parser):
        parser.add_argument('-i', '--iteration', type=int, default=30)
        parser.add_argument('-c', '--count', type=int, default=None)
        parser.add_argument('-t', '--timeout', type=int, default=3)

    def handle(self, *args, **options):
        result = ' RESULT '
        user_creator = UserCreateCommand()
        follow_creator = FollowCreateCommand()
        post_creator = PostCreateCommand()
        post_like_creator = PostLikeCreateCommand()
        post_view_creator = PostViewCreateCommand()
        comment_creator = CommentCreateCommand()
        reply_creator = ReplyCreateCommand()
        comment_like_creator = CommentLikeCreateCommand()
        follows_count = 0
        posts = []
        post_like_count = 0
        post_view_count = 0
        comments = []
        replies = []
        comment_like_count = 0

        dependencies = post_creator.check_dependencies()
        if not dependencies:
            msg = 'NO POST OBJECT CREATED.'
            self.stdout.write(
                '=' * (
                    math.ceil(len(msg) / 2) - math.ceil(len(result) / 2) - 1
                ) + result + '=' * (
                    math.ceil(len(msg) / 2) - math.ceil(len(result) / 2)
                )
            )
            self.stdout.write(msg)
            self.stdout.write('=' * len(msg))
            return

        for iteration in range(options.get('iteration')):
            if iteration != 0:
                self.stdout.write('\n')
            self.stdout.write(self.style.SUCCESS('=' * (len(str(iteration + 1)) + 10 + (6 * 2))))
            self.stdout.write(self.style.SUCCESS((' ' * 6) + f'ITERATION {iteration + 1}'))
            self.stdout.write(self.style.SUCCESS('=' * (len(str(iteration + 1)) + 10 + (6 * 2))))
            self.stdout.write('\n')

            stg1 = 'STAGE 1: GENERATE USER OBJECT'
            self.stdout.write('=' * (len(stg1) + (6 * 2)))
            self.stdout.write((' ' * 6) + stg1)
            self.stdout.write('=' * (len(stg1) + (6 * 2)))
            self.stdout.write('\n')
            _, profile_obj = user_creator.handle_user_create(options.get('timeout'))

            ids = list(Profile.objects.values_list('pk', flat=True))
            profiles_ids = random.sample(ids, k=min(10, len(ids)))
            profiles = [Profile.objects.get(pk=id) for id in profiles_ids]

            stg2 = 'STAGE 2: GENERATE FOLLOW OBJECTS'
            self.stdout.write('\n')
            self.stdout.write('=' * (len(stg2) + (6 * 2)))
            self.stdout.write((' ' * 6) + stg2)
            self.stdout.write('=' * (len(stg2) + (6 * 2)))
            self.stdout.write('\n')
            follows_in_iteration = follow_creator.handle_follow_create(
                profiles=profiles,
                profile_obj=profile_obj
            )

            stg3 = 'STAGE 3: GENERATE POST OBJECTS'
            self.stdout.write('\n')
            self.stdout.write('=' * (len(stg3) + (6 * 2)))
            self.stdout.write((' ' * 6) + stg3)
            self.stdout.write('=' * (len(stg3) + (6 * 2)))
            self.stdout.write('\n')
            posts_in_iteration = post_creator.handle_post_create(
                options.get('count') or random.randint(1, 3),
                timeout=options.get('timeout'),
                profile_obj=profile_obj
            )

            posts = posts_in_iteration

            stg4 = 'STAGE 4: GENERATE POSTLIKE OBJECTS'
            self.stdout.write('\n')
            self.stdout.write('=' * (len(stg4) + (6 * 2)))
            self.stdout.write((' ' * 6) + stg4)
            self.stdout.write('=' * (len(stg4) + (6 * 2)))
            self.stdout.write('\n')
            post_likes_in_iteration = post_like_creator.handle_postlike_create(
                posts=posts,
                profile_obj=profile_obj
            )

            stg5 = 'STAGE 5: GENERATE POSTVIEW OBJECTS'
            self.stdout.write('\n')
            self.stdout.write('=' * (len(stg5) + (6 * 2)))
            self.stdout.write((' ' * 6) + stg5)
            self.stdout.write('=' * (len(stg5) + (6 * 2)))
            self.stdout.write('\n')
            post_views_in_iteration = post_view_creator.handle_postview_create(
                posts=posts,
                profile_obj=profile_obj
            )

            stg6 = 'STAGE 6: GENERATE COMMENT OBJECTS'
            self.stdout.write('\n')
            self.stdout.write('=' * (len(stg6) + (6 * 2)))
            self.stdout.write((' ' * 6) + stg6)
            self.stdout.write('=' * (len(stg6) + (6 * 2)))
            self.stdout.write('\n')
            comments_in_iteration = comment_creator.handle_comment_create(
                posts=posts,
                profile_obj=profile_obj
            )

            comments = comments_in_iteration

            stg7 = 'STAGE 7: GENERATE COMMENT (REPLY) OBJECTS'
            self.stdout.write('\n')
            self.stdout.write('=' * (len(stg7) + (6 * 2)))
            self.stdout.write((' ' * 6) + stg7)
            self.stdout.write('=' * (len(stg7) + (6 * 2)))
            self.stdout.write('\n')
            replies_in_iteration = reply_creator.handle_reply_create(
                comments=comments,
                profile_obj=profile_obj
            )

            stg8 = 'STAGE 8: GENERATE COMMENTLIKE OBJECTS'
            self.stdout.write('\n')
            self.stdout.write('=' * (len(stg8) + (6 * 2)))
            self.stdout.write((' ' * 6) + stg8)
            self.stdout.write('=' * (len(stg8) + (6 * 2)))
            self.stdout.write('\n')
            comment_likes_in_iteration = comment_like_creator.handle_commentlike_create(
                comments=comments,
                profile_obj=profile_obj
            )

            follows_count += follows_in_iteration
            posts += [posts_in_iteration]
            post_like_count += post_likes_in_iteration
            post_view_count += post_views_in_iteration
            comments += [comments_in_iteration]
            replies += [replies_in_iteration]
            comment_like_count += comment_likes_in_iteration

        longest = lambda a, b, c, d, e, f, g: max(a, b, c, d, e, f, g, key=len)
        biggest = lambda a, b, c, d, e, f, g: max(a, b, c, d, e, f, g)

        follow_msg = ' FOLLOW OBJECT(S) HAVE BEEN CREATED SUCCESSFULLY.'
        post_msg = ' POST OBJECT(S) HAVE BEEN CREATED SUCCESSFULLY.'
        post_like_msg = ' POSTLIKE OBJECT(S) HAVE BEEN CREATED SUCCESSFULLY.'
        post_view_msg = ' POSTVIEW OBJECT(S) HAVE BEEN CREATED SUCCESSFULLY.'
        comment_msg = ' COMMENT OBJECT(S) HAVE BEEN CREATED SUCCESSFULLY.'
        reply_msg = ' COMMENT (REPLY) OBJECT(S) HAVE BEEN CREATED SUCCESSFULLY.'
        comment_like_msg = ' COMMENTLIKE OBJECT(S) HAVE BEEN CREATED SUCCESSFULLY.'

        self.stdout.write('\n')
        self.stdout.write(self.style.SUCCESS(
            '=' * (
                len(str(
                    biggest(
                        follows_count,
                        len(posts),
                        post_like_count,
                        post_view_count,
                        len(comments),
                        len(replies),
                        comment_like_count
                    )
                )) + math.ceil(len(
                    longest(
                        follow_msg,
                        post_msg,
                        post_like_msg,
                        post_view_msg,
                        comment_msg,
                        reply_msg,
                        comment_like_msg
                    )
                ) / 2) - math.ceil(len(result) / 2) - 1
            ) + result + '=' * (
                math.ceil(len(
                    longest(
                        follow_msg,
                        post_msg,
                        post_like_msg,
                        post_view_msg,
                        comment_msg,
                        reply_msg,
                        comment_like_msg
                    )
                ) / 2) - math.ceil(len(result) / 2)
            )
        ))

        if follows_count != 0:
            self.stdout.write(self.style.SUCCESS(str(follows_count) + follow_msg))
        else:
            self.stdout.write(self.style.SUCCESS('NO FOLLOW OBJECT CREATED.'))
        if len(posts) != 0:
            self.stdout.write(self.style.SUCCESS(str(len(posts)) + post_msg))
        else:
            self.stdout.write(self.style.SUCCESS('NO POST OBJECT CREATED.'))
        if post_like_count != 0:
            self.stdout.write(self.style.SUCCESS(str(post_like_count) + post_like_msg))
        else:
            self.stdout.write(self.style.SUCCESS('NO POSTLIKE OBJECT CREATED.'))
        if post_view_count != 0:
            self.stdout.write(self.style.SUCCESS(str(post_view_count) + post_view_msg))
        else:
            self.stdout.write(self.style.SUCCESS('NO POSTVIEW OBJECT CREATED.'))
        if len(comments) != 0:
            self.stdout.write(self.style.SUCCESS(str(len(comments)) + comment_msg))
        else:
            self.stdout.write(self.style.SUCCESS('NO COMMENT OBJECT CREATED.'))
        if len(replies) != 0:
            self.stdout.write(self.style.SUCCESS(str(len(replies)) + reply_msg))
        else:
            self.stdout.write(self.style.SUCCESS('NO COMMENT (REPLY) OBJECT CREATED.'))
        if comment_like_count != 0:
            self.stdout.write(self.style.SUCCESS(str(comment_like_count) + comment_like_msg))
        else:
            self.stdout.write(self.style.SUCCESS('NO COMMENTLIKE OBJECT CREATED.'))


        self.stdout.write(self.style.SUCCESS(
            '=' * (
                len(str(
                    biggest(
                        follows_count,
                        len(posts),
                        post_like_count,
                        post_view_count,
                        len(comments),
                        len(replies),
                        comment_like_count
                    )
                )) + len(
                    longest(
                        follow_msg,
                        post_msg,
                        post_like_msg,
                        post_view_msg,
                        comment_msg,
                        reply_msg,
                        comment_like_msg
                    )
                )
            )
        ))
