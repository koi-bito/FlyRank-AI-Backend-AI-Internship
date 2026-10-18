import os
from repository import SQLiteTaskRepository

def test_sqlite_repository_contract():
    print("=== Testing Repository Interface Contract ===")
    test_db = "test_repo.db"
    if os.path.exists(test_db):
        os.remove(test_db)
        
    repo = SQLiteTaskRepository(test_db)
    
    # Check default seeded tasks
    tasks = repo.get_all()
    assert len(tasks) == 3
    print(f"[PASS] get_all() returned {len(tasks)} seeded records.")
    
    # Create task
    new_task = repo.create("Verify repository pattern")
    assert new_task["id"] == 4
    assert new_task["title"] == "Verify repository pattern"
    assert new_task["done"] == 0 or new_task["done"] is False
    print(f"[PASS] create() inserted task ID {new_task['id']}")
    
    # Get by ID
    fetched = repo.get_by_id(4)
    assert fetched is not None
    assert fetched["title"] == "Verify repository pattern"
    print(f"[PASS] get_by_id(4) retrieved: {fetched['title']}")
    
    # Update task
    updated = repo.update(4, title="Updated repository pattern", done=True)
    assert updated is not None
    assert updated["title"] == "Updated repository pattern"
    assert updated["done"] == 1 or updated["done"] is True
    print(f"[PASS] update(4) verified.")
    
    # Delete task
    deleted = repo.delete(4)
    assert deleted is True
    assert repo.get_by_id(4) is None
    print(f"[PASS] delete(4) verified.")
    
    # Cleanup test DB
    if os.path.exists(test_db):
        os.remove(test_db)
        
    print("\n>>> REPOSITORY CONTRACT TEST PASSED! <<<")

if __name__ == "__main__":
    test_sqlite_repository_contract()
