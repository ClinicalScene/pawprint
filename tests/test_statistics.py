from datetime import datetime, timedelta
import numpy as np

import pawprint


def test_sessions(pawprint_default_statistics_tracker):
    """Test the calculation of session durations."""

    tracker = pawprint_default_statistics_tracker
    stats = pawprint.Statistics(tracker)

    # Calculate user session durations
    stats.sessions()

    # Read the results
    sessions = stats["sessions"].read()

    # Expected values
    users = np.array(["Frodo", "Gandalf", "Frodo", "Frodo"])
    durations = np.array([5, 40, 0, 4])
    events = np.array([6, 4, 1, 5])

    print(sessions.total_events)
    assert np.all(sessions[tracker.user_field] == users)
    assert np.all(sessions.duration == durations)
    assert np.all(sessions.total_events == events)


def test_sessions_in_batches(pawprint_default_statistics_tracker):
    """Test the calculation of session durations."""

    tracker = pawprint_default_statistics_tracker
    stats = pawprint.Statistics(tracker)

    # Calculate user session durations
    stats.sessions(batch_size=2)

    # Read the results
    sessions = stats["sessions"].read()

    # Expected values
    users = np.array(["Frodo", "Gandalf", "Frodo", "Frodo"])
    durations = np.array([5, 40, 0, 4])
    events = np.array([6, 4, 1, 5])

    print(sessions.total_events)
    assert np.all(sessions[tracker.user_field] == users)
    assert np.all(sessions.duration == durations)
    assert np.all(sessions.total_events == events)


def test_sessions_with_no_new_data(pawprint_default_statistics_tracker):
    """Test that no new sessions created with no new data"""
    tracker = pawprint_default_statistics_tracker
    stats = pawprint.Statistics(tracker)

    # Calculate user session durations
    stats.sessions()

    # Read the results
    sessions = stats["sessions"].read()

    # Expected values
    users = np.array(["Frodo", "Gandalf", "Frodo", "Frodo"])
    durations = np.array([5, 40, 0, 4])
    events = np.array([6, 4, 1, 5])

    # calculate sessions again with no new data
    stats.sessions(clean=False)
    sessions = stats["sessions"].read()

    assert np.all(sessions[tracker.user_field] == users)
    assert np.all(sessions.duration == durations)
    assert np.all(sessions.total_events == events)
    assert len(sessions) == 4


def test_sessions_with_new_data(pawprint_default_statistics_tracker):
    """Test that the correct number of new sessions are created with new data"""
    tracker = pawprint_default_statistics_tracker
    stats = pawprint.Statistics(tracker)

    # Calculate user session durations
    stats.sessions()

    # Read the results
    sessions = stats["sessions"].read()

    # New data
    new_users = ["Frodo", "Sam", "Sauron", "Bilbo", "Bilbo", "Bilbo"]
    new_timedeltas = [1005, 2000, 2010, 2100, 2101, 2102]
    new_events = ["wanted", "helped", "looked", "joined", "fought", "wrote"]

    # Yesterday morning
    today = datetime.now()
    yesterday = datetime(today.year, today.month, today.day, 9, 0) - timedelta(days=1)

    # Write all events
    for user, delta, event in zip(new_users, new_timedeltas, new_events):
        tracker.write(user_id=user, timestamp=yesterday + timedelta(minutes=delta), event=event)

    # Expected values
    users = np.array(["Frodo", "Gandalf", "Frodo", "Frodo", "Sam", "Sauron", "Bilbo"])
    durations = np.array([5, 40, 0, 5, 0, 0, 2])
    events = np.array([6, 4, 1, 6, 1, 1, 3])

    # calculate sessions again with new data
    stats.sessions(clean=False)
    sessions = stats["sessions"].read()

    print(sessions)
    assert np.all(sessions[tracker.user_field] == users)
    assert np.all(sessions.duration == durations)
    assert np.all(sessions.total_events == events)
    assert len(stats["sessions"].read()) == 7


def test_sessions_clean_equals_true_resets(pawprint_default_statistics_tracker):
    """Test that using clean=True still gives correct sessions for all events in the database"""
    tracker = pawprint_default_statistics_tracker
    stats = pawprint.Statistics(tracker)

    # Calculate user session durations
    stats.sessions()

    # Read the results
    sessions = stats["sessions"].read()

    # New data
    new_users = ["Sam", "Sauron", "Bilbo", "Bilbo", "Bilbo"]
    new_timedeltas = [2000, 2010, 2100, 2101, 2102]
    new_events = ["helped", "looked", "joined", "fought", "wrote"]

    # Yesterday morning
    today = datetime.now()
    yesterday = datetime(today.year, today.month, today.day, 9, 0) - timedelta(days=1)

    # Write all events
    for user, delta, event in zip(new_users, new_timedeltas, new_events):
        tracker.write(user_id=user, timestamp=yesterday + timedelta(minutes=delta), event=event)

    # Expected values
    users = np.array(["Frodo", "Gandalf", "Frodo", "Frodo", "Sam", "Sauron", "Bilbo"])
    durations = np.array([5, 40, 0, 4, 0, 0, 2])
    events = np.array([6, 4, 1, 5, 1, 1, 3])

    # calculate sessions again with new data
    stats.sessions(clean=True)
    sessions = stats["sessions"].read()

    assert np.all(sessions[tracker.user_field] == users)
    assert np.all(sessions.duration == durations)
    assert np.all(sessions.total_events == events)
    assert len(stats["sessions"].read()) == 7


def test_sessions_with_new_data_in_batches(pawprint_default_statistics_tracker):
    """Test that the correct number of new sessions are created with new data"""
    tracker = pawprint_default_statistics_tracker
    stats = pawprint.Statistics(tracker)

    # Calculate user session durations
    stats.sessions(batch_size=2)

    # Read the results
    sessions = stats["sessions"].read()

    # New data
    new_users = ["Frodo", "Sam", "Sauron", "Bilbo", "Bilbo", "Bilbo"]
    new_timedeltas = [1005, 2000, 2010, 2100, 2101, 2102]
    new_events = ["wanted", "helped", "looked", "joined", "fought", "wrote"]

    # Yesterday morning
    today = datetime.now()
    yesterday = datetime(today.year, today.month, today.day, 9, 0) - timedelta(days=1)

    # Write all events
    for user, delta, event in zip(new_users, new_timedeltas, new_events):
        tracker.write(user_id=user, timestamp=yesterday + timedelta(minutes=delta), event=event)

    # Expected values
    users = np.array(["Frodo", "Gandalf", "Frodo", "Frodo", "Sam", "Sauron", "Bilbo"])
    durations = np.array([5, 40, 0, 5, 0, 0, 2])
    events = np.array([6, 4, 1, 6, 1, 1, 3])

    # calculate sessions again with new data
    stats.sessions(clean=False, batch_size=2)
    sessions = stats["sessions"].read()

    print(sessions)
    assert np.all(sessions[tracker.user_field] == users)
    assert np.all(sessions.duration == durations)
    assert np.all(sessions.total_events == events)
    assert len(stats["sessions"].read()) == 7


# def test_engagement_metrics(pawprint_default_statistics_tracker):
#     """Test the calculation of user engagement metrics."""

#     tracker = pawprint_default_statistics_tracker
#     stats = pawprint.Statistics(tracker)

#     # Calculate user engagement
#     stats.sessions()
#     stats.engagement(min_sessions=0)

#     # Read the results
#     stickiness = stats["engagement"].read()

#     # Expected values
#     dau = np.array([2, 1])
#     wau = np.array([2, 2])
#     mau = np.array([2, 2])
#     engagement = np.array([1, 0.5])

#     assert np.all(stickiness.dau == dau)
#     assert np.all(stickiness.wau == wau)
#     assert np.all(stickiness.mau == mau)
#     assert np.all(stickiness.engagement == engagement)
#     assert set(stickiness.columns) == {"timestamp", "dau", "wau", "mau", "engagement"}


# def test_engagement_min_sessions(pawprint_default_statistics_tracker):

#     tracker = pawprint_default_statistics_tracker
#     stats = pawprint.Statistics(tracker)
#     stats.sessions()

#     # Now test with a minimum number of sessions
#     stats.engagement(min_sessions=2)
#     stickiness = stats["engagement"].read()

#     # Ground truth
#     active = np.array([1, 1])
#     engagement_active = np.array([1, 1])
#     dau = np.array([2, 1])

#     assert np.all(stickiness.dau_active == active)
#     assert np.all(stickiness.wau_active == active)
#     assert np.all(stickiness.mau_active == active)
#     assert np.all(stickiness.dau == dau)
#     assert np.all(stickiness.engagement_active == engagement_active)
#     assert set(stickiness.columns) == {
#         "timestamp",
#         "dau",
#         "wau",
#         "mau",
#         "engagement",
#         "dau_active",
#         "wau_active",
#         "mau_active",
#         "engagement_active",
#     }

#     # Test that running engagements again doesn't error if there's no new data
#     stats.engagement()


# def test_engagement_too_many_min_sessions(pawprint_default_statistics_tracker):
#     tracker = pawprint_default_statistics_tracker
#     stats = pawprint.Statistics(tracker)
#     stats.sessions()

#     # Test with too large a minimum sessions parameter
#     stats.engagement(min_sessions=20)
#     stickiness = stats["engagement"].read()
#     assert len(stickiness) == 2
#     assert set(stickiness.columns) == {"timestamp", "dau", "wau", "mau", "engagement"}


# def test_engagement_append_mode(pawprint_default_statistics_tracker):
#     tracker = pawprint_default_statistics_tracker
#     stats = pawprint.Statistics(tracker)
#     stats.sessions()

#     stats.engagement(min_sessions=20)

#     # Try again with append-only
#     stats.engagement(clean=False)
#     stickiness = stats["engagement"].read()
#     assert len(stickiness.columns) == 5
#     assert len(stickiness) == 2

#     stats.engagement(clean=True, min_sessions=2)
#     stickiness = stats["engagement"].read()
#     assert len(stickiness) == 2
#     assert len(stickiness.columns) == 9
