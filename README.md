# Footprint Inspection

MVP skeleton cho hệ thống giám định dấu giày có hỗ trợ AI. Repository này chỉ cung cấp kiến trúc, cấu hình và điểm mở rộng; chưa chứa API nghiệp vụ, giao diện, thuật toán xử lý ảnh hay mô hình AI.

## Kiến trúc

Hệ thống được chia thành bốn lớp độc lập:

- **Frontend**: React/Vite phục vụ trải nghiệm vận hành giám định.
- **Backend**: FastAPI điều phối hồ sơ, dữ liệu, quy trình nghiệp vụ và tích hợp dịch vụ.
- **AI services**: Các package xử lý ảnh, trích xuất đặc trưng, truy hồi và so khớp, đặt trong `backend/app/` để có thể tách thành service độc lập sau MVP.
- **Data**: PostgreSQL là nguồn dữ liệu giao dịch; storage và vector retrieval có các điểm mở rộng sẵn.

Luồng dự kiến: Hồ sơ vụ việc → Thu nhận ảnh → Tiền xử lý → Phân tích đặc trưng → So khớp mẫu → Sinh báo cáo.

## Cấu trúc thư mục

```text
footprint-inspection/
├── backend/                 # FastAPI và các domain/AI module
│   ├── app/
│   │   ├── api/v1/routers/  # Điểm đăng ký API tương lai
│   │   ├── core/            # Cấu hình, bảo mật, logging
│   │   ├── database/        # Kết nối và metadata cơ sở dữ liệu
│   │   ├── models/ schemas/ crud/
│   │   ├── services/        # Điều phối nghiệp vụ theo domain
│   │   ├── image_processing/# Preprocess, segmentation, normalization
│   │   ├── feature_extraction/
│   │   ├── matching/        # Alignment, similarity, retrieval
│   │   ├── ai/ report/ storage/ utils/
│   │   └── dependencies/ middleware/
│   ├── tests/ scripts/
│   ├── main.py
│   └── requirements.txt
├── frontend/                # React 19 + Vite + TypeScript
│   └── src/features/        # case, capture, preprocess, analysis, matching, report
├── docs/                    # architecture, api, database, workflows
├── datasets/                # raw, processed, samples
├── models/                  # segmentation, feature, matching, checkpoints
├── reports/ scripts/ logs/  # Artifacts, automation, local logs
├── docker/                  # backend, frontend, postgres container definitions
└── docker-compose.yml
```

## Yêu cầu

- Docker Desktop và Docker Compose (khuyến nghị), hoặc
- Python 3.12+, Node.js 22+ và PostgreSQL 16+.

## Chạy bằng Docker

1. Sao chép `.env.example` thành `.env` và thay đổi mật khẩu PostgreSQL nếu cần.
2. Khởi động các service:

   ```bash
   docker compose up --build
   ```

3. Các cổng mặc định: frontend `http://localhost:5173`, backend `http://localhost:8000`, PostgreSQL `localhost:5432`.

Các Dockerfile hiện dựng môi trường phát triển; khi triển khai production, thay cấu hình dev server bằng build tĩnh/frontend server và process manager phù hợp.

## Chạy Backend cục bộ

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Chạy Frontend cục bộ

```bash
cd frontend
npm install
npm run dev
```

## Module nghiệp vụ dự kiến

| Module | Vị trí mở rộng |
| --- | --- |
| Case Management | `services/`, `models/`, `schemas/`, `crud/` |
| Image Acquisition | `services/`, `storage/` |
| Image Preprocessing | `image_processing/preprocessing/` |
| Segmentation | `image_processing/segmentation/` |
| Feature Extraction | `feature_extraction/` |
| Candidate Retrieval | `matching/retrieval/` |
| Matching | `matching/alignment/`, `matching/similarity/` |
| AI | `ai/` |
| Report (PDF/JSON) | `report/` |
| Audit | `core/logging/`, `middleware/` |

## Roadmap

1. Thiết kế schema và Alembic migrations.
2. Xây dựng API versioned, xác thực và audit trail.
3. Hiện thực pipeline xử lý ảnh, trích xuất đặc trưng và đánh giá chất lượng.
4. Tích hợp vector search, matching và mô hình AI có versioning.
5. Xây giao diện điều hành, báo cáo PDF/JSON và bộ kiểm thử end-to-end.
