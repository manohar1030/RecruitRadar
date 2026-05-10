import schedule
import time
import sys
from datetime import datetime
from scraper import run_apify_scraper, extract_post_data
from ai_filter import filter_real_posts
from storage import add_posts


def run_daily_job():
    """Main daily job - scrape, filter, save"""
    print(f"\n{'='*50}")
    print(f"Daily LinkedIn Automation Started")
    print(f"Time: {datetime.now().strftime('%d/%m/%Y %H:%M')} IST")
    print(f"{'='*50}\n")

    try:
        # Step 1: Scrape posts
        raw_posts = run_apify_scraper()

        if not raw_posts:
            print("No posts scraped. Exiting.")
            return

        # Step 2: Extract needed fields
        posts = [extract_post_data(p) for p in raw_posts]

        # Step 3: AI filter
        real_posts = filter_real_posts(posts, limit=4)

        if not real_posts:
            print("No real hiring posts found today.")
            return

        # Step 4: Save to MongoDB
        add_posts(real_posts)

        print(f"\n{'='*50}")
        print(f"Done! {len(real_posts)} recruiters saved.")
        print(f"Open Streamlit dashboard to view.")
        print(f"{'='*50}\n")

    except Exception as e:
        print(f"❌ ERROR: Daily job failed due to an exception: {e}", file=sys.stderr)


if __name__ == "__main__":
    print("Scheduler started — runs daily at 9:00 AM IST")
    print("Press Ctrl+C to stop\n")

    # Schedule daily at 9 AM
    schedule.every().day.at("09:00").do(run_daily_job)

    # Run immediately on first start
    print("Running now for first time...")
    run_daily_job()

    # Keep running
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)
        except KeyboardInterrupt:
            print("Scheduler stopped manually.")
            break
        except Exception as e:
            print(f"Scheduler loop error: {e}", file=sys.stderr)
            time.sleep(60)