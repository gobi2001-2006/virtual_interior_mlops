import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Sofa, UploadCloud, LayoutGrid, BarChart3, Compass } from 'lucide-react';

export const Navbar: React.FC = () => {
  const location = useLocation();

  const navLinks = [
    { name: 'Home', path: '/', icon: Compass },
    { name: 'Upload Room', path: '/upload', icon: UploadCloud },
    { name: 'Furniture Catalog', path: '/furniture', icon: Sofa },
    { name: '3D Designer', path: '/designer', icon: LayoutGrid },
    { name: 'MLOps Hub', path: '/mlops', icon: BarChart3 },
  ];

  return (
    <header className="sticky top-0 z-40 w-full glass-panel border-b border-warm-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand Logo */}
        <Link to="/" className="flex items-center gap-2.5 group">
          <div className="w-9 h-9 rounded-xl bg-sage-500 text-white flex items-center justify-center shadow-sm group-hover:bg-sage-600 transition-colors">
            <Sofa className="w-5 h-5" />
          </div>
          <div className="flex flex-col">
            <span className="font-semibold text-charcoal text-base tracking-tight leading-tight">
              Aura<span className="text-sage-600">Space</span>
            </span>
            <span className="text-[10px] text-charcoal-muted uppercase font-medium tracking-wider">
              MLOps Virtual Interior
            </span>
          </div>
        </Link>

        {/* Navigation Links */}
        <nav className="hidden md:flex items-center gap-1">
          {navLinks.map((link) => {
            const Icon = link.icon;
            const isActive = location.pathname === link.path;
            return (
              <Link
                key={link.path}
                to={link.path}
                className={`px-3.5 py-2 rounded-xl text-xs font-medium flex items-center gap-2 transition-all ${
                  isActive
                    ? 'bg-sage-100 text-sage-700 font-semibold shadow-xs'
                    : 'text-charcoal-muted hover:text-charcoal hover:bg-neutral-100/60'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-sage-600' : 'text-charcoal-muted'}`} />
                {link.name}
              </Link>
            );
          })}
        </nav>

        {/* Right CTA */}
        <div className="flex items-center gap-3">
          <Link
            to="/upload"
            className="px-4 py-2 bg-sage-600 text-white text-xs font-medium rounded-xl hover:bg-sage-700 transition-all shadow-sm shadow-sage-200"
          >
            Design My Room
          </Link>
        </div>
      </div>
    </header>
  );
};
