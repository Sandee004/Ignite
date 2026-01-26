import { Terminal } from "lucide-react";

interface HeaderProps {
  isConnected: boolean;
}

export function Header({ isConnected }: HeaderProps) {
  return (
    <header className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-6 mb-12 py-6 border-b border-gray-100">
      {/* Logo Section */}
      <div className="flex items-center gap-5">
        {/* Icon Container with Glow Effect */}
        <div className="relative group">
          {/* The Glow */}
          <div className="absolute -inset-0.5 bg-gradient-to-r from-green-500 to-emerald-500 rounded-2xl blur opacity-20 group-hover:opacity-40 transition duration-500" />

          {/* The Icon */}
          <div className="relative flex items-center justify-center w-14 h-14 rounded-xl bg-gray-900 text-white shadow-xl ring-1 ring-gray-900/5">
            <Terminal className="w-7 h-7" strokeWidth={2} />
          </div>
        </div>

        <div>
          <h1 className="text-3xl font-bold tracking-tight text-gray-900">
            Ignite
          </h1>
          <p className="text-sm font-medium text-gray-500 mt-1">
            Select your stack. Provision your machine.
          </p>
        </div>
      </div>

      {/* Status Indicator (Glass Style) */}
      <div
        className={`flex items-center gap-3 px-4 py-2 rounded-full border shadow-sm transition-colors duration-300 ${
          isConnected
            ? "bg-white border-green-100/50"
            : "bg-gray-50 border-gray-200"
        }`}
      >
        {/* The Dot Animation */}
        <span className="relative flex h-2.5 w-2.5">
          {isConnected && (
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
          )}
          <span
            className={`relative inline-flex rounded-full h-2.5 w-2.5 ${
              isConnected ? "bg-green-500" : "bg-gray-400"
            }`}
          ></span>
        </span>

        <span
          className={`text-xs font-semibold tracking-wide uppercase ${
            isConnected ? "text-green-700" : "text-gray-500"
          }`}
        >
          {isConnected ? "System Online" : "Disconnected"}
        </span>
      </div>
    </header>
  );
}
