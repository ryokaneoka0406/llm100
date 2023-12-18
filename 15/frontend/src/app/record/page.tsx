"use client";
import React, { useState, useRef } from "react";

const Page: React.FC = () => {
  const [recording, setRecording] = useState<boolean>(false);
  const [audioURL, setAudioURL] = useState<string>("");
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;

      mediaRecorder.ondataavailable = (e: BlobEvent) => {
        const audioBlob = new Blob([e.data], { type: "audio/wav" });
        const audioURL = URL.createObjectURL(audioBlob);
        setAudioURL(audioURL);
      };

      mediaRecorder.start();
      setRecording(true);
    } catch (err) {
      console.error("Error in starting recording:", err);
    }
  };

  const stopRecording = () => {
    mediaRecorderRef.current?.stop();
    setRecording(false);
  };

  return (
    <div>
      <h1>ブラウザでの録音</h1>
      {recording ? (
        <button onClick={stopRecording}>録音停止</button>
      ) : (
        <button onClick={startRecording}>録音開始</button>
      )}
      {audioURL && <audio src={audioURL} controls />}
    </div>
  );
};

export default Page;
