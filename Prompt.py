import customtkinter as ctk
import google.generativeai as genai

# ====== API KEY ======
genai.configure(api_key="YOUR_GEMINI_API_KEY")

model = genai.GenerativeModel("gemini-1.5-flash")

# ====== Hàm phân tích ======
def analyze_idea():
    idea = idea_entry.get("1.0", "end").strip()

    if not idea:
        result_box.delete("1.0", "end")
        result_box.insert("end", "⚠️ Vui lòng nhập ý tưởng.")
        return

    system_prompt = """
Bạn là chuyên gia AI Architect cấp cao.

Khi nhận một ý tưởng, hãy:
1. Phân tích toàn diện.
2. Đưa ra phương án tối ưu nhất cho:
   - Giao diện UI/UX
   - Logic hệ thống
   - Cơ chế hoạt động
   - Kiến trúc phần mềm
   - Công nghệ phù hợp
   - Tối ưu hiệu năng
3. Sau đó tổng hợp lại thành 1 PROMPT hoàn chỉnh, chuyên nghiệp, rõ ràng để AI khác có thể hiểu và lập trình chính xác.
Trình bày có cấu trúc rõ ràng.
"""

    try:
        response = model.generate_content(system_prompt + "\n\nÝ tưởng:\n" + idea)

        result_box.delete("1.0", "end")
        result_box.insert("end", response.text)

    except Exception as e:
        result_box.delete("1.0", "end")
        result_box.insert("end", f"LỖI:\n{str(e)}")

# ====== GUI ======
ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.geometry("900x700")
app.title("Gemini AI Prompt Generator Pro")

title = ctk.CTkLabel(app, text="AI Ý TƯỞNG → PROMPT TỐI ƯU (Gemini)", font=("Arial", 20))
title.pack(pady=10)

idea_entry = ctk.CTkTextbox(app, height=150)
idea_entry.pack(padx=20, pady=10, fill="x")

analyze_btn = ctk.CTkButton(app, text="Phân tích & Tạo Prompt", command=analyze_idea)
analyze_btn.pack(pady=10)

result_box = ctk.CTkTextbox(app)
result_box.pack(padx=20, pady=10, fill="both", expand=True)

app.mainloop()
