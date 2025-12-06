# Voice Selection Feature Walkthrough

I have successfully added the ability to select different voices for the Host and Guest in the Paper2Podcast application.

## Changes Implemented

### 1. UI Updates (`app.py`)
- Added a **"Voice Selection"** section to the sidebar.
- Added **"Host Voice"** and **"Guest Voice"** dropdown menus.
- The available voices are:
    - **Alloy** (Female)
    - **Echo** (Male)
    - **Fable** (Male)
    - **Onyx** (Male)
    - **Nova** (Female)
    - **Shimmer** (Female)

### 2. Dynamic Host Naming (`app.py` & `agents.py`)
- The system now automatically assigns a gender-appropriate name to the Host based on the selected voice.
    - **Female Voices** (Alloy, Nova, Shimmer) -> Sarah, Emma, Chloe, Olivia, or Ava.
    - **Male Voices** (Echo, Fable, Onyx) -> Mike, David, James, Robert, or John.
- This name is passed to the AI agents so the script reflects the correct persona.

### 3. Audio Generation (`audio_utils.py`)
- The audio generation engine now uses the specific OpenAI voice IDs selected in the UI for the corresponding speaker segments.

## How to Use

1.  Open the application.
2.  In the sidebar, look for the **"Voice Selection"** section.
3.  Choose your preferred **Host Voice** and **Guest Voice**.
4.  Upload your PDF and click **"Generate Podcast"**.
5.  The generated script will use a name matching your Host's voice, and the final audio will use the selected voices.

## Verification
- The application starts successfully.
- The voice selection dropdowns appear in the sidebar.
- The backend logic correctly maps the selection to the audio generation API.

### 4. AI Album Art Generator (`image_utils.py` & `app.py`)
- Added **"Google API Key"** input in the sidebar.
- Implemented **Imagen 3** integration to generate unique cover art for each episode.
- The system generates an artistic prompt based on the paper's title and uses it to create the image.
- The generated image is displayed above the audio player.


