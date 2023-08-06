from germanium.tools.trivials import assert_equal
from germanium.tools.http import assert_http_method_not_allowed
from germanium.tools.rest import assert_valid_JSON_response

from .test_case import PystonTestCase
from .factories import UserFactory, IssueFactory


class ExtraResourceTestCase(PystonTestCase):

    def test_not_supported_message_for_put_post_and_delete(self):
        resp = self.put(self.EXTRA_API_URL, data={})
        assert_http_method_not_allowed(resp)

        resp = self.post(self.EXTRA_API_URL, data={})
        assert_http_method_not_allowed(resp)

        resp = self.delete(self.EXTRA_API_URL)
        assert_http_method_not_allowed(resp)

    def test_should_return_data_for_get(self):
        resp = self.get(self.EXTRA_API_URL)
        assert_valid_JSON_response(resp)

    def test_resource_with_serializable_result(self):
        [IssueFactory(solver=UserFactory()) for _ in range(10)]

        resp_data = self.deserialize(self.get(self.COUNT_ISSUES_PER_USER))
        assert_equal(len(resp_data), 10 * 3)
        for row in resp_data:
            assert_equal(set(row.keys()), {'email', 'created_issues_count'})

    def test_resource_with_serializableobj_result(self):
        issues = [IssueFactory() for _ in range(10)]
        for issue in issues:
            issue.watched_by.add(*[UserFactory() for _ in range(5)])

        resp_data = self.deserialize(self.get(self.COUNT_WATCHERS_PER_ISSUE))
        assert_equal(len(resp_data), 10)
        for row in resp_data:
            assert_equal(set(row.keys()), {'name', 'watchers_count'})
            assert_equal(row['watchers_count'], 5)
