"""
Unit tests for takeover.manager
"""

from __future__ import annotations

import unittest

from unittest.mock import patch

from modules.takeover.manager import (
    run_takeover_detection,
)


class TestTakeoverManager(
    unittest.TestCase,
):

    @patch(
        "modules.takeover.manager.export_results",
    )
    @patch(
        "modules.takeover.manager.print_summary",
    )
    @patch(
        "modules.takeover.manager.generate_statistics",
    )
    @patch(
        "modules.takeover.manager.filter_results",
    )
    @patch(
        "modules.takeover.manager.analyze",
    )
    @patch(
        "modules.takeover.manager.resolve_ipv4",
    )
    @patch(
        "modules.takeover.manager.resolve_cname",
    )
    @patch(
        "modules.takeover.manager.extract_title",
    )
    @patch(
        "modules.takeover.manager.extract_body",
    )
    @patch(
        "modules.takeover.manager.extract_status_code",
    )
    @patch(
        "modules.takeover.manager.request_page",
    )
    @patch(
        "modules.takeover.manager.normalize_target",
    )
    def test_run_takeover_detection(

        self,

        mock_normalize,

        mock_request,

        mock_status,

        mock_body,

        mock_title,

        mock_cname,

        mock_ip,

        mock_analyze,

        mock_filter,

        mock_statistics,

        mock_summary,

        mock_export,

    ):

        mock_normalize.return_value = (

            "demo.example.com"

        )

        mock_request.return_value = object()

        mock_status.return_value = 404

        mock_body.return_value = (

            "There isn't a "

            "GitHub Pages site here."

        )

        mock_title.return_value = ""

        mock_cname.return_value = (

            "demo.github.io"

        )

        mock_ip.return_value = (

            "185.199.108.153"

        )

        analysis = {

            "target": "demo.example.com",

            "vulnerable": True,

            "provider": "GitHub Pages",

            "confidence": 95,

            "methods": [

                "http",

                "status",

                "cname",

            ],

            "status_code": 404,

            "fingerprint": (

                "GitHub Pages"

            ),

            "cname": "demo.github.io",

            "ip": "185.199.108.153",

            "http_title": "",

            "recommendations": [],

        }

        mock_analyze.return_value = (

            analysis

        )

        mock_filter.return_value = [

            analysis,

        ]

        statistics = {

            "targets": 1,

            "vulnerable": 1,

            "safe": 0,

            "provider_statistics": {

                "GitHub Pages": 1,

            },

            "confidence_statistics": {

                "high": 1,

                "medium": 0,

                "low": 0,

                "unknown": 0,

            },

            "average_confidence": 95,

            "highest_confidence": 95,

            "elapsed": 0.10,

        }

        mock_statistics.return_value = (

            statistics

        )

        results, stats = (

            run_takeover_detection(

                [

                    "demo.example.com",

                ]

            )

        )

        self.assertEqual(

            len(results),

            1,

        )

        self.assertTrue(

            results[0][

                "vulnerable"

            ]

        )

        self.assertEqual(

            stats,

            statistics,

        )

        mock_export.assert_called_once()

        mock_summary.assert_called_once()


if __name__ == "__main__":

    unittest.main(

        verbosity=2,

    )