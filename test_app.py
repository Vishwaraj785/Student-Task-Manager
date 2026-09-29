from app import app


def test_health():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def test_add_task():
    client = app.test_client()

    response = client.post(
        "/add",
        data={
            "title": "Finish DevOps Assignment",
            "description": "Complete CCA2 pipeline",
            "subject": "Cloud Computing",
            "priority": "High",
            "due_date": "2026-10-05",
        },
    )

    assert response.status_code == 302


def test_invalid_task():
    client = app.test_client()

    response = client.post(
        "/add",
        data={
            "title": "",
            "description": "Missing title",
            "subject": "Cloud Computing",
            "priority": "High",
            "due_date": "2026-10-05",
        },
    )

    assert response.status_code == 400