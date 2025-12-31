import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from stackoverflow_collector import StackOverflowCollector


def main() -> None:
    load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

    api_key = os.getenv("STACKEXCHANGE_API_KEY")
    print("Loaded API key?", bool(api_key))

    collector = StackOverflowCollector(api_key=api_key, print_quota=True)

    rows = collector.get_questions(
        tagged=["python"],
        min_score=20,
        min_answers=2,
        max_pages=1,
        page_size=20,
        require_accepted=True,
    )

    df = pd.DataFrame(rows)

    print("\nrows collected:", len(df))
    if len(df) > 0:
        print("\nColumns:", df.columns.tolist())
        print("\nSample titles:")
        print(df["question_title"].head(5).to_string(index=False))

        out = Path("data/raw")
        out.mkdir(parents=True, exist_ok=True)
        df.to_csv(out / "stackoverflow_sample.csv", index=False)
        print("\nSaved to: data/raw/stackoverflow_sample.csv")

if __name__ == "__main__":
    main()