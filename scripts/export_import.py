"""
Data Export and Offline Package Utility for IELTS by GAMA.
CLI interface for backing up learner progress and packaging offline curriculum updates.
"""

import argparse
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from core.database.db_manager import DatabaseManager
from core.progress.analytics import LearningAnalytics
from core.sync.update_manager import UpdateManager


def main():
    parser = argparse.ArgumentParser(description="IELTS by GAMA Data & Package Utility")
    subparsers = parser.add_subparsers(dest="action", help="Action to execute")

    # Export learner
    exp_p = subparsers.add_parser("export-learner", help="Export learner data to JSON")
    exp_p.add_argument("--learner-id", default="default_learner", help="Learner ID")
    exp_p.add_argument("--out", required=True, help="Output JSON path")

    # Import learner
    imp_p = subparsers.add_parser("import-learner", help="Import learner data from JSON")
    imp_p.add_argument("--learner-id", default="default_learner", help="Learner ID")
    imp_p.add_argument("--src", required=True, help="Source JSON path")

    # Create offline update package
    pkg_p = subparsers.add_parser("create-package", help="Create a portable .gama offline update zip")
    pkg_p.add_argument("--version", default="1.1.0", help="New content version")
    pkg_p.add_argument("--out", required=True, help="Output .gama or .zip package path")

    # Import offline package
    imp_pkg = subparsers.add_parser("import-package", help="Import a .gama offline update zip")
    imp_pkg.add_argument("--src", required=True, help="Package path")

    # Rollback
    subparsers.add_parser("rollback-package", help="Rollback last imported update")

    args = parser.parse_args()
    db = DatabaseManager()
    analytics = LearningAnalytics(db)
    updater = UpdateManager(db)

    if args.action == "export-learner":
        data = analytics.export_learner_data_json(args.learner_id)
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(data)
        print(f"[OK] Exported learner profile and mistakes to {args.out}")

    elif args.action == "import-learner":
        with open(args.src, "r", encoding="utf-8") as f:
            data = f.read()
        res = analytics.import_learner_data_json(args.learner_id, data)
        print(f"[OK] Successfully imported {res['restored_mistakes']} mistakes for {args.learner_id}")

    elif args.action == "create-package":
        out_path = updater.create_offline_package(args.out, version=args.version)
        print(f"[OK] Created offline package at {out_path} (Version {args.version})")

    elif args.action == "import-package":
        res = updater.import_offline_package(args.src)
        print(f"[OK] Imported package: {res['inserted']} inserted, {res['updated']} updated (Version {res['version']})")

    elif args.action == "rollback-package":
        res = updater.rollback()
        print(f"[OK] Rollback result: {res}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
