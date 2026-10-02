from app.api import documents


def auth(client):
    token = client.post('/auth/login', json={'username': 'admin', 'password': 'test-password'}).json()['access_token']
    return {'Authorization': f'Bearer {token}'}


def test_legacy_document_routes_create_update_and_preserve_history(client):
    headers = auth(client)
    created = client.post('/documents/', headers=headers, json={'doc_type': 'وارد', 'doc_number': 'TEST-1', 'subject': 'test', 'date': '2026-10-02T00:00:00'})
    assert created.status_code == 200
    doc_id = created.json()['id']
    assert client.put(f'/documents/{doc_id}', headers=headers, json={'subject': 'updated'}).status_code == 200
    assert client.get(f'/documents/{doc_id}', headers=headers).json()['subject'] == 'updated'
    assert len(client.get(f'/documents/{doc_id}/history', headers=headers).json()) == 2


def test_pdf_storage_uses_generated_names_and_unique_document_numbers(client, tmp_path, monkeypatch):
    monkeypatch.setattr(documents, 'UPLOAD_DIR', str(tmp_path))
    monkeypatch.setattr(documents, 'process_pdf_file', lambda path: {'subject': 'offline OCR fixture', 'content': 'text'})
    headers = auth(client)
    first = client.post('/documents/upload-pdf', headers=headers, files={'file': ('../fixture.pdf', b'%PDF-fixture', 'application/pdf')})
    second = client.post('/documents/upload-pdf', headers=headers, files={'file': ('../fixture.pdf', b'%PDF-fixture', 'application/pdf')})
    assert first.status_code == second.status_code == 200
    assert first.json()['doc_number'] != second.json()['doc_number']
    assert len(list(tmp_path.glob('*.pdf'))) == 2
    assert all('fixture' not in path.name for path in tmp_path.iterdir())


def test_legacy_history_read_and_delete_preserve_warid_history_with_same_id(client):
    from app.db.database import get_db
    from app.main import app
    from app.models import DocumentHistory
    headers = auth(client)
    created = client.post('/documents/', headers=headers, json={'doc_type': 'وارد', 'doc_number': 'TEST-COLLISION', 'subject': 'legacy', 'date': '2026-10-02T00:00:00'}).json()
    database = app.dependency_overrides[get_db]()
    db = next(database)
    db.add(DocumentHistory(document_id=created['id'], document_type='warid', action='created', action_by=1))
    db.commit()
    database.close()
    history = client.get(f"/documents/{created['id']}/history", headers=headers)
    assert history.status_code == 200
    assert len(history.json()) == 1
    assert history.json()[0]['document_type'] == 'document'
    assert client.delete(f"/documents/{created['id']}", headers=headers).status_code == 200
    database = app.dependency_overrides[get_db]()
    db = next(database)
    assert db.query(DocumentHistory).filter(DocumentHistory.document_type == 'warid').count() == 1
    database.close()
