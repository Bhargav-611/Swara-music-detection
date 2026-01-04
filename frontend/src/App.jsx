import './App.css';
import YouTubeUpload from './components/YouTubeUpload';
import SongRecognition from './components/SongRecognition';

function App() {
  return (
    <div className="app">
      <header>
        <h1>🎵 Audio Fingerprinting System</h1>
        <p className="subtitle">Upload YouTube songs or recognize music from audio recordings</p>
      </header>

      <main>
        <YouTubeUpload />
        <SongRecognition />
      </main>
    </div>
  );
}

export default App;
