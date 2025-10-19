import clsx from "clsx"
import { useCallback } from "react"
import { useDropzone } from "react-dropzone"

export interface DropzoneProps {
  onUpload: (document: string) => void;
  className?: string;
}

export function Dropzone({ onUpload, className }: DropzoneProps) {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    const reader = new FileReader();
    reader.onload = e => {
      const document = e.target?.result as string;
      const cleanedDocument = document.replace(/([^\n])\n([^\n])/g, "$1 $2");
      onUpload(cleanedDocument);
    }
    reader.readAsText(file);
  }, []);
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "text/plain": [".txt"] },
    multiple: false,
  });
  return (
    <div
      {...getRootProps()}
      className={clsx(
        "rounded-lg flex items-center justify-center cursor-pointer",
        className,
      )}
    >
      <input {...getInputProps()} />
      {
        isDragActive &&
        <p className="text-lg">
          Drop the file here...
        </p>
      }
      {
        !isDragActive &&
        <p className="text-lg text-gray-400 text-center">
          Drop text (.txt) file here.
          <br />
          Or click to select a file.
        </p>
      }
    </div>
  );
}