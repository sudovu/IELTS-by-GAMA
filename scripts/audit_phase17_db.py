import sqlite3
import os

for path in ['data/ielts_gama.db', 'data/ielts_gama_phase17_backup.db']:
    con = sqlite3.connect(path)
    cur = con.cursor()
    integ = cur.execute('PRAGMA integrity_check').fetchall()
    fk = cur.execute('PRAGMA foreign_key_check').fetchall()
    tbls = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    print(f"Path: {path}")
    print(f"  Integrity check: {integ}")
    print(f"  Foreign key check violations: {len(fk)}")
    print(f"  Table count: {len(tbls)}")
    print(f"  Tables: {tbls}")
    con.close()

# Test restoration into temporary database
import tempfile
with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_file:
    tmp_path = tmp_file.name

try:
    src_con = sqlite3.connect('data/ielts_gama_phase17_backup.db')
    dst_con = sqlite3.connect(tmp_path)
    src_con.backup(dst_con)
    cur = dst_con.cursor()
    restored_integ = cur.execute('PRAGMA integrity_check').fetchall()
    restored_tbls = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    print(f"Restoration Test into {tmp_path}:")
    print(f"  Integrity: {restored_integ}")
    print(f"  Restored table count: {len(restored_tbls)}")
    src_con.close()
    dst_con.close()
finally:
    if os.path.exists(tmp_path):
        os.remove(tmp_path)
        print("  Temporary restoration DB cleaned up successfully.")
