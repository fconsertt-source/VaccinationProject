import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import json
import os
import re

class VaccinationSystem:
    def __init__(self):
        self.window = None
        self.current_child_data = {}
        self.data_file = "children_data.json"
        self.add_vaccination_window = None
        
        # الخطوط
        self.font_title = ("Arial", 16, "bold")
        self.font_subtitle = ("Arial", 14, "bold")
        self.font_normal = ("Arial", 12)
        self.font_small = ("Arial", 10)
        
        # الجنسيات المتاحة
        self.nationalities = [
            "ليبي", "مصري", "تونسي", "جزائري", "مغربي", "سوداني", "سوري", 
            "لبناني", "أردني", "فلسطيني", "يمني", "سعودي", "إماراتي", 
            "قطري", "كويتي", "عماني", "بحريني", "عراقي", "أخرى"
        ]
        
        # الفئات العمرية (محدثة)
        self.age_categories = [
            "حديثي الولادة",
            "عمر الشهرين", 
            "عمر 4 أشهر",
            "عمر 6 أشهر",
            "عمر 9 أشهر",
            "عمر 12 شهر",
            "عمر 15 شهر", 
            "عمر 18 شهر",
            "عمر 6 سنوات",
            "عمر 12 سنة",
            "عمر 15 سنة",
            "تعويضي",
            "منشطة"
        ]
        
        # جميع التطعيمات المتاحة للتعويض
        self.all_vaccines = {
            "B.C.G": {"name": "بي سي جي", "doses": ["جرعة وحيدة"]},
            "O.P.V": {"name": "شلل الأطفال الفموي", "doses": ["الجرعة الأولى", "الجرعة الثانية", "الجرعة الثالثة", "جرعة منشطة"]},
            "Hep.B": {"name": "الالتهاب الكبدي البائي", "doses": ["الجرعة الأولى", "الجرعة الثانية", "الجرعة الثالثة"]},
            "HEXA": {"name": "السداسي", "doses": ["الجرعة الأولى", "الجرعة الثانية", "الجرعة الثالثة", "جرعة منشطة"]},
            "ROTA": {"name": "الروتا", "doses": ["الجرعة الأولى", "الجرعة الثانية", "الجرعة الثالثة"]},
            "PCV.13": {"name": "الالتهاب الرئوي 13", "doses": ["الجرعة الأولى", "الجرعة الثانية", "جرعة منشطة"]},
            "MENG.A+CY+W135": {"name": "التهاب السحائي الرباعي", "doses": ["الجرعة الأولى", "الجرعة الثانية", "جرعة منشطة"]},
            "M.M.R": {"name": "المركب الفيروسي", "doses": ["الجرعة الأولى", "الجرعة الثانية", "الجرعة الثالثة"]},
            "Hep A": {"name": "الالتهاب الكبدي الألفي", "doses": ["الجرعة الأولى", "الجرعة الثانية"]},
            "Chicken pox": {"name": "الجديري المائي", "doses": ["الجرعة الأولى"]},
            "PENTA": {"name": "الخماسي", "doses": ["جرعة منشطة"]},
            "TETRA": {"name": "الثلاثي البكتيري + شلل الأطفال بالحقن", "doses": ["جرعة منشطة"]},
            "HPV": {"name": "الورم الحليمي (للبنات فقط)", "doses": ["الجرعة الأولى", "الجرعة الثانية", "الجرعة الثالثة"]},
            "Tdap": {"name": "الثلاثي البكتيري", "doses": ["جرعة منشطة"]}
        }
        
        # الفترات الزمنية الدنيا بين الجرعات (بالأيام)
        self.vaccine_intervals = {
            "ROTA": 28,    # 28 يوم بين الجرعات
            "MENG.A+CY+W135": 90,  # 90 يوم بين الجرعات
            "M.M.R": 120,   # 120 يوم بين الجرعات
            "HPV": 30,     # 30 يوم بين الجرعات
            "Hep A": 180,   # 180 يوم بين الجرعات
            "Hep.B": 30,    # 30 يوم بين الجرعات
            "default": 21   # 21 يوم كحد أدنى للتطعيمات الأخرى
        }
        
        # القيود الخاصة (Chicken pox و M.M.R لا يعطيان معاً)
        self.vaccine_restrictions = {
            "Chicken pox": ["M.M.R"],
            "M.M.R": ["Chicken pox"]
        }
        
        self.initialize_data_file()
    
    def initialize_data_file(self):
        """تهيئة ملف البيانات"""
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump([], f)
    
    def load_data(self):
        """تحميل البيانات"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def save_data(self, data):
        """حفظ البيانات"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def validate_date(self, day, month, year):
        """التحقق من صحة التاريخ"""
        try:
            day = int(day)
            month = int(month)
            year = int(year)
            datetime(year, month, day)
            return True
        except:
            return False
    
    def calculate_exact_age(self, birth_date):
        """حساب العمر بالضبط (سنة، شهر، يوم)"""
        try:
            birth = datetime.strptime(birth_date, "%Y-%m-%d")
            today = datetime.now()
            
            # حساب الفرق
            years = today.year - birth.year
            months = today.month - birth.month
            days = today.day - birth.day
            
            # تعديل إذا كانت الأيام سالبة
            if days < 0:
                months -= 1
                # حساب أيام الشهر السابق
                prev_month = today.month - 1 if today.month > 1 else 12
                prev_year = today.year if today.month > 1 else today.year - 1
                days_in_prev_month = (datetime(prev_year, prev_month + 1, 1) - timedelta(days=1)).day
                days = days_in_prev_month - birth.day + today.day
            
            # تعديل إذا كانت الأشهر سالبة
            if months < 0:
                years -= 1
                months += 12
            
            return years, months, days
        except:
            return 0, 0, 0
    
    def calculate_age_category(self, birth_date):
        """حساب الفئة العمرية (مصحح)"""
        try:
            years, months, days = self.calculate_exact_age(birth_date)
            total_months = years * 12 + months
            
            if total_months < 2:  # أقل من شهرين
                return "حديثي الولادة"
            elif total_months < 4:  # أقل من 4 أشهر
                return "عمر الشهرين"
            elif total_months < 6:  # أقل من 6 أشهر
                return "عمر 4 أشهر"
            elif total_months < 9:  # أقل من 9 أشهر
                return "عمر 6 أشهر"
            elif total_months < 12:  # أقل من 12 شهر
                return "عمر 9 أشهر"
            elif total_months < 15:  # أقل من 15 شهر
                return "عمر 12 شهر"
            elif total_months < 18:  # أقل من 18 شهر
                return "عمر 15 شهر"
            elif total_months < 24:  # أقل من سنتين
                return "عمر 18 شهر"
            elif total_months < 72:  # أقل من 6 سنوات
                return "عمر 6 سنوات"
            elif total_months < 144:  # أقل من 12 سنة
                return "عمر 12 سنة"
            else:
                return "عمر 15 سنة"
        except:
            return "غير محدد"
    
    def get_compensation_vaccines(self, child_age_months):
        """الحصول على التطعيمات المناسبة للتعويض بناءً على العمر"""
        compensation_vaccines = []
        
        # تحديد التطعيمات المناسبة للعمر
        if child_age_months >= 0:  # جميع الأعمار
            compensation_vaccines.extend(["B.C.G", "O.P.V", "Hep.B"])
        
        if child_age_months >= 2:  # عمر شهرين فما فوق
            compensation_vaccines.extend(["HEXA", "ROTA", "PCV.13"])
        
        if child_age_months >= 9:  # عمر 9 أشهر فما فوق
            compensation_vaccines.append("MENG.A+CY+W135")
        
        if child_age_months >= 12:  # عمر 12 شهر فما فوق
            compensation_vaccines.extend(["M.M.R", "Hep A", "Chicken pox"])
        
        if child_age_months >= 18:  # عمر 18 شهر فما فوق
            compensation_vaccines.append("PENTA")
        
        if child_age_months >= 72:  # عمر 6 سنوات فما فوق
            compensation_vaccines.append("TETRA")
        
        if child_age_months >= 144:  # عمر 12 سنة فما فوق
            compensation_vaccines.extend(["HPV", "Tdap"])
        
        return compensation_vaccines
    
    def check_vaccine_interval(self, vaccine_code, dose, last_vaccination_date):
        """التحقق من الفترة الزمنية بين الجرعات"""
        if not last_vaccination_date:
            return True, "يمكن إعطاء الجرعة الأولى"
        
        try:
            last_date = datetime.strptime(last_vaccination_date, "%Y-%m-%d")
            today = datetime.now()
            days_passed = (today - last_date).days
            
            # الحصول على الفترة المطلوبة
            required_interval = self.vaccine_intervals.get(vaccine_code, self.vaccine_intervals["default"])
            
            if days_passed >= required_interval:
                return True, f"مرت {days_passed} يوم - يمكن إعطاء الجرعة"
            else:
                days_remaining = required_interval - days_passed
                return False, f"لم تمر الفترة الكافية. باقي {days_remaining} يوم"
                
        except:
            return True, "غير معروف - يمكن المحاولة"
    
    def check_vaccine_restrictions(self, selected_vaccine, existing_vaccines):
        """التحقق من القيود الخاصة بين التطعيمات"""
        if selected_vaccine in self.vaccine_restrictions:
            restricted_vaccines = self.vaccine_restrictions[selected_vaccine]
            for vaccine in existing_vaccines:
                if vaccine in restricted_vaccines:
                    return False, f"{selected_vaccine} لا يمكن إعطاؤه مع {vaccine}"
        return True, "لا توجد قيود"
    
    def get_last_vaccination_date(self, vaccine_code):
        """الحصول على تاريخ آخر جرعة للتطعيم المحدد"""
        last_date = None
        for item in self.vaccine_table.get_children():
            values = self.vaccine_table.item(item)["values"]
            vaccine_type = values[1]
            if vaccine_code in vaccine_type:
                if last_date is None or values[0] > last_date:
                    last_date = values[0]
        return last_date
    
    def to_uppercase(self, event):
        """تحويل النص إلى أحرف كبيرة"""
        widget = event.widget
        current_text = widget.get()
        widget.delete(0, tk.END)
        widget.insert(0, current_text.upper())
    
    def validate_phone(self, event):
        """التحقق من رقم الهاتف (أرقام فقط)"""
        widget = event.widget
        current_text = widget.get()
        if not current_text.isdigit() and current_text != "":
            widget.delete(0, tk.END)
            widget.insert(0, re.sub(r'[^\d]', '', current_text))
            messagebox.showwarning("تحذير", "رقم الهاتف يجب أن يحتوي على أرقام فقط")
    
    def validate_national_id(self, event):
        """التحقق من الرقم الوطني"""
        widget = event.widget
        current_text = widget.get()
        
        if current_text == "":
            widget.config(fg="black")
            return
        
        if not current_text.isdigit() or len(current_text) != 12:
            widget.config(fg="red")
        else:
            widget.config(fg="black")
    
    def validate_passport(self, event):
        """التحقق من جواز السفر (إنجليزي فقط)"""
        widget = event.widget
        current_text = widget.get()
        
        # التحقق من أن النص إنجليزي فقط
        if current_text and not re.match("^[A-Z0-9]*$", current_text):
            widget.delete(0, tk.END)
            widget.insert(0, re.sub(r'[^A-Z0-9]', '', current_text.upper()))
            messagebox.showwarning("تحذير", "جواز السفر يجب أن يحتوي على أحرف إنجليزية وأرقام فقط")
    
    def on_nationality_change(self, event):
        """تغيير حالة الحقول بناءً على الجنسية"""
        nationality = self.nationality_combo.get()
        
        if nationality == "ليبي":
            self.entry_national_id.config(state="normal", bg="white")
            self.entry_family_paper.config(state="normal", bg="white")
            self.entry_registration_no.config(state="normal", bg="white")
        else:
            self.entry_national_id.config(state="disabled", bg="#f0f0f0")
            self.entry_family_paper.config(state="disabled", bg="#f0f0f0")
            self.entry_registration_no.config(state="disabled", bg="#f0f0f0")
    
    def add_custom_nationality(self):
        """إضافة جنسية جديدة"""
        custom_window = tk.Toplevel(self.window)
        custom_window.title("إضافة جنسية جديدة")
        custom_window.geometry("300x150")
        custom_window.configure(bg="#f0f8ff")
        
        tk.Label(custom_window, text="اسم الجنسية الجديدة:", 
                font=self.font_normal, bg="#f0f8ff").pack(pady=10)
        
        nationality_entry = tk.Entry(custom_window, font=self.font_normal, width=30)
        nationality_entry.pack(pady=5)
        
        def save_nationality():
            new_nationality = nationality_entry.get().strip()
            if not new_nationality:
                messagebox.showwarning("تحذير", "يرجى إدخال اسم الجنسية")
                return
            
            if new_nationality in self.nationalities:
                messagebox.showwarning("تحذير", "هذه الجنسية موجودة مسبقاً")
                return
            
            self.nationalities.insert(-1, new_nationality)
            self.nationality_combo['values'] = self.nationalities
            self.nationality_combo.set(new_nationality)
            custom_window.destroy()
            messagebox.showinfo("نجاح", f"تم إضافة الجنسية: {new_nationality}")
        
        tk.Button(custom_window, text="حفظ", command=save_nationality,
                 font=self.font_normal, bg="#4CAF50", fg="white", width=15).pack(pady=10)
    
    def update_age_category_auto(self, event=None):
        """تحديث الفئة العمرية تلقائياً عند تغيير تاريخ الميلاد"""
        day = self.entry_day.get()
        month = self.entry_month.get()
        year = self.entry_year.get()
        
        if day and month and year and self.validate_date(day, month, year):
            birth_date = f"{year}-{month}-{day}"
            age_category = self.calculate_age_category(birth_date)
            
            # تحديث القائمة المنسدلة تلقائياً
            self.age_category_combo.set(age_category)
            
            # تحديث العمر التفصيلي
            years, months, days = self.calculate_exact_age(birth_date)
            age_text = f"العمر: {years} سنة, {months} شهر, {days} يوم"
            self.exact_age_label.config(text=age_text)
        else:
            self.exact_age_label.config(text="العمر: غير محدد")
    
    def create_main_window(self):
        """إنشاء النافذة الرئيسية"""
        self.window = tk.Tk()
        self.window.title("نظام التطعيمات - البيانات الشخصية")
        self.window.geometry("1100x900")
        self.window.configure(bg="#f0f8ff")
        
        # العنوان الرئيسي
        title_frame = tk.Frame(self.window, bg="#2c3e50", height=80)
        title_frame.pack(fill="x", padx=10, pady=10)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="السجل الصحي للأطفال", 
                              font=self.font_title, fg="white", bg="#2c3e50")
        title_label.pack(expand=True)
        
        # الإطار الرئيسي
        main_container = tk.Frame(self.window, bg="#f0f8ff", padx=20, pady=20)
        main_container.pack(fill="both", expand=True)
        
        # قسم البيانات الشخصية
        self.create_personal_info_section(main_container)
        
        # قسم التطعيمات
        self.create_vaccination_section(main_container)
        
        # أزرار التحكم
        self.create_control_buttons(main_container)
        
        self.window.mainloop()
    
    def create_personal_info_section(self, parent):
        """إنشاء قسم البيانات الشخصية"""
        personal_frame = tk.LabelFrame(parent, text="البيانات الشخصية للطفل", 
                                      font=self.font_subtitle, bg="#e8f4f8", 
                                      padx=15, pady=15)
        personal_frame.pack(fill="x", pady=(0, 20))
        
        # استخدام grid لتحسين التخطيط
        # الصف 0: الاسم الرباعي
        tk.Label(personal_frame, text="الاسم:", font=self.font_normal, bg="#e8f4f8").grid(row=0, column=7, padx=5, pady=5, sticky='e')
        self.entry_name = tk.Entry(personal_frame, font=self.font_normal, width=18)
        self.entry_name.grid(row=0, column=6, padx=5, pady=5, sticky='w')
        
        tk.Label(personal_frame, text="اسم الأب:", font=self.font_normal, bg="#e8f4f8").grid(row=0, column=5, padx=5, pady=5, sticky='e')
        self.entry_father_name = tk.Entry(personal_frame, font=self.font_normal, width=18)
        self.entry_father_name.grid(row=0, column=4, padx=5, pady=5, sticky='w')
        
        tk.Label(personal_frame, text="اسم الجد:", font=self.font_normal, bg="#e8f4f8").grid(row=0, column=3, padx=5, pady=5, sticky='e')
        self.entry_grandfather_name = tk.Entry(personal_frame, font=self.font_normal, width=18)
        self.entry_grandfather_name.grid(row=0, column=2, padx=5, pady=5, sticky='w')
        
        tk.Label(personal_frame, text="اللقب:", font=self.font_normal, bg="#e8f4f8").grid(row=0, column=1, padx=5, pady=5, sticky='e')
        self.entry_surname = tk.Entry(personal_frame, font=self.font_normal, width=18)
        self.entry_surname.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        
        # الصف 1: اسم الأم وتاريخ الميلاد
        tk.Label(personal_frame, text="اسم الأم:", font=self.font_normal, bg="#e8f4f8").grid(row=1, column=7, padx=5, pady=5, sticky='e')
        self.entry_mother_name = tk.Entry(personal_frame, font=self.font_normal, width=40)
        self.entry_mother_name.grid(row=1, column=4, columnspan=3, padx=5, pady=5, sticky='w')
        
        tk.Label(personal_frame, text="تاريخ الميلاد:", font=self.font_normal, bg="#e8f4f8").grid(row=1, column=3, padx=5, pady=5, sticky='e')
        
        date_frame = tk.Frame(personal_frame, bg="#e8f4f8")
        date_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky='w')
        
        tk.Label(date_frame, text="يوم:", font=self.font_small, bg="#e8f4f8").pack(side="left")
        self.entry_day = tk.Entry(date_frame, font=self.font_normal, width=3, justify="center")
        self.entry_day.pack(side="left", padx=2)
        self.entry_day.bind('<KeyRelease>', self.update_age_category_auto)
        
        tk.Label(date_frame, text="شهر:", font=self.font_small, bg="#e8f4f8").pack(side="left")
        self.entry_month = tk.Entry(date_frame, font=self.font_normal, width=3, justify="center")
        self.entry_month.pack(side="left", padx=2)
        self.entry_month.bind('<KeyRelease>', self.update_age_category_auto)
        
        tk.Label(date_frame, text="سنة:", font=self.font_small, bg="#e8f4f8").pack(side="left")
        self.entry_year = tk.Entry(date_frame, font=self.font_normal, width=5, justify="center")
        self.entry_year.pack(side="left", padx=2)
        self.entry_year.bind('<KeyRelease>', self.update_age_category_auto)
        
        # الصف 2: الجنس والجنسية
        tk.Label(personal_frame, text="الجنس:", font=self.font_normal, bg="#e8f4f8").grid(row=2, column=7, padx=5, pady=5, sticky='e')
        
        gender_frame = tk.Frame(personal_frame, bg="#e8f4f8")
        gender_frame.grid(row=2, column=6, columnspan=2, padx=5, pady=5, sticky='w')
        
        self.gender_var = tk.StringVar(value="ذكر")
        tk.Radiobutton(gender_frame, text="ذكر", variable=self.gender_var, 
                      value="ذكر", font=self.font_normal, bg="#e8f4f8").pack(side="left")
        tk.Radiobutton(gender_frame, text="أنثى", variable=self.gender_var,
                      value="أنثى", font=self.font_normal, bg="#e8f4f8").pack(side="left", padx=10)
        
        tk.Label(personal_frame, text="الجنسية:", font=self.font_normal, bg="#e8f4f8").grid(row=2, column=3, padx=5, pady=5, sticky='e')
        
        nationality_frame = tk.Frame(personal_frame, bg="#e8f4f8")
        nationality_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky='w')
        
        self.nationality_combo = ttk.Combobox(nationality_frame, values=self.nationalities, 
                                             font=self.font_normal, state="readonly", width=15)
        self.nationality_combo.set("ليبي")
        self.nationality_combo.pack(side="left")
        self.nationality_combo.bind('<<ComboboxSelected>>', self.on_nationality_change)
        
        tk.Button(nationality_frame, text="إضافة جنسية", command=self.add_custom_nationality,
                 font=self.font_small, bg="#FF9800", fg="white").pack(side="left", padx=5)
        
        # الصف 3: جواز السفر ورقم الهاتف
        tk.Label(personal_frame, text="جواز السفر:", font=self.font_normal, bg="#e8f4f8").grid(row=3, column=7, padx=5, pady=5, sticky='e')
        self.entry_passport = tk.Entry(personal_frame, font=self.font_normal, width=20)
        self.entry_passport.grid(row=3, column=6, padx=5, pady=5, sticky='w')
        self.entry_passport.bind('<KeyRelease>', self.to_uppercase)
        self.entry_passport.bind('<FocusOut>', self.validate_passport)
        
        tk.Label(personal_frame, text="رقم الهاتف:", font=self.font_normal, bg="#e8f4f8").grid(row=3, column=5, padx=5, pady=5, sticky='e')
        self.entry_phone = tk.Entry(personal_frame, font=self.font_normal, width=15)
        self.entry_phone.grid(row=3, column=4, padx=5, pady=5, sticky='w')
        self.entry_phone.bind('<KeyRelease>', self.validate_phone)
        
        # الصف 4: الرقم الوطني وورقة العائلة
        tk.Label(personal_frame, text="الرقم الوطني:", font=self.font_normal, bg="#e8f4f8").grid(row=4, column=7, padx=5, pady=5, sticky='e')
        self.entry_national_id = tk.Entry(personal_frame, font=self.font_normal, width=15, justify="center")
        self.entry_national_id.grid(row=4, column=6, padx=5, pady=5, sticky='w')
        self.entry_national_id.bind('<KeyRelease>', self.validate_national_id)
        
        tk.Label(personal_frame, text="ورقة العائلة:", font=self.font_normal, bg="#e8f4f8").grid(row=4, column=5, padx=5, pady=5, sticky='e')
        self.entry_family_paper = tk.Entry(personal_frame, font=self.font_normal, width=15)
        self.entry_family_paper.grid(row=4, column=4, padx=5, pady=5, sticky='w')
        
        # الصف 5: رقم القيد
        tk.Label(personal_frame, text="رقم القيد:", font=self.font_normal, bg="#e8f4f8").grid(row=5, column=7, padx=5, pady=5, sticky='e')
        self.entry_registration_no = tk.Entry(personal_frame, font=self.font_normal, width=15)
        self.entry_registration_no.grid(row=5, column=6, padx=5, pady=5, sticky='w')
        
        # الصف 6: العمر التفصيلي
        age_frame = tk.Frame(personal_frame, bg="#e8f4f8")
        age_frame.grid(row=6, column=0, columnspan=8, pady=10, sticky='w')
        
        self.exact_age_label = tk.Label(age_frame, text="العمر: غير محدد", 
                                       font=self.font_normal, bg="#e8f4f8", fg="#2c3e50")
        self.exact_age_label.pack(side="left", padx=10)
        
        # تكوين الأعمدة لتحسين التخطيط
        for i in range(8):
            personal_frame.columnconfigure(i, weight=1)
    
    def create_vaccination_section(self, parent):
        """إنشاء قسم التطعيمات"""
        vaccine_frame = tk.LabelFrame(parent, text="سجل التطعيمات", 
                                    font=self.font_subtitle, bg="#f0f8ff", 
                                    padx=15, pady=15)
        vaccine_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # معلومات الفئة العمرية
        age_frame = tk.Frame(vaccine_frame, bg="#f0f8ff")
        age_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(age_frame, text="الفئة العمرية:", font=self.font_normal, bg="#f0f8ff").pack(side="right", padx=(10, 5))
        
        self.age_category_combo = ttk.Combobox(age_frame, values=self.age_categories, 
                                              font=self.font_normal, state="readonly", width=15)
        self.age_category_combo.pack(side="right", padx=(0, 10))
        
        self.auto_age_label = tk.Label(age_frame, text="(تلقائي: غير محدد)", 
                                      font=self.font_small, bg="#f0f8ff", fg="#666")
        self.auto_age_label.pack(side="right", padx=(10, 0))
        
        # إنشاء الجدول
        columns = ("التاريخ", "نوع التطعيم", "الجرعة", "الملاحظات", "الحالة", "الفئة العمرية")
        self.vaccine_table = ttk.Treeview(vaccine_frame, columns=columns, show="headings", height=8)
        
        # تعريف العناوين
        for col in columns:
            self.vaccine_table.heading(col, text=col)
        
        # تحديد عرض الأعمدة
        self.vaccine_table.column("التاريخ", width=100, anchor="center")
        self.vaccine_table.column("نوع التطعيم", width=150, anchor="center")
        self.vaccine_table.column("الجرعة", width=120, anchor="center")
        self.vaccine_table.column("الملاحظات", width=200, anchor="center")
        self.vaccine_table.column("الحالة", width=80, anchor="center")
        self.vaccine_table.column("الفئة العمرية", width=120, anchor="center")
        
        self.vaccine_table.pack(fill="both", expand=True)
        
        # شريط التمرير
        scrollbar = ttk.Scrollbar(vaccine_frame, orient="vertical", command=self.vaccine_table.yview)
        scrollbar.pack(side="right", fill="y")
        self.vaccine_table.configure(yscrollcommand=scrollbar.set)
        
        # أزرار إدارة التطعيمات
        vaccine_buttons_frame = tk.Frame(vaccine_frame, bg="#f0f8ff")
        vaccine_buttons_frame.pack(fill="x", pady=(10, 0))
        
        buttons = [
            ("إضافة تطعيم", self.add_vaccination, "#4CAF50"),
            ("إدراج تطعيم", self.insert_vaccination, "#2196F3"),  # زر الإدراج المضاف
            ("حذف تطعيم", self.delete_vaccination, "#f44336")
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(vaccine_buttons_frame, text=text, command=command,
                          font=self.font_normal, bg=color, fg="white", width=15)
            btn.pack(side="right", padx=5)
    
    def create_control_buttons(self, parent):
        """إنشاء أزرار التحكم"""
        control_frame = tk.Frame(parent, bg="#f0f8ff")
        control_frame.pack(fill="x", pady=20)
        
        control_buttons = [
            ("حفظ البيانات", self.save_data, "#2c3e50"),
            ("بحث طفل", self.search_child, "#3498db"),
            ("عرض الكل", self.show_all, "#9b59b6"),
            ("جديد", self.new_record, "#e74c3c"),
            ("طباعة", self.print_record, "#27ae60")
        ]
        
        for text, command, color in control_buttons:
            btn = tk.Button(control_frame, text=text, command=command,
                          font=self.font_normal, bg=color, fg="white", width=12, height=2)
            btn.pack(side="left", padx=8)
    
    def add_vaccination(self):
        """إضافة تطعيم جديد"""
        self.open_vaccination_window("إضافة تطعيم جديد")
    
    def insert_vaccination(self):
        """إدراج تطعيم جديد"""
        self.open_vaccination_window("إدراج تطعيم جديد")
    
    def open_vaccination_window(self, title):
        """فتح نافذة إضافة/إدراج التطعيم"""
        # التحقق من وجود نافذة مفتوحة مسبقاً
        if self.add_vaccination_window and self.add_vaccination_window.winfo_exists():
            self.add_vaccination_window.lift()
            self.add_vaccination_window.focus_force()
            return
        
        if not self.entry_name.get().strip():
            messagebox.showwarning("تحذير", "يرجى إدخال اسم الطفل أولاً")
            return
        
        selected_age = self.age_category_combo.get()
        if not selected_age:
            messagebox.showwarning("تحذير", "يرجى اختيار الفئة العمرية أولاً")
            return
        
        # نافذة إضافة تطعيم
        self.add_vaccination_window = tk.Toplevel(self.window)
        self.add_vaccination_window.title(title)
        self.add_vaccination_window.geometry("600x500")  # زيادة الحجم
        self.add_vaccination_window.configure(bg="#f0f8ff")
        self.add_vaccination_window.transient(self.window)
        self.add_vaccination_window.grab_set()
        
        # إغلاق النافذة عند الضغط على X
        self.add_vaccination_window.protocol("WM_DELETE_WINDOW", self.close_add_vaccination_window)
        
        # معلومات العمر والفئة
        info_frame = tk.Frame(self.add_vaccination_window, bg="#f0f8ff")
        info_frame.pack(fill="x", pady=5)
        
        tk.Label(info_frame, text=f"الفئة العمرية: {selected_age}", 
                font=self.font_normal, bg="#f0f8ff", fg="#2c3e50").pack(side="left", padx=10)
        
        # الحصول على العمر بالشهور للتعويض
        day = self.entry_day.get()
        month = self.entry_month.get()
        year = self.entry_year.get()
        child_age_months = 0
        if day and month and year and self.validate_date(day, month, year):
            birth_date = f"{year}-{month}-{day}"
            years, months, days = self.calculate_exact_age(birth_date)
            child_age_months = years * 12 + months
        
        # أنواع التطعيمات المتاحة
        tk.Label(self.add_vaccination_window, text="نوع التطعيم:", font=self.font_normal, bg="#f0f8ff").pack(pady=5)
        
        vaccine_options = []
        if selected_age == "تعويضي":
            # عرض جميع التطعيمات المناسبة للعمر للتعويض
            compensation_vaccines = self.get_compensation_vaccines(child_age_months)
            for vaccine_code in compensation_vaccines:
                if vaccine_code in self.all_vaccines:
                    vaccine_info = self.all_vaccines[vaccine_code]
                    vaccine_options.append(f"{vaccine_code} - {vaccine_info['name']}")
        elif selected_age == "منشطة":
            # للمنشطة، نعرض تطعيمات مخصصة
            vaccine_options = ["مخصص - تطعيم منشط"]
        else:
            # الفئات العمرية العادية
            pass  # سيتم معالجتها لاحقاً
        
        self.vaccine_combo = ttk.Combobox(self.add_vaccination_window, values=vaccine_options, 
                                    font=self.font_normal, state="readonly", width=50)
        self.vaccine_combo.pack(pady=5)
        if vaccine_options:
            self.vaccine_combo.set(vaccine_options[0])
        self.vaccine_combo.bind('<<ComboboxSelected>>', self.on_vaccine_selected)
        
        # معلومات الفترة الزمنية
        self.interval_label = tk.Label(self.add_vaccination_window, text="", 
                                     font=self.font_small, bg="#f0f8ff", fg="#666")
        self.interval_label.pack(pady=2)
        
        # معلومات القيود
        self.restriction_label = tk.Label(self.add_vaccination_window, text="", 
                                        font=self.font_small, bg="#f0f8ff", fg="#f44336")
        self.restriction_label.pack(pady=2)
        
        tk.Label(self.add_vaccination_window, text="الجرعة:", font=self.font_normal, bg="#f0f8ff").pack(pady=5)
        
        self.dose_combo = ttk.Combobox(self.add_vaccination_window, 
                                 font=self.font_normal, state="readonly", width=20)
        self.dose_combo.pack(pady=5)
        
        # تحديث الجرعات بناءً على التطعيم المختار أولاً
        self.update_dose_options()
        
        tk.Label(self.add_vaccination_window, text="التاريخ:", font=self.font_normal, bg="#f0f8ff").pack(pady=5)
        self.date_entry = tk.Entry(self.add_vaccination_window, font=self.font_normal, justify="center")
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.pack(pady=5)
        
        tk.Label(self.add_vaccination_window, text="الملاحظات:", font=self.font_normal, bg="#f0f8ff").pack(pady=5)
        self.notes_entry = tk.Text(self.add_vaccination_window, font=self.font_normal, height=4, width=50)
        self.notes_entry.pack(pady=5)
        
        buttons_frame = tk.Frame(self.add_vaccination_window, bg="#f0f8ff")
        buttons_frame.pack(pady=10)
        
        tk.Button(buttons_frame, text="حفظ التطعيم", command=self.save_vaccine,
                 font=self.font_normal, bg="#4CAF50", fg="white", width=15).pack(side="left", padx=5)
        
        tk.Button(buttons_frame, text="إلغاء", command=self.close_add_vaccination_window,
                 font=self.font_normal, bg="#f44336", fg="white", width=15).pack(side="left", padx=5)
    
    def on_vaccine_selected(self, event):
        """عند اختيار نوع التطعيم، تحديث قائمة الجرعات والتحقق من الفترات"""
        self.update_dose_options()
        self.check_vaccine_interval_and_restrictions()
    
    def update_dose_options(self):
        """تحديث خيارات الجرعات بناءً على التطعيم المختار"""
        selected_vaccine = self.vaccine_combo.get()
        
        if selected_vaccine:
            # استخراج كود التطعيم
            vaccine_code = selected_vaccine.split(" - ")[0]
            
            if vaccine_code in self.all_vaccines:
                doses = self.all_vaccines[vaccine_code]["doses"]
            else:
                # جرعات افتراضية للتطعيمات الأخرى
                doses = ["الجرعة الأولى", "الجرعة الثانية", "الجرعة الثالثة", "جرعة منشطة"]
            
            self.dose_combo['values'] = doses
            if doses:
                self.dose_combo.set(doses[0])
        else:
            self.dose_combo.set("")
            self.dose_combo['values'] = []
    
    def check_vaccine_interval_and_restrictions(self):
        """التحقق من الفترة الزمنية والقيود"""
        selected_vaccine = self.vaccine_combo.get()
        selected_dose = self.dose_combo.get()
        
        if selected_vaccine and selected_dose:
            vaccine_code = selected_vaccine.split(" - ")[0]
            
            # التحقق من الفترة الزمنية
            last_date = self.get_last_vaccination_date(vaccine_code)
            can_give, interval_msg = self.check_vaccine_interval(vaccine_code, selected_dose, last_date)
            self.interval_label.config(text=interval_msg)
            if not can_give:
                self.interval_label.config(fg="#f44336")
            else:
                self.interval_label.config(fg="#4CAF50")
            
            # التحقق من القيود
            existing_vaccines = self.get_existing_vaccines()
            can_combine, restriction_msg = self.check_vaccine_restrictions(vaccine_code, existing_vaccines)
            self.restriction_label.config(text=restriction_msg)
            if not can_combine:
                self.restriction_label.config(fg="#f44336")
            else:
                self.restriction_label.config(fg="#4CAF50")
    
    def get_existing_vaccines(self):
        """الحصول على التطعيمات الموجودة في الجدول"""
        existing_vaccines = []
        for item in self.vaccine_table.get_children():
            values = self.vaccine_table.item(item)["values"]
            vaccine_type = values[1]
            vaccine_code = vaccine_type.split(" - ")[0]
            existing_vaccines.append(vaccine_code)
        return existing_vaccines
    
    def save_vaccine(self):
        """حفظ التطعيم"""
        selected_age = self.age_category_combo.get()
        vaccine_type = self.vaccine_combo.get()
        vaccine_dose = self.dose_combo.get()
        
        if not vaccine_type:
            messagebox.showwarning("تحذير", "يرجى اختيار نوع التطعيم")
            return
        
        if not vaccine_dose:
            messagebox.showwarning("تحذير", "يرجى اختيار الجرعة")
            return
        
        # التحقق النهائي من القيود
        vaccine_code = vaccine_type.split(" - ")[0]
        existing_vaccines = self.get_existing_vaccines()
        can_combine, restriction_msg = self.check_vaccine_restrictions(vaccine_code, existing_vaccines)
        
        if not can_combine:
            messagebox.showerror("خطأ", restriction_msg)
            return
        
        if selected_age == "تعويضي":
            vaccine_name = "تطعيم تعويضي"
        elif selected_age == "منشطة":
            vaccine_name = "تطعيم منشط"
        else:
            vaccine_parts = vaccine_type.split(" - ")
            vaccine_name = vaccine_parts[1] if len(vaccine_parts) > 1 else vaccine_type
        
        vaccine_data = (
            self.date_entry.get(),
            f"{vaccine_code} - {vaccine_name}",
            vaccine_dose,
            self.notes_entry.get("1.0", tk.END).strip(),
            "مكتمل",
            selected_age
        )
        self.vaccine_table.insert("", "end", values=vaccine_data)
        self.close_add_vaccination_window()
        messagebox.showinfo("نجاح", "تم إضافة التطعيم بنجاح")
    
    def close_add_vaccination_window(self):
        """إغلاق نافذة إضافة التطعيم"""
        if self.add_vaccination_window:
            self.add_vaccination_window.destroy()
            self.add_vaccination_window = None
    
    def delete_vaccination(self):
        """حذف تطعيم"""
        selected = self.vaccine_table.selection()
        if not selected:
            messagebox.showwarning("تحذير", "يرجى اختيار تطعيم للحذف")
            return
        
        if messagebox.askyesno("تأكيد", "هل أنت متأكد من حذف هذا التطعيم؟"):
            self.vaccine_table.delete(selected)
    
    # باقي الدوال (save_data, search_child, show_all, new_record, print_record) تبقى كما هي
    # ... [يتبع باقي الدوال بنفس الشكل السابق]

# تشغيل التطبيق
if __name__ == "__main__":
    try:
        app = VaccinationSystem()
        app.create_main_window()
    except Exception as e:
        messagebox.showerror("خطأ", f"حدث خطأ في التطبيق: {str(e)}")