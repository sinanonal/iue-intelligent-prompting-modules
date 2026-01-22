import streamlit as st
from auth import require_access, render_top_bar

require_access()
render_top_bar("Module 1 – Foundations")


# -----------------------------------------
#   TIER 1 — Foundations of Generative AI
#   MODULE 1 — Foundations of Generative AI
# -----------------------------------------

st.set_page_config(page_title="Module 1 — Foundations of Generative AI", layout="wide")

# ------------------ UTILITIES ------------------
def safe_strip(key: str) -> str:
    return str(st.session_state.get(key, "")).strip()

def word_count(text: str) -> int:
    return len([w for w in text.split() if w.strip()])

def build_csv_bytes():
    """Create a CSV of the student's Module 1 responses and return as bytes (Excel-friendly)."""
    name = safe_strip("student_name")
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Video quiz
    q1 = safe_strip("q1_intro")
    q2 = safe_strip("q2_slide")

    # Prompt Lab
    m1_prompt_used = safe_strip("m1_prompt_used")
    m1_ai_response = safe_strip("m1_ai_response")
    m1_prompt_reflection = safe_strip("m1_prompt_reflection")

    # Module reflection
    reflection = safe_strip("reflection_m1")

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Name", "Timestamp",
        "Q1: Intro", "Q2: Slide Observation",
        "Prompt Lab: Prompt Used", "Prompt Lab: AI Response", "Prompt Lab: Reflection",
        "Module Reflection"
    ])
    writer.writerow([
        name, ts,
        q1, q2,
        m1_prompt_used, m1_ai_response, m1_prompt_reflection,
        reflection
    ])
    return output.getvalue().encode("utf-8-sig")

def section_download_block():
    """Show a downloadable CSV if we have at least a name or any answers."""
    name = safe_strip("student_name")
    has_any = any([
        name,
        safe_strip("q1_intro"),
        safe_strip("q2_slide"),
        safe_strip("m1_prompt_used"),
        safe_strip("m1_ai_response"),
        safe_strip("m1_prompt_reflection"),
        safe_strip("reflection_m1"),
    ])

    if has_any:
        csv_bytes = build_csv_bytes()
        file_label = f"Module1_Responses_{name.replace(' ', '_') or 'Student'}.csv"
        st.download_button(
            label="⬇️ Download My Module 1 Responses (CSV)",
            data=csv_bytes,
            file_name=file_label,
            mime="text/csv",
            help="Downloads your name and answers as a CSV file you can submit or keep."
        )
    else:
        st.info("Fill in your name and at least one answer to enable the download button.")

def goto_module_2_button():
    st.markdown("---")
    if st.button("➡️ Go to Module 2"):
        try:
            st.switch_page("pages/Module 2.py")
        except Exception:
            st.info("Module 2 will be available soon. (To enable navigation, create `pages/Module 2.py`.)")

def render_mcq_block(section_id: str, questions: list[dict]):
    """
    Render 3 MCQs for a section.
    questions: list of dicts with keys: q, options, answer (exact match to one option)
    """
    st.markdown("### 🧠 Check Your Understanding (3 Questions)")
    selected = []
    for i, item in enumerate(questions, start=1):
        key = f"m1_{section_id}_mcq_{i}"
        choice = st.radio(
            f"{i}) {item['q']}",
            item["options"],
            index=None,
            key=key
        )
        selected.append(choice)

    if st.button("Check Answers", key=f"m1_{section_id}_mcq_check"):
        correct = 0
        for i, item in enumerate(questions):
            if selected[i] == item["answer"]:
                correct += 1
        if correct == len(questions):
            st.success("✅ Excellent! You answered all questions correctly.")
        else:
            st.warning(f"You answered {correct}/{len(questions)} correctly. Review the reading and try again.")

def render_reading_section(title: str, body: str, section_id: str, questions: list[dict]):
    st.subheader(title)
    st.markdown(body)
    render_mcq_block(section_id, questions)
    st.markdown("---")

# ------------------ HEADER ------------------
st.title("📘 Tier 1 — Foundations of Generative AI")
st.header("Module 1 — Foundations of Generative AI")
st.markdown("""
This module introduces the core ideas behind generative AI and large language models (LLMs).
Use the menu on the left to explore each subject in this module.
""")

# ------------------ SIDEBAR ------------------
st.sidebar.title("Module 1 Navigation")

st.sidebar.markdown("**Student Info**")
st.sidebar.text_input("Your full name (for downloads):", key="student_name")
st.sidebar.markdown("---")

# ------------------ READING CONTENT ------------------
READINGS = {
    "1. Introduction: Entering the Era of Intelligent Assistance": {
        "id": "s1_intro",
        "text": """
### Reading
Over the past few years, artificial intelligence has shifted from a specialized research domain to a practical tool used across industries, classrooms, and everyday life. Students now encounter AI not in abstract discussions about the future, but in concrete forms such as writing assistants, recommendation engines, chatbots, and automated tutoring systems. Among these tools, generative AI has had the greatest impact. These systems do not simply categorize information; they produce new content, generate explanations, and help learners explore unfamiliar subjects with remarkable fluency. As a result, the ability to understand and communicate with these systems—through clear, strategic prompting—has emerged as an essential academic and professional skill.

This chapter provides the foundational knowledge you need before learning specific prompting techniques in later modules. It explains what generative AI is, how large language models work, what they can and cannot do, and why your instructions matter so much. Although AI often appears intelligent, its behavior is driven by patterns rather than genuine understanding. Recognizing this distinction will help you use AI responsibly and effectively.

Because this course is interdisciplinary, the examples in this chapter draw from fields such as engineering, business, the arts, psychology, and health sciences. Regardless of your major, the concepts you encounter here will provide a base from which you can build advanced prompting skills in the weeks ahead.
""",
        "mcq": [
            {
                "q": "What is the main reason generative AI has had a strong impact compared to many other AI tools?",
                "options": [
                    "It can access private databases and real-time systems by default",
                    "It produces new content and explanations, not just categories or labels",
                    "It replaces the need for learning in academic settings",
                    "It guarantees accurate and unbiased information"
                ],
                "answer": "It produces new content and explanations, not just categories or labels"
            },
            {
                "q": "According to the reading, what skill is becoming essential for academic and professional work?",
                "options": [
                    "Writing code for AI models from scratch",
                    "Clear, strategic prompting to communicate with AI systems",
                    "Memorizing AI definitions and terminology",
                    "Avoiding AI tools in all coursework"
                ],
                "answer": "Clear, strategic prompting to communicate with AI systems"
            },
            {
                "q": "Why does the chapter emphasize that AI behavior is driven by patterns rather than genuine understanding?",
                "options": [
                    "To show that AI is always wrong",
                    "To help students use AI responsibly and interpret output correctly",
                    "To discourage interdisciplinary use of AI",
                    "To argue that AI cannot produce fluent language"
                ],
                "answer": "To help students use AI responsibly and interpret output correctly"
            }
        ]
    },

    "2. What is Generative AI?": {
        "id": "s2_genai",
        "text": """
### Reading
Generative artificial intelligence refers to algorithms that can create new content. Traditional AI systems typically classify, sort, or make decisions based on predefined rules or learned patterns. For example, a classical machine learning model might determine whether an email is spam or predict the likelihood that a customer will make a purchase. Generative AI goes beyond classification. It produces original text, visuals, or other forms of output by learning the structure and patterns of human-generated content.

Modern generative AI systems, especially large language models (LLMs), have been trained on vast collections of text taken from books, articles, websites, academic papers, and human conversations. Through this exposure, the model learns not only the rules of grammar but also the structures of arguments, the flow of explanations, the tone appropriate to different audiences, and the connections between ideas across disciplines.

At first glance, this ability to generate human-like content may give the impression of intelligence, creativity, and deep understanding. However, generative AI models do not think. They do not possess beliefs, values, consciousness, or emotional awareness. Instead, they operate on the statistical relationships between the words and concepts they encountered during training. Understanding this distinction is critical for interpreting their output accurately and using them appropriately in academic work.
""",
        "mcq": [
            {
                "q": "Which statement best describes the difference between traditional AI and generative AI?",
                "options": [
                    "Traditional AI creates new content, while generative AI only classifies",
                    "Traditional AI classifies/predicts, while generative AI creates new content",
                    "Generative AI always provides fact-checked answers",
                    "Traditional AI cannot learn from data"
                ],
                "answer": "Traditional AI classifies/predicts, while generative AI creates new content"
            },
            {
                "q": "Why can LLM output appear intelligent or creative?",
                "options": [
                    "Because the model has beliefs and emotions",
                    "Because the model plans the entire response in advance",
                    "Because the model has learned patterns from large amounts of human text",
                    "Because the model verifies statements against external sources"
                ],
                "answer": "Because the model has learned patterns from large amounts of human text"
            },
            {
                "q": "According to the reading, how should we understand what LLMs are doing when they generate text?",
                "options": [
                    "They reason like humans",
                    "They rely on statistical relationships learned during training",
                    "They use real-time internet access to confirm facts",
                    "They copy and paste training documents"
                ],
                "answer": "They rely on statistical relationships learned during training"
            }
        ]
    },

    "3. How Large Language Models Learn": {
        "id": "s3_learn",
        "text": """
### Reading
To appreciate what generative AI can and cannot do, it is helpful to understand the basics of how an LLM is trained. The process begins with massive datasets consisting of text from a wide range of sources. The model is exposed to this text repeatedly, learning which words tend to appear near one another and which sequences of words tend to follow particular patterns. Through this process, the model constructs an internal representation of language—an intricate map of how humans communicate.

The fundamental task of the model is to predict the next token in a sequence. A token is typically a piece of a word, though in some cases it corresponds to a whole word or even punctuation. As the model processes text, it repeatedly predicts the most likely next token, adjusts its internal parameters based on the correctness of its predictions, and gradually develops a sophisticated sense of linguistic structure.

Importantly, the model does not memorize its training data. It does not store specific documents. Instead, it abstracts patterns and statistical relationships from the material it encounters. This abstraction enables the model to generate new sentences that resemble the style and structure of the training data without directly copying it. At the same time, because the model does not consult external sources or verify its statements, inaccuracies can arise even when the generated text sounds authoritative.
""",
        "mcq": [
            {
                "q": "What is the fundamental task an LLM learns during training?",
                "options": [
                    "Searching the internet to verify facts",
                    "Predicting the next token in a sequence",
                    "Memorizing entire documents word-for-word",
                    "Making ethical decisions based on values"
                ],
                "answer": "Predicting the next token in a sequence"
            },
            {
                "q": "What is a token in the context of LLMs?",
                "options": [
                    "A private database record",
                    "A piece of a word (or sometimes a full word/punctuation)",
                    "A guaranteed fact",
                    "A paragraph of stored training text"
                ],
                "answer": "A piece of a word (or sometimes a full word/punctuation)"
            },
            {
                "q": "Why can an LLM produce inaccuracies even when the text sounds confident?",
                "options": [
                    "Because it refuses to generate any uncertain content",
                    "Because it does not consult external sources or verify statements",
                    "Because it always copies a single website",
                    "Because it only uses predefined rules"
                ],
                "answer": "Because it does not consult external sources or verify statements"
            }
        ]
    },

    "4. The Mechanics of Text Generation": {
        "id": "s4_mech",
        "text": """
### Reading
When a user enters a prompt, the model analyzes the input and generates a response one token at a time. The process is incremental and dynamic. The model does not plan the entire response in advance. Instead, it determines the next token based on the current sequence and its learned probabilities, adds that token to the sequence, and then predicts the next one. This cycle continues until the model determines that the response is complete.

This generative process has practical implications. First, the phrasing of your prompt influences the model’s predictions. Even a slight change in wording can alter the direction or tone of the response. Second, the model’s capabilities are constrained by the size of its context window—the number of tokens it can consider at once. If a conversation or input exceeds this limit, earlier portions may be forgotten. Finally, because the model is not verifying facts but generating plausible text, it may produce statements that are incorrect, incomplete, or misleading. These limitations underscore the importance of precision and clarity when interacting with generative AI systems.
""",
        "mcq": [
            {
                "q": "How does an LLM generate a response after you enter a prompt?",
                "options": [
                    "It writes the full response first, then edits it",
                    "It generates the response one token at a time",
                    "It searches external databases and compiles results",
                    "It chooses from a fixed list of answers"
                ],
                "answer": "It generates the response one token at a time"
            },
            {
                "q": "Why can a small change in prompt wording change the output?",
                "options": [
                    "Because the model’s next-token predictions are sensitive to phrasing",
                    "Because the model uses emotions to interpret tone",
                    "Because the model always ignores the user’s wording",
                    "Because the model only responds with copied text"
                ],
                "answer": "Because the model’s next-token predictions are sensitive to phrasing"
            },
            {
                "q": "What does the context window limit imply?",
                "options": [
                    "The model can remember an unlimited conversation history",
                    "Earlier parts of long inputs may be forgotten if the limit is exceeded",
                    "The model can verify facts more accurately",
                    "The model can access private emails and calendars"
                ],
                "answer": "Earlier parts of long inputs may be forgotten if the limit is exceeded"
            }
        ]
    },

    "5. Strengths Across Disciplines": {
        "id": "s5_strengths",
        "text": """
### Reading
Generative AI is valuable not because it replaces human expertise but because it enhances it. Students in a wide variety of fields can use AI to support their learning and creative processes. In the humanities, generative AI can help students interpret complex texts, explore historical perspectives, or articulate arguments more clearly. Business students can use AI to generate marketing strategies, clarify financial concepts, or draft professional communication. Engineering students can leverage AI to break down complicated technical topics, generate design alternatives, or outline procedures for experiments. Students in the health sciences may use AI to translate medical terminology into patient-friendly language or practice reasoning through clinical scenarios. In the arts, generative AI can assist with brainstorming themes, writing artist statements, or exploring conceptual ideas for creative work.

Across all of these areas, AI acts as a flexible partner capable of adapting to different tasks and audiences. When guided effectively, the model can enhance productivity, deepen understanding, and accelerate early stages of a project. However, to take advantage of these strengths, students must understand how to provide context, specify expectations, and verify the accuracy of the responses they receive.
""",
        "mcq": [
            {
                "q": "According to the reading, why is generative AI valuable across disciplines?",
                "options": [
                    "It replaces human expertise in most fields",
                    "It enhances human learning and creative work when guided well",
                    "It guarantees perfect accuracy and citations",
                    "It removes the need for domain knowledge"
                ],
                "answer": "It enhances human learning and creative work when guided well"
            },
            {
                "q": "Which is an example of a health sciences use mentioned in the reading?",
                "options": [
                    "Generating lab equipment automatically",
                    "Translating medical terminology into patient-friendly language",
                    "Predicting stock prices with certainty",
                    "Writing legal advice that replaces professionals"
                ],
                "answer": "Translating medical terminology into patient-friendly language"
            },
            {
                "q": "What must students do to take advantage of AI’s strengths effectively?",
                "options": [
                    "Provide context, specify expectations, and verify accuracy",
                    "Avoid using AI for any learning task",
                    "Use only vague prompts so the AI is more creative",
                    "Assume AI output is correct if it sounds confident"
                ],
                "answer": "Provide context, specify expectations, and verify accuracy"
            }
        ]
    },

    "6. Limitations and Common Pitfalls": {
        "id": "s6_limits",
        "text": """
### Reading
Despite its adaptability, generative AI has well-defined limitations. The most important is that the model does not possess factual memory or access to realtime information. It generates responses based on patterns rather than truth. This can lead to what researchers call hallucinations, in which the system produces confident but incorrect information. Hallucinations may be subtle, such as a slight error in a definition, or more severe, such as fabricated citations or inaccurate statistics.

Another limitation arises from ambiguity. When a prompt lacks specificity, the model must infer the user’s intent. These inferences are often incorrect. A request such as “Explain Mendelian genetics” could produce an explanation at an elementary, intermediate, or advanced level, depending on the model’s interpretation. Without clear guidance about the intended audience or purpose, the model may produce a response that is technically correct but inappropriate for the assignment.

Generative AI also struggles with tasks that require moral reasoning, legal interpretation, highly specialized expertise, or real-world judgment. Although the model can outline general arguments or summarize common viewpoints, it cannot substitute for human evaluation or professional decision-making. These limitations do not diminish the value of generative AI. Instead, they highlight the need for thoughtful prompting, verification, and ethical consideration.
""",
        "mcq": [
            {
                "q": "What is meant by “hallucinations” in generative AI?",
                "options": [
                    "The model refuses to answer all questions",
                    "The model produces confident but incorrect information",
                    "The model accesses real-time information without permission",
                    "The model stores and repeats private data"
                ],
                "answer": "The model produces confident but incorrect information"
            },
            {
                "q": "Why does prompt ambiguity often cause problems?",
                "options": [
                    "Because the model must infer intent and may infer incorrectly",
                    "Because ambiguity increases the context window automatically",
                    "Because the model becomes more accurate with less detail",
                    "Because ambiguity forces the model to cite sources"
                ],
                "answer": "Because the model must infer intent and may infer incorrectly"
            },
            {
                "q": "Which type of task is highlighted as a challenge for generative AI?",
                "options": [
                    "Summarizing common viewpoints",
                    "Brainstorming themes for a project",
                    "Moral or legal interpretation requiring real-world judgment",
                    "Explaining a concept with an analogy"
                ],
                "answer": "Moral or legal interpretation requiring real-world judgment"
            }
        ]
    },

    "7. What is a Prompt?": {
        "id": "s7_prompt",
        "text": """
### Reading
A prompt is the text you provide to an AI system to initiate an interaction. It can take the form of a question, instruction, task, or multi-step directive. The quality of the model’s response depends heavily on the clarity and structure of the prompt. A prompt is not just a query; it is a tool for shaping the model’s behavior. A carefully designed prompt communicates intent, establishes context, and guides the structure of the output.

Unlike human conversation, AI interactions do not rely on shared knowledge or assumptions. The model cannot guess your purpose or infer the background of your assignment. Therefore, prompts must explicitly state the task, audience, level of detail, desired format, and any necessary constraints. This level of specificity may feel unnatural at first, but it is essential for effective communication with generative systems.

For example, the prompt “Summarize this article” leaves many questions unanswered. A more effective prompt might specify the audience (e.g., first-year nursing students), the length (e.g., a 150-word summary), the purpose (e.g., highlighting clinical relevance), and the format (e.g., a narrative paragraph). Small clarifications of this sort significantly improve the relevance and accuracy of the model’s response.
""",
        "mcq": [
            {
                "q": "Which best defines a prompt according to the reading?",
                "options": [
                    "A hidden rule the AI creates on its own",
                    "The text you provide to initiate and shape an AI interaction",
                    "A guarantee that the AI will be accurate",
                    "A citation list attached to an answer"
                ],
                "answer": "The text you provide to initiate and shape an AI interaction"
            },
            {
                "q": "Why must prompts be more explicit than human conversation?",
                "options": [
                    "Because AI relies on shared assumptions like humans do",
                    "Because the model cannot guess your purpose or assignment context",
                    "Because longer prompts always reduce accuracy",
                    "Because AI has access to your course materials automatically"
                ],
                "answer": "Because the model cannot guess your purpose or assignment context"
            },
            {
                "q": "Which prompt is more effective based on the reading?",
                "options": [
                    "“Summarize this article.”",
                    "“Summarize this article for first-year nursing students in 150 words, focusing on clinical relevance, in one paragraph.”",
                    "“Write whatever you want about this article.”",
                    "“Give me the best summary possible.”"
                ],
                "answer": "“Summarize this article for first-year nursing students in 150 words, focusing on clinical relevance, in one paragraph.”"
            }
        ]
    },

    "8. Why Prompts Matter So Much": {
        "id": "s8_matter",
        "text": """
### Reading
Prompt engineering—the practice of designing effective prompts—is not about tricking the model but about communicating clearly. AI models follow the instructions they receive. If the instructions are incomplete or ambiguous, the model’s output will reflect that ambiguity. The model does not understand context that is not explicitly provided, and it does not read your mind. Your ability to get high-quality results depends on how well you can articulate your needs.

Strong prompts share several characteristics. They state the intent of the task, specify the audience, establish the scope, and outline the desired format. They may also provide examples or ask the model to follow a particular structure. As you gain experience, you will learn how different prompting strategies influence the model and how to adapt these strategies to different tasks.

Prompts are also iterative. A strong prompt often emerges through refinement. You may begin with a simple request, evaluate the response, identify missing details, and revise the prompt accordingly. This iterative process mirrors human problem-solving and helps you develop a deeper understanding of both the task and the model’s behavior.
""",
        "mcq": [
            {
                "q": "What is prompt engineering primarily about, according to the reading?",
                "options": [
                    "Tricking the model into giving hidden answers",
                    "Communicating clearly to guide the model’s behavior",
                    "Avoiding constraints so the model is free",
                    "Copying prompts from the internet without changes"
                ],
                "answer": "Communicating clearly to guide the model’s behavior"
            },
            {
                "q": "Which set of elements is emphasized as common characteristics of strong prompts?",
                "options": [
                    "Intent, audience, scope, and output format",
                    "Random wording, minimal context, and no constraints",
                    "Only the task name and nothing else",
                    "Personal opinions and emotional tone only"
                ],
                "answer": "Intent, audience, scope, and output format"
            },
            {
                "q": "What does it mean that prompts are iterative?",
                "options": [
                    "You write one prompt and never change it",
                    "You refine prompts based on the response to improve results",
                    "You must always use the same prompt template",
                    "You should avoid evaluating AI output"
                ],
                "answer": "You refine prompts based on the response to improve results"
            }
        ]
    },

    "9. Ethical and Responsible Use of AI": {
        "id": "s9_ethics",
        "text": """
### Reading
In academic settings, the use of AI raises important questions about integrity, authorship, and responsibility. Universities such as SIUE maintain strict policies on academic honesty, and these policies apply to AI assistance. Using AI to brainstorm ideas, clarify concepts, revise drafts, or explore alternative perspectives can be beneficial and appropriate. However, using AI to complete assignments without acknowledgment, fabricate sources, or bypass learning objectives violates academic standards.

Responsible use also includes awareness of privacy and data protection. When interacting with AI systems, avoid entering personal or sensitive information. Remember that AI models may reflect biases present in their training data. Evaluate outputs critically and consider multiple perspectives.

Transparency is another key principle. When instructors require disclosure of AI assistance, be honest about how you used the tool. In many professional contexts, the ability to collaborate effectively with AI is considered a skill rather than a shortcut. Clear communication about your use of AI helps maintain trust and accountability.
""",
        "mcq": [
            {
                "q": "Which use of AI is described as generally appropriate in academic settings?",
                "options": [
                    "Fabricating citations and sources",
                    "Completing assignments without acknowledgment",
                    "Brainstorming ideas or clarifying concepts with AI assistance",
                    "Bypassing learning objectives"
                ],
                "answer": "Brainstorming ideas or clarifying concepts with AI assistance"
            },
            {
                "q": "What is one recommended privacy practice when using AI tools?",
                "options": [
                    "Share personal sensitive information to get better answers",
                    "Avoid entering personal or sensitive information",
                    "Upload private student records for more context",
                    "Assume everything you enter is always deleted immediately"
                ],
                "answer": "Avoid entering personal or sensitive information"
            },
            {
                "q": "Why is transparency emphasized?",
                "options": [
                    "Because AI output is always perfect",
                    "Because clear disclosure maintains trust and accountability",
                    "Because instructors never allow AI use",
                    "Because transparency makes prompts shorter"
                ],
                "answer": "Because clear disclosure maintains trust and accountability"
            }
        ]
    },

    "10. The Future of Generative AI in Academic and Professional Life": {
        "id": "s10_future",
        "text": """
### Reading
Generative AI is not a passing trend. Its capabilities will continue to grow, and its presence in workplaces and research environments will expand. Mastery of prompt engineering will soon be as essential as proficiency in writing, data analysis, or digital literacy. Employers increasingly expect graduates to know how to collaborate with AI tools, and those who lack these skills may find themselves at a disadvantage.

Learning to use AI effectively is not about replacing human intelligence. It is about extending your capacity to think, create, and communicate. AI can help you explore ideas more quickly, understand complex material, and express your thoughts more clearly. It can serve as a tutor, a brainstorming partner, a writing coach, or an analytical assistant. The more you understand its strengths and limitations, the more effectively you can integrate it into your academic and professional work.

This course will teach you how to harness these abilities. Module 1 provides a foundation for understanding how AI systems function. Module 2 introduces the core principles of prompt interpretation. Subsequent modules will teach you specific prompting patterns, multimodal techniques, verification strategies, and real-world applications across disciplines. By the end of the semester, you will be able to design, evaluate, and refine prompts with confidence.
""",
        "mcq": [
            {
                "q": "What does the reading suggest about the future role of generative AI?",
                "options": [
                    "It will likely fade away soon",
                    "Its capabilities and workplace presence will likely expand",
                    "It will eliminate the need for communication skills",
                    "It will only matter in computer science fields"
                ],
                "answer": "Its capabilities and workplace presence will likely expand"
            },
            {
                "q": "How does the reading describe effective AI use?",
                "options": [
                    "Replacing human intelligence",
                    "Extending your ability to think, create, and communicate",
                    "Avoiding learning and relying on AI",
                    "Using AI only for entertainment"
                ],
                "answer": "Extending your ability to think, create, and communicate"
            },
            {
                "q": "What is the role of Module 2 according to the reading?",
                "options": [
                    "Core principles of prompt interpretation",
                    "Advanced multimodal video editing",
                    "Final exam preparation only",
                    "Building neural networks from scratch"
                ],
                "answer": "Core principles of prompt interpretation"
            }
        ]
    },

    "11. Summary and Key Takeaways": {
        "id": "s11_summary",
        "text": """
### Reading
Generative AI represents a major shift in how we interact with information. Although these systems can produce impressive text, their capabilities arise from learned patterns rather than genuine understanding. As a user, your effectiveness depends on your ability to communicate clearly, specify your expectations, and evaluate the model’s output critically.

This chapter emphasized several foundational concepts. Generative AI creates content based on statistical relationships in language. It operates within a context window, which limits the amount of information it can consider at once. It is highly sensitive to the structure and clarity of prompts. It excels at explanation, brainstorming, summarization, and organization but struggles with factual accuracy, ambiguity, and specialized judgment. Ethical use of AI is essential, especially in academic settings where transparency and integrity matter.

As we move into the next module, you will learn how AI interprets your inputs through the lenses of intent, structure, and context. These principles form the backbone of effective prompting and will prepare you for more advanced techniques throughout the course.
""",
        "mcq": [
            {
                "q": "According to the summary, what most affects your effectiveness when using generative AI?",
                "options": [
                    "How fast you type",
                    "Clear communication, expectations, and critical evaluation of output",
                    "Using the longest possible prompts",
                    "Avoiding verification because AI is reliable"
                ],
                "answer": "Clear communication, expectations, and critical evaluation of output"
            },
            {
                "q": "Which limitation is emphasized as a key concern?",
                "options": [
                    "Unlimited memory of past conversations",
                    "Guaranteed factual accuracy",
                    "Sensitivity to prompt structure and limited context window",
                    "Direct access to real-time databases"
                ],
                "answer": "Sensitivity to prompt structure and limited context window"
            },
            {
                "q": "What will Module 2 focus on next?",
                "options": [
                    "Intent, structure, and context in how AI interprets inputs",
                    "Hardware design for AI chips",
                    "Programming reinforcement learning agents",
                    "Building a web crawler for citations"
                ],
                "answer": "Intent, structure, and context in how AI interprets inputs"
            }
        ]
    },
}

# ------------------ SIDEBAR PAGES ------------------
sidebar_pages = [
    "✅ Start Here (Checklist)",
    "🎧 Lecture Video / Voice Recording",
    "📖 Readings (Chapter Sections 1–11)",
    "🧪 Prompt Lab (ChatGPT Practice)",
    "📝 Reflection Assignment",
]

page = st.sidebar.radio("Choose a page:", sidebar_pages)

# =======================================================
# START PAGE: CHECKLIST
# =======================================================
if page == "✅ Start Here (Checklist)":
    st.subheader("✅ Module 1 Checklist")

    st.markdown("""
Use this checklist to complete Module 1 in order. After completing the Module assignments, download your responses and submit the file on Blackboard.  
You can return here anytime to see what is still missing.
""")

    name = safe_strip("student_name")
    q1 = safe_strip("q1_intro")
    q2 = safe_strip("q2_slide")

    prompt_used = safe_strip("m1_prompt_used")
    ai_resp = safe_strip("m1_ai_response")
    prompt_ref = safe_strip("m1_prompt_reflection")

    refl = safe_strip("reflection_m1")
    refl_wc = word_count(refl)

    def status_line(done: bool, text: str):
        st.write(("✅ " if done else "⬜ ") + text)

    status_line(bool(name), "Enter your full name (left sidebar)")
    status_line(bool(q1 and q2), "Watch the video + answer Q1 and Q2")
    status_line(bool(prompt_used and ai_resp and prompt_ref), "Complete Prompt Lab (prompt + AI response + reflection)")
    status_line(150 <= refl_wc <= 250, "Write the 150–250 word Module Reflection")

    st.markdown("---")
    st.markdown("### ⬇️ Download Your Responses (Video Questions+Prompt Lab+Reflection)")
    section_download_block()
    goto_module_2_button()

# =======================================================
# LECTURE VIDEO PAGE
# =======================================================
elif page == "🎧 Lecture Video / Voice Recording":
    st.subheader("🎧 Lecture for Module 1 — Foundations of Generative AI")

    st.markdown("### 📄 Downloadable PDF Notes")
    pdf_path = "notes/Intelligent_Prompting.pdf"  # adjust if needed
    try:
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="Download Module 1 Notes (PDF)",
                data=pdf_file,
                file_name="Intelligent_Prompting.pdf",
                mime="application/pdf"
            )
    except Exception:
        st.warning(f"PDF notes not found. Add your file to `{pdf_path}` (or update the path in the code).")

    st.markdown("### 📺 Video Lecture")
    st.video("https://siue.yuja.com/Dashboard/Permalink?authCode=167158588&b=14078175&linkType=video")

    st.markdown("---")
    with st.expander("📝 Lecture Transcript (click to open)", expanded=False):
        st.markdown("*Replace this placeholder with your real transcript after recording the lecture.*")

    st.markdown("---")
    st.markdown("## 🧠 Video Questions")

    with st.form("video_questions_form"):
        st.markdown("### **1) Please briefly introduce yourself — your major, hometown, interests, etc.**")
        st.text_area("Your response:", key="q1_intro", height=120)

        st.markdown("### **2) What did you notice in this slide?**")
        st.text_area("Your response:", key="q2_slide", height=120)

        submitted = st.form_submit_button("Submit Video Questions")

    if submitted:
        if safe_strip("q1_intro") and safe_strip("q2_slide"):
            st.success("Thank you! Your responses have been recorded.")
        else:
            st.warning("Please answer both questions before submitting.")

    

    goto_module_2_button()

# =======================================================
# READINGS PAGE (Sections 1–11 with MCQs after each)
# =======================================================
elif page == "📖 Readings (Chapter Sections 1–11)":
    st.subheader("📖 Module 1 Readings (Sections 1–11)")

    st.markdown("""
Use the dropdown to select a reading section.  
Each section includes **3 multiple-choice questions** to check understanding.
""")

    section_title = st.selectbox("Choose a reading section:", list(READINGS.keys()))
    section = READINGS[section_title]

    render_reading_section(
        title=section_title,
        body=section["text"],
        section_id=section["id"],
        questions=section["mcq"]
    )


# =======================================================
# PROMPT LAB (Option A — practice in ChatGPT, paste back)
# =======================================================
elif page == "🧪 Prompt Lab (ChatGPT Practice)":
    st.subheader("🧪 Prompt Lab — Practice in ChatGPT (Module 1)")

    st.markdown("""
**Goal:** Practice writing clear prompts and reflecting on what improved.

**What to submit in this app:**
1) The prompt you used  
2) The AI response  
3) A short reflection (3–5 sentences)
""")

    st.markdown("### Step 1 — Open ChatGPT")
    try:
        st.link_button("Open ChatGPT", "https://chat.openai.com/")
    except Exception:
        st.markdown("Open ChatGPT: https://chat.openai.com/")

    st.markdown("---")
    st.markdown("### Step 2 — Choose ONE prompt below and run it in ChatGPT")

    prompt_choice = st.radio(
        "Pick a prompt to copy into ChatGPT:",
        [
            "Option A — Explain Generative AI (clarity + constraints)",
            "Option B — Verification Habit (check what to verify)",
            "Option C — Improve a vague prompt (before/after)"
        ],
        index=0
    )

    if prompt_choice.startswith("Option A"):
        suggested_prompt = (
            "Explain **generative AI** to a first-year college student in my major (**[your major]**). "
            "Use: (1) 3 bullet points, (2) 1 real example in my field, and (3) one limitation of LLMs. "
            "Keep it under 180 words."
        )
    elif prompt_choice.startswith("Option B"):
        suggested_prompt = (
            "I will paste a short claim about AI. Tell me: "
            "(1) what parts might be incorrect or oversimplified, "
            "(2) what I should verify, and "
            "(3) where I could verify it (types of sources). "
            "Keep it under 150 words.\n\nClaim: [paste your claim here]"
        )
    else:
        suggested_prompt = (
            "Here is a vague prompt I wrote: “[paste it here]”.\n\n"
            "1) Rewrite it to be clear and specific (include constraints and output format).\n"
            "2) Explain what you changed and why.\n"
            "3) Provide 2 alternative versions for different audiences."
        )

    st.text_area(
        "Suggested prompt (copy this into ChatGPT, then customize it):",
        value=suggested_prompt,
        height=170
    )

    st.markdown("---")
    st.markdown("### Step 3 — Paste your work here")

    st.text_area(
        "✅ Paste the exact prompt you used in ChatGPT:",
        key="m1_prompt_used",
        height=140,
        placeholder="Paste your final prompt here..."
    )

    st.text_area(
        "✅ Paste the AI response you received:",
        key="m1_ai_response",
        height=220,
        placeholder="Paste the AI response here..."
    )

    st.markdown("---")
    st.markdown("### Step 4 — Reflection (3–5 sentences)")
    st.caption("Aim for ~50–120 words.")
    st.text_area(
        "What worked well? What would you change to make your prompt clearer or more specific?",
        key="m1_prompt_reflection",
        height=160,
        placeholder="Write 3–5 sentences..."
    )

    pr_wc = word_count(safe_strip("m1_prompt_reflection"))
    st.caption(f"Prompt Lab reflection word count: {pr_wc}")

    st.markdown("---")
    if st.button("Check Prompt Lab Completeness", key="m1_promptlab_check"):
        missing = []
        if not safe_strip("m1_prompt_used"):
            missing.append("your prompt")
        if not safe_strip("m1_ai_response"):
            missing.append("the AI response")
        if not safe_strip("m1_prompt_reflection"):
            missing.append("your reflection")
        if missing:
            st.warning("Please add: " + ", ".join(missing) + ".")
        else:
            st.success("Prompt Lab looks complete. You can download your responses below.")


    goto_module_2_button()

# =======================================================
# REFLECTION ASSIGNMENT
# =======================================================
elif page == "📝 Reflection Assignment":
    st.subheader("📝 Module 1 Reflection")

    st.markdown("""
Submit a **150–250 word** reflection:
- What did you learn?
- How could generative AI help in your major?
- What questions do you still have?
""")

    st.text_area("Write your reflection here:", height=220, key="reflection_m1")

    wc = word_count(safe_strip("reflection_m1"))
    st.caption(f"Word count: {wc} (target 150–250)")
    if wc > 0 and (wc < 150 or wc > 250):
        st.warning("Your reflection is outside the 150–250 word range. Please revise.")

    if st.button("Preview Reflection", key="m1_reflection_preview"):
        if safe_strip("reflection_m1"):
            st.success("### Reflection Preview:")
            st.write(safe_strip("reflection_m1"))
        else:
            st.warning("Write a reflection to preview.")

    st.markdown("---")
    st.markdown("### ⬇️ Download Your Responses (Video Questions+Prompt Lab+Reflection)")
    section_download_block()

    goto_module_2_button()
