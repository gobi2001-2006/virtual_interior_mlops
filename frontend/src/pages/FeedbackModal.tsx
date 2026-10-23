import React, { useState } from 'react';
import { api } from '../services/api';
import { LayoutItem } from '../types';
import {
  ThumbsUp,
  ThumbsDown,
  Star,
  CheckCircle,
  X,
  MessageSquare,
  AlertCircle
} from 'lucide-react';

interface FeedbackModalProps {
  roomId: string;
  layoutId?: string;
  modelVersion?: string;
  currentItems: LayoutItem[];
  isOpen: boolean;
  onClose: () => void;
  onSubmitted?: () => void;
}

export const FeedbackModal: React.FC<FeedbackModalProps> = ({
  roomId,
  layoutId,
  modelVersion = 'v001',
  currentItems,
  isOpen,
  onClose,
  onSubmitted,
}) => {
  const [isLiked, setIsLiked] = useState<boolean | null>(true);
  const [starRating, setStarRating] = useState<number>(4);
  const [acceptedRecommendation, setAcceptedRecommendation] = useState(true);
  const [dissatisfactionReason, setDissatisfactionReason] = useState('');
  const [comments, setComments] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  if (!isOpen) return null;

  const dissatisfactionReasons = [
    'Furniture collision or overlap',
    'Inadequate walking clearance',
    'Incorrect room typology detected',
    'Style mismatch with room',
    'Furniture oversized for dimensions',
    'Other layout preference',
  ];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setErrorMsg(null);

    // Capture adjusted furniture coordinates for layout learning
    const adjustedLayoutPayload = {
      items_count: currentItems.length,
      placements: currentItems.map((item) => ({
        furniture_id: item.furniture_id,
        pos_x: item.pos_x,
        pos_z: item.pos_z,
        rot_y: item.rot_y,
      })),
    };

    try {
      await api.submitFeedback({
        room_id: roomId,
        layout_id: layoutId,
        model_version: modelVersion,
        is_liked: isLiked ?? undefined,
        star_rating: starRating,
        accepted_recommendation: acceptedRecommendation,
        dissatisfaction_reason: isLiked === false ? dissatisfactionReason : undefined,
        comments: comments || undefined,
        user_adjusted_layout: adjustedLayoutPayload,
      });

      setIsSuccess(true);
      if (onSubmitted) onSubmitted();
      setTimeout(() => {
        setIsSuccess(false);
        onClose();
      }, 1500);
    } catch (err: any) {
      setErrorMsg(err.message || 'Failed to submit feedback. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/40 backdrop-blur-xs flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl border border-warm-border relative">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-1.5 rounded-lg text-charcoal-muted hover:text-charcoal hover:bg-neutral-100 transition-colors"
        >
          <X className="w-4 h-4" />
        </button>

        {isSuccess ? (
          <div className="py-8 text-center space-y-3">
            <div className="w-12 h-12 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center mx-auto">
              <CheckCircle className="w-6 h-6" />
            </div>
            <h3 className="font-bold text-base text-charcoal">Feedback Recorded!</h3>
            <p className="text-xs text-charcoal-muted">
              Thank you. Your layout coordinates and ratings have been saved to PostgreSQL for MLOps telemetry.
            </p>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <h2 className="text-lg font-bold text-charcoal">Design & Layout Feedback</h2>
              <p className="text-xs text-charcoal-muted mt-0.5">
                Help improve our deterministic layout engine and model training lifecycle.
              </p>
            </div>

            {errorMsg && (
              <div className="p-3 rounded-xl bg-red-50 text-red-700 text-xs flex items-center gap-2">
                <AlertCircle className="w-4 h-4 shrink-0" />
                <span>{errorMsg}</span>
              </div>
            )}

            {/* Satisfaction thumbs */}
            <div>
              <label className="block text-xs font-medium text-charcoal mb-2">
                Overall Layout Satisfaction
              </label>
              <div className="flex gap-3">
                <button
                  type="button"
                  onClick={() => setIsLiked(true)}
                  className={`flex-1 py-2.5 rounded-xl border text-xs font-semibold flex items-center justify-center gap-2 transition-all ${
                    isLiked === true
                      ? 'bg-sage-600 text-white border-sage-600 shadow-sm'
                      : 'bg-background hover:bg-neutral-100 border-warm-border text-charcoal-muted'
                  }`}
                >
                  <ThumbsUp className="w-4 h-4" />
                  Liked the Arrangement
                </button>
                <button
                  type="button"
                  onClick={() => setIsLiked(false)}
                  className={`flex-1 py-2.5 rounded-xl border text-xs font-semibold flex items-center justify-center gap-2 transition-all ${
                    isLiked === false
                      ? 'bg-red-600 text-white border-red-600 shadow-sm'
                      : 'bg-background hover:bg-neutral-100 border-warm-border text-charcoal-muted'
                  }`}
                >
                  <ThumbsDown className="w-4 h-4" />
                  Needs Adjustment
                </button>
              </div>
            </div>

            {/* 5-Star Rating */}
            <div>
              <label className="block text-xs font-medium text-charcoal mb-1.5">
                Rating (1 to 5 Stars)
              </label>
              <div className="flex gap-1.5">
                {[1, 2, 3, 4, 5].map((star) => (
                  <button
                    key={star}
                    type="button"
                    onClick={() => setStarRating(star)}
                    className="p-1 text-neutral-300 hover:text-amber-400 transition-colors"
                  >
                    <Star
                      className={`w-6 h-6 ${
                        star <= starRating ? 'text-amber-400 fill-amber-400' : 'text-neutral-300'
                      }`}
                    />
                  </button>
                ))}
              </div>
            </div>

            {/* Dissatisfaction Reasons (conditional) */}
            {isLiked === false && (
              <div>
                <label className="block text-xs font-medium text-charcoal mb-1.5">
                  Reason for Dissatisfaction
                </label>
                <select
                  value={dissatisfactionReason}
                  onChange={(e) => setDissatisfactionReason(e.target.value)}
                  className="w-full px-3 py-2 rounded-xl border border-warm-border text-xs bg-background text-charcoal"
                >
                  <option value="">-- Select a reason --</option>
                  {dissatisfactionReasons.map((r) => (
                    <option key={r} value={r}>
                      {r}
                    </option>
                  ))}
                </select>
              </div>
            )}

            {/* Comments */}
            <div>
              <label className="block text-xs font-medium text-charcoal mb-1.5">
                Comments or Spatial Preferences (Optional)
              </label>
              <textarea
                rows={3}
                value={comments}
                onChange={(e) => setComments(e.target.value)}
                placeholder="e.g. Moved the sofa closer to the north wall for TV clearance..."
                className="w-full p-3 rounded-xl border border-warm-border text-xs bg-background focus:outline-hidden focus:border-sage-500"
              />
            </div>

            <div className="flex justify-end gap-2 pt-2">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 rounded-xl border border-warm-border text-xs font-medium text-charcoal-muted hover:bg-neutral-50"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={isSubmitting}
                className="px-5 py-2 bg-sage-600 hover:bg-sage-700 text-white rounded-xl text-xs font-semibold shadow-xs disabled:opacity-50"
              >
                {isSubmitting ? 'Saving...' : 'Submit Feedback'}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};
