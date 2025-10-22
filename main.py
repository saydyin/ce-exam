import json
import random
import tkinter as tk
from tkinter import messagebox, ttk
import os
from PIL import Image, ImageTk
import time
import requests
from io import BytesIO
import urllib.request
import threading

# ==================== CONFIGURATION ====================
QUESTION_BANK = "question_bank.json"
EXAM_FILE = "questions.json"
BACKUP_FILE = "exam_backup.json"

SECTION_REQUIREMENTS = {
    "AMSTHEC": {"total": 75, "difficulty": {"easy": 7, "medium": 7, "hard": 7}, "terms": 5},
    "HPGE": {"total": 50, "difficulty": {"easy": 5, "medium": 5, "hard": 5}, "terms": 5},
    "PSAD": {"total": 75, "difficulty": {"easy": 7, "medium": 7, "hard": 7}, "terms": 5}
}

SECTION_TIMES = {
    "AMSTHEC": 5 * 60 * 60,
    "HPGE": 4 * 60 * 60,
    "PSAD": 5 * 60 * 60
}

MOTIVATIONAL_QUOTES = [
    "Success is the sum of small efforts, repeated day in and day out.",
    "The expert in anything was once a beginner.",
    "Your limitation—it's only your imagination.",
    "Push yourself, because no one else is going to do it for you.",
    "Dream it. Wish it. Do it.",
    "The harder you work for something, the greater you'll feel when you achieve it."
]

PRC_INSTRUCTIONS = [
    "Read each question carefully before answering",
    "Manage your time wisely - you have limited time for each section",
    "Answer all questions to the best of your ability",
    "You cannot return to previous sections once completed",
    "The timer will start when you begin the exam section",
    "Double-check your answers before submitting each section",
    "The exam will automatically submit when time expires",
    "Results will be shown immediately after submitting"
]

# ==================== MATERIAL 3 THEME ====================
class Material3Theme:
    def __init__(self):
        self.is_dark = False
        self.set_light_theme()
    
    def set_light_theme(self):
        self.is_dark = False
        self.primary = "#6750A4"
        self.on_primary = "#FFFFFF"
        self.primary_container = "#EADDFF"
        self.on_primary_container = "#21005D"
        self.surface = "#FEF7FF"
        self.surface_dim = "#DED8E1"
        self.surface_container = "#F3EDF7"
        self.surface_container_high = "#ECE6F0"
        self.on_surface = "#1C1B1F"
        self.on_surface_variant = "#49454F"
        self.outline = "#79747E"
        self.outline_variant = "#CAC4D0"
        self.error = "#B3261E"
        self.on_error = "#FFFFFF"
        self.success = "#1E8E3E"
        self.on_success = "#FFFFFF"
        self.shadow = "#000000"
    
    def set_dark_theme(self):
        self.is_dark = True
        self.primary = "#D0BCFF"
        self.on_primary = "#381E72"
        self.primary_container = "#4F378B"
        self.on_primary_container = "#EADDFF"
        self.surface = "#1C1B1F"
        self.surface_dim = "#141218"
        self.surface_container = "#211F26"
        self.surface_container_high = "#2B2930"
        self.on_surface = "#E6E1E5"
        self.on_surface_variant = "#CAC4D0"
        self.outline = "#938F99"
        self.outline_variant = "#49454F"
        self.error = "#F2B8B5"
        self.on_error = "#601410"
        self.success = "#79DD7A"
        self.on_success = "#0F5223"
        self.shadow = "#000000"
    
    def toggle(self):
        if self.is_dark:
            self.set_light_theme()
        else:
            self.set_dark_theme()

# ==================== EXAM GENERATOR ====================
def generate_exam():
    """Generate exam with proper randomization"""
    try:
        if not os.path.exists(QUESTION_BANK):
            sample_questions = [
                {
                    "stem": "What is the reaction force R1 for a simply supported beam with 15 kN/m UDL over 10m span?",
                    "figure": "https://i.imgur.com/2s8Q9bL.png",
                    "choices": ["75 kN", "150 kN", "225 kN", "300 kN"],
                    "correct_answer": "A",
                    "section": "AMSTHEC",
                    "difficulty": 2,
                    "explanation": "For a simply supported beam with UDL, reactions are equal: R1 = R2 = (wL)/2 = (15 × 10)/2 = 75 kN"
                },
                {
                    "stem": "A soil has void ratio e = 0.6 and specific gravity Gs = 2.65. What is the porosity?",
                    "figure": "https://i.imgur.com/9z4K7pS.png",
                    "choices": ["0.375", "0.429", "0.545", "0.625"],
                    "correct_answer": "A",
                    "section": "HPGE",
                    "difficulty": 2,
                    "explanation": "Porosity n = e / (1 + e) = 0.6 / (1 + 0.6) = 0.375"
                },
                {
                    "stem": "What is the maximum bending moment for a simply supported beam with 15 kN/m UDL over 10m span?",
                    "figure": "https://i.imgur.com/2s8Q9bL.png",
                    "choices": ["187.5 kN·m", "281.25 kN·m", "375 kN·m", "468.75 kN·m"],
                    "correct_answer": "A",
                    "section": "PSAD",
                    "difficulty": 2,
                    "explanation": "Maximum bending moment = wL²/8 = (15 × 10²)/8 = 187.5 kN·m"
                }
            ]
            with open(QUESTION_BANK, 'w', encoding='utf-8') as f:
                json.dump(sample_questions, f, indent=2, ensure_ascii=False)
        
        with open(QUESTION_BANK, 'r', encoding='utf-8') as f:
            bank = json.load(f)
    except Exception as e:
        print(f"Error loading question bank: {e}")
        return False

    random.seed(time.time() + random.randint(1, 1000000))
    
    categorized = {sec: {"easy": [], "medium": [], "hard": [], "terms": [], "other": []} 
                   for sec in SECTION_REQUIREMENTS}
    
    for q in bank:
        if not all(f in q for f in ["stem", "section", "correct_answer", "choices"]):
            continue
        if q["section"] not in SECTION_REQUIREMENTS or len(q["choices"]) < 2:
            continue
        
        section = q["section"]
        difficulty = q.get("difficulty")
        is_term = q.get("term", False)
        
        if is_term:
            categorized[section]["terms"].append(q)
        elif difficulty == 1:
            categorized[section]["easy"].append(q)
        elif difficulty == 2:
            categorized[section]["medium"].append(q)
        elif difficulty == 3:
            categorized[section]["hard"].append(q)
        else:
            categorized[section]["other"].append(q)
    
    final_questions = []
    for section, requirements in SECTION_REQUIREMENTS.items():
        section_data = categorized[section]
        selected = []
        
        for difficulty, count in requirements["difficulty"].items():
            available = section_data[difficulty][:]
            random.shuffle(available)
            selected.extend(available[:count])
        
        available_terms = section_data["terms"][:]
        random.shuffle(available_terms)
        selected.extend(available_terms[:min(requirements["terms"], len(available_terms))])
        
        remaining = requirements["total"] - len(selected)
        if remaining > 0:
            all_remaining = []
            for cat in ["easy", "medium", "hard", "terms", "other"]:
                all_remaining.extend([q for q in section_data[cat] if q not in selected])
            random.shuffle(all_remaining)
            selected.extend(all_remaining[:remaining])
        
        random.shuffle(selected)
        final_questions.extend(selected[:requirements["total"]])
    
    try:
        with open(EXAM_FILE, "w", encoding="utf-8") as f:
            json.dump(final_questions, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving exam: {e}")
        return False

# ==================== MAIN APPLICATION ====================
class ExamSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Civil Engineering Exam Simulator")
        self.root.state('zoomed')
        self.root.minsize(1200, 700)
        
        self.theme = Material3Theme()
        self.timer_id = None
        self.current_section = None
        self.questions = []
        self.all_answers = {}
        self.section_results = {}
        self.section_times = {}
        self.image_cache = {}
        
        self.load_backup()
        self.apply_theme()
        self.show_loading_screen()
        self.root.after(100, self.initialize_app)
    
    # ==================== THEME & STYLING ====================
    def apply_theme(self):
        self.root.configure(bg=self.theme.surface)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Custom.Horizontal.TProgressbar",
                       background=self.theme.primary,
                       troughcolor=self.theme.surface_container,
                       borderwidth=0,
                       thickness=8)
    
    def create_elevation(self, parent, level=1):
        """Create Material 3 elevation effect"""
        colors = [self.theme.surface_container, self.theme.surface_container_high]
        return tk.Frame(parent, bg=colors[min(level-1, 1)])
    
    def create_button(self, parent, text, command, style="filled", width=140):
        """Create Material 3 button"""
        if style == "filled":
            bg, fg = self.theme.primary, self.theme.on_primary
        elif style == "outlined":
            bg, fg = self.theme.surface, self.theme.primary
        elif style == "error":
            bg, fg = self.theme.error, self.theme.on_error
        else:
            bg, fg = self.theme.surface_container, self.theme.on_surface
        
        btn = tk.Button(parent, text=text, command=command, bg=bg, fg=fg,
                       font=("Segoe UI", 11, "bold"), relief='flat', bd=0,
                       cursor="hand2", padx=24, pady=12)
        
        def on_enter(e):
            new_bg = self.adjust_color(bg, -15 if self.theme.is_dark else -10)
            btn.config(bg=new_bg)
        
        def on_leave(e):
            btn.config(bg=bg)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn
    
    def adjust_color(self, color, amount):
        """Adjust color brightness"""
        if color.startswith('#'):
            color = color[1:]
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        new_rgb = [max(0, min(255, c + amount)) for c in rgb]
        return f"#{new_rgb[0]:02x}{new_rgb[1]:02x}{new_rgb[2]:02x}"
    
    # ==================== BACKUP & DATA ====================
    def load_backup(self):
        try:
            if os.path.exists(BACKUP_FILE):
                with open(BACKUP_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.all_answers = data.get('answers', {})
                    self.section_results = data.get('results', {})
                    self.section_times = data.get('times', {})
        except Exception as e:
            print(f"Warning: Could not load backup: {e}")
    
    def save_backup(self):
        try:
            with open(BACKUP_FILE, 'w', encoding='utf-8') as f:
                json.dump({
                    'answers': self.all_answers,
                    'results': self.section_results,
                    'times': self.section_times
                }, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save backup: {e}")
    
    # ==================== INITIALIZATION ====================
    def show_loading_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        container = tk.Frame(self.root, bg=self.theme.surface)
        container.pack(fill='both', expand=True)
        
        tk.Label(container, text="Civil Engineering Exam Simulator",
                font=("Segoe UI", 28, "bold"),
                bg=self.theme.surface, fg=self.theme.primary).pack(pady=(100, 20))
        
        tk.Label(container, text="Initializing exam system...",
                font=("Segoe UI", 14),
                bg=self.theme.surface, fg=self.theme.on_surface_variant).pack(pady=20)
        
        self.loading_progress = ttk.Progressbar(container, mode='indeterminate',
                                               length=300, style="Custom.Horizontal.TProgressbar")
        self.loading_progress.pack(pady=20)
        self.loading_progress.start()
    
    def initialize_app(self):
        try:
            success = generate_exam()
            self.loading_progress.stop()
            if success:
                self.root.after(100, self.show_main_menu)
            else:
                messagebox.showerror("Error", "Failed to generate exam")
        except Exception as e:
            self.loading_progress.stop()
            messagebox.showerror("Error", f"Initialization failed: {e}")
    
    # ==================== MAIN MENU ====================
    def show_main_menu(self):
        self.cancel_timer()
        for widget in self.root.winfo_children():
            widget.destroy()
        
        container = tk.Frame(self.root, bg=self.theme.surface)
        container.pack(fill='both', expand=True, padx=40, pady=30)
        
        # Header
        header = tk.Frame(container, bg=self.theme.surface)
        header.pack(fill="x", pady=(0, 30))
        
        tk.Label(header, text="Civil Engineering Exam Simulator",
                font=("Segoe UI", 32, "bold"),
                bg=self.theme.surface, fg=self.theme.primary).pack(anchor="w")
        
        tk.Label(header, text="PRC Board Examination Practice System",
                font=("Segoe UI", 14),
                bg=self.theme.surface, fg=self.theme.on_surface_variant).pack(anchor="w", pady=(5, 0))
        
        # Progress
        completed = len(self.section_results)
        if completed > 0:
            progress_frame = tk.Frame(header, bg=self.theme.surface)
            progress_frame.pack(fill="x", pady=(20, 0))
            
            progress_bg = tk.Frame(progress_frame, bg=self.theme.surface_container, height=12)
            progress_bg.pack(fill="x")
            
            progress_fill = tk.Frame(progress_bg, bg=self.theme.primary, height=12)
            progress_fill.place(relx=0, rely=0, relwidth=completed/3, relheight=1)
            
            tk.Label(progress_frame, text=f"{completed} of 3 sections completed",
                    font=("Segoe UI", 12, "bold"),
                    bg=self.theme.surface, fg=self.theme.on_surface).pack(pady=(5, 0))
        
        # Controls
        controls = tk.Frame(header, bg=self.theme.surface)
        controls.pack(side="right", pady=10)
        
        theme_btn = self.create_button(controls, "🌓 Theme", self.toggle_theme, "text")
        theme_btn.pack(side="left", padx=5)
        
        if self.all_answers or self.section_results:
            reset_btn = self.create_button(controls, "🔄 Reset", self.confirm_reset, "error")
            reset_btn.pack(side="left", padx=5)
        
        # Sections
        sections_frame = tk.Frame(container, bg=self.theme.surface)
        sections_frame.pack(fill="both", expand=True, pady=20)
        
        sections = [
            ("AMSTHEC", "Mathematics, Surveying &\nTransportation Engineering", 75, 5, "#6750A4"),
            ("HPGE", "Hydraulics &\nGeotechnical Engineering", 50, 4, "#7D5260"),
            ("PSAD", "Structural Design &\nConstruction", 75, 5, "#366A6F")
        ]
        
        for i, (name, desc, count, hours, color) in enumerate(sections):
            card = self.create_elevation(sections_frame, level=1)
            card.grid(row=0, column=i, sticky="nsew", padx=15, pady=10)
            sections_frame.columnconfigure(i, weight=1)
            sections_frame.rowconfigure(0, weight=1)
            
            inner = tk.Frame(card, bg=self.theme.surface_container, padx=24, pady=24)
            inner.pack(fill="both", expand=True)
            
            # Color indicator
            tk.Frame(inner, bg=color, height=4).pack(fill="x", pady=(0, 20))
            
            tk.Label(inner, text=name, font=("Segoe UI", 20, "bold"),
                    bg=self.theme.surface_container, fg=self.theme.on_surface).pack(anchor="w")
            
            tk.Label(inner, text=desc, font=("Segoe UI", 12),
                    bg=self.theme.surface_container, fg=self.theme.on_surface_variant,
                    justify="left").pack(anchor="w", pady=(8, 20))
            
            stats = tk.Frame(inner, bg=self.theme.surface_container)
            stats.pack(fill="x", pady=(0, 20))
            
            tk.Label(stats, text=f"📝 {count} Questions", font=("Segoe UI", 11),
                    bg=self.theme.surface_container, fg=self.theme.on_surface).pack(side="left")
            
            tk.Label(stats, text=f"⏱️ {hours}h", font=("Segoe UI", 11),
                    bg=self.theme.surface_container, fg=self.theme.on_surface).pack(side="left", padx=(15, 0))
            
            if name in self.section_results:
                score = self.section_results[name]["score_pct"]
                status_text = f"✓ {score:.1f}%"
                btn = self.create_button(inner, status_text, lambda n=name: self.show_section_instructions(n), "text")
            else:
                btn = self.create_button(inner, "Start Section →", lambda n=name: self.show_section_instructions(n), "filled")
            btn.pack(anchor="w", pady=(10, 0))
        
        # Final results button
        if completed == 3:
            final_btn = self.create_button(container, "📊 View Final Results", self.show_final_results, "filled", 200)
            final_btn.pack(pady=30)
    
    # ==================== INSTRUCTIONS ====================
    def show_section_instructions(self, section_name):
        self.current_section = section_name
        
        if not self.questions:
            self.questions = self.load_questions(EXAM_FILE)
        
        self.section_questions = [q for q in self.questions if q["section"] == section_name]
        
        if section_name not in self.all_answers:
            self.all_answers[section_name] = [None] * len(self.section_questions)
        
        if section_name not in self.section_times:
            self.section_times[section_name] = SECTION_TIMES[section_name]
        
        for widget in self.root.winfo_children():
            widget.destroy()
        
        container = tk.Frame(self.root, bg=self.theme.surface)
        container.pack(fill='both', expand=True, padx=40, pady=30)
        
        # Header
        section_titles = {
            "AMSTHEC": "Mathematics, Surveying & Transportation Engineering",
            "HPGE": "Hydraulics & Geotechnical Engineering",
            "PSAD": "Structural Design & Construction"
        }
        
        tk.Label(container, text=section_titles[section_name],
                font=("Segoe UI", 24, "bold"),
                bg=self.theme.surface, fg=self.theme.primary).pack(anchor="w")
        
        tk.Label(container, text="Examination Instructions",
                font=("Segoe UI", 18),
                bg=self.theme.surface, fg=self.theme.on_surface).pack(anchor="w", pady=(5, 20))
        
        # Scrollable content
        canvas = tk.Canvas(container, bg=self.theme.surface, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg=self.theme.surface)
        
        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Quote
        card1 = self.create_elevation(scrollable, level=1)
        card1.pack(fill="x", pady=(0, 20))
        
        inner1 = tk.Frame(card1, bg=self.theme.surface_container, padx=30, pady=25)
        inner1.pack(fill="both", expand=True)
        
        tk.Label(inner1, text="💫 Motivation", font=("Segoe UI", 14, "bold"),
                bg=self.theme.surface_container, fg=self.theme.primary).pack(anchor="w")
        
        quote = random.choice(MOTIVATIONAL_QUOTES)
        tk.Label(inner1, text=f'"{quote}"', font=("Segoe UI", 13, "italic"),
                bg=self.theme.surface_container, fg=self.theme.on_surface,
                justify="left", wraplength=800).pack(anchor="w", pady=(10, 0))
        
        # Instructions
        card2 = self.create_elevation(scrollable, level=1)
        card2.pack(fill="x", pady=(0, 20))
        
        inner2 = tk.Frame(card2, bg=self.theme.surface_container, padx=30, pady=25)
        inner2.pack(fill="both", expand=True)
        
        tk.Label(inner2, text="📋 Examination Guidelines", font=("Segoe UI", 14, "bold"),
                bg=self.theme.surface_container, fg=self.theme.primary).pack(anchor="w", pady=(0, 15))
        
        for instruction in PRC_INSTRUCTIONS:
            tk.Label(inner2, text=f"• {instruction}", font=("Segoe UI", 11),
                    bg=self.theme.surface_container, fg=self.theme.on_surface,
                    justify="left", anchor="w", wraplength=800).pack(anchor="w", pady=5)
        
        # Section info
        card3 = self.create_elevation(scrollable, level=1)
        card3.pack(fill="x", pady=(0, 20))
        
        inner3 = tk.Frame(card3, bg=self.theme.surface_container, padx=30, pady=25)
        inner3.pack(fill="both", expand=True)
        
        tk.Label(inner3, text="📊 Section Details", font=("Segoe UI", 14, "bold"),
                bg=self.theme.surface_container, fg=self.theme.primary).pack(anchor="w", pady=(0, 15))
        
        info_text = [
            f"Total Questions: {len(self.section_questions)}",
            f"Time Allotted: {SECTION_TIMES[section_name] // 3600} hours",
            "Timer starts immediately when you begin",
            "Use the answer sheet on the right to mark your answers",
            "You can change answers anytime before submitting"
        ]
        
        for info in info_text:
            tk.Label(inner3, text=f"• {info}", font=("Segoe UI", 11),
                    bg=self.theme.surface_container, fg=self.theme.on_surface,
                    justify="left", anchor="w").pack(anchor="w", pady=5)
        
        # Buttons
        btn_frame = tk.Frame(container, bg=self.theme.surface)
        btn_frame.pack(fill="x", pady=(20, 0))
        
        back_btn = self.create_button(btn_frame, "← Back", self.show_main_menu, "text")
        back_btn.pack(side="left", padx=5)
        
        start_btn = self.create_button(btn_frame, "Begin Exam →", self.start_section_exam, "filled", 150)
        start_btn.pack(side="left", padx=5)
        
        self.bind_mousewheel(canvas)
    
    # ==================== EXAM INTERFACE ====================
    def start_section_exam(self):
        self.time_left = self.section_times[self.current_section]
        self.show_preload_screen()
        threading.Thread(target=self.preload_images, daemon=True).start()
    
    def show_preload_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        container = tk.Frame(self.root, bg=self.theme.surface)
        container.pack(fill='both', expand=True)
        
        tk.Label(container, text=f"Preparing {self.current_section} Exam",
                font=("Segoe UI", 22, "bold"),
                bg=self.theme.surface, fg=self.theme.primary).pack(pady=(100, 20))
        
        tk.Label(container, text="Loading questions and images...",
                font=("Segoe UI", 14),
                bg=self.theme.surface, fg=self.theme.on_surface_variant).pack(pady=10)
        
        self.preload_progress = ttk.Progressbar(container, mode='determinate',
                                               length=400, style="Custom.Horizontal.TProgressbar")
        self.preload_progress.pack(pady=20)
        
        self.preload_status = tk.Label(container, text="Initializing...",
                                       font=("Segoe UI", 12),
                                       bg=self.theme.surface, fg=self.theme.on_surface_variant)
        self.preload_status.pack(pady=10)
    
    def preload_images(self):
        total = len(self.section_questions)
        if total == 0:
            self.root.after(0, self.show_exam_interface)
            return
        
        for i, q in enumerate(self.section_questions):
            image_url = q.get("figure")
            if not image_url:
                continue
            
            cache_key = f"{image_url}_normal"
            if cache_key in self.image_cache:
                continue
            
            try:
                time.sleep(0.3)
                
                if image_url.startswith(('http://', 'https://')):
                    response = requests.get(image_url, timeout=10)
                    response.raise_for_status()
                    img = Image.open(BytesIO(response.content))
                else:
                    if os.path.exists(image_url):
                        img = Image.open(image_url)
                    else:
                        continue
                
                w, h = img.size
                if w > 700:
                    ratio = 700 / w
                    img = img.resize((int(w * ratio), int(h * ratio)), Image.Resampling.LANCZOS)
                
                photo = ImageTk.PhotoImage(img)
                self.image_cache[cache_key] = photo
            except Exception as e:
                print(f"Failed to load image {i+1}: {e}")
            
            progress = ((i + 1) / total) * 100
            self.root.after(0, lambda p=progress: self.preload_progress.config(value=p))
            self.root.after(0, lambda i=i, t=total: self.preload_status.config(
                text=f"Loaded {i+1}/{t} images..."
            ))
        
        self.root.after(0, self.show_exam_interface)
    
    def show_exam_interface(self):
        self.cancel_timer()
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Top bar
        topbar = tk.Frame(self.root, bg=self.theme.primary, height=64)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)
        
        menu_btn = tk.Button(topbar, text="← Menu", command=self.confirm_exit,
                            bg=self.theme.primary, fg=self.theme.on_primary,
                            font=("Segoe UI", 11, "bold"), relief='flat', cursor="hand2",
                            padx=16, pady=8)
        menu_btn.pack(side="left", padx=16, pady=12)
        
        section_titles = {
            "AMSTHEC": "AMSTHEC",
            "HPGE": "HPGE",
            "PSAD": "PSAD"
        }
        
        tk.Label(topbar, text=section_titles[self.current_section],
                font=("Segoe UI", 16, "bold"),
                bg=self.theme.primary, fg=self.theme.on_primary).pack(side="left", padx=20)
        
        # Timer
        self.timer_label = tk.Label(topbar, text=self.format_time(self.time_left),
                                    font=("Segoe UI", 18, "bold"),
                                    bg=self.theme.primary, fg=self.theme.on_primary)
        self.timer_label.pack(side="right", padx=30)
        
        # Progress
        answered = sum(1 for ans in self.all_answers[self.current_section] if ans is not None)
        self.progress_label = tk.Label(topbar, text=f"{answered}/{len(self.section_questions)}",
                                      font=("Segoe UI", 12, "bold"),
                                      bg=self.theme.primary, fg=self.theme.on_primary)
        self.progress_label.pack(side="right", padx=20)
        
        # Main container
        main = tk.Frame(self.root, bg=self.theme.surface)
        main.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left: Questions
        left = tk.Frame(main, bg=self.theme.surface)
        left.pack(side="left", fill="both", expand=True, padx=(0, 15))
        
        tk.Label(left, text="Questions", font=("Segoe UI", 18, "bold"),
                bg=self.theme.surface, fg=self.theme.on_surface).pack(anchor="w", pady=(0, 15))
        
        q_canvas = tk.Canvas(left, bg=self.theme.surface, highlightthickness=0)
        q_scroll = ttk.Scrollbar(left, orient="vertical", command=q_canvas.yview)
        q_frame = tk.Frame(q_canvas, bg=self.theme.surface)
        
        q_frame.bind("<Configure>", lambda e: q_canvas.configure(scrollregion=q_canvas.bbox("all")))
        q_canvas.create_window((0, 0), window=q_frame, anchor="nw")
        q_canvas.configure(yscrollcommand=q_scroll.set)
        
        q_canvas.pack(side="left", fill="both", expand=True)
        q_scroll.pack(side="right", fill="y")
        
        self.bind_mousewheel(q_canvas)
        
        # Right: Answer sheet
        right = tk.Frame(main, bg=self.theme.surface, width=280)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)
        
        tk.Label(right, text="Answer Sheet", font=("Segoe UI", 16, "bold"),
                bg=self.theme.surface, fg=self.theme.on_surface).pack(pady=(0, 15))
        
        a_canvas = tk.Canvas(right, bg=self.theme.surface, highlightthickness=0)
        a_scroll = ttk.Scrollbar(right, orient="vertical", command=a_canvas.yview)
        a_frame = tk.Frame(a_canvas, bg=self.theme.surface)
        
        a_frame.bind("<Configure>", lambda e: a_canvas.configure(scrollregion=a_canvas.bbox("all")))
        a_canvas.create_window((0, 0), window=a_frame, anchor="nw")
        a_canvas.configure(yscrollcommand=a_scroll.set)
        
        a_canvas.pack(side="left", fill="both", expand=True)
        a_scroll.pack(side="right", fill="y")
        
        self.bind_mousewheel(a_canvas)
        
        # Create answer buttons
        self.answer_buttons = []
        for i in range(len(self.section_questions)):
            row = tk.Frame(a_frame, bg=self.theme.surface)
            row.pack(fill="x", pady=5, padx=10)
            
            tk.Label(row, text=str(i+1), font=("Segoe UI", 11, "bold"),
                    bg=self.theme.surface, fg=self.theme.on_surface,
                    width=3).pack(side="left", padx=(0, 10))
            
            btn_group = []
            for letter in ['A', 'B', 'C', 'D']:
                canvas = tk.Canvas(row, width=36, height=36,
                                  bg=self.theme.surface, highlightthickness=0,
                                  cursor="hand2")
                canvas.pack(side="left", padx=2)
                canvas.create_oval(6, 6, 30, 30,
                                  outline=self.theme.outline,
                                  fill=self.theme.surface, width=2)
                canvas.create_text(18, 18, text=letter,
                                 font=("Segoe UI", 10, "bold"),
                                 fill=self.theme.on_surface)
                
                btn_data = {'canvas': canvas, 'letter': letter, 'index': i}
                btn_group.append(btn_data)
                canvas.bind("<Button-1>", lambda e, d=btn_data: self.select_answer(d))
            
            self.answer_buttons.append(btn_group)
        
        # Create questions
        for i, q in enumerate(self.section_questions):
            card = self.create_elevation(q_frame, level=1)
            card.pack(fill="x", pady=10)
            
            inner = tk.Frame(card, bg=self.theme.surface_container, padx=24, pady=24)
            inner.pack(fill="both", expand=True)
            
            # Header
            header = tk.Frame(inner, bg=self.theme.surface_container)
            header.pack(fill="x", pady=(0, 15))
            
            tk.Label(header, text=f"Question {i+1}",
                    font=("Segoe UI", 14, "bold"),
                    bg=self.theme.surface_container, fg=self.theme.primary).pack(side="left")
            
            # Tags
            tags = tk.Frame(header, bg=self.theme.surface_container)
            tags.pack(side="left", padx=(15, 0))
            
            difficulty = q.get("difficulty")
            if difficulty:
                diff_text = {1: "Easy", 2: "Medium", 3: "Hard"}.get(difficulty, "")
                diff_color = {"Easy": "#4CAF50", "Medium": "#FF9800", "Hard": "#F44336"}.get(diff_text, "#999")
                if diff_text:
                    tk.Label(tags, text=diff_text, font=("Segoe UI", 9, "bold"),
                            bg=diff_color, fg="white", padx=8, pady=2).pack(side="left", padx=2)
            
            if q.get("term"):
                tk.Label(tags, text="TERM", font=("Segoe UI", 9, "bold"),
                        bg="#2196F3", fg="white", padx=8, pady=2).pack(side="left", padx=2)
            
            # Question text
            tk.Label(inner, text=q['stem'], font=("Segoe UI", 12),
                    bg=self.theme.surface_container, fg=self.theme.on_surface,
                    justify="left", wraplength=650).pack(anchor="w", pady=(0, 15))
            
            # Image
            if q.get("figure"):
                self.display_image(inner, q["figure"])
            
            # Choices
            for j, choice in enumerate(q["choices"]):
                letter = chr(65 + j)
                c_frame = tk.Frame(inner, bg=self.theme.surface_container)
                c_frame.pack(fill="x", pady=5)
                
                indicator = tk.Canvas(c_frame, width=24, height=24,
                                     bg=self.theme.surface_container, highlightthickness=0)
                indicator.pack(side="left", padx=(0, 12))
                indicator.create_oval(2, 2, 22, 22,
                                     outline=self.theme.outline,
                                     fill=self.theme.surface_container, width=1)
                indicator.create_text(12, 12, text=letter,
                                    font=("Segoe UI", 10),
                                    fill=self.theme.on_surface)
                
                tk.Label(c_frame, text=choice, font=("Segoe UI", 11),
                        bg=self.theme.surface_container, fg=self.theme.on_surface,
                        justify="left", wraplength=600).pack(side="left", fill="x", expand=True)
        
        # Submit button
        submit_frame = tk.Frame(self.root, bg=self.theme.surface)
        submit_frame.pack(side="bottom", fill="x", pady=20)
        
        submit_btn = self.create_button(submit_frame, "Submit Section →", self.confirm_submit, "filled", 180)
        submit_btn.pack()
        
        self.update_answer_sheet()
        self.start_timer()
    
    def select_answer(self, btn_data):
        i = btn_data['index']
        letter = btn_data['letter']
        self.all_answers[self.current_section][i] = letter
        self.update_answer_sheet()
        self.save_backup()
        
        # Update progress
        answered = sum(1 for ans in self.all_answers[self.current_section] if ans is not None)
        if hasattr(self, 'progress_label') and self.progress_label.winfo_exists():
            self.progress_label.config(text=f"{answered}/{len(self.section_questions)}")
    
    def update_answer_sheet(self):
        for i, btn_group in enumerate(self.answer_buttons):
            user_ans = self.all_answers[self.current_section][i]
            for btn_data in btn_group:
                canvas = btn_data['canvas']
                letter = btn_data['letter']
                canvas.delete("all")
                
                if letter == user_ans:
                    canvas.create_oval(6, 6, 30, 30,
                                     outline=self.theme.primary,
                                     fill=self.theme.primary, width=2)
                    canvas.create_text(18, 18, text=letter,
                                     font=("Segoe UI", 10, "bold"),
                                     fill=self.theme.on_primary)
                else:
                    canvas.create_oval(6, 6, 30, 30,
                                     outline=self.theme.outline,
                                     fill=self.theme.surface, width=2)
                    canvas.create_text(18, 18, text=letter,
                                     font=("Segoe UI", 10, "bold"),
                                     fill=self.theme.on_surface)
    
    def display_image(self, parent, image_url):
        cache_key = f"{image_url}_normal"
        if cache_key in self.image_cache:
            photo = self.image_cache[cache_key]
            img_label = tk.Label(parent, image=photo, bg=parent.cget('bg'))
            img_label.image = photo
            img_label.pack(pady=15)
            return
        
        loading = tk.Label(parent, text="Loading image...",
                          font=("Segoe UI", 10),
                          bg=parent.cget('bg'), fg=self.theme.on_surface_variant)
        loading.pack(pady=10)
    
    # ==================== TIMER ====================
    def start_timer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.update_timer()
    
    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            if self.timer_label and self.timer_label.winfo_exists():
                self.timer_label.config(text=self.format_time(self.time_left))
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            messagebox.showwarning("Time's Up!", f"Time expired for {self.current_section}")
            self.submit_section()
    
    def cancel_timer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
    
    def format_time(self, seconds):
        hrs, rem = divmod(int(seconds), 3600)
        mins, secs = divmod(rem, 60)
        return f"{hrs:02d}:{mins:02d}:{secs:02d}"
    
    # ==================== SUBMISSION & RESULTS ====================
    def confirm_exit(self):
        if messagebox.askyesno("Exit", "Save progress and return to menu?"):
            self.section_times[self.current_section] = self.time_left
            self.cancel_timer()
            self.save_backup()
            self.show_main_menu()
    
    def confirm_submit(self):
        unanswered = sum(1 for ans in self.all_answers[self.current_section] if ans is None)
        if unanswered > 0:
            if not messagebox.askyesno("Confirm", f"You have {unanswered} unanswered questions. Submit anyway?"):
                return
        self.submit_section()
    
    def submit_section(self):
        self.cancel_timer()
        if self.current_section in self.section_times:
            del self.section_times[self.current_section]
        
        answers = self.all_answers[self.current_section]
        correct = 0
        wrong_list = []
        
        for i, q in enumerate(self.section_questions):
            user_ans = answers[i]
            correct_ans = q["correct_answer"]
            if user_ans == correct_ans:
                correct += 1
            else:
                wrong_list.append({
                    "number": i + 1,
                    "stem": q["stem"],
                    "user_answer": user_ans or "No answer",
                    "correct_answer": correct_ans,
                    "choices": q["choices"],
                    "explanation": q.get("explanation", "")
                })
        
        total = len(answers)
        pct = (correct / total) * 100 if total > 0 else 0
        
        self.section_results[self.current_section] = {
            "score_pct": pct,
            "correct": correct,
            "total": total,
            "wrong": wrong_list
        }
        
        self.save_backup()
        self.show_section_result(pct, correct, total, wrong_list)
    
    def show_section_result(self, pct, correct, total, wrong_list):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Top bar
        topbar = tk.Frame(self.root, bg=self.theme.primary, height=64)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)
        
        tk.Label(topbar, text=f"{self.current_section} Results",
                font=("Segoe UI", 18, "bold"),
                bg=self.theme.primary, fg=self.theme.on_primary).pack(side="left", padx=30, pady=15)
        
        container = tk.Frame(self.root, bg=self.theme.surface)
        container.pack(fill="both", expand=True, padx=40, pady=30)
        
        # Summary card
        summary = self.create_elevation(container, level=1)
        summary.pack(fill="x", pady=(0, 25))
        
        inner = tk.Frame(summary, bg=self.theme.surface_container, padx=40, pady=40)
        inner.pack(fill="both", expand=True)
        
        score_color = self.theme.success if pct >= 70 else self.theme.error
        
        tk.Label(inner, text=f"{pct:.1f}%", font=("Segoe UI", 52, "bold"),
                bg=self.theme.surface_container, fg=score_color).pack()
        
        tk.Label(inner, text=f"{correct} / {total} Correct",
                font=("Segoe UI", 18),
                bg=self.theme.surface_container, fg=self.theme.on_surface).pack(pady=(10, 5))
        
        status = "PASSED" if pct >= 70 else "FAILED"
        tk.Label(inner, text=status, font=("Segoe UI", 24, "bold"),
                bg=self.theme.surface_container, fg=score_color).pack(pady=(10, 0))
        
        # Wrong answers
        if wrong_list:
            tk.Label(container, text="Review Wrong Answers",
                    font=("Segoe UI", 18, "bold"),
                    bg=self.theme.surface, fg=self.theme.on_surface).pack(anchor="w", pady=(0, 15))
            
            review_container = tk.Frame(container, bg=self.theme.surface, height=400)
            review_container.pack(fill="both", expand=True, pady=(0, 20))
            
            canvas = tk.Canvas(review_container, bg=self.theme.surface, highlightthickness=0)
            scrollbar = ttk.Scrollbar(review_container, orient="vertical", command=canvas.yview)
            scrollable = tk.Frame(canvas, bg=self.theme.surface)
            
            scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=scrollable, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            self.bind_mousewheel(canvas)
            
            for wrong in wrong_list:
                card = self.create_elevation(scrollable, level=1)
                card.pack(fill="x", pady=10)
                
                inner_card = tk.Frame(card, bg=self.theme.surface_container, padx=25, pady=25)
                inner_card.pack(fill="both", expand=True)
                
                tk.Label(inner_card, text=f"Question {wrong['number']}",
                        font=("Segoe UI", 14, "bold"),
                        bg=self.theme.surface_container, fg=self.theme.primary).pack(anchor="w", pady=(0, 10))
                
                tk.Label(inner_card, text=wrong['stem'], font=("Segoe UI", 11),
                        bg=self.theme.surface_container, fg=self.theme.on_surface,
                        justify="left", wraplength=900).pack(anchor="w", pady=(0, 15))
                
                for j, choice in enumerate(wrong['choices']):
                    letter = chr(65 + j)
                    c_frame = tk.Frame(inner_card, bg=self.theme.surface_container)
                    c_frame.pack(fill="x", pady=4)
                    
                    indicator = tk.Canvas(c_frame, width=24, height=24,
                                         bg=self.theme.surface_container, highlightthickness=0)
                    indicator.pack(side="left", padx=(0, 10))
                    
                    if letter == wrong['user_answer'] and letter != wrong['correct_answer']:
                        indicator.create_oval(2, 2, 22, 22,
                                            outline=self.theme.error,
                                            fill=self.theme.error, width=2)
                        indicator.create_text(12, 12, text="✗",
                                            font=("Segoe UI", 10, "bold"),
                                            fill=self.theme.on_error)
                        choice_color = self.theme.error
                    elif letter == wrong['correct_answer']:
                        indicator.create_oval(2, 2, 22, 22,
                                            outline=self.theme.success,
                                            fill=self.theme.success, width=2)
                        indicator.create_text(12, 12, text="✓",
                                            font=("Segoe UI", 10, "bold"),
                                            fill=self.theme.on_success)
                        choice_color = self.theme.success
                    else:
                        indicator.create_oval(2, 2, 22, 22,
                                            outline=self.theme.outline_variant,
                                            fill=self.theme.surface_container, width=1)
                        indicator.create_text(12, 12, text=letter,
                                            font=("Segoe UI", 9),
                                            fill=self.theme.on_surface_variant)
                        choice_color = self.theme.on_surface
                    
                    tk.Label(c_frame, text=f"{letter}. {choice}", font=("Segoe UI", 11),
                            bg=self.theme.surface_container, fg=choice_color,
                            justify="left", wraplength=850).pack(side="left")
                
                ans_frame = tk.Frame(inner_card, bg=self.theme.surface_container)
                ans_frame.pack(fill="x", pady=(15, 10))
                
                tk.Label(ans_frame, text=f"Your answer: {wrong['user_answer']}",
                        font=("Segoe UI", 11, "bold"),
                        bg=self.theme.surface_container, fg=self.theme.error).pack(side="left", padx=(0, 20))
                
                tk.Label(ans_frame, text=f"Correct: {wrong['correct_answer']}",
                        font=("Segoe UI", 11, "bold"),
                        bg=self.theme.surface_container, fg=self.theme.success).pack(side="left")
                
                if wrong['explanation']:
                    exp_frame = tk.Frame(inner_card, bg=self.theme.surface_container)
                    exp_frame.pack(fill="x", pady=(10, 0))
                    
                    tk.Label(exp_frame, text="💡 Explanation:",
                            font=("Segoe UI", 11, "bold"),
                            bg=self.theme.surface_container, fg=self.theme.primary).pack(anchor="w")
                    
                    tk.Label(exp_frame, text=wrong['explanation'], font=("Segoe UI", 10),
                            bg=self.theme.surface_container, fg=self.theme.on_surface,
                            justify="left", wraplength=900).pack(anchor="w", pady=(5, 0))
        
        # Navigation buttons
        nav = tk.Frame(container, bg=self.theme.surface)
        nav.pack(fill="x", pady=20)
        
        back_btn = self.create_button(nav, "← Back to Menu", self.show_main_menu, "text")
        back_btn.pack(side="left", padx=5)
    
    def show_final_results(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Top bar
        topbar = tk.Frame(self.root, bg=self.theme.primary, height=64)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)
        
        tk.Label(topbar, text="Final Examination Results",
                font=("Segoe UI", 18, "bold"),
                bg=self.theme.primary, fg=self.theme.on_primary).pack(side="left", padx=30, pady=15)
        
        container = tk.Frame(self.root, bg=self.theme.surface)
        container.pack(fill="both", expand=True, padx=40, pady=30)
        
        # Calculate weighted average
        total_weight = sum(req["total"] for req in SECTION_REQUIREMENTS.values())
        weighted_sum = 0
        for section in SECTION_REQUIREMENTS:
            if section in self.section_results:
                weight = SECTION_REQUIREMENTS[section]["total"]
                score = self.section_results[section]["score_pct"]
                weighted_sum += (score * weight)
        
        wa = weighted_sum / total_weight if total_weight > 0 else 0
        
        # Check passing criteria
        section_passed = all(self.section_results[s]["score_pct"] >= 50 for s in SECTION_REQUIREMENTS)
        weighted_passed = wa >= 70
        passed = section_passed and weighted_passed
        
        # Overall result card
        overall = self.create_elevation(container, level=1)
        overall.pack(fill="x", pady=(0, 30))
        
        inner = tk.Frame(overall, bg=self.theme.surface_container, padx=40, pady=40)
        inner.pack(fill="both", expand=True)
        
        status_color = self.theme.success if passed else self.theme.error
        status_text = "PASSED ✓" if passed else "FAILED ✗"
        
        tk.Label(inner, text=status_text, font=("Segoe UI", 40, "bold"),
                bg=self.theme.surface_container, fg=status_color).pack()
        
        tk.Label(inner, text=f"Weighted Average: {wa:.2f}%",
                font=("Segoe UI", 22),
                bg=self.theme.surface_container, fg=self.theme.on_surface).pack(pady=(15, 0))
        
        # Individual sections
        tk.Label(container, text="Section Breakdown",
                font=("Segoe UI", 18, "bold"),
                bg=self.theme.surface, fg=self.theme.on_surface).pack(anchor="w", pady=(0, 20))
        
        sections_frame = tk.Frame(container, bg=self.theme.surface)
        sections_frame.pack(fill="x", pady=(0, 30))
        
        for i, section in enumerate(SECTION_REQUIREMENTS.keys()):
            if section in self.section_results:
                card = self.create_elevation(sections_frame, level=1)
                card.grid(row=0, column=i, sticky="nsew", padx=10)
                sections_frame.columnconfigure(i, weight=1)
                
                inner_card = tk.Frame(card, bg=self.theme.surface_container, padx=20, pady=20)
                inner_card.pack(fill="both", expand=True)
                
                score = self.section_results[section]['score_pct']
                section_passed = score >= 50
                color = self.theme.success if section_passed else self.theme.error
                icon = "✓" if section_passed else "✗"
                
                tk.Label(inner_card, text=section, font=("Segoe UI", 14, "bold"),
                        bg=self.theme.surface_container, fg=self.theme.on_surface).pack()
                
                tk.Label(inner_card, text=f"{score:.1f}%", font=("Segoe UI", 24, "bold"),
                        bg=self.theme.surface_container, fg=color).pack(pady=(10, 5))
                
                tk.Label(inner_card, text=f"{icon} {self.section_results[section]['correct']}/{self.section_results[section]['total']}",
                        font=("Segoe UI", 12),
                        bg=self.theme.surface_container, fg=self.theme.on_surface_variant).pack()
        
        # Navigation
        nav = tk.Frame(container, bg=self.theme.surface)
        nav.pack(fill="x", pady=20)
        
        menu_btn = self.create_button(nav, "← Back to Menu", self.show_main_menu, "text")
        menu_btn.pack(side="left", padx=5)
        
        restart_btn = self.create_button(nav, "🔄 Start New Exam", self.confirm_reset, "filled")
        restart_btn.pack(side="left", padx=5)
    
    # ==================== UTILITIES ====================
    def load_questions(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                questions = json.load(f)
            return [q for q in questions if all(k in q for k in ["stem", "choices", "correct_answer", "section"])]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load questions: {e}")
            return []
    
    def toggle_theme(self):
        self.theme.toggle()
        self.apply_theme()
        self.show_main_menu()
    
    def confirm_reset(self):
        if messagebox.askyesno("Reset", "Start a new exam? All progress will be lost."):
            self.all_answers = {}
            self.section_results = {}
            self.section_times = {}
            self.image_cache = {}
            
            try:
                if os.path.exists(EXAM_FILE):
                    os.remove(EXAM_FILE)
                if os.path.exists(BACKUP_FILE):
                    os.remove(BACKUP_FILE)
            except Exception as e:
                print(f"Cleanup error: {e}")
            
            if generate_exam():
                self.show_main_menu()
            else:
                messagebox.showerror("Error", "Failed to generate new exam")
    
    def bind_mousewheel(self, widget):
        def scroll(event):
            widget.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        def bind_scroll(event):
            widget.bind_all("<MouseWheel>", scroll)
        
        def unbind_scroll(event):
            widget.unbind_all("<MouseWheel>")
        
        widget.bind("<Enter>", bind_scroll)
        widget.bind("<Leave>", unbind_scroll)

# ==================== ENTRY POINT ====================
if __name__ == "__main__":
    root = tk.Tk()
    app = ExamSimulatorApp(root)
    root.mainloop()