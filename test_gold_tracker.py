import unittest
import re # Import re for escaping
import gold_tracker # To allow modification of its REWARD_TRACK_DATA for a specific test

# From gold_tracker module
calculate_gold = gold_tracker.calculate_gold
# We will use gold_tracker.REWARD_TRACK_DATA directly to access the list
# and also to modify it for one test case.

class TestGoldTracker(unittest.TestCase):

    def setUp(self):
        # Save a copy of the original REWARD_TRACK_DATA before each test
        # This is particularly for test_empty_reward_track_data and test_sparse_data (if added)
        self.original_reward_track_data = list(gold_tracker.REWARD_TRACK_DATA)
        # Ensure gold_tracker.REWARD_TRACK_DATA is reset to its original state from file
        # This handles cases where a previous test might have modified it and failed before tearDown
        gold_tracker.REWARD_TRACK_DATA = [
            {"level": 1, "xp_to_next": 100, "gold_reward": 50},
            {"level": 2, "xp_to_next": 150, "gold_reward": 75},
            {"level": 3, "xp_to_next": 200, "gold_reward": 100},
        ]


    def tearDown(self):
        # Restore the original REWARD_TRACK_DATA after each test
        gold_tracker.REWARD_TRACK_DATA = self.original_reward_track_data

    def test_valid_calculations(self):
        # Based on current REWARD_TRACK_DATA:
        # L1: 50 gold
        # L2: 75 gold
        # L3: 100 gold

        # Scenario 1: Level 1, some XP
        # Expected: 50 (for level 1, as XP > 0)
        self.assertEqual(calculate_gold(current_level=1, current_xp=50), 50)

        # Scenario 2: Mid-tier level (level 2), some XP
        # Expected: 50 (L1) + 75 (L2, as XP > 0) = 125
        self.assertEqual(calculate_gold(current_level=2, current_xp=50), 125)

        # Scenario 3: Maximum level (level 3), some XP
        # Expected: 50 (L1) + 75 (L2) + 100 (L3, as XP > 0) = 225
        self.assertEqual(calculate_gold(current_level=3, current_xp=100), 225)

        # Scenario 4: A level with 0 XP
        # Test with Level 1, 0 XP. Expected: 0 (no gold for L1 as XP is 0)
        self.assertEqual(calculate_gold(current_level=1, current_xp=0), 0)

        # Test with Level 2, 0 XP. Expected: 50 (L1 gold)
        self.assertEqual(calculate_gold(current_level=2, current_xp=0), 50)

        # Test with Level 3, 0 XP. Expected: 50 (L1) + 75 (L2) = 125
        self.assertEqual(calculate_gold(current_level=3, current_xp=0), 125)

    def test_invalid_level_input(self):
        # Test level 0
        with self.assertRaisesRegex(ValueError, "Current level must be 1 or greater."):
            calculate_gold(current_level=0, current_xp=50)

        # Test level -1
        with self.assertRaisesRegex(ValueError, "Current level must be 1 or greater."):
            calculate_gold(current_level=-1, current_xp=50)

        # Test level greater than max level in REWARD_TRACK_DATA (max is 3, test 4)
        max_defined_level = max(item['level'] for item in gold_tracker.REWARD_TRACK_DATA) if gold_tracker.REWARD_TRACK_DATA else 0
        level_to_test = max_defined_level + 1
        # Escape the message because it contains parentheses, which are special characters in regex
        expected_message = re.escape(f"Current level {level_to_test} is beyond the maximum defined level ({max_defined_level}) in reward track.")
        with self.assertRaisesRegex(ValueError, expected_message):
            calculate_gold(current_level=level_to_test, current_xp=50)

    def test_invalid_xp_input(self):
        # Test negative XP
        with self.assertRaisesRegex(ValueError, "Current XP cannot be negative."):
            calculate_gold(current_level=1, current_xp=-10)

    def test_empty_reward_track_data(self):
        # Temporarily set gold_tracker.REWARD_TRACK_DATA to []
        gold_tracker.REWARD_TRACK_DATA.clear()

        with self.assertRaisesRegex(ValueError, "Reward track data is empty."):
            calculate_gold(current_level=1, current_xp=50)
        # tearDown will restore it, or setUp for the next test will.

    def test_sparse_track_missing_level(self):
        # Test for a level that is missing in a sparse track
        # This test assumes the error message for a missing (but not out-of-bounds) level.
        original_data = list(gold_tracker.REWARD_TRACK_DATA)
        gold_tracker.REWARD_TRACK_DATA.clear()
        gold_tracker.REWARD_TRACK_DATA.extend([
            {"level": 1, "xp_to_next": 100, "gold_reward": 50},
            {"level": 3, "xp_to_next": 200, "gold_reward": 100},
        ])

        # Escape the message for regex, just in case, though this one has no special chars.
        expected_message = re.escape("Current level 2 is not defined in the reward track data.")
        with self.assertRaisesRegex(ValueError, expected_message):
            calculate_gold(current_level=2, current_xp=10)

        gold_tracker.REWARD_TRACK_DATA.clear()
        gold_tracker.REWARD_TRACK_DATA.extend(original_data)


if __name__ == '__main__':
    unittest.main()
