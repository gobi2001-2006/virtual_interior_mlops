import {
  Room,
  FurnitureItem,
  Layout,
  LayoutItem,
  UserFeedback,
  FeedbackSummary,
  MLOpsStatus,
  MLOpsMetrics,
  TrainingJob,
  ModelVersion,
  RoomPredictResult,
  ModelStatusResult
} from '../types';

export const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

async function request<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE}${endpoint}`;
  const response = await fetch(url, {
    ...options,
    headers: {
      Accept: 'application/json',
      ...options?.headers,
    },
  });

  if (!response.ok) {
    let errorDetail = `Error ${response.status}: ${response.statusText}`;
    try {
      const errorJson = await response.json();
      if (errorJson.detail) errorDetail = errorJson.detail;
    } catch {
      // ignore
    }
    throw new Error(errorDetail);
  }

  return response.json();
}

export const api = {
  // Rooms
  predictRoomImage: async (file: File): Promise<RoomPredictResult> => {
    const formData = new FormData();
    formData.append('file', file);
    return request<RoomPredictResult>('/rooms/predict', {
      method: 'POST',
      body: formData,
    });
  },

  getModelStatus: async (): Promise<ModelStatusResult> => {
    return request<ModelStatusResult>('/rooms/model-status');
  },

  analyzeRoom: async (formData: FormData): Promise<Room> => {
    return request<Room>('/rooms/analyze', {
      method: 'POST',
      body: formData,
    });
  },

  getRooms: async (): Promise<Room[]> => {
    return request<Room[]>('/rooms');
  },

  getRoom: async (id: string): Promise<Room> => {
    return request<Room>(`/rooms/${id}`);
  },

  updateRoom: async (id: string, updates: Partial<Room>): Promise<Room> => {
    return request<Room>(`/rooms/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updates),
    });
  },

  // Furniture
  getFurnitureCatalog: async (params?: {
    category?: string;
    room_type?: string;
    style?: string;
    max_price?: number;
  }): Promise<FurnitureItem[]> => {
    const q = new URLSearchParams();
    if (params?.category) q.append('category', params.category);
    if (params?.room_type) q.append('room_type', params.room_type);
    if (params?.style) q.append('style', params.style);
    if (params?.max_price) q.append('max_price', params.max_price.toString());
    const queryStr = q.toString() ? `?${q.toString()}` : '';
    return request<FurnitureItem[]>(`/furniture${queryStr}`);
  },

  getFurnitureItem: async (id: string): Promise<FurnitureItem> => {
    return request<FurnitureItem>(`/furniture/${id}`);
  },

  // Layouts
  recommendLayout: async (data: {
    room_id: string;
    room_type?: string;
    style?: string;
    budget?: string;
    width_m?: number;
    length_m?: number;
  }): Promise<Layout> => {
    return request<Layout>('/layouts/recommend', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
  },

  saveCustomLayout: async (data: {
    room_id: string;
    name?: string;
    room_type: string;
    style?: string;
    budget?: string;
    items: LayoutItem[];
  }): Promise<Layout> => {
    return request<Layout>('/layouts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
  },

  getLayout: async (id: string): Promise<Layout> => {
    return request<Layout>(`/layouts/${id}`);
  },

  // Feedback
  submitFeedback: async (data: UserFeedback): Promise<UserFeedback> => {
    return request<UserFeedback>('/feedback', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
  },

  getFeedbackSummary: async (): Promise<FeedbackSummary> => {
    return request<FeedbackSummary>('/feedback/summary');
  },

  // MLOps
  getMLOpsStatus: async (): Promise<MLOpsStatus> => {
    return request<MLOpsStatus>('/mlops/status');
  },

  getMLOpsMetrics: async (): Promise<MLOpsMetrics> => {
    return request<MLOpsMetrics>('/mlops/metrics');
  },

  triggerRetraining: async (config: {
    epochs: number;
    batch_size: number;
    learning_rate: number;
    include_approved_feedback: boolean;
  }): Promise<TrainingJob> => {
    return request<TrainingJob>('/mlops/train', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(config),
    });
  },

  getTrainingJob: async (jobId: string): Promise<TrainingJob> => {
    return request<TrainingJob>(`/mlops/train/${jobId}`);
  },

  promoteModel: async (versionTag: string): Promise<ModelVersion> => {
    return request<ModelVersion>(`/mlops/promote/${versionTag}`, {
      method: 'POST',
    });
  },
};
