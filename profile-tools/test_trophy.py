import unittest

from trophy import render_trophy_svg


class TrophyTests(unittest.TestCase):
    def test_render_trophy_svg_contains_all_panels(self):
        stats = {
            "stars": 12,
            "repos": 6,
            "followers": 8,
            "forks": 4,
            "contributions": 31,
            "years": 4,
        }

        svg = render_trophy_svg("FogPurification", stats)

        self.assertIn("<svg", svg)
        self.assertIn("FogPurification", svg)
        for label in ("Stars", "Repositories", "Followers", "Forks", "Contributions", "Years on GitHub"):
            self.assertIn(label, svg)
        for value in ("12", "6", "8", "4", "31"):
            self.assertIn(value, svg)


if __name__ == "__main__":
    unittest.main()
