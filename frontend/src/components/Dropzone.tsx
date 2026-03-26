import { UploadCloud } from "lucide-react";
import { useRef } from "react";

interface DropzoneProps {
  fileName: string | null;
  disabled?: boolean;
  onFileSelected: (file: File) => void;
}

export function Dropzone({ fileName, disabled, onFileSelected }: DropzoneProps) {
  const inputRef = useRef<HTMLInputElement | null>(null);

  return (
    <div
      className="rounded-[1.75rem] border border-dashed border-pine/30 bg-white/80 p-8 text-center shadow-panel"
      onDragOver={(event) => event.preventDefault()}
      onDrop={(event) => {
        event.preventDefault();
        const file = event.dataTransfer.files?.[0];
        if (file && !disabled) {
          onFileSelected(file);
        }
      }}
    >
      <UploadCloud className="mx-auto h-12 w-12 text-pine" />
      <h2 className="mt-4 font-display text-2xl">Drop a PDF or DOCX resume</h2>
      <p className="mt-2 text-sm text-ink/70">
        ATS Forge extracts text, scores job alignment, and prepares a cleaner version for download.
      </p>
      <button
        className="mt-6 rounded-full bg-ink px-5 py-3 font-semibold text-white transition hover:bg-pine disabled:cursor-not-allowed disabled:opacity-60"
        disabled={disabled}
        onClick={() => inputRef.current?.click()}
        type="button"
      >
        Choose File
      </button>
      <input
        ref={inputRef}
        accept=".pdf,.docx"
        className="hidden"
        onChange={(event) => {
          const file = event.target.files?.[0];
          if (file) {
            onFileSelected(file);
          }
        }}
        type="file"
      />
      {fileName ? <p className="mt-4 text-sm font-semibold text-pine">Selected: {fileName}</p> : null}
    </div>
  );
}
