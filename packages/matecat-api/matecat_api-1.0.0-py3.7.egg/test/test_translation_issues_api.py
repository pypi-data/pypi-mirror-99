# coding: utf-8

"""
    MateCat API

    We developed a set of Rest API to let you integrate Matecat in your translation management system or in any other application. Use our API to create projects and check their status.  # noqa: E501

    OpenAPI spec version: 2.0.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import matecat_api
from matecat_api.api.translation_issues_api import TranslationIssuesApi  # noqa: E501
from matecat_api.rest import ApiException


class TestTranslationIssuesApi(unittest.TestCase):
    """TranslationIssuesApi unit test stubs"""

    def setUp(self):
        self.api = TranslationIssuesApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_api_v2_jobs_id_job_password_segments_id_segment_translation_issues_id_issue_comments_get(self):
        """Test case for api_v2_jobs_id_job_password_segments_id_segment_translation_issues_id_issue_comments_get

        Get comments  # noqa: E501
        """
        pass

    def test_api_v2_jobs_id_job_password_segments_id_segment_translation_issues_id_issue_comments_post(self):
        """Test case for api_v2_jobs_id_job_password_segments_id_segment_translation_issues_id_issue_comments_post

        Add comment to a translation issue  # noqa: E501
        """
        pass

    def test_api_v2_jobs_id_job_password_segments_id_segment_translation_issues_id_issue_delete(self):
        """Test case for api_v2_jobs_id_job_password_segments_id_segment_translation_issues_id_issue_delete

        Delete a translation Issue  # noqa: E501
        """
        pass

    def test_api_v2_jobs_id_job_password_segments_id_segment_translation_issues_id_issue_post(self):
        """Test case for api_v2_jobs_id_job_password_segments_id_segment_translation_issues_id_issue_post

        Update translation issues  # noqa: E501
        """
        pass

    def test_api_v2_jobs_id_job_password_segments_id_segment_translation_issues_post(self):
        """Test case for api_v2_jobs_id_job_password_segments_id_segment_translation_issues_post

        Create translation issues  # noqa: E501
        """
        pass

    def test_api_v2_jobs_id_job_password_translation_issues_get(self):
        """Test case for api_v2_jobs_id_job_password_translation_issues_get

        Project translation issues  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
