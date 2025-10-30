import tkinter as tk
from tkinter import ttk, messagebox

# --- الوظائف التي سيتم تنفيذها عند الضغط على الأزرار ---

def save_data():
    """هذه الوظيفة تحفظ البيانات (مؤقتًا) وتظهر رسالة تأكيد."""
    child_name = entry_child_name.get()
    if not child_name:
        messagebox.showwarning("بيانات ناقصة", "يرجى إدخال اسم الطفل على الأقل.")
        return
    
    # في المستقبل، هنا سنضيف كود حفظ البيانات في قاعدة البيانات
    print("جاري حفظ البيانات...")
    messagebox.showinfo("نجاح", f"تم حفظ بيانات: {child_name}\n(هذه مجرد محاكاة)")

def open_vaccination_window():
    """هذه الوظيفة تفتح نافذة التطعيمات."""
    child_name = entry_child_name.get()
    if not child_name:
        messagebox.showwarning("بيانات ناقصة", "يرجى إدخال اسم الطفل قبل الانتقال للتطعيمات.")
        return

    # إغلاق النافذة الحالية
    window.destroy()

    # --- إنشاء نافذة التطعيمات الجديدة ---
    vaccination_window = tk.Tk()
    vaccination_window.title("جلسة التطعيم")
    vaccination_window.geometry("900x600")

    # إطار لعرض اسم الطفل
    info_frame = tk.Frame(vaccination_window)
    info_frame.pack(pady=20)
    
    tk.Label(info_frame, text=f"التطعيمات لـ: {child_name}", font=("Arial", 16, "bold")).pack()

    # هذا مجرد مكان holder لجدول التطعيمات الذي سنقوم ببنائه لاحقًا
    placeholder_label = tk.Label(vaccination_window, text="هنا سيتم وضع جدول إدخال التطعيمات الديناميكي", font=("Arial", 12))
    placeholder_label.pack(pady=50)

    # زر للعودة (اختياري)
    back_button = tk.Button(vaccination_window, text="<< العودة للبيانات الشخصية", command=vaccination_window.destroy)
    back_button.pack(pady=10)

    vaccination_window.mainloop()


# --- الكود الرئيسي لإنشاء النافذة الأولى ---
try:
    # ... (كل أكواد التحقق والدوال السابقة تبقى كما هي) ...
    def validate_national_id(*args):
        user_input = national_id_var.get()
        if len(user_input) != 12 and len(user_input) > 0:
            national_id_label.config(fg="red")
        else:
            national_id_label.config(fg="black")

    def to_uppercase(event):
        current_text = passport_var.get()
        entry_passport.delete(0, tk.END)
        entry_passport.insert(0, current_text.upper())

    window = tk.Tk()
    window.title("منظومة التطعيمات")
    screen_width = window.winfo_screenwidth()
    window_width = int(screen_width * 0.9)
    window_height = 750
    position_x = int((screen_width - window_width) / 2)
    position_y = 50
    window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    personal_frame = tk.LabelFrame(window, text="البيانات الشخصية", font=("Arial", 12, "bold"))
    personal_frame.pack(padx=20, pady=20, fill="x")

    # ... (كل أكواد إنشاء الحقول تبقى كما هي) ...
    entry_child_name = tk.Entry(personal_frame, justify="right", font=("Arial", 11))
    entry_child_name.grid(row=0, column=0, padx=10, pady=5, sticky='e')
    tk.Label(personal_frame, text="الاسم:", font=("Arial", 11)).grid(row=0, column=1, padx=10, pady=5, sticky='e')
    entry_father_name = tk.Entry(personal_frame, justify="right", font=("Arial", 11))
    entry_father_name.grid(row=0, column=2, padx=10, pady=5, sticky='e')
    tk.Label(personal_frame, text="اسم الأب:", font=("Arial", 11)).grid(row=0, column=3, padx=10, pady=5, sticky='e')
    entry_grandfather_name = tk.Entry(personal_frame, justify="right", font=("Arial", 11))
    entry_grandfather_name.grid(row=0, column=4, padx=10, pady=5, sticky='e')
    tk.Label(personal_frame, text="اسم الجد:", font=("Arial", 11)).grid(row=0, column=5, padx=10, pady=5, sticky='e')
    entry_surname = tk.Entry(personal_frame, justify="right", font=("Arial", 11))
    entry_surname.grid(row=0, column=6, padx=10, pady=5, sticky='e')
    tk.Label(personal_frame, text="اللقب:", font=("Arial", 11)).grid(row=0, column=7, padx=10, pady=5, sticky='e')
    entry_mother_name = tk.Entry(personal_frame, width=60, justify="right", font=("Arial", 11))
    entry_mother_name.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky='e')
    tk.Label(personal_frame, text="اسم الأم (ثلاثي):", font=("Arial", 11)).grid(row=1, column=4, padx=10, pady=5, sticky='e')
    entry_day = tk.Entry(personal_frame, width=5, justify="right", font=("Arial", 11))
    entry_day.grid(row=2, column=0, padx=10, pady=5, sticky='e')
    tk.Label(personal_frame, text="يوم:", font=("Arial", 11)).grid(row=2, column=1, padx=10, pady=5, sticky='e')
    entry_month = tk.Entry(personal_frame, width=5, justify="right", font=("Arial", 11))
    entry_month.grid(row=2, column=2, padx=10, pady=5, sticky='e')
    tk.Label(personal_frame, text="شهر:", font=("Arial", 11)).grid(row=2, column=3, padx=10, pady=5, sticky='e')
    entry_year = tk.Entry(personal_frame, width=8, justify="right", font=("Arial", 11))
    entry_year.grid(row=2, column=4, padx=10, pady=5, sticky='e')
    tk.Label(personal_frame, text="سنة:", font=("Arial", 11)).grid(row=2, column=5, padx=10, pady=5, sticky='e')
    gender_var = tk.StringVar(value="ذكر")
    tk.Label(personal_frame, text="الجنس:", font=("Arial", 11)).grid(row=3, column=5, padx=10, pady=5, sticky='e')
    tk.Radiobutton(personal_frame, text="ذكر", variable=gender_var, value="ذكر", font=("Arial", 11)).grid(row=3, column=4, padx=10, pady=5, sticky='e')
    tk.Radiobutton(personal_frame, text="أنثى", variable=gender_var, value="أنثى", font=("Arial", 11)).grid(row=3, column=3, padx=10, pady=5, sticky='e')
    nationalities = ["ليبي", "مصري", "تونسي", "جزائري", "سوداني", "سوري", "أخرى"]
    nationality_combobox = ttk.Combobox(personal_frame, values=nationalities, font=("Arial", 11), state="readonly")
    nationality_combobox.grid(row=4, column=0, padx=10, pady=5, sticky='e')
    nationality_combobox.set("ليبي")
    tk.Label(personal_frame, text="الجنسية:", font=("Arial", 11)).grid(row=4, column=1, padx=10, pady=5, sticky='e')
    national_id_var = tk.StringVar()
    entry_national_id = tk.Entry(personal_frame, textvariable=national_id_var, justify="right", font=("Arial", 11))
    entry_national_id.grid(row=4, column=2, padx=10, pady=5, sticky='e')
    national_id_label = tk.Label(personal_frame, text="الرقم الوطني (12 رقم):", font=("Arial", 11))
    national_id_label.grid(row=4, column=3, padx=10, pady=5, sticky='e')
    national_id_var.trace_add('write', validate_national_id)
    passport_var = tk.StringVar()
    entry_passport = tk.Entry(personal_frame, textvariable=passport_var, justify="right", font=("Arial", 11))
    entry_passport.grid(row=5, column=0, padx=10, pady=5, sticky='e')
    entry_passport.bind('<KeyRelease>', to_uppercase)
    tk.Label(personal_frame, text="رقم جواز السفر:", font=("Arial", 11)).grid(row=5, column=1, padx=10, pady=5, sticky='e')
    entry_family_paper = tk.Entry(personal_frame, justify="right", font=("Arial", 11))
    entry_family_paper.grid(row=6, column=0, padx=10, pady=5, sticky='e')
    tk.Label(personal_frame, text="رقم ورقة العائلة:", font=("Arial", 11)).grid(row=6, column=1, padx=10, pady=5, sticky='e')
    entry_registration_no = tk.Entry(personal_frame, justify="right", font=("Arial", 11))
    entry_registration_no.grid(row=7, column=0, padx=10, pady=5, sticky='e')
    tk.Label(personal_frame, text="رقم القيد:", font=("Arial", 11)).grid(row=7, column=1, padx=10, pady=5, sticky='e')

    # --- إضافة الأزرار ---
    buttons_frame = tk.Frame(window)
    buttons_frame.pack(pady=20, fill="x", padx=20)

    save_button = tk.Button(buttons_frame, text="حفظ البيانات", command=save_data, font=("Arial", 12), bg="lightgreen")
    save_button.pack(side="right", padx=10)

    next_button = tk.Button(buttons_frame, text="التالي -> التطعيمات", command=open_vaccination_window, font=("Arial", 12), bg="lightblue")
    next_button.pack(side="left", padx=10)

    print("تم إنشاء جميع العناصر بنجاح. جاري تشغيل النافذة...")
    window.mainloop()

except Exception as e:
    print(f"حدث خطأ ما! الرسالة هي: {e}")