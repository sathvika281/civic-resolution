from app.db.factory import get_repository
from app.services.seed_service import seed_all


def main() -> None:
    repo = get_repository()
    seed_all(repo)
    print("Seed complete.")


if __name__ == "__main__":
    main()
