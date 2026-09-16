import streamlit as st

from src.helpdesk import HelpdeskAgent
from src.database import (
    init_db,
    create_ticket,
    get_all_tickets,
    update_ticket_status
)


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="AI IT Helpdesk Agent",
    page_icon="🤖",
    layout="wide"
)


# ==================================================
# INITIALIZE DATABASE
# ==================================================

init_db()


# ==================================================
# LOAD AI AGENT
# ==================================================

@st.cache_resource
def load_agent():
    return HelpdeskAgent("data/faqs.csv")


agent = load_agent()


# ==================================================
# HEADER
# ==================================================

st.title("🤖 AI IT Helpdesk Agent")

st.caption(
    "AI-powered IT ticket classification, priority prediction, "
    "FAQ retrieval and response drafting"
)


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.header("🤖 AI IT Helpdesk Agent")

    st.write(
        "AI-powered IT support system for ticket "
        "classification, priority prediction, "
        "knowledge retrieval, and response drafting."
    )

    st.divider()

    st.info(
        "AI-assisted system with human oversight "
        "for sensitive IT operations."
    )


# ==================================================
# TABS
# ==================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🎫 New Ticket",
        "📋 Ticket History",
        "📚 Knowledge Base",
        "ℹ️ About"
    ]
)


# ==================================================
# TAB 1 — NEW TICKET
# ==================================================

with tab1:

    st.subheader("Submit an IT Issue")

    ticket = st.text_area(
        "Describe the problem",
        height=160,
        placeholder=(
            "Example: I cannot connect my laptop to the "
            "office Wi-Fi and I have a meeting in 20 minutes."
        ),
        key="ticket_description"
    )

    employee = st.text_input(
        "Employee / Requester",
        placeholder="e.g. Employee-001",
        key="employee_requester"
    )

    if st.button(
        "Analyze & Create Ticket",
        type="primary",
        use_container_width=True,
        key="analyze_ticket"
    ):

        if not ticket.strip():

            st.warning(
                "Please enter a ticket description."
            )

        else:

            # ------------------------------------------
            # AI ANALYSIS
            # ------------------------------------------

            result = agent.analyze(ticket)

            # ------------------------------------------
            # SAVE TICKET
            # ------------------------------------------

            ticket_id = create_ticket(
                employee=(
                    employee
                    if employee.strip()
                    else "Anonymous"
                ),
                description=ticket,
                category=result["category"],
                priority=result["priority"],
                confidence=result["confidence"],
                faq_title=result["faq"]["title"],
                faq_solution=result["faq"]["solution"],
                response=result["response"]
            )

            st.success(
                f"✅ Ticket created successfully! "
                f"Ticket ID: **{ticket_id}**"
            )

            # ------------------------------------------
            # METRICS
            # ------------------------------------------

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Category",
                result["category"]
            )

            c2.metric(
                "Priority",
                result["priority"]
            )

            c3.metric(
                "Confidence",
                f'{result["confidence"] * 100:.1f}%'
            )

            # ------------------------------------------
            # AI ANALYSIS
            # ------------------------------------------

            st.subheader("🧠 AI Analysis")

            st.write(
                result["reason"]
            )

            # ------------------------------------------
            # KNOWLEDGE ARTICLE
            # ------------------------------------------

            st.subheader(
                "📚 Recommended Knowledge Article"
            )

            faq = result["faq"]

            st.info(
                f"**{faq['title']}**\n\n"
                f"{faq['solution']}\n\n"
                f"**Source:** {faq['source']}"
            )

            # ------------------------------------------
            # DRAFT RESPONSE
            # ------------------------------------------

            st.subheader(
                "💬 Draft Support Response"
            )

            st.text_area(
                "Copy this response to the requester",
                result["response"],
                height=220,
                key="draft_support_response"
            )

            # ------------------------------------------
            # TECHNICAL DETAILS
            # ------------------------------------------

            with st.expander(
                "🔧 Technical Details"
            ):

                st.json(
                    {
                        "ticket_id": ticket_id,
                        "category_scores": result[
                            "category_scores"
                        ],
                        "priority_factors": result[
                            "priority_factors"
                        ],
                        "matched_faq_score": result[
                            "faq_score"
                        ]
                    }
                )


# ==================================================
# TAB 2 — TICKET HISTORY
# ==================================================

with tab2:

    st.subheader("📋 Ticket History")

    tickets = get_all_tickets()

    if not tickets:

        st.info(
            "No tickets have been created yet."
        )

    else:

        st.write(
            f"Total tickets: **{len(tickets)}**"
        )

        for ticket_data in tickets:

            (
                ticket_id,
                employee,
                description,
                category,
                priority,
                confidence,
                status,
                created_at
            ) = ticket_data

            with st.expander(
                f"{ticket_id} | {category} | "
                f"{priority} | {status}"
            ):

                c1, c2, c3 = st.columns(3)

                c1.write(
                    f"**Employee:** {employee}"
                )

                c2.write(
                    f"**Category:** {category}"
                )

                c3.write(
                    f"**Priority:** {priority}"
                )

                st.write(
                    f"**Created:** {created_at}"
                )

                st.write(
                    f"**Confidence:** "
                    f"{confidence * 100:.1f}%"
                )

                st.write(
                    f"**Description:** {description}"
                )

                st.divider()

                status_options = [
                    "Open",
                    "In Progress",
                    "Resolved",
                    "Closed"
                ]

                new_status = st.selectbox(
                    "Update Status",
                    status_options,
                    index=status_options.index(status),
                    key=f"status_select_{ticket_id}"
                )

                if st.button(
                    "Update Status",
                    key=f"update_status_{ticket_id}"
                ):

                    update_ticket_status(
                        ticket_id,
                        new_status
                    )

                    st.success(
                        f"{ticket_id} updated to "
                        f"{new_status}"
                    )

                    st.rerun()


# ==================================================
# TAB 3 — KNOWLEDGE BASE
# ==================================================

with tab3:

    st.subheader("📚 Knowledge Base")

    st.write(
        f"{len(agent.faqs)} support articles "
        "are available for retrieval."
    )

    for _, faq in agent.faqs.iterrows():

        faq_id = faq.get(
            "id",
            ""
        )

        title = faq.get(
            "title",
            "Untitled FAQ"
        )

        category = faq.get(
            "category",
            "General"
        )

        solution = faq.get(
            "solution",
            ""
        )

        source = faq.get(
            "source",
            "Internal IT Knowledge Base"
        )

        with st.expander(
            f"{faq_id} — {title}"
        ):

            st.write(
                f"**Category:** {category}"
            )

            st.write(
                solution
            )

            st.caption(
                f"Source: {source}"
            )


# ==================================================
# TAB 4 — ABOUT
# ==================================================

with tab4:

    st.subheader("About the Project")

    st.markdown("""
    ### AI IT Helpdesk Agent

    The **AI IT Helpdesk Agent** is an AI/ML-powered application
    that assists IT support teams in handling technical support
    requests efficiently.

    ### What the System Does

    The system analyzes an IT issue and automatically:

    - **Classifies** the ticket into an appropriate support category.
    - **Predicts** the ticket priority based on urgency and impact.
    - **Retrieves** the most relevant knowledge-base article.
    - **Generates** a draft response for the support team.
    - **Stores** tickets with a unique ID for future tracking.
    - **Manages** ticket history and status.

    ### AI/ML Techniques

    - **Natural Language Processing (NLP)** for understanding ticket descriptions
    - **TF-IDF** for text feature extraction
    - **Logistic Regression** for ticket classification
    - **Cosine Similarity** for knowledge-base retrieval
    - **Rule-based analysis** for priority prediction

    ### Technology Stack

    **Python · Scikit-learn · Pandas · NumPy · SQLite · Streamlit**

    ### System Workflow

    **IT Issue → Text Processing → Category Prediction → Priority Prediction → Knowledge Retrieval → Response Drafting → Ticket Storage**

    ### Human-in-the-Loop

    The system provides AI-based recommendations and response drafts.
    Sensitive actions such as account changes, access permissions,
    password resets, and device administration remain under human control.

    ### Project Objective

    The objective of this project is to demonstrate how **AI, NLP,
    and Machine Learning** can be applied to automate and improve
    common IT helpdesk operations.
    """)