import sqlite3
import os
import tempfile

def create_and_verify_backup():
    src_path = "data/ielts_gama.db"
    dst_path = "data/ielts_gama_phase18_backup.db"

    # 1. Create backup via SQLite online backup API
    src_conn = sqlite3.connect(src_path)
    dst_conn = sqlite3.connect(dst_path)
    with dst_conn:
        src_conn.backup(dst_conn)
    dst_conn.close()
    src_conn.close()

    # 2. Verify backup
    verify_conn = sqlite3.connect(dst_path)
    integrity = verify_conn.execute("PRAGMA integrity_check").fetchall()
    fk = verify_conn.execute("PRAGMA foreign_key_check").fetchall()
    tables = [r[0] for r in verify_conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    size = os.path.getsize(dst_path)
    verify_conn.close()

    print(f"Backup created: {dst_path}")
    print(f"File size: {size} bytes")
    print(f"Integrity check: {integrity}")
    print(f"Foreign key violations: {len(fk)}")
    print(f"Table count: {len(tables)}")

    # 3. Test restoration into isolated temporary database
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    tmp_path = tmp_file.name
    tmp_file.close()

    try:
        b_conn = sqlite3.connect(dst_path)
        r_conn = sqlite3.connect(tmp_path)
        with r_conn:
            b_conn.backup(r_conn)
        b_conn.close()
        r_conn.close()

        chk_conn = sqlite3.connect(tmp_path)
        r_integrity = chk_conn.execute("PRAGMA integrity_check").fetchall()
        r_tables = [r[0] for r in chk_conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
        chk_conn.close()

        print(f"Temporary restoration check: {r_integrity}, restored tables: {len(r_tables)}")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

if __name__ == "__main__":
    create_and_verify_backup()
