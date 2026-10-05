# The Context Management Game: MCP & Multi-Agent Protocol & Orchestration
*Từ Harness Engineering đến một workflow thực tế.*

**Nguyên tắc cốt lõi:** Right context. Right actor. Right time. (Đúng ngữ cảnh. Đúng tác nhân. Đúng thời điểm).

---

## 1. Sự tiếp nối của Harness Engineering (The Continuation)
Nếu Harness Engineering là quá trình thiết kế môi trường để agent làm việc hữu ích (bao gồm Instructions, Tools, Permissions, Validation), thì bước tiếp theo chính là **Context Management** (Quản lý ngữ cảnh).

*   **Context Management:** Quyết định xem agent nhìn thấy gì, khi nào và để làm gì. Nó xoay quanh các yếu tố: Truy cập (Access), Phạm vi (Scope), Cô lập (Isolation) và Bằng chứng (Evidence).
*   *Tóm lại:* Harness tạo ra môi trường, còn Context Management quyết định cách sử dụng môi trường đó.

> 💡 **Ghi chú:** Nếu harness là môi trường làm việc, câu hỏi tiếp theo là agent lấy thông tin ở đâu, cần thấy bao nhiêu và bằng chứng (evidence) nào xác nhận kết quả.

## 2. Bài toán thực sự: "The Game"
Sức mạnh không nằm ở việc nạp càng nhiều ngữ cảnh (context) càng tốt. Cửa sổ ngữ cảnh (context window) lớn không tự tạo ra quyết định tốt. 

Mục tiêu là cung cấp **đúng context, cho đúng tác nhân, vào đúng thời điểm** thông qua 5 bước:
1.  **Acquire:** Thu thập thông tin.
2.  **Scope:** Xác định phạm vi tín hiệu (lọc nhiễu).
3.  **Isolate:** Cô lập dữ liệu.
4.  **Act:** Hành động.
5.  **Verify:** Kiểm chứng nước đi.

## 3. Vấn đề của lập trình Web (The Web-Dev Problem)
Ngữ cảnh của một ứng dụng web không nằm ở một chỗ mà phân tán khắp nơi: Code, GitHub, Docs, Figma, Browser, Database, Logs, Deploy, Auth...

Nếu không có sự kết nối giữa các hệ thống này, con người sẽ phải làm "integration layer" (lớp tích hợp) theo quy trình thủ công: **Copy → Paste → Explain → Hope** (Sao chép → Dán → Giải thích → Hy vọng kết quả đúng). Việc copy-paste này vừa làm chậm tiến độ, vừa làm mất đi các bằng chứng xác thực (evidence).

## 4. Giao thức truy cập: MCP (The Access Protocol)
**MCP (Model Context Protocol)** giải quyết bài toán trên bằng cách mở ra quyền truy cập có cấu trúc:

*   **Host:** Codex hoặc AI application.
*   **Client:** Chịu trách nhiệm kết nối, xác thực (auth) và cấp quyền (consent).
*   **Server:** Cung cấp tài nguyên (resources), công cụ (tools) và hành động (actions).

**MCP routes access:** Nó chỉ điều hướng quyền truy cập, tạo ra một ranh giới I/O với nguồn dữ liệu gốc (source of truth) hiện tại. Nó không tự quyết định workflow (luồng công việc). Việc quyết định ai dùng tool nào với quyền gì thuộc về Orchestration.

## 5. Bối cảnh hiện tại (The Current Landscape)
Hãy chọn sử dụng MCP theo nhu cầu thực tế, không phải chạy theo trào lưu (hype). Mỗi server được thêm vào sẽ kéo theo schema, permission và những rủi ro thất bại (failure surface) mới. **Tuyệt đối không bật mọi công cụ cho mọi agent.**

Các nhóm công cụ MCP phổ biến:
*   **Repository & delivery:** GitHub
*   **Current docs:** Context7, tài liệu của vendor
*   **Design & components:** Figma, shadcn
*   **Browser evidence:** Playwright, Chrome DevTools
*   **Data & runtime:** Supabase, Neon, Sentry, Vercel
*   **Product systems:** Clerk, Stripe

*Mục tiêu của việc sử dụng MCP là:* Cải thiện ngữ cảnh · Giảm copy-paste · Khép kín vòng lặp kiểm chứng.

## 6. Định nghĩa thực sự về Agent (The Actors)
Một Agent không chỉ là một AI Model có cái tên riêng. Cùng một model, nhưng sự khác biệt nằm ở trách nhiệm, ngữ cảnh, công cụ và quyền hạn.

Công thức của một Agent:
> **Agent = Model + Instructions + Context + Tools + Authority + Feedback loop**

> 💡 **Ghi chú:** Có công cụ (tool) hay câu lệnh (prompt) không thôi chưa tạo thành agent. Quyền hạn (Authority) và vòng lặp phản hồi (Feedback loop) mới quyết định agent có thể theo đuổi công việc đến đâu.

## 7. Sự cô lập ngữ cảnh (Context Isolation) & Sub-agents
Nguyên tắc: **Loại bỏ nhiễu (Noise đi ra) · Mang về bằng chứng (Evidence quay về).**

Để làm được điều này, hệ thống chia thành Agent chính và các Sub-agents hẹp, ví dụ:
*   **Main agent** (Quản lý chung)
    *   *Repository explorer* (Chuyên khám phá repo)
    *   *Implementation agent* (Chuyên thực thi)
    *   *Browser verifier* (Chuyên kiểm chứng trên trình duyệt)
    *   *Reviewer* (Chuyên đánh giá)

**Context contract (Hợp đồng ngữ cảnh của Sub-agent):**
Sub-agent là một ngữ cảnh riêng với nhiệm vụ hẹp, làm việc song song chỉ tốt khi không bị chồng chéo. Mỗi Sub-agent cần được quy định rõ:
1. Mục tiêu
2. Context bắt đầu (Starting context)
3. Các công cụ được phép dùng (Allowed tools)
4. Phạm vi ghi/chỉnh sửa (Write scope)
5. Luật phê duyệt (Approval rules)
6. Đầu ra bắt buộc cần trả về (Output)

## 8. Mô hình tư duy tổng kết (One Mental Model)
Để áp dụng thực tế, hãy ghi nhớ 5 trụ cột tư duy này:
1.  **Harness:** Thiết kế môi trường.
2.  **MCP:** Điều hướng truy cập (Route access).
3.  **Agents:** Thực hiện công việc.
4.  **Sub-agents:** Cô lập trách nhiệm.
5.  **Evidence:** Tạo niềm tin bằng chứng thực.

**Câu hỏi quan trọng nhất:** *Agent này cần ngữ cảnh (context) gì để đưa ra nước đi đúng tiếp theo?*