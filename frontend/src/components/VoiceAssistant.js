import { useEffect } from "react";
import SpeechRecognition, {
  useSpeechRecognition,
} from "react-speech-recognition";

/**
 * Component to handle voice-to-text processing using the browser's Web Speech API
 * @param {Function} onUserMessage - Callback function to process the final transcript
 */
const VoiceAssistant = ({ onUserMessage }) => {
  // Destructuring tools from the hook to manage listening state and text transcripts
  const {
    transcript,
    listening,
    resetTranscript,
    browserSupportsSpeechRecognition,
  } = useSpeechRecognition();

  useEffect(() => {
    // When the user stops talking, capture the final transcript
    if (!listening && transcript.trim().length > 0) {
      onUserMessage(transcript.trim()); // Pass text to the main state machine in Home.js
      resetTranscript(); // Clear the buffer for the next sentence
    }
  }, [listening, transcript, onUserMessage, resetTranscript]);

  // Compatibility check for older browsers or non-supported environments
  if (!browserSupportsSpeechRecognition) {
    return <span>Browser doesn't support speech recognition.</span>;
  }

  /**
   * Toggles the microphone state. Configured for en-IN to better recognize Indian accents.
   */
  const handleMicClick = () => {
    if (listening) {
      SpeechRecognition.stopListening();
    } else {
      SpeechRecognition.startListening({ language: "en-IN" });
    }
  };

  return (
    <div className="voice-ui" style={{ textAlign: "center", margin: "20px 0" }}>
      {/* The pulse-active class is toggled via CSS based on the listening state for the visual appearance */}
      <button
        className={`btn-talk ${listening ? "pulse-active" : ""}`}
        onClick={handleMicClick}
        style={{
          transition: "all 0.3s ease",
          outline: "none",
          minWidth: "160px",
        }}
      >
        {listening ? "Listening..." : "Push to Talk"}
      </button>

      {/* Dynamic status indicators showing the user if the mic is currently being used or not */}
      <p
        className="status"
        style={{
          marginTop: "10px",
          fontSize: "0.9rem",
          color: listening ? "#2ecc71" : "#7f8c8d",
        }}
      >
        <span
          className={`status-dot ${listening ? "status-listening" : "status-off"}`}
        ></span>
        {listening ? "Microphone is Active" : "Click to start speaking"}
      </p>

      {/* Real-time transcript preview: This provides visual confirmation as the user speaks */}
      {transcript && (
        <div
          style={{ marginTop: "15px", fontStyle: "italic", color: "#34495e" }}
        >
          <p className="preview">"{transcript}"</p>
        </div>
      )}
    </div>
  );
};

export default VoiceAssistant;
