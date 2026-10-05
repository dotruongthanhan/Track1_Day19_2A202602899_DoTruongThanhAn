# AI Support Log - Nhật Ký Ứng Dụng AI Minh Bạch

> **Dự án:** Track 1 - Day 19: AI-Powered In-Context Learning Experience  
> **Họ và tên học viên:** Đỗ Trương Thành Ân  
> **Mã học viên / MSSV:** `2A202602899`  
> **Đội ngũ:** Nhóm 2A (Track 1)  
> **Phương án phụ trách chính:** **Option B (Conditional Checkpoint & Batch Synthesis)**  
> **Ngày hoàn thiện:** 06/10/2026  

---

## 1. Tuyên Bố Minh Bạch & Đạo Đức Ứng Dụng AI (AI Transparency & Ethical Statement)

Bản nhật ký này được lập nhằm ghi chép công khai, trung thực và minh bạch 100% quá trình sử dụng các công cụ Trí tuệ nhân tạo (AI) trong suốt chu trình phát triển sản phẩm Day 19.

### Nguyên tắc làm việc của cá nhân tôi (Đỗ Trương Thành Ân):
1. **AI là Trợ lý (Co-pilot), Con người là Kiến trúc sư (Lead Architect):** AI được sử dụng để gia tăng tốc độ tạo mẫu (prototyping speed), sinh mã nguồn ban đầu (scaffolding), và gợi ý giải pháp; không phó mặc hoàn toàn quyền quyết định cấu trúc hệ thống hay thẩm mỹ sản phẩm cho AI.
2. **Không chấp nhận "Vibe Coding" thiếu kiểm chứng:** Mọi dòng code, cấu hình môi trường, và prompt do AI sinh ra đều được tôi trực tiếp kiểm tra cú pháp, đo kiểm chức năng thực tế trên trình duyệt (browser console, network panel) và sửa lại các lỗi tiềm ẩn.
3. **Bảo mật dữ liệu và mã nguồn:** Tuyệt đối không đưa API Key hay dữ liệu nhạy cảm vào mã nguồn công khai; mọi kết nối AI đều được đóng gói an toàn qua file biến môi trường `.env` và proxy server.
4. **Trung thực về sai sót của AI:** Ghi nhận rõ ràng các trường hợp AI đề xuất sai, sinh code lỗi hoặc ảo giác (hallucination), cùng giải pháp cụ thể mà tôi đã tự tay khắc phục.

---

## 2. Danh Mục Công Cụ AI Đã Ứng Dụng (AI Toolstack)

| Công cụ / Mô hình | Nhà phát triển | Vai trò trong dự án | Mức độ phụ thuộc |
| :--- | :--- | :--- | :--- |
| **Google Antigravity Agent** | Google DeepMind | Trợ lý Pair-Programming: Lập trình giao diện, quản lý codebase, phân tích log, gợi ý cú pháp Git & Shell. | Hỗ trợ lập trình chính (Co-developer) |
| **Gemini API (`gemini-3.5-flash-lite`)** | Google | Hạt nhân suy luận (Inference Engine) cho Trợ giảng AI: Nhận ngữ cảnh bài giảng, take-note và highlight để thực hiện tổng hợp đối chiếu in-context. | Tích hợp trực tiếp vào sản phẩm Option B |
| **Google AI Studio** | Google | Môi trường thử nghiệm Prompt, kiểm tra danh mục mô hình (`ModelService.ListModels`), quản lý hạn ngạch API. | Đo kiểm & Tối ưu Prompt |
| **PyMuPDF / pdf2image (AI Script)** | Python Ecosystem | Script tự động hóa trích xuất 27 trang PDF slide thành hình ảnh độ nét cao. | Tự động hóa dữ liệu đầu vào |

---

## 3. Nhật Ký Chi Tiết Các Phiên Làm Việc Cùng AI (Chronological AI Interaction Log)

### Phiên 1: Khởi tạo kiến trúc giao diện Split-Screen 1:1
- **Mục tiêu:** Dựng khung giao diện web hiện đại với layout chia đôi 1:1: nửa trái là tài liệu học tập (Slide PDF / Reader Markdown), nửa phải tích hợp 50% Take-note cá nhân và 50% Khung Chat Trợ giảng AI.
- **Yêu cầu gửi AI (Prompt):**
  > *"Hãy xây dựng giao diện web học tập bằng HTML5, CSS hiện đại (Tailwind-like/CSS Grid), chia đôi màn hình 1:1. Nửa trái có 2 tab: Mục 1 xem Slide PDF tuần tự, Mục 2 xem tài liệu chuyên sâu Markdown. Nửa phải chia đôi theo chiều dọc: nửa trên là bảng Take-note ghi chú bullet point có gắn nhãn, nửa dưới là khung chat với Trợ giảng AI."*
- **Đánh giá phản hồi AI:** AI sinh khung HTML/CSS rất nhanh, bố cục trực quan, màu sắc hiện đại. Tuy nhiên, AI sử dụng `<iframe>` để nhúng PDF khiến việc render trên thiết bị di động và việc highlight text gặp khó khăn.
- **Can thiệp của tôi (Human Action):** Thay thế toàn bộ giải pháp `<iframe>` bằng cơ chế render ảnh tuần tự từng slide (`slide_1.png` đến `slide_27.png`), xây dựng bộ điều hướng chuyển trang (Next/Prev/Slider) mượt mà và trực quan hơn.

---

### Phiên 2: Xây dựng công cụ Highlight nổi & Cơ chế Hủy Highlight (Unwrap DOM)
- **Mục tiêu:** Cho phép người học quét chọn bất kỳ đoạn văn bản nào trên tài liệu, xuất hiện thanh công cụ nổi (floating toolbar) với 4 màu (`#bae6fd`, `#fbcfe8`, `#bbf7d0`, `#fef08a`), có thể thêm ghi chú trực tiếp hoặc hủy highlight mà không làm vỡ cấu trúc văn bản.
- **Yêu cầu gửi AI (Prompt):**
  > *"Viết script JavaScript xử lý sự kiện `mouseup`/`selectionchange` trên trình đọc bài học. Khi người dùng bôi đen chữ, tính toán tọa độ để hiển thị floating toolbar ngay trên đoạn text được chọn. Cung cấp nút chọn màu highlight và nút gỡ bỏ highlight (un-highlight)."*
- **Đánh giá phản hồi AI:** Toolbar nổi hiển thị đúng vị trí. Tuy nhiên, hàm un-highlight do AI viết bị lỗi nghiêm trọng: khi xóa thẻ `<mark>`, AI dùng `.remove()` làm mất luôn cả nội dung chữ bên trong của người dùng.
- **Can thiệp của tôi (Human Action):** Tự tay viết lại hàm `unwrapHighlight(markElement)`:
  ```javascript
  // Giải pháp con người sửa lại: Giữ nguyên text node, chỉ gỡ bỏ thẻ bọc
  const parent = markElement.parentNode;
  while (markElement.firstChild) {
      parent.insertBefore(markElement.firstChild, markElement);
  }
  parent.removeChild(markElement);
  ```
  Đồng thời bổ sung tính năng lưu danh sách highlight vào `localStorage` để không mất khi reload trang.

---

### Phiên 3: Thiết lập Cơ chế Checkpoint có điều kiện & Navigation Interceptor (Option B)
- **Mục tiêu:** Cài đặt logic cốt lõi của Option B: khi tổng số highlight + take-note chạm ngưỡng 5 items, hoặc khi người học bấm đổi slide / chuyển bài học, hệ thống sẽ đưa ra thông báo gợi ý tổng hợp (Proactive Nudge).
- **Yêu cầu gửi AI (Prompt):**
  > *"Viết logic giám sát số lượng note và highlight. Nếu `notes.length + highlights.length >= 5`, hiển thị popup nhẹ hỏi: 'Bạn đã tích lũy 5 ý quan trọng. Bạn có muốn tổng hợp ngay không?'. Đồng thời nếu người dùng bấm nút chuyển slide hoặc đổi bài học khi có dữ liệu chưa tổng hợp, hiện modal xác nhận với 2 nút: 'Tổng hợp ngay' và 'Để cuối buổi'."*
- **Đánh giá phản hồi AI:** AI viết đúng logic đếm và hiển thị modal. Tuy nhiên, AI lại tự động gọi API tổng hợp ngay lập tức khi đạt 5 items mà không chờ người dùng bấm đồng ý, vi phạm nghiêm trọng quyền kiểm soát của người học (làm gián đoạn việc học).
- **Can thiệp của tôi (Human Action):** Chỉnh sửa lại ranh giới kiểm soát: Đặt cờ trạng thái `hasPromptedBatch5`, chỉ hiển thị hộp thoại gợi ý nhẹ nhàng ở góc dưới bên phải, người học bấm **"Có"** thì hệ thống mới kích hoạt AI; nếu bấm **"Để sau"**, hệ thống im lặng lưu vào hàng đợi (queue) để chờ tổng hợp cuối buổi.

---

### Phiên 4: Tích hợp Gemini API thế hệ mới & Thiết kế Cross-Reconciliation Prompt
- **Mục tiêu:** Kết nối trực tiếp mô hình ngôn ngữ lớn để trả lời câu hỏi và thực hiện tổng hợp đối chiếu (in-context cross-reconciliation).
- **Yêu cầu gửi AI (Prompt):**
  > *"Xây dựng hàm gọi Gemini API gửi kèm: (1) Toàn văn nội dung slide/bài học hiện tại, (2) Danh sách các đoạn highlight của người dùng, (3) Các ghi chú người dùng đã viết. Thiết kế System Instruction yêu cầu AI không được trả lời chung chung, phải dẫn nguồn trang cụ thể và điền tiếp các ý còn dang dở."*
- **Đánh giá phản hồi AI:** AI đã soạn thảo System Instruction khá tốt. Tuy nhiên trong mã nguồn JavaScript, AI lại chèn một hàm mock giả lập (fake response) với `setTimeout` và vô tình cắt ngắn chuỗi kết quả khiến câu trả lời chỉ còn đúng 1 câu.
- **Can thiệp của tôi (Human Action):** 
  - Gỡ bỏ 100% mock code.
  - Viết hàm `executeGeminiChat` gọi API thực tế.
  - Nâng cấu hình `maxOutputTokens: 8192` để nhận trọn vẹn bản tổng hợp chi tiết và cấu trúc bảng/bullet points rõ ràng.

---

### Phiên 5: Khắc phục lỗi Deprecation Model `gemini-1.5-flash` (HTTP 404)
- **Mục tiêu:** Sửa lỗi hệ thống khi gọi API: `models/gemini-1.5-flash is not found for API version v1beta`.
- **Yêu cầu gửi AI (Prompt):**
  > *"API trả về lỗi 404 không tìm thấy model gemini-1.5-flash trên endpoint v1beta. Kiểm tra xem lỗi xuất phát từ file nào và hãy sửa lỗi đó."*
- **Đánh giá phản hồi AI:** AI phân tích log và phát hiện ra trong `index.html` và `server.py` đang cố định chuỗi tên model cũ `gemini-1.5-flash` (vốn đã bị Google AI Studio thay thế trên một số cluster).
- **Can thiệp của tôi (Human Action):** Cập nhật hệ thống sang model thế hệ mới nhất `gemini-3.5-flash-lite` và `gemini-2.5-flash`. Thêm hàm truy vấn danh sách model đang hoạt động qua `ModelService.ListModels` để ứng dụng tự động fallback thông minh nếu một model gặp sự cố.

---

### Phiên 6: Bảo mật API Key, Dọn dẹp Tài nguyên & Deploy lên GitHub Pages / Railway
- **Mục tiêu:** Chuẩn bị mã nguồn sạch, bảo mật tuyệt đối API key, dọn dẹp các tệp tin nặng không cần thiết (file PPTX) và cấu hình triển khai trực tuyến.
- **Yêu cầu gửi AI (Prompt):**
  > *"Kiểm tra toàn bộ repo để chắc chắn không bị lộ API Key lên GitHub. Xóa file PPTX và các ảnh slide cũ vì chúng ta đã chuyển hẳn sang PDF. Hướng dẫn cách deploy project lên GitHub Pages và Railway."*
- **Đánh giá phản hồi AI:** Hướng dẫn cấu hình `.gitignore` chuẩn (`.env`, `env.js`, `.venv`). Hướng dẫn bật GitHub Pages trong Settings và cấu hình Railway Procfile.
- **Can thiệp của tôi (Human Action):** 
  - Tự tay tạo modal cấu hình API Key lưu trữ trên `localStorage` trình duyệt người dùng để Option B có thể chạy độc lập 100% trên GitHub Pages mà không cần server trung gian.
  - Chạy script dọn dẹp triệt để `tu-duy-product.pptx` (4.8MB) và thư mục `assets/slides_media/` giúp repo gọn gàng, push git mượt mà không gặp lỗi RPC HTTP 400.

---

## 4. Những Điểm AI Hỗ Trợ Đắc Lực Nhất (High-Impact Contributions)

1. **Gia tăng tốc độ xây dựng Giao diện (UI Scaffolding Speed):** Giúp tiết kiệm hơn 70% thời gian viết CSS và cấu trúc thẻ HTML. Layout Split Screen 1:1 được dựng lên nhanh chóng, chuẩn responsive và dễ bảo trì.
2. **Tự động hóa xử lý dữ liệu (Asset Extraction Automation):** Thay vì phải chụp thủ công 27 slide bài giảng, AI đã gợi ý script Python sử dụng thư viện đồ họa để xuất toàn bộ ảnh slide có độ sắc nét cao chỉ trong vài giây.
3. **Kỹ thuật xây dựng System Prompt (Prompt Engineering):** AI hỗ trợ tạo khung prompt bám sát quy tắc "Ground Truth In-Context", buộc mô hình phải trích xuất chính xác số trang slide khi giải thích thắc mắc của người học.
4. **Chuẩn hóa Bộ tài liệu Báo cáo (Documentation Quality):** Hỗ trợ chuyển đổi các ghi chép rời rạc thành bảng biểu Markdown chuẩn GitHub Flavored Markdown (GFM) cho [README.md](file:///Users/dotruongthanhan/Documents/GitHub/Track1_Day19_2A202602899_DoTruongThanhAn/README.md), [three-option-design-sheet.md](file:///Users/dotruongthanhan/Documents/GitHub/Track1_Day19_2A202602899_DoTruongThanhAn/three-option-design-sheet.md) và [group-feedback-synthesis.md](file:///Users/dotruongthanhan/Documents/GitHub/Track1_Day19_2A202602899_DoTruongThanhAn/group-feedback-synthesis.md).

---

## 5. Nhật Ký Sai Sót Của AI & Hành Động Chỉnh Sửa Của Lập Trình Viên (Human Error Corrections)

Dưới đây là các lỗi sai cụ thể mà AI đã mắc phải và cách tôi đã phát hiện, phân tích nguyên nhân gốc rễ và tự tay sửa chữa:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      MA TRẬN KIỂM SOÁT LỖI SAI CỦA AI                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

| STT | Vấn đề phát sinh từ AI | Nguyên nhân kỹ thuật gốc rễ | Hậu quả nếu không can thiệp | Giải pháp do tôi tự tay chỉnh sửa |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Câu trả lời chat bị cắt ngắn cụt lủn** | AI viết code sót lại logic mock giả lập với hàm `setTimeout` và cắt chuỗi bằng `.slice(0, 3)`. | Người học chỉ nhận được 1 câu trả lời cộc lốc, không có phân tích chi tiết. | Xóa sạch toàn bộ code mock; kết nối trực tiếp `fetch()` tới endpoint Gemini với `maxOutputTokens: 8192`. |
| **2** | **Lỗi gọi API 404 Deprecated Model** | AI tự động đổi model sang `gemini-1.5-flash` (model không còn hỗ trợ trên endpoint `v1beta`). | Toàn bộ tính năng AI bị tê liệt, báo lỗi đỏ trong console. | Đổi sang `gemini-3.5-flash-lite`; bổ sung cơ chế kiểm tra `ListModels` để tự động fallback khi cần. |
| **3** | **Mất sự kiện khi chuyển bài (DOM Orphan)** | AI sử dụng phương thức `element.cloneNode(true)` để xóa event listener cũ. | Khi người dùng chuyển từ Slide sang Tài liệu chuyên sâu (Mục 2), nút bấm bị đơ hoàn toàn. | Viết lại hàm `switchLesson` với cơ chế truy vấn động (`document.getElementById`), bảo toàn trọn vẹn sự kiện click. |
| **4** | **Lỗi xóa mất chữ khi Un-highlight** | Hàm xóa highlight của AI gọi `mark.remove()`, xóa cả thẻ `<mark>` lẫn nội dung văn bản bên trong. | Người học bị mất chữ trong bài giảng sau khi bấm hủy bôi đen. | Viết hàm `unwrapHighlight()` chèn lại toàn bộ `childNodes` vào phần tử cha trước khi gỡ thẻ `<mark>`. |
| **5** | **Xâm phạm quyền kiểm soát của người học** | AI tự ý kích hoạt quá trình tổng hợp ngay khi đạt 5 notes/highlights mà không hỏi người dùng. | Làm gián đoạn việc nghe giảng của người học, gây ức chế (Cognitive Overload). | Thiết lập cờ trạng thái; chuyển thành thông báo gợi ý nhẹ nhàng ở góc màn hình, người học bấm "Có" mới thực thi. |
| **6** | **Rủi ro lộ lọt API Key** | AI lưu trực tiếp API key dưới dạng hằng số trong code JavaScript client. | API Key bị đẩy lên GitHub repository công khai, nguy cơ bị đánh cắp hạn ngạch. | Đưa key vào `.env`, viết `.env.example`, thêm `.gitignore` và bổ sung modal nhập key an toàn trên `localStorage`. |
| **7** | **Lỗi RPC HTTP 400 khi Git Push** | AI giữ lại tệp slide PPTX 4.8MB và hàng chục file ảnh cũ không còn sử dụng. | Git push thất bại do vượt ngưỡng buffer hoặc lỗi kết nối. | Rà soát và xóa sạch toàn bộ file `tu-duy-product.pptx` và thư mục `assets/slides_media/`, chuẩn hóa tài nguyên repo. |

---

## 6. Bài Học & Đúc Kết Cá Nhân (Key Takeaways & Reflections)

Qua quá trình thực hiện Day 19 với sự hỗ trợ của AI, tôi rút ra 3 bài học sâu sắc về phương pháp làm việc cùng AI trong phát triển sản phẩm công nghệ:

1. **Hiểu bản chất kỹ thuật quan trọng hơn Prompting:**
   - Prompt hay chỉ giúp AI hiểu đúng ý định, nhưng nếu lập trình viên không có nền tảng vững vàng về DOM manipulation, asynchronous JavaScript, HTTP lifecycle và API status codes, bạn sẽ không thể nào phát hiện ra tại sao nút bấm bị đơ (`cloneNode`), tại sao chữ bị mất (`unwrap`), hay tại sao API trả về 404.
2. **Thiết kế ranh giới tương tác Human–AI (Interaction Boundaries):**
   - AI có xu hướng hành động "quá nhiệt tình" (overly proactive) — ví dụ tự động tổng hợp khi chạm mốc 5 ý. Là người làm sản phẩm, tôi phải luôn đặt câu hỏi: *"Hành động này có làm đứt gãy trải nghiệm người học không?"*. Việc trao quyền quyết định cuối cùng cho con người (Human-in-the-loop) là yếu tố sống còn để sản phẩm không gây phiền toái.
3. **Thẩm định thực tế (Ground-Truth Testing) luôn là thước đo cao nhất:**
   - AI có thể tạo ra một prototype nhìn rất đẹp mắt trong vài phút, nhưng chỉ khi đưa vào tay người dùng thật (phiên test cùng bạn Hồ Hoàng Phương Anh), chúng tôi mới nhận diện được những hiểu nhầm thực tế (như việc tưởng phải bấm nút mới mở được bảng note). Dữ liệu hành vi người dùng luôn có giá trị hơn mọi suy đoán của AI.

---

> **Cam kết:** Tôi xác nhận toàn bộ nội dung trong bản nhật ký này phản ánh trung thực quá trình làm việc của tôi. Mọi đóng góp của AI và sự can thiệp của con người đều được trình bày đúng với thực tế diễn ra trong dự án.  
>  
> **Người thực hiện:**  
> **Đỗ Trương Thành Ân**  
> Mã học viên: `2A202602899` — Nhóm 2A, Track 1

