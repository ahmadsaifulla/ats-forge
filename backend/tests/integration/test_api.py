"""Integration tests for API endpoints."""

from io import BytesIO

from fastapi.testclient import TestClient


def test_upload_analyze_optimize_download_flow(
    client: TestClient,
    sample_docx_bytes: bytes,
    sample_job_description: str,
):
    upload_response = client.post(
        "/api/upload-resume",
        files={
            "file": (
                "resume.docx",
                BytesIO(sample_docx_bytes),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        },
    )
    assert upload_response.status_code == 200
    resume_id = upload_response.json()["resume"]["resume_id"]

    analyze_response = client.post(
        "/api/analyze",
        json={"resume_id": resume_id, "job_description": sample_job_description},
    )
    assert analyze_response.status_code == 200
    assert analyze_response.json()["total_score"] >= 0

    optimize_response = client.post(
        "/api/optimize",
        json={"resume_id": resume_id, "job_description": sample_job_description},
    )
    assert optimize_response.status_code == 200
    document_id = optimize_response.json()["optimized_resume"]["document_id"]

    download_response = client.get(f"/api/download/{document_id}")
    assert download_response.status_code == 200
    assert download_response.headers["content-type"].startswith(
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )


def test_upload_rejects_empty_file(client: TestClient):
    response = client.post(
        "/api/upload-resume",
        files={"file": ("empty.docx", BytesIO(b""), "application/octet-stream")},
    )

    assert response.status_code == 400
    assert "empty" in response.json()["reason"].lower()


def test_analyze_rejects_short_job_description(client: TestClient, sample_docx_bytes: bytes):
    upload_response = client.post(
        "/api/upload-resume",
        files={
            "file": (
                "resume.docx",
                BytesIO(sample_docx_bytes),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        },
    )
    resume_id = upload_response.json()["resume"]["resume_id"]

    response = client.post(
        "/api/analyze",
        json={"resume_id": resume_id, "job_description": "Too short"},
    )

    assert response.status_code == 422
    assert response.json()["error"] == "validation_error"


def test_upload_rejects_huge_file(client: TestClient):
    large_content = b"a" * (11 * 1024 * 1024)
    response = client.post(
        "/api/upload-resume",
        files={"file": ("huge.pdf", BytesIO(large_content), "application/pdf")},
    )

    assert response.status_code == 400
    assert "limit" in response.json()["reason"].lower()
