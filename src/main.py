import json
import csv
import argparse
import os
from scraper import search_youtube
from formatter import format_video_data

# ---------------- PATH SETUP ---------------- #
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, "data")


# ---------------- SAVE FUNCTIONS ---------------- #
def save_to_json(data, filename=None):
    if filename is None:
        filename = os.path.join(DATA_DIR, "output.json")

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"❌ Error saving JSON: {e}")


def save_to_csv(data, filename=None):
    if not data:
        print("⚠️ No data to save in CSV.")
        return

    if filename is None:
        filename = os.path.join(DATA_DIR, "output.csv")

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    try:
        keys = data[0].keys()

        with open(filename, "w", newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)

    except Exception as e:
        print(f"❌ Error saving CSV: {e}")


# ---------------- MAIN EXECUTION ---------------- #
def main():
    parser = argparse.ArgumentParser(
        description="YouTube Scraper Tool - Fetch, Filter, and Save Video Data"
    )

    parser.add_argument("--query", type=str, required=True, help="Search query")
    parser.add_argument("--max", type=int, default=10, help="Max results to fetch")
    parser.add_argument("--min_views", type=int, default=10000, help="Minimum views filter")

    args = parser.parse_args()

    try:
        raw_data = search_youtube(args.query, args.max)
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return

    if not raw_data:
        print("❌ No results fetched from YouTube.")
        return

    clean_data = format_video_data(raw_data, args.query, args.min_views)

    print(f"\n🔎 Total fetched: {len(raw_data)}")
    print(f"✅ After filtering: {len(clean_data)}")

    if not clean_data:
        print("⚠️ No videos matched your filter criteria.")
        return

    save_to_json(clean_data)
    save_to_csv(clean_data)

    print("\n📁 Data saved successfully (JSON + CSV)\n")

    print("🔥 Top Results:\n")
    for i, video in enumerate(clean_data[:5], 1):
      print(f"{i}. {video['title']}")
      print(f"   👁 Views: {video['views']} | ⭐ Score: {video['score']}")


# ---------------- ENTRY POINT ---------------- #
if __name__ == "__main__":
    main()