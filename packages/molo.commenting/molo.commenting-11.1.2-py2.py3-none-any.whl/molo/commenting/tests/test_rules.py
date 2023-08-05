from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, RequestFactory
from django.utils import timezone

from molo.commenting.models import MoloComment
from molo.core.models import SectionIndexPage
from molo.core.tests.base import MoloTestCaseMixin


from ..rules import CommentDataRule


class TestCommentDataRuleSegmentation(TestCase, MoloTestCaseMixin):
    def setUp(self):
        # Create an article
        self.mk_main()
        self.section = SectionIndexPage.objects.first()

        self.article = self.mk_article(self.section, title='article 1',
                                       subtitle='article 1 subtitle',
                                       slug='article-1')
        self.content_type = ContentType.objects.get_for_model(self.article)

        # Fabricate a request with a logged-in user
        # so we can use it to test the segment rule
        self.request_factory = RequestFactory()
        self.request = self.request_factory.get('/')
        self.request.user = get_user_model().objects.create_user(
            username='tester', email='tester@example.com', password='tester')

    def _create_comment(self, comment, parent=None):
        return MoloComment.objects.create(
            content_type=self.content_type,
            object_pk=self.article.pk,
            content_object=self.article,
            site=Site.objects.get_current(),
            user=self.request.user,
            comment=comment,
            parent=parent,
            submit_date=timezone.now())

    def test_comment_data_rule_is_static(self):
        rule = CommentDataRule(expected_content='that is some random content.',
                               operator=CommentDataRule.EQUALS)
        self.assertTrue(rule.static)

    def test_comment_data_exact_rule(self):
        self._create_comment('that is some random content.')
        rule = CommentDataRule(expected_content='that is some random content.',
                               operator=CommentDataRule.EQUALS)

        self.assertTrue(rule.test_user(self.request))

    def test_comment_data_exact_rule_fails(self):
        self._create_comment('that is some random content.')
        rule = CommentDataRule(expected_content='that is some other content',
                               operator=CommentDataRule.EQUALS)

        self.assertFalse(rule.test_user(self.request))

    def test_comment_data_contains_rule(self):
        self._create_comment('that is some random content.')
        rule = CommentDataRule(expected_content='some random',
                               operator=CommentDataRule.CONTAINS)

        self.assertTrue(rule.test_user(self.request))

    def test_comment_data_contains_rule_fails(self):
        self._create_comment('that is some random content.')
        rule = CommentDataRule(expected_content='somerandom',
                               operator=CommentDataRule.CONTAINS)

        self.assertFalse(rule.test_user(self.request))

    def test_test_user_without_request(self):
        self._create_comment('that is some random content.')
        rule = CommentDataRule(expected_content='that is some random content.',
                               operator=CommentDataRule.EQUALS)

        self.assertTrue(rule.test_user(None, self.request.user))

    def test_test_user_without_user_or_request(self):
        self._create_comment('that is some random content.')
        rule = CommentDataRule(expected_content='that is some random content.',
                               operator=CommentDataRule.EQUALS)
        self.assertFalse(rule.test_user(None))

    def test_get_column_header(self):
        rule = CommentDataRule(expected_content='that is some random content.',
                               operator=CommentDataRule.EQUALS)
        self.assertEqual(rule.get_column_header(), "Comment Data")

    def test_get_user_data_string_returns_data_for_exact_match(self):
        self._create_comment('that is some random content.')
        rule = CommentDataRule(expected_content='that is some random content.',
                               operator=CommentDataRule.EQUALS)

        self.assertEqual(rule.get_user_info_string(self.request.user),
                         '"that is some random content."')

    def test_get_user_data_string_returns_data_for_contains(self):
        self._create_comment('that is some random content.')
        rule = CommentDataRule(expected_content='some random',
                               operator=CommentDataRule.CONTAINS)

        self.assertEqual(rule.get_user_info_string(self.request.user),
                         '"that is some random content."')

    def test_get_user_data_string_concatenates_multiple_matches(self):
        self._create_comment('that is some random content.')
        self._create_comment('that is some other content.')
        rule = CommentDataRule(expected_content='that is some',
                               operator=CommentDataRule.CONTAINS)

        self.assertEqual(rule.get_user_info_string(self.request.user),
                         '"that is some random content."\n'
                         '"that is some other content."')

    def test_get_user_data_string_returns_if_no_matches(self):
        self._create_comment('that is some random content.')
        self._create_comment('that is some other content.')
        rule = CommentDataRule(expected_content='bla bla bla',
                               operator=CommentDataRule.CONTAINS)

        self.assertEqual(rule.get_user_info_string(self.request.user),
                         'No matching comments')
