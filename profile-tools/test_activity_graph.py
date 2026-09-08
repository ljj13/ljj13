import unittest

from activity_graph import render_svg


class ActivityGraphTests(unittest.TestCase):
    def test_render_svg_contains_activity_series_and_summary(self):
        days = [
            {"date": "2026-09-01", "contributionCount": 0},
            {"date": "2026-09-02", "contributionCount": 3},
            {"date": "2026-09-03", "contributionCount": 1},
        ]

        svg = render_svg("FogPurification", days)

        self.assertIn("<svg", svg)
        self.assertIn("Contribution Activity", svg)
        self.assertIn("FogPurification", svg)
        self.assertIn('data-point-count="3"', svg)
        self.assertIn("polyline", svg)
        self.assertIn("Total 4 contributions", svg)


if __name__ == "__main__":
    unittest.main()
