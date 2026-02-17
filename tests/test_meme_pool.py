"""
Tests para meme_pool.py — pool de memes con rotación.
"""

import sys
import os
import json
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "beexo-telegram-bot"))

os.environ.setdefault("TELEGRAM_BOT_TOKEN", "test:token")
os.environ.setdefault("TARGET_CHAT_IDS", "123")
os.environ.setdefault("GROQ_API_KEY", "test_key")
os.environ.setdefault("GEMINI_API_KEY", "test_key")

import pytest
import meme_pool


@pytest.fixture(autouse=True)
def temp_pool(tmp_path):
    """Usa un directorio temporal para el pool y memes."""
    pool_file = str(tmp_path / "memes_pool.json")
    memes_dir = str(tmp_path / "memes")
    os.makedirs(memes_dir, exist_ok=True)

    # Patch paths
    original_pool = meme_pool.POOL_PATH
    original_dir = meme_pool.MEMES_DIR
    meme_pool.POOL_PATH = pool_file
    meme_pool.MEMES_DIR = memes_dir
    yield tmp_path
    meme_pool.POOL_PATH = original_pool
    meme_pool.MEMES_DIR = original_dir


def _create_test_pool(tmp_path, count=5):
    """Crea un pool de prueba con memes sintéticos."""
    pool = []
    memes_dir = str(tmp_path / "memes")
    for i in range(1, count + 1):
        filename = f"meme_{i:04d}.png"
        pool.append({
            "id": i,
            "file": filename,
            "top": f"Top text {i}",
            "bottom": f"Bottom text {i}",
            "grad_top": "#0a0a1a",
            "grad_bottom": "#1a1a3a",
            "accent": "#4ecdc4",
            "sep": "line",
            "icon": "TEST",
            "used": False,
        })
        # Crear archivo dummy
        with open(os.path.join(memes_dir, filename), "w") as f:
            f.write("fake png")
    meme_pool._save_pool(pool)
    return pool


class TestPoolCRUD:
    """Tests para operaciones CRUD del pool."""

    def test_load_empty(self):
        pool = meme_pool._load_pool()
        assert pool == []

    def test_save_and_load(self, tmp_path):
        _create_test_pool(tmp_path, 3)
        pool = meme_pool._load_pool()
        assert len(pool) == 3

    def test_pool_size(self, tmp_path):
        _create_test_pool(tmp_path, 5)
        assert meme_pool.pool_size() == 5


class TestPickMeme:
    """Tests para pick_meme() — selección de memes."""

    def test_picks_one(self, tmp_path):
        _create_test_pool(tmp_path, 5)
        meme = meme_pool.pick_meme()
        assert meme is not None
        assert "top" in meme
        assert "bottom" in meme
        assert "file" in meme

    def test_marks_as_used(self, tmp_path):
        _create_test_pool(tmp_path, 5)
        meme = meme_pool.pick_meme()
        # Pool should have 4 available now
        assert meme_pool.pool_size() == 4

    def test_picks_all(self, tmp_path):
        _create_test_pool(tmp_path, 3)
        ids = set()
        for _ in range(3):
            m = meme_pool.pick_meme()
            assert m is not None
            ids.add(m["id"])
        assert len(ids) == 3
        assert meme_pool.pool_size() == 0


class TestRemoveMeme:
    """Tests para remove_meme() — eliminar y borrar archivo."""

    def test_removes_from_pool(self, tmp_path):
        _create_test_pool(tmp_path, 3)
        result = meme_pool.remove_meme(1)
        assert result is True
        pool = meme_pool._load_pool()
        assert len(pool) == 2
        assert all(m["id"] != 1 for m in pool)

    def test_deletes_file(self, tmp_path):
        _create_test_pool(tmp_path, 3)
        memes_dir = str(tmp_path / "memes")
        assert os.path.exists(os.path.join(memes_dir, "meme_0001.png"))
        meme_pool.remove_meme(1)
        assert not os.path.exists(os.path.join(memes_dir, "meme_0001.png"))

    def test_nonexistent_id(self, tmp_path):
        _create_test_pool(tmp_path, 3)
        result = meme_pool.remove_meme(999)
        assert result is False


class TestAddMeme:
    """Tests para add_meme() — agregar meme nuevo."""

    def test_adds_to_pool(self, tmp_path):
        _create_test_pool(tmp_path, 2)
        meme = meme_pool.add_meme("Nuevo top", "Nuevo bottom")
        pool = meme_pool._load_pool()
        assert len(pool) == 3
        assert pool[-1]["top"] == "Nuevo top"
        assert pool[-1]["id"] == 3  # max_id was 2, new is 3

    def test_increments_id(self, tmp_path):
        _create_test_pool(tmp_path, 5)
        meme = meme_pool.add_meme("Test", "Test")
        assert meme["id"] == 6


class TestPoolRotation:
    """Tests para el flujo completo: pick → remove → add."""

    def test_full_rotation(self, tmp_path):
        _create_test_pool(tmp_path, 3)
        # Pick one
        meme = meme_pool.pick_meme()
        assert meme is not None
        initial_id = meme["id"]
        # Remove it
        meme_pool.remove_meme(initial_id)
        # Add replacement
        new = meme_pool.add_meme("Reemplazo", "De meme")
        pool = meme_pool._load_pool()
        assert len(pool) == 3  # 3 - 1 + 1 = 3
        assert pool[-1]["top"] == "Reemplazo"
        assert new["id"] > 0
