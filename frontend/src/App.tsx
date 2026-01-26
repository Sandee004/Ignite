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
import { InstallationModal } from "./components/InstallationModal";

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
  const [customApps, setCustomApps] = useState<string[]>([]);
  const [customInput, setCustomInput] = useState("");
  const [installStatus, setInstallStatus] = useState<InstallStatus>("idle");
  const [isConnected] = useState(true);
  const [showProgress, setShowProgress] = useState(false);

  const toggleApp = useCallback((appId: string) => {
    setSelectedApps((prev) =>
      prev.includes(appId)
        ? prev.filter((id) => id !== appId)
        : [...prev, appId],
    );
    setInstallStatus("idle");
  }, []);

  const addCustomApp = (e?: React.FormEvent) => {
    e?.preventDefault();
    const trimmed = customInput.trim().toLowerCase();

    if (!trimmed) return;
    if (customApps.includes(trimmed)) {
      toast.error("App already added to list");
      return;
    }
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
    const finalPayload = [...selectedApps, ...customApps];
    if (finalPayload.length === 0) return;

    setInstallStatus("loading");

    try {
      const response = await fetch("http://127.0.0.1:8000/install", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ apps: finalPayload }),
      });

      setShowProgress(true);

      if (!response.ok) {
        throw new Error("Installation request failed");
      }

      setInstallStatus("success");

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
    <div className="relative min-h-screen bg-slate-50 overflow-hidden font-sans text-slate-900 selection:bg-green-100 selection:text-green-900">
      {/* 🎨 BACKGROUND EFFECTS */}
      <div className="fixed inset-0 z-0 pointer-events-none">
        {/* Top Right Green Glow */}
        <div className="absolute top-[-10%] right-[-5%] w-[500px] h-[500px] rounded-full bg-green-200/40 blur-[120px] mix-blend-multiply opacity-70 animate-pulse-slow" />

        {/* Bottom Left Teal Glow */}
        <div className="absolute bottom-[-10%] left-[-10%] w-[600px] h-[600px] rounded-full bg-emerald-100/60 blur-[100px] mix-blend-multiply opacity-60" />

        {/* Subtle Grid Pattern Overlay */}
        <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 brightness-100 contrast-150" />
      </div>

      {/* MAIN CONTENT (Relative z-10 puts it above the background) */}
      <div className="relative z-10 max-w-5xl mx-auto px-6 py-10 pb-40">
        <Header isConnected={isConnected} />

        {categories.map((category) => (
          <CategorySection
            key={category.title}
            title={category.title}
            apps={category.apps}
            selectedApps={selectedApps}
            onToggle={toggleApp}
          />
        ))}

        {/* Custom Request Section */}
        <section className="mt-16">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-white rounded-lg shadow-sm border border-slate-100">
              <TerminalSquare className="w-5 h-5 text-slate-700" />
            </div>
            <h2 className="text-xl font-bold text-slate-900 tracking-tight">
              Custom Request
            </h2>
          </div>

          <div className="bg-white/80 backdrop-blur-xl rounded-2xl border border-white/50 shadow-xl shadow-slate-200/40 p-6 ring-1 ring-slate-900/5 transition-all hover:shadow-2xl hover:shadow-slate-200/50">
            <p className="text-sm text-slate-500 mb-5 font-medium">
              Can't find what you need? Type the app name below (e.g. "blender",
              "telegram", "node").
            </p>

            <form onSubmit={addCustomApp} className="flex gap-3 mb-4">
              <input
                type="text"
                value={customInput}
                onChange={(e) => setCustomInput(e.target.value)}
                placeholder="Type app name..."
                className="flex-1 px-5 py-3.5 rounded-xl bg-slate-50 border-2 border-transparent focus:bg-white focus:border-green-500/50 focus:ring-4 focus:ring-green-500/10 outline-none transition-all placeholder:text-slate-400 font-medium text-slate-700"
              />
              <button
                type="submit"
                disabled={!customInput.trim()}
                className="px-6 py-3 bg-slate-900 text-white rounded-xl font-semibold hover:bg-slate-800 disabled:opacity-50 disabled:cursor-not-allowed transition-all active:scale-95 flex items-center gap-2 shadow-lg shadow-slate-900/20"
              >
                <Plus size={18} />
                Add
              </button>
            </form>

            {customApps.length > 0 && (
              <div className="flex flex-wrap gap-2 animate-in fade-in slide-in-from-top-2 pt-2">
                {customApps.map((app) => (
                  <div
                    key={app}
                    className="flex items-center gap-2 px-3 py-1.5 bg-green-50 text-green-700 border border-green-200/60 rounded-lg text-sm font-semibold shadow-sm"
                  >
                    <span>{app}</span>
                    <button
                      onClick={() => removeCustomApp(app)}
                      className="hover:bg-green-100 p-0.5 rounded-md transition-colors text-green-600/70 hover:text-green-700"
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
        selectedCount={selectedApps.length + customApps.length}
        status={installStatus}
        onInstall={handleInstall}
      />

      <InstallationModal
        isOpen={showProgress}
        onClose={() => {
          setShowProgress(false);
          setSelectedApps([]);
          setCustomApps([]);
        }}
      />
    </div>
  );
}
