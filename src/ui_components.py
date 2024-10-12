import streamlit as st

from src.config import IMAGE_EXTENSIONS, VIDEO_EXTENSIONS
from src.utils import encode_image, encode_video, all_images, all_videos


@st.cache_data
def cached_encode_image(image):
    return encode_image(image)


@st.cache_data
def cached_encode_video(video):
    return encode_video(video)


def file_upload():
    # Sidebar header
    st.sidebar.header("Upload Files")
    uploaded_files, file_objects = None, None

    # File uploader with improved grammar and standardized code
    uploaded_files = st.sidebar.file_uploader(
        "Please select either up to 3 images or a single video file...",
        type=IMAGE_EXTENSIONS + VIDEO_EXTENSIONS,
        accept_multiple_files=True,
    )

    if uploaded_files is not None and len(uploaded_files) > 0:
        # check if all of the uploaded files are images or videos
        if all_images(uploaded_files) and len(uploaded_files) <= 3:
            with st.sidebar.status("Processing image..."):
                file_objects = [cached_encode_image(image) for image in uploaded_files]
                st.sidebar.image(uploaded_files, use_column_width=True)

        elif all_videos(uploaded_files) and len(uploaded_files) == 1:
            with st.sidebar.status("Processing video..."):
                file_objects = cached_encode_video(uploaded_files[0])
                st.sidebar.video(uploaded_files[0])
        else:
            st.error(
                "Please upload up to 3 images or a single video file with the following extensions: "
                + ", ".join(IMAGE_EXTENSIONS + VIDEO_EXTENSIONS)
            )

    return uploaded_files, file_objects


def header():
    # CSS to center crop the image in a circle
    circle_image_css = """
    <style>
    .center-cropped {
        display: block;
        margin-left: auto;
        margin-right: auto;
        border-radius: 50%;
        width: 96px;
        height: 96px;
        object-fit: cover;
    }
    </style>
    """

    # Inject CSS
    st.markdown(circle_image_css, unsafe_allow_html=True)

    st.markdown(
        """
        <div align="center">
            <h3 style="margin-bottom:-55px;margin-left:55px;color:#6332e5"></h3>
            <img src="url here" width="800"/>   
        </div
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div style='text-align: center; margin-bottom:4'>"
        "<p>DermaTech is your personal AI assistant for skin care advice and analysis.</p>"
        "</div>",
        unsafe_allow_html=True,
    )


def patient_card():
    st.sidebar.header("Patient Card")
    with st.sidebar.form("patient_card"):
        age = st.number_input("Age", min_value=0, max_value=120, step=1)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        skin_type = st.selectbox("Skin Type", ["Normal", "Dry", "Oily", "Combination", "Sensitive"])
        submit_button = st.form_submit_button(label="Submit")
    
    if submit_button:
        return f"Patient: Age {age}, Gender {gender}, Skin Type {skin_type}"
    return None
