import { AppCard } from "./AppCard";
import type { LucideIcon } from "lucide-react";

export interface AppItem {
  id: string;
  name: string;
  icon: LucideIcon;
}

interface CategorySectionProps {
  title: string;
  apps: AppItem[];
  selectedApps: string[];
  onToggle: (id: string) => void;
}

export function CategorySection({
  title,
  apps,
  selectedApps,
  onToggle,
}: CategorySectionProps) {
  return (
    <section className="mb-10">
      <h2 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-4 px-1">
        {title}
      </h2>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {apps.map((app) => (
          <AppCard
            key={app.id}
            id={app.id}
            name={app.name}
            icon={app.icon}
            isSelected={selectedApps.includes(app.id)}
            onToggle={onToggle}
          />
        ))}
      </div>
    </section>
  );
}
