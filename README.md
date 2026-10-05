# Track 1 - Day 19: AI-Powered In-Context Learning Experience
> Dự án nghiên cứu và phát triển Prototype giải quyết bài toán mất ngữ cảnh khi ghi chú và học tập cùng AI trên tài liệu số.

---

## 1. Thông tin cá nhân & Đội ngũ

- **Họ và tên:** Đỗ Trương Thành Ân
- **Mã học viên / MSSV:** `2A202602899`
- **Tên nhóm:** Nhóm 2A (Track 1)
- **Danh sách 3 thành viên trong nhóm:**
  1. **Đỗ Trương Thành Ân** (Mã học viên: `2A202602899`) – Chịu trách nhiệm chính xây dựng **Option B**
  2. **Dương Hải Minh** (Mã học viên: `2A202602680`) – Chịu trách nhiệm chính xây dựng **Option A**
  3. **Tô Anh Đức** (Mã học viên: `2A202602639`) – Chịu trách nhiệm chính xây dựng **Option C**
- **Case bài toán nghiên cứu:** Hỗ trợ sinh viên / người học trực tuyến đọc tài liệu số (Slide PDF bài giảng, tài liệu chuyên sâu Markdown), thực hiện bôi vàng (highlight) và ghi chú (take-note), khắc phục triệt để tình trạng AI trả lời lệch ngữ cảnh (out-of-context), ảo giác hoặc thiếu căn cứ đối chiếu khi người học xem lại bài.

---

## 2. Hypothesis Problem (Giả thuyết vấn đề chuẩn 5 thành tố - Day 18)

Nhóm kế thừa và thống nhất câu phát biểu giả thuyết vấn đề dựa trên 5 thành tố chuẩn từ Day 18:

| Thành tố chuẩn | Nội dung xác định |
| :--- | :--- |
| **1. Target User** | Sinh viên / người học trực tuyến có thói quen đọc tài liệu số (PDF, slide bài giảng), thường xuyên highlight các ý quan trọng nhưng hay gặp tình trạng quên ngữ cảnh khi xem lại và muốn dùng AI hỗ trợ giải thích/tóm tắt nhưng e ngại AI trả lời lệch kiến thức bài học. |
| **2. Situation** | Khi đang tự học hoặc ôn tập lại sau giờ học, người học mở lại tài liệu bài giảng (file PDF/slide) đã có sẵn các đoạn highlight trước đó, gặp một khái niệm phức tạp khó hiểu và cần AI giải thích/tổng hợp lại ngay tại vị trí đó. |
| **3. Task** | Yêu cầu AI làm rõ, giải thích hoặc tóm tắt đoạn nội dung/khái niệm đã highlight dựa đúng trên ngữ cảnh của bài giảng gốc và đối chiếu được độ chính xác của câu trả lời. |
| **4. Desired Outcome** | Nhận được lời giải thích/tóm tắt bám sát 100% ngữ cảnh tài liệu gốc (in-context), hiểu rõ lý do và ý nghĩa của đoạn highlight mà không bị ảo giác (hallucination) hay lạc đề, giúp lấp đầy khoảng trống kiến thức mà không phải tốn công đọc lại toàn bộ bài giảng từ đầu. |
| **5. Content / Data Fixture** | Cùng một tệp tài liệu bài giảng PDF chuẩn (`tu-duy-product.pdf` - 27 slide) đã được bôi vàng sẵn các vị trí highlight quan trọng và 1 ghi chú vướng mắc "chưa hiểu" tại khái niệm chuyên môn phức tạp (làm ground truth để thử nghiệm đồng nhất cho cả 3 phương án). |

> **Câu phát biểu giả thuyết vấn đề (Problem Statement):**  
> *"Khi người dùng take note hoặc highlight bài giảng, rồi sử dụng AI ở ngoài để hỏi đáp/giải thích, thì câu trả lời của AI thường bị out of context (thiếu ngữ cảnh), rời rạc và lạc đề khỏi bài giảng gốc; khiến người học dù mở lại file tài liệu bôi vàng chi chít vẫn không thể nhớ hoặc kiểm chứng được lý do tại sao đoạn đó lại quan trọng mà phải mất công đọc lại toàn bộ tài liệu từ đầu."*

---

## 3. Three Solution Options (Mô tả cơ chế & Prototype Links)

Nhóm đã phát triển 3 hướng tiếp cận giải pháp với mức độ can thiệp (agency) và thời điểm kích hoạt ngữ cảnh khác nhau:

| Phương án | Cơ chế hoạt động (Solution Mechanism) | Trải nghiệm người dùng (UX Flow) | Link Prototype |
| :--- | :--- | :--- | :--- |
| **Option A**<br>*(User Initiates / Truy xuất theo yêu cầu)* | **Context On-Demand:** AI hoàn toàn thụ động chờ lệnh. Khi ôn tập, người học quét chọn đoạn highlight không hiểu và bấm nút yêu cầu giải thích. AI đọc đoạn trước/sau của vị trí đó và hiển thị pop-up giải thích 1–2 câu ngắn gọn. | Ưu: Giao diện sạch sẽ lúc đọc bài.<br>Nhược: Người học phải bấm thủ công từng đoạn lúc ôn tập, dễ nản nếu tài liệu có nhiều highlight. | 🔗 [Trải nghiệm Option A](https://minhdh329.github.io/Track1_Day19_2A202602899_DoTruongThanhAn/)<br>*(Mirror: [GitHub Pages Dương Hải Minh](https://minhdh329.github.io/Track1_Day19_2A202602680_DuongHaiMinh/))* |
| **Option B**<br>*(Conditional Checkpoint & Batch Synthesis)*<br>**[Đỗ Trương Thành Ân phụ trách chính]** | **Cơ chế Checkpoint có điều kiện kết hợp Batch Synthesis:** Hệ thống tự động theo dõi 2 luồng dữ liệu song song (highlight và take-note). Khi chạm mốc điều kiện (`Count(Highlights) + Count(Notes) >= 5`), AI chủ động gửi gợi ý: *"Bạn có muốn tổng hợp ngay không?"*. Nếu chọn **Có**, AI đối chiếu toàn văn tài liệu gốc để điền tiếp các bullet points ghi chú và giải thích chi tiết các đoạn highlight; nếu chọn **Không**, dữ liệu được lưu tạm vào hàng đợi và tự động tổng hợp toàn diện vào cuối buổi học. | Ưu: Giải quyết triệt để mất ngữ cảnh, người học chủ động chọn dừng lại tổng hợp hay tiếp tục nghe giảng liền mạch.<br>Nhược: Cần đồng bộ dữ liệu thời gian thực và quản lý hiển thị không gây xao nhãng. | 🔗 [Trải nghiệm Option B (Railway)](https://track1day192a202602899dotruongthanhan-production.up.railway.app/)<br>🔗 [Trải nghiệm Option B (GitHub Pages)](https://dotruongthanhan.github.io/Track1_Day19_2A202602899_DoTruongThanhAn/) |
| **Option C**<br>*(Proactive Context & Constrained Chat)* | **Smart AI Note (Split-Screen) & Constrained Chat:** Khi người học kéo chọn văn bản và gắn màu để lưu bài giảng, AI tự động viết ngay 2–3 câu giải thích ngữ cảnh tại chỗ. Cung cấp ô chat giới hạn phạm vi, chỉ trả lời dựa trên note đã lưu và ngữ cảnh AI sinh ra, từ chối câu hỏi ngoài phạm vi bài học. | Ưu: Ngữ cảnh được bắt giữ tức thì lúc lưu; chat không bị lan man.<br>Nhược: Phải review/đóng box AI ngay lúc đang nghe giảng; chat giới hạn có thể gây hụt hẫng khi muốn hỏi rộng hơn. | 🔗 [Trải nghiệm Option C (Vercel)](https://ainote-itt9q3xqj-anhduc0712s-projects.vercel.app/) |

### Distance Check giữa 3 phương án:
- **A khác B:** Option A thụ động chờ người học gọi giải thích từng highlight đơn lẻ lúc ôn bài; Option B chủ động theo dõi đồng thời highlight và take-note, kích hoạt gợi ý theo ngưỡng 5 items và hỗ trợ tổng hợp gộp cuối buổi.
- **B khác C:** Option B gom dữ liệu theo checkpoint và cho phép hoãn tổng hợp đến cuối phiên; Option C sinh ngữ cảnh tức thì cho từng highlight ngay khi lưu và dùng chat giới hạn phạm vi trên các note đã lưu.
- **C khác A:** Option A chỉ giải thích theo yêu cầu khi ôn lại; Option C chủ động can thiệp ngay lúc lưu note trong giờ học và bổ sung công cụ chat khép kín.

---

## 4. Đóng góp cụ thể của tôi trong sản phẩm nhóm

Trong suốt quá trình phát triển dự án Day 19, tôi (**Đỗ Trương Thành Ân - `2A202602899`**) đã đảm nhận các vai trò và đóng góp cụ thể sau:

### 4.1. Trực tiếp xây dựng và hoàn thiện Option B
- **Thiết kế kiến trúc ứng dụng:** Xây dựng giao diện học tập chia đôi 1:1 Split-Screen:
  - Nửa bên trái: Trình đọc tài liệu song ngữ / đa định dạng (Slide PDF tuần tự từng trang từ `tu-duy-product.pdf` và Reader chuyên sâu cho tài liệu Markdown `mcp-multi-agent.md`).
  - Nửa bên phải: Khu vực tích hợp 50% Take-note cá nhân và 50% Trợ giảng AI Chat tương tác.
- **Phát triển tính năng Highlight & Un-highlight bền vững:**
  - Xây dựng thanh công cụ nổi (floating toolbar) xuất hiện chính xác phía trên đoạn bôi đen với 4 bảng màu (`#bae6fd`, `#fbcfe8`, `#bbf7d0`, `#fef08a`), hỗ trợ gạch chân, gạch ngang và trích dẫn thẳng vào ghi chú.
  - Xây dựng cơ chế **hủy highlight (Unwrap DOM)** thông minh: Cho phép xóa từng đoạn bôi đen hoặc xóa toàn bộ trong bài học mà không làm vỡ cấu trúc DOM.
- **Cơ chế Checkpoint có điều kiện & Navigation Interceptor:**
  - Lập trình bộ đếm tích lũy thời gian thực theo công thức `Count(Notes) + Count(Highlights)`, tự động kích hoạt hộp thông báo Proactive Nudge khi đạt mốc 5 ý.
  - Bổ sung Navigation Interceptor: Tự động chặn khi người dùng đổi slide hoặc chuyển bài học mới, hiển thị modal hỏi xác nhận: *"Bạn có muốn tổng hợp lại nội dung đã note và highlight không?"* với 2 lựa chọn Có/Không.
- **Tích hợp mô hình Gemini AI thế hệ mới nhất:**
  - Kết nối model `gemini-3.5-flash-lite` qua Google AI Studio API và Python Local Server (`server.py`).
  - Gỡ bỏ hoàn toàn giới hạn ký tự / output token, thiết lập `maxOutputTokens: 8192` để câu trả lời tổng hợp và giải thích được trình bày đầy đủ, chi tiết, giàu cấu trúc Markdown.
  - Tích hợp hàm tự động truy vấn `ModelService.ListModels` để tự thích ứng với các model đang hoạt động, loại trừ triệt để các model đã bị khai tử.

### 4.2. Đóng góp vào bối cảnh chung của nhóm
- Chuẩn hóa bộ dữ liệu kiểm thử (Content Fixture) gồm bài giảng `tu-duy-product.pdf` (27 slide) và tài liệu `mcp-multi-agent.md` làm tiêu chuẩn ground truth chung cho cả nhóm đối chiếu.
- Thống nhất cơ chế lưu trữ dữ liệu cục bộ an toàn (`localStorage`), đảm bảo người học không bị mất dữ liệu take-note và highlight khi tải lại trang.

### 4.3. Xây dựng Human–AI Decision Table
Cùng nhóm thiết lập bảng phân định ranh giới quyền hạn rõ ràng giữa Người học (Human) và Trí tuệ nhân tạo (AI):

| Hoạt động | Quyền hạn của Người học (Human) | Quyền hạn của AI Agent | Ranh giới kiểm soát (Control Boundary) |
| :--- | :--- | :--- | :--- |
| **Đọc & Đánh dấu** | Toàn quyền chọn vùng bôi đen, đổi màu, gạch chân hoặc hủy highlight bất kỳ lúc nào. | Không can thiệp, chỉ quét ngầm vị trí và nội dung bôi đen để đưa vào buffer. | Người học kiểm soát 100% nội dung đánh dấu. |
| **Ghi chú (Take-note)** | Toàn quyền nhập, sửa, thêm gạch đầu dòng, gắn nhãn "(?) Chưa hiểu" hoặc xóa note. | Không tự động ghi đè, không tự xóa hay sửa đổi ghi chú của người học. | Note là sở hữu riêng của người học. |
| **Kích hoạt Tổng hợp** | Quyết định bấm "Có" (tổng hợp ngay) hoặc "Không" (để cuối buổi / tiếp tục học liền mạch). | Chủ động gửi thông báo gợi ý khi đạt ngưỡng 5 items hoặc khi chuyển bài; không tự động ép người học dừng lại. | Quyền quyết định nhịp độ học thuộc về người học (Human in the loop). |
| **Xuất kết quả AI** | Đọc, kiểm tra trích dẫn, chọn "Thêm vào ghi chú", "Gửi vào chat" hoặc đóng pop-up. | Trích xuất toàn văn tài liệu gốc để điền tiếp các ý dang dở và giải thích highlight; dẫn nguồn slide/vị trí cụ thể. | Minh chứng (evidence) quay về để người học kiểm chứng độ tin cậy. |

### 4.4. Hỗ trợ đồng đội
- Chia sẻ giải pháp kỹ thuật xử lý hình ảnh slide từ PDF không bị vỡ tỷ lệ.
- Hỗ trợ xây dựng kịch bản kiểm thử (Usability Test Protocol) thống nhất 5 tiêu điểm quan sát hành vi (First Action, Hesitation, Evidence Checking, Control & Recovery, Trade-offs).
- Đóng gói tài liệu cấu hình môi trường `.env`, `.env.example`, `.gitignore` để bảo mật API key cho toàn đội.

---

## 5. Dữ liệu kiểm thử & Bài học (Testing Data & Insights)

### 5.1. Tóm tắt dữ kiện quan sát từ phiên test do tôi trực tiếp dẫn dắt (Phiếu 2)
- **Người điều phối:** Đỗ Trương Thành Ân (`2A202602899`)
- **Người tham gia thử nghiệm (Tester):** Hồ Hoàng Phương Anh (`2A202602460`)
- **Ngày thực hiện:** 05/10/2026
- **Dữ kiện hành vi thực tế quan sát được (Fact-First):**
  - *First Action:* Tester thực hiện chuyển slide bài học đầu tiên để nắm cấu trúc trước khi thao tác.
  - *Hesitation / Breakdown:* Ban đầu có chút hiểu nhầm giống Option A là tưởng phải bấm nút mới mở được bảng note (sau đó nhận ra bảng note đã mở sẵn ở nửa phải màn hình).
  - *Evidence Checking:* Tester có chủ động đối chiếu phần trích dẫn nội dung gốc khi AI trả về kết quả tổng hợp.
  - *Control & Recovery:* Khi muốn làm mới nội dung thảo luận hoặc kết quả AI chưa ưng ý, tester chủ động dùng nút "+ Chat mới" để reset phiên hỏi đáp.
  - *Selected Option:* **Thích sự kết hợp giữa Option C và Option B.** Tester cực kỳ thích khả năng sinh giải thích tức thì ngay khi highlight của Option C, nhưng đánh giá rất cao khả năng tổng hợp đối chiếu toàn diện của Option B.
  - *Trade-off:* Tester chia sẻ rằng Option A đòi hỏi người học phải tự click mở từng cái nên dễ sinh tâm lý lười trong giờ học; Option B hỗ trợ ghi chú và tổng hợp bài rất tốt.
  - *Counter-evidence:* Không ghi nhận mâu thuẫn tiêu cực; người học đánh giá cao việc có nút xác nhận chuyển bài.

---

### 5.2. Bảng tổng hợp đối chiếu 3 phiên kiểm thử của cả nhóm (Group Feedback Synthesis)

| Tiêu điểm quan sát | Feedback 1 (Tester TV 1: Đinh Xuân Quyền) | Feedback 2 (Tester TV 2: Hồ Hoàng Phương Anh) | Feedback 3 (Tester TV 3: Trần Đình Hinh) | Quy luật lặp lại (Pattern) hoặc Điểm đối lập |
| :--- | :--- | :--- | :--- | :--- |
| **First Action**<br>*(Điểm chạm đầu tiên)* | Tìm định nghĩa trong văn bản để Highlight. | Chuyển slide đầu tiên để duyệt bài. | Cố gắng bôi đen đoạn cần ghi chú. | Cả 3 tester đều bắt đầu bằng thao tác trực tiếp trên nội dung bài giảng; 2 tester hướng tới đoạn cần lưu, 1 tester điều hướng slide. |
| **Major Breakdown**<br>*(Điểm nghẽn lớn nhất)* | Không ghi nhận do dự, thao tác trơn tru. | Hiểu nhầm nghĩ rằng phải bấm nút mới mở được khung note. | Không ghi nhận do dự hay lúng túng. | Chỉ có 1 hiểu nhầm nhỏ về cách hiển thị note ở Tester 2; nhìn chung luồng thao tác dễ tiếp cận. |
| **Control Taken**<br>*(Cách lấy lại kiểm soát)* | Dùng nút tắt/đóng phía trên câu trả lời của AI. | Bấm nút "+ Chat mới" để bắt đầu luồng hỏi đáp mới. | Dùng nút tắt/đóng trên khung AI. | Cả 3 đều chủ động dùng công cụ điều khiển giao diện để thoát hoặc làm lại khi cần. |
| **Selected Option**<br>*(Phương án lựa chọn)* | **Option B** | **Option C (kết hợp B)** | **Option A** | **Kết quả phân tán 1:1:1.** Mỗi phương án nhận được 1 lựa chọn, phản ánh rõ ràng sự phân hóa trong thói quen học tập của người dùng. |
| **Key Trade-off**<br>*(Sự đánh đổi chấp nhận)* | Chấp nhận tốn thêm thời gian take-note để nhận bản giải thích cô đọng, sâu sắc hơn. | Nhận thấy Option A lười bấm; thích giải thích tức thì của C kết hợp tổng hợp của B. | Sẵn sàng hy sinh độ chi tiết để đổi lấy sự nhanh chóng, tiện lợi tối đa. | **Xuất hiện 2 trường phái đối lập:** Ưu tiên tiện lợi, tối giản (Tester 3) đối lập với ưu tiên độ sâu sắc, có hệ thống và tổng hợp (Tester 1, Tester 2). |

---

### 5.3. Quyết định hành động tiếp theo của cả nhóm (Next Change)

- **Đúng MỘT Next Change duy nhất cho vòng tiếp theo:**  
  > **Xây dựng và kiểm thử luồng học tập kết hợp (Hybrid In-Context Flow):** Cho phép người học chủ động gọi giải thích ngữ cảnh tức thì ngay tại đoạn highlight (kế thừa ưu điểm của Option C), đồng thời các đoạn giải thích và note này được tự động gom vào bộ đệm để xuất ra một bản **Tổng hợp đối chiếu toàn diện vào cuối phiên học** (kế thừa Option B), **loại bỏ hoàn toàn việc bật popup chen ngang giữa giờ** để không làm đứt gãy mạch nghe giảng.

- **Dữ kiện thực tế dẫn đến quyết định:**  
  - Kết quả 3 phiếu kiểm thử phân bổ đều (A: 1, B: 1, C: 1), trong đó Tester 2 nêu rõ nhu cầu muốn kết hợp tính tức thì của C với khả năng tổng hợp của B.
  - Tester 1 sẵn sàng đánh đổi thời gian để nhận bản giải thích chi tiết, trong khi Tester 3 ưu tiên sự tiện lợi. Luồng kết hợp là giải pháp dung hòa tốt nhất giữa việc giải tỏa thắc mắc tại chỗ và việc hệ thống hóa kiến thức cuối buổi.

---

### 5.4. Những điều vẫn CHƯA THỂ CHỨNG MINH sau 3 phiên test (Still Unproven)

1. **Hiệu quả thực tế của luồng kết hợp:** Liệu việc vừa giải thích tức thì vừa tổng hợp cuối buổi có thực sự giảm tải nhận thức và ít gây gián đoạn hơn trong bối cảnh học thực tế (khi giảng viên giảng nhanh) hay không?
2. **Hành vi kiểm chứng minh chứng:** Người học có thực sự đọc lại các trích dẫn nguồn đối chiếu và hiểu đúng bản chất vấn đề hay chỉ tin tưởng thụ động vào văn bản AI sinh ra?
3. **Mức độ ghi nhớ dài hạn:** Việc nhận bản tổng hợp cuối buổi có thực sự giúp người học nhớ bài lâu hơn và tiết kiệm thời gian ôn thi so với việc tự ghi chép truyền thống hay không?
4. **Quy mô mẫu thử nghiệm:** Kích thước mẫu thử mới dừng lại ở 3 tester, mỗi người chọn một phương án khác nhau nên chưa đủ cơ sở thống kê để khẳng định phương án nào được số đông người dùng ưa chuộng nhất.

---

## 6. AI Support Log

> 📄 **Xem tài liệu chi tiết:** [ai-support-log.md](./ai-support-log.md) — *Nhật ký ghi chép việc ứng dụng AI minh bạch của cá nhân (Đỗ Trương Thành Ân).*

Nhật ký ghi nhận quá trình tương tác, hỗ trợ và hiệu chỉnh giữa Người phát triển và Trợ lý AI (AI-Assisted Engineering):

### 6.1. Các công cụ AI đã sử dụng
- **Google Antigravity Coding Agent:** Trợ lý pair-programming điều phối dự án, sinh mã nguồn, phân tích lỗi và tối ưu hóa hệ thống.
- **Google Gemini API (`gemini-3.5-flash-lite`, `gemini-2.5-flash`):** Mô hình ngôn ngữ lớn đóng vai trò hạt nhân suy luận, thực hiện tổng hợp đối chiếu và giải đáp thắc mắc của người học.
- **Google AI Studio:** Môi trường thử nghiệm prompt, cấu hình tham số generation config và quản lý API Key.

### 6.2. AI đã hỗ trợ hiệu quả khâu nào?
- **Khởi tạo và cấu trúc giao diện nhanh:** Tự động scaffold toàn bộ giao diện HTML5/CSS3 chuẩn hiện đại, responsive, dựng layout 1:1 Split Screen sắc nét và mượt mà.
- **Trích xuất dữ liệu tài liệu học tập:** Hỗ trợ render toàn bộ 27 trang PDF slide thành ảnh độ phân giải cao (`assets/pdf_slides/`) và chuyển đổi tài liệu `mcp-multi-agent.md` sang giao diện Reader.
- **Thiết kế System Prompt chuyên sâu:** Xây dựng khung prompt "Cross-reconciliation" buộc AI phải bám sát 100% tài liệu gốc, trích dẫn số trang/vị trí cụ thể, điền tiếp các ý dang dở và giải thích highlight mà không bị hallucination.
- **Xây dựng Server Proxy chuẩn Python (`server.py`):** Viết server chuẩn không phụ thuộc thư viện ngoài, hỗ trợ CORS, endpoint `/api/synthesize` và `/api/chat`.

### 6.3. Những điểm sai sót của AI mà tôi đã tự tay phát hiện và chỉnh sửa (Human Refinement)

| Vấn đề phát sinh từ AI | Nguyên nhân kỹ thuật | Giải pháp tôi đã tự tay chỉnh sửa |
| :--- | :--- | :--- |
| **Phản hồi chat bị cắt ngắn thành 1 câu** | AI ban đầu để lại logic mock giả lập với hàm `setTimeout` và cắt dữ liệu bằng `s.clean_content.slice(0, 3)`, khiến câu trả lời bị cộc lốc dù giao diện hiển thị AI đang hoạt động. | Loại bỏ toàn bộ mock code; viết hàm `executeGeminiChat` gọi trực tiếp vào API thật, nâng `maxOutputTokens: 8192` và prompt nghiêm cấm tóm tắt sơ sài. |
| **Lỗi `models/gemini-1.5-flash is not found`** | AI tự động thêm logic ghi đè model `gemini-3.5-flash-lite` về `gemini-1.5-flash` (model đã bị Google khai tử trên endpoint `v1beta`), dẫn đến lỗi HTTP 404. | Gỡ bỏ hoàn toàn model 1.5; giữ nguyên `gemini-3.5-flash-lite`, bổ sung hàm gọi `ListModels` để tự động chọn đúng model đang khả dụng cho API key. |
| **Mất sự kiện khi chuyển bài học (DOM Orphan)** | AI sử dụng kỹ thuật `cloneNode(true)` để xóa event listener cũ, vô tình làm đứt gãy tham chiếu của các nút chuyển bài học Mục 1 và Mục 2. | Viết lại cơ chế `switchLesson` với cơ chế truy vấn động (`document.getElementById`), bảo toàn toàn bộ sự kiện click và dữ liệu reader. |
| **Nguy cơ rò rỉ API Key lên GitHub** | AI ban đầu hardcode API key vào file JavaScript hoặc lưu biến tĩnh trong mã nguồn. | Tách toàn bộ API key vào `.env`, bổ sung `.env.example`, cập nhật `.gitignore` để bảo vệ thông tin mật, bổ sung modal cấu hình key lưu an toàn trên `localStorage` trình duyệt. |
| **Tồn đọng tệp tin rác PowerPoint (PPTX)** | Mã nguồn ban đầu còn lưu trữ file `tu-duy-product.pptx` (4.8MB) và 35 ảnh trích xuất cũ không còn sử dụng. | Tiến hành rà soát và xóa sạch toàn bộ file PPTX và thư mục `assets/slides_media/`, chuyển đổi đồng nhất 100% sang định dạng PDF và hình ảnh chuẩn. |