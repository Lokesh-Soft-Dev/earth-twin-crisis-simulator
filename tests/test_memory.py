# tests/test_memory.py
from memory.memory_store import read_memory, append_memory, clear_memory

def test_memory_append_and_read():
    clear_memory()
    append_memory({"event": "test1"})
    data = read_memory()
    assert len(data.get("sessions", [])) == 1
    assert data["sessions"][0]["event"] == "test1"
    clear_memory()
