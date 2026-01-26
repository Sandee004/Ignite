import { Check } from "lucide-react";
import type { LucideIcon } from "lucide-react";

interface AppCardProps {
  id: string;
  name: string;
  icon: LucideIcon;
  isSelected: boolean;
  onToggle: (id: string) => void;
}

export function AppCard({
  id,
  name,
  icon: Icon,
  isSelected,
  onToggle,
}: AppCardProps) {
  return (
    <button
      onClick={() => onToggle(id)}
      className={`group relative flex flex-col items-center justify-center gap-3 p-6 rounded-2xl border-2 transition-all duration-200 ease-out hover:shadow-lg hover:scale-[1.02] active:scale-[0.98] focus:outline-none focus-visible:ring-2 focus-visible:ring-green-500 focus-visible:ring-offset-2 min-h-[140px] ${
        isSelected
          ? "border-green-500 bg-green-50 shadow-md"
          : "border-gray-200 bg-white hover:border-gray-300"
      }`}
    >
      {/* Check badge */}
      {isSelected && (
        <div className="absolute top-3 right-3 flex items-center justify-center w-6 h-6 rounded-full bg-green-500 animate-in zoom-in duration-200">
          <Check className="w-4 h-4 text-white" strokeWidth={3} />
        </div>
      )}

      {/* Icon */}
      <div
        className={`flex items-center justify-center w-14 h-14 rounded-xl transition-colors duration-200 ${
          isSelected ? "text-green-600" : "text-gray-900"
        }`}
      >
        <Icon className="w-10 h-10" strokeWidth={1.5} />
      </div>

      {/* Name */}
      <span
        className={`text-sm font-medium transition-colors duration-200 ${
          isSelected ? "text-green-700" : "text-gray-600"
        }`}
      >
        {name}
      </span>
    </button>
  );
}
