import clsx from "clsx"
import type { Message } from "@/lib/chat"
import { TypingDots } from "@/components/typingDots"

export interface ChatHistoryProps {
  messages: Message[];
  className?: string;
}

export function ChatHistory({ messages, className }: ChatHistoryProps) {
  return (
    <div className={className}>
      {messages.map(({ sender, content, loading }, index) =>
        <div
          key={index}
          className={clsx(
            "mb-6 py-2 px-5 text-base rounded-3xl w-fit max-w-[80%] font-[family-name:var(--font-geist-sans)]",
            sender === "user" ? "bg-blue-600 ml-auto" : "bg-neutral-800"
          )}
        >
          {
            !loading &&
            <p>
              {content}
            </p>
          }
          {
            loading &&
            <TypingDots className="my-2" />
          }
        </div>
      )}
    </div>
  );
}