export type RoomType =
  | 'Bedroom'
  | 'LivingRoom'
  | 'Kitchen'
  | 'DiningRoom'
  | 'Bathroom'
  | 'HomeOffice'
  | 'Other';

export interface TopPrediction {
  class_name: string;
  confidence: number;
}

export interface RoomPredictResult {
  model_version: string;
  predicted_room: string;
  confidence: number;
  probabilities: Record<string, number>;
  latency_ms?: number;
  is_demo_fallback?: boolean;
}

export interface ModelStatusResult {
  model_version: string;
  is_loaded: boolean;
  is_trained: boolean;
  device: string;
  architecture: string;
  classes: string[];
  num_classes: number;
}

export interface RoomPrediction {
  id: string;
  room_id: string;
  model_version: string;
  predicted_room_type: string;
  confidence: number;
  top_predictions: TopPrediction[];
  is_demo_fallback: boolean;
  latency_ms: number;
  created_at: string;
}

export interface Room {
  id: string;
  name: string;
  image_path: string;
  original_filename?: string;
  room_type_preference?: string;
  style_preference: string;
  budget_preference: string;
  width_m: number;
  length_m: number;
  height_m: number;
  created_at: string;
  updated_at: string;
  latest_prediction?: RoomPrediction;
}

export interface FurnitureItem {
  id: string;
  name: string;
  category: string;
  width_m: number;
  height_m: number;
  depth_m: number;
  price_estimate: number;
  currency: string;
  style: string;
  suitable_rooms: string[];
  model_type: string;
  model_path?: string;
  image_url?: string;
  color_hex: string;
  description?: string;
  created_at: string;
}

export interface LayoutItem {
  id?: string;
  layout_id?: string;
  furniture_id: string;
  pos_x: number;
  pos_y: number;
  pos_z: number;
  rot_y: number;
  scale_x?: number;
  scale_y?: number;
  scale_z?: number;
  placement_reason?: string;
  ml_score?: number;
  furniture?: FurnitureItem;
}

export interface LayoutWarning {
  code: string;
  message: string;
}

export interface Layout {
  id: string;
  room_id: string;
  name: string;
  room_type: string;
  style: string;
  budget: string;
  total_cost: number;
  is_recommended: boolean;
  layout_model_version?: string;
  items: LayoutItem[];
  warnings?: LayoutWarning[];
  created_at: string;
  updated_at: string;
}

export interface UserFeedback {
  id?: string;
  room_id: string;
  layout_id?: string;
  furniture_id?: string;
  model_version?: string;
  is_liked?: boolean;
  star_rating?: number;
  accepted_recommendation?: boolean;
  corrected_room_type?: string;
  dissatisfaction_reason?: string;
  comments?: string;
  user_adjusted_layout?: Record<string, any>;
}

export interface FeedbackSummary {
  total_feedbacks: number;
  positive_count: number;
  negative_count: number;
  positive_rate: number;
  average_star_rating: number;
  total_corrected_room_types: number;
  approved_for_retraining_count: number;
  dissatisfaction_reasons_breakdown: Record<string, number>;
}

export interface TrainingJob {
  id: string;
  job_id: string;
  status: 'QUEUED' | 'RUNNING' | 'COMPLETED' | 'FAILED';
  model_version_target: string;
  epochs: number;
  batch_size: number;
  learning_rate: number;
  dataset_size: number;
  training_history?: Array<{
    epoch: number;
    train_loss: number;
    train_acc: number;
    val_acc: number;
    val_macro_f1: number;
  }>;
  error_message?: string;
  started_at?: string;
  completed_at?: string;
  created_at: string;
}

export interface ModelVersion {
  id: string;
  version_tag: string;
  architecture: string;
  weights_path: string;
  metadata_path?: string;
  accuracy?: number;
  macro_f1?: number;
  is_active: boolean;
  is_promoted: boolean;
  promoted_at?: string;
  created_at: string;
}

export interface MLOpsStatus {
  active_model_version: string;
  is_trained_model_loaded: boolean;
  is_demo_fallback_active: boolean;
  model_architecture: string;
  supported_classes: string[];
  active_layout_model_version?: string;
  is_layout_model_loaded?: boolean;
  layout_model_architecture?: string;
  layout_model_metrics?: {
    mse?: number;
    mae?: number;
    r2_score?: number;
    collision_rate?: number;
    out_of_bounds_rate?: number;
    feasible_layout_rate?: number;
  };
  kaggle_dataset_status?: string;
  kaggle_dataset_path?: string;
  total_room_analyses: number;
  total_saved_designs: number;
  total_feedback_records: number;
  approved_feedback_samples: number;
  min_approved_samples_required: number;
  retraining_permitted: boolean;
  active_training_jobs_count: number;
  recent_training_jobs: TrainingJob[];
  available_models: ModelVersion[];
  last_evaluation?: {
    accuracy: number;
    macro_f1: number;
    precision: number;
    recall: number;
    sample_count: number;
  };
}

export interface MLOpsMetrics {
  total_predictions: number;
  average_latency_ms: number;
  prediction_volume_by_day: Record<string, number>;
  predictions_by_class: Record<string, number>;
  feedback_sentiment_rate: number;
}
