DUNE = {"title": "Dune", "author": "Frank Herbert", "year": 1965}


def test_create_book(client):
    r = client.post("/books", json=DUNE)
    assert r.status_code == 201
    assert r.json()["id"] is not None


def test_duplicate_returns_409(client):
    client.post("/books", json=DUNE)
    r = client.post("/books", json=DUNE)
    assert r.status_code == 409


def test_invalid_input_returns_422(client):
    r = client.post("/books", json={"title": "", "author": "X", "year": 1965})
    assert r.status_code == 422


def test_get_missing_returns_404(client):
    r = client.get("/books/999")
    assert r.status_code == 404


def test_patch_changes_only_given_fields(client):
    book_id = client.post("/books", json=DUNE).json()["id"]
    r = client.patch(f"/books/{book_id}", json={"year": 1966})
    assert r.status_code == 200
    assert r.json()["year"] == 1966
    assert r.json()["title"] == "Dune"


def test_delete_then_get_returns_404(client):
    book_id = client.post("/books", json=DUNE).json()["id"]
    assert client.delete(f"/books/{book_id}").status_code == 204
    assert client.get(f"/books/{book_id}").status_code == 404


def test_list_respects_limit(client):
    for i in range(3):
        client.post("/books", json={**DUNE, "title": f"Book {i}"})
    r = client.get("/books?limit=2")
    assert len(r.json()) == 2
