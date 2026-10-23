import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Navbar } from './components/Navbar';
import { Footer } from './components/Footer';
import { HomePage } from './pages/HomePage';
import { UploadPage } from './pages/UploadPage';
import { AnalysisResultPage } from './pages/AnalysisResultPage';
import { FurnitureCatalogPage } from './pages/FurnitureCatalogPage';
import { DesignerPage } from './pages/DesignerPage';
import { MLOpsDashboardPage } from './pages/MLOpsDashboardPage';

export const App: React.FC = () => {
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      <main className="flex-1">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/upload" element={<UploadPage />} />
          <Route path="/analysis/:roomId" element={<AnalysisResultPage />} />
          <Route path="/furniture" element={<FurnitureCatalogPage />} />
          <Route path="/catalog" element={<FurnitureCatalogPage />} />
          <Route path="/designer" element={<DesignerPage />} />
          <Route path="/mlops" element={<MLOpsDashboardPage />} />
        </Routes>
      </main>
      <Footer />
    </div>
  );
};

export default App;
