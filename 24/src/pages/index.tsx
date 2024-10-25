"use client";
import React, { useCallback, useEffect, useState } from "react";
import { WavRecorder, WavStreamPlayer } from "../lib/wavtools/index.js";
import { RealtimeClient } from "@openai/realtime-api-beta";
import { ItemType } from "@openai/realtime-api-beta/dist/lib/client";

export default function Home() {
  const client = new RealtimeClient({
    apiKey: "YOUR_API_KEY",
    dangerouslyAllowAPIKeyInBrowser: true,
  });

  const wavRecorder = new WavRecorder({ sampleRate: 24000 });
  const wavStreamPlayer = new WavStreamPlayer({ sampleRate: 24000 });

  const [isConnected, setIsConnected] = useState(false);
  const [items, setItems] = useState<ItemType[]>([]);
  const [name, setName] = useState<String>("");
  const [job, setJob] = useState<String>("");
  const [hobby, setHobby] = useState<String>("");
  const [food, setFood] = useState<String>("");
  const [movie, setMovie] = useState<String>("");

  const connectConversation = useCallback(async () => {
    setIsConnected(true);
    setItems(client.conversation.getItems());

    await wavRecorder.begin();

    await wavStreamPlayer.connect();

    await client.connect();

    client.sendUserMessageContent([
      {
        type: `input_text`,
        text: `Please greet and start the interview.`,
      },
    ]);

    if (client.getTurnDetectionType() === "server_vad") {
      await wavRecorder.record((data) => client.appendInputAudio(data.mono));
    }
  }, []);

  const disconnectConversation = useCallback(async () => {
    setIsConnected(false);
    setItems([]);

    client.disconnect();

    await wavRecorder.end();

    await wavStreamPlayer.interrupt();
  }, []);

  /**
   * Core RealtimeClient and audio capture setup
   * Set all of our instructions, tools, events and more
   */
  useEffect(() => {
    // Set instructions
    client.updateSession({
      instructions: `You are an experienced researcher.
You will now conduct an interview with the user.
# Purpose of the interview
To understand the user's persona

# Interview questions
1. Please tell me your name.
2. What is your occupation?
3. What are your hobbies?
4. What is your favorite food?
5. What is your favorite movie?

# Interview guidelines
- Please ask one topic at a time.
- If the user starts talking about something else, continue asking questions about that topic and skillfully bring the conversation back.
- After obtaining answers to all the questions, please tell the user "The interview is now complete. Thank you for your time."
`,
    });
    // Set transcription, otherwise we don't get user transcriptions back
    client.updateSession({ input_audio_transcription: { model: "whisper-1" } });
    // ユーザーが話終えたことをサーバー側で判断する'server_vad'に設定。（'manual'モードもある）
    client.updateSession({ turn_detection: { type: "server_vad" } });

    client.addTool(
      {
        name: "get_name",
        description:
          "Record the interviewee’s name. Call this function when the interviewee states their name.",
        parameters: {
          type: "object",
          properties: {
            name: {
              type: "string",
              description:
                "The name of the interviewee.(e.g., 'John', 'Alice')",
            },
          },
          required: ["name"],
        },
      },
      async ({ name }: { name: string }) => {
        console.log("Function was called");
        setName(name);
        return { name };
      }
    );
    client.addTool(
      {
        name: "get_job",
        description:
          "Record the interviewee’s job. Call this function when the interviewee states their job.",
        parameters: {
          type: "object",
          properties: {
            job: {
              type: "string",
              description:
                "The job of the interviewee.(e.g., 'engineer', 'doctor')",
            },
          },
          required: ["job"],
        },
      },
      async ({ job }: { job: string }) => {
        console.log("Function was called");
        setJob(job);
        return { job };
      }
    );
    client.addTool(
      {
        name: "get_hobby",
        description:
          "Record the interviewee’s hobby. Call this function when the interviewee states their hobby.",
        parameters: {
          type: "object",
          properties: {
            hobby: {
              type: "string",
              description:
                "The hobby of the interviewee.(e.g., 'reading', 'cooking')",
            },
          },
          required: ["hobby"],
        },
      },
      async ({ hobby }: { hobby: string }) => {
        console.log("Function was called");
        setHobby(hobby);
        return { hobby };
      }
    );
    client.addTool(
      {
        name: "get_food",
        description:
          "Record the interviewee’s food. Call this function when the interviewee states their food.",
        parameters: {
          type: "object",
          properties: {
            food: {
              type: "string",
              description:
                "The favorite food of the interviewee.(e.g., 'sushi', 'pizza')",
            },
          },
          required: ["food"],
        },
      },
      async ({ food }: { food: string }) => {
        console.log("Function was called");
        setFood(food);
        return { food };
      }
    );
    client.addTool(
      {
        name: "get_movie",
        description: "Retrieves the favorite movie of the user.",
        parameters: {
          type: "object",
          properties: {
            movie: {
              type: "string",
              description: "The favorite movie of the user.",
            },
          },
          required: ["movie"],
        },
      },
      async ({ movie }: { movie: string }) => {
        console.log("Function was called");
        setMovie(movie);
        return { movie };
      }
    );

    // 不要
    client.on("error", (event: any) => console.error(event));

    // 必要
    client.on("conversation.interrupted", async () => {
      console.log("interrupted");
      const trackSampleOffset = await wavStreamPlayer.interrupt();
      if (trackSampleOffset?.trackId) {
        const { trackId, offset } = trackSampleOffset;
        await client.cancelResponse(trackId, offset);
      }
    });

    // 必要
    client.on("conversation.updated", async ({ item, delta }: any) => {
      console.log("convesation.updated");
      const items = client.conversation.getItems();
      console.log("items", items);
      if (delta?.audio) {
        wavStreamPlayer.add16BitPCM(delta.audio, item.id);
      }
      if (item.status === "completed" && item.formatted.audio?.length) {
        const wavFile = await WavRecorder.decode(
          item.formatted.audio,
          24000,
          24000
        );
        item.formatted.file = wavFile;
      }
      setItems(items);
    });

    setItems(client.conversation.getItems());

    return () => {
      // cleanup; resets to defaults
      client.reset();
    };
  }, []);
  return (
    <div className="flex justify-center mt-10">
      <div className="container shadow rounded-md p-6 font-sans max-w-sm sm:max-w-xl bg-white">
        <h1 className="text-2xl text-gray-600 mb-3">Interviewer App</h1>
        <div className="my-4 flex flex-col max-w-xs mx-auto">
          <div className="pb-4">
            <ol>
              <li>Name: {name}</li>
              <li>Occupation: {job}</li>
              <li>Hobby: {hobby}</li>
              <li>Favorite food: {food}</li>
              <li>Favorite movie: {movie}</li>
            </ol>
          </div>

          {isConnected ? (
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
              onClick={disconnectConversation}
            >
              Stop
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
              onClick={connectConversation}
            >
              Start
            </button>
          )}
          <ol>
            {items.map((item) => {
              return (
                <li>
                  {item.role} : {JSON.stringify(item.formatted.transcript)}
                </li>
              );
            })}
          </ol>
        </div>
      </div>
    </div>
  );
}
