export interface PreprocessingConfig { threshold: number; invert: boolean }

export interface PreprocessingStatistics {
  num_points: number; min_x: number | null; max_x: number | null; min_y: number | null; max_y: number | null
  width: number; height: number; density: number
}

export interface PreprocessingArtifacts {
  original: string; grayscale: string; edges: string; processed: string; point_cloud: string; preview_points: number[][]
}

export interface PreprocessingResult {
  image: { width: number; height: number; mode: string }
  preprocessing: PreprocessingConfig & { edge_method: string; coordinate_order: string }
  statistics: PreprocessingStatistics
  artifacts: PreprocessingArtifacts
  processing_time_ms: number
}

export interface PreprocessingError { code: string; message: string }
