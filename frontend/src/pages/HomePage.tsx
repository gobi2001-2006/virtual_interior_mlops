import React from 'react';
import { Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { api } from '../services/api';
import {
  UploadCloud,
  Layers,
  Sparkles,
  BarChart3,
  ArrowRight,
  CheckCircle2,
  ShieldAlert,
  Move3d,
  Sofa
} from 'lucide-react';

export const HomePage: React.FC = () => {
  const { data: mlopsStatus } = useQuery({
    queryKey: ['mlops-status'],
    queryFn: api.getMLOpsStatus,
  });

  const { data: recentRooms } = useQuery({
    queryKey: ['recent-rooms'],
    queryFn: api.getRooms,
  });

  const steps = [
    {
      num: '01',
      title: 'Room Photograph Upload',
      desc: 'Upload an interior photo with dimension and style preferences.',
      icon: UploadCloud,
    },
    {
      num: '02',
      title: 'Transfer Learning Classifier',
      desc: 'MobileNetV3-Small classifies room typology with confidence scoring.',
      icon: Sparkles,
    },
    {
      num: '03',
      title: 'Deterministic Layout Engine',
      desc: 'Generates explainable furniture placement respecting clearances.',
      icon: Layers,
    },
    {
      num: '04',
      title: 'Interactive 3D Workspace',
      desc: 'Arrange, rotate, and resize virtual furniture in real room coordinates.',
      icon: Move3d,
    },
    {
      num: '05',
      title: 'Governed MLOps Retraining',
      desc: 'User feedback feeds an approved validation pipeline for model retraining.',
      icon: BarChart3,
    },
  ];

  return (
    <div className="space-y-16 pb-16">
      {/* Hero Section */}
      <section className="relative pt-12 md:pt-20 max-w-5xl mx-auto text-center px-4">
        {/* Model status pill */}
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-sage-50 border border-sage-200/60 text-xs font-medium text-sage-700 mb-6 shadow-xs">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>
            Active Model: <strong>{mlopsStatus?.active_model_version || 'v001-demo-fallback'}</strong>
          </span>
          <span className="text-sage-400">•</span>
          <span>{mlopsStatus?.is_trained_model_loaded ? 'Trained Weights Loaded' : 'Honest Demo Fallback'}</span>
        </div>

        <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold tracking-tight text-charcoal leading-tight">
          Spatial Interior Design,{' '}
          <span className="text-sage-600 block mt-1">Engineered with MLOps.</span>
        </h1>

        <p className="mt-6 text-base sm:text-lg text-charcoal-muted max-w-2xl mx-auto leading-relaxed">
          Transform ordinary room photographs into interactive 3D layouts using vision transfer learning,
          explainable spatial ergonomics, and a feedback retraining lifecycle.
        </p>

        <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-3">
          <Link
            to="/upload"
            className="w-full sm:w-auto px-6 py-3.5 bg-sage-600 hover:bg-sage-700 text-white font-medium rounded-xl shadow-md shadow-sage-200 transition-all flex items-center justify-center gap-2 group text-sm"
          >
            Design My Room
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </Link>
          <Link
            to="/furniture"
            className="w-full sm:w-auto px-6 py-3.5 bg-white hover:bg-neutral-50 text-charcoal font-medium rounded-xl border border-warm-border shadow-xs transition-all flex items-center justify-center gap-2 text-sm"
          >
            <Sofa className="w-4 h-4 text-sage-600" />
            Explore Furniture
          </Link>
          <Link
            to="/mlops"
            className="w-full sm:w-auto px-6 py-3.5 bg-white hover:bg-neutral-50 text-charcoal-muted font-medium rounded-xl border border-warm-border shadow-xs transition-all flex items-center justify-center gap-2 text-sm"
          >
            <BarChart3 className="w-4 h-4" />
            MLOps Hub
          </Link>
        </div>
      </section>

      {/* Workflow Steps */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-10">
          <h2 className="text-xs font-semibold text-sage-600 uppercase tracking-widest">
            End-to-End System
          </h2>
          <p className="mt-1 text-2xl font-bold text-charcoal">
            How The Architecture Works
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
          {steps.map((s) => {
            const Icon = s.icon;
            return (
              <div
                key={s.num}
                className="bg-white p-5 rounded-2xl border border-warm-border card-hover flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between mb-4">
                    <span className="text-xs font-bold text-sage-600 tracking-wider">
                      {s.num}
                    </span>
                    <div className="w-8 h-8 rounded-lg bg-sage-50 text-sage-600 flex items-center justify-center">
                      <Icon className="w-4 h-4" />
                    </div>
                  </div>
                  <h3 className="font-semibold text-sm text-charcoal mb-1.5">{s.title}</h3>
                  <p className="text-xs text-charcoal-muted leading-relaxed">{s.desc}</p>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* Live System Operational Status */}
      <section className="max-w-5xl mx-auto px-4">
        <div className="bg-warm-cream p-6 sm:p-8 rounded-2xl border border-warm-border">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-6">
            <div>
              <h3 className="text-base font-bold text-charcoal">
                Pipeline Telemetry & Governance Status
              </h3>
              <p className="text-xs text-charcoal-muted mt-0.5">
                Real-time values synchronized with PostgreSQL and Inference Service
              </p>
            </div>
            <Link
              to="/mlops"
              className="text-xs font-semibold text-sage-700 hover:text-sage-800 flex items-center gap-1"
            >
              Open Full MLOps Dashboard <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div className="bg-white p-4 rounded-xl border border-warm-border">
              <span className="text-[11px] font-medium text-charcoal-muted uppercase">Room Analyses</span>
              <p className="text-2xl font-bold text-charcoal mt-1">
                {mlopsStatus?.total_room_analyses ?? 0}
              </p>
            </div>
            <div className="bg-white p-4 rounded-xl border border-warm-border">
              <span className="text-[11px] font-medium text-charcoal-muted uppercase">Saved Layouts</span>
              <p className="text-2xl font-bold text-charcoal mt-1">
                {mlopsStatus?.total_saved_designs ?? 0}
              </p>
            </div>
            <div className="bg-white p-4 rounded-xl border border-warm-border">
              <span className="text-[11px] font-medium text-charcoal-muted uppercase">Feedback Records</span>
              <p className="text-2xl font-bold text-charcoal mt-1">
                {mlopsStatus?.total_feedback_records ?? 0}
              </p>
            </div>
            <div className="bg-white p-4 rounded-xl border border-warm-border">
              <span className="text-[11px] font-medium text-charcoal-muted uppercase">Approved For Retrain</span>
              <p className="text-2xl font-bold text-charcoal mt-1 text-sage-700">
                {mlopsStatus?.approved_feedback_samples ?? 0} / {mlopsStatus?.min_approved_samples_required ?? 10}
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Recent Designs (if any) */}
      {recentRooms && recentRooms.length > 0 && (
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-lg font-bold text-charcoal">Recent Room Analyses</h2>
              <p className="text-xs text-charcoal-muted">Rooms classified and configured in this session</p>
            </div>
            <Link to="/upload" className="text-xs font-semibold text-sage-700 hover:underline">
              Analyze Another Room
            </Link>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {recentRooms.slice(0, 3).map((r) => (
              <div key={r.id} className="bg-white rounded-2xl border border-warm-border overflow-hidden card-hover">
                <div className="h-44 bg-neutral-100 overflow-hidden relative">
                  <img
                    src={`http://localhost:8000${r.image_path}`}
                    alt={r.name}
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      (e.target as any).src = 'https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=600&q=80';
                    }}
                  />
                  <div className="absolute top-3 right-3 bg-white/90 backdrop-blur-xs text-[11px] font-semibold px-2.5 py-1 rounded-full shadow-xs">
                    {r.latest_prediction?.predicted_room_type || 'Room'}
                  </div>
                </div>
                <div className="p-4">
                  <h4 className="font-semibold text-sm text-charcoal">{r.name}</h4>
                  <p className="text-xs text-charcoal-muted mt-1">
                    {r.width_m}m × {r.length_m}m • {r.style_preference} • {r.budget_preference}
                  </p>
                  <div className="mt-4 pt-3 border-t border-warm-border flex items-center justify-between">
                    <span className="text-[11px] text-charcoal-muted">
                      Confidence: {((r.latest_prediction?.confidence || 0.65) * 100).toFixed(0)}%
                    </span>
                    <Link
                      to={`/designer?roomId=${r.id}`}
                      className="text-xs font-semibold text-sage-600 hover:text-sage-700"
                    >
                      Open in 3D →
                    </Link>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
};
