import clsx from "clsx"

// Credits: https://codepen.io/itsmanojb/pen/xQpZbR

export interface TypingDotsProps {
  className?: string;
}

export function TypingDots({ className }: TypingDotsProps) {
  return (
    <div className={clsx("flex gap-x-2", className)}>
      <span className="dot w-2 h-2 bg-neutral-500"></span>
      <span className="dot w-2 h-2 bg-neutral-500"></span>
      <span className="dot w-2 h-2 bg-neutral-500"></span>
    </div>
  )
}