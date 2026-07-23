"""
Unit tests for
email.manager
"""

from __future__ import annotations

import unittest
from unittest.mock import patch

from modules.email.manager import (
    run_email_security,
)


class TestEmailManager(
    unittest.TestCase,
):

    @patch(
        "modules.email.manager.export_results",
    )
    @patch(
        "modules.email.manager.print_summary",
    )
    @patch(
        "modules.email.manager.generate_statistics",
    )
    @patch(
        "modules.email.manager.filter_results",
    )
    @patch(
        "modules.email.manager.analyze",
    )
    @patch(
        "modules.email.manager.create_result",
    )
    @patch(
        "modules.email.manager.resolve_dnskey",
    )
    @patch(
        "modules.email.manager.resolve_bimi",
    )
    @patch(
        "modules.email.manager.resolve_tls_rpt",
    )
    @patch(
        "modules.email.manager.resolve_mta_sts",
    )
    @patch(
        "modules.email.manager.resolve_dmarc",
    )
    @patch(
        "modules.email.manager.resolve_dkim",
    )
    @patch(
        "modules.email.manager.resolve_spf",
    )
    @patch(
        "modules.email.manager.resolve_mx",
    )
    @patch(
        "modules.email.manager.normalize_target",
    )
    def test_run_email_security(

        self,

        mock_normalize,

        mock_mx,

        mock_spf,

        mock_dkim,

        mock_dmarc,

        mock_mta_sts,

        mock_tls_rpt,

        mock_bimi,

        mock_dnssec,

        mock_create,

        mock_analyze,

        mock_filter,

        mock_statistics,

        mock_summary,

        mock_export,

    ):

        mock_normalize.return_value = (

            "example.com"

        )

        mock_mx.return_value = [

            "mx.example.com",

        ]

        mock_spf.return_value = (

            True,

            "v=spf1",

        )

        mock_dkim.return_value = (

            True,

            "default",

        )

        mock_dmarc.return_value = (

            True,

            "v=DMARC1",

        )

        mock_mta_sts.return_value = True

        mock_tls_rpt.return_value = True

        mock_bimi.return_value = False

        mock_dnssec.return_value = False

        result = {

            "target": "example.com",

            "provider": "Google Workspace",

            "score": 20,

            "risk": "Low",

            "spf": True,

            "dkim": True,

            "dmarc": True,

        }

        mock_create.return_value = result

        mock_analyze.return_value = result

        mock_filter.return_value = [

            result,

        ]

        statistics = {

            "targets": 1,

            "low": 1,

            "medium": 0,

            "high": 0,

            "critical": 0,

            "average_score": 20,

            "highest_score": 20,

            "elapsed": 0.01,

        }

        mock_statistics.return_value = (

            statistics

        )

        results, stats = run_email_security(

            [

                "example.com",

            ],

        )

        self.assertEqual(

            len(

                results,

            ),

            1,

        )

        self.assertEqual(

            stats[

                "targets"

            ],

            1,

        )

        mock_export.assert_called_once()

        mock_summary.assert_called_once()


if __name__ == "__main__":

    unittest.main(

        verbosity=2,

    )