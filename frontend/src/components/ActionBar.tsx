import { Loader2, Rocket, CheckCircle2 } from "lucide-react";

type InstallStatus = "idle" | "loading" | "success" | "error";

interface ActionBarProps {
  selectedCount: number;
  status: InstallStatus;
  onInstall: () => void;
}

export function ActionBar({
  selectedCount,
  status,
  onInstall,
}: ActionBarProps) {
  const isDisabled =
    selectedCount === 0 || status === "loading" || status === "success";

  return (
    <div
      className={`fixed bottom-6 left-1/2 -translate-x-1/2 z-50 bg-white/90 backdrop-blur-md rounded-full border border-gray-200 shadow-2xl px-4 py-3 flex items-center gap-4 transition-all duration-300 ease-out ${
        selectedCount > 0
          ? "opacity-100 translate-y-0"
          : "opacity-0 translate-y-4 pointer-events-none"
      }`}
    >
      {/* Summary */}
      <div className="flex items-center gap-2 px-3">
        <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
        <span className="text-sm font-medium text-gray-900 whitespace-nowrap">
          {selectedCount} app{selectedCount !== 1 ? "s" : ""} selected
        </span>
      </div>

      {/* Divider */}
      <div className="w-px h-8 bg-gray-200" />

      {/* Install Button */}
      <button
        onClick={onInstall}
        disabled={isDisabled}
        className={`flex items-center justify-center gap-2 px-6 py-2.5 rounded-full font-semibold text-sm transition-all duration-200 ease-out focus:outline-none focus-visible:ring-2 focus-visible:ring-green-500 focus-visible:ring-offset-2 disabled:cursor-not-allowed min-w-[160px] ${
          status === "success"
            ? "bg-green-500 text-white"
            : status === "error"
              ? "bg-red-500 text-white"
              : "bg-gray-900 text-white hover:bg-gray-800 active:scale-[0.98]"
        } ${isDisabled && status !== "success" ? "opacity-50" : ""}`}
      >
        {status === "loading" ? (
          <>
            <Loader2 className="w-4 h-4 animate-spin" />
            <span>Igniting...</span>
          </>
        ) : status === "success" ? (
          <>
            <CheckCircle2 className="w-4 h-4" />
            <span>Started</span>
          </>
        ) : (
          <>
            <Rocket className="w-4 h-4" />
            <span>Install Now</span>
          </>
        )}
      </button>
    </div>
  );
}
