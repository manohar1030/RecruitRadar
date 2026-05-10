import sys
from datetime import datetime
from scraper import run_apify_scraper, extract_post_data
from ai_filter import filter_real_posts
from storage import add_posts


def run_daily_job():
    print(f"\n{'='*50}")
    print(f"🚀 Daily LinkedIn Automation Started")
    print(f"⏰ Time: {datetime.now().strftime('%d/%m/%Y %H:%M')} IST")
    print(f"{'='*50}\n")

    try:
        # Step 1: Scrape
        raw_posts = run_apify_scraper()
        if not raw_posts:
            print("❌ No posts scraped. Exiting.")
            return

        # Step 2: Extract
        posts = [extract_post_data(p) for p in raw_posts]

        # Step 3: AI Filter
        real_posts = filter_real_posts(posts, limit=4)
        if not real_posts:
            print("❌ No real hiring posts found.")
            return

        # Step 4: Save to MongoDB
        add_posts(real_posts)

        print(f"\n{'='*50}")
        print(f"✅ Done! {len(real_posts)} recruiters saved.")
        print(f"{'='*50}\n")

    except Exception as e:
        print(f"❌ ERROR: Daily job failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    run_daily_job()