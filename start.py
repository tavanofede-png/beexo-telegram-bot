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
