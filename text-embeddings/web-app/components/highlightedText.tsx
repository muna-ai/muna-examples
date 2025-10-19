import clsx from "clsx"
import { useEffect, useRef, Fragment, type MutableRefObject } from "react"

export interface HighlightedTextProps {
  children: string;
  highlight?: string;
  scrollRef?: MutableRefObject<HTMLDivElement>;
  className?: string;
}

export function HighlightedText({ children, highlight, scrollRef, className }: HighlightedTextProps) {
  // Scroll to highlight
  const highlightRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (highlightRef.current && scrollRef.current)
      scrollRef.current.scrollTo({
        top: highlightRef.current.offsetTop,
        behavior: "smooth"
      });
  }, [highlight, scrollRef]);
  // Render block as is
  if (!highlight)
    return (
      <pre className={clsx("whitespace-pre-wrap", className)}>
        {children}
      </pre>
    );
  // Render highlighted lines
  const escapedSubText = highlight.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const regex = new RegExp(`(${escapedSubText})`, "gi");
  return (
    <pre className={clsx("whitespace-pre-wrap", className)}>
      {children.split(/\n/g).map((line, index) =>
        <Fragment key={index}>
          {line.split(regex).map((part, i) =>
            regex.test(part) ? (
              <span
                key={i}
                ref={highlightRef}
                className="bg-pink-600/90 rounded-sm py-0.5 px-1"
              >
                {part}
              </span>
            ) :
            part
          )}
          <br />
        </Fragment>
      )}
    </pre>
  );
}