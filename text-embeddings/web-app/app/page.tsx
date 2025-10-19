"use client"

import { Muna, type Embedding } from "muna"
import { useCallback, useEffect, useMemo, useRef, useState } from "react"
import { findClosestEmbedding, splitDocument } from "@/lib/ai"
import type { Message } from "@/lib/chat"
import { Dropzone } from "@/components/dropzone"
import { Footer } from "@/components/footer"
import { Header } from "@/components/header"
import { ChatBox } from "@/components/chatBox"
import { ChatHistory } from "@/components/chatHistory"
import { HighlightedText } from "@/components/highlightedText"
import { Toolbar } from "@/components/toolbar"
import { ScrollArea } from "@/components/ui/scroll-area"

const openai = new Muna({ url: "/api/muna" }).beta.openai;
const EMBEDDING_MODEL = "@google/embedding-gemma";

export default function Home() {
  // State
  const [document, setDocument] = useState<string>(INITIAL_DOCUMENT);
  const [messages, setMessages] = useState<Message[]>([]);
  const documentRef = useRef<HTMLDivElement>(null);
  const messagesRef = useRef<HTMLDivElement>(null);
  const vectorDatabaseRef = useRef<Embedding[] | null>(null);
  const chunks = useMemo(() => document ? splitDocument({ document }) : [], [document]);
  const highlight = useMemo(
    () => messages.findLast(({ sender, loading }) => sender === "assistant" && !loading)?.content,
    [messages]
  );
  const ensureVectorDatabase = useCallback(async (): Promise<Embedding[]> => {
    if (vectorDatabaseRef.current)
      return vectorDatabaseRef.current;
    const documentEmbedding = await openai.embeddings.create({
      model: EMBEDDING_MODEL,
      input: chunks
    });
    vectorDatabaseRef.current = documentEmbedding.data;
    return documentEmbedding.data;
  }, [chunks]);
  // Message handler
  const onMessage = useCallback(async (message: string) => {
    // Add message
    setMessages(prev => [
      ...prev,
      { sender: "user", content: message },
      { sender: "assistant", loading: true }
    ]);
    // Populate vector database if not populated
    const database = await ensureVectorDatabase();
    // Embed the query
    const { data: [query] } = await openai.embeddings.create({
      model: EMBEDDING_MODEL,
      input: message
    });
    // Query our vector database
    const result = findClosestEmbedding({ query, database });
    // Respond
    setMessages(prev => [
      ...prev.slice(0, -1),
      { sender: "assistant", content: chunks[result.index] }
    ]);
  }, [chunks, ensureVectorDatabase]);
  useEffect(() => {
    vectorDatabaseRef.current = null;
  }, [chunks]);
  // Scroll to end on new message
  useEffect(() => {
    const scrollableDiv = messagesRef.current;
    if (scrollableDiv)
      scrollableDiv.scrollTo({ top: scrollableDiv.scrollHeight, behavior: "smooth" });
  }, [messages]);
  // Render
  return (
    <div className="h-screen flex flex-col bg-black font-[family-name:var(--font-geist-mono)] divide-y divide-gray-200/20 divide-dashed">
      
      {/* Header */}
      <Header />

      {/* Toolbar */}
      <Toolbar
        onClear={() => {
          setDocument(null);
          setMessages([]);
          vectorDatabaseRef.current = null;
        }}
        className="px-8 py-1"
      />

      {/* App */}
      <main className="flex-1 relative">
        <div className="absolute inset-0 flex text-white divide-x divide-gray-200/20 divide-dashed">

          {/* Left side - File upload and display */}
          <div className="w-1/2 p-8">
            {
              !document &&
              <Dropzone
                onUpload={setDocument}
                className="h-full border border-dashed border-gray-200/20"
              />
            }
            {
              document &&
              <ScrollArea className="h-full">
                <HighlightedText highlight={highlight} scrollRef={documentRef} className="text-lg">
                  {document}
                </HighlightedText>
              </ScrollArea>
            }
          </div>

          {/* Right side - Chat interface */}
          <div className="w-1/2 p-8 flex flex-col">

            {/* Chat history */}
            <ScrollArea ref={messagesRef} className="flex-grow mb-4">
              <ChatHistory messages={messages} />
            </ScrollArea>

            {/* Chat box */}
            <ChatBox
              placeholder="What are Ava's hobbies?"
              onMessage={onMessage}
              disabled={!document}
            />
          </div>

        </div>
      </main>
      
      {/* Footer */}
      <Footer className="" />
    </div>
  );
}

const INITIAL_DOCUMENT = `
Here’s a list of 10 random facts about a hypothetical person named Ava Ramirez.

Birthplace: Ava was born in Buenos Aires, Argentina, but moved to Toronto, Canada when she was 7 years old.

Career: She works as a UX researcher for a health-tech startup focused on mental wellness.

Hidden talent: She can solve a Rubik’s Cube in under a minute and has been known to do it blindfolded after memorizing the cube’s state.

Hobbies: Ava practices aerial silks and takes improv comedy classes every Thursday night.

Favorite book: Sapiens by Yuval Noah Harari — she’s read it three times and keeps a copy full of sticky notes and highlights.

Tech quirk: She uses a custom-built split mechanical keyboard and refuses to type on anything else.

Pets: She has a rescue cat named Pixel, who has one blue eye and one green eye.

Languages: Ava speaks fluent Spanish, English, and conversational Japanese.

Phobia: She has an irrational fear of escalators after getting her shoelace caught in one as a kid.

Fun fact: During the pandemic, Ava started baking sourdough and now runs a small online store that sells bread-making kits to beginners.
`.trim();
