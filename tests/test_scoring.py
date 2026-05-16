import unittest

from earnings_call_risk_map.scoring import score_note, severity_label


class ScoringCalibrationTests(unittest.TestCase):
    def test_severity_label_boundaries_are_inclusive_at_thresholds(self):
        cases = {
            0: "none",
            1: "low",
            3: "low",
            4: "medium",
            6: "medium",
            7: "high",
            8: "high",
        }
        for score, expected in cases.items():
            with self.subTest(score=score):
                self.assertEqual(severity_label(score), expected)

    def test_high_impact_language_starts_at_score_seven(self):
        medium_note = score_note(
            {
                "id": "medium",
                "date": "2026-05-01",
                "topic": "medium edge",
                "text": "Margin compression pressure.",
                "evidence_url": "https://example.com/medium-edge",
            },
            as_of="2026-05-15",
            data_cutoff="2026-05-01",
        )
        high_note = score_note(
            {
                "id": "high",
                "date": "2026-05-01",
                "topic": "high edge",
                "text": "Guidance cut pressure.",
                "evidence_url": "https://example.com/high-edge",
            },
            as_of="2026-05-15",
            data_cutoff="2026-05-01",
        )

        self.assertEqual(medium_note["risk_score"], 6)
        self.assertEqual(medium_note["risk_level"], "medium")
        self.assertNotIn("high-impact language", medium_note["review_reasons"])
        self.assertEqual(high_note["risk_score"], 7)
        self.assertEqual(high_note["risk_level"], "high")
        self.assertIn("high-impact language", high_note["review_reasons"])

    def test_stale_risk_note_can_cross_from_medium_to_high(self):
        stale_note = score_note(
            {
                "id": "stale",
                "date": "2026-01-01",
                "topic": "stale edge",
                "text": "Margin compression pressure.",
                "evidence_url": "https://example.com/stale-edge",
            },
            as_of="2026-05-15",
            data_cutoff="2026-05-01",
        )

        self.assertEqual(stale_note["risk_score"], 7)
        self.assertEqual(stale_note["risk_level"], "high")
        self.assertIn("data is stale", stale_note["review_reasons"])
        self.assertIn("high-impact language", stale_note["review_reasons"])


if __name__ == "__main__":
    unittest.main()
