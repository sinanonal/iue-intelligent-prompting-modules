
import os, time, yaml
import streamlit as st
from openai import OpenAI, RateLimitError

# ----------------------- Settings -----------------------
st.set_page_config(page_title="SIUE Intelligent Prompting — Course Modules", page_icon="🧠", layout="wide")

# SIUE simple brand
st.markdown(
    """
    <style>
    .stApp { background:#ffffff; }
    h1, h2, h3, h4 { color:#d6001c; }
    .siue-banner { display:flex; align-items:center; gap:12px; padding-bottom:6px; border-bottom:2px solid #d6001c; }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown("<div class='siue-banner'><strong>SIUE Intelligent Prompting — Weekly Modules</strong></div>", unsafe_allow_html=True)

# ----------------------- Helpers -----------------------
@st.cache_data(show_spinner=False)
def load_syllabus(path:str='syllabus.yaml'):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def get_client():
    # OPENAI_API_KEY must be set in Streamlit Secrets
    return OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Backoff chat
def chat(messages, model=None, **kwargs):
    client = get_client()
    mdl = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    kwargs.setdefault("max_tokens", 400)
    kwargs.setdefault("temperature", 0.6)
    for attempt in range(5):
        try:
            resp = client.chat.completions.create(model=mdl, messages=messages, **kwargs)
            return resp.choices[0].message.content
        except RateLimitError:
            wait = 2 ** attempt
            if attempt < 4:
                time.sleep(wait)
            else:
                st.error("Rate limit exceeded. Please wait a minute and try again.")
                return ""
        except Exception as e:
            st.error(f"LLM error: {e}")
            return ""

@st.cache_data(show_spinner=False, ttl=300)
def cached_chat(messages, model=None, **kwargs):
    return chat(messages, model=model, **kwargs)

# ----------------------- UI Controls -----------------------
with st.sidebar:
    st.header("Navigation")
    data = load_syllabus()
    # Build hierarchical options preserving exact names
    options = []
    mapping = {}
    for tier in data.get('tiers', []):
        tier_name = tier['tier']
        for w in tier['weeks']:
            label = f"{w['week']} — {w['title']}"
            options.append(label)
            mapping[label] = {**w, 'tier': tier_name}

    selected = st.selectbox("Choose module", options)
    st.divider()
    st.caption("Use Settings to control model behavior.")
    temp = st.slider("Creativity (temperature)", 0.0, 1.5, 0.6, 0.1)
    max_toks = st.slider("Max tokens", 100, 1200, 400, 50)
    model = st.text_input("Model", os.getenv("OPENAI_MODEL", "gpt-4o-mini"))

# ----------------------- Render Page -----------------------
week = mapping[selected]

st.subheader(week['week'])
st.markdown(f"**Title:** {week['title']}")
st.markdown(f"**Module:** {week['module']}")

with st.expander("Learning Outcomes", expanded=True):
    st.markdown("\n".join([f"- {lo}" for lo in week.get('learning_outcomes', [])]))

with st.expander("Activity Types", expanded=False):
    st.markdown("\n".join([f"- {a}" for a in week.get('activity_types', [])]))

with st.expander("Grounding / Context", expanded=False):
    default_ctx = week.get('grounding', '') or ''
    ctx = st.text_area("Optional context to ground answers", value=default_ctx, height=140)
    must_use_ctx = st.checkbox("Force model to use only the provided context (say 'Not enough information' if missing)", value=False)

st.markdown("---")
st.markdown("### In-Class Demos")

for i, demo in enumerate(week.get('in_class_demo', []), start=1):
    st.markdown(f"**Demo {i}:**")
    prompt = st.text_area(f"Prompt {i}", value=demo, height=120, key=f"demo_{week['id']}_{i}")
    if st.button(f"Run Demo {i}", key=f"btn_{week['id']}_{i}"):
        sys = "You are a clear, precise assistant for classroom demonstrations."
        if must_use_ctx and ctx.strip():
            user = f"Context:\n{ctx}\n\nInstruction: Use only the provided context. If the answer is not in context, say 'Not enough information.'\n\nTask: {prompt}"
        elif must_use_ctx and not ctx.strip():
            user = f"Instruction: If the answer is not in context, say 'Not enough information.'\n\nTask: {prompt}"
        else:
            user = prompt
        out = cached_chat([
            {"role":"system","content":sys},
            {"role":"user","content":user}
        ], model=model, temperature=temp, max_tokens=max_toks)
        st.markdown("**Output:**")
        st.write(out)
        st.divider()

st.markdown("---")
with st.expander("Assessment / Deliverable", expanded=True):
    st.write(week.get('assessment', ''))

# Export last demo outputs (simple template)
with st.sidebar:
    st.markdown("---")
    st.caption("Tip: copy answers for Blackboard submission.")
