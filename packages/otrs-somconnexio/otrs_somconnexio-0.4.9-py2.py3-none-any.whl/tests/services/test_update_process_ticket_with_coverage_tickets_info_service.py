# coding: utf-8
import unittest
from mock import Mock, patch

from otrs_somconnexio.services.update_process_ticket_with_coverage_tickets_info_service import \
    UpdateProcessTicketWithCoverageTicketsInfoService


class UpdateProcessTicketWithCoverageTicketsInfoServiceTestCase(unittest.TestCase):
    @patch('otrs_somconnexio.services.update_process_ticket_with_coverage_tickets_info_service.OTRSClient',
           return_value=Mock(spec=['update_ticket']),
           )
    @patch('otrs_somconnexio.services.update_process_ticket_with_coverage_tickets_info_service.CoverageArticle')
    def test_run(self, MockCoverageArticle, MockOTRSClient):
        coverage_article = object()
        expected_coverage_ticket = object()
        coverage_tickets = [expected_coverage_ticket]

        def mock_coverage_article_side_effect(ticket):
            if ticket == expected_coverage_ticket:
                mock_coverage_article = Mock(spec=['call'])
                mock_coverage_article.call.return_value = coverage_article
                return mock_coverage_article

        MockCoverageArticle.side_effect = mock_coverage_article_side_effect

        UpdateProcessTicketWithCoverageTicketsInfoService(123, coverage_tickets).run()

        MockOTRSClient.return_value.update_ticket.assert_called_once_with(
            123,
            coverage_article
        )
