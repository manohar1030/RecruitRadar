import streamlit as st
from storage import load_data, update_status, get_grouped_data

st.set_page_config(
    page_title="LinkedIn Hiring Tracker",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Layout */
    .block-container {
        padding: 2.5rem 3rem 3rem 3rem;
        max-width: 1100px;
    }

    /* Hide default streamlit branding */
    #MainMenu, footer, header { visibility: hidden; }

    /* ── Page header ── */
    .page-header {
        margin-bottom: 2.5rem;
    }
    .page-header h1 {
        font-size: 1.75rem;
        font-weight: 700;
        color: #0f172a;
        margin: 0 0 0.25rem 0;
        letter-spacing: -0.02em;
    }
    .page-header p {
        font-size: 0.9rem;
        color: #64748b;
        margin: 0;
    }

    /* ── Stat cards ── */
    .stat-row {
        display: flex;
        gap: 1rem;
        margin-bottom: 2rem;
    }
    .stat-card {
        flex: 1;
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
    }
    .stat-label {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #94a3b8;
        margin-bottom: 0.4rem;
    }
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        color: #0f172a;
        line-height: 1;
    }
    .stat-value.green { color: #16a34a; }
    .stat-value.amber { color: #d97706; }

    /* ── Search bar override ── */
    div[data-testid="stTextInput"] input {
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        padding: 0.65rem 1rem;
        font-size: 0.875rem;
        background: #f8fafc;
        transition: border-color 0.15s;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #3b82f6;
        background: #fff;
        box-shadow: 0 0 0 3px rgba(59,130,246,0.12);
    }

    /* ── Date section header ── */
    .date-section {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin: 2rem 0 1rem 0;
    }
    .date-label {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #94a3b8;
        white-space: nowrap;
    }
    .date-line {
        flex: 1;
        height: 1px;
        background: #e2e8f0;
    }

    /* ── Post card ── */
    .post-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 1.25rem 1.5rem 0.75rem 1.5rem;
        margin-bottom: 0.25rem;
        transition: box-shadow 0.2s, border-color 0.2s;
    }
    .post-card:hover {
        box-shadow: 0 4px 20px rgba(0,0,0,0.07);
        border-color: #cbd5e1;
    }
    .card-top {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 0.5rem;
    }
    .card-name {
        font-size: 0.9375rem;
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 0.2rem;
    }
    .card-company {
        font-size: 0.8125rem;
        color: #475569;
        font-weight: 500;
    }
    .card-contact {
        font-size: 0.8125rem;
        color: #64748b;
        margin-top: 0.35rem;
    }
    .card-contact a {
        color: #3b82f6;
        text-decoration: none;
    }
    .card-contact a:hover { text-decoration: underline; }

    /* ── Status badges ── */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.3rem 0.75rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        white-space: nowrap;
    }
    .badge-sent {
        background: #dcfce7;
        color: #15803d;
        border: 1px solid #bbf7d0;
    }
    .badge-pending {
        background: #fef3c7;
        color: #92400e;
        border: 1px solid #fde68a;
    }
    .badge-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: currentColor;
    }

    /* ── Action buttons ── */
    div[data-testid="stButton"] button,
    div[data-testid="stLinkButton"] a {
        border-radius: 8px !important;
        font-size: 0.8125rem !important;
        font-weight: 500 !important;
        height: 36px !important;
        padding: 0 1rem !important;
        transition: all 0.15s !important;
    }

    div[data-testid="stButton"] button[kind="primary"] {
        background: #2563eb !important;
        border-color: #2563eb !important;
        color: #fff !important;
    }
    div[data-testid="stButton"] button[kind="primary"]:hover {
        background: #1d4ed8 !important;
        border-color: #1d4ed8 !important;
    }

    div[data-testid="stButton"] button[kind="secondary"] {
        background: #f1f5f9 !important;
        border-color: #e2e8f0 !important;
        color: #475569 !important;
    }
    div[data-testid="stButton"] button[kind="secondary"]:hover {
        background: #e2e8f0 !important;
        color: #0f172a !important;
    }

    div[data-testid="stLinkButton"] a {
        background: #f8fafc !important;
        border: 1px solid #e2e8f0 !important;
        color: #374151 !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    div[data-testid="stLinkButton"] a:hover {
        background: #f1f5f9 !important;
        border-color: #cbd5e1 !important;
    }

    /* ── Empty state ── */
    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
        color: #94a3b8;
    }
    .empty-title {
        font-size: 1rem;
        font-weight: 600;
        color: #475569;
        margin-bottom: 0.5rem;
    }
    .empty-sub {
        font-size: 0.875rem;
    }

    /* ── Dark mode ── */
    @media (prefers-color-scheme: dark) {
        .page-header h1 { color: #f1f5f9; }
        .page-header p { color: #94a3b8; }
        .stat-card { background: #1e293b; border-color: #334155; }
        .stat-value { color: #f1f5f9; }
        .post-card { background: #1e293b; border-color: #334155; }
        .post-card:hover { border-color: #475569; box-shadow: 0 4px 20px rgba(0,0,0,0.3); }
        .card-name { color: #f1f5f9; }
        .card-company { color: #94a3b8; }
        .card-contact { color: #64748b; }
        .date-line { background: #334155; }
        .badge-sent { background: rgba(21,128,61,0.15); border-color: rgba(21,128,61,0.3); color: #4ade80; }
        .badge-pending { background: rgba(146,64,14,0.15); border-color: rgba(146,64,14,0.3); color: #fbbf24; }
    }
</style>
""", unsafe_allow_html=True)


def render_header(total, sent, unsent):
    st.markdown("""
    <div class="page-header">
        <h1>LinkedIn Hiring Tracker</h1>
        <p>AI-powered recruiter finder — only verified, real hiring posts</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-card">
            <div class="stat-label">Total Recruiters</div>
            <div class="stat-value">{total}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Requests Sent</div>
            <div class="stat-value green">{sent}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Pending</div>
            <div class="stat-value amber">{unsent}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_date_header(date):
    st.markdown(f"""
    <div class="date-section">
        <span class="date-label">{date}</span>
        <div class="date-line"></div>
    </div>
    """, unsafe_allow_html=True)


def render_card(post):
    contact = post.get("contactInfo", "")
    profile_url = post.get("profileUrl", "")
    post_url = post.get("postUrl", "")
    status = post.get("status", "unsent")
    post_id = post.get("id", "")
    name = post.get("posterName", "Unknown")
    company = post.get("jobCompany", "")

    badge_html = (
        '<span class="badge badge-sent"><span class="badge-dot"></span>Sent</span>'
        if status == "sent"
        else '<span class="badge badge-pending"><span class="badge-dot"></span>Pending</span>'
    )

    if contact:
        if contact.startswith("http"):
            contact_content = f'<a href="{contact}" target="_blank">{contact}</a>'
        else:
            contact_content = contact
        contact_html = f'<div class="card-contact">Contact &nbsp;·&nbsp; {contact_content}</div>'
    else:
        contact_html = '<div class="card-contact" style="opacity:0.5;">No contact info available</div>'

    st.markdown(f"""
    <div class="post-card">
        <div class="card-top">
            <div>
                <div class="card-name">{name}</div>
                <div class="card-company">{company if company else "Company not specified"}</div>
                {contact_html}
            </div>
            <div>{badge_html}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    btn_col1, btn_col2, btn_col3, spacer = st.columns([1, 1, 1.2, 3])

    with btn_col1:
        if profile_url:
            st.link_button("View Profile", profile_url, use_container_width=True)
        else:
            st.button("View Profile", disabled=True, use_container_width=True, key=f"np_{post_id}")

    with btn_col2:
        if post_url:
            st.link_button("View Post", post_url, use_container_width=True)
        else:
            st.button("View Post", disabled=True, use_container_width=True, key=f"npo_{post_id}")

    with btn_col3:
        if status == "unsent":
            if st.button("Mark as Sent", key=f"sent_{post_id}", use_container_width=True, type="primary"):
                update_status(post_id, "sent")
                st.rerun()
        else:
            if st.button("Undo", key=f"unsent_{post_id}", use_container_width=True):
                update_status(post_id, "unsent")
                st.rerun()

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)


def main():
    data = load_data()
    total = len(data)
    sent = sum(1 for d in data if d.get("status") == "sent")
    unsent = total - sent

    render_header(total, sent, unsent)

    search = st.text_input(
        "search",
        label_visibility="collapsed",
        placeholder="Search by recruiter name or company...",
    )
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    grouped = get_grouped_data()

    if not grouped:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-title">No posts yet</div>
            <div class="empty-sub">Run <code>python scheduler.py</code> to fetch today's hiring posts.</div>
        </div>
        """, unsafe_allow_html=True)
        return

    any_results = False
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

        any_results = True
        render_date_header(date)

        for post in filtered:
            render_card(post)

    if search and not any_results:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-title">No results found</div>
            <div class="empty-sub">Try a different recruiter name or company.</div>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
