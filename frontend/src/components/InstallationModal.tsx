import { useEffect, useState } from "react";
import {
  Loader2,
  CheckCircle2,
  XCircle,
  Terminal,
  AlertCircle,
} from "lucide-react";

interface InstallationModalProps {
  isOpen: boolean;
  onClose: () => void;
}

// 1. Update Types to match Backend
interface FailedApp {
  name: string;
  reason: string;
}

interface ProgressState {
  status: "idle" | "running" | "completed" | "error";
  queue: string[];
  current_app: string | null;
  completed: string[];
  failed: FailedApp[]; // Changed from string[] to object[]
}

export function InstallationModal({ isOpen, onClose }: InstallationModalProps) {
  const [progress, setProgress] = useState<ProgressState | null>(null);

  useEffect(() => {
    if (!isOpen) return;
    const interval = setInterval(async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/progress");
        const data = await res.json();
        setProgress(data);
      } catch (e) {
        console.error("Polling error", e);
      }
    }, 1000);
    return () => clearInterval(interval);
  }, [isOpen]);

  if (!isOpen || !progress) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-2xl border border-gray-100 overflow-hidden animate-in zoom-in-95 duration-200">
        {/* Header */}
        <div className="bg-gray-50 px-6 py-4 border-b border-gray-100 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div
              className={`p-2 rounded-lg ${progress.status === "completed" ? "bg-green-100" : "bg-gray-200"}`}
            >
              {progress.status === "running" ? (
                <Loader2 className="animate-spin w-5 h-5 text-gray-700" />
              ) : (
                <Terminal className="w-5 h-5 text-gray-700" />
              )}
            </div>
            <div>
              <h3 className="font-semibold text-gray-900">
                {progress.status === "completed"
                  ? "Setup Complete"
                  : "Provisioning..."}
              </h3>
              <p className="text-xs text-gray-500">
                {progress.status === "completed"
                  ? "Your machine is ready."
                  : "Do not close this window."}
              </p>
            </div>
          </div>
        </div>

        {/* The List */}
        <div className="p-6 space-y-3 max-h-[60vh] overflow-y-auto">
          {progress.queue.map((appName) => {
            const isCompleted = progress.completed.includes(appName);
            // Check if this app is in the failed list (by matching name)
            const failureData = progress.failed.find((f) => f.name === appName);
            const isFailed = !!failureData;
            const isCurrent = progress.current_app === appName;
            const isPending = !isCompleted && !isFailed && !isCurrent;

            return (
              <div
                key={appName}
                className={`flex flex-col p-3 rounded-xl transition-all duration-300 ${
                  isCurrent
                    ? "bg-green-50 border border-green-100 scale-[1.02] shadow-sm"
                    : isFailed
                      ? "bg-red-50 border border-red-100"
                      : "bg-transparent"
                }`}
              >
                <div className="flex items-center justify-between w-full">
                  <div className="flex items-center gap-3">
                    {isCompleted && (
                      <CheckCircle2 className="w-5 h-5 text-green-500" />
                    )}
                    {isFailed && <XCircle className="w-5 h-5 text-red-500" />}
                    {isCurrent && (
                      <Loader2 className="w-5 h-5 text-green-600 animate-spin" />
                    )}
                    {isPending && (
                      <div className="w-5 h-5 rounded-full border-2 border-gray-200" />
                    )}

                    <span
                      className={`font-medium capitalize ${
                        isCurrent
                          ? "text-green-900"
                          : isCompleted
                            ? "text-gray-500 line-through decoration-green-500/50"
                            : isFailed
                              ? "text-red-700"
                              : "text-gray-700"
                      }`}
                    >
                      {appName}
                    </span>
                  </div>

                  {isCurrent && (
                    <span className="text-xs font-semibold text-green-600 animate-pulse">
                      Installing...
                    </span>
                  )}
                </div>

                {/* ERROR REASON (The new part) */}
                {isFailed && (
                  <div className="ml-8 mt-1 flex items-start gap-1.5">
                    <AlertCircle className="w-3 h-3 text-red-500 mt-0.5 shrink-0" />
                    <p className="text-xs text-red-600 font-medium leading-tight">
                      {failureData.reason}
                    </p>
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* Footer */}
        <div className="px-6 py-4 bg-gray-50 border-t border-gray-100 flex justify-end">
          <button
            onClick={onClose}
            disabled={progress.status === "running"}
            className={`px-6 py-2 rounded-lg font-medium text-sm transition-all ${
              progress.status === "running"
                ? "bg-gray-200 text-gray-400 cursor-not-allowed"
                : "bg-gray-900 text-white hover:bg-gray-800 shadow-lg hover:shadow-xl"
            }`}
          >
            {progress.status === "running" ? "Wait to finish..." : "Done"}
          </button>
        </div>
      </div>
    </div>
  );
}
