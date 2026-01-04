import { useState, useRef, useEffect } from 'react';
import { api } from '../services/api';
import './SongRecognition.css';

function SongRecognition() {
  const [recording, setRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [audioBlob, setAudioBlob] = useState(null);
  const [audioUrl, setAudioUrl] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const mediaRecorderRef = useRef(null);
  const streamRef = useRef(null);
  const timerRef = useRef(null);
  const audioPreviewRef = useRef(null);

  useEffect(() => {
    return () => {
      // Cleanup on unmount
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }
      if (audioUrl) {
        URL.revokeObjectURL(audioUrl);
      }
    };
  }, [audioUrl]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;

      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      const chunks = [];

      mediaRecorder.ondataavailable = (e) => {
        chunks.push(e.data);
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunks, { type: 'audio/webm' });
        const url = URL.createObjectURL(blob);
        setAudioBlob(blob);
        setAudioUrl(url);
        setSelectedFile(null);
      };

      mediaRecorder.start();
      setRecording(true);
      setRecordingTime(0);
      setResult(null);

      // Start timer
      timerRef.current = setInterval(() => {
        setRecordingTime((prev) => {
          const newTime = prev + 1;
          // Auto-stop at 10 seconds
          if (newTime >= 10) {
            stopRecording();
            return 10;
          }
          return newTime;
        });
      }, 1000);

      // Auto-stop at 10 seconds as backup
      setTimeout(() => {
        if (mediaRecorder.state === 'recording') {
          stopRecording();
        }
      }, 10000);
    } catch (error) {
      setResult({
        type: 'error',
        message: `Error accessing microphone: ${error.message}. Please ensure microphone permissions are granted.`,
      });
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
      setRecording(false);
      
      if (timerRef.current) {
        clearInterval(timerRef.current);
        timerRef.current = null;
      }
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      const url = URL.createObjectURL(file);
      setAudioUrl(url);
      setAudioBlob(file);
      stopRecording(); // Stop any ongoing recording
      setResult(null);
    }
  };

  const handleRecognize = async () => {
    if (!audioBlob) {
      setResult({
        type: 'error',
        message: 'Please record or upload an audio file first',
      });
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const data = await api.recognizeSong(audioBlob);
      
      if (data.status === 'success') {
        const song = data.result.song || {};
        setResult({
          type: 'success',
          message: `🎵 Song Identified: ${song.title || 'Unknown'}`,
          details: {
            songId: data.result.song_id,
            score: data.result.score,
            audioUrl: song.audio_url,
          },
        });
      } else {
        setResult({
          type: 'error',
          message: `❌ ${data.message || 'Song not found in database'}`,
          details: 'Try recording a longer clip (5-10 seconds) or ensure the song exists in the database.',
        });
      }
    } catch (error) {
      setResult({
        type: 'error',
        message: `Error: ${error.message}`,
      });
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
  };

  const hasAudio = audioBlob !== null;

  return (
    <section className="card song-recognition">
      <h2>🎤 Recognize Song</h2>
      <p className="description">Record or upload an audio clip (5-10 seconds) to identify the song</p>
      
      <div className="recording-controls">
        {!recording ? (
          <button
            type="button"
            className="btn btn-record"
            onClick={startRecording}
            disabled={loading}
          >
            🎙️ Start Recording
          </button>
        ) : (
          <button
            type="button"
            className="btn btn-stop"
            onClick={stopRecording}
          >
            ⏹️ Stop Recording
          </button>
        )}
        
        {recording && (
          <div className="timer">{formatTime(recordingTime)}</div>
        )}
      </div>

      <div className="file-upload-section">
        <label htmlFor="audio-file" className="file-label">
          <span>📁 Or Upload Audio File</span>
          <input
            type="file"
            id="audio-file"
            accept="audio/*"
            onChange={handleFileChange}
            disabled={loading || recording}
            style={{ display: 'none' }}
          />
        </label>
        {selectedFile && (
          <div className="file-name">Selected: {selectedFile.name}</div>
        )}
      </div>

      {audioUrl && (
        <audio
          ref={audioPreviewRef}
          src={audioUrl}
          controls
          className="audio-preview"
        />
      )}

      <button
        type="button"
        className="btn btn-primary"
        onClick={handleRecognize}
        disabled={!hasAudio || loading}
        style={{ display: hasAudio ? 'inline-flex' : 'none' }}
      >
        {loading ? (
          <>
            <span className="btn-loading"></span>
            Analyzing...
          </>
        ) : (
          '🔍 Recognize Song'
        )}
      </button>

      {result && (
        <div className={`result-message ${result.type}`}>
          <h3>{result.message}</h3>
          {result.details && (
            <div className="result-details">
              {typeof result.details === 'object' ? (
                <>
                  <p><strong>Song ID:</strong> {result.details.songId}</p>
                  <p><strong>Match Score:</strong> {result.details.score}</p>
                  {result.details.audioUrl && (
                    <p>
                      <strong>Audio URL:</strong>{' '}
                      <a href={result.details.audioUrl} target="_blank" rel="noopener noreferrer">
                        {result.details.audioUrl}
                      </a>
                    </p>
                  )}
                </>
              ) : (
                <p>{result.details}</p>
              )}
            </div>
          )}
        </div>
      )}
    </section>
  );
}

export default SongRecognition;

