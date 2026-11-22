/**
 * Audio Controller for Ahlan AI Levantine Arabic Tutor.
 * - Plays high-definition Lebanese female voice audio (ar-LB-LaylaNeural) via HTML5 Audio.
 * - Records microphone input continuously with user-controlled Start / Stop.
 * - Real-time speech recognition and transcription preview.
 */

class AudioController {
  constructor() {
    this.audioPlayer = new Audio();
    this.mediaRecorder = null;
    this.audioChunks = [];
    this.isRecording = false;
    this.isPlaying = false;
    this.recognition = null;
    this.liveTranscript = '';
    this.recordStartTime = null;
    this.recordTimerInterval = null;

    this.onStateChange = null;
    this.onTranscriptUpdate = null;
    this.onPlaybackStateChange = null;

    this.initRecognition();
    this.initAudioPlayerEvents();
  }

  initAudioPlayerEvents() {
    this.audioPlayer.addEventListener('play', () => {
      this.isPlaying = true;
      if (this.onPlaybackStateChange) this.onPlaybackStateChange(true);
    });

    this.audioPlayer.addEventListener('ended', () => {
      this.isPlaying = false;
      if (this.onPlaybackStateChange) this.onPlaybackStateChange(false);
    });

    this.audioPlayer.addEventListener('error', (e) => {
      console.warn('Audio playback error:', e);
      this.isPlaying = false;
      if (this.onPlaybackStateChange) this.onPlaybackStateChange(false);
    });
  }

  initRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      this.recognition = new SpeechRecognition();
      this.recognition.continuous = true;
      this.recognition.interimResults = true;
      this.recognition.lang = 'ar-LB'; // Target Lebanese / Levantine Arabic

      this.recognition.onresult = (event) => {
        let text = '';
        for (let i = 0; i < event.results.length; ++i) {
          text += event.results[i][0].transcript + ' ';
        }
        this.liveTranscript = text.trim();
        if (this.onTranscriptUpdate) {
          this.onTranscriptUpdate(this.liveTranscript);
        }
      };

      this.recognition.onerror = (event) => {
        console.warn('Speech recognition event:', event.error);
      };

      this.recognition.onend = () => {
        // If user is still recording, keep recognition alive without auto-stopping!
        if (this.isRecording) {
          try {
            this.recognition.start();
          } catch (e) {}
        }
      };
    }
  }

  /**
   * Start user microphone recording (runs until user explicitly clicks Stop)
   */
  async startRecording(onTranscript, onStateChange) {
    this.onTranscriptUpdate = onTranscript;
    this.onStateChange = onStateChange;
    this.liveTranscript = '';
    this.audioChunks = [];

    // Stop any ongoing playback while speaking
    this.stopAudio();

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      this.mediaRecorder = new MediaRecorder(stream);

      this.mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          this.audioChunks.push(e.data);
        }
      };

      this.mediaRecorder.onstop = () => {
        stream.getTracks().forEach(track => track.stop());
      };

      this.mediaRecorder.start(250);
      this.isRecording = true;
      this.recordStartTime = Date.now();

      // Start recognition in parallel
      if (this.recognition) {
        try {
          this.recognition.start();
        } catch (e) {}
      }

      if (this.onStateChange) this.onStateChange(true);

    } catch (err) {
      console.error('Error accessing microphone:', err);
      // Fallback to pure SpeechRecognition if MediaRecorder stream fails
      if (this.recognition) {
        this.isRecording = true;
        try {
          this.recognition.start();
          if (this.onStateChange) this.onStateChange(true);
        } catch (e) {}
      } else {
        alert('Could not access your microphone. Please check your browser microphone permissions.');
      }
    }
  }

  /**
   * Stop recording when the user clicks 'Done Speaking'
   */
  stopRecording() {
    this.isRecording = false;

    if (this.mediaRecorder && this.mediaRecorder.state !== 'inactive') {
      this.mediaRecorder.stop();
    }

    if (this.recognition) {
      try {
        this.recognition.stop();
      } catch (e) {}
    }

    if (this.onStateChange) this.onStateChange(false);

    return this.liveTranscript;
  }

  /**
   * Play Lebanese Female Voice Audio from URL or fallback TTS
   */
  async playAudio(audioUrl, fallbackArabicText = '') {
    this.stopAudio();

    if (audioUrl) {
      try {
        this.audioPlayer.src = audioUrl;
        await this.audioPlayer.play();
        return;
      } catch (e) {
        console.warn('Audio play from URL failed, requesting dynamic TTS:', e);
      }
    }

    // Dynamic backend TTS fallback
    if (fallbackArabicText) {
      try {
        const res = await API.post('/tts', { text: fallbackArabicText });
        if (res.audio_url) {
          this.audioPlayer.src = res.audio_url;
          await this.audioPlayer.play();
          return;
        }
      } catch (err) {
        console.error('TTS endpoint error:', err);
      }

      // Browser Web Speech fallback if all else fails
      if (window.speechSynthesis) {
        const utter = new SpeechSynthesisUtterance(fallbackArabicText);
        utter.lang = 'ar-SA';
        utter.rate = 0.9;
        utter.onstart = () => {
          this.isPlaying = true;
          if (this.onPlaybackStateChange) this.onPlaybackStateChange(true);
        };
        utter.onend = () => {
          this.isPlaying = false;
          if (this.onPlaybackStateChange) this.onPlaybackStateChange(false);
        };
        window.speechSynthesis.speak(utter);
      }
    }
  }

  stopAudio() {
    if (this.audioPlayer) {
      this.audioPlayer.pause();
      this.audioPlayer.currentTime = 0;
    }
    if (window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }
    this.isPlaying = false;
    if (this.onPlaybackStateChange) this.onPlaybackStateChange(false);
  }
}

window.audioController = new AudioController();
