import requests
import streamlit as st

from config import MAX_CODE_CHARS, OLLAMA_URL
from services.ollama import build_prompt, call_ollama, strip_code_fence

LANGUAGES = ["python", "javascript", "typescript", "java", "c++", "c#", "go", "ruby"]

LANGUAGE_TO_PYGMENTS = {
    "python": "python", "javascript": "javascript", "typescript": "typescript",
    "java": "java", "c++": "cpp", "c#": "csharp", "go": "go", "ruby": "ruby",
}
LANGUAGE_TO_EXTENSION = {
    "python": "py", "javascript": "js", "typescript": "ts", "java": "java",
    "c++": "cpp", "c#": "cs", "go": "go", "ruby": "rb",
}
EXTENSION_TO_LANGUAGE = {
    "py": "python", "js": "javascript", "ts": "typescript", "java": "java",
    "cpp": "c++", "cc": "c++", "cxx": "c++", "cs": "c#", "go": "go", "rb": "ruby",
}


def run_app() -> None:
    st.set_page_config(
        page_title="Code Comment Generator",
        page_icon=":material/auto_awesome:",
        layout="wide",
    )

    st.title("Code Comment Generator", anchor=False)
    st.caption("Turn dense code into clear, maintainable code with helpful comments.")

    if "output" not in st.session_state:
        st.session_state.output = ""
    if "detected_language" not in st.session_state:
        st.session_state.detected_language = None

    st.write("")
    left, right = st.columns(2, gap="large", vertical_alignment="top")

    with left:
        with st.container(border=True):
            st.subheader("Your code", anchor=False)
            st.caption("Paste a snippet or upload a source file to get started.")

            uploaded_file = st.file_uploader(
                "Import a file (optional)",
                type=["py", "js", "ts", "java", "cpp", "cs", "go", "rb", "txt"],
                label_visibility="collapsed",
            )

            file_text = ""
            if uploaded_file is not None:
                file_text = uploaded_file.read().decode("utf-8", errors="ignore")
                ext = uploaded_file.name.rsplit(".", 1)[-1].lower()
                st.session_state.detected_language = EXTENSION_TO_LANGUAGE.get(ext)

            code_input = st.text_area(
                "Paste your code",
                value=file_text,
                height=390,
                placeholder="Paste your code here...",
                label_visibility="collapsed",
            )

            default_index = (
                LANGUAGES.index(st.session_state.detected_language)
                if st.session_state.detected_language in LANGUAGES
                else 0
            )
            language = st.selectbox("Language", LANGUAGES, index=default_index)
            if st.session_state.detected_language:
                st.caption(
                    f"Detected **{st.session_state.detected_language}** "
                    "from the uploaded file's extension."
                )

            char_count = len(code_input)
            over_limit = char_count > MAX_CODE_CHARS
            counter_color = "red" if over_limit else "gray"
            st.markdown(
                f":{counter_color}[{char_count:,} / {MAX_CODE_CHARS:,} characters]"
            )

            generate = st.button(
                "Generate comments",
                type="primary",
                icon=":material/auto_awesome:",
                disabled=not code_input.strip() or over_limit,
                width="stretch",
            )

    with right:
        with st.container(border=True):
            st.subheader("Commented code", anchor=False)
            st.caption("Your generated result will appear here.")

            if generate:
                if over_limit:
                    st.error(f"That's {char_count:,} characters — please keep it under {MAX_CODE_CHARS:,}.")
                else:
                    with st.spinner("Generating comments..."):
                        try:
                            raw_reply = call_ollama(build_prompt(code_input, language))
                            st.session_state.output = strip_code_fence(raw_reply)
                        except requests.exceptions.ConnectionError:
                            print("Ollama connection error")
                            st.error("Couldn't reach Ollama. Is it running at " + OLLAMA_URL + "?")
                        except requests.exceptions.Timeout:
                            print("Ollama request timed out")
                            st.error("Ollama took too long to respond. Try again or use a shorter snippet.")
                        except Exception as exc:  # noqa: BLE001 - surfaced to the user below
                            print(f"Code comment generation failed: {exc}")
                            st.error("Failed to generate comments. Check the terminal for details.")

            if st.session_state.output:
                st.code(
                    st.session_state.output,
                    language=LANGUAGE_TO_PYGMENTS.get(language, "text"),
                    line_numbers=True,
                )
                st.download_button(
                    "Download commented file",
                    st.session_state.output,
                    file_name=f"commented.{LANGUAGE_TO_EXTENSION.get(language, 'txt')}",
                    icon=":material/download:",
                    width="content",
                )
            else:
                st.info(
                    "Your commented code will appear here.",
                    icon=":material/code:",
                )
