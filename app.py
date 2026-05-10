import streamlit as st
import html
from storage import load_data, update_status, get_grouped_data

# Page config
st.set_page_config(
    page_title="RecruitRadar",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Read the font
st.markdown('<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">', unsafe_allow_html=True)

# Custom CSS for Dark-Mode Glassmorphism
st.markdown("""
<style>
    * {
        font-family: 'Outfit', sans-serif;
    }

    /* Target the main app container */
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
    }

    .block-container {
        max-width: 900px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }

    /* ── Header ── */
    .page-header {
        margin-bottom: 3rem;
        text-align: center;
    }

    .page-header h1 {
        font-size: 2.75rem;
        font-weight: 800;
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }

    .page-header p {
        font-size: 1.05rem;
        color: #94a3b8;
        font-weight: 300;
    }

    /* ── Stats ── */
    .stat-row {
        display: flex;
        gap: 1.25rem;
        margin-bottom: 3rem;
    }

    .stat-card {
        flex: 1;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
    }
    .stat-card:hover {
        transform: translateY(-2px);
        border-color: rgba(255, 255, 255, 0.1);
    }

    .stat-label {
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #94a3b8;
        margin-bottom: 0.5rem;
    }

    .stat-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #f8fafc;
        line-height: 1;
    }

    .stat-value.green {
        background: linear-gradient(135deg, #4ade80, #22c55e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .stat-value.amber {
        background: linear-gradient(135deg, #fbbf24, #f59e0b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* ── Search ── */
    .stTextInput input {
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding: 0.8rem 1.2rem !important;
        font-size: 1rem !important;
        background: rgba(255, 255, 255, 0.03) !important;
        color: #f8fafc !important;
        transition: all 0.2s !important;
        box-shadow: none !important;
    }
    .stTextInput input:focus {
        border-color: #38bdf8 !important;
        background: rgba(255, 255, 255, 0.05) !important;
        box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2) !important;
    }

    /* ── Date Section ── */
    .date-section {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin: 2.5rem 0 1.5rem 0;
    }

    .date-label {
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #94a3b8;
        white-space: nowrap;
    }

    .date-line {
        flex: 1;
        height: 1px;
        background: linear-gradient(to right, rgba(255,255,255,0.1), transparent);
    }

    /* ── Post Card container override ── */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        margin-bottom: 1rem !important;
        backdrop-filter: blur(10px) !important;
        transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s !important;
    }
    
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-2px);
        border-color: rgba(56, 189, 248, 0.3) !important;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2) !important;
    }

    .card-top {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 1rem;
    }

    .card-info {
        flex: 1;
    }

    .card-name {
        font-size: 1.1rem;
        font-weight: 600;
        color: #f1f5f9;
        margin-bottom: 0.2rem;
    }

    .card-company {
        font-size: 0.9rem;
        color: #94a3b8;
        font-weight: 400;
    }

    .card-contact {
        font-size: 0.85rem;
        color: #64748b;
        margin-top: 0.5rem;
    }

    .card-contact a {
        color: #38bdf8;
        text-decoration: none;
        transition: color 0.15s;
    }

    .card-contact a:hover {
        color: #7dd3fc;
    }

    /* ── Badge ── */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        white-space: nowrap;
    }

    .badge-sent {
        background: rgba(34, 197, 94, 0.1) !important;
        color: #4ade80 !important;
        border: 1px solid rgba(34, 197, 94, 0.2) !important;
    }

    .badge-pending {
        background: rgba(245, 158, 11, 0.1) !important;
        color: #fbbf24 !important;
        border: 1px solid rgba(245, 158, 11, 0.2) !important;
    }

    .badge-dot {
        display: inline-block;
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: currentColor;
    }

    /* ── Streamlit Buttons Override ── */
    .stButton > button, .stLinkButton > a {
        border-radius: 10px !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: all 0.2s !important;
        height: 40px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 0 1rem !important;
        width: 100% !important;
    }

    /* Primary Button (Mark as Sent) */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #38bdf8, #3b82f6) !important;
        border: none !important;
        color: white !important;
    }
    .stButton > button[kind="primary"]:hover {
        opacity: 0.9 !important;
        transform: scale(1.02);
    }

    /* Secondary Button (Undo) */
    .stButton > button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #f1f5f9 !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
    }

    /* Link Buttons */
    .stLinkButton > a {
        background: transparent !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #94a3b8 !important;
        text-decoration: none !important;
    }
    .stLinkButton > a:hover {
        border-color: rgba(255, 255, 255, 0.2) !important;
        color: #f1f5f9 !important;
    }

    /* Disable button styling */
    .stButton > button:disabled, .stLinkButton > a[disabled] {
        opacity: 0.4 !important;
        cursor: not-allowed !important;
        transform: none !important;
    }

    div[data-testid="column"] {
        gap: 0.5rem;
    }
    
    /* ── Empty State ── */
    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        margin-top: 2rem;
    }

    .empty-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #f1f5f9;
        margin-bottom: 0.5rem;
    }

    .empty-sub {
        font-size: 0.9rem;
        color: #64748b;
    }
</style>
""", unsafe_allow_html=True)


def fix_url(url):
    """Ensures the URL has a proper scheme for standard web links so Streamlit doesn't navigate locally."""
    if not url:
        return ""
    if not str(url).startswith("http://") and not str(url).startswith("https://"):
        return "https://" + str(url)
    return str(url)


def render_header(total, sent, unsent):
    st.markdown("""
<div class="page-header">
<h1>RecruitRadar</h1>
<p>AI-powered recruiter finder — verified hiring signals</p>
</div>
""", unsafe_allow_html=True)
    
    st.markdown(f"""
<div class="stat-row">
<div class="stat-card">
<div class="stat-label">Total Leads</div>
<div class="stat-value">{{total}}</div>
</div>
<div class="stat-card">
<div class="stat-label">Requests Sent</div>
<div class="stat-value green">{{sent}}</div>
</div>
<div class="stat-card">
<div class="stat-label">Action Needed</div>
<div class="stat-value amber">{{unsent}}</div>
</div>
</div>
""".format(total=total, sent=sent, unsent=unsent), unsafe_allow_html=True)


def render_card(post):
    contact = str(post.get("contactInfo", ""))
    profile_url = fix_url(post.get("profileUrl", ""))
    post_url = fix_url(post.get("postUrl", ""))
    status = post.get("status", "unsent")
    post_id = str(post.get("id", ""))
    
    # Safely escape HTML to prevent <div> bleeding or empty field errors
    name = html.escape(str(post.get('posterName', 'Unknown')))
    company = html.escape(str(post.get('jobCompany', 'Not specified')))

    if contact and contact.lower() != "nan":
        clean_contact = html.escape(contact)
        if contact.startswith("http"):
            domain = clean_contact.replace("https://", "").replace("http://", "").replace("www.", "")
            contact_html = f'Contact: <a href="{fix_url(contact)}" target="_blank">{domain}</a>'
        elif "@" in contact:
            contact_html = f'Contact: <a href="mailto:{clean_contact}">{clean_contact}</a>'
        else:
            contact_html = f'Contact: {clean_contact}'
    else:
        contact_html = '<span style="opacity: 0.5;">No contact info available</span>'

    if status == "sent":
        badge_html = '<span class="badge badge-sent"><span class="badge-dot"></span>Sent</span>'
    else:
        badge_html = '<span class="badge badge-pending"><span class="badge-dot"></span>Pending</span>'

    with st.container(border=True):
        st.markdown(f"""
<div class="card-top">
<div class="card-info">
<div class="card-name">{name}</div>
<div class="card-company">{company}</div>
<div class="card-contact">{contact_html}</div>
</div>
<div>
{badge_html}
</div>
</div>
""", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1.2])
        
        # We must ensure that the key is 100% unique
        safe_key = f"btn_{post_id}_{name.replace(' ', '_')}"
        
        with col1:
            if profile_url:
                st.link_button("View Profile", profile_url, use_container_width=True)
            else:
                st.button("View Profile", disabled=True, use_container_width=True, key=f"np_{safe_key}")
        
        with col2:
            if post_url:
                st.link_button("View Post", post_url, use_container_width=True)
            else:
                st.button("View Post", disabled=True, use_container_width=True, key=f"npo_{safe_key}")
        
        with col3:
            if status == "unsent":
                if st.button("Mark as Sent", key=f"sent_{safe_key}", use_container_width=True, type="primary"):
                    update_status(post_id, "sent")
                    st.rerun()
            else:
                if st.button("Undo Action", key=f"unsent_{safe_key}", use_container_width=True, type="secondary"):
                    update_status(post_id, "unsent")
                    st.rerun()


def main():
    data = load_data()
    total = len(data)
    sent = sum(1 for d in data if d.get("status") == "sent")
    unsent = total - sent

    render_header(total, sent, unsent)

    search = st.text_input("Search", label_visibility="collapsed", placeholder="Search by recruiter name or company...")

    grouped = get_grouped_data()

    if not grouped:
        st.markdown("""
<div class="empty-state">
<div class="empty-title">No leads found yet</div>
<div class="empty-sub">Run your scheduler to fetch the latest hiring posts.</div>
</div>
""", unsafe_allow_html=True)
        return

    # Filter and display posts
    for date, posts in grouped.items():
        filtered = posts
        if search:
            search_lower = search.lower()
            filtered = [
                p for p in posts
                if search_lower in str(p.get("posterName", "")).lower()
                or search_lower in str(p.get("jobCompany", "")).lower()
            ]

        if not filtered:
            continue
            
        st.markdown(f"""
<div class="date-section">
<span class="date-label">{html.escape(str(date))}</span>
<div class="date-line"></div>
</div>
""", unsafe_allow_html=True)

        for post in filtered:
            render_card(post)


if __name__ == "__main__":
    main()