import os
import subprocess
import sys


def run_migration_if_requested():
    v = os.getenv("MIGRATE_ON_START")
    if not v or v.lower() not in ("1", "true", "yes"):
        return

    print("MIGRATE_ON_START detected — running migration script...")
    sys.stdout.flush()
    try:
        # Ensure SQLite file is available at expected path inside container.
        # The repo may place the DB at different paths; search for it and copy
        # to `beexo-telegram-bot/beexy_history.db` if found.
        import shutil
        expected = os.path.join(os.path.dirname(__file__), "beexo-telegram-bot", "beexy_history.db")
        if not os.path.exists(expected):
            print(f"Looking for beexy_history.db in project tree...")
            for root, dirs, files in os.walk(os.path.dirname(__file__)):
                if 'beexy_history.db' in files:
                    src = os.path.join(root, 'beexy_history.db')
                    try:
                        os.makedirs(os.path.dirname(expected), exist_ok=True)
                        shutil.copy2(src, expected)
                        print(f"Copied {src} -> {expected}")
                        break
                    except Exception as _e:
                        print("Failed to copy local sqlite:", _e)
        else:
            print(f"SQLite already present at {expected}")

        # Run the migration script using the same Python interpreter
        completed = subprocess.run(
            [sys.executable, "beexo-telegram-bot/tools/migrate_sqlite_to_postgres.py"],
            check=False,
        )
        print(f"Migration exit code: {completed.returncode}")
    except Exception as e:
        print("Migration failed with exception:", e)
    sys.stdout.flush()


def start_bot():
    # Replace current process with the bot process
    print("Starting bot...")
    sys.stdout.flush()
    os.execv(sys.executable, [sys.executable, "beexo-telegram-bot/bot.py"])


if __name__ == "__main__":
    run_migration_if_requested()
    start_bot()
