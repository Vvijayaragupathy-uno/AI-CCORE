import requests
import streamlit as st
from typing import List, Dict
import xml.etree.ElementTree as ET
from llm import get_llm_response

# Fetch Research Papers Using arXiv API
def fetch_research_papers(query: str, max_results: int = 5) -> List[Dict]:
    url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results,
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch research papers: {response.status_code}")

    # Parse the response (XML format)
    root = ET.fromstring(response.text)
    papers = []
    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        title = entry.find("{http://www.w3.org/2005/Atom}title").text.strip()
        abstract = entry.find("{http://www.w3.org/2005/Atom}summary").text.strip()
        link = entry.find("{http://www.w3.org/2005/Atom}id").text.strip()
        papers.append({
            "title": title,
            "abstract": abstract,
            "link": link,
        })
    return papers

# Summarize Research Papers
def summarize_paper(abstract: str):
    summary_prompt = f"Summarize the following research paper abstract in 2-3 sentences:\n\n{abstract}"
    summary = get_llm_response(summary_prompt, max_tokens=400, stream=False)
    return summary

# Display Articles and Enable Interactive Q&A
def article_page():
    st.title("Research Papers Using arXiv")
    st.write("Explore summaries of research papers Abstract and interact with them.")

    # Allow users to set the number of results
    max_results = st.slider("Number of results to display", min_value=5, max_value=10, value=5)

    # Fetch research papers
    query = st.text_input("Enter a Keyword (e.g., 'machine learning'):")
    if query:
        try:
            papers = fetch_research_papers(query, max_results=max_results)
            st.success(f"Fetched {len(papers)} research papers.")
        except Exception as e:
            st.error(f"Failed to fetch research papers: {str(e)}")
            return

        # Display articles
        for i, paper in enumerate(papers):
            st.subheader(f"Article {i + 1}: {paper['title']}")
            st.write(f"**Abstract:** {paper['abstract']}")

            # Construct the PDF download link
            pdf_link = paper['link'].replace("abs", "pdf") + ".pdf"
            st.markdown(f"[Download PDF]({pdf_link})", unsafe_allow_html=True)

            # Generate and display summary
            if st.button(f"Summarize Article {i + 1}", key=f"summarize_{i}"):
                summary = summarize_paper(paper['abstract'])
                st.write(f"**Summary:** {summary}")

            # Enable interactive Q&A
            if st.button(f"Ask Questions About Article {i + 1}", key=f"qa_{i}"):
                st.session_state.selected_paper_index = i  # Track which article is selected
                st.session_state.qa_history = st.session_state.get("qa_history", [])  # Initialize Q&A history

            # Display Q&A for the selected article
            if "selected_paper_index" in st.session_state and st.session_state.selected_paper_index == i:
                st.header(f"Q&A for: {paper['title']}")

                # Display Q&A history
                if "qa_history" in st.session_state:
                    for qa in st.session_state.qa_history:
                        st.write(f"**Q:** {qa['question']}")
                        st.write(f"**A:** {qa['answer']}")

                # Predefined clickable questions
                predefined_questions = [
                    "What is the main contribution of this paper?",
                    "Extract the code from the method they are using",
                    "Extract the key concepts from the paper",
                    "What methods are used in this paper?",
                    "What are the key findings of this paper?",
                ]
                for question in predefined_questions:
                    if st.button(question, key=f"predefined_{i}_{question}"):
                        answer = get_llm_response(
                            f"Context: {paper['abstract']}\n\nQuestion: {question}"
                        )
                        if "qa_history" not in st.session_state:
                            st.session_state.qa_history = []
                        st.session_state.qa_history.append({"question": question, "answer": answer})
                        st.rerun()  # Refresh to display the new Q&A

                # Allow custom questions
                with st.form(key=f"custom_question_form_{i}"):
                    custom_question = st.text_input("Ask your own question:", key=f"custom_{i}")
                    if st.form_submit_button("Submit"):
                        if custom_question:
                            answer = get_llm_response(
                                f"Context: {paper['abstract']}\n\nQuestion: {custom_question}"
                            )
                            if "qa_history" not in st.session_state:
                                st.session_state.qa_history = []
                            st.session_state.qa_history.append({"question": custom_question, "answer": answer})
                            st.rerun()  # Refresh to display the new Q&A