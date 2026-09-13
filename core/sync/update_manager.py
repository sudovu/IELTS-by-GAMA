"""
Content and Knowledge Update Manager for IELTS by GAMA.
Supports versioned incremental updates, SHA256 checksum verification,
offline update package (.gama bundle) import/export, and automatic rollback.
"""

import hashlib
import json
import os
import shutil
import zipfile
import datetime
from typing import Dict, Any, List, Optional
from ..database.db_manager import DatabaseManager
from ..database.repositories import KnowledgeRepository, SettingsRepository


class UpdateManager:
    """Handles versioned content synchronization and offline packages."""

    def __init__(self, db: DatabaseManager = None):
        self.db = db or DatabaseManager()
        self.knowledge_repo = KnowledgeRepository(self.db)
        self.settings_repo = SettingsRepository(self.db)

    def get_current_version(self) -> str:
        return self.settings_repo.get("content_version", "1.0.0")

    def _compute_checksum(self, data: str) -> str:
        return hashlib.sha256(data.encode("utf-8")).hexdigest()

    def create_offline_package(self, output_zip_path: str, version: str = "1.1.0") -> str:
        """Exports the compact knowledge base and content catalog into a portable .gama package."""
        all_knowledge = self.knowledge_repo.get_all(limit=5000)
        payload = {
            "version": version,
            "exported_at": datetime.datetime.utcnow().isoformat(),
            "items_count": len(all_knowledge),
            "items": all_knowledge
        }
        raw_json = json.dumps(payload, indent=2, ensure_ascii=False)
        checksum = self._compute_checksum(raw_json)

        manifest = {
            "package_type": "gama_offline_update",
            "version": version,
            "created_at": payload["exported_at"],
            "checksum_sha256": checksum
        }

        os.makedirs(os.path.dirname(os.path.abspath(output_zip_path)), exist_ok=True)
        with zipfile.ZipFile(output_zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("manifest.json", json.dumps(manifest, indent=2))
            zf.writestr("content.json", raw_json)

        return output_zip_path

    def import_offline_package(self, package_zip_path: str) -> Dict[str, Any]:
        """Validates checksum, creates rollback snapshot, and merges content into SQLite."""
        if not os.path.exists(package_zip_path):
            raise FileNotFoundError(f"Package {package_zip_path} not found")

        with zipfile.ZipFile(package_zip_path, "r") as zf:
            if "manifest.json" not in zf.namelist() or "content.json" not in zf.namelist():
                raise ValueError("Invalid .gama package: missing manifest.json or content.json")

            manifest = json.loads(zf.read("manifest.json").decode("utf-8"))
            content_bytes = zf.read("content.json")
            content_str = content_bytes.decode("utf-8")

            # Validate checksum
            actual_checksum = self._compute_checksum(content_str)
            if actual_checksum != manifest.get("checksum_sha256"):
                raise ValueError("Checksum verification failed: package data may be corrupted or tampered")

            data = json.loads(content_str)

        # Create rollback snapshot of current knowledge
        snapshot = self.knowledge_repo.get_all(limit=5000)
        self.settings_repo.set("last_rollback_snapshot", json.dumps(snapshot))
        self.settings_repo.set("last_rollback_version", self.get_current_version())

        # Incremental deduplicated upsert
        inserted = 0
        updated = 0
        for item in data.get("items", []):
            existing = self.db.fetchone(
                "SELECT id, compact_knowledge FROM knowledge_base WHERE topic = ? AND query_trigger = ?",
                (item["topic"], item["query_trigger"])
            )
            if existing:
                if existing["compact_knowledge"] != item["compact_knowledge"]:
                    self.knowledge_repo.upsert_knowledge(
                        topic=item["topic"],
                        query_trigger=item["query_trigger"],
                        compact_knowledge=item["compact_knowledge"],
                        subtopic=item.get("subtopic"),
                        source=item.get("source", "package_update"),
                        confidence=item.get("confidence", 0.95),
                        version=data.get("version", "1.1.0")
                    )
                    updated += 1
            else:
                self.knowledge_repo.upsert_knowledge(
                    topic=item["topic"],
                    query_trigger=item["query_trigger"],
                    compact_knowledge=item["compact_knowledge"],
                    subtopic=item.get("subtopic"),
                    source=item.get("source", "package_update"),
                    confidence=item.get("confidence", 0.95),
                    version=data.get("version", "1.1.0")
                )
                inserted += 1

        new_version = data.get("version", "1.1.0")
        self.settings_repo.set("content_version", new_version)

        return {
            "success": True,
            "version": new_version,
            "inserted": inserted,
            "updated": updated,
            "total_processed": len(data.get("items", []))
        }

    def rollback(self) -> Dict[str, Any]:
        """Rolls back to pre-update snapshot if available."""
        snapshot_json = self.settings_repo.get("last_rollback_snapshot")
        if not snapshot_json:
            return {"success": False, "message": "No rollback snapshot found"}

        items = json.loads(snapshot_json)
        old_version = self.settings_repo.get("last_rollback_version", "1.0.0")

        # Restore items
        for item in items:
            self.knowledge_repo.upsert_knowledge(
                topic=item["topic"],
                query_trigger=item["query_trigger"],
                compact_knowledge=item["compact_knowledge"],
                subtopic=item.get("subtopic"),
                source=item.get("source", "curated"),
                confidence=item.get("confidence", 0.95),
                version=old_version
            )

        self.settings_repo.set("content_version", old_version)
        self.settings_repo.set("last_rollback_snapshot", "")

        return {
            "success": True,
            "restored_version": old_version,
            "restored_count": len(items)
        }
