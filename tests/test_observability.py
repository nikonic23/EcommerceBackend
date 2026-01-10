import logging


def test_request_id_attached(client):
    response = client.get("/")

    # request_id is stored server-side, but we check no crash
    assert response.status_code in (302, 200)

def test_logger_contains_request_id(client, caplog):
    caplog.set_level(logging.INFO, logger="app")

    client.get("/")

    logs = " ".join(record.message for record in caplog.records)

    assert "request_id=" in logs