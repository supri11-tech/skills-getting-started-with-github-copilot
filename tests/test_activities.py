from src.app import activities


class TestActivities:
    """Test cases for activities endpoints"""

    def test_get_activities(self, client):
        """Test getting all activities"""
        response = client.get("/activities")

        assert response.status_code == 200
        data = response.json()

        # Check that we get a dictionary
        assert isinstance(data, dict)

        # Check that all expected activities are present
        expected_activities = [
            "Chess Club", "Basketball Club", "Tennis Team", "Debate Club",
            "Science Club", "Art Club", "Drama Society", "Programming Class", "Gym Class"
        ]

        for activity in expected_activities:
            assert activity in data
            assert "description" in data[activity]
            assert "schedule" in data[activity]
            assert "max_participants" in data[activity]
            assert "participants" in data[activity]
            assert isinstance(data[activity]["participants"], list)

    def test_signup_for_activity_success(self, client):
        """Test successful signup for an activity"""
        # Use an activity that exists
        activity_name = "Chess Club"
        email = "test@mergington.edu"

        # Ensure the email is not already signed up
        initial_participants = activities[activity_name]["participants"].copy()
        if email in initial_participants:
            activities[activity_name]["participants"].remove(email)

        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

        # Check that the participant was added
        assert email in activities[activity_name]["participants"]

        # Clean up - remove the test participant
        activities[activity_name]["participants"].remove(email)

    def test_signup_for_nonexistent_activity(self, client):
        """Test signup for an activity that doesn't exist"""
        response = client.post(
            "/activities/NonexistentActivity/signup",
            params={"email": "test@mergington.edu"}
        )

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_signup_duplicate_participant(self, client):
        """Test signing up a participant who is already signed up"""
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # This email is already in the data

        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"]

    def test_unregister_from_activity_success(self, client):
        """Test successful unregistration from an activity"""
        activity_name = "Chess Club"
        email = "test@mergington.edu"

        # First, sign up the participant
        activities[activity_name]["participants"].append(email)

        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

        # Check that the participant was removed
        assert email not in activities[activity_name]["participants"]

    def test_unregister_from_nonexistent_activity(self, client):
        """Test unregistration from an activity that doesn't exist"""
        response = client.delete(
            "/activities/NonexistentActivity/unregister",
            params={"email": "test@mergington.edu"}
        )

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_unregister_non_participant(self, client):
        """Test unregistering a participant who is not signed up"""
        activity_name = "Chess Club"
        email = "notsignedup@mergington.edu"

        # Ensure the email is not in participants
        if email in activities[activity_name]["participants"]:
            activities[activity_name]["participants"].remove(email)

        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "not signed up" in data["detail"]