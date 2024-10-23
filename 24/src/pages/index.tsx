"use client";
import React, { useCallback, useEffect, useState } from "react";
import { WavRecorder, WavStreamPlayer } from "../lib/wavtools/index.js";
import { RealtimeClient } from "@openai/realtime-api-beta";
import { ItemType } from "@openai/realtime-api-beta/dist/lib/client";

export default function Home() {
  const client = new RealtimeClient({
    apiKey: "Your API Key",
    dangerouslyAllowAPIKeyInBrowser: true,
  });

  const wavRecorder = new WavRecorder({ sampleRate: 24000 });
  const wavStreamPlayer = new WavStreamPlayer({ sampleRate: 24000 });

  const [isConnected, setIsConnected] = useState(false);
  const [items, setItems] = useState<ItemType[]>([]);

  const connectConversation = useCallback(async () => {
    setIsConnected(true);
    setItems(client.conversation.getItems());

    await wavRecorder.begin();

    await wavStreamPlayer.connect();

    await client.connect();

    client.sendUserMessageContent([
      {
        type: `input_text`,
        text: `Hello!`,
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
      instructions: "あなたは役にたつAIアシスタントです",
    });
    // Set transcription, otherwise we don't get user transcriptions back
    client.updateSession({ input_audio_transcription: { model: "whisper-1" } });
    // ユーザーが話終えたことをサーバー側で判断する'server_vad'に設定。（'manual'モードもある）
    client.updateSession({ turn_detection: { type: "server_vad" } });

    client.addTool(
      {
        name: "get_time",
        description: "Retrieves the current date and time.",
        parameters: {
          type: "object",
          properties: {
            timezone: {
              type: "string",
              description:
                "The timezone for which to retrieve the current time (e.g., 'UTC', 'Asia/Tokyo').",
            },
          },
          required: ["timezone"],
        },
      },
      async ({ timezone }: { timezone: string }) => {
        console.log("関数が呼ばれました");
        const currentTime = new Date().toLocaleString("en-US", {
          timeZone: timezone,
        });
        return { currentTime };
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
        <h1 className="text-2xl text-gray-600 mb-3">Realtime API App</h1>
        <div className="my-4 flex flex-col max-w-xs mx-auto">
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
              停止
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
              開始
            </button>
          )}
          <div>
            {items.map((item) => {
              return (
                <>
                  <div>
                    {item.role} : {JSON.stringify(item.formatted.transcript)}
                  </div>
                </>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
