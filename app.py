import streamlit as st
from storage import load_data, update_status, get_grouped_data

# Page config
st.set_page_config(
    page_title="LinkedIn Hiring Tracker",
    page_icon="💼",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Minimal CSS to tweak standard Streamlit components
st.markdown("""
<style>
    /* Clean up the default Streamlit padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 800px; /* Keep it minimal and readable */
    }

    /* Make badges look clean */
    .badge-sent {
        background-color: #e6f4ea;
        color: #1e8e3e;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
    }
    
    .badge-pending {
        background-color: #fce8e6;
        color: #d93025;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
    }

    /* Minimal divider */
    hr {
        margin-top: 1rem;
        margin-bottom: 1.5rem;
        border: 0;
        border-top: 1px solid #f0f0f0;
    }

    /* Dark mode adjustments for badges and dividers */
    @media (prefers-color-scheme: dark) {
        .badge-sent { background-color: rgba(30, 142, 62, 0.2); }
        .badge-pending { background-color: rgba(217, 48, 37, 0.2); }
        hr { border-top: 1px solid #333; }
    }
</style>
""", unsafe_allow_html=True)


def render_header(total, sent, unsent):
    st.title("LinkedIn Hiring Tracker")
    st.markdown("AI-powered daily recruiter finder — only real hiring posts.")
    st.write("") # Spacing
    
    # Use Streamlit's native metric components for a minimal look
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Recruiters", total)
    col2.metric("Requests Sent", sent)
    col3.metric("Pending", unsent)
    
    st.markdown("<hr>", unsafe_allow_html=True)


def render_card(post):
    contact = post.get("contactInfo", "")
    profile_url = post.get("profileUrl", "")
    post_url = post.get("postUrl", "")
    status = post.get("status", "unsent")
    post_id = post.get("id", "")

    # Native Streamlit container with a border makes a perfect minimal card
    with st.container(border=True):
        col_text, col_badge = st.columns([4, 1])
        
        with col_text:
            st.markdown(f"**{post.get('posterName', 'Unknown')}** • {post.get('jobCompany', 'Not specified')}")
            if contact:
                st.caption(f"📧 {contact}")
            else:
                st.caption("No contact info found")
                
        with col_badge:
            if status == "sent":
                st.markdown("<div align='right'><span class='badge-sent'>SENT</span></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div align='right'><span class='badge-pending'>PENDING</span></div>", unsafe_allow_html=True)

        st.write("") # Small spacing before buttons
        
        # Action Buttons
        btn_col1, btn_col2, btn_col3 = st.columns(3)
        
        with btn_col1:
            if profile_url:
                st.link_button("Profile", profile_url, use_container_width=True)
            else:
                st.button("Profile", disabled=True, use_container_width=True, key=f"np_{post_id}")

        with btn_col2:
            if post_url:
                st.link_button("Post", post_url, use_container_width=True)
            else:
                st.button("Post", disabled=True, use_container_width=True, key=f"npo_{post_id}")

        with btn_col3:
            if status == "unsent":
                if st.button("Mark Sent", key=f"sent_{post_id}", use_container_width=True, type="primary"):
                    update_status(post_id, "sent")
                    st.rerun()
            else:
                if st.button("Undo", key=f"unsent_{post_id}", use_container_width=True):
                    update_status(post_id, "unsent")
                    st.rerun()


def main():
    data = load_data()
    total = len(data)
    sent = sum(1 for d in data if d.get("status") == "sent")
    unsent = total - sent

    render_header(total, sent, unsent)

    search = st.text_input("Search recruiters or companies...", label_visibility="collapsed", placeholder="Search recruiters or companies...")
    st.write("") # Spacing

    grouped = get_grouped_data()

    if not grouped:
        st.info("No data yet. Run `python scheduler.py` to fetch today's hiring posts.")
        return

    # Filter and display posts
    for date, posts in grouped.items():
        filtered = posts
        if search:
            filtered = [
                p for p in posts
                if search.lower() in p.get("posterName", "").lower()
                or search.lower() in p.get("jobCompany", "").lower()
            ]

        if not filtered:
            continue
            
        st.subheader(f"{date}", divider="gray")

        # Display cards one per row for a cleaner, readable timeline
        for post in filtered:
            render_card(post)


if __name__ == "__main__":
    main()