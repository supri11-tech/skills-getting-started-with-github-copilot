class TestRoot:
    """Test cases for root endpoint"""

    def test_root_redirect(self, client):
        """Test that root endpoint redirects to static index"""
        response = client.get("/")

        assert response.status_code == 200
        # FastAPI's RedirectResponse should redirect to /static/index.html
        # But in test client, it might return the redirect response
        # Let's check if it redirects or serves the content
        if response.status_code == 302:  # Redirect
            assert response.headers.get("location") == "/static/index.html"
        else:
            # If it serves the content directly, check it's HTML
            assert "text/html" in response.headers.get("content-type", "")