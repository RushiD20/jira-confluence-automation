import tempfile
import unittest
from pathlib import Path

from status_report import build_report, fetch_status_data, generate_report


class StatusReportTests(unittest.TestCase):
    def test_fetch_status_data_returns_expected_sections(self):
        data = fetch_status_data()

        self.assertIn("reporting_period", data)
        self.assertIn("project_or_team", data)
        self.assertIn("owner", data)
        self.assertIn("overall_status", data)
        self.assertIn("accomplishments", data)
        self.assertIn("progress_and_metrics", data)
        self.assertIn("blockers_and_risks", data)
        self.assertIn("next_period_plan", data)
        self.assertIn("decisions_or_support_needed", data)

    def test_build_report_uses_expected_markdown_format(self):
        data = fetch_status_data()
        report = build_report(data)

        self.assertIn("# Weekly Status Report", report)
        self.assertIn("**Reporting period:**", report)
        self.assertIn("## Accomplishments", report)
        self.assertIn("## Progress and Metrics", report)
        self.assertIn("## Blockers and Risks", report)
        self.assertIn("## Next Period's Plan", report)
        self.assertIn("## Decisions or Support Needed", report)

    def test_generate_report_writes_markdown_file(self):
        data = fetch_status_data()

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "weekly_report.md"
            result_path = generate_report(data=data, output_path=output_path)

            self.assertTrue(result_path.exists())
            self.assertIn("# Weekly Status Report", result_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
