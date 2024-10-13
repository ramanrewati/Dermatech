import streamlit as st

from src.api import client
from src.config import SYSTEM_MESSAGE, MODEL
from src.ui_components import file_upload, header, patient_card, disclaimer_note
from src.utils import prepare_content_with_images, all_images, all_videos

def main():
    # Title section
    header()

    # Patient Card
    patient_info = patient_card()
    if patient_info:
        SYSTEM_MESSAGE["content"] = f"{SYSTEM_MESSAGE['content']} {patient_info}"

    # Sidebar section for file upload
    uploaded_files, file_objects = file_upload()
    disclaimer_note()

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if st.session_state.messages:
        # Add clear chat history button to sidebar
        st.sidebar.button(
            "Clear Chat History",
            on_click=lambda: st.session_state.messages.clear(),
            type="primary",
        )

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            content = message["content"]
            if isinstance(content, list):
                st.markdown(content[0]["text"])
                # Display uploaded images
                for item in content[1:]:
                    if "image_url" in item:
                        st.image(item["image_url"], width=400)
            else:
                st.markdown(content)

    if prompt := st.chat_input("Ask about your skin care concerns", key="prompt"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
            content = prepare_content_with_images(prompt, file_objects) if file_objects else prompt
            if file_objects:
                if all_images(uploaded_files):
                    st.image(uploaded_files, width=400)
                elif all_videos(uploaded_files):
                    st.video(uploaded_files[0], autoplay=True)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": content})

        # Get response from the assistant
        with st.chat_message("assistant"):
            messages = [SYSTEM_MESSAGE] + st.session_state.messages
            stream = client.chat.completions.create(
                model=MODEL, messages=messages, stream=True
            )
            response = st.write_stream(stream)

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()