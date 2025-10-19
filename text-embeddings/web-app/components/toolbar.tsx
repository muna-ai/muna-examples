import clsx from "clsx"
import { XMarkIcon } from "@heroicons/react/24/solid"
import { Button } from "@/components/ui/button"

export interface ToolbarProps {
  onClear?: () => void;
  className?: string;
}

export function Toolbar({ onClear, className }: ToolbarProps) {
  return (
    <div className={clsx("flex flex-row items-center min-h-12", className)}>
      {/* Clear button */}
      <div>
        {
          onClear &&
          <Button
            onClick={onClear}
            className="bg-transparent text-gray-400 text-sm transition hover:bg-neutral-800/50 disabled:bg-neutral-700"
          >
            <XMarkIcon className="w-4 h-auto mr-2" />
            Clear
          </Button>
        }
      </div>
    </div>
  );
}