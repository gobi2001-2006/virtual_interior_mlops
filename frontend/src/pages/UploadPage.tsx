import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { RoomPredictResult } from '../types';
import { formatRoomTypeLabel } from '../utils/formatters';
import {
  UploadCloud,
  Image as ImageIcon,
  X,
  Sparkles,
  AlertCircle,
  Maximize2,
  Check,
  Palette,
  DollarSign,
  Loader2,
  CheckCircle2
} from 'lucide-react';

export const UploadPage: React.FC = () => {
  const navigate = useNavigate();
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  // AI Prediction state
  const [isPredicting, setIsPredicting] = useState(false);
  const [predictionResult, setPredictionResult] = useState<RoomPredictResult | null>(null);

  // Form parameters
  const [roomName, setRoomName] = useState('My Living Room');
  const [roomTypePref, setRoomTypePref] = useState('');
  const [stylePreference, setStylePreference] = useState('Scandinavian');
  const [budgetPreference, setBudgetPreference] = useState('medium');
  const [widthM, setWidthM] = useState(4.2);
  const [lengthM, setLengthM] = useState(5.0);
  const [heightM, setHeightM] = useState(2.8);

  const supportedStyles = [
    'modern',
    'minimalist',
    'traditional',
    'Scandinavian',
    'industrial',
    'contemporary'
  ];

  const handleFile = async (file: File) => {
    setErrorMsg(null);
    const validExtensions = ['image/jpeg', 'image/png', 'image/webp'];
    if (!validExtensions.includes(file.type)) {
      setErrorMsg('Invalid file format. Please upload a JPEG, PNG, or WebP image.');
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      setErrorMsg('File exceeds 10MB limit. Please select a smaller photo.');
      return;
    }

    setSelectedFile(file);
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);

    // Run direct vision prediction
    setIsPredicting(true);
    try {
      const pred = await api.predictRoomImage(file);
      setPredictionResult(pred);
      setRoomTypePref(pred.predicted_room);
      setRoomName(`My ${formatRoomTypeLabel(pred.predicted_room)}`);
    } catch (err: any) {
      console.warn('Real-time prediction notice:', err);
      // Prediction error does not block form submission; will be handled gracefully
    } finally {
      setIsPredicting(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const removeImage = () => {
    setSelectedFile(null);
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    setPreviewUrl(null);
    setPredictionResult(null);
    setRoomTypePref('');
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedFile) {
      setErrorMsg('Please select or drop an image photograph of your room.');
      return;
    }

    setIsLoading(true);
    setErrorMsg(null);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('name', roomName);
      if (roomTypePref) formData.append('room_type_preference', roomTypePref);
      formData.append('style_preference', stylePreference);
      formData.append('budget_preference', budgetPreference);
      formData.append('width_m', widthM.toString());
      formData.append('length_m', lengthM.toString());
      formData.append('height_m', heightM.toString());

      const createdRoom = await api.analyzeRoom(formData);
      navigate(`/analysis/${createdRoom.id}`, { state: { room: createdRoom } });
    } catch (err: any) {
      setErrorMsg(err.message || 'Failed to analyze room photograph. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="text-center mb-8">
        <h1 className="text-2xl sm:text-3xl font-bold text-charcoal">
          Upload Room Photograph
        </h1>
        <p className="text-sm text-charcoal-muted mt-1.5 max-w-xl mx-auto">
          Send your room image to our MobileNetV3-Small vision pipeline to classify room typology
          and compute deterministic furniture recommendations.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-8">
        {/* Error Alert */}
        {errorMsg && (
          <div className="p-4 rounded-xl bg-red-50 border border-red-200 text-red-700 text-xs flex items-center gap-2.5">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{errorMsg}</span>
          </div>
        )}

        {/* Upload Drop Zone / Preview */}
        <div className="bg-white p-6 rounded-2xl border border-warm-border shadow-xs">
          {!previewUrl ? (
            <div
              onDrop={handleDrop}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onClick={() => fileInputRef.current?.click()}
              className={`border-2 border-dashed rounded-2xl p-10 text-center cursor-pointer transition-all ${
                isDragging
                  ? 'border-sage-500 bg-sage-50/50 scale-[0.99]'
                  : 'border-warm-border hover:border-sage-400 bg-neutral-50/50'
              }`}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept="image/jpeg,image/png,image/webp"
                className="hidden"
                onChange={(e) => {
                  if (e.target.files && e.target.files[0]) {
                    handleFile(e.target.files[0]);
                  }
                }}
              />
              <div className="w-14 h-14 rounded-2xl bg-sage-100 text-sage-600 flex items-center justify-center mx-auto mb-4">
                <UploadCloud className="w-7 h-7" />
              </div>
              <h3 className="font-semibold text-sm text-charcoal">
                Drop your room photograph here, or <span className="text-sage-600 underline">browse</span>
              </h3>
              <p className="text-xs text-charcoal-muted mt-1">
                Supports JPEG, PNG, and WebP (Max 10MB)
              </p>
            </div>
          ) : (
            <div className="relative rounded-2xl overflow-hidden border border-warm-border bg-neutral-900 group">
              <img
                src={previewUrl}
                alt="Room Preview"
                className="w-full h-80 object-cover opacity-95 group-hover:opacity-100 transition-opacity"
              />
              <div className="absolute top-4 right-4 flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => fileInputRef.current?.click()}
                  className="px-3 py-1.5 bg-black/60 hover:bg-black/80 backdrop-blur-xs text-white text-xs font-medium rounded-xl shadow-xs transition-colors"
                >
                  Replace
                </button>
                <button
                  type="button"
                  onClick={removeImage}
                  className="p-1.5 bg-red-600/80 hover:bg-red-700 backdrop-blur-xs text-white rounded-xl shadow-xs transition-colors"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
              <div className="absolute bottom-4 left-4 bg-black/60 backdrop-blur-xs text-white text-xs px-3 py-1 rounded-lg">
                {selectedFile?.name} ({(selectedFile?.size! / (1024 * 1024)).toFixed(2)} MB)
              </div>
            </div>
          )}

          {/* AI Vision Classification Result / Spinner */}
          {isPredicting && (
            <div className="mt-4 p-4 rounded-xl bg-sage-50 border border-sage-200 text-sage-900 text-xs flex items-center gap-3">
              <Loader2 className="w-5 h-5 text-sage-600 animate-spin shrink-0" />
              <div>
                <span className="font-semibold block">Analyzing Room Typology...</span>
                <span className="text-[11px] text-sage-700">
                  Running MobileNetV3-Small vision pipeline (v003) on CPU...
                </span>
              </div>
            </div>
          )}

          {predictionResult && !isPredicting && (
            <div className="mt-4 p-5 rounded-2xl bg-neutral-50 border border-warm-border space-y-4">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <div className="flex items-center gap-2.5">
                  <div className="w-8 h-8 rounded-xl bg-sage-100 text-sage-700 flex items-center justify-center">
                    <Sparkles className="w-4 h-4" />
                  </div>
                  <div>
                    <span className="text-[10px] font-semibold text-charcoal-muted uppercase tracking-wider block">
                      AI Detected Typology • Model {predictionResult.model_version}
                    </span>
                    <span className="text-base font-bold text-charcoal">
                      {formatRoomTypeLabel(predictionResult.predicted_room)}
                    </span>
                  </div>
                </div>

                <div className="text-right">
                  <span className="px-3 py-1 bg-sage-100 text-sage-800 font-semibold text-xs rounded-full inline-block">
                    {(predictionResult.confidence * 100).toFixed(1)}% Confidence
                  </span>
                  {predictionResult.latency_ms && (
                    <span className="block text-[10px] text-charcoal-muted mt-0.5">
                      Latency: {predictionResult.latency_ms} ms
                    </span>
                  )}
                </div>
              </div>

              {/* All Six Class Probabilities */}
              <div className="space-y-1.5 pt-3 border-t border-warm-border">
                <span className="text-[11px] font-semibold text-charcoal block mb-1">
                  Class Probabilities Breakdown:
                </span>
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                  {Object.entries(predictionResult.probabilities).map(([cls, prob]) => {
                    const isSelected = cls === predictionResult.predicted_room;
                    return (
                      <div
                        key={cls}
                        className={`p-2 rounded-xl text-xs flex flex-col justify-between border ${
                          isSelected
                            ? 'bg-sage-100/70 border-sage-300 font-medium'
                            : 'bg-white border-warm-border text-charcoal-light'
                        }`}
                      >
                        <div className="flex items-center justify-between">
                          <span className="truncate">{formatRoomTypeLabel(cls)}</span>
                          <span className="font-semibold ml-1">{(prob * 100).toFixed(1)}%</span>
                        </div>
                        <div className="w-full h-1 bg-neutral-200 rounded-full mt-1.5 overflow-hidden">
                          <div
                            className={`h-full ${isSelected ? 'bg-sage-600' : 'bg-charcoal-muted/30'}`}
                            style={{ width: `${Math.min(100, prob * 100)}%` }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Room Specifications & Preferences */}
        <div className="bg-white p-6 rounded-2xl border border-warm-border shadow-xs space-y-6">
          <h2 className="text-base font-bold text-charcoal flex items-center gap-2">
            <Maximize2 className="w-4 h-4 text-sage-600" />
            Room Dimensions & Specifications
          </h2>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-charcoal mb-1.5">
                Room Name / Identifier
              </label>
              <input
                type="text"
                value={roomName}
                onChange={(e) => setRoomName(e.target.value)}
                placeholder="e.g. Master Bedroom"
                className="w-full px-3.5 py-2.5 rounded-xl border border-warm-border text-xs focus:outline-hidden focus:border-sage-500 focus:ring-1 focus:ring-sage-500 bg-background"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-charcoal mb-1.5">
                Preferred Room Category (Optional Hint)
              </label>
              <select
                value={roomTypePref}
                onChange={(e) => setRoomTypePref(e.target.value)}
                className="w-full px-3.5 py-2.5 rounded-xl border border-warm-border text-xs focus:outline-hidden focus:border-sage-500 bg-background"
              >
                <option value="">Auto-Detect via ML (Recommended)</option>
                <option value="Bedroom">Bedroom</option>
                <option value="LivingRoom">Living Room</option>
                <option value="DiningRoom">Dining Room</option>
                <option value="HomeOffice">Home Office</option>
                <option value="Kitchen">Kitchen</option>
                <option value="Bathroom">Bathroom</option>
              </select>
            </div>
          </div>

          {/* Physical Dimensions */}
          <div className="grid grid-cols-3 gap-4 pt-2">
            <div>
              <label className="block text-[11px] font-medium text-charcoal-muted mb-1">
                Width (meters)
              </label>
              <input
                type="number"
                step="0.1"
                min="2.0"
                max="20.0"
                value={widthM}
                onChange={(e) => setWidthM(parseFloat(e.target.value) || 4.0)}
                className="w-full px-3 py-2 rounded-xl border border-warm-border text-xs bg-background"
              />
            </div>
            <div>
              <label className="block text-[11px] font-medium text-charcoal-muted mb-1">
                Length (meters)
              </label>
              <input
                type="number"
                step="0.1"
                min="2.0"
                max="20.0"
                value={lengthM}
                onChange={(e) => setLengthM(parseFloat(e.target.value) || 5.0)}
                className="w-full px-3 py-2 rounded-xl border border-warm-border text-xs bg-background"
              />
            </div>
            <div>
              <label className="block text-[11px] font-medium text-charcoal-muted mb-1">
                Ceiling Height (meters)
              </label>
              <input
                type="number"
                step="0.1"
                min="2.0"
                max="6.0"
                value={heightM}
                onChange={(e) => setHeightM(parseFloat(e.target.value) || 2.8)}
                className="w-full px-3 py-2 rounded-xl border border-warm-border text-xs bg-background"
              />
            </div>
          </div>

          {/* Style Selector */}
          <div className="pt-2">
            <label className="block text-xs font-medium text-charcoal mb-2 flex items-center gap-1.5">
              <Palette className="w-3.5 h-3.5 text-sage-600" />
              Design Style Aesthetic
            </label>
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2">
              {supportedStyles.map((style) => (
                <button
                  key={style}
                  type="button"
                  onClick={() => setStylePreference(style)}
                  className={`py-2 px-3 rounded-xl text-xs font-medium capitalize transition-all border ${
                    stylePreference === style
                      ? 'bg-sage-600 text-white border-sage-600 shadow-xs'
                      : 'bg-background hover:bg-neutral-100/80 border-warm-border text-charcoal-muted'
                  }`}
                >
                  {style}
                </button>
              ))}
            </div>
          </div>

          {/* Budget Selector */}
          <div className="pt-2">
            <label className="block text-xs font-medium text-charcoal mb-2 flex items-center gap-1.5">
              <DollarSign className="w-3.5 h-3.5 text-sage-600" />
              Budget Preference Tier
            </label>
            <div className="grid grid-cols-3 gap-3">
              {[
                { id: 'low', label: 'Economy', desc: 'Space-saving & budget-conscious' },
                { id: 'medium', label: 'Standard', desc: 'Balanced aesthetics & durability' },
                { id: 'high', label: 'Premium', desc: 'Signature designer furnishings' },
              ].map((tier) => (
                <button
                  key={tier.id}
                  type="button"
                  onClick={() => setBudgetPreference(tier.id)}
                  className={`p-3 rounded-xl text-left border transition-all ${
                    budgetPreference === tier.id
                      ? 'bg-sage-50 border-sage-400 text-charcoal shadow-xs'
                      : 'bg-background hover:bg-neutral-50 border-warm-border text-charcoal-muted'
                  }`}
                >
                  <div className="font-semibold text-xs text-charcoal">{tier.label}</div>
                  <div className="text-[10px] text-charcoal-muted mt-0.5">{tier.desc}</div>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Submit Action */}
        <div className="flex justify-end">
          <button
            type="submit"
            disabled={isLoading || !selectedFile}
            className={`px-8 py-3.5 rounded-xl font-medium text-sm flex items-center gap-2 shadow-md transition-all ${
              isLoading || !selectedFile
                ? 'bg-neutral-300 text-neutral-500 cursor-not-allowed'
                : 'bg-sage-600 hover:bg-sage-700 text-white shadow-sage-200'
            }`}
          >
            {isLoading ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                <span>Classifying Photograph & Generating Layout...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4" />
                <span>Analyze Room & Generate 3D Layout</span>
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};
