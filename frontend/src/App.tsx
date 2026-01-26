import { useState, useCallback } from "react";
import { toast } from "sonner";
import {
  Chrome,
  Code,
  MessageSquare,
  Container,
  Music,
  Maximize2,
  Compass,
  Github,
  Figma,
  FileText,
  Mail,
  Video,
  Plus,
  X,
  TerminalSquare,
} from "lucide-react";
import { Header } from "./components/Header";
import { CategorySection, type AppItem } from "./components/CategorySection";
import { ActionBar } from "./components/ActionBar";

type InstallStatus = "idle" | "loading" | "success" | "error";

// App data organized by category
const categories: { title: string; apps: AppItem[] }[] = [
  {
    title: "Browsers",
    apps: [
      { id: "google-chrome", name: "Chrome", icon: Chrome },
      { id: "firefox", name: "Firefox", icon: Compass },
    ],
  },
  {
    title: "Dev Tools",
    apps: [
      { id: "visual-studio-code", name: "VS Code", icon: Code },
      { id: "docker", name: "Docker", icon: Container },
      { id: "github-desktop", name: "GitHub Desktop", icon: Github },
      { id: "figma", name: "Figma", icon: Figma },
    ],
  },
  {
    title: "Communication",
    apps: [
      { id: "discord", name: "Discord", icon: MessageSquare },
      { id: "slack", name: "Slack", icon: Mail },
      { id: "zoom", name: "Zoom", icon: Video },
    ],
  },
  {
    title: "Productivity",
    apps: [
      { id: "spotify", name: "Spotify", icon: Music },
      { id: "rectangle", name: "Rectangle", icon: Maximize2 },
      { id: "notion", name: "Notion", icon: FileText },
    ],
  },
];

export default function App() {
  const [selectedApps, setSelectedApps] = useState<string[]>([]);
  const [customApps, setCustomApps] = useState<string[]>([]); // New State for manual entries
  const [customInput, setCustomInput] = useState("");
  const [installStatus, setInstallStatus] = useState<InstallStatus>("idle");
  const [isConnected] = useState(true);

  // Toggle grid selection
  const toggleApp = useCallback((appId: string) => {
    setSelectedApps((prev) =>
      prev.includes(appId)
        ? prev.filter((id) => id !== appId)
        : [...prev, appId],
    );
    setInstallStatus("idle");
  }, []);

  // Handle adding custom app from input
  const addCustomApp = (e?: React.FormEvent) => {
    e?.preventDefault();
    const trimmed = customInput.trim().toLowerCase();

    if (!trimmed) return;
    if (customApps.includes(trimmed)) {
      toast.error("App already added to list");
      return;
    }
    // Prevent adding if it's already in the main grid selection (optional check)
    if (selectedApps.includes(trimmed)) {
      toast.info("This app is already selected above");
      return;
    }

    setCustomApps([...customApps, trimmed]);
    setCustomInput("");
  };

  const removeCustomApp = (appToRemove: string) => {
    setCustomApps(customApps.filter((app) => app !== appToRemove));
  };

  const handleInstall = async () => {
    // Merge both lists
    const finalPayload = [...selectedApps, ...customApps];

    if (finalPayload.length === 0) return;

    setInstallStatus("loading");

    try {
      // 🚀 The API Call with the merged payload
      const response = await fetch("http://127.0.0.1:8000/install", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ apps: finalPayload }), // Sending both grid + custom apps
      });

      if (!response.ok) {
        throw new Error("Installation request failed");
      }

      setInstallStatus("success");
      toast.success("Installation started!", {
        description: `Queued ${finalPayload.length} app${finalPayload.length > 1 ? "s" : ""} for installation.`,
      });

      // Reset after a delay
      setTimeout(() => {
        setSelectedApps([]);
        setCustomApps([]);
        setInstallStatus("idle");
      }, 3000);
    } catch (error) {
      setInstallStatus("error");
      toast.error("Connection failed", {
        description:
          "Make sure the Python backend is running on localhost:8000",
      });

      setTimeout(() => {
        setInstallStatus("idle");
      }, 2000);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="max-w-5xl mx-auto px-6 py-10 pb-40">
        <Header isConnected={isConnected} />

        {/* Existing Grid Categories */}
        {categories.map((category) => (
          <CategorySection
            key={category.title}
            title={category.title}
            apps={category.apps}
            selectedApps={selectedApps}
            onToggle={toggleApp}
          />
        ))}

        {/* --- NEW: Custom Request Section --- */}
        <section className="mt-12">
          <div className="flex items-center gap-2 mb-6">
            <TerminalSquare className="w-5 h-5 text-gray-500" />
            <h2 className="text-xl font-semibold text-gray-900">
              Custom Request
            </h2>
          </div>

          <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-sm">
            <p className="text-sm text-gray-500 mb-4">
              Can't find what you need? Type the app name below (e.g. "blender",
              "telegram", "node").
            </p>

            {/* Input Form */}
            <form onSubmit={addCustomApp} className="flex gap-3 mb-4">
              <input
                type="text"
                value={customInput}
                onChange={(e) => setCustomInput(e.target.value)}
                placeholder="Type app name..."
                className="flex-1 px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-green-500/20 focus:border-green-500 transition-all"
              />
              <button
                type="submit"
                disabled={!customInput.trim()}
                className="px-5 py-3 bg-gray-900 text-white rounded-xl font-medium hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
              >
                <Plus size={18} />
                Add
              </button>
            </form>

            {/* Custom Tags List */}
            {customApps.length > 0 && (
              <div className="flex flex-wrap gap-2 animate-in fade-in slide-in-from-top-2">
                {customApps.map((app) => (
                  <div
                    key={app}
                    className="flex items-center gap-2 px-3 py-1.5 bg-green-50 text-green-700 border border-green-200 rounded-lg text-sm font-medium"
                  >
                    <span>{app}</span>
                    <button
                      onClick={() => removeCustomApp(app)}
                      className="hover:bg-green-100 p-0.5 rounded-md transition-colors"
                    >
                      <X size={14} />
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        </section>
      </div>

      <ActionBar
        selectedCount={selectedApps.length + customApps.length} // Update count to include both
        status={installStatus}
        onInstall={handleInstall}
      />
    </div>
  );
}
