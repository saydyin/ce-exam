import json
import random
import tkinter as tk
from tkinter import messagebox, ttk
from collections import defaultdict
import os
from PIL import Image, ImageTk
import math
import time
import requests
from io import BytesIO
import urllib.request
import threading

# ----------------------------
# CONFIGURATION
# ----------------------------
QUESTION_BANK = "question_bank.json"
EXAM_FILE = "questions.json"
BACKUP_FILE = "exam_backup.json"

# Updated section structure with difficulty and term requirements
SECTION_REQUIREMENTS = {
    "MSTE": {
        "total": 75,
        "difficulty": {"easy": 7, "medium": 7, "hard": 7},
        "terms": 5
    },
    "Hydro & Geo": {
        "total": 50,
        "difficulty": {"easy": 5, "medium": 5, "hard": 5},
        "terms": 5
    },
    "Design": {
        "total": 75,
        "difficulty": {"easy": 7, "medium": 7, "hard": 7},
        "terms": 5
    }
}

SECTION_TIMES = {
    "MSTE": 5 * 60 * 60,
    "Hydro & Geo": 4 * 60 * 60,
    "Design": 5 * 60 * 60
}

# Motivational quotes
MOTIVATIONAL_QUOTES = [
    "Success is the sum of small efforts, repeated day in and day out. - Robert Collier",
    "The expert in anything was once a beginner. - Helen Hayes",
    "Your limitation—it's only your imagination.",
    "Push yourself, because no one else is going to do it for you.",
    "Great things never come from comfort zones.",
    "Dream it. Wish it. Do it.",
    "Success doesn't just find you. You have to go out and get it.",
    "The harder you work for something, the greater you'll feel when you achieve it.",
    "Don't stop when you're tired. Stop when you're done.",
    "Wake up with determination. Go to bed with satisfaction."
]

# PRC Exam Instructions
PRC_INSTRUCTIONS = [
    "Read each question carefully before answering.",
    "Manage your time wisely - you have limited time for each section.",
    "Answer all questions to the best of your ability.",
    "You cannot return to previous sections once completed.",
    "The timer will start when you begin the exam section.",
    "Ensure you have a stable internet connection throughout the exam.",
    "No external resources are allowed during the examination.",
    "Double-check your answers before submitting each section.",
    "Use the answer sheet on the right side to mark your answers.",
    "You can change your answers at any time before submitting.",
    "The exam will automatically submit when time expires.",
    "Results will be shown immediately after submitting each section."
]

class MaterialTheme:
    def __init__(self):
        self.is_dark = False
        self.set_light_theme()
    
    def set_light_theme(self):
        self.is_dark = False
        self.primary = "#6750A4"
        self.surface = "#FEF7FF"
        self.surface_container = "#F3EDF7"
        self.on_surface = "#1C1B1F"
        self.on_primary = "#FFFFFF"
        self.outline = "#79747E"
        self.primary_container = "#EADDFF"
        self.on_primary_container = "#21005D"
        self.secondary_container = "#E8DEF8"
        self.tertiary_container = "#FFD8E4"
        self.error = "#B3261E"
        self.on_error = "#FFFFFF"
        self.success = "#0D7813"
        self.warning = "#7D5260"
        self.shadow_color = "#E0E0E0"
    
    def set_dark_theme(self):
        self.is_dark = True
        self.primary = "#D0BCFF"
        self.surface = "#141218"
        self.surface_container = "#211F26"
        self.on_surface = "#E6E1E5"
        self.on_primary = "#381E72"
        self.outline = "#938F99"
        self.primary_container = "#4F378B"
        self.on_primary_container = "#EADDFF"
        self.secondary_container = "#4A4458"
        self.tertiary_container = "#633B48"
        self.error = "#F2B8B5"
        self.on_error = "#601410"
        self.success = "#79DD7A"
        self.warning = "#EFB8C8"
        self.shadow_color = "#2A2A2A"
    
    def toggle(self):
        if self.is_dark:
            self.set_light_theme()
        else:
            self.set_dark_theme()

def generate_exam():
    """Generate exam with improved randomization and difficulty/term tagging"""
    try:
        # Create a simple exam file if question bank doesn't exist
        if not os.path.exists(QUESTION_BANK):
            sample_questions = [
                {
                    "stem": "What is the reaction force R1 for a simply supported beam with 15 kN/m UDL over 10m span?",
                    "figure": "https://i.imgur.com/2s8Q9bL.png",
                    "choices": ["75 kN", "150 kN", "225 kN", "300 kN"],
                    "correct_answer": "A",
                    "section": "MSTE",
                    "difficulty": 2,
                    "explanation": "For a simply supported beam with UDL, reactions are equal: R1 = R2 = (wL)/2 = (15 × 10)/2 = 75 kN"
                },
                {
                    "stem": "A soil has void ratio e = 0.6 and specific gravity G_s = 2.65. What is the porosity?",
                    "figure": "https://i.imgur.com/9z4K7pS.png", 
                    "choices": ["0.375", "0.429", "0.545", "0.625"],
                    "correct_answer": "A",
                    "section": "Hydro & Geo",
                    "difficulty": 2,
                    "explanation": "Porosity n = e / (1 + e) = 0.6 / (1 + 0.6) = 0.375"
                },
                {
                    "stem": "What is the maximum bending moment for a simply supported beam with 15 kN/m UDL over 10m span?",
                    "figure": "https://i.imgur.com/2s8Q9bL.png",
                    "choices": ["187.5 kN·m", "281.25 kN·m", "375 kN·m", "468.75 kN·m"],
                    "correct_answer": "A",
                    "section": "Design",
                    "difficulty": 2,
                    "explanation": "Maximum bending moment = wL²/8 = (15 × 10²)/8 = 187.5 kN·m"
                }
            ]
            with open(QUESTION_BANK, 'w', encoding='utf-8') as f:
                json.dump(sample_questions, f, indent=2, ensure_ascii=False)
            print("Created sample question bank")
        
        with open(QUESTION_BANK, 'r', encoding='utf-8') as f:
            bank = json.load(f)
    except FileNotFoundError:
        messagebox.showerror("Error", f"Question bank not found: {QUESTION_BANK}")
        return False
    except json.JSONDecodeError as e:
        messagebox.showerror("Error", f"Invalid JSON in question bank:\n{e}")
        return False
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error loading question bank:\n{e}")
        return False

    # Use current time for better randomization
    random.seed(time.time() + random.randint(1, 1000000))

    # Validate question structure and categorize
    required_fields = ["stem", "section", "correct_answer", "choices"]
    valid_questions = []
    # Categorize questions by section, difficulty, and terms
    categorized_questions = {
        section: {
            "easy": [],
            "medium": [], 
            "hard": [],
            "terms": [],
            "other": []
        }
        for section in SECTION_REQUIREMENTS
    }

    for q in bank:
        try:
            if not all(field in q for field in required_fields):
                continue
            if q["section"] not in SECTION_REQUIREMENTS:
                continue
            if len(q["choices"]) < 2:
                continue

            section = q["section"]
            difficulty = q.get("difficulty")
            is_term = q.get("term", False)

            # Categorize by difficulty and terms
            if is_term:
                categorized_questions[section]["terms"].append(q)
            elif difficulty == 1:
                categorized_questions[section]["easy"].append(q)
            elif difficulty == 2:
                categorized_questions[section]["medium"].append(q)
            elif difficulty == 3:
                categorized_questions[section]["hard"].append(q)
            else:
                categorized_questions[section]["other"].append(q)

            valid_questions.append(q)
        except Exception as e:
            print(f"Warning: Error processing question: {e}")
            continue

    if not valid_questions:
        messagebox.showerror("Error", "No valid questions found in question bank")
        return False

    final_questions = []
    for section_name, requirements in SECTION_REQUIREMENTS.items():
        if section_name not in categorized_questions:
            # If no questions for this section, use questions from other sections
            all_questions = []
            for other_section in categorized_questions:
                for category in categorized_questions[other_section].values():
                    all_questions.extend(category)
            if not all_questions:
                messagebox.showerror("Error", f"No questions found for any section")
                return False
            random.shuffle(all_questions)
            selected = all_questions[:requirements["total"]]
        else:
            section_data = categorized_questions[section_name]
            selected = []
            target_total = requirements["total"]

            # Select required difficulty questions
            for difficulty, count in requirements["difficulty"].items():
                available = section_data[difficulty][:]
                random.shuffle(available)
                selected.extend(available[:count])

            # Select required term questions
            available_terms = section_data["terms"][:]
            random.shuffle(available_terms)
            term_count = min(requirements["terms"], len(available_terms))
            selected.extend(available_terms[:term_count])

            # Fill remaining slots with other questions
            remaining_slots = target_total - len(selected)
            if remaining_slots > 0:
                # Combine all remaining questions from this section
                all_remaining = []
                for category in ["easy", "medium", "hard", "terms", "other"]:
                    # Only take questions that haven't been selected yet
                    remaining_in_category = [q for q in section_data[category] if q not in selected]
                    all_remaining.extend(remaining_in_category)
                random.shuffle(all_remaining)
                selected.extend(all_remaining[:remaining_slots])

        # Final shuffle and add to final questions
        random.shuffle(selected)
        final_questions.extend(selected[:requirements["total"]])

    try:
        with open(EXAM_FILE, "w", encoding="utf-8") as f:
            json.dump(final_questions, f, indent=2, ensure_ascii=False)
        print(f"Generated exam with {len(final_questions)} questions")
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save exam file:\n{e}")
        return False

class ExamSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Civil Engineering Exam Simulator")
        # Start in fullscreen mode
        self.root.state('zoomed')  # Maximized window
        self.root.minsize(1200, 700)  # Minimum size
        # Configure theme
        self.theme = MaterialTheme()
        self.apply_material_theme()
        self.timer_id = None
        self.timer_label = None
        self.current_section = None
        self.questions = []
        self.all_answers = {}
        self.section_results = {}
        self.section_times = {}  # Store time left for each section
        # Focus mode variables
        self.focus_mode = False
        self.current_focus_question = None
        self.original_scroll_position = {}
        self.focus_container = None
        self.focus_exit_btn = None
        # Image cache for better performance
        self.image_cache = {}
        # Load backup if exists
        self.load_backup()
        # Show loading screen
        self.show_loading_screen()
        # Generate exam in background
        self.root.after(100, self.initialize_app)

    def show_loading_screen(self):
        """Show loading screen while initializing"""
        for widget in self.root.winfo_children():
            widget.destroy()
        loading_frame = tk.Frame(self.root, bg=self.theme.surface)
        loading_frame.pack(fill='both', expand=True)
        tk.Label(loading_frame, text="Civil Engineering Exam Simulator", 
                font=("Segoe UI", 24, "bold"), 
                bg=self.theme.surface, fg=self.theme.primary).pack(pady=50)
        tk.Label(loading_frame, text="Initializing...", 
                font=("Segoe UI", 16), 
                bg=self.theme.surface, fg=self.theme.on_surface).pack(pady=20)
        # Progress bar
        progress_frame = tk.Frame(loading_frame, bg=self.theme.surface)
        progress_frame.pack(pady=20)
        self.loading_progress = ttk.Progressbar(progress_frame, mode='indeterminate', length=300)
        self.loading_progress.pack(pady=10)
        self.loading_progress.start()

    def initialize_app(self):
        """Initialize the app in background to prevent freezing"""
        try:
            success = generate_exam()
            self.loading_progress.stop()
            if success:
                self.root.after(100, self.show_main_menu)
            else:
                self.root.after(100, lambda: messagebox.showerror("Error", "Failed to generate exam. Check question_bank.json"))
        except Exception as e:
            self.loading_progress.stop()
            self.root.after(100, lambda: messagebox.showerror("Error", f"Initialization failed: {e}"))

    def apply_material_theme(self):
        """Apply Material Design 3 theme"""
        self.root.configure(bg=self.theme.surface)
        # Configure ttk style
        style = ttk.Style()
        style.theme_use('clam')
        # Configure notebook style
        style.configure("Material.TNotebook", 
                       background=self.theme.surface,
                       borderwidth=0)
        style.configure("Material.TNotebook.Tab",
                       padding=(20, 8),
                       background=self.theme.surface_container,
                       foreground=self.theme.on_surface,
                       borderwidth=0,
                       focuscolor=self.theme.surface_container)
        style.map("Material.TNotebook.Tab",
                 background=[("selected", self.theme.primary_container)],
                 foreground=[("selected", self.theme.on_primary_container)])

    def create_card(self, parent, elevated=True, padding=20):
        """Create a Material Design card"""
        if elevated:
            shadow_frame = tk.Frame(parent, bg=self.theme.shadow_color)
            shadow_frame.pack(fill='both', expand=True, padx=(0, 2), pady=(0, 2))
            content_frame = tk.Frame(shadow_frame, bg=self.theme.surface_container, padx=padding, pady=padding)
            content_frame.pack(fill='both', expand=True)
            return content_frame, shadow_frame
        else:
            content_frame = tk.Frame(parent, bg=self.theme.surface_container, padx=padding, pady=padding)
            content_frame.pack(fill='both', expand=True)
            return content_frame, None

    def create_material_button(self, parent, text, command, **kwargs):
        """Create a Material Design styled button"""
        bg_color = kwargs.get('bg_color', self.theme.primary)
        fg_color = kwargs.get('fg_color', self.theme.on_primary)
        elevated = kwargs.get('elevated', True)
        width = kwargs.get('width', 120)
        height = kwargs.get('height', 40)
        if elevated:
            btn_container = tk.Frame(parent, bg=parent.cget('bg'))
            shadow = tk.Frame(btn_container, bg=self.theme.shadow_color)
            shadow.pack(fill='both', expand=True, padx=(0, 2), pady=(0, 2))
            btn_frame = tk.Frame(shadow, bg=bg_color)
            btn_frame.pack(fill='both', expand=True)
        else:
            btn_container = tk.Frame(parent, bg=parent.cget('bg'))
            btn_frame = tk.Frame(btn_container, bg=bg_color)
            btn_frame.pack(fill='both', expand=True)

        button = tk.Button(btn_frame, text=text, command=command,
                          bg=bg_color, fg=fg_color, font=("Segoe UI", 10, "bold"),
                          relief='flat', bd=0, cursor="hand2",
                          width=width//8, height=height//20)
        button.pack(fill='both', expand=True, padx=16, pady=8)

        # Bind hover effects
        def on_enter(e):
            if elevated:
                new_color = self.adjust_color(bg_color, -10)
                btn_frame.config(bg=new_color)
                button.config(bg=new_color)
        def on_leave(e):
            btn_frame.config(bg=bg_color)
            button.config(bg=bg_color)

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        return btn_container

    def adjust_color(self, color, amount):
        """Lighten or darken a color"""
        if color.startswith('#'):
            color = color[1:]
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        new_rgb = [max(0, min(255, c + amount)) for c in rgb]
        return f"#{new_rgb[0]:02x}{new_rgb[1]:02x}{new_rgb[2]:02x}"

    def load_backup(self):
        """Load backup data if available"""
        try:
            if os.path.exists(BACKUP_FILE):
                with open(BACKUP_FILE, 'r', encoding='utf-8') as f:
                    backup_data = json.load(f)
                    self.all_answers = backup_data.get('answers', {})
                    self.section_results = backup_data.get('results', {})
                    self.section_times = backup_data.get('times', {})
        except Exception as e:
            print(f"Warning: Could not load backup: {e}")

    def save_backup(self):
        """Save current progress to backup file"""
        try:
            backup_data = {
                'answers': self.all_answers,
                'results': self.section_results,
                'times': self.section_times
            }
            with open(BACKUP_FILE, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save backup: {e}")

    def show_main_menu(self):
        self.cancel_timer()
        for widget in self.root.winfo_children():
            widget.destroy()
        # Main container with responsive padding
        main_container = tk.Frame(self.root, bg=self.theme.surface)
        main_container.pack(fill='both', expand=True, padx=40, pady=30)
        # Header with theme toggle
        header = tk.Frame(main_container, bg=self.theme.surface)
        header.pack(fill="x", pady=(0, 40))
        # App title with Material Design typography
        title_frame = tk.Frame(header, bg=self.theme.surface)
        title_frame.pack(fill="x")
        tk.Label(title_frame, text="Civil Engineering", 
                font=("Segoe UI", 18, "bold"), 
                bg=self.theme.surface, fg=self.theme.on_surface).pack(anchor="w")
        tk.Label(title_frame, text="Exam Simulator", 
                font=("Segoe UI", 28, "bold"), 
                bg=self.theme.surface, fg=self.theme.primary).pack(anchor="w")
        # Progress indicator
        completed = len(self.section_results)
        if completed > 0:
            progress_frame = tk.Frame(header, bg=self.theme.surface)
            progress_frame.pack(fill="x", pady=(20, 0))
            # Progress bar background
            progress_bg = tk.Frame(progress_frame, bg=self.theme.surface_container, height=8)
            progress_bg.pack(fill="x", pady=5)
            # Progress fill
            progress_fill = tk.Frame(progress_bg, bg=self.theme.primary, height=8)
            progress_fill.place(relx=0, rely=0, relwidth=completed/3, relheight=1)
            tk.Label(progress_frame, text=f"Progress: {completed}/3 sections completed", 
                    font=("Segoe UI", 12), 
                    bg=self.theme.surface, fg=self.theme.on_surface).pack()
        # Theme toggle and reset buttons
        button_frame = tk.Frame(header, bg=self.theme.surface)
        button_frame.pack(side="right")
        theme_btn = self.create_material_button(button_frame, "🌓 Toggle Theme", self.toggle_theme,
                                              width=140, elevated=False)
        theme_btn.pack(side="left", padx=5)
        # Reset exam button (only show if there's progress)
        if self.all_answers or self.section_results:
            reset_btn = self.create_material_button(button_frame, "🔄 Reset Exam", self.confirm_reset_exam,
                                                  bg_color=self.theme.error, width=140, elevated=False)
            reset_btn.pack(side="left", padx=5)

        # Sections grid - Use grid layout for better responsiveness
        sections_frame = tk.Frame(main_container, bg=self.theme.surface)
        sections_frame.pack(fill="both", expand=True)
        # Configure grid for responsive layout
        sections_frame.columnconfigure(0, weight=1)
        sections_frame.columnconfigure(1, weight=1)
        sections_frame.columnconfigure(2, weight=1)
        sections_frame.rowconfigure(0, weight=1)

        sections = [
            ("MSTE", "Mathematics, Surveying,\nTransportation Engineering", 75, 5, "#6750A4"),
            ("Hydro & Geo", "Hydraulics and\nGeotechnical Engineering", 50, 4, "#7D5260"),
            ("Design", "Structural Design and\nConstruction", 75, 5, "#366A6F")
        ]

        for i, (name, description, count, hours, color) in enumerate(sections):
            # Create card container
            card_container = tk.Frame(sections_frame, bg=self.theme.surface)
            card_container.grid(row=0, column=i, sticky="nsew", padx=15, pady=10)
            # Create elevated card
            card_content, _ = self.create_card(card_container, elevated=True, padding=24)
            # Section icon/color indicator
            color_indicator = tk.Frame(card_content, bg=color, width=60, height=4)
            color_indicator.pack(anchor="w", pady=(0, 20))
            # Section title
            tk.Label(card_content, text=name, 
                    font=("Segoe UI", 18, "bold"), 
                    bg=self.theme.surface_container, fg=self.theme.on_surface).pack(anchor="w")
            # Section description
            tk.Label(card_content, text=description, 
                    font=("Segoe UI", 12), 
                    bg=self.theme.surface_container, fg=self.theme.outline,
                    justify="left").pack(anchor="w", pady=(8, 20))
            # Stats
            stats_frame = tk.Frame(card_content, bg=self.theme.surface_container)
            stats_frame.pack(fill="x", pady=(0, 25))
            tk.Label(stats_frame, text=f"📝 {count} Questions", 
                    font=("Segoe UI", 11), 
                    bg=self.theme.surface_container, fg=self.theme.on_surface).pack(side="left")
            tk.Label(stats_frame, text=f"⏱️ {hours} Hours", 
                    font=("Segoe UI", 11), 
                    bg=self.theme.surface_container, fg=self.theme.on_surface).pack(side="left", padx=(20, 0))
            # Show time left if section was started but not completed
            time_left = self.section_times.get(name)
            if time_left and name not in self.section_results:
                time_str = self.format_time(time_left)
                tk.Label(stats_frame, text=f"⏰ {time_str} left", 
                        font=("Segoe UI", 10), 
                        bg=self.theme.surface_container, fg=self.theme.primary).pack(side="left", padx=(20, 0))
            # Action button
            status = "✓ Completed" if name in self.section_results else "▶ Start Section"
            btn_bg = self.theme.primary if name not in self.section_results else self.theme.surface_container
            btn_fg = self.theme.on_primary if name not in self.section_results else self.theme.outline
            action_btn = self.create_material_button(card_content, status, 
                                      command=lambda n=name: self.show_section_instructions(n),
                                      bg_color=btn_bg, fg_color=btn_fg,
                                      width=160, height=44, elevated=name not in self.section_results)
            action_btn.pack(anchor="w")

        # Final results button (only when all sections completed)
        if len(self.section_results) == 3:
            results_frame = tk.Frame(main_container, bg=self.theme.surface)
            results_frame.pack(pady=30)
            results_btn = self.create_material_button(results_frame, "📊 View Final Results", 
                                                    self.show_final_results,
                                                    width=220, height=52)
            results_btn.pack()

    def show_section_instructions(self, section_name):
        """Show instructions screen before starting exam section"""
        self.current_section = section_name
        # Load questions if not already loaded
        if not self.questions:
            self.questions = self.load_questions(EXAM_FILE)
        self.section_questions = [q for q in self.questions if q["section"] == section_name]
        # Initialize answers if not exists
        if section_name not in self.all_answers:
            self.all_answers[section_name] = [None] * len(self.section_questions)
        # Set initial time if not exists
        if section_name not in self.section_times:
            self.section_times[section_name] = SECTION_TIMES[section_name]

        for widget in self.root.winfo_children():
            widget.destroy()

        # Main container
        main_container = tk.Frame(self.root, bg=self.theme.surface)
        main_container.pack(fill='both', expand=True, padx=40, pady=30)

        # Header
        header = tk.Frame(main_container, bg=self.theme.surface)
        header.pack(fill="x", pady=(0, 30))
        section_title = {
            "MSTE": "Mathematics, Surveying & Transportation Engineering",
            "Hydro & Geo": "Hydraulics & Geotechnical Engineering", 
            "Design": "Structural Design & Construction"
        }
        tk.Label(header, text=section_title[section_name],
                font=("Segoe UI", 24, "bold"), 
                bg=self.theme.surface, fg=self.theme.primary).pack(anchor="w")
        tk.Label(header, text="Exam Instructions",
                font=("Segoe UI", 18, "bold"), 
                bg=self.theme.surface, fg=self.theme.on_surface).pack(anchor="w", pady=(10, 0))

        # Instructions container with scrollbar
        instructions_container = tk.Frame(main_container, bg=self.theme.surface)
        instructions_container.pack(fill="both", expand=True, pady=(0, 30))

        # Create scrollable frame for instructions
        instructions_canvas = tk.Canvas(instructions_container, bg=self.theme.surface, highlightthickness=0)
        scrollbar = ttk.Scrollbar(instructions_container, orient="vertical", command=instructions_canvas.yview)
        scrollable_frame = tk.Frame(instructions_canvas, bg=self.theme.surface)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: instructions_canvas.configure(scrollregion=instructions_canvas.bbox("all"))
        )
        instructions_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        instructions_canvas.configure(yscrollcommand=scrollbar.set)
        instructions_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self._bind_mousewheel(instructions_canvas)

        # Instructions card inside scrollable frame
        instructions_card, _ = self.create_card(scrollable_frame, elevated=True, padding=30)
        instructions_card.pack(fill="x", pady=(0, 20))

        # Random motivational quote
        quote = random.choice(MOTIVATIONAL_QUOTES)
        quote_frame = tk.Frame(instructions_card, bg=self.theme.surface_container)
        quote_frame.pack(fill="x", pady=(0, 30))
        tk.Label(quote_frame, text="💫 Motivational Quote", 
                font=("Segoe UI", 14, "bold"),
                bg=self.theme.surface_container, fg=self.theme.primary).pack(anchor="w")
        quote_label = tk.Label(quote_frame, text=f'"{quote}"', 
                font=("Segoe UI", 12, "italic"),
                bg=self.theme.surface_container, fg=self.theme.on_surface,
                justify="left", wraplength=0)
        quote_label.pack(anchor="w", pady=(10, 0), fill='x', expand=True)
        def update_wrap(event):
            quote_label.configure(wraplength=event.width - 60)
        quote_frame.bind('<Configure>', update_wrap)

        # PRC Instructions
        instructions_frame = tk.Frame(instructions_card, bg=self.theme.surface_container)
        instructions_frame.pack(fill="x", pady=(0, 30))
        tk.Label(instructions_frame, text="📋 PRC Examination Guidelines", 
                font=("Segoe UI", 14, "bold"),
                bg=self.theme.surface_container, fg=self.theme.primary).pack(anchor="w")
        for instruction in PRC_INSTRUCTIONS:
            instruction_label = tk.Label(instructions_frame, text=f"• {instruction}", 
                    font=("Segoe UI", 11),
                    bg=self.theme.surface_container, fg=self.theme.on_surface,
                    justify="left", anchor="w", wraplength=0)
            instruction_label.pack(anchor="w", pady=(8, 0), fill='x', expand=True)
            def update_instruction_wrap(event, label=instruction_label):
                label.configure(wraplength=event.width - 40)
            instruction_label.bind('<Configure>', update_instruction_wrap)

        # Section specific info
        info_frame = tk.Frame(instructions_card, bg=self.theme.surface_container)
        info_frame.pack(fill="x")
        tk.Label(info_frame, text="📊 Section Information", 
                font=("Segoe UI", 14, "bold"),
                bg=self.theme.surface_container, fg=self.theme.primary).pack(anchor="w")
        info_text = [
            f"Total Questions: {len(self.section_questions)}",
            f"Time Allotted: {SECTION_TIMES[section_name] // 3600} hours",
            f"Timer starts when you click 'Begin Exam'",
            f"You cannot pause the timer once started",
            f"Use the answer sheet on the right side to mark your answers",
            f"Click on A, B, C, or D to select your answer",
            f"You can change answers anytime before submitting",
            f"Exam auto-submits when time expires"
        ]
        for info in info_text:
            info_label = tk.Label(info_frame, text=f"• {info}", 
                    font=("Segoe UI", 11),
                    bg=self.theme.surface_container, fg=self.theme.on_surface,
                    justify="left", anchor="w", wraplength=0)
            info_label.pack(anchor="w", pady=(8, 0), fill='x', expand=True)
            def update_info_wrap(event, label=info_label):
                label.configure(wraplength=event.width - 40)
            info_label.bind('<Configure>', update_info_wrap)

        # Action buttons (outside the scrollable area)
        button_frame = tk.Frame(main_container, bg=self.theme.surface)
        button_frame.pack(fill="x", pady=20)
        back_btn = self.create_material_button(button_frame, "← Back to Menu", 
                                             self.show_main_menu,
                                             width=160, height=44)
        back_btn.pack(side="left")
        start_btn = self.create_material_button(button_frame, "🚀 Begin Exam", 
                                              self.start_section_exam,
                                              width=160, height=44)
        start_btn.pack(side="left", padx=(20, 0))

    # ============= NEW METHODS FOR IMAGE PRELOADING =============
    def start_section_exam(self):
        """Start the exam section with timer after preloading images"""
        self.time_left = self.section_times[self.current_section]
        # Show loading screen while preloading images
        self.show_image_preload_screen()
        # Start image preloading in background thread
        threading.Thread(target=self.preload_section_images, daemon=True).start()

    def show_image_preload_screen(self):
        """Show a loading screen while images are being preloaded"""
        for widget in self.root.winfo_children():
            widget.destroy()
        loading_frame = tk.Frame(self.root, bg=self.theme.surface)
        loading_frame.pack(fill='both', expand=True, padx=40, pady=30)
        tk.Label(loading_frame, text=f"⏳ Preparing {self.current_section} Exam",
                font=("Segoe UI", 20, "bold"),
                bg=self.theme.surface, fg=self.theme.primary).pack(pady=30)
        tk.Label(loading_frame, text="Loading questions and images...",
                font=("Segoe UI", 14),
                bg=self.theme.surface, fg=self.theme.on_surface).pack(pady=10)
        # Progress bar
        self.preload_progress = ttk.Progressbar(loading_frame, mode='determinate', length=400)
        self.preload_progress.pack(pady=20)
        self.preload_progress['value'] = 0
        # Status label
        self.preload_status = tk.Label(loading_frame, text="Initializing...",
                                      font=("Segoe UI", 12),
                                      bg=self.theme.surface, fg=self.theme.outline)
        self.preload_status.pack(pady=10)

    def preload_section_images(self):
        """Preload all images for the current section in background"""
        total_questions = len(self.section_questions)
        if total_questions == 0:
            self.root.after(0, lambda: self.start_exam_interface())
            return

        self.root.after(0, lambda: self.preload_progress.config(value=0))
        self.root.after(0, lambda: self.preload_status.config(text="Loading images..."))

        for i, q in enumerate(self.section_questions):
            image_path_or_url = q.get("figure")
            if not image_path_or_url:
                continue

            cache_key = f"{image_path_or_url}_normal"
            focus_cache_key = f"{image_path_or_url}_focus"

            if cache_key in self.image_cache and focus_cache_key in self.image_cache:
                continue

            try:
                time.sleep(0.5)  # Delay to avoid HTTP 429

                if image_path_or_url.startswith(('http://', 'https://')):
                    try:
                        response = requests.get(image_path_or_url, timeout=10)
                        response.raise_for_status()
                        img_data = BytesIO(response.content)
                        img = Image.open(img_data)
                    except Exception:
                        try:
                            with urllib.request.urlopen(image_path_or_url, timeout=10) as response:
                                img_data = BytesIO(response.read())
                                img = Image.open(img_data)
                        except Exception:
                            continue
                else:
                    if not os.path.exists(image_path_or_url):
                        continue
                    img = Image.open(image_path_or_url)

                # Normal size
                w, h = img.size
                max_width = 600
                if w > max_width:
                    ratio = max_width / w
                    h = int(h * ratio)
                    w = max_width
                    img_normal = img.resize((w, h), Image.Resampling.LANCZOS)
                else:
                    img_normal = img.copy()
                photo_normal = ImageTk.PhotoImage(img_normal)
                self.image_cache[cache_key] = photo_normal

                # Focus size
                w2, h2 = img.size
                max_width_focus = 800
                if w2 > max_width_focus:
                    ratio = max_width_focus / w2
                    h2 = int(h2 * ratio)
                    w2 = max_width_focus
                    img_focus = img.resize((w2, h2), Image.Resampling.LANCZOS)
                else:
                    img_focus = img.copy()
                photo_focus = ImageTk.PhotoImage(img_focus)
                self.image_cache[focus_cache_key] = photo_focus

            except Exception as e:
                print(f"Warning: Failed to preload image for Q{i+1}: {e}")
                continue

            progress = ((i + 1) / total_questions) * 100
            self.root.after(0, lambda p=progress: self.preload_progress.config(value=p))
            self.root.after(0, lambda i=i, t=total_questions: self.preload_status.config(
                text=f"Loaded {i+1}/{t} images..."
            ))

        self.root.after(0, lambda: self.start_exam_interface())

    def start_exam_interface(self):
        """Start the actual exam interface after images are preloaded"""
        self.show_material_exam_interface()
    # ============================================================

    def toggle_theme(self):
        self.theme.toggle()
        self.apply_material_theme()
        self.show_main_menu()

    def confirm_reset_exam(self):
        """Confirm before resetting the entire exam"""
        if messagebox.askyesno("Reset Exam", 
                             "This will delete all your progress and start a new exam. Continue?"):
            self.reset_exam()

    def reset_exam(self):
        """Reset the entire exam with proper cleanup"""
        self.all_answers = {}
        self.section_results = {}
        self.section_times = {}
        self.image_cache = {}  # Clear image cache
        try:
            if os.path.exists(EXAM_FILE):
                os.remove(EXAM_FILE)
            if os.path.exists(BACKUP_FILE):
                os.remove(BACKUP_FILE)
        except Exception as e:
            print(f"Cleanup warning: {e}")
        if generate_exam():
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Failed to generate new exam")

    def _bind_mousewheel(self, canvas):
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

    def display_image(self, parent, image_path_or_url, focus_mode=False):
        """Display image from local file or hosted URL with caching"""
        try:
            cache_key = f"{image_path_or_url}_{focus_mode}"
            if cache_key in self.image_cache:
                photo = self.image_cache[cache_key]
                img_label = tk.Label(parent, image=photo, bg=parent.cget('bg'))
                img_label.image = photo
                img_label.pack(pady=15 if focus_mode else 10)
                return img_label

            loading_label = tk.Label(parent, text="🔄 Loading image...", 
                                   font=("Segoe UI", 10), 
                                   bg=parent.cget('bg'), fg=self.theme.outline)
            loading_label.pack(pady=15 if focus_mode else 10)

            def load_image():
                try:
                    if image_path_or_url.startswith(('http://', 'https://')):
                        try:
                            response = requests.get(image_path_or_url, timeout=10)
                            response.raise_for_status()
                            img_data = BytesIO(response.content)
                            img = Image.open(img_data)
                        except requests.RequestException:
                            try:
                                with urllib.request.urlopen(image_path_or_url, timeout=10) as response:
                                    img_data = BytesIO(response.read())
                                    img = Image.open(img_data)
                            except Exception as url_e:
                                self.root.after(0, lambda p=parent, l=loading_label, e=str(url_e): self.show_image_error(p, l, f"Failed to load from URL: {e}"))
                                return
                    else:
                        if not os.path.exists(image_path_or_url):
                            self.root.after(0, lambda p=parent, l=loading_label, e=image_path_or_url: self.show_image_error(p, l, f"File not found: {e}"))
                            return
                        img = Image.open(image_path_or_url)

                    w, h = img.size
                    max_width = 800 if focus_mode else 600
                    if w > max_width:
                        ratio = max_width / w
                        h = int(h * ratio)
                        w = max_width
                        img = img.resize((w, h), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    self.image_cache[cache_key] = photo
                    self.root.after(0, lambda p=parent, l=loading_label, ph=photo: self.update_image_display(p, l, ph))
                except Exception as e:
                    self.root.after(0, lambda p=parent, l=loading_label, e=str(e): self.show_image_error(p, l, f"Error loading image: {e[:100]}"))

            thread = threading.Thread(target=load_image, daemon=True)
            thread.start()
            return loading_label
        except Exception as e:
            error_label = tk.Label(parent, text=f"⚠️ Error: {str(e)[:100]}", 
                                 fg=self.theme.error, bg=parent.cget('bg'),
                                 font=("Segoe UI", 10))
            error_label.pack(pady=10)
            return error_label

    def show_image_error(self, parent, loading_label, error_msg):
        """Show error message for failed image load"""
        if loading_label and loading_label.winfo_exists():
            loading_label.destroy()
        error_label = tk.Label(parent, text=f"⚠️ {error_msg}", 
                             fg=self.theme.error, bg=parent.cget('bg'),
                             font=("Segoe UI", 10))
        error_label.pack(pady=10)
        return error_label

    def update_image_display(self, parent, loading_label, photo):
        """Update the image display in the main thread"""
        if loading_label and loading_label.winfo_exists():
            loading_label.destroy()
        img_label = tk.Label(parent, image=photo, bg=parent.cget('bg'))
        img_label.image = photo
        img_label.pack(pady=10)

    def show_material_exam_interface(self):
        self.cancel_timer()
        for widget in self.root.winfo_children():
            widget.destroy()

        # Top App Bar
        app_bar = tk.Frame(self.root, bg=self.theme.primary, height=70)
        app_bar.pack(fill="x", padx=0, pady=0)
        app_bar.pack_propagate(False)

        nav_btn = self.create_material_button(app_bar, "← Menu", self.confirm_exit_section,
                                            bg_color=self.theme.primary, 
                                            fg_color=self.theme.on_primary,
                                            elevated=False, width=90, height=40)
        nav_btn.pack(side="left", padx=16, pady=15)

        section_title = {
            "MSTE": "Mathematics, Surveying & Transportation Engineering",
            "Hydro & Geo": "Hydraulics & Geotechnical Engineering", 
            "Design": "Structural Design & Construction"
        }
        title_label = tk.Label(app_bar, text=section_title[self.current_section],
                font=("Segoe UI", 16, "bold"), 
                bg=self.theme.primary, fg=self.theme.on_primary)
        title_label.pack(side="left", padx=20)

        stats_frame = tk.Frame(app_bar, bg=self.theme.primary)
        stats_frame.pack(side="right", padx=20, pady=15)
        answered = sum(1 for ans in self.all_answers[self.current_section] if ans is not None)
        progress_text = f"Answered: {answered}/{len(self.section_questions)}"
        self.progress_label = tk.Label(stats_frame, text=progress_text, 
                font=("Segoe UI", 12, "bold"),
                bg=self.theme.primary, fg=self.theme.on_primary)
        self.progress_label.pack()

        timer_frame = tk.Frame(app_bar, bg=self.theme.primary)
        timer_frame.pack(side="right", padx=30, pady=15)
        self.timer_label = tk.Label(timer_frame, text=self.format_time(self.time_left),
                                   font=("Segoe UI", 16, "bold"), 
                                   fg="#FF6B6B", bg=self.theme.primary)
        self.timer_label.pack()

        main_container = tk.Frame(self.root, bg=self.theme.surface)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        split_container = tk.Frame(main_container, bg=self.theme.surface)
        split_container.pack(fill="both", expand=True)

        questions_frame = tk.Frame(split_container, bg=self.theme.surface)
        questions_frame.pack(side="left", fill="both", expand=True, padx=(0, 15))

        questions_header = tk.Frame(questions_frame, bg=self.theme.surface)
        questions_header.pack(fill="x", pady=(0, 20))
        tk.Label(questions_header, text="Questions", 
                font=("Segoe UI", 18, "bold"),
                bg=self.theme.surface, fg=self.theme.on_surface).pack(side="left")

        focus_btn = self.create_material_button(questions_header, "🔍 Focus Mode", 
                                              self.toggle_focus_mode,
                                              width=140, height=36, elevated=False)
        focus_btn.pack(side="right")

        self.questions_canvas = tk.Canvas(questions_frame, bg=self.theme.surface, highlightthickness=0)
        questions_scrollbar = ttk.Scrollbar(questions_frame, orient="vertical", command=self.questions_canvas.yview)
        self.questions_scrollable = tk.Frame(self.questions_canvas, bg=self.theme.surface)
        self.questions_canvas.create_window((0, 0), window=self.questions_scrollable, anchor="nw")
        self.questions_canvas.configure(yscrollcommand=questions_scrollbar.set)
        self.questions_canvas.pack(side="left", fill="both", expand=True)
        questions_scrollbar.pack(side="right", fill="y")
        self._bind_mousewheel(self.questions_canvas)

        answers_frame = tk.Frame(split_container, bg=self.theme.surface)
        answers_frame.pack(side="right", fill="both", padx=(15, 0))
        answers_frame.config(width=320)

        answers_header = tk.Frame(answers_frame, bg=self.theme.surface)
        answers_header.pack(fill="x", pady=(0, 20))
        tk.Label(answers_header, text="Answer Sheet", 
                font=("Segoe UI", 16, "bold"),
                bg=self.theme.surface, fg=self.theme.on_surface).pack()

        answers_canvas = tk.Canvas(answers_frame, bg=self.theme.surface, highlightthickness=0)
        answers_scrollbar = ttk.Scrollbar(answers_frame, orient="vertical", command=answers_canvas.yview)
        answers_scrollable = tk.Frame(answers_canvas, bg=self.theme.surface)
        answers_canvas.create_window((0, 0), window=answers_scrollable, anchor="nw")
        answers_canvas.configure(yscrollcommand=answers_scrollbar.set)
        answers_canvas.pack(side="left", fill="both", expand=True)
        answers_scrollbar.pack(side="right", fill="y")
        self._bind_mousewheel(answers_canvas)

        self.answer_buttons = []
        for i in range(len(self.section_questions)):
            row_frame = tk.Frame(answers_scrollable, bg=self.theme.surface)
            row_frame.pack(fill="x", padx=10, pady=6)

            q_num_frame = tk.Frame(row_frame, bg=self.theme.surface, width=40, height=35)
            q_num_frame.pack(side="left", padx=(0, 15))
            q_num_frame.pack_propagate(False)
            q_num_label = tk.Label(q_num_frame, text=str(i+1), 
                    font=("Segoe UI", 12, "bold"),
                    bg=self.theme.surface, fg=self.theme.on_surface)
            q_num_label.place(relx=0.5, rely=0.5, anchor="center")

            opt_frame = tk.Frame(row_frame, bg=self.theme.surface)
            opt_frame.pack(side="left", fill="x", expand=True)
            btn_group = []
            for letter in ['A', 'B', 'C', 'D']:
                opt_btn = tk.Canvas(opt_frame, width=32, height=32, 
                                  bg=self.theme.surface, highlightthickness=0,
                                  cursor="hand2")
                opt_btn.pack(side="left", padx=3, fill="x", expand=True)
                opt_btn.create_oval(4, 4, 28, 28, 
                                  outline=self.theme.outline, 
                                  fill=self.theme.surface, 
                                  width=2)
                opt_btn.create_text(16, 16, text=letter, 
                                  font=("Segoe UI", 10, "bold"),
                                  fill=self.theme.on_surface)
                btn_data = {'canvas': opt_btn, 'letter': letter, 'index': i}
                btn_group.append(btn_data)
                opt_btn.bind("<Button-1>", lambda e, data=btn_data: self.select_answer(data))
            self.answer_buttons.append(btn_group)

        self.question_cards = []
        for i, q in enumerate(self.section_questions):
            card_content, shadow_frame = self.create_card(self.questions_scrollable, elevated=True, padding=24)
            self.question_cards.append((card_content, shadow_frame))
            card_content.question_index = i

            header_frame = tk.Frame(card_content, bg=self.theme.surface_container)
            header_frame.pack(fill="x", pady=(0, 16))

            left_header = tk.Frame(header_frame, bg=self.theme.surface_container)
            left_header.pack(side="left")
            tk.Label(left_header, text=f"Question {i+1}", 
                    font=("Segoe UI", 14, "bold"),
                    bg=self.theme.surface_container, fg=self.theme.primary).pack(side="left")

            tags_frame = tk.Frame(left_header, bg=self.theme.surface_container)
            tags_frame.pack(side="left", padx=(15, 0))
            difficulty = q.get("difficulty")
            if difficulty:
                difficulty_text = {1: "Easy", 2: "Medium", 3: "Hard"}.get(difficulty, "")
                if difficulty_text:
                    difficulty_color = {"Easy": "#4CAF50", "Medium": "#FF9800", "Hard": "#F44336"}[difficulty_text]
                    difficulty_tag = tk.Label(tags_frame, text=difficulty_text,
                                            font=("Segoe UI", 9, "bold"),
                                            bg=difficulty_color, fg="white",
                                            padx=8, pady=2)
                    difficulty_tag.pack(side="left", padx=(0, 5))
            if q.get("term"):
                term_tag = tk.Label(tags_frame, text="TERM",
                                  font=("Segoe UI", 9, "bold"),
                                  bg="#2196F3", fg="white",
                                  padx=8, pady=2)
                term_tag.pack(side="left")

            focus_btn = self.create_material_button(header_frame, "🔍 Focus", 
                                                  lambda idx=i: self.enter_focus_mode(idx),
                                                  width=80, height=32, elevated=False)
            focus_btn.pack(side="right")

            stem_label = tk.Label(card_content, text=q['stem'],
                    font=("Segoe UI", 12),
                    bg=self.theme.surface_container, fg=self.theme.on_surface,
                    justify="left", wraplength=0)
            stem_label.pack(anchor="w", pady=(0, 20), fill='x', expand=True)
            def update_stem_wrap(event, label=stem_label):
                label.configure(wraplength=event.width - 60)
            card_content.bind('<Configure>', update_stem_wrap)

            image_label = None
            if q.get("figure"):
                image_label = self.display_image(card_content, q["figure"])

            choice_labels = []
            for j, choice in enumerate(q["choices"]):
                letter = chr(65 + j)
                choice_frame = tk.Frame(card_content, bg=self.theme.surface_container)
                choice_frame.pack(fill="x", pady=6)
                indicator = tk.Canvas(choice_frame, width=26, height=26, 
                                    bg=self.theme.surface_container, highlightthickness=0)
                indicator.pack(side="left", padx=(0, 15))
                indicator.create_oval(3, 3, 23, 23, 
                                    outline=self.theme.outline, 
                                    fill=self.theme.surface_container, 
                                    width=1)
                indicator.create_text(13, 13, text=letter,
                                    font=("Segoe UI", 10),
                                    fill=self.theme.on_surface)
                choice_label = tk.Label(choice_frame, text=choice,
                        font=("Segoe UI", 11),
                        bg=self.theme.surface_container, fg=self.theme.on_surface,
                        justify="left", wraplength=0)
                choice_label.pack(side="left", fill="x", expand=True)
                choice_labels.append(choice_label)
                def update_choice_wrap(event, label=choice_label):
                    label.configure(wraplength=event.width - 50)
                choice_frame.bind('<Configure>', update_choice_wrap)

            card_content.stem_label = stem_label
            card_content.choice_labels = choice_labels
            card_content.image_label = image_label

        submit_frame = tk.Frame(self.root, bg=self.theme.surface)
        submit_frame.pack(side="bottom", fill="x", pady=25)
        submit_btn = self.create_material_button(submit_frame, "📤 Submit Section", 
                                               self.confirm_submit_section,
                                               width=180, height=52)
        submit_btn.pack()

        self.questions_scrollable.bind("<Configure>", lambda e: self.questions_canvas.configure(scrollregion=self.questions_canvas.bbox("all")))
        answers_scrollable.bind("<Configure>", lambda e: answers_canvas.configure(scrollregion=answers_canvas.bbox("all")))

        self.update_answer_sheet()
        self.update_progress_display()
        self.start_timer()

    def toggle_focus_mode(self):
        if self.focus_mode:
            self.exit_focus_mode()
        else:
            messagebox.showinfo("Focus Mode", 
                              "Click the '🔍 Focus' button on any question card to enter focus mode for that question.\n"
                              "In focus mode, the question will be expanded for better readability.")

    def enter_focus_mode(self, question_index):
        if self.focus_mode:
            self.exit_focus_mode()
        self.focus_mode = True
        self.current_focus_question = question_index
        self.original_scroll_position = {
            "x": self.questions_canvas.xview()[0],
            "y": self.questions_canvas.yview()[0]
        }
        self.focus_container = tk.Frame(self.questions_scrollable, bg=self.theme.surface)
        self.focus_container.pack(fill="both", expand=True, pady=10)
        q = self.section_questions[question_index]
        focus_card, focus_shadow = self.create_card(self.focus_container, elevated=True, padding=40)
        focus_card.pack(fill="both", expand=True, pady=20)

        header_frame = tk.Frame(focus_card, bg=self.theme.surface_container)
        header_frame.pack(fill="x", pady=(0, 25))
        tk.Label(header_frame, text=f"Question {question_index + 1} - Focus Mode", 
                font=("Segoe UI", 18, "bold"),
                bg=self.theme.surface_container, fg=self.theme.primary).pack(side="left")

        tags_frame = tk.Frame(header_frame, bg=self.theme.surface_container)
        tags_frame.pack(side="left", padx=(20, 0))
        difficulty = q.get("difficulty")
        if difficulty:
            difficulty_text = {1: "Easy", 2: "Medium", 3: "Hard"}.get(difficulty, "")
            if difficulty_text:
                difficulty_color = {"Easy": "#4CAF50", "Medium": "#FF9800", "Hard": "#F44336"}[difficulty_text]
                difficulty_tag = tk.Label(tags_frame, text=difficulty_text,
                                        font=("Segoe UI", 11, "bold"),
                                        bg=difficulty_color, fg="white",
                                        padx=12, pady=4)
                difficulty_tag.pack(side="left", padx=(0, 10))
        if q.get("term"):
            term_tag = tk.Label(tags_frame, text="TERM",
                              font=("Segoe UI", 11, "bold"),
                              bg="#2196F3", fg="white",
                              padx=12, pady=4)
            term_tag.pack(side="left")

        exit_btn = self.create_material_button(header_frame, "← Exit Focus Mode", 
                                             self.exit_focus_mode,
                                             width=140, height=36, elevated=False)
        exit_btn.pack(side="right")

        stem_label = tk.Label(focus_card, text=q['stem'],
                font=("Segoe UI", 14),
                bg=self.theme.surface_container, fg=self.theme.on_surface,
                justify="left", wraplength=0)
        stem_label.pack(anchor="w", pady=(0, 30), fill='x', expand=True)
        def update_focus_stem_wrap(event):
            stem_label.configure(wraplength=event.width - 100)
        focus_card.bind('<Configure>', update_focus_stem_wrap)

        if q.get("figure"):
            self.display_image(focus_card, q["figure"], focus_mode=True)

        for j, choice in enumerate(q["choices"]):
            letter = chr(65 + j)
            choice_frame = tk.Frame(focus_card, bg=self.theme.surface_container)
            choice_frame.pack(fill="x", pady=10)
            indicator = tk.Canvas(choice_frame, width=32, height=32, 
                                bg=self.theme.surface_container, highlightthickness=0)
            indicator.pack(side="left", padx=(0, 20))
            indicator.create_oval(4, 4, 28, 28, 
                                outline=self.theme.outline, 
                                fill=self.theme.surface_container, 
                                width=2)
            indicator.create_text(16, 16, text=letter,
                                font=("Segoe UI", 12, "bold"),
                                fill=self.theme.on_surface)
            choice_label = tk.Label(choice_frame, text=choice,
                    font=("Segoe UI", 13),
                    bg=self.theme.surface_container, fg=self.theme.on_surface,
                    justify="left", wraplength=0)
            choice_label.pack(side="left", fill="x", expand=True)
            def update_focus_choice_wrap(event, label=choice_label):
                label.configure(wraplength=event.width - 80)
            choice_frame.bind('<Configure>', update_focus_choice_wrap)

        for i, (card_content, shadow_frame) in enumerate(self.question_cards):
            if i != question_index:
                card_content.pack_forget()
                if shadow_frame:
                    shadow_frame.pack_forget()
        self.questions_canvas.yview_moveto(0)

    def exit_focus_mode(self):
        if not self.focus_mode:
            return
        self.focus_mode = False
        self.current_focus_question = None
        if self.focus_container and self.focus_container.winfo_exists():
            self.focus_container.destroy()
            self.focus_container = None
        for i, (card_content, shadow_frame) in enumerate(self.question_cards):
            if card_content and card_content.winfo_exists():
                card_content.pack(fill="x", pady=10)
            if shadow_frame and shadow_frame.winfo_exists():
                shadow_frame.pack(fill="x", pady=10)
        if self.original_scroll_position:
            self.questions_canvas.xview_moveto(self.original_scroll_position["x"])
            self.questions_canvas.yview_moveto(self.original_scroll_position["y"])

    def update_progress_display(self):
        if hasattr(self, 'progress_label') and self.progress_label.winfo_exists():
            answered = sum(1 for ans in self.all_answers[self.current_section] if ans is not None)
            progress_text = f"Answered: {answered}/{len(self.section_questions)}"
            self.progress_label.config(text=progress_text)
        self.root.after(1000, self.update_progress_display)

    def update_answer_sheet(self):
        for i, btn_group in enumerate(self.answer_buttons):
            user_ans = self.all_answers[self.current_section][i]
            for btn_data in btn_group:
                canvas = btn_data['canvas']
                letter = btn_data['letter']
                canvas.delete("all")
                if letter == user_ans:
                    canvas.create_oval(4, 4, 28, 28, 
                                     outline=self.theme.primary, 
                                     fill=self.theme.primary, 
                                     width=2)
                    canvas.create_text(16, 16, text=letter,
                                     font=("Segoe UI", 10, "bold"),
                                     fill=self.theme.on_primary)
                else:
                    canvas.create_oval(4, 4, 28, 28, 
                                     outline=self.theme.outline, 
                                     fill=self.theme.surface, 
                                     width=2)
                    canvas.create_text(16, 16, text=letter,
                                     font=("Segoe UI", 10, "bold"),
                                     fill=self.theme.on_surface)

    def select_answer(self, btn_data):
        i = btn_data['index']
        letter = btn_data['letter']
        self.all_answers[self.current_section][i] = letter
        self.update_answer_sheet()
        self.save_backup()

    def confirm_exit_section(self):
        if messagebox.askyesno("Confirm Exit", 
                             "Your progress and remaining time will be saved. Return to main menu?"):
            self.section_times[self.current_section] = self.time_left
            self.cancel_timer()
            self.save_backup()
            self.show_main_menu()

    def confirm_submit_section(self):
        unanswered = sum(1 for ans in self.all_answers[self.current_section] if ans is None)
        if unanswered > 0:
            msg = f"You have {unanswered} unanswered questions. Submit anyway?"
            if not messagebox.askyesno("Unanswered Questions", msg):
                return
        self.submit_entire_section()

    def format_time(self, seconds):
        hrs, rem = divmod(int(seconds), 3600)
        mins, secs = divmod(rem, 60)
        return f"{hrs:02d}:{mins:02d}:{secs:02d}"

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
            messagebox.showwarning("Time's Up!", f"Time expired for {self.current_section}!")
            self.submit_entire_section()

    def cancel_timer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def submit_entire_section(self):
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
                    "question_number": i + 1,
                    "stem": q["stem"],
                    "user_answer": user_ans or "No answer",
                    "correct_answer": correct_ans,
                    "choices": q["choices"],
                    "explanation": q.get("explanation", "No explanation available.")
                })
        total = len(answers)
        pct = (correct / total) * 100 if total > 0 else 0
        self.section_results[self.current_section] = {
            "score_pct": pct,
            "correct_count": correct,
            "total_count": total,
            "wrong_list": wrong_list
        }
        self.save_backup()
        self.show_detailed_section_result(pct, correct, total, wrong_list)

    def show_detailed_section_result(self, pct, correct, total, wrong_list):
        for widget in self.root.winfo_children():
            widget.destroy()
        app_bar = tk.Frame(self.root, bg=self.theme.primary, height=70)
        app_bar.pack(fill="x", padx=0, pady=0)
        app_bar.pack_propagate(False)
        tk.Label(app_bar, text=f"{self.current_section} - Results",
                font=("Segoe UI", 20, "bold"), 
                bg=self.theme.primary, fg=self.theme.on_primary).pack(side="left", padx=20, pady=20)

        main_container = tk.Frame(self.root, bg=self.theme.surface)
        main_container.pack(fill="both", expand=True, padx=30, pady=25)

        summary_card, _ = self.create_card(main_container, elevated=True, padding=30)
        summary_card.pack(fill="x", pady=(0, 25))

        score_color = self.theme.success if pct >= 70 else self.theme.error
        tk.Label(summary_card, text=f"{pct:.1f}%", 
                font=("Segoe UI", 48, "bold"),
                bg=self.theme.surface_container, fg=score_color).pack()
        tk.Label(summary_card, text=f"Correct: {correct}/{total}", 
                font=("Segoe UI", 18),
                bg=self.theme.surface_container, fg=self.theme.on_surface).pack(pady=(10, 5))

        status_text = "PASS" if pct >= 70 else "FAIL"
        status_color = self.theme.success if pct >= 70 else self.theme.error
        tk.Label(summary_card, text=status_text, 
                font=("Segoe UI", 24, "bold"),
                bg=self.theme.surface_container, fg=status_color).pack(pady=(10, 0))

        if wrong_list:
            review_header = tk.Frame(main_container, bg=self.theme.surface)
            review_header.pack(fill="x", pady=(10, 15))
            tk.Label(review_header, text="Detailed Review", 
                    font=("Segoe UI", 18, "bold"),
                    bg=self.theme.surface, fg=self.theme.on_surface).pack(anchor="w")

            review_container = tk.Frame(main_container, bg=self.theme.surface, height=400)
            review_container.pack(fill="both", expand=True, pady=(0, 20))
            review_canvas = tk.Canvas(review_container, bg=self.theme.surface, highlightthickness=0)
            review_scrollbar = ttk.Scrollbar(review_container, orient="vertical", command=review_canvas.yview)
            review_scrollable = tk.Frame(review_canvas, bg=self.theme.surface)
            review_canvas.create_window((0, 0), window=review_scrollable, anchor="nw")
            review_canvas.configure(yscrollcommand=review_scrollbar.set)
            review_canvas.pack(side="left", fill="both", expand=True)
            review_scrollbar.pack(side="right", fill="y")
            self._bind_mousewheel(review_canvas)

            for wrong in wrong_list:
                question_card, _ = self.create_card(review_scrollable, elevated=True, padding=25)
                question_card.pack(fill="x", pady=10)

                q_header = tk.Frame(question_card, bg=self.theme.surface_container)
                q_header.pack(fill="x", pady=(0, 15))
                tk.Label(q_header, text=f"Question {wrong['question_number']}", 
                        font=("Segoe UI", 14, "bold"),
                        bg=self.theme.surface_container, fg=self.theme.primary).pack(side="left")

                tk.Label(question_card, text=wrong['stem'],
                        font=("Segoe UI", 11),
                        bg=self.theme.surface_container, fg=self.theme.on_surface,
                        justify="left", wraplength=1000).pack(anchor="w", pady=(0, 20))

                for j, choice in enumerate(wrong['choices']):
                    letter = chr(65 + j)
                    choice_frame = tk.Frame(question_card, bg=self.theme.surface_container)
                    choice_frame.pack(fill="x", pady=3)
                    indicator = tk.Canvas(choice_frame, width=26, height=26, 
                                        bg=self.theme.surface_container, highlightthickness=0)
                    indicator.pack(side="left", padx=(0, 12))
                    if letter == wrong['user_answer'] and letter != wrong['correct_answer']:
                        indicator.create_oval(3, 3, 23, 23, 
                                            outline=self.theme.error, 
                                            fill=self.theme.error, 
                                            width=2)
                        indicator.create_text(13, 13, text="✗",
                                            font=("Segoe UI", 10, "bold"),
                                            fill=self.theme.on_error)
                    elif letter == wrong['correct_answer']:
                        indicator.create_oval(3, 3, 23, 23, 
                                            outline=self.theme.success, 
                                            fill=self.theme.success, 
                                            width=2)
                        indicator.create_text(13, 13, text="✓",
                                            font=("Segoe UI", 10, "bold"),
                                            fill=self.theme.on_error)
                    else:
                        indicator.create_oval(3, 3, 23, 23, 
                                            outline=self.theme.outline, 
                                            fill=self.theme.surface_container, 
                                            width=1)
                        indicator.create_text(13, 13, text=letter,
                                            font=("Segoe UI", 9),
                                            fill=self.theme.on_surface)
                    choice_text = f"{letter}. {choice}"
                    choice_color = self.theme.error if (letter == wrong['user_answer'] and letter != wrong['correct_answer']) else self.theme.on_surface
                    if letter == wrong['correct_answer']:
                        choice_color = self.theme.success
                    tk.Label(choice_frame, text=choice_text,
                            font=("Segoe UI", 11),
                            bg=self.theme.surface_container, fg=choice_color,
                            justify="left", wraplength=900).pack(side="left", fill="x", expand=True)

                answer_frame = tk.Frame(question_card, bg=self.theme.surface_container)
                answer_frame.pack(fill="x", pady=(15, 10))
                tk.Label(answer_frame, text=f"Your answer: {wrong['user_answer']}", 
                        font=("Segoe UI", 11, "bold"),
                        bg=self.theme.surface_container, fg=self.theme.error).pack(side="left", padx=(0, 20))
                tk.Label(answer_frame, text=f"Correct answer: {wrong['correct_answer']}", 
                        font=("Segoe UI", 11, "bold"),
                        bg=self.theme.surface_container, fg=self.theme.success).pack(side="left")

                if wrong['explanation']:
                    exp_frame = tk.Frame(question_card, bg=self.theme.surface_container)
                    exp_frame.pack(fill="x", pady=(10, 0))
                    tk.Label(exp_frame, text="Explanation:", 
                            font=("Segoe UI", 11, "bold"),
                            bg=self.theme.surface_container, fg=self.theme.primary).pack(anchor="w")
                    tk.Label(exp_frame, text=wrong['explanation'],
                            font=("Segoe UI", 10),
                            bg=self.theme.surface_container, fg=self.theme.on_surface,
                            justify="left", wraplength=1000).pack(anchor="w", pady=(5, 0))

            review_scrollable.bind("<Configure>", lambda e: review_canvas.configure(scrollregion=review_canvas.bbox("all")))

        nav_frame = tk.Frame(main_container, bg=self.theme.surface)
        nav_frame.pack(fill="x", pady=20)
        back_btn = self.create_material_button(nav_frame, "← Back to Menu", 
                                             self.show_main_menu,
                                             width=160, height=44)
        back_btn.pack(side="left")
        if wrong_list:
            retry_btn = self.create_material_button(nav_frame, "🔄 Retry Section", 
                                                  lambda: self.start_section(self.current_section),
                                                  width=160, height=44)
            retry_btn.pack(side="left", padx=(20, 0))

    def show_final_results(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        app_bar = tk.Frame(self.root, bg=self.theme.primary, height=70)
        app_bar.pack(fill="x", padx=0, pady=0)
        app_bar.pack_propagate(False)
        tk.Label(app_bar, text="Final Exam Results",
                font=("Segoe UI", 20, "bold"), 
                bg=self.theme.primary, fg=self.theme.on_primary).pack(side="left", padx=20, pady=20)

        main_container = tk.Frame(self.root, bg=self.theme.surface)
        main_container.pack(fill="both", expand=True, padx=30, pady=25)

        total_weight = sum(req["total"] for req in SECTION_REQUIREMENTS.values())
        weighted_sum = 0
        for section_name in SECTION_REQUIREMENTS:
            if section_name in self.section_results:
                weight = SECTION_REQUIREMENTS[section_name]["total"]
                score = self.section_results[section_name]["score_pct"]
                weighted_sum += (score * weight)
        wa = weighted_sum / total_weight if total_weight > 0 else 0

        section_passed = all(self.section_results[sec]["score_pct"] >= 50 for sec in SECTION_REQUIREMENTS)
        weighted_passed = wa >= 70
        passed = section_passed and weighted_passed

        overall_card, _ = self.create_card(main_container, elevated=True, padding=30)
        overall_card.pack(fill="x", pady=(0, 25))

        status_color = self.theme.success if passed else self.theme.error
        status_text = "PASS" if passed else "FAIL"
        tk.Label(overall_card, text=status_text, 
                font=("Segoe UI", 36, "bold"),
                bg=self.theme.surface_container, fg=status_color).pack()
        tk.Label(overall_card, text=f"Weighted Average: {wa:.2f}%", 
                font=("Segoe UI", 20),
                bg=self.theme.surface_container, fg=self.theme.on_surface).pack(pady=(10, 20))

        sections_frame = tk.Frame(overall_card, bg=self.theme.surface_container)
        sections_frame.pack(fill="x", pady=10)
        for i, section in enumerate(SECTION_REQUIREMENTS.keys()):
            if section in self.section_results:
                score = self.section_results[section]['score_pct']
                section_passed = score >= 50
                section_color = self.theme.success if section_passed else self.theme.error
                status_icon = "✅" if section_passed else "❌"
                section_frame = tk.Frame(sections_frame, bg=self.theme.surface_container)
                section_frame.grid(row=0, column=i, sticky="nsew", padx=20)
                sections_frame.columnconfigure(i, weight=1)
                tk.Label(section_frame, text=section, 
                        font=("Segoe UI", 14, "bold"),
                        bg=self.theme.surface_container, fg=self.theme.on_surface).pack()
                tk.Label(section_frame, text=f"{status_icon} {score:.1f}%", 
                        font=("Segoe UI", 16, "bold"),
                        bg=self.theme.surface_container, fg=section_color).pack(pady=(5, 0))

        nav_frame = tk.Frame(main_container, bg=self.theme.surface)
        nav_frame.pack(fill="x", pady=20)
        menu_btn = self.create_material_button(nav_frame, "← Back to Menu", 
                                             self.show_main_menu,
                                             width=160, height=44)
        menu_btn.pack(side="left")
        restart_btn = self.create_material_button(nav_frame, "🔄 Restart All", 
                                                self.restart_all,
                                                width=160, height=44)
        restart_btn.pack(side="left", padx=(20, 0))

    def load_questions(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                questions = json.load(f)
            valid_questions = []
            for i, q in enumerate(questions):
                if not all(k in q for k in ["stem", "choices", "correct_answer", "section"]):
                    print(f"Warning: Question {i} missing required fields")
                    continue
                if len(q["choices"]) < 2:
                    print(f"Warning: Question {i} has insufficient choices")
                    continue
                valid_questions.append(q)
            return valid_questions
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load questions: {e}")
            return []

    def start_section(self, section_name):
        self.current_section = section_name
        self.section_times[section_name] = SECTION_TIMES[section_name]
        self.all_answers[section_name] = [None] * len([q for q in self.questions if q["section"] == section_name])
        self.start_section_exam()

    def restart_all(self):
        self.reset_exam()

if __name__ == "__main__":
    root = tk.Tk()
    app = ExamSimulatorApp(root)
    root.mainloop()