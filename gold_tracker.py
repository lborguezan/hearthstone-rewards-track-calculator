# --- Hearthstone Reward Track Gold Calculator ---
#
# What the script does:
# This script calculates the total amount of gold a player has earned from the Hearthstone
# reward track based on their current level and current XP on that level.
# It uses a predefined data structure (REWARD_TRACK_DATA) that holds the gold rewards
# for each level of the track.
#
# How to run the script:
# 1. Ensure you have Python installed.
# 2. Update the REWARD_TRACK_DATA below if necessary (see instructions).
# 3. Run the script from your terminal: python gold_tracker.py
#    The script includes example usage at the end, which will print calculations
#    for a few scenarios and also test error handling.
#
# How to update REWARD_TRACK_DATA:
# The `REWARD_TRACK_DATA` is a Python list of dictionaries. Each dictionary represents
# one level on the reward track and must have the following keys:
#   - "level": (integer) The level number (e.g., 1, 2, 3, ...).
#   - "xp_to_next": (integer) The amount of XP required to complete this level and move to the next.
#                   (Note: This specific script version primarily uses "gold_reward" and "level"
#                    for its calculation, but "xp_to_next" is standard for reward track data).
#   - "gold_reward": (integer) The amount of gold awarded when this level is achieved/completed.
#                    The script assumes gold for a level is claimed if any XP is earned on that level,
#                    or if the level is surpassed.
#
# Example entry:
#   {"level": 1, "xp_to_next": 100, "gold_reward": 50}
#
# Important:
# - The accuracy of the calculations performed by this script is entirely dependent on the
#   correctness and completeness of the `REWARD_TRACK_DATA`.
# - Ensure the levels are listed contiguously if you expect calculations for all intermediate levels.
#   The script can handle sparse data, but it will only calculate based on explicitly defined levels.
# - You can find up-to-date reward track data on Hearthstone wikis (e.g., Hearthstone Wiki on Fandom)
#   or community forums like Reddit (r/hearthstone). Search for the specific expansion's reward track.
#
# How to use the calculate_gold function:
# You can import and use the `calculate_gold` function in your own Python scripts:
#
#   from gold_tracker import calculate_gold, REWARD_TRACK_DATA
#
#   # Optional: Update REWARD_TRACK_DATA if needed by modifying gold_tracker.REWARD_TRACK_DATA
#   # my_level = 10
#   # my_xp = 250
#   # total_gold_earned = calculate_gold(current_level=my_level, current_xp=my_xp)
#   # print(f"If you are Level {my_level} with {my_xp} XP, you have earned {total_gold_earned} gold so far.")
#
# The function returns an integer representing the total gold earned from all levels up to
# and including the `current_level` (if `current_xp` on that level is > 0).
# It will raise a ValueError if the inputs are invalid (e.g., negative XP, level out of bounds).

REWARD_TRACK_DATA = [
    {"level": 1, "xp_to_next": 100, "gold_reward": 50},
    {"level": 2, "xp_to_next": 150, "gold_reward": 75},
    {"level": 3, "xp_to_next": 200, "gold_reward": 100},
    # Add more levels as needed
]

def calculate_gold(current_level: int, current_xp: int) -> int:
    """
    Calculates the total gold earned based on the current level and XP.
    Includes error handling for invalid level and XP.
    """
    # Check for negative XP
    if current_xp < 0:
        raise ValueError("Current XP cannot be negative.")

    # Check for invalid current_level (must be 1 or greater)
    if current_level < 1:
        raise ValueError("Current level must be 1 or greater.")

    # Check if current_level exceeds the defined track data
    # This is done by checking if REWARD_TRACK_DATA[current_level - 1] exists.
    # This implicitly assumes levels are 1-indexed and contiguous in the data.
    try:
        # Attempt to access the data for current_level.
        # This also handles the case where REWARD_TRACK_DATA might be empty.
        if not REWARD_TRACK_DATA: # Handle empty track data explicitly
             raise ValueError("Reward track data is empty.")
        target_level_data = None
        level_exists_in_data = False
        for item in REWARD_TRACK_DATA:
            if item["level"] == current_level:
                target_level_data = item
                level_exists_in_data = True
                break

        if not level_exists_in_data:
            # If current_level is higher than any level in the track
            # or if the specific level is missing (for non-contiguous tracks)
            max_defined_level = 0
            if REWARD_TRACK_DATA: # ensure not empty before trying to get max
                max_defined_level = max(item['level'] for item in REWARD_TRACK_DATA)

            if current_level > max_defined_level :
                 raise ValueError(f"Current level {current_level} is beyond the maximum defined level ({max_defined_level}) in reward track.")
            else: # Level is within range of min/max but not explicitly defined (sparse track)
                 raise ValueError(f"Current level {current_level} is not defined in the reward track data.")

    except IndexError: # This would catch if current_level -1 is out of bounds of the list
        # This is a bit redundant if max_defined_level check is robust, but keeps the spirit of the requirement.
        max_defined_level = len(REWARD_TRACK_DATA) # Assuming 1-indexed contiguous levels
        raise ValueError(f"Current level {current_level} is beyond the maximum defined level ({max_defined_level}) in reward track.")


    total_gold = 0
    for track_entry in REWARD_TRACK_DATA:
        level_data_level = track_entry["level"]
        gold_for_level = track_entry["gold_reward"]

        if level_data_level < current_level:
            total_gold += gold_for_level
        elif level_data_level == current_level:
            if current_xp > 0: # Gold for current level only if XP > 0
                total_gold += gold_for_level
            break # Gold calculation stops at current level
        # No need for 'else' here, as levels beyond current_level are not processed for gold.

    return total_gold

if __name__ == "__main__":
    # Valid examples
    print(f"Gold for Level 2, XP 50: {calculate_gold(current_level=2, current_xp=50)}")
    print(f"Gold for Level 1, XP 75: {calculate_gold(current_level=1, current_xp=75)}")
    print(f"Gold for Level 3, XP 0: {calculate_gold(current_level=3, current_xp=0)}")
    print(f"Gold for Level 1, XP 0: {calculate_gold(current_level=1, current_xp=0)}")

    # Last level in data, XP > 0
    last_level = REWARD_TRACK_DATA[-1]["level"] if REWARD_TRACK_DATA else 0
    if last_level > 0:
        print(f"Gold for Level {last_level}, XP 1: {calculate_gold(current_level=last_level, current_xp=1)}")

    print("\n--- Error Handling Tests ---")

    # Test case: current_xp is negative
    try:
        calculate_gold(current_level=1, current_xp=-10)
    except ValueError as e:
        print(f"Caught expected error for negative XP: {e}")

    # Test case: current_level is less than 1
    try:
        calculate_gold(current_level=0, current_xp=50)
    except ValueError as e:
        print(f"Caught expected error for level < 1: {e}")

    try:
        calculate_gold(current_level=-1, current_xp=50)
    except ValueError as e:
        print(f"Caught expected error for level < 1 (negative): {e}")

    # Test case: current_level is beyond the defined track data
    # Assuming REWARD_TRACK_DATA has 3 levels as defined. Level 4 should be an error.
    beyond_max_level = (max(item['level'] for item in REWARD_TRACK_DATA) + 1) if REWARD_TRACK_DATA else 1
    try:
        calculate_gold(current_level=beyond_max_level, current_xp=50)
    except ValueError as e:
        print(f"Caught expected error for level beyond track data (e.g., Level {beyond_max_level}): {e}")

    # Test case: REWARD_TRACK_DATA is empty (edge case for error handling)
    # Temporarily modify REWARD_TRACK_DATA for this test
    original_track_data = list(REWARD_TRACK_DATA) # Make a copy
    REWARD_TRACK_DATA.clear()
    try:
        calculate_gold(current_level=1, current_xp=50)
    except ValueError as e:
        print(f"Caught expected error for empty track data: {e}")
    REWARD_TRACK_DATA.extend(original_track_data) # Restore

    # Test case: Level is missing in a sparse track (hypothetical)
    # For this, we'd need to modify the track data to be sparse.
    # E.g., REWARD_TRACK_DATA = [{"level": 1, ...}, {"level": 3, ...}]
    # and then try calculate_gold(current_level=2, current_xp=10)
    print("\nTesting with a temporarily sparse track (missing level 2):")
    original_track_data_sparse_test = list(REWARD_TRACK_DATA)
    REWARD_TRACK_DATA.clear()
    REWARD_TRACK_DATA.extend([
        {"level": 1, "xp_to_next": 100, "gold_reward": 50},
        {"level": 3, "xp_to_next": 200, "gold_reward": 100},
    ])
    try:
        calculate_gold(current_level=2, current_xp=10) # Level 2 is missing
    except ValueError as e:
        print(f"Caught expected error for missing level in sparse track: {e}")
    REWARD_TRACK_DATA.clear()
    REWARD_TRACK_DATA.extend(original_track_data_sparse_test) # Restore
