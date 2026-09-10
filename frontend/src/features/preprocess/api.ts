import axios from 'axios'
import type { PreprocessingConfig, PreprocessingError, PreprocessingResult } from './types'

export async function preprocessShoeprint(file: File, config: PreprocessingConfig): Promise<PreprocessingResult> {
  const formData = new FormData()
  formData.append('image', file)
  formData.append('threshold', String(config.threshold))
  formData.append('invert', String(config.invert))
  try {
    const { data } = await axios.post<{ success: boolean; data: PreprocessingResult }>('/api/v1/preprocess', formData)
    return data.data
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const body = error.response?.data as { error?: Partial<PreprocessingError>; detail?: Partial<PreprocessingError> } | undefined
      throw new Error(body?.error?.message ?? body?.detail?.message ?? 'Không thể xử lý ảnh. Vui lòng thử lại.')
    }
    throw error
  }
}
