import clsx from "clsx"
import Image from "next/image"
import Link from "next/link"

export interface HeaderProps {
  className?: string;
}

export function Header({ className }: HeaderProps) {
  return (
    <header className={clsx("relative flex flex-row justify-center text-4xl py-6", className)}>
      <Link href="https://muna.ai" target="_blank" className="w-14 h-14 absolute top-0 left-0 ml-8 mt-4">
        <Image
          src="https://www.muna.ai/logo_1024.png"
          fill
          alt="Muna logo"
          className=""
        />
      </Link>
      <p>
        Retrieval with Embeddings
      </p>
    </header>
  );
}