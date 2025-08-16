interface AnalysisSectionProps {
  title: string;
  children: React.ReactNode;
}

export default function AnalysisSection({ title, children }: AnalysisSectionProps) {
  return (
    <div className="mb-12">
      <h2 className="text-2xl font-semibold mb-6 pb-2 border-b border-notion-border">
        {title}
      </h2>
      <div className="space-y-4">
        {children}
      </div>
    </div>
  );
}