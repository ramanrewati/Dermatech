import streamlit as st
from src.config import IMAGE_EXTENSIONS, VIDEO_EXTENSIONS
from src.utils import encode_image, encode_video, all_images, all_videos

# Caching functions
@st.cache_data
def cached_encode_image(image):
    return encode_image(image)

@st.cache_data
def cached_encode_video(video):
    return encode_video(video)

# UI Components
def header():
    st.markdown(
        """
        <style>
        .center-cropped {
            display: block;
            margin: 0 auto;
            border-radius: 50%;
            width: 96px;
            height: 96px;
            object-fit: cover;
        }
        .header-container {
            text-align: center;
            padding: 20px 0;
            background-color: rgba(99, 50, 229, 0.1);
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .header-title {
            color: #6332e5;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .header-subtitle {
            font-size: 1.2em;
            color: #666;
        }
        .content-container {
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .image-container img {
            border: 2px solid #6332e5;
            border-radius: 10px;
        }
        </style>
        
        <div class="header-container">
            <h1 class="header-title">DermaTech</h1>
            <p class="header-subtitle">Your personal AI assistant for skin care advice and analysis.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def file_upload():
    st.sidebar.header("Upload Files")
    
    uploaded_files = st.sidebar.file_uploader(
        "Upload up to 3 images or 1 video",
        type=IMAGE_EXTENSIONS + VIDEO_EXTENSIONS,
        accept_multiple_files=True,
    )
    
    if not uploaded_files:
        return None, None
    
    if all_images(uploaded_files) and len(uploaded_files) <= 3:
        return process_images(uploaded_files)
    elif all_videos(uploaded_files) and len(uploaded_files) == 1:
        return process_video(uploaded_files[0])
    else:
        st.error(f"Please upload up to 3 images or a single video file. Supported formats: {', '.join(IMAGE_EXTENSIONS + VIDEO_EXTENSIONS)}")
        return None, None

def process_images(images):
    with st.sidebar.status("Processing images..."):
        file_objects = [cached_encode_image(image) for image in images]
        st.sidebar.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.sidebar.image(images, use_column_width=True)
        st.sidebar.markdown('</div>', unsafe_allow_html=True)
    return images, file_objects

def process_video(video):
    with st.sidebar.status("Processing video..."):
        file_object = cached_encode_video(video)
        st.sidebar.video(video)
    return [video], file_object

def disclaimer_note():  # Improved Disclaimer Note
    st.sidebar.markdown(
        """
        <div style="background-color: #004040; padding: 10px; border-radius: 5px; border: 1px solid #FFE499; margin-bottom: 10px;">
            <p style="font-size: 0.9em; color: #fefefa;">
                <b>Note:</b> This is a prototype and doesn't represent the final build. Lower precision modes are used for efficient inference. In case you are unable to use it, please try running it locally (at least 16GB of VRAM is required to run the model) or contact <a href="mailto:rewatiramansingh01@proton.me">rewatiramansingh01@proton.me</a> to refresh the server.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def patient_card():
    st.sidebar.header("Patient Information")
    with st.sidebar.form("patient_card"):
        age = st.number_input("Age", min_value=0, max_value=120, step=1)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        skin_type = st.selectbox("Skin Type", ["Normal", "Dry", "Oily", "Combination", "Sensitive"])
        if st.form_submit_button("Submit"):
            return f"Patient: Age {age}, Gender {gender}, Skin Type {skin_type}"
    return None

# Main App
def main():
    st.set_page_config(page_title="DermaTech", page_icon="🩺", layout="wide")
    
    header()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        disclaimer_note()
        patient_info = patient_card()
        uploaded_files, file_objects = file_upload()
    
    with col2:
        st.markdown('<div class="content-container">', unsafe_allow_html=True)
        if patient_info:
            st.info(patient_info)
        
        if uploaded_files and file_objects:
            st.success("Files uploaded successfully!")
            # Add your main content and AI analysis here
            st.write("AI analysis results will be displayed here.")
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()