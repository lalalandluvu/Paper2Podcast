# How to Deploy Paper2Podcast

Since this is a Python application, it **cannot** be hosted on GitHub Pages (which only supports static websites like HTML/CSS).

The best and easiest way to host this app for free is **Streamlit Community Cloud**.

## Steps to Deploy

1.  **Sign Up / Log In**:
    *   Go to [share.streamlit.io](https://share.streamlit.io/).
    *   Sign up or log in with your **GitHub account**.

2.  **Connect Your Repository**:
    *   Click the **"New app"** button.
    *   Select "From existing repo".
    *   Choose your repository: `lalalandluvu/Paper2Podcast`.
    *   **Branch**: `main`
    *   **Main file path**: `app.py`

3.  **Deploy**:
    *   Click **"Deploy!"**.
    *   Streamlit will start building your app. This might take a few minutes as it installs the dependencies from `requirements.txt`.

4.  **Using the App**:
    *   Once deployed, you will get a public URL (e.g., `https://paper2podcast.streamlit.app`).
    *   When you open the app, you will need to enter your **OpenAI API Key** in the sidebar to make it work.

## Troubleshooting

*   **"Module not found" errors**: This usually means a package is missing from `requirements.txt`. The current file should be correct, but if you added new libraries, let me know.
*   **API Key issues**: Ensure you are pasting a valid OpenAI API key that has access to GPT-4o and TTS models.
