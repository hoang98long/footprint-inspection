import { useEffect, useRef, useState } from 'react'
import { ArrowPathIcon, ArrowUpTrayIcon, BeakerIcon, PhotoIcon, PlayIcon, XMarkIcon } from '@heroicons/react/24/outline'
import { preprocessShoeprint } from './api'
import type { PreprocessingResult } from './types'

type Status = 'idle' | 'uploading' | 'processing' | 'success' | 'error'
const acceptedTypes = new Set(['image/jpeg', 'image/png', 'image/tiff'])
const experimentThresholds = [50, 85, 100, 128, 150, 180]

function Artifact({ title, source }: { title: string; source?: string }) {
  return <section className="preprocess-artifact"><h3>{title}</h3>{source ? <img src={source} alt={title} /> : <div className="artifact-placeholder">Chưa có kết quả</div>}</section>
}

export function PreprocessPage({ onBack }: { onBack: () => void }) {
  const [file, setFile] = useState<File | null>(null)
  const [previewUrl, setPreviewUrl] = useState<string>()
  const [dimensions, setDimensions] = useState<string>()
  const [threshold, setThreshold] = useState(128)
  const [invert, setInvert] = useState(true)
  const [status, setStatus] = useState<Status>('idle')
  const [result, setResult] = useState<PreprocessingResult>()
  const [error, setError] = useState<string>()
  const [comparison, setComparison] = useState<{ threshold: number; points: number }[]>()
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => () => { if (previewUrl) URL.revokeObjectURL(previewUrl) }, [previewUrl])

  const selectFile = (candidate?: File) => {
    if (!candidate) return
    if (!acceptedTypes.has(candidate.type)) { setError('Chỉ hỗ trợ ảnh JPG, PNG hoặc TIFF.'); setStatus('error'); return }
    if (candidate.size > 25 * 1024 * 1024) { setError('Dung lượng ảnh tối đa là 25 MB.'); setStatus('error'); return }
    if (previewUrl) URL.revokeObjectURL(previewUrl)
    const url = URL.createObjectURL(candidate)
    const probe = new Image()
    probe.onload = () => setDimensions(`${probe.naturalWidth} × ${probe.naturalHeight}`)
    probe.src = url
    setFile(candidate); setPreviewUrl(url); setError(undefined); setResult(undefined); setComparison(undefined); setStatus('idle')
  }

  const run = async () => {
    if (!file) { setError('Hãy chọn một ảnh dấu vết trước khi xử lý.'); setStatus('error'); return }
    setStatus('processing'); setError(undefined); setComparison(undefined)
    try { setResult(await preprocessShoeprint(file, { threshold, invert })); setStatus('success') }
    catch (reason) { setError(reason instanceof Error ? reason.message : 'Không thể xử lý ảnh.'); setStatus('error') }
  }

  const compareThresholds = async () => {
    if (!file) { setError('Hãy chọn một ảnh trước khi so sánh ngưỡng.'); setStatus('error'); return }
    setStatus('processing'); setError(undefined)
    try {
      const rows = await Promise.all(experimentThresholds.map(async value => ({ threshold: value, points: (await preprocessShoeprint(file, { threshold: value, invert })).statistics.num_points })))
      setComparison(rows); setStatus('success')
    } catch (reason) { setError(reason instanceof Error ? reason.message : 'Không thể so sánh ngưỡng.'); setStatus('error') }
  }

  const reset = () => { if (previewUrl) URL.revokeObjectURL(previewUrl); setFile(null); setPreviewUrl(undefined); setDimensions(undefined); setThreshold(128); setInvert(true); setResult(undefined); setComparison(undefined); setError(undefined); setStatus('idle'); if (inputRef.current) inputRef.current.value = '' }
  const busy = status === 'processing' || status === 'uploading'

  return <main className="content preprocess-page">
    <div className="preprocess-heading"><div><p className="eyebrow">IMAGE PREPROCESSING</p><h2>Tiền xử lý ảnh dấu giày</h2><p>Tạo point cloud 2D theo baseline Pillow FIND_EDGES, sẵn sàng cho ICP ở bước sau.</p></div><button className="outline" onClick={onBack}>Quay lại</button></div>
    <section className="preprocess-layout">
      <div className="card preprocess-controls">
        <h3>Ảnh dấu vết</h3>
        <div className="preprocess-dropzone" onDragOver={event => event.preventDefault()} onDrop={event => { event.preventDefault(); selectFile(event.dataTransfer.files[0]) }}>
          {previewUrl ? <img src={previewUrl} alt="Xem trước ảnh tải lên" /> : <><ArrowUpTrayIcon /><b>Kéo thả ảnh vào đây</b><span>JPG, PNG hoặc TIFF · tối đa 25 MB</span></>}
          <input ref={inputRef} type="file" accept=".jpg,.jpeg,.png,.tif,.tiff,image/jpeg,image/png,image/tiff" onChange={event => selectFile(event.target.files?.[0])} />
          <button type="button" onClick={() => inputRef.current?.click()}><PhotoIcon /> Chọn ảnh</button>
        </div>
        {file && <div className="selected-file"><span><b>{file.name}</b><small>{dimensions ?? 'Đang đọc kích thước…'}</small></span><button aria-label="Xóa ảnh" onClick={reset}><XMarkIcon /></button></div>}
        <section className="parameter-panel"><h3>Tham số tiền xử lý</h3><label>Threshold: <b>{threshold}</b><input type="range" min="0" max="255" value={threshold} onChange={event => setThreshold(Number(event.target.value))} /><input className="threshold-number" type="number" min="0" max="255" value={threshold} onChange={event => setThreshold(Math.min(255, Math.max(0, Number(event.target.value))))} /></label><label className="toggle-label"><input type="checkbox" checked={invert} onChange={event => setInvert(event.target.checked)} /><span /> Invert: {invert ? 'BẬT' : 'TẮT'}</label><p>Edge method: <b>Pillow FIND_EDGES</b></p></section>
        {error && <p className="preprocess-error">{error}</p>}
        <div className="preprocess-actions"><button className="outline" onClick={reset}><ArrowPathIcon /> Reset</button><button disabled={busy} onClick={run}><PlayIcon /> {busy ? 'Đang xử lý…' : 'Run Preprocessing'}</button></div>
      </div>
      <div className="preprocess-results">
        <section className="preprocess-grid"><Artifact title="Original" source={result?.artifacts.original ?? previewUrl} /><Artifact title="Edge Detection" source={result?.artifacts.edges} /><Artifact title="Inverted" source={result?.artifacts.processed} /><Artifact title="Point Cloud" source={result?.artifacts.point_cloud} /></section>
        {result && <section className="card preprocessing-statistics"><h3>Thống kê kết quả</h3><div><Stat label="Kích thước ảnh" value={`${result.image.width} × ${result.image.height}`} /><Stat label="Points extracted" value={result.statistics.num_points.toLocaleString()} /><Stat label="Bounding box" value={result.statistics.min_x === null ? '—' : `X: ${result.statistics.min_x} → ${result.statistics.max_x}; Y: ${result.statistics.min_y} → ${result.statistics.max_y}`} /><Stat label="Density" value={`${(result.statistics.density * 100).toFixed(2)}%`} /><Stat label="Threshold" value={String(result.preprocessing.threshold)} /><Stat label="Processing time" value={`${result.processing_time_ms.toFixed(2)} ms`} /></div></section>}
      </div>
    </section>
    <section className="card threshold-comparison"><div><h3><BeakerIcon /> Compare Thresholds</h3><p>Thử các ngưỡng cố định để hỗ trợ nghiên cứu, không tự chọn ngưỡng tối ưu.</p></div><button className="outline" disabled={busy} onClick={compareThresholds}>Chạy so sánh</button>{comparison && <table><thead><tr><th>Threshold</th><th>Number of Points</th></tr></thead><tbody>{comparison.map(row => <tr key={row.threshold}><td>{row.threshold}</td><td>{row.points.toLocaleString()}</td></tr>)}</tbody></table>}</section>
  </main>
}

function Stat({ label, value }: { label: string; value: string }) { return <div><small>{label}</small><b>{value}</b></div> }
