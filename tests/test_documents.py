
def test_create_document(client):
    response = client.post(
        "/documents",
        json={
            "title": "Dokumen Testing",
            "content": "Testing create document",
            "user_id": None
        }
    )

    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "Dokumen Testing"
    assert data["content"] == "Testing create document"
    assert "id" in data

def test_read_all_documents(client):
    client.post(
        "/documents",
        json={
            "title": "Dokumen Pertama",
            "content": "Isi dokumen pertama",
            "user_id": None
        }
    )

    response = client.get("/documents")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Dokumen Pertama"

def test_read_single_document(client):
    create_response = client.post(
        "/documents",
        json={
            "title": "Dokumen Detail",
            "content": "Testing read document",
            "user_id": None
        }
    )

    document_id = create_response.json()["id"]

    response = client.get(f"/documents/{document_id}")

    assert response.status_code == 200
    assert response.json()["id"] == document_id
    assert response.json()["title"] == "Dokumen Detail"

def test_update_document(client):
    create_response = client.post(
        "/documents",
        json={
            "title": "Judul Lama",
            "content": "Konten lama",
            "user_id": None
        }
    )

    document_id = create_response.json()["id"]

    response = client.patch(
        f"/documents/{document_id}",
        json={
            "title": "Judul Baru",
            "content": "Konten baru"
        }
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Judul Baru"
    assert response.json()["content"] == "Konten baru"

def test_delete_document(client):
    create_response = client.post(
        "/documents",
        json={
            "title": "Dokumen Hapus",
            "content": "Dokumen untuk testing delete",
            "user_id": None
        }
    )

    document_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/documents/{document_id}"
    )

    assert delete_response.status_code == 204

    get_response = client.get(f"/documents/{document_id}")

    assert get_response.status_code == 404