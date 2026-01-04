import { useState } from 'react';
import { api } from '../services/api';
import './YouTubeUpload.css';

function YouTubeUpload() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const isValidYouTubeUrl = (url) => {
    const pattern = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+/;
    return pattern.test(url);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!url.trim()) {
      setResult({ type: 'error', message: 'Please enter a YouTube URL' });
      return;
    }

    if (!isValidYouTubeUrl(url)) {
      setResult({ type: 'error', message: 'Please enter a valid YouTube URL' });
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      console.log('Starting YouTube upload for URL:', url);
      const data = await api.uploadYouTube(url);
      console.log('Upload successful, response:', data);
      setResult({
        type: 'success',
        message: data.message || 'Song processing started in background',
        details: 'The song is being processed and will be added to the database shortly.',
      });
      setUrl('');
    } catch (error) {
      console.error('Upload failed:', error);
      setResult({
        type: 'error',
        message: error.message || 'Failed to upload song',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="card youtube-upload">
      <h2>📺 Add Song from YouTube</h2>
      <p className="description">Enter a YouTube URL to add the song to the database</p>
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="youtube-url">YouTube URL:</label>
          <input
            type="url"
            id="youtube-url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://www.youtube.com/watch?v=..."
            required
            disabled={loading}
          />
        </div>
        
        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? (
            <>
              <span className="btn-loading"></span>
              Processing...
            </>
          ) : (
            'Upload Song'
          )}
        </button>
      </form>
      
      {result && (
        <div className={`result-message ${result.type}`}>
          <h3>{result.type === 'success' ? '✅' : '❌'} {result.message}</h3>
          {result.details && <p>{result.details}</p>}
        </div>
      )}
    </section>
  );
}

export default YouTubeUpload;

