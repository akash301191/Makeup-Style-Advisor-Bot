import tempfile
import streamlit as st

from agno.agent import Agent
from agno.media import Image
from agno.models.openai import OpenAIChat
from agno.tools.serpapi import SerpApiTools

from textwrap import dedent

def render_sidebar():
    st.sidebar.title("🔐 API Configuration")
    st.sidebar.markdown("---")

    # OpenAI API Key input
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://platform.openai.com/account/api-keys)."
    )
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key
        st.sidebar.success("✅ OpenAI API key updated!")

    # SerpAPI Key input
    serp_api_key = st.sidebar.text_input(
        "Serp API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://serpapi.com/manage-api-key)."
    )
    if serp_api_key:
        st.session_state.serp_api_key = serp_api_key
        st.sidebar.success("✅ Serp API key updated!")

    st.sidebar.markdown("---")

def render_makeup_preferences():
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    # Column 1: Image Upload
    with col1:
        st.subheader("📷 Upload Your Face Image")
        uploaded_image = st.file_uploader(
            "Upload a clear, front-facing image of your face in natural lighting, **without makeup** for best results.",
            type=["jpg", "jpeg", "png"]
        )

    # Column 2: Style & Occasion
    with col2:
        st.subheader("🎯 Style & Occasion")

        preferred_style = st.selectbox(
            "What kind of makeup style do you prefer?",
            [
                "Natural / Everyday", "Soft Glam", "Bold / Dramatic",
                "Editorial / Creative", "K-Beauty Inspired", "Classic Professional"
            ]
        )

        occasion = st.selectbox(
            "What's the occasion or context?",
            [
                "Everyday", "Work / Office", "Date Night",
                "Wedding / Formal", "Party / Night Out"
            ]
        )

    # Column 3: Feature & Budget Preferences
    with col3:
        st.subheader("✨ Feature & Budget Preferences")

        highlight_feature = st.selectbox(
            "Which feature would you like to highlight?",
            ["Eyes", "Lips", "Balanced / Both"]
        )

        product_range = st.selectbox(
            "What's your preferred product range?",
            ["Budget", "Mid-range", "Luxury"]
        )

    return {
        "uploaded_image": uploaded_image,
        "preferred_style": preferred_style,
        "occasion": occasion,
        "highlight_feature": highlight_feature,
        "product_range": product_range
    }

def generate_makeup_report(user_makeup_preferences):
    # Unpack user input
    uploaded_image = user_makeup_preferences["uploaded_image"]
    preferred_style = user_makeup_preferences["preferred_style"]
    occasion = user_makeup_preferences["occasion"]
    highlight_feature = user_makeup_preferences["highlight_feature"]
    product_range = user_makeup_preferences["product_range"]

    # Save uploaded image temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(uploaded_image.getvalue())
        image_path = tmp.name

    # Step 1: Facial Feature Analysis (natural face, no makeup)
    facial_feature_analyzer = Agent(
        model=OpenAIChat(id="gpt-4o", api_key=st.session_state.openai_api_key),
        name="Facial Feature Analyzer",
        role="Analyzes a neutral, makeup-free face image to extract general facial characteristics (e.g., face shape, lip fullness, eye shape), without identifying or recognizing the person.",
        description=dedent("""
            You are a beauty assistant. Given a generic, makeup-free face image, analyze visible geometry and proportions to determine abstract characteristics like skin tone, facial shape, eye shape, and lip structure.

            Avoid making any personal or identifying claims.
        """),
        instructions=[
            "Evaluate the uploaded face image anonymously.",
            "Extract non-identifying visual features like face shape, skin tone range, eye structure, and lip geometry.",
            "Describe facial proportions and symmetry in generic terms only.",
            "Do not attempt to identify, guess, or comment on who the person is.",
        ],
        markdown=True,
    )

    # Run the facial analysis
    visual_insights = facial_feature_analyzer.run(
        "Extract general facial structure and proportions from this image.",
        images=[Image(filepath=image_path)] 
    ).content 

    # Step 2: Makeup Research Agent
    makeup_search_agent = Agent(
        name="Makeup Research Assistant",
        role="Finds personalized makeup tutorials, product lists, and technique resources based on facial features and user preferences.",
        model=OpenAIChat(id="gpt-4o", api_key=st.session_state.openai_api_key),
        description="Generates targeted Google search queries and uses SerpAPI to find makeup tutorials, product suggestions, and technique guides tailored to the user's visual traits and style preferences.",
        instructions=[
            "Use the user's visual insights (face shape, skin tone, eye/lip structure).",
            "Incorporate user preferences: makeup style, occasion, focus area, and product budget.",
            "Generate a focused Google search prompt (e.g., 'luxury soft glam wedding makeup for oval face with eye focus').",
            "Use SerpAPI to fetch 8-10 relevant resources (makeup tutorials, product recommendations, focus area specific guides)",
            "Return all links in Markdown format with short, descriptive titles.",
        ],
        tools=[SerpApiTools(api_key=st.session_state.serp_api_key)],
        markdown=True,
        tool_call_limit=3
    )

    # Construct the updated search prompt
    search_prompt = f"""
    Visual Insights:
    {visual_insights}

    Makeup Preferences:
    - Style: {preferred_style}
    - Occasion: {occasion}
    - Focus Area: {highlight_feature}
    - Product Range: {product_range}

    Based on these inputs, generate a relevant Google search and return 8-10 high-quality links that include makeup tutorials, product suggestions, and face-shape-specific application guides. Format all links in Markdown with clear titles.
    """

    # Execute the agent
    research_links = makeup_search_agent.run(search_prompt).content  

    # Step 3: Report Generator Agent
    makeup_report_generator = Agent(
        name="Makeup Report Generator",
        model=OpenAIChat(id="o3-mini", api_key=st.session_state.openai_api_key),
        role="Generates a structured, descriptive makeup recommendation report using visual analysis and curated research links.",
        description=dedent("""
            You are a beauty assistant report generator. You are given:
            1. A visual analysis of the user’s facial features from a makeup-free image.
            2. A list of curated makeup tutorials, product suggestions, and application guides based on the user's appearance and style preferences.

            Your task is to write a rich, well-structured Markdown report with makeup recommendations tailored to the user's natural features and goals.
        """),
        instructions=[
            "Start the report with: ## 💄 Makeup Recommendation Report",
            "",
            "### 👤 Facial Feature Overview",
            "- Summarize the user’s face shape, skin tone, eye shape, and lip structure.",
            "- Explain how these features affect makeup choices.",
            "- Embed hyperlinks where useful (e.g., [eye shape tips](https://...), [lip contouring for full lips](https://...)).",
            "",
            "### 🎯 Focus Area Strategy",
            "- Explain how to emphasize the user's selected focus area (eyes, lips, or both).",
            "- Suggest techniques such as gradient shading, tightlining, contouring, etc.",
            "- Add links to relevant tutorials or visual guides.",
            "",
            "### 💡 Style & Occasion-Based Looks",
            "- Provide 2–3 look recommendations aligned with the user’s preferred makeup style and occasion.",
            "- Include explanations and links to tutorials (e.g., [soft glam wedding look](https://...), [bold evening eyes](https://...)).",
            "",
            "### 🛍️ Product Recommendations",
            "- Recommend makeup products (foundation, eye products, lipsticks) matching the user’s skin tone and budget range.",
            "- Embed links to product guides or brand collections (e.g., [luxury bridal foundations](https://...), [smudge-proof eyeliners](https://...)).",
            "",
            "### 💬 Application Techniques by Face Shape",
            "- Include contouring, blush, and highlight placements specific to their face shape.",
            "- Suggest eye/lip techniques that suit their structure.",
            "- Add guide links (e.g., [oval face contouring](https://...), [round eye liner tricks](https://...)).",
            "",
            "### 🔗 Curated Makeup Inspirations",
            "- List the curated inspiration links from the research agent.",
            "- Use clear, titled Markdown hyperlinks (e.g., [Soft Glam Bridal Tutorial](https://...)).",
            "- Group similar links where appropriate.",
            "",
            "**Important:** Embed helpful, relevant hyperlinks throughout—not just in the final section. Aim for 1–2 links per section.",
            "",
            "Use a confident, friendly, professional tone.",
            "Format the output in clean Markdown with headings, bullet points, and short, clear paragraphs.",
            "Output only the final Markdown report—no extra commentary or reasoning."
        ],
        markdown=True,
        add_datetime_to_instructions=True
    )

    # Construct the report generation prompt
    final_prompt = f"""
    Visual Insights from Uploaded Photo:
    {visual_insights}

    Web-Sourced Makeup Inspirations: 
    {research_links}

    Generate a markdown-formatted makeup recommendation report.
    """

    # Execute the agent
    final_report = makeup_report_generator.run(final_prompt).content

    return final_report
  
def main() -> None:
    # Page config
    st.set_page_config(page_title="Makeup Style Advisor Bot", page_icon="💄", layout="wide")

    # Custom styling
    st.markdown(
        """
        <style>
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        div[data-testid="stTextInput"] {
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Header and intro
    st.markdown("<h1 style='font-size: 2.5rem;'>💄 Makeup Style Advisor Bot</h1>", unsafe_allow_html=True)
    st.markdown(
        "Welcome to Makeup Style Advisor Bot — a smart beauty assistant that analyzes your facial features and preferences to suggest personalized makeup lookbooks and styling cues tailored to your profile.",
        unsafe_allow_html=True
    )

    render_sidebar()
    user_makeup_preferences = render_makeup_preferences()

    st.markdown("---")

    # Call the report generation method when the user clicks the button
    if st.button("💄 Generate Makeup Report"):
        if not hasattr(st.session_state, "openai_api_key"):
            st.error("Please provide your OpenAI API key in the sidebar.")
        elif not hasattr(st.session_state, "serp_api_key"):
            st.error("Please provide your SerpAPI key in the sidebar.")
        elif "uploaded_image" not in user_makeup_preferences or not user_makeup_preferences["uploaded_image"]:
            st.error("Please upload a makeup-free facial photo before generating the report.")
        else:
            with st.spinner("Analyzing your features and preparing a personalized makeup guide..."):
                report = generate_makeup_report(user_makeup_preferences)

                st.session_state.makeup_report = report
                st.session_state.makeup_image = user_makeup_preferences["uploaded_image"]

    # Display and download section
    if "makeup_report" in st.session_state:
        st.markdown("## 📸 Uploaded Natural Face Image")
        st.image(st.session_state.makeup_image, use_container_width=False)

        st.markdown(st.session_state.makeup_report, unsafe_allow_html=True)

        st.download_button(
            label="📥 Download Makeup Report",
            data=st.session_state.makeup_report,
            file_name="makeup_recommendation_report.md",
            mime="text/markdown"
        )

if __name__ == "__main__":
    main()
