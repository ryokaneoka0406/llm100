"use client";
import React, { useState, useRef } from "react";

export default function Home() {
  const [recording, setRecording] = useState<boolean>(false);
  const [audioURL, setAudioURL] = useState<string>("");
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [transcription, setTranscription] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;

      mediaRecorder.ondataavailable = (e: BlobEvent) => {
        const audioBlob = new Blob([e.data], { type: "audio/wav" });
        setAudioBlob(audioBlob);
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

  const sendAudio = async () => {
    setLoading(true);
    if (!audioBlob) return;

    const formData = new FormData();
    formData.append("audio", audioBlob, "audio.wav");

    try {
      const response = await fetch("http://127.0.0.1:8000/transcribe/", {
        method: "POST",
        body: formData,
      });
      const responseData = await response.json();
      setTranscription(responseData.transcription);
      setLoading(false);
    } catch (error) {
      console.error("Error in sending audio:", error);
    }
  };

  return (
    <div className="flex justify-center mt-10">
      <div className="container shadow rounded-md p-6 font-sans max-w-sm sm:max-w-xl bg-white">
        <h1 className="text-2xl text-gray-600 mb-3">Browser recording app</h1>
        <h2 className="text-gray-500 text-xl">Record your voice</h2>
        <div className="my-4 flex flex-col max-w-xs mx-auto">
          {recording ? (
            <button
              className="px-5
                  py-3
                  mb-4
                  rounded
                  focus:outline-none focus:ring focus:ring-offset-2
                  tracking-wider
                  font-semibold
                  text-sm
                  sm:text-base;
                  bg-blue-600
                  hover:bg-blue-800
                  focus:ring-blue-800 focus:ring-opacity-50
                  active:bg-bule-800
                  text-white"
              onClick={stopRecording}
            >
              Stop recording
            </button>
          ) : (
            <button
              className="px-5
                  py-3
                  mb-4
                  rounded
                  focus:outline-none focus:ring focus:ring-offset-2
                  tracking-wider
                  font-semibold
                  text-sm
                  sm:text-base;
                  bg-blue-600
                  hover:bg-blue-800
                  focus:ring-blue-800 focus:ring-opacity-50
                  active:bg-bule-800
                  text-white"
              onClick={startRecording}
            >
              Start recording
            </button>
          )}
          {audioURL && <audio src={audioURL} controls />}
        </div>
        <h2 className="text-gray-500 text-xl">Get transcription</h2>
        <div className="my-4 flex flex-col max-w-xs mx-auto">
          {audioURL && !recording && !loading ? (
            <button
              className="px-5
                  py-3
                  mb-4
                  rounded
                  focus:outline-none focus:ring focus:ring-offset-2
                  tracking-wider
                  font-semibold
                  text-sm
                  sm:text-base;
                  bg-blue-600
                  hover:bg-blue-800
                  focus:ring-blue-800 focus:ring-opacity-50
                  active:bg-bule-800
                  text-white"
              onClick={sendAudio}
            >
              Transcribe
            </button>
          ) : (
            <button
              disabled
              className="px-5
                  py-3
                  mb-4
                  rounded
                  focus:outline-none focus:ring focus:ring-offset-2
                  tracking-wider
                  font-semibold
                  text-sm
                  sm:text-base;
                  bg-gray-600
                  active:bg-bule-800
                  text-white"
              onClick={stopRecording}
            >
              Transcribe
            </button>
          )}
          {transcription && <p>{transcription}</p>}
        </div>
      </div>
    </div>
  );
}
