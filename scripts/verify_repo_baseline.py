from pathlib import Path


REQUIRED_PATHS = [
    "README.md",
    "src/tc1_service.py",
    "tests/test_tc1_service.py",
    "config/operations.yml",
    "docs/runbook.md",
    "docs/release-checklist.md",
]


def main() -> int:
    missing = [path for path in REQUIRED_PATHS if not Path(path).exists()]
    if missing:
        print("Missing required repository paths:")
        for path in missing:
            print(f"- {path}")
        return 1
    print("TC1 repository baseline looks ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
