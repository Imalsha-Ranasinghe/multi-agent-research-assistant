import unittest

from workflow import parse_review_verdict, review_decision


class TestReviewVerdict(unittest.TestCase):

    def test_approve(self):
        self.assertEqual(
            parse_review_verdict("VERDICT: APPROVE\nFEEDBACK: Looks good."),
            "APPROVE",
        )

    def test_revise(self):
        self.assertEqual(
            parse_review_verdict("VERDICT: REVISE\nFEEDBACK: Add evidence."),
            "REVISE",
        )

    def test_case_insensitive(self):
        self.assertEqual(
            parse_review_verdict("verdict: approve"),
            "APPROVE",
        )

    def test_missing_verdict_defaults_to_revise(self):
        self.assertEqual(
            parse_review_verdict("The report looks good."),
            "REVISE",
        )

    def test_ambiguous_verdict_defaults_to_revise(self):
        self.assertEqual(
            parse_review_verdict("VERDICT: APPROVED"),
            "REVISE",
        )
    
    def test_approved_report_finishes(self):
        state = {
            "status": "approved",
            "revision_count": 0,
        }
        self.assertEqual(review_decision(state), "finish")

    def test_report_needing_revision_returns_to_writer(self):
        state = {
            "status": "revise",
            "revision_count": 1,
        }
        self.assertEqual(review_decision(state), "revise")

    def test_revision_limit_stops_loop(self):
        state = {
            "status": "revise",
            "revision_count": 2,
        }
        self.assertEqual(review_decision(state), "finish")

    def test_missing_status_requests_revision(self):
        state = {"revision_count": 0}
        self.assertEqual(review_decision(state), "revise")



if __name__ == "__main__":
    unittest.main()
