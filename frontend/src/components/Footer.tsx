import React from 'react';
import { Sofa, ShieldCheck, Cpu } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="w-full bg-white border-t border-warm-border mt-auto py-10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-2.5">
            <div className="w-7 h-7 rounded-lg bg-sage-500 text-white flex items-center justify-center">
              <Sofa className="w-4 h-4" />
            </div>
            <span className="font-semibold text-sm text-charcoal">
              AuraSpace Interior MLOps
            </span>
          </div>

          <div className="flex items-center gap-6 text-xs text-charcoal-muted">
            <div className="flex items-center gap-1.5">
              <Cpu className="w-3.5 h-3.5 text-sage-600" />
              <span>MobileNetV3-Small Classification</span>
            </div>
            <div className="flex items-center gap-1.5">
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
              <span>Feedback Loop & Model Governance</span>
            </div>
          </div>

          <p className="text-xs text-charcoal-muted">
            © 2026 AuraSpace. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};
