import streamlit as st
from streamlit_survey_main.streamlit_survey import StreamlitSurvey
import pandas as pd
import random

participant_videos = pd.read_csv('participant_videos_random_order.csv')

if "seed" not in st.session_state:
    st.session_state["seed"] = random.randint(1,1000)

participant_videos = participant_videos.sample(n=31, random_state=st.session_state["seed"]) 

survey = StreamlitSurvey()

with survey.pages(31) as page:

    if page.current == 0:
       st.title("User Study :notes: :video_camera:")
       st.markdown("<h5> Instructions</h5>", unsafe_allow_html=True)
       st.markdown("<p><b>Please make sure your computer sound is on for this study</b> and that you are in a quiet environment. <b>Please use headphones</b> to ensure you hear the audio properly (please avoid laptop/phone speakers).</p><p> This form contains 30 questions. Each question includes two videos with sound, labeled 1 and 2. The videos contain the same still image, but the sound in each video is different. For each question, please listen to both videos and <b>select the video in which the sound is a better match for the image in the video and press submit</b>. For example, if the image in the video is of a cow, and video 1 has the sound of a cow moo and video 2 has the sound of cat meowing, you should select video 1. It’s possible for both videos to have sounds that are relevant (or irrelevant) to the image, in this case please select the video with the sound you feel is the best match for the image. Thank you for your time! </p>", unsafe_allow_html=True)
       st.markdown(":warning: :red[At the end of the survey, please be sure to **export your survey data** using the instructions on the final page. Thank you for participating!]")

    elif page.current > 0 and page.current < 30:
        first_video = participant_videos.iloc[page.current].first_video_path
        second_video = participant_videos.iloc[page.current].second_video_path
    
        first_video_file = open(first_video, 'rb')
        first_video_bytes = first_video_file.read()
        second_video_file = open(second_video, 'rb')
        second_video_bytes = second_video_file.read()
        col1, col2 = st.columns(2)

        col1.header('Video 1')
        col1.video(first_video_bytes)
        col2.header('Video 2')
        col2.video(second_video_bytes)

        st.markdown("**Which video has a sound that better matches the image?**")
        result = survey.selectbox("Use the dropdown below:", options=["----", "Video 1", "Video 2"],
                id=f"RESP_{page.current}_VID1={participant_videos.iloc[page.current].first_video_uid}_VID2={participant_videos.iloc[page.current].second_video_uid}")

        if result == '----':
            st.warning("Select 'Video 1' or 'Video 2' from the dropdown above.")

    elif page.current == 30:
        first_video = participant_videos.iloc[page.current].first_video_path
        second_video = participant_videos.iloc[page.current].second_video_path
    
        first_video_file = open(first_video, 'rb')
        first_video_bytes = first_video_file.read()
        second_video_file = open(second_video, 'rb')
        second_video_bytes = second_video_file.read()
        col1, col2 = st.columns(2)

        col1.header('Video 1')
        col1.video(first_video_bytes)
        col2.header('Video 2')
        col2.video(second_video_bytes)

        st.markdown("**Which video has a sound that better matches the image?**")
        result = survey.selectbox("Use the dropdown below:", options=["----", "Video 1", "Video 2"],
                id=f"RESP_{page.current}_VID1={participant_videos.iloc[page.current].first_video_uid}_VID2={participant_videos.iloc[page.current].second_video_uid}")

        if result == '----':
            st.warning("Select 'Video 1' or 'Video 2' from the dropdown above.")

        st.markdown(":warning: :red[Please make your final selection above and then **export your survey data** using the button below. Finally, email your results (found in 'sound_user_survey_results.json' to jwilkins@adobe.com. Thank you for participating!]")

        """#### Export survey data"""
        survey.download_button("Export Survey Data", file_name='sound_user_survey_results.json', use_container_width=True)
