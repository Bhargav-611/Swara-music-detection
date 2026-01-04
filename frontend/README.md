# Audio Fingerprinting Frontend

A modern React + Vite frontend for the Shazam-like Audio Fingerprinting API.

## Features

1. **YouTube Song Upload**: Add songs to the database by providing a YouTube URL
2. **Audio Recognition**: Record or upload audio clips (5-10 seconds) to identify songs

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- Backend API running on `http://localhost:8000`

### Installation

Dependencies should already be installed. If not:

```bash
npm install
```

### Development

1. Make sure your backend API is running:
   ```bash
   cd ../backend
   uvicorn api:app --reload
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

3. Open your browser to the URL shown in the terminal (usually `http://localhost:5173`)

### Configuration

If your backend API is running on a different URL or port, update the `API_BASE_URL` constant in `src/services/api.js`:

```javascript
const API_BASE_URL = 'http://localhost:8000'; // Change this to your API URL
```

### Build for Production

```bash
npm run build
```

The built files will be in the `dist` folder.

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── YouTubeUpload.jsx      # YouTube URL upload component
│   │   ├── YouTubeUpload.css
│   │   ├── SongRecognition.jsx    # Audio recording/recognition component
│   │   └── SongRecognition.css
│   ├── services/
│   │   └── api.js                 # API service functions
│   ├── App.jsx                    # Main app component
│   ├── App.css                    # Main app styles
│   ├── index.css                  # Global styles
│   └── main.jsx                   # Entry point
├── index.html
└── package.json
```

## Usage

### Adding Songs from YouTube

1. Paste a YouTube URL in the input field
2. Click "Upload Song"
3. The song will be processed in the background and added to the database

### Recognizing Songs

1. **Recording Option**:
   - Click "Start Recording"
   - Allow microphone access when prompted
   - Record for 5-10 seconds (auto-stops at 10 seconds)
   - Click "Stop Recording" (or wait for auto-stop)
   - Click "Recognize Song"

2. **File Upload Option**:
   - Click "Or Upload Audio File"
   - Select an audio file from your device
   - Click "Recognize Song"

### Results

- **Success**: Shows song title, ID, match score, and audio URL
- **Not Found**: Indicates the song is not in the database (try adding it first via YouTube)

## Browser Compatibility

- Chrome/Edge: Full support
- Firefox: Full support
- Safari: Full support (may require HTTPS for microphone access)
- Mobile browsers: Responsive design works, but microphone access may vary

## Notes

- Microphone access requires user permission
- Audio recordings are stored temporarily in memory and sent to the backend
- The backend handles temporary file storage and cleanup
- For production, update CORS settings in `backend/api.py` to use specific origins instead of `*`
