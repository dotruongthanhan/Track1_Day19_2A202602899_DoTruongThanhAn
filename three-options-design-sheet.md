# Three-Option Design Sheet

## Thông tin nền tảng & Giả thuyết nghiên cứu

- **Hypothesis Problem nhóm tiếp tục:** Khi người dùng take note hoặc highlight bài giảng, rồi sử dụng AI ở ngoài trả lời, thì câu trả lời của AI thường bị out of context (thiếu ngữ cảnh), rời rạc, lạc đề khỏi bài giảng.
- **Evidence ban đầu hỗ trợ giả thuyết:** Nhiều lúc mở lại file PDF bôi vàng chi chít, người học không nhớ tại sao lúc đó lại highlight câu này, rồi lại phải đọc lại từ đầu trang.
- **Điều vẫn chưa được chứng minh:** Việc AI tóm tắt có đúng hay sai phụ thuộc hoàn toàn vào cảm giác của người học, không có kết quả hay cơ sở đối chiếu rõ ràng để kiểm chứng (verification).

---

## 1. Những thứ phải giữ nguyên

| | Quyết định chung cho A/B/C |
| :--- | :--- |
| **Target user** | Sinh viên / người học trực tuyến có thói quen đọc tài liệu số (PDF, slide bài giảng), thường xuyên highlight các ý quan trọng nhưng hay gặp tình trạng quên ngữ cảnh khi xem lại và muốn dùng AI hỗ trợ giải thích/tóm tắt nhưng e ngại AI trả lời lệch kiến thức bài học. |
| **Situation** | Khi đang tự học/ôn tập lại sau giờ học, người học mở lại tài liệu bài giảng (file PDF/slide) đã có sẵn các đoạn highlight trước đó, gặp một khái niệm phức tạp khó hiểu và cần AI giải thích/tổng hợp lại ngay tại vị trí đó. |
| **Task** | Yêu cầu AI làm rõ, giải thích hoặc tóm tắt đoạn nội dung/khái niệm đã highlight dựa đúng trên ngữ cảnh của bài giảng gốc và đối chiếu được độ chính xác của câu trả lời. |
| **Desired outcome** | Nhận được lời giải thích/tóm tắt bám sát 100% ngữ cảnh tài liệu gốc (in-context), hiểu rõ lý do và ý nghĩa của đoạn highlight mà không bị ảo giác (hallucination) hay lạc đề, giúp lấp đầy khoảng trống kiến thức mà không phải tốn công đọc lại toàn bộ bài giảng từ đầu. |
| **Content/data fixture** | Cùng một tệp tài liệu bài giảng PDF chuẩn (ví dụ: 1 chương tài liệu học thuật 15 trang) đã được bôi vàng sẵn 3 vị trí highlight quan trọng và 1 ghi chú vướng mắc "chưa hiểu" tại một khái niệm chuyên môn phức tạp (làm ground truth để thử nghiệm đồng nhất cho cả 3 phương án). |

---

## 2. Những thứ được phép khác

| Thành phần | Option A | Option B | Option C |
| :--- | :--- | :--- | :--- |
| **Solution mechanism** | | **Cơ chế Checkpoint có điều kiện kết hợp Tổng hợp cuối buổi (Conditional Checkpoint & Batch Synthesis):**<br>- Hệ thống quét ngầm tự động 2 nguồn input: các đoạn highlight trên slide/PDF (kèm bối cảnh văn bản xung quanh) và các gạch đầu dòng take-note của user.<br>- Khi tích lũy đạt ngưỡng điều kiện (tổng 5 bullet points + highlights), AI chủ động kích hoạt câu hỏi: *"Bạn có muốn tổng hợp ngay không?"*<br>- Phân nhánh xử lý: Nếu chọn **Có** thì tổng hợp đối chiếu tức thì (in-context micro-synthesis); nếu chọn **Không** thì lưu tạm vào bộ nhớ đệm (buffer) và tự động tổng hợp toàn bộ một thể vào cuối buổi học. | |
| **User làm gì?** | | - Đọc tài liệu, bôi vàng (highlight) các ý quan trọng và ghi chú (take-note) các câu hỏi, gạch đầu dòng thắc mắc/chưa hiểu như bình thường.<br>- Khi đạt ngưỡng 5 items và AI hiển thị câu hỏi:<br>  + Chọn **"Có"** (hoặc ấn Enter): Xem ngay phản hồi đối chiếu để hiểu sâu, giải tỏa khúc mắc tại chỗ.<br>  + Chọn **"Không"** (hoặc ấn Esc): Tiếp tục nghe giảng liền mạch, không bị gián đoạn.<br>- Cuối buổi: Nhận bản tổng hợp toàn diện (nếu đã chọn hoãn lại) mà không cần thao tác thủ công. | |
| **AI làm gì?** | | - **Quét & bắt sự kiện tự động:** Trích xuất nội dung highlight (kèm số trang và đoạn văn trước/sau) cùng các dòng note của user; theo dõi bộ đếm điều kiện theo thời gian thực.<br>- **Kích hoạt chủ động (Proactive Nudge):** Khi chạm mốc 5 items, gửi thông báo hỏi user có muốn tổng hợp ngay không.<br>- **Tổng hợp đối chiếu 2 chiều (Cross-reconciliation Synthesis):**<br>  + Hệ thống hóa các điểm quan trọng và giải thích thẳng vào các điểm "chưa hiểu" dựa trên nội dung chuẩn của tài liệu gốc (kèm trích dẫn số trang/vị trí).<br>  + Nếu user chọn hoãn ("Không"): Đưa vào hàng đợi và tự động tổng hợp toàn bộ tài liệu + note ngay khi kết thúc buổi học. | |
| **Trigger** | | - **Trigger giữa buổi (In-session Checkpoint):** Kích hoạt có điều kiện khi: `Count(Highlights) + Count(Take-note bullets) >= 5`.<br>- **Trigger cuối buổi (End-of-session Batch):** Kích hoạt khi user hoàn thành/đóng phiên học, tự động xử lý toàn bộ dữ liệu đã tích lũy trong hàng đợi nếu trước đó user chưa tổng hợp. | |
| **Trade-off chính** | | - **Được (Gain):** Giải quyết triệt để vấn đề mất ngữ cảnh (in-context 100%), cân bằng hoàn hảo giữa việc giải tỏa thắc mắc kịp thời và việc duy trì sự tập trung liền mạch nghe giảng; người học có toàn quyền kiểm soát (agency) nhịp độ học.<br>- **Mất (Cost/Risk):** Thêm một bước tương tác quyết định (Yes/No) có thể gây xao nhãng nhẹ nếu giảng viên đang giảng nhanh; hệ thống đòi hỏi độ phức tạp cao hơn trong việc đồng bộ dữ liệu thời gian thực giữa tài liệu và khung note. | |
