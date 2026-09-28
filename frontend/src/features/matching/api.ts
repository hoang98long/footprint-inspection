import axios from 'axios'
import type { MatchingResult } from './types'

export async function alignShoeprints(qImage: File, kImage: File, threshold = 128): Promise<MatchingResult> {
  const form = new FormData(); form.append('q_image', qImage); form.append('k_image', kImage); form.append('threshold', String(threshold))
  try { return (await axios.post<{ data: MatchingResult }>('/api/v1/matching/align', form)).data.data }
  catch (error) { if (axios.isAxiosError(error)) throw new Error(error.response?.data?.error?.message ?? 'Không thể căn chỉnh hai dấu giày.'); throw error }
}
