import json
import random
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import os
from PIL import Image, ImageTk
import time
import requests
from io import BytesIO
import threading
import platform
from datetime import datetime
import math

# ==================== CONFIGURATION ====================
QUESTION_BANK = "question_bank.json"
EXAM_FILE = "questions.json"
BACKUP_FILE = "exam_backup.json"
SETTINGS_FILE = "settings.json"
BOOKMARKS_FILE = "bookmarks.json"

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

# ==================== SETTINGS MANAGEMENT ====================
class Settings:
    def __init__(self):
        self.settings = {
            "theme": "light",
            "font_size": "medium",
            "auto_save": True,
            "show_explanations": True,
            "timer_alerts": True,
            "screen_scaling": 100,
            "animations": True,
            "study_mode": False,
            "keyboard_shortcuts": True,
            "show_progress": True,
            "confirm_on_exit": True,
            "navigation_mode": "buttons" # "buttons" or "scroll"
        }
        self.load_settings()

    def load_settings(self):
        try:
            if os.path.exists(SETTINGS_FILE):
                with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    self.settings.update(json.load(f))
        except Exception as e:
            print(f"Warning: Could not load settings: {e}")

    def save_settings(self):
        try:
            with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save settings: {e}")

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value
        self.save_settings()

# ==================== BOOKMARKS MANAGEMENT ====================
class Bookmarks:
    def __init__(self):
        self.bookmarks = []
        self.load_bookmarks()

    def load_bookmarks(self):
        try:
            if os.path.exists(BOOKMARKS_FILE):
                with open(BOOKMARKS_FILE, 'r', encoding='utf-8') as f:
                    self.bookmarks = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load bookmarks: {e}")

    def save_bookmarks(self):
        try:
            with open(BOOKMARKS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.bookmarks, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save bookmarks: {e}")

    def add_bookmark(self, section, question_index):
        bookmark_id = f"{section}_{question_index}"
        if bookmark_id not in [b["id"] for b in self.bookmarks]:
            self.bookmarks.append({
                "id": bookmark_id,
                "section": section,
                "question_index": question_index,
                "timestamp": datetime.now().isoformat()
            })
            self.save_bookmarks()
            return True
        return False

    def remove_bookmark(self, bookmark_id):
        self.bookmarks = [b for b in self.bookmarks if b["id"] != bookmark_id]
        self.save_bookmarks()

    def get_bookmarks(self):
        return self.bookmarks

# ==================== MATERIAL 3 THEME ====================
class Material3Theme:
    def __init__(self, settings):
        self.settings = settings
        self.is_dark = settings.get("theme") == "dark"
        self.font_sizes = {
            "small": {"normal": 10, "medium": 12, "large": 14, "xlarge": 16, "xxlarge": 20},
            "medium": {"normal": 12, "medium": 14, "large": 16, "xlarge": 18, "xxlarge": 24},
            "large": {"normal": 14, "medium": 16, "large": 18, "xlarge": 20, "xxlarge": 28}
        }
        self.update_theme()

    def update_theme(self):
        self.is_dark = self.settings.get("theme") == "dark"
        if self.is_dark:
            self.set_dark_theme()
        else:
            self.set_light_theme()

    def set_light_theme(self):
        self.primary = "#6750A4"
        self.on_primary = "#FFFFFF"
        self.primary_container = "#EADDFF"
        self.on_primary_container = "#21005D"
        self.secondary = "#625B71"
        self.on_secondary = "#FFFFFF"
        self.secondary_container = "#E8DEF8"
        self.on_secondary_container = "#1D192B"
        self.tertiary = "#7D5260"
        self.on_tertiary = "#FFFFFF"
        self.tertiary_container = "#FFD8E4"
        self.on_tertiary_container = "#31111D"
        self.error = "#B3261E"
        self.on_error = "#FFFFFF"
        self.error_container = "#FFDAD6"
        self.on_error_container = "#410002"
        self.surface = "#FEF7FF"
        self.surface_dim = "#DED8E1"
        self.surface_bright = "#FFFBFF"
        self.surface_container_lowest = "#FFFFFF"
        self.surface_container_low = "#F7F2FA"
        self.surface_container = "#F3EDF7"
        self.surface_container_high = "#ECE6F0"
        self.surface_container_highest = "#E6DFE9"
        self.on_surface = "#1C1B1F"
        self.on_surface_variant = "#49454F"
        self.outline = "#79747E"
        self.outline_variant = "#CAC4D0"
        self.shadow = "#000000"
        self.scrim = "#000000"
        self.inverse_surface = "#313033"
        self.inverse_on_surface = "#F4EFF4"
        self.inverse_primary = "#D0BCFF"
        self.success = "#1E8E3E"
        self.on_success = "#FFFFFF"
        self.success_container = "#D8FFE8"
        self.on_success_container = "#00210A"
        self.bookmark = "#FFA000"
        self.on_bookmark = "#FFFFFF"

    def set_dark_theme(self):
        self.primary = "#D0BCFF"
        self.on_primary = "#381E72"
        self.primary_container = "#4F378B"
        self.on_primary_container = "#EADDFF"
        self.secondary = "#CCC2DC"
        self.on_secondary = "#332D41"
        self.secondary_container = "#4A4458"
        self.on_secondary_container = "#E8DEF8"
        self.tertiary = "#EFB8C8"
        self.on_tertiary = "#492532"
        self.tertiary_container = "#633B48"
        self.on_tertiary_container = "#FFD8E4"
        self.error = "#F2B8B5"
        self.on_error = "#601410"
        self.error_container = "#8C1D18"
        self.on_error_container = "#FFDAD6"
        self.surface = "#1C1B1F"
        self.surface_dim = "#141218"
        self.surface_bright = "#E5E1E6"
        self.surface_container_lowest = "#09080A"
        self.surface_container_low = "#211F26"
        self.surface_container = "#211F26"
        self.surface_container_high = "#2B2930"
        self.surface_container_highest = "#36343B"
        self.on_surface = "#E6E1E5"
        self.on_surface_variant = "#CAC4D0"
        self.outline = "#938F99"
        self.outline_variant = "#49454F"
        self.shadow = "#000000"
        self.scrim = "#000000"
        self.inverse_surface = "#E6E1E5"
        self.inverse_on_surface = "#313033"
        self.inverse_primary = "#6750A4"
        self.success = "#79DD7A"
        self.on_success = "#0F5223"
        self.success_container = "#0F5223"
        self.on_success_container = "#D8FFE8"
        self.bookmark = "#FFD54F"
        self.on_bookmark = "#000000"

    def toggle(self):
        self.settings.set("theme", "dark" if not self.is_dark else "light")
        self.update_theme()

    def get_font_size(self, size_type="normal"):
        font_size = self.font_sizes.get(self.settings.get("font_size", "medium"), self.font_sizes["medium"])
        return font_size.get(size_type, 12)

# ==================== EXAM GENERATOR ====================
def generate_exam():
    """Generate exam with proper randomization and group_id support"""
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
                },
                {
                    "stem": "Define the term 'bearing capacity' in geotechnical engineering.",
                    "figure": "",
                    "choices": [
                        "The ability of soil to support loads without failure",
                        "The maximum pressure that can be applied to soil",
                        "The pressure at which soil starts to fail",
                        "All of the above"
                    ],
                    "correct_answer": "D",
                    "section": "HPGE",
                    "difficulty": 1,
                    "term": True,
                    "explanation": "Bearing capacity refers to the ability of soil to support loads applied to the ground. It encompasses the maximum pressure that can be applied without causing shear failure, and the pressure at which soil begins to fail."
                },
                {
                    "stem": "What is the term for the ratio of the volume of voids to the total volume of soil?",
                    "figure": "",
                    "choices": ["Void ratio", "Porosity", "Water content", "Degree of saturation"],
                    "correct_answer": "B",
                    "section": "HPGE",
                    "difficulty": 1,
                    "term": True,
                    "explanation": "Porosity is defined as the ratio of the volume of voids to the total volume of soil. It is expressed as a percentage or decimal fraction."
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

        # Select by difficulty
        for difficulty, count in requirements["difficulty"].items():
            available = section_data[difficulty][:]
            random.shuffle(available)
            selected.extend(available[:count])

        # Select terms
        available_terms = section_data["terms"][:]
        random.shuffle(available_terms)
        selected.extend(available_terms[:min(requirements["terms"], len(available_terms))])

        # Fill remaining
        remaining = requirements["total"] - len(selected)
        if remaining > 0:
            all_remaining = []
            for cat in ["easy", "medium", "hard", "terms", "other"]:
                all_remaining.extend([q for q in section_data[cat] if q not in selected])
            random.shuffle(all_remaining)
            selected.extend(all_remaining[:remaining])

        # === GROUPING LOGIC STARTS HERE ===
        # Group by group_id (or assign individual ID if none)
        groups = {}
        for idx, q in enumerate(selected):
            gid = q.get("group_id", f"__single__{idx}")
            if gid not in groups:
                groups[gid] = []
            groups[gid].append(q)

        # Convert to list of groups (each group is a list of questions in original order)
        group_list = list(groups.values())

        # Shuffle the groups (not the questions inside)
        random.shuffle(group_list)

        # Flatten while preserving internal order
        grouped_selected = []
        for group in group_list:
            grouped_selected.extend(group)

        # Shuffle choices for each question (as before)
        for q in grouped_selected:
            if "choices" in q and len(q["choices"]) > 1:
                original_index = ord(q["correct_answer"]) - ord('A')
                if 0 <= original_index < len(q["choices"]):
                    original_correct = q["choices"][original_index]
                    random.shuffle(q["choices"])
                    try:
                        new_index = q["choices"].index(original_correct)
                        q["correct_answer"] = chr(ord('A') + new_index)
                    except ValueError:
                        pass

        final_questions.extend(grouped_selected[:requirements["total"]])

    try:
        with open(EXAM_FILE, "w", encoding="utf-8") as f:
            json.dump(final_questions, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving exam: {e}")
        return False

# ==================== MAIN APPLICATION ====================
# (Rest of the code remains unchanged from your original file)
# We'll now paste the rest of your original code exactly as-is,
# because only `generate_exam()` was modified.

import json
import random
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import os
from PIL import Image, ImageTk
import time
import requests
from io import BytesIO
import threading
import platform
from datetime import datetime
import math

# ... [All the rest of your original ExamSimulatorApp class and main entry point] ...

# But to avoid duplication, we'll just continue from where we left off.
# Since the rest of the code is unchanged, we include it verbatim below.

# ==================== MAIN APPLICATION ====================
class ExamSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Civil Engineering Exam Simulator")
        # Set up app icon
        self.setup_icon()
        # Initialize settings
        self.settings = Settings()
        # Set up scaling based on user settings
        scaling = self.settings.get("screen_scaling", 100) / 100
        if platform.system() == "Windows":
            self.root.tk.call('tk', 'scaling', scaling)
        # Set window size
        self.root.state('zoomed')
        self.root.minsize(1200, 700)
        # Initialize bookmarks
        self.bookmarks = Bookmarks()
        # Initialize theme
        self.theme = Material3Theme(self.settings)
        # Initialize variables
        self.timer_id = None
        self.current_section = None
        self.questions = []
        self.all_answers = {}
        self.section_results = {}
        self.section_times = {}
        self.image_cache = {}
        self.timer_alerts = []
        self.current_question_index = 0
        self.bookmarked_questions = set()
        # Load backup
        self.load_backup()
        # Apply theme
        self.apply_theme()
        # Set up keyboard shortcuts
        if self.settings.get("keyboard_shortcuts", True):
            self.setup_keyboard_shortcuts()
        # Show loading screen
        self.show_loading_screen()
        # Initialize app after a short delay
        self.root.after(100, self.initialize_app)

    def setup_icon(self):
        """Set up a unique application icon"""
        try:
            # Create a simple icon using PIL
            icon_size = (256, 256)
            icon = Image.new('RGBA', icon_size, color=(0, 0, 0, 0))
            # Draw a simple icon
            from PIL import ImageDraw
            draw = ImageDraw.Draw(icon)
            # Background circle
            draw.ellipse([20, 20, 236, 236], fill=(103, 80, 164, 255))
            # Draw a graduation cap
            # Mortarboard
            draw.polygon([50, 100, 206, 100, 180, 150, 76, 150], fill=(255, 255, 255, 255))
            # Tassel
            draw.rectangle([200, 90, 210, 150], fill=(255, 215, 0, 255))
            # Button
            draw.ellipse([115, 140, 141, 166], fill=(255, 215, 0, 255))
            # Save as icon
            icon_path = "exam_icon.ico"
            icon.save(icon_path)
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Could not set icon: {e}")

    def setup_keyboard_shortcuts(self):
        """Set up keyboard shortcuts for navigation"""
        self.root.bind("<Control-n>", lambda e: self.show_main_menu())
        self.root.bind("<Control-s>", lambda e: self.save_backup())
        self.root.bind("<Control-r>", lambda e: self.confirm_reset())
        self.root.bind("<Control-t>", lambda e: self.toggle_theme())
        self.root.bind("<Control-b>", lambda e: self.show_bookmarks())
        self.root.bind("<Control-h>", lambda e: self.show_help())
        self.root.bind("<Escape>", lambda e: self.confirm_exit())
        self.root.bind("<Left>", lambda e: self.navigate_question(-1))
        self.root.bind("<Right>", lambda e: self.navigate_question(1))
        self.root.bind("<Up>", lambda e: self.scroll_up())
        self.root.bind("<Down>", lambda e: self.scroll_down())

    def navigate_question(self, direction):
        """Navigate between questions"""
        if hasattr(self, 'current_question_index'):
            new_index = self.current_question_index + direction
            if 0 <= new_index < len(self.section_questions):
                self.current_question_index = new_index
                self.update_question_display()

    def scroll_up(self):
        """Scroll up in the current view"""
        if hasattr(self, 'q_canvas'):
            self.q_canvas.yview_scroll(-1, "units")
        elif hasattr(self, 'canvas'):
            self.canvas.yview_scroll(-1, "units")

    def scroll_down(self):
        """Scroll down in the current view"""
        if hasattr(self, 'q_canvas'):
            self.q_canvas.yview_scroll(1, "units")
        elif hasattr(self, 'canvas'):
            self.canvas.yview_scroll(1, "units")

    def show_help(self):
        """Show help dialog with keyboard shortcuts"""
        help_text = """Keyboard Shortcuts:
Ctrl+N: Go to Main Menu
Ctrl+S: Save Progress
Ctrl+R: Reset Exam
Ctrl+T: Toggle Theme
Ctrl+B: View Bookmarks
Ctrl+H: Show Help
Esc: Exit Current Section
Left/Right: Navigate Questions
Up/Down: Scroll
Exam Tips:
• Read each question carefully
• Manage your time wisely
• Bookmark difficult questions
• Review your answers before submitting"""
        messagebox.showinfo("Help & Shortcuts", help_text)

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
        """Create Material 3 button with animation"""
        if style == "filled":
            bg, fg = self.theme.primary, self.theme.on_primary
        elif style == "outlined":
            bg, fg = self.theme.surface, self.theme.primary
        elif style == "error":
            bg, fg = self.theme.error, self.theme.on_error
        elif style == "text":
            bg, fg = self.theme.surface, self.theme.primary
        else:
            bg, fg = self.theme.surface_container, self.theme.on_surface

        font_size = self.theme.get_font_size("medium")
        btn = tk.Button(parent, text=text, command=command, bg=bg, fg=fg,
                       font=("Segoe UI", font_size, "bold"), relief='flat', bd=0,
                       cursor="hand2", padx=24, pady=12)

        def on_enter(e):
            if self.settings.get("animations", True):
                # Animate button press
                new_bg = self.adjust_color(bg, -15 if self.theme.is_dark else -10)
                btn.config(bg=new_bg)

        def on_leave(e):
            if self.settings.get("animations", True):
                btn.config(bg=bg)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    def create_fab(self, parent, icon, command, tooltip=""):
        """Create a floating action button"""
        fab = tk.Button(parent, text=icon, command=command,
                       bg=self.theme.primary, fg=self.theme.on_primary,
                       font=("Segoe UI", 16, "bold"), relief='flat', bd=0,
                       cursor="hand2", width=3, height=1)
        if tooltip:
            self.create_tooltip(fab, tooltip)
        return fab

    def create_tooltip(self, widget, text):
        """Create a tooltip for a widget"""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            label = tk.Label(tooltip, text=text, background=self.theme.surface_container,
                           foreground=self.theme.on_surface, relief="solid", borderwidth=1,
                           font=("Segoe UI", self.theme.get_font_size("normal")))
            label.pack()
            widget.tooltip = tooltip

        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip

        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

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
        if not self.settings.get("auto_save", True):
            return
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
        # Create animated logo
        self.logo_frame = tk.Frame(container, bg=self.theme.surface)
        self.logo_frame.pack(pady=(100, 20))
        # Draw animated logo
        self.draw_animated_logo()
        font_size = self.theme.get_font_size("xxlarge")
        tk.Label(container, text="Civil Engineering Exam Simulator",
                font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface, fg=self.theme.primary).pack(pady=(20, 10))
        font_size = self.theme.get_font_size("large")
        tk.Label(container, text="PRC Board Examination Practice System",
                font=("Segoe UI", font_size),
                bg=self.theme.surface, fg=self.theme.on_surface_variant).pack(pady=(0, 20))
        self.loading_progress = ttk.Progressbar(container, mode='indeterminate',
                                               length=300, style="Custom.Horizontal.TProgressbar")
        self.loading_progress.pack(pady=20)
        self.loading_progress.start()
        font_size = self.theme.get_font_size("medium")
        tk.Label(container, text="Initializing exam system...",
                font=("Segoe UI", font_size),
                bg=self.theme.surface, fg=self.theme.on_surface_variant).pack(pady=10)
        # Version info
        font_size = self.theme.get_font_size("normal")
        tk.Label(container, text="Version 2.0",
                font=("Segoe UI", font_size),
                bg=self.theme.surface, fg=self.theme.on_surface_variant).pack(side="bottom", pady=10)

    def draw_animated_logo(self):
        """Draw an animated logo"""
        try:
            # Create a canvas for the logo
            canvas = tk.Canvas(self.logo_frame, width=200, height=200, bg=self.theme.surface, highlightthickness=0)
            canvas.pack()
            # Draw a circle
            circle = canvas.create_oval(20, 20, 180, 180, outline=self.theme.primary, width=3)
            # Draw a graduation cap
            # Mortarboard
            mortarboard = canvas.create_polygon(50, 100, 150, 100, 130, 140, 70, 140,
                                             fill=self.theme.primary, outline="")
            # Tassel
            tassel = canvas.create_rectangle(145, 90, 155, 140, fill=self.theme.bookmark, outline="")
            # Button
            button = canvas.create_oval(90, 130, 110, 150, fill=self.theme.bookmark, outline="")
            # Animate the logo
            self.animate_logo(canvas, circle, mortarboard, tassel, button)
        except Exception as e:
            print(f"Could not draw animated logo: {e}")

    def animate_logo(self, canvas, circle, mortarboard, tassel, button, angle=0):
        """Animate the logo"""
        try:
            # Rotate the tassel
            cx, cy = 150, 100
            length = 50
            x = cx + length * math.cos(math.radians(angle))
            y = cy + length * math.sin(math.radians(angle))
            canvas.coords(tassel, cx-5, cy-5, x, y)
            # Schedule next frame
            angle = (angle + 5) % 360
            canvas.after(50, lambda: self.animate_logo(canvas, circle, mortarboard, tassel, button, angle))
        except Exception as e:
            print(f"Animation error: {e}")

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
        font_size = self.theme.get_font_size("xxlarge")
        tk.Label(header, text="Civil Engineering Exam Simulator",
                font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface, fg=self.theme.primary).pack(anchor="w")
        font_size = self.theme.get_font_size("large")
        tk.Label(header, text="PRC Board Examination Practice System",
                font=("Segoe UI", font_size),
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
            font_size = self.theme.get_font_size("medium")
            tk.Label(progress_frame, text=f"{completed} of 3 sections completed",
                    font=("Segoe UI", font_size, "bold"),
                    bg=self.theme.surface, fg=self.theme.on_surface).pack(pady=(5, 0))
        # Controls
        controls = tk.Frame(header, bg=self.theme.surface)
        controls.pack(side="right", pady=10)
        theme_btn = self.create_button(controls, "🌓 Theme", self.toggle_theme, "text")
        theme_btn.pack(side="left", padx=5)
        settings_btn = self.create_button(controls, "⚙️ Settings", self.show_settings, "text")
        settings_btn.pack(side="left", padx=5)
        bookmarks_btn = self.create_button(controls, "🔖 Bookmarks", self.show_bookmarks, "text")
        bookmarks_btn.pack(side="left", padx=5)
        help_btn = self.create_button(controls, "❓ Help", self.show_help, "text")
        help_btn.pack(side="left", padx=5)
        if self.all_answers or self.section_results:
            reset_btn = self.create_button(controls, "🔄 Reset", self.confirm_reset, "error")
            reset_btn.pack(side="left", padx=5)
        # Mode selection
        mode_frame = tk.Frame(container, bg=self.theme.surface)
        mode_frame.pack(fill="x", pady=(0, 20))
        font_size = self.theme.get_font_size("large")
        tk.Label(mode_frame, text="Select Mode:",
                font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface, fg=self.theme.on_surface).pack(side="left", padx=(0, 20))
        mode_var = tk.StringVar(value="exam")
        exam_radio = tk.Radiobutton(mode_frame, text="Exam Mode", variable=mode_var, value="exam",
                                    bg=self.theme.surface, fg=self.theme.on_surface,
                                    selectcolor=self.theme.primary, activebackground=self.theme.surface,
                                    activeforeground=self.theme.on_surface,
                                    font=("Segoe UI", self.theme.get_font_size("medium")),
                                    command=lambda: self.update_mode("exam"))
        exam_radio.pack(side="left", padx=(0, 20))
        study_radio = tk.Radiobutton(mode_frame, text="Study Mode", variable=mode_var, value="study",
                                    bg=self.theme.surface, fg=self.theme.on_surface,
                                    selectcolor=self.theme.primary, activebackground=self.theme.surface,
                                    activeforeground=self.theme.on_surface,
                                    font=("Segoe UI", self.theme.get_font_size("medium")),
                                    command=lambda: self.update_mode("study"))
        study_radio.pack(side="left")
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
            font_size = self.theme.get_font_size("xlarge")
            tk.Label(inner, text=name, font=("Segoe UI", font_size, "bold"),
                    bg=self.theme.surface_container, fg=self.theme.on_surface).pack(anchor="w")
            font_size = self.theme.get_font_size("medium")
            tk.Label(inner, text=desc, font=("Segoe UI", font_size),
                    bg=self.theme.surface_container, fg=self.theme.on_surface_variant,
                    justify="left").pack(anchor="w", pady=(8, 20))
            stats = tk.Frame(inner, bg=self.theme.surface_container)
            stats.pack(fill="x", pady=(0, 20))
            font_size = self.theme.get_font_size("normal")
            tk.Label(stats, text=f"📝 {count} Questions", font=("Segoe UI", font_size),
                    bg=self.theme.surface_container, fg=self.theme.on_surface).pack(side="left")
            tk.Label(stats, text=f"⏱️ {hours}h", font=("Segoe UI", font_size),
                    bg=self.theme.surface_container, fg=self.theme.on_surface).pack(side="left", padx=(15, 0))
            # Progress bar for completed sections
            if name in self.section_results:
                score = self.section_results[name]["score_pct"]
                status_text = f"✓ {score:.1f}%"
                btn = self.create_button(inner, status_text, lambda n=name: self.show_section_instructions(n), "text")
                # Add progress bar
                progress_bg = tk.Frame(inner, bg=self.theme.outline_variant, height=6)
                progress_bg.pack(fill="x", pady=(10, 0))
                progress_color = self.theme.success if score >= 70 else self.theme.error
                progress_fill = tk.Frame(progress_bg, bg=progress_color, height=6)
                progress_fill.place(relx=0, rely=0, relwidth=score/100, relheight=1)
            else:
                btn = self.create_button(inner, "Start Section →", lambda n=name: self.show_section_instructions(n), "filled")
            btn.pack(anchor="w", pady=(10, 0))
        # Final results button
        if completed == 3:
            final_btn = self.create_button(container, "📊 View Final Results", self.show_final_results, "filled", 200)
            final_btn.pack(pady=30)
        # Floating action buttons
        fab_frame = tk.Frame(self.root, bg=self.theme.surface)
        fab_frame.place(relx=0.98, rely=0.9, anchor="se")
        self.create_fab(fab_frame, "📊", self.show_analytics, "Performance Analytics").pack(pady=5)
        self.create_fab(fab_frame, "🔖", self.show_bookmarks, "Bookmarks").pack(pady=5)

    def update_mode(self, mode):
        """Update the application mode"""
        self.settings.set("study_mode", mode == "study")

    # ==================== BOOKMARKS ====================
    def show_bookmarks(self):
        """Show bookmarked questions"""
        self.cancel_timer()
        for widget in self.root.winfo_children():
            widget.destroy()
        container = tk.Frame(self.root, bg=self.theme.surface)
        container.pack(fill='both', expand=True, padx=40, pady=30)
        # Header
        header = tk.Frame(container, bg=self.theme.surface)
        header.pack(fill="x", pady=(0, 20))
        font_size = self.theme.get_font_size("xxlarge")
        tk.Label(header, text="Bookmarked Questions",
                font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface, fg=self.theme.primary).pack(anchor="w")
        # Back button
        back_btn = self.create_button(header, "← Back", self.show_main_menu, "text")
        back_btn.pack(side="right")
        # Bookmarks list
        bookmarks = self.bookmarks.get_bookmarks()
        if not bookmarks:
            empty_frame = tk.Frame(container, bg=self.theme.surface)
            empty_frame.pack(fill="both", expand=True)
            font_size = self.theme.get_font_size("large")
            tk.Label(empty_frame, text="No bookmarks yet",
                    font=("Segoe UI", font_size),
                    bg=self.theme.surface, fg=self.theme.on_surface_variant).pack(pady=100)
            font_size = self.theme.get_font_size("medium")
            tk.Label(empty_frame, text="Bookmark questions during your exam to review them later",
                    font=("Segoe UI", font_size),
                    bg=self.theme.surface, fg=self.theme.on_surface_variant).pack()
            return
        # Scrollable content
        canvas = tk.Canvas(container, bg=self.theme.surface, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg=self.theme.surface)
        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.bind_mousewheel(canvas)
        # Load questions for bookmarked items
        if not self.questions:
            self.questions = self.load_questions(EXAM_FILE)
        # Display bookmarks
        for bookmark in bookmarks:
            section = bookmark["section"]
            question_index = bookmark["question_index"]
            # Find the question
            section_questions = [q for q in self.questions if q["section"] == section]
            if question_index < len(section_questions):
                question = section_questions[question_index]
                card = self.create_elevation(scrollable, level=1)
                card.pack(fill="x", pady=10)
                inner = tk.Frame(card, bg=self.theme.surface_container, padx=20, pady=20)
                inner.pack(fill="both", expand=True)
                # Header
                header_frame = tk.Frame(inner, bg=self.theme.surface_container)
                header_frame.pack(fill="x", pady=(0, 10))
                font_size = self.theme.get_font_size("large")
                tk.Label(header_frame, text=f"{section} - Question {question_index + 1}",
                        font=("Segoe UI", font_size, "bold"),
                        bg=self.theme.surface_container, fg=self.theme.primary).pack(side="left")
                # Remove bookmark button
                remove_btn = tk.Button(header_frame, text="Remove",
                                      command=lambda b=bookmark["id"]: self.remove_bookmark(b),
                                      bg=self.theme.error, fg=self.theme.on_error,
                                      font=("Segoe UI", self.theme.get_font_size("normal"), "bold"),
                                      relief='flat', cursor="hand2", padx=10, pady=5)
                remove_btn.pack(side="right")
                # Question text
                font_size = self.theme.get_font_size("medium")
                tk.Label(inner, text=question['stem'], font=("Segoe UI", font_size),
                        bg=self.theme.surface_container, fg=self.theme.on_surface,
                        justify="left", wraplength=800).pack(anchor="w", pady=(0, 10))
                # Answer (if available)
                if section in self.all_answers and question_index < len(self.all_answers[section]):
                    user_answer = self.all_answers[section][question_index]
                    if user_answer:
                        font_size = self.theme.get_font_size("normal")
                        tk.Label(inner, text=f"Your answer: {user_answer}",
                                font=("Segoe UI", font_size, "bold"),
                                bg=self.theme.surface_container, fg=self.theme.on_surface).pack(anchor="w")
                # View button
                view_btn = self.create_button(inner, "View Question",
                                            lambda s=section, i=question_index: self.view_bookmarked_question(s, i),
                                            "text", 120)
                view_btn.pack(anchor="w", pady=(10, 0))

    def view_bookmarked_question(self, section, question_index):
        """View a specific bookmarked question"""
        # Set the current section and question index
        self.current_section = section
        if not self.questions:
            self.questions = self.load_questions(EXAM_FILE)
        self.section_questions = [q for q in self.questions if q["section"] == section]
        self.current_question_index = question_index
        # Show the question viewer
        self.show_question_viewer()

    def remove_bookmark(self, bookmark_id):
        """Remove a bookmark"""
        self.bookmarks.remove_bookmark(bookmark_id)
        self.show_bookmarks() # Refresh the bookmarks view

    def toggle_bookmark(self):
        """Toggle bookmark for the current question"""
        bookmark_id = f"{self.current_section}_{self.current_question_index}"
        if bookmark_id in [b["id"] for b in self.bookmarks.get_bookmarks()]:
            # Remove bookmark
            self.bookmarks.remove_bookmark(bookmark_id)
            if hasattr(self, 'bookmark_btn'):
                self.bookmark_btn.config(text="🔖", bg=self.theme.surface_container)
        else:
            # Add bookmark
            if self.bookmarks.add_bookmark(self.current_section, self.current_question_index):
                if hasattr(self, 'bookmark_btn'):
                    self.bookmark_btn.config(text="🔖", bg=self.theme.bookmark)

    # ==================== ANALYTICS ====================
    def show_analytics(self):
        """Show performance analytics"""
        self.cancel_timer()
        for widget in self.root.winfo_children():
            widget.destroy()
        container = tk.Frame(self.root, bg=self.theme.surface)
        container.pack(fill='both', expand=True, padx=40, pady=30)
        # Header
        header = tk.Frame(container, bg=self.theme.surface)
        header.pack(fill="x", pady=(0, 20))
        font_size = self.theme.get_font_size("xxlarge")
        tk.Label(header, text="Performance Analytics",
                font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface, fg=self.theme.primary).pack(anchor="w")
        # Back button
        back_btn = self.create_button(header, "← Back", self.show_main_menu, "text")
        back_btn.pack(side="right")
        # Export button
        export_btn = self.create_button(header, "Export Results", self.export_results, "filled")
        export_btn.pack(side="right", padx=10)
        # Calculate overall statistics
        total_questions = 0
        total_correct = 0
        section_stats = {}
        for section, req in SECTION_REQUIREMENTS.items():
            if section in self.section_results:
                result = self.section_results[section]
                correct = result["correct"]
                total = result["total"]
                pct = result["score_pct"]
                total_questions += total
                total_correct += correct
                section_stats[section] = {
                    "correct": correct,
                    "total": total,
                    "percentage": pct,
                    "passed": pct >= 70
                }
        overall_pct = (total_correct / total_questions * 100) if total_questions > 0 else 0
        # Overall stats card
        overall_card = self.create_elevation(container, level=1)
        overall_card.pack(fill="x", pady=(0, 20))
        overall_inner = tk.Frame(overall_card, bg=self.theme.surface_container, padx=30, pady=30)
        overall_inner.pack(fill="both", expand=True)
        font_size = self.theme.get_font_size("large")
        tk.Label(overall_inner, text="Overall Performance",
                font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface_container, fg=self.theme.primary).pack(anchor="w", pady=(0, 15))
        stats_frame = tk.Frame(overall_inner, bg=self.theme.surface_container)
        stats_frame.pack(fill="x")
        # Overall score
        score_frame = tk.Frame(stats_frame, bg=self.theme.surface_container)
        score_frame.pack(side="left", fill="both", expand=True, padx=10)
        font_size = self.theme.get_font_size("xxlarge")
        score_color = self.theme.success if overall_pct >= 70 else self.theme.error
        tk.Label(score_frame, text=f"{overall_pct:.1f}%",
                font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface_container, fg=score_color).pack()
        font_size = self.theme.get_font_size("medium")
        tk.Label(score_frame, text=f"{total_correct}/{total_questions} Correct",
                font=("Segoe UI", font_size),
                bg=self.theme.surface_container, fg=self.theme.on_surface).pack()
        # Progress visualization
        progress_frame = tk.Frame(stats_frame, bg=self.theme.surface_container)
        progress_frame.pack(side="left", fill="both", expand=True, padx=10)
        font_size = self.theme.get_font_size("large")
        tk.Label(progress_frame, text="Progress",
                font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface_container, fg=self.theme.primary).pack(anchor="w")
        # Progress bars for each section
        for section, stats in section_stats.items():
            section_frame = tk.Frame(progress_frame, bg=self.theme.surface_container)
            section_frame.pack(fill="x", pady=5)
            font_size = self.theme.get_font_size("medium")
            tk.Label(section_frame, text=section, font=("Segoe UI", font_size),
                    bg=self.theme.surface_container, fg=self.theme.on_surface,
                    width=10, anchor="w").pack(side="left")
            # Progress bar
            bar_bg = tk.Frame(section_frame, bg=self.theme.outline_variant, height=10)
            bar_bg.pack(side="left", fill="x", expand=True, padx=(10, 0))
            bar_color = self.theme.success if stats["passed"] else self.theme.error
            bar_fill = tk.Frame(bar_bg, bg=bar_color, height=10)
            bar_fill.place(relx=0, rely=0, relwidth=stats["percentage"]/100, relheight=1)
            # Percentage
            font_size = self.theme.get_font_size("normal")
            tk.Label(section_frame, text=f"{stats['percentage']:.1f}%", font=("Segoe UI", font_size),
                    bg=self.theme.surface_container, fg=self.theme.on_surface,
                    width=6).pack(side="right")
        # Section breakdown
        font_size = self.theme.get_font_size("xlarge")
        tk.Label(container, text="Section Breakdown",
                font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface, fg=self.theme.on_surface).pack(anchor="w", pady=(20, 10))
        sections_grid = tk.Frame(container, bg=self.theme.surface)
        sections_grid.pack(fill="both", expand=True)
        for i, (section, stats) in enumerate(section_stats.items()):
            card = self.create_elevation(sections_grid, level=1)
            card.grid(row=0, column=i, sticky="nsew", padx=10, pady=10)
            sections_grid.columnconfigure(i, weight=1)
            inner = tk.Frame(card, bg=self.theme.surface_container, padx=20, pady=20)
            inner.pack(fill="both", expand=True)
            # Section name
            font_size = self.theme.get_font_size("large")
            tk.Label(inner, text=section, font=("Segoe UI", font_size, "bold"),
                    bg=self.theme.surface_container, fg=self.theme.on_surface).pack()
            # Score
            font_size = self.theme.get_font_size("xlarge")
            score_color = self.theme.success if stats["passed"] else self.theme.error
            tk.Label(inner, text=f"{stats['percentage']:.1f}%",
                    font=("Segoe UI", font_size, "bold"),
                    bg=self.theme.surface_container, fg=score_color).pack(pady=(10, 5))
            # Details
            font_size = self.theme.get_font_size("medium")
            tk.Label(inner, text=f"{stats['correct']}/{stats['total']} Correct",
                    font=("Segoe UI", font_size),
                    bg=self.theme.surface_container, fg=self.theme.on_surface).pack()
            # Status
            status = "PASSED" if stats["passed"] else "FAILED"
            font_size = self.theme.get_font_size("normal")
            tk.Label(inner, text=status, font=("Segoe UI", font_size, "bold"),
                    bg=self.theme.surface_container, fg=score_color).pack(pady=(5, 0))

    def export_results(self):
        """Export results to a file"""
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Export Results"
            )
            if file_path:
                export_data = {
                    "timestamp": datetime.now().isoformat(),
                    "overall_percentage": 0,
                    "sections": {}
                }
                # Calculate overall percentage
                total_correct = 0
                total_questions = 0
                for section, result in self.section_results.items():
                    total_correct += result["correct"]
                    total_questions += result["total"]
                    export_data["sections"][section] = {
                        "percentage": result["score_pct"],
                        "correct": result["correct"],
                        "total": result["total"],
                        "wrong_answers": result["wrong"]
                    }
                export_data["overall_percentage"] = (total_correct / total_questions * 100) if total_questions > 0 else 0
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("Export Successful", f"Results exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export results: {e}")

    # ==================== SETTINGS MENU ====================
    def show_settings(self):
        self.cancel_timer()
        for widget in self.root.winfo_children():
            widget.destroy()
        container = tk.Frame(self.root, bg=self.theme.surface)
        container.pack(fill='both', expand=True, padx=40, pady=30)
        # Header
        header = tk.Frame(container, bg=self.theme.surface)
        header.pack(fill="x", pady=(0, 30))
        font_size = self.theme.get_font_size("xxlarge")
        tk.Label(header, text="Settings",
                font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface, fg=self.theme.primary).pack(anchor="w")
        # Back button
        back_btn = self.create_button(header, "← Back", self.show_main_menu, "text")
        back_btn.pack(side="right")
        # Settings container with notebook for tabs
        notebook = ttk.Notebook(container)
        notebook.pack(fill="both", expand=True)
        # General tab
        general_frame = tk.Frame(notebook, bg=self.theme.surface)
        notebook.add(general_frame, text="General")
        # Theme setting
        theme_card = self.create_elevation(general_frame, level=1)
        theme_card.pack(fill="x", pady=15, padx=10)
        theme_inner = tk.Frame(theme_card, bg=self.theme.surface_container, padx=24, pady=20)
        theme_inner.pack(fill="both", expand=True)
        font_size = self.theme.get_font_size("large")
        tk.Label(theme_inner, text="Theme",
                font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface_container, fg=self.theme.on_surface).pack(anchor="w", pady=(0, 10))
        theme_options = tk.Frame(theme_inner, bg=self.theme.surface_container)
        theme_options.pack(fill="x")
        theme_var = tk.StringVar(value=self.settings.get("theme", "light"))
        light_radio = tk.Radiobutton(theme_options, text="Light Theme", variable=theme_var, value="light",
                                    bg=self.theme.surface_container, fg=self.theme.on_surface,
                                    selectcolor=self.theme.primary, activebackground=self.theme.surface_container,
                                    activeforeground=self.theme.on_surface,
                                    font=("Segoe UI", self.theme.get_font_size("medium")),
                                    command=lambda: self.update_setting("theme", theme_var.get()))
        light_radio.pack(side="left", padx=(0, 20))
        dark_radio = tk.Radiobutton(theme_options, text="Dark Theme", variable=theme_var, value="dark",
                                   bg=self.theme.surface_container, fg=self.theme.on_surface,
                                   selectcolor=self.theme.primary, activebackground=self.theme.surface_container,
                                   activeforeground=self.theme.on_surface,
                                   font=("Segoe UI", self.theme.get_font_size("medium")),
                                   command=lambda: self.update_setting("theme", theme_var.get()))
        dark_radio.pack(side="left")
        # Font size setting
        font_card = self.create_elevation(general_frame, level=1)
        font_card.pack(fill="x", pady=15, padx=10)
        font_inner = tk.Frame(font_card, bg=self.theme.surface_container, padx=24, pady=20)
        font_inner.pack(fill="both", expand=True)
        font_size = self.theme.get_font_size("large")
        tk.Label(font_inner, text="Font Size",
                font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface_container, fg=self.theme.on_surface).pack(anchor="w", pady=(0, 10))
        font_options = tk.Frame(font_inner, bg=self.theme.surface_container)
        font_options.pack(fill="x")
        font_var = tk.StringVar(value=self.settings.get("font_size", "medium"))
        for size, label in [("small", "Small"), ("medium", "Medium"), ("large", "Large")]:
            radio = tk.Radiobutton(font_options, text=label, variable=font_var, value=size,
                                 bg=self.theme.surface_container, fg=self.theme.on_surface,
                                 selectcolor=self.theme.primary, activebackground=self.theme.surface_container,
                                 activeforeground=self.theme.on_surface,
                                 font=("Segoe UI", self.theme.get_font_size("medium")),
                                 command=lambda s=size: self.update_setting("font_size", s))
            radio.pack(side="left", padx=(0, 20))
        # Screen scaling setting
        scale_card = self.create_elevation(general_frame, level=1)
        scale_card.pack(fill="x", pady=15, padx=10)
        scale_inner = tk.Frame(scale_card, bg=self.theme.surface_container, padx=24, pady=20)
        scale_inner.pack(fill="both", expand=True)
        font_size = self.theme.get_font_size("large")
        tk.Label(scale_inner, text="Screen Scaling",
                font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface_container, fg=self.theme.on_surface).pack(anchor="w", pady=(0, 10))
        scale_frame = tk.Frame(scale_inner, bg=self.theme.surface_container)
        scale_frame.pack(fill="x")
        scale_var = tk.IntVar(value=self.settings.get("screen_scaling", 100))
        scale_label = tk.Label(scale_frame, text=f"{scale_var.get()}%",
                              font=("Segoe UI", self.theme.get_font_size("medium")),
                              bg=self.theme.surface_container, fg=self.theme.on_surface)
        scale_label.pack(side="left", padx=(0, 20))
        scale_slider = ttk.Scale(scale_frame, from_=80, to=120, orient="horizontal",
                                variable=scale_var, length=200,
                                command=lambda v: self.update_scale(scale_label, int(float(v))))
        scale_slider.pack(side="left", fill="x", expand=True)
        # Navigation mode setting
        nav_card = self.create_elevation(general_frame, level=1)
        nav_card.pack(fill="x", pady=15, padx=10)
        nav_inner = tk.Frame(nav_card, bg=self.theme.surface_container, padx=24, pady=20)
        nav_inner.pack(fill="both", expand=True)
        font_size = self.theme.get_font_size("large")
        tk.Label(nav_inner, text="Navigation Mode",
                font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface_container, fg=self.theme.on_surface).pack(anchor="w", pady=(0, 10))
        nav_options = tk.Frame(nav_inner, bg=self.theme.surface_container)
        nav_options.pack(fill="x")
        nav_var = tk.StringVar(value=self.settings.get("navigation_mode", "buttons"))
        buttons_radio = tk.Radiobutton(nav_options, text="Next/Previous Buttons", variable=nav_var, value="buttons",
                                     bg=self.theme.surface_container, fg=self.theme.on_surface,
                                     selectcolor=self.theme.primary, activebackground=self.theme.surface_container,
                                     activeforeground=self.theme.on_surface,
                                     font=("Segoe UI", self.theme.get_font_size("medium")),
                                     command=lambda: self.update_setting("navigation_mode", "buttons"))
        buttons_radio.pack(side="left", padx=(0, 20))
        scroll_radio = tk.Radiobutton(nav_options, text="Scroll Through Questions", variable=nav_var, value="scroll",
                                    bg=self.theme.surface_container, fg=self.theme.on_surface,
                                    selectcolor=self.theme.primary, activebackground=self.theme.surface_container,
                                    activeforeground=self.theme.on_surface,
                                    font=("Segoe UI", self.theme.get_font_size("medium")),
                                    command=lambda: self.update_setting("navigation_mode", "scroll"))
        scroll_radio.pack(side="left")
        # Features tab
        features_frame = tk.Frame(notebook, bg=self.theme.surface)
        notebook.add(features_frame, text="Features")
        # Auto-save setting
        auto_save_card = self.create_elevation(features_frame, level=1)
        auto_save_card.pack(fill="x", pady=15, padx=10)
        auto_save_inner = tk.Frame(auto_save_card, bg=self.theme.surface_container, padx=24, pady=20)
        auto_save_inner.pack(fill="both", expand=True)
        font_size = self.theme.get_font_size("large")
        tk.Label(auto_save_inner, text="Auto Save",
                font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface_container, fg=self.theme.on_surface).pack(anchor="w", pady=(0, 10))
        auto_save_var = tk.BooleanVar(value=self.settings.get("auto_save", True))
        auto_save_check = tk.Checkbutton(auto_save_inner, text="Automatically save progress",
                                        variable=auto_save_var,
                                        bg=self.theme.surface_container, fg=self.theme.on_surface,
                                        selectcolor=self.theme.primary,
                                        activebackground=self.theme.surface_container,
                                        activeforeground=self.theme.on_surface,
                                        font=("Segoe UI", self.theme.get_font_size("medium")),
                                        command=lambda: self.update_setting("auto_save", auto_save_var.get()))
        auto_save_check.pack(anchor="w", pady=5)
        # Explanations setting
        explanations_card = self.create_elevation(features_frame, level=1)
        explanations_card.pack(fill="x", pady=15, padx=10)
        explanations_inner = tk.Frame(explanations_card, bg=self.theme.surface_container, padx=24, pady=20)
        explanations_inner.pack(fill="both", expand=True)
        font_size = self.theme.get_font_size("large")
        tk.Label(explanations_inner, text="Explanations",
                font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface_container, fg=self.theme.on_surface).pack(anchor="w", pady=(0, 10))
        explanations_var = tk.BooleanVar(value=self.settings.get("show_explanations", True))
        explanations_check = tk.Checkbutton(explanations_inner, text="Show explanations in results",
                                          variable=explanations_var,
                                          bg=self.theme.surface_container, fg=self.theme.on_surface,
                                          selectcolor=self.theme.primary,
                                          activebackground=self.theme.surface_container,
                                          activeforeground=self.theme.on_surface,
                                          font=("Segoe UI", self.theme.get_font_size("medium")),
                                          command=lambda: self.update_setting("show_explanations", explanations_var.get()))
        explanations_check.pack(anchor="w", pady=5)
        # Timer alerts setting
        timer_alerts_card = self.create_elevation(features_frame, level=1)
        timer_alerts_card.pack(fill="x", pady=15, padx=10)
        timer_alerts_inner = tk.Frame(timer_alerts_card, bg=self.theme.surface_container, padx=24, pady=20)
        timer_alerts_inner.pack(fill="both", expand=True)
        font_size = self.theme.get_font_size("large")
        tk.Label(timer_alerts_inner, text="Timer Alerts",
                font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface_container, fg=self.theme.on_surface).pack(anchor="w", pady=(0, 10))
        timer_alerts_var = tk.BooleanVar(value=self.settings.get("timer_alerts", True))
        timer_alerts_check = tk.Checkbutton(timer_alerts_inner, text="Show timer alerts",
                                          variable=timer_alerts_var,
                                          bg=self.theme.surface_container, fg=self.theme.on_surface,
                                          selectcolor=self.theme.primary,
                                          activebackground=self.theme.surface_container,
                                          activeforeground=self.theme.on_surface,
                                          font=("Segoe UI", self.theme.get_font_size("medium")),
                                          command=lambda: self.update_setting("timer_alerts", timer_alerts_var.get()))
        timer_alerts_check.pack(anchor="w", pady=5)
        # Animations setting
        animations_card = self.create_elevation(features_frame, level=1)
        animations_card.pack(fill="x", pady=15, padx=10)
        animations_inner = tk.Frame(animations_card, bg=self.theme.surface_container, padx=24, pady=20)
        animations_inner.pack(fill="both", expand=True)
        font_size = self.theme.get_font_size("large")
        tk.Label(animations_inner, text="Animations",
                font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface_container, fg=self.theme.on_surface).pack(anchor="w", pady=(0, 10))
        animations_var = tk.BooleanVar(value=self.settings.get("animations", True))
        animations_check = tk.Checkbutton(animations_inner, text="Enable UI animations",
                                        variable=animations_var,
                                        bg=self.theme.surface_container, fg=self.theme.on_surface,
                                        selectcolor=self.theme.primary,
                                        activebackground=self.theme.surface_container,
                                        activeforeground=self.theme.on_surface,
                                        font=("Segoe UI", self.theme.get_font_size("medium")),
                                        command=lambda: self.update_setting("animations", animations_var.get()))
        animations_check.pack(anchor="w", pady=5)
        # Keyboard shortcuts setting
        shortcuts_card = self.create_elevation(features_frame, level=1)
        shortcuts_card.pack(fill="x", pady=15, padx=10)
        shortcuts_inner = tk.Frame(shortcuts_card, bg=self.theme.surface_container, padx=24, pady=20)
        shortcuts_inner.pack(fill="both", expand=True)
        font_size = self.theme.get_font_size("large")
        tk.Label(shortcuts_inner, text="Keyboard Shortcuts",
                font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface_container, fg=self.theme.on_surface).pack(anchor="w", pady=(0, 10))
        shortcuts_var = tk.BooleanVar(value=self.settings.get("keyboard_shortcuts", True))
        shortcuts_check = tk.Checkbutton(shortcuts_inner, text="Enable keyboard shortcuts",
                                       variable=shortcuts_var,
                                       bg=self.theme.surface_container, fg=self.theme.on_surface,
                                       selectcolor=self.theme.primary,
                                       activebackground=self.theme.surface_container,
                                       activeforeground=self.theme.on_surface,
                                       font=("Segoe UI", self.theme.get_font_size("medium")),
                                       command=lambda: self.update_setting("keyboard_shortcuts", shortcuts_var.get()))
        shortcuts_check.pack(anchor="w", pady=5)
        # Show progress setting
        progress_card = self.create_elevation(features_frame, level=1)
        progress_card.pack(fill="x", pady=15, padx=10)
        progress_inner = tk.Frame(progress_card, bg=self.theme.surface_container, padx=24, pady=20)
        progress_inner.pack(fill="both", expand=True)
        font_size = self.theme.get_font_size("large")
        tk.Label(progress_inner, text="Progress Indicators",
                font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface_container, fg=self.theme.on_surface).pack(anchor="w", pady=(0, 10))
        progress_var = tk.BooleanVar(value=self.settings.get("show_progress", True))
        progress_check = tk.Checkbutton(progress_inner, text="Show progress indicators",
                                      variable=progress_var,
                                      bg=self.theme.surface_container, fg=self.theme.on_surface,
                                      selectcolor=self.theme.primary,
                                      activebackground=self.theme.surface_container,
                                      activeforeground=self.theme.on_surface,
                                      font=("Segoe UI", self.theme.get_font_size("medium")),
                                      command=lambda: self.update_setting("show_progress", progress_var.get()))
        progress_check.pack(anchor="w", pady=5)
        # Confirm on exit setting
        confirm_card = self.create_elevation(features_frame, level=1)
        confirm_card.pack(fill="x", pady=15, padx=10)
        confirm_inner = tk.Frame(confirm_card, bg=self.theme.surface_container, padx=24, pady=20)
        confirm_inner.pack(fill="both", expand=True)
        font_size = self.theme.get_font_size("large")
        tk.Label(confirm_inner, text="Exit Confirmation",
                font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface_container, fg=self.theme.on_surface).pack(anchor="w", pady=(0, 10))
        confirm_var = tk.BooleanVar(value=self.settings.get("confirm_on_exit", True))
        confirm_check = tk.Checkbutton(confirm_inner, text="Confirm before exiting",
                                      variable=confirm_var,
                                      bg=self.theme.surface_container, fg=self.theme.on_surface,
                                      selectcolor=self.theme.primary,
                                      activebackground=self.theme.surface_container,
                                      activeforeground=self.theme.on_surface,
                                      font=("Segoe UI", self.theme.get_font_size("medium")),
                                      command=lambda: self.update_setting("confirm_on_exit", confirm_var.get()))
        confirm_check.pack(anchor="w", pady=5)
        # Buttons
        btn_frame = tk.Frame(container, bg=self.theme.surface)
        btn_frame.pack(fill="x", pady=(20, 0))
        reset_btn = self.create_button(btn_frame, "Reset to Defaults", self.reset_settings, "error")
        reset_btn.pack(side="right", padx=5)

    def update_setting(self, key, value):
        self.settings.set(key, value)
        if key == "theme":
            self.theme.update_theme()
            self.apply_theme()
            self.show_settings() # Refresh to apply theme
        elif key == "font_size":
            self.show_settings() # Refresh to apply font size
        elif key == "screen_scaling":
            scaling = value / 100
            if platform.system() == "Windows":
                self.root.tk.call('tk', 'scaling', scaling)
        elif key == "keyboard_shortcuts":
            if value:
                self.setup_keyboard_shortcuts()
            else:
                # Remove all keyboard shortcuts
                self.root.unbind("<Control-n>")
                self.root.unbind("<Control-s>")
                self.root.unbind("<Control-r>")
                self.root.unbind("<Control-t>")
                self.root.unbind("<Control-b>")
                self.root.unbind("<Control-h>")
                self.root.unbind("<Escape>")
                self.root.unbind("<Left>")
                self.root.unbind("<Right>")
                self.root.unbind("<Up>")
                self.root.unbind("<Down>")

    def update_scale(self, label, value):
        label.config(text=f"{value}%")
        self.update_setting("screen_scaling", value)

    def reset_settings(self):
        if messagebox.askyesno("Reset Settings", "Reset all settings to default values?"):
            self.settings = Settings()
            self.theme = Material3Theme(self.settings)
            self.apply_theme()
            scaling = self.settings.get("screen_scaling", 100) / 100
            if platform.system() == "Windows":
                self.root.tk.call('tk', 'scaling', scaling)
            # Set up keyboard shortcuts if enabled
            if self.settings.get("keyboard_shortcuts", True):
                self.setup_keyboard_shortcuts()
            self.show_settings()

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
        font_size = self.theme.get_font_size("xxlarge")
        tk.Label(container, text=section_titles[section_name],
                font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface, fg=self.theme.primary).pack(anchor="w")
        font_size = self.theme.get_font_size("xlarge")
        tk.Label(container, text="Examination Instructions",
                font=("Segoe UI", font_size),
                bg=self.theme.surface, fg=self.theme.on_surface).pack(anchor="w", pady=(5, 20))
        # Mode indicator
        mode_text = "Study Mode" if self.settings.get("study_mode", False) else "Exam Mode"
        mode_color = self.theme.tertiary if self.settings.get("study_mode", False) else self.theme.primary
        mode_frame = tk.Frame(container, bg=self.theme.surface)
        mode_frame.pack(fill="x", pady=(0, 20))
        font_size = self.theme.get_font_size("large")
        tk.Label(mode_frame, text=mode_text,
                font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface, fg=mode_color).pack(anchor="w")
        # Navigation preference
        nav_frame = tk.Frame(container, bg=self.theme.surface)
        nav_frame.pack(fill="x", pady=(10, 20))
        font_size = self.theme.get_font_size("large")
        tk.Label(nav_frame, text="Navigation Preference:",
                font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface, fg=self.theme.on_surface).pack(side="left", padx=(0, 20))
        nav_var = tk.StringVar(value=self.settings.get("navigation_mode", "buttons"))
        buttons_radio = tk.Radiobutton(nav_frame, text="Buttons", variable=nav_var, value="buttons",
                                      bg=self.theme.surface, fg=self.theme.on_surface,
                                      selectcolor=self.theme.primary, activebackground=self.theme.surface,
                                      activeforeground=self.theme.on_surface,
                                      font=("Segoe UI", self.theme.get_font_size("medium")))
        buttons_radio.pack(side="left", padx=(0, 20))
        scroll_radio = tk.Radiobutton(nav_frame, text="Scroll Wheel", variable=nav_var, value="scroll",
                                     bg=self.theme.surface, fg=self.theme.on_surface,
                                     selectcolor=self.theme.primary, activebackground=self.theme.surface,
                                     activeforeground=self.theme.on_surface,
                                     font=("Segoe UI", self.theme.get_font_size("medium")))
        scroll_radio.pack(side="left")
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
        font_size = self.theme.get_font_size("large")
        tk.Label(inner1, text="💫 Motivation", font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface_container, fg=self.theme.primary).pack(anchor="w")
        quote = random.choice(MOTIVATIONAL_QUOTES)
        font_size = self.theme.get_font_size("medium")
        tk.Label(inner1, text=f'"{quote}"', font=("Segoe UI", font_size, "italic"),
                bg=self.theme.surface_container, fg=self.theme.on_surface,
                justify="left", wraplength=800).pack(anchor="w", pady=(10, 0))
        # Instructions
        card2 = self.create_elevation(scrollable, level=1)
        card2.pack(fill="x", pady=(0, 20))
        inner2 = tk.Frame(card2, bg=self.theme.surface_container, padx=30, pady=25)
        inner2.pack(fill="both", expand=True)
        font_size = self.theme.get_font_size("large")
        tk.Label(inner2, text="📋 Examination Guidelines", font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface_container, fg=self.theme.primary).pack(anchor="w", pady=(0, 15))
        font_size = self.theme.get_font_size("medium")
        for instruction in PRC_INSTRUCTIONS:
            tk.Label(inner2, text=f"• {instruction}", font=("Segoe UI", font_size),
                    bg=self.theme.surface_container, fg=self.theme.on_surface,
                    justify="left", anchor="w", wraplength=800).pack(anchor="w", pady=5)
        # Section info
        card3 = self.create_elevation(scrollable, level=1)
        card3.pack(fill="x", pady=(0, 20))
        inner3 = tk.Frame(card3, bg=self.theme.surface_container, padx=30, pady=25)
        inner3.pack(fill="both", expand=True)
        font_size = self.theme.get_font_size("large")
        tk.Label(inner3, text="📊 Section Details", font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface_container, fg=self.theme.primary).pack(anchor="w", pady=(0, 15))
        info_text = [
            f"Total Questions: {len(self.section_questions)}",
            f"Time Allotted: {SECTION_TIMES[section_name] // 3600} hours" if not self.settings.get("study_mode", False) else "No time limit in Study Mode",
            "Timer starts immediately when you begin" if not self.settings.get("study_mode", False) else "Take your time to understand each question",
            "Use the answer sheet on the right to mark your answers",
            "You can change answers anytime before submitting"
        ]
        font_size = self.theme.get_font_size("medium")
        for info in info_text:
            tk.Label(inner3, text=f"• {info}", font=("Segoe UI", font_size),
                    bg=self.theme.surface_container, fg=self.theme.on_surface,
                    justify="left", anchor="w").pack(anchor="w", pady=5)
        # Buttons
        btn_frame = tk.Frame(container, bg=self.theme.surface)
        btn_frame.pack(fill="x", pady=(20, 0))
        back_btn = self.create_button(btn_frame, "← Back", self.show_main_menu, "text")
        back_btn.pack(side="left", padx=5)
        start_btn = self.create_button(btn_frame, "Begin Exam →", lambda: self.start_section_exam(nav_var.get()), "filled", 150)
        start_btn.pack(side="left", padx=5)
        self.bind_mousewheel(canvas)

    # ==================== EXAM INTERFACE ====================
    def start_section_exam(self, nav_mode=None):
        if nav_mode is None:
            nav_mode = self.settings.get("navigation_mode", "buttons")
        self.nav_mode = nav_mode
        if self.settings.get("study_mode", False):
            self.time_left = float('inf') # No time limit in study mode
        else:
            self.time_left = self.section_times[self.current_section]
        self.current_question_index = 0
        self.show_preload_screen()
        threading.Thread(target=self.preload_images, daemon=True).start()

    def show_preload_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        container = tk.Frame(self.root, bg=self.theme.surface)
        container.pack(fill='both', expand=True)
        font_size = self.theme.get_font_size("xxlarge")
        tk.Label(container, text=f"Preparing {self.current_section} Exam",
                font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface, fg=self.theme.primary).pack(pady=(100, 20))
        font_size = self.theme.get_font_size("large")
        tk.Label(container, text="Loading questions and images...",
                font=("Segoe UI", font_size),
                bg=self.theme.surface, fg=self.theme.on_surface_variant).pack(pady=10)
        self.preload_progress = ttk.Progressbar(container, mode='determinate',
                                               length=400, style="Custom.Horizontal.TProgressbar")
        self.preload_progress.pack(pady=20)
        self.preload_status = tk.Label(container, text="Initializing...",
                                       font=("Segoe UI", self.theme.get_font_size("medium")),
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
                            font=("Segoe UI", self.theme.get_font_size("medium"), "bold"),
                            relief='flat', cursor="hand2",
                            padx=16, pady=8)
        menu_btn.pack(side="left", padx=16, pady=12)
        section_titles = {
            "AMSTHEC": "AMSTHEC",
            "HPGE": "HPGE",
            "PSAD": "PSAD"
        }
        font_size = self.theme.get_font_size("xlarge")
        tk.Label(topbar, text=section_titles[self.current_section],
                font=("Segoe UI", font_size, "bold"),
                bg=self.theme.primary, fg=self.theme.on_primary).pack(side="left", padx=20)
        # Timer (only in exam mode)
        if not self.settings.get("study_mode", False):
            self.timer_label = tk.Label(topbar, text=self.format_time(self.time_left),
                                        font=("Segoe UI", self.theme.get_font_size("xlarge"), "bold"),
                                        bg=self.theme.primary, fg=self.theme.on_primary)
            self.timer_label.pack(side="right", padx=30)
        # Progress
        answered = sum(1 for ans in self.all_answers[self.current_section] if ans is not None)
        self.progress_label = tk.Label(topbar, text=f"{answered}/{len(self.section_questions)}",
                                      font=("Segoe UI", self.theme.get_font_size("medium"), "bold"),
                                      bg=self.theme.primary, fg=self.theme.on_primary)
        self.progress_label.pack(side="right", padx=20)
        # Main container
        main = tk.Frame(self.root, bg=self.theme.surface)
        main.pack(fill="both", expand=True, padx=20, pady=20)
        # Left: Questions
        left = tk.Frame(main, bg=self.theme.surface)
        left.pack(side="left", fill="both", expand=True, padx=(0, 15))
        font_size = self.theme.get_font_size("xlarge")
        tk.Label(left, text="Questions", font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface, fg=self.theme.on_surface).pack(anchor="w", pady=(0, 15))
        # Question navigation based on mode
        nav_frame = tk.Frame(left, bg=self.theme.surface)
        nav_frame.pack(fill="x", pady=(0, 10))
        self.question_label = tk.Label(nav_frame, text=f"Question {self.current_question_index + 1} of {len(self.section_questions)}",
                                      font=("Segoe UI", self.theme.get_font_size("medium")),
                                      bg=self.theme.surface, fg=self.theme.on_surface)
        self.question_label.pack(side="left", expand=True)
        if self.nav_mode == "buttons":
            self.prev_btn = self.create_button(nav_frame, "← Previous", lambda: self.navigate_question(-1), "text")
            self.prev_btn.pack(side="left", padx=(0, 10))
            self.next_btn = self.create_button(nav_frame, "Next →", lambda: self.navigate_question(1), "text")
            self.next_btn.pack(side="right")
        else:
            # Scroll mode - bind mousewheel
            def on_mousewheel(event):
                if event.delta > 0:
                    self.navigate_question(-1)
                else:
                    self.navigate_question(1)
            self.root.bind("<MouseWheel>", on_mousewheel)
        # Progress bar
        if self.settings.get("show_progress", True):
            progress_bg = tk.Frame(left, bg=self.theme.surface_container, height=8)
            progress_bg.pack(fill="x", pady=(0, 15))
            self.progress_fill = tk.Frame(progress_bg, bg=self.theme.primary, height=8)
            progress_width = (self.current_question_index + 1) / len(self.section_questions)
            self.progress_fill.place(relx=0, rely=0, relwidth=progress_width, relheight=1)
        # Question canvas
        self.q_canvas = tk.Canvas(left, bg=self.theme.surface, highlightthickness=0)
        q_scroll = ttk.Scrollbar(left, orient="vertical", command=self.q_canvas.yview)
        self.q_frame = tk.Frame(self.q_canvas, bg=self.theme.surface)
        self.q_frame.bind("<Configure>", lambda e: self.q_canvas.configure(scrollregion=self.q_canvas.bbox("all")))
        self.q_canvas.create_window((0, 0), window=self.q_frame, anchor="nw")
        self.q_canvas.configure(yscrollcommand=q_scroll.set)
        self.q_canvas.pack(side="left", fill="both", expand=True)
        q_scroll.pack(side="right", fill="y")
        self.bind_mousewheel(self.q_canvas)
        # Right: Answer sheet
        right = tk.Frame(main, bg=self.theme.surface, width=280)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)
        font_size = self.theme.get_font_size("large")
        tk.Label(right, text="Answer Sheet", font=("Segoe UI", font_size, "bold"),
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
            # Question number
            font_size = self.theme.get_font_size("medium")
            tk.Label(row, text=str(i+1), font=("Segoe UI", font_size, "bold"),
                    bg=self.theme.surface, fg=self.theme.on_surface,
                    width=3).pack(side="left", padx=(0, 10))
            # Bookmark indicator
            bookmark_id = f"{self.current_section}_{i}"
            is_bookmarked = bookmark_id in [b["id"] for b in self.bookmarks.get_bookmarks()]
            if is_bookmarked:
                bookmark_indicator = tk.Label(row, text="🔖", font=("Segoe UI", self.theme.get_font_size("normal")),
                                            bg=self.theme.surface, fg=self.theme.bookmark)
                bookmark_indicator.pack(side="left", padx=(0, 5))
            # Answer options
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
                                 font=("Segoe UI", self.theme.get_font_size("normal"), "bold"),
                                 fill=self.theme.on_surface)
                btn_data = {'canvas': canvas, 'letter': letter, 'index': i}
                btn_group.append(btn_data)
                canvas.bind("<Button-1>", lambda e, d=btn_data: self.select_answer(d))
            self.answer_buttons.append(btn_group)
        # Floating action buttons
        fab_frame = tk.Frame(self.root, bg=self.theme.surface)
        fab_frame.place(relx=0.98, rely=0.85, anchor="se")
        # Bookmark button
        bookmark_id = f"{self.current_section}_{self.current_question_index}"
        is_bookmarked = bookmark_id in [b["id"] for b in self.bookmarks.get_bookmarks()]
        bookmark_color = self.theme.bookmark if is_bookmarked else self.theme.surface_container
        self.bookmark_btn = self.create_fab(fab_frame, "🔖", self.toggle_bookmark, "Bookmark Question")
        self.bookmark_btn.config(bg=bookmark_color)
        # Explanation button (only in study mode)
        if self.settings.get("study_mode", False):
            self.create_fab(fab_frame, "💡", self.show_explanation, "Show Explanation").pack(pady=5)
        # Submit button
        submit_btn = self.create_button(self.root, "Submit Section", self.confirm_submit, "filled", 180)
        submit_btn.pack(side="bottom", pady=20)
        # Update question display
        self.update_question_display()
        # Update answer sheet
        self.update_answer_sheet()
        # Start timer (only in exam mode)
        if not self.settings.get("study_mode", False):
            self.start_timer()

    def update_question_display(self):
        """Update the question display"""
        # Clear the question frame
        for widget in self.q_frame.winfo_children():
            widget.destroy()
        # Get current question
        if 0 <= self.current_question_index < len(self.section_questions):
            q = self.section_questions[self.current_question_index]
            # Create question card
            card = self.create_elevation(self.q_frame, level=1)
            card.pack(fill="x", pady=10)
            inner = tk.Frame(card, bg=self.theme.surface_container, padx=24, pady=24)
            inner.pack(fill="both", expand=True)
            # Header
            header = tk.Frame(inner, bg=self.theme.surface_container)
            header.pack(fill="x", pady=(0, 15))
            font_size = self.theme.get_font_size("large")
            tk.Label(header, text=f"Question {self.current_question_index + 1}",
                    font=("Segoe UI", font_size, "bold"),
                    bg=self.theme.surface_container, fg=self.theme.primary).pack(side="left")
            # Tags
            tags = tk.Frame(header, bg=self.theme.surface_container)
            tags.pack(side="left", padx=(15, 0))
            difficulty = q.get("difficulty")
            if difficulty:
                diff_text = {1: "Easy", 2: "Medium", 3: "Hard"}.get(difficulty, "")
                diff_color = {"Easy": "#4CAF50", "Medium": "#FF9800", "Hard": "#F44336"}.get(diff_text, "#999")
                if diff_text:
                    tk.Label(tags, text=diff_text, font=("Segoe UI", self.theme.get_font_size("normal"), "bold"),
                            bg=diff_color, fg="white", padx=8, pady=2).pack(side="left", padx=2)
            if q.get("term"):
                tk.Label(tags, text="TERM", font=("Segoe UI", self.theme.get_font_size("normal"), "bold"),
                        bg="#2196F3", fg="white", padx=8, pady=2).pack(side="left", padx=2)
            # Question text
            font_size = self.theme.get_font_size("medium")
            tk.Label(inner, text=q['stem'], font=("Segoe UI", font_size),
                    bg=self.theme.surface_container, fg=self.theme.on_surface,
                    justify="left", wraplength=650).pack(anchor="w", pady=(0, 15))
            # Image
            if q.get("figure"):
                self.display_image(inner, q["figure"])
            # Choices in two columns
            choices_frame = tk.Frame(inner, bg=self.theme.surface_container)
            choices_frame.pack(anchor="w", pady=(0, 15))
            left_frame = tk.Frame(choices_frame, bg=self.theme.surface_container)
            left_frame.pack(side="left", fill="x", expand=True, padx=(0, 20))
            right_frame = tk.Frame(choices_frame, bg=self.theme.surface_container)
            right_frame.pack(side="left", fill="x", expand=True)
            for j, choice in enumerate(q["choices"]):
                letter = chr(65 + j)
                c_frame = tk.Frame(left_frame if j % 2 == 0 else right_frame, bg=self.theme.surface_container)
                c_frame.pack(anchor="w", pady=5)
                indicator = tk.Canvas(c_frame, width=24, height=24,
                                     bg=self.theme.surface_container, highlightthickness=0)
                indicator.pack(side="left", padx=(0, 12))
                user_ans = self.all_answers[self.current_section][self.current_question_index]
                is_selected = letter == user_ans
                if is_selected:
                    indicator.create_oval(2, 2, 22, 22,
                                         outline=self.theme.primary,
                                         fill=self.theme.primary, width=3)
                    indicator.create_text(12, 12, text=letter,
                                         font=("Segoe UI", self.theme.get_font_size("normal"), "bold"),
                                         fill=self.theme.on_primary)
                    choice_color = self.theme.primary
                    choice_bg = self.adjust_color(self.theme.surface_container, -10 if self.theme.is_dark else 10)
                else:
                    indicator.create_oval(2, 2, 22, 22,
                                         outline=self.theme.outline,
                                         fill=self.theme.surface_container, width=2)
                    indicator.create_text(12, 12, text=letter,
                                         font=("Segoe UI", self.theme.get_font_size("normal")),
                                         fill=self.theme.on_surface)
                    choice_color = self.theme.on_surface
                    choice_bg = self.theme.surface_container
                font_size = self.theme.get_font_size("medium")
                choice_label = tk.Label(c_frame, text=choice, font=("Segoe UI", font_size),
                                       bg=choice_bg, fg=choice_color,
                                       justify="left", anchor="w", wraplength=300)
                choice_label.pack(side="left")
                # Make choice clickable
                c_frame.bind("<Button-1>", lambda e, l=letter: self.select_answer_direct(l))
                indicator.bind("<Button-1>", lambda e, l=letter: self.select_answer_direct(l))
                choice_label.bind("<Button-1>", lambda e, l=letter: self.select_answer_direct(l))
        # Update navigation buttons if in buttons mode
        if self.nav_mode == "buttons":
            self.prev_btn.config(state="normal" if self.current_question_index > 0 else "disabled")
            self.next_btn.config(state="normal" if self.current_question_index < len(self.section_questions) - 1 else "disabled")
        # Update question label
        self.question_label.config(text=f"Question {self.current_question_index + 1} of {len(self.section_questions)}")
        # Update progress bar
        if self.settings.get("show_progress", True) and hasattr(self, 'progress_fill'):
            progress_width = (self.current_question_index + 1) / len(self.section_questions)
            self.progress_fill.place(relx=0, rely=0, relwidth=progress_width, relheight=1)
        # Update bookmark button
        if hasattr(self, 'bookmark_btn'):
            bookmark_id = f"{self.current_section}_{self.current_question_index}"
            is_bookmarked = bookmark_id in [b["id"] for b in self.bookmarks.get_bookmarks()]
            bookmark_color = self.theme.bookmark if is_bookmarked else self.theme.surface_container
            self.bookmark_btn.config(bg=bookmark_color)

    def select_answer_direct(self, letter):
        """Select an answer directly from the question view"""
        self.all_answers[self.current_section][self.current_question_index] = letter
        self.update_answer_sheet()
        self.update_question_display() # Refresh to show selection
        self.save_backup()
        # Update progress
        answered = sum(1 for ans in self.all_answers[self.current_section] if ans is not None)
        if hasattr(self, 'progress_label') and self.progress_label.winfo_exists():
            self.progress_label.config(text=f"{answered}/{len(self.section_questions)}")

    def select_answer(self, btn_data):
        """Select an answer from the answer sheet"""
        i = btn_data['index']
        letter = btn_data['letter']
        # Update the answer
        self.all_answers[self.current_section][i] = letter
        # Update the answer sheet display
        self.update_answer_sheet()
        # Save progress
        self.save_backup()
        # Update progress
        answered = sum(1 for ans in self.all_answers[self.current_section] if ans is not None)
        if hasattr(self, 'progress_label') and self.progress_label.winfo_exists():
            self.progress_label.config(text=f"{answered}/{len(self.section_questions)}")
        # If this is the current question, update the display
        if i == self.current_question_index:
            self.update_question_display()

    def update_answer_sheet(self):
        """Update the answer sheet display"""
        for i, btn_group in enumerate(self.answer_buttons):
            user_ans = self.all_answers[self.current_section][i]
            for btn_data in btn_group:
                canvas = btn_data['canvas']
                letter = btn_data['letter']
                canvas.delete("all")
                if letter == user_ans:
                    # Make selected answer more visually distinct
                    canvas.create_oval(6, 6, 30, 30,
                                     outline=self.theme.primary,
                                     fill=self.theme.primary, width=3)
                    canvas.create_text(18, 18, text=letter,
                                     font=("Segoe UI", self.theme.get_font_size("normal"), "bold"),
                                     fill=self.theme.on_primary)
                else:
                    canvas.create_oval(6, 6, 30, 30,
                                     outline=self.theme.outline,
                                     fill=self.theme.surface, width=2)
                    canvas.create_text(18, 18, text=letter,
                                     font=("Segoe UI", self.theme.get_font_size("normal"), "bold"),
                                     fill=self.theme.on_surface)

    def display_image(self, parent, image_url):
        """Display an image in the question"""
        cache_key = f"{image_url}_normal"
        if cache_key in self.image_cache:
            photo = self.image_cache[cache_key]
            img_label = tk.Label(parent, image=photo, bg=parent.cget('bg'))
            img_label.image = photo
            img_label.pack(pady=15)
            return
        loading = tk.Label(parent, text="Loading image...",
                          font=("Segoe UI", self.theme.get_font_size("normal")),
                          bg=parent.cget('bg'), fg=self.theme.on_surface_variant)
        loading.pack(pady=10)

    def show_explanation(self):
        """Show explanation for the current question (study mode only)"""
        if 0 <= self.current_question_index < len(self.section_questions):
            q = self.section_questions[self.current_question_index]
            explanation = q.get("explanation", "No explanation available for this question.")
            messagebox.showinfo("Explanation", explanation)

    # ==================== QUESTION VIEWER ====================
    def show_question_viewer(self):
        """Show a single question viewer"""
        self.cancel_timer()
        for widget in self.root.winfo_children():
            widget.destroy()
        container = tk.Frame(self.root, bg=self.theme.surface)
        container.pack(fill='both', expand=True, padx=40, pady=30)
        # Header
        header = tk.Frame(container, bg=self.theme.surface)
        header.pack(fill="x", pady=(0, 20))
        font_size = self.theme.get_font_size("xxlarge")
        tk.Label(header, text="Question Viewer",
                font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface, fg=self.theme.primary).pack(anchor="w")
        # Back button
        back_btn = self.create_button(header, "← Back to Bookmarks", self.show_bookmarks, "text")
        back_btn.pack(side="right")
        # Question navigation
        nav_frame = tk.Frame(container, bg=self.theme.surface)
        nav_frame.pack(fill="x", pady=(0, 10))
        prev_btn = self.create_button(nav_frame, "← Previous", lambda: self.navigate_question(-1), "text")
        prev_btn.pack(side="left", padx=(0, 10))
        question_label = tk.Label(nav_frame, text=f"Question {self.current_question_index + 1} of {len(self.section_questions)}",
                                 font=("Segoe UI", self.theme.get_font_size("medium")),
                                 bg=self.theme.surface, fg=self.theme.on_surface)
        question_label.pack(side="left", expand=True)
        next_btn = self.create_button(nav_frame, "Next →", lambda: self.navigate_question(1), "text")
        next_btn.pack(side="right")
        # Progress bar
        if self.settings.get("show_progress", True):
            progress_bg = tk.Frame(container, bg=self.theme.surface_container, height=8)
            progress_bg.pack(fill="x", pady=(0, 15))
            progress_fill = tk.Frame(progress_bg, bg=self.theme.primary, height=8)
            progress_width = (self.current_question_index + 1) / len(self.section_questions)
            progress_fill.place(relx=0, rely=0, relwidth=progress_width, relheight=1)
        # Question canvas
        canvas = tk.Canvas(container, bg=self.theme.surface, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        q_frame = tk.Frame(canvas, bg=self.theme.surface)
        q_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=q_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.bind_mousewheel(canvas)
        # Get current question
        if 0 <= self.current_question_index < len(self.section_questions):
            q = self.section_questions[self.current_question_index]
            # Create question card
            card = self.create_elevation(q_frame, level=1)
            card.pack(fill="x", pady=10)
            inner = tk.Frame(card, bg=self.theme.surface_container, padx=24, pady=24)
            inner.pack(fill="both", expand=True)
            # Header
            header = tk.Frame(inner, bg=self.theme.surface_container)
            header.pack(fill="x", pady=(0, 15))
            font_size = self.theme.get_font_size("large")
            tk.Label(header, text=f"Question {self.current_question_index + 1}",
                    font=("Segoe UI", font_size, "bold"),
                    bg=self.theme.surface_container, fg=self.theme.primary).pack(side="left")
            # Tags
            tags = tk.Frame(header, bg=self.theme.surface_container)
            tags.pack(side="left", padx=(15, 0))
            difficulty = q.get("difficulty")
            if difficulty:
                diff_text = {1: "Easy", 2: "Medium", 3: "Hard"}.get(difficulty, "")
                diff_color = {"Easy": "#4CAF50", "Medium": "#FF9800", "Hard": "#F44336"}.get(diff_text, "#999")
                if diff_text:
                    tk.Label(tags, text=diff_text, font=("Segoe UI", self.theme.get_font_size("normal"), "bold"),
                            bg=diff_color, fg="white", padx=8, pady=2).pack(side="left", padx=2)
            if q.get("term"):
                tk.Label(tags, text="TERM", font=("Segoe UI", self.theme.get_font_size("normal"), "bold"),
                        bg="#2196F3", fg="white", padx=8, pady=2).pack(side="left", padx=2)
            # Question text
            font_size = self.theme.get_font_size("medium")
            tk.Label(inner, text=q['stem'], font=("Segoe UI", font_size),
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
                # Check if this is the correct answer
                is_correct = letter == q["correct_answer"]
                if is_correct:
                    indicator.create_oval(2, 2, 22, 22,
                                        outline=self.theme.success,
                                        fill=self.theme.success, width=2)
                    indicator.create_text(12, 12, text="✓",
                                      font=("Segoe UI", self.theme.get_font_size("normal"), "bold"),
                                      fill=self.theme.on_success)
                else:
                    indicator.create_oval(2, 2, 22, 22,
                                        outline=self.theme.outline,
                                        fill=self.theme.surface_container, width=1)
                    indicator.create_text(12, 12, text=letter,
                                      font=("Segoe UI", self.theme.get_font_size("normal")),
                                      fill=self.theme.on_surface)
                font_size = self.theme.get_font_size("medium")
                choice_color = self.theme.success if is_correct else self.theme.on_surface
                tk.Label(c_frame, text=f"{letter}. {choice}", font=("Segoe UI", font_size),
                        bg=self.theme.surface_container, fg=choice_color,
                        justify="left", wraplength=600).pack(side="left", fill="x", expand=True)
            # Explanation
            if q.get("explanation"):
                exp_frame = tk.Frame(inner, bg=self.theme.surface_container)
                exp_frame.pack(fill="x", pady=(15, 0))
                font_size = self.theme.get_font_size("medium")
                tk.Label(exp_frame, text="💡 Explanation:",
                        font=("Segoe UI", font_size, "bold"),
                        bg=self.theme.surface_container, fg=self.theme.primary).pack(anchor="w")
                font_size = self.theme.get_font_size("normal")
                tk.Label(exp_frame, text=q['explanation'], font=("Segoe UI", font_size),
                        bg=self.theme.surface_container, fg=self.theme.on_surface,
                        justify="left", wraplength=650).pack(anchor="w", pady=(5, 0))
            # User's answer (if available)
            if self.current_section in self.all_answers and self.current_question_index < len(self.all_answers[self.current_section]):
                user_answer = self.all_answers[self.current_section][self.current_question_index]
                if user_answer:
                    ans_frame = tk.Frame(inner, bg=self.theme.surface_container)
                    ans_frame.pack(fill="x", pady=(15, 0))
                    font_size = self.theme.get_font_size("medium")
                    tk.Label(ans_frame, text=f"Your answer: {user_answer}",
                            font=("Segoe UI", font_size, "bold"),
                            bg=self.theme.surface_container, fg=self.theme.on_surface).pack(anchor="w")
                    if user_answer != q["correct_answer"]:
                        tk.Label(ans_frame, text="This is incorrect",
                                font=("Segoe UI", self.theme.get_font_size("normal")),
                                bg=self.theme.surface_container, fg=self.theme.error).pack(anchor="w")

    # ==================== TIMER ====================
    def start_timer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        # Set up timer alerts if enabled
        if self.settings.get("timer_alerts", True):
            self.setup_timer_alerts()
        self.update_timer()

    def setup_timer_alerts(self):
        self.timer_alerts = []
        # Add alerts at specific time intervals
        alert_times = [
            self.time_left - 300, # 5 minutes
            self.time_left - 600, # 10 minutes
            self.time_left - 1800 # 30 minutes
        ]
        for alert_time in alert_times:
            if alert_time > 0:
                self.timer_alerts.append(alert_time)

    def update_timer(self):
        if self.time_left > 0 and self.time_left != float('inf'):
            self.time_left -= 1
            # Check for timer alerts
            if self.settings.get("timer_alerts", True) and self.time_left in self.timer_alerts:
                minutes = self.time_left // 60
                messagebox.showinfo("Time Alert", f"{minutes} minutes remaining!")
                self.timer_alerts.remove(self.time_left)
            if self.timer_label and self.timer_label.winfo_exists():
                self.timer_label.config(text=self.format_time(self.time_left))
            self.timer_id = self.root.after(1000, self.update_timer)
        elif self.time_left == float('inf'):
            # Study mode - no timer
            pass
        else:
            messagebox.showwarning("Time's Up!", f"Time expired for {self.current_section}")
            self.submit_section()

    def cancel_timer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        self.timer_alerts = []

    def format_time(self, seconds):
        hrs, rem = divmod(int(seconds), 3600)
        mins, secs = divmod(rem, 60)
        return f"{hrs:02d}:{mins:02d}:{secs:02d}"

    # ==================== SUBMISSION & RESULTS ====================
    def confirm_exit(self):
        if self.settings.get("confirm_on_exit", True):
            if messagebox.askyesno("Exit", "Save progress and return to menu?"):
                self.section_times[self.current_section] = self.time_left
                self.cancel_timer()
                self.save_backup()
                self.show_main_menu()
        else:
            self.section_times[self.current_section] = self.time_left
            self.cancel_timer()
            self.save_backup()
            self.show_main_menu()

    def confirm_submit(self):
        unanswered = sum(1 for ans in self.all_answers[self.current_section] if ans is not None)
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
                    "explanation": q.get("explanation", ""),
                    "term": q.get("term", False)
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
        font_size = self.theme.get_font_size("xlarge")
        tk.Label(topbar, text=f"{self.current_section} Results",
                font=("Segoe UI", font_size, "bold"),
                bg=self.theme.primary, fg=self.theme.on_primary).pack(side="left", padx=30, pady=15)
        container = tk.Frame(self.root, bg=self.theme.surface)
        container.pack(fill="both", expand=True, padx=40, pady=30)
        # Summary card
        summary = self.create_elevation(container, level=1)
        summary.pack(fill="x", pady=(0, 25))
        inner = tk.Frame(summary, bg=self.theme.surface_container, padx=40, pady=40)
        inner.pack(fill="both", expand=True)
        score_color = self.theme.success if pct >= 70 else self.theme.error
        font_size = self.theme.get_font_size("xxlarge")
        tk.Label(inner, text=f"{pct:.1f}%", font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface_container, fg=score_color).pack()
        font_size = self.theme.get_font_size("xlarge")
        tk.Label(inner, text=f"{correct} / {total} Correct",
                font=("Segoe UI", font_size),
                bg=self.theme.surface_container, fg=self.theme.on_surface).pack(pady=(10, 5))
        status = "PASSED" if pct >= 70 else "FAILED"
        font_size = self.theme.get_font_size("large")
        tk.Label(inner, text=status, font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface_container, fg=score_color).pack(pady=(10, 0))
        # Performance breakdown
        breakdown_frame = tk.Frame(inner, bg=self.theme.surface_container)
        breakdown_frame.pack(fill="x", pady=(20, 0))
        # Correct answers
        correct_frame = tk.Frame(breakdown_frame, bg=self.theme.surface_container)
        correct_frame.pack(side="left", fill="both", expand=True, padx=10)
        font_size = self.theme.get_font_size("medium")
        tk.Label(correct_frame, text="Correct",
                font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface_container, fg=self.theme.success).pack()
        font_size = self.theme.get_font_size("xlarge")
        tk.Label(correct_frame, text=f"{correct}",
                font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface_container, fg=self.theme.success).pack()
        # Incorrect answers
        incorrect_frame = tk.Frame(breakdown_frame, bg=self.theme.surface_container)
        incorrect_frame.pack(side="left", fill="both", expand=True, padx=10)
        font_size = self.theme.get_font_size("medium")
        tk.Label(incorrect_frame, text="Incorrect",
                font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface_container, fg=self.theme.error).pack()
        font_size = self.theme.get_font_size("xlarge")
        tk.Label(incorrect_frame, text=f"{total - correct}",
                font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface_container, fg=self.theme.error).pack()
        # Unanswered
        unanswered = total - correct - len(wrong_list)
        if unanswered > 0:
            unanswered_frame = tk.Frame(breakdown_frame, bg=self.theme.surface_container)
            unanswered_frame.pack(side="left", fill="both", expand=True, padx=10)
            font_size = self.theme.get_font_size("medium")
            tk.Label(unanswered_frame, text="Unanswered",
                    font=("Segoe UI", font_size, "bold"),
                    bg=self.theme.surface_container, fg=self.theme.on_surface_variant).pack()
            font_size = self.theme.get_font_size("xlarge")
            tk.Label(unanswered_frame, text=f"{unanswered}",
                    font=("Segoe UI", font_size, "bold"),
                    bg=self.theme.surface_container, fg=self.theme.on_surface_variant).pack()
        # Navigation buttons
        nav_frame = tk.Frame(inner, bg=self.theme.surface_container)
        nav_frame.pack(fill="x", pady=(20, 0))
        review_btn = self.create_button(nav_frame, "Review Wrong Answers",
                                      lambda: self.show_review(wrong_list), "text")
        review_btn.pack(side="left", padx=(0, 10))
        all_btn = self.create_button(nav_frame, "Review All Questions",
                                    self.show_all_questions, "text")
        all_btn.pack(side="left")
        # Wrong answers
        if wrong_list:
            font_size = self.theme.get_font_size("xlarge")
            tk.Label(container, text="Review Wrong Answers",
                    font=("Segoe UI", font_size, "bold"),
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
                # Header with question number and term indicator
                header = tk.Frame(inner_card, bg=self.theme.surface_container)
                header.pack(fill="x", pady=(0, 10))
                font_size = self.theme.get_font_size("large")
                tk.Label(header, text=f"Question {wrong['number']}",
                        font=("Segoe UI", font_size, "bold"),
                        bg=self.theme.surface_container, fg=self.theme.primary).pack(side="left")
                if wrong.get("term"):
                    tk.Label(header, text="TERM", font=("Segoe UI", self.theme.get_font_size("normal"), "bold"),
                            bg="#2196F3", fg="white", padx=8, pady=2).pack(side="left", padx=(10, 0))
                font_size = self.theme.get_font_size("medium")
                tk.Label(inner_card, text=wrong['stem'], font=("Segoe UI", font_size),
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
                                            font=("Segoe UI", self.theme.get_font_size("normal"), "bold"),
                                            fill=self.theme.on_error)
                        choice_color = self.theme.error
                    elif letter == wrong['correct_answer']:
                        indicator.create_oval(2, 2, 22, 22,
                                            outline=self.theme.success,
                                            fill=self.theme.success, width=2)
                        indicator.create_text(12, 12, text="✓",
                                            font=("Segoe UI", self.theme.get_font_size("normal"), "bold"),
                                            fill=self.theme.on_success)
                        choice_color = self.theme.success
                    else:
                        indicator.create_oval(2, 2, 22, 22,
                                            outline=self.theme.outline_variant,
                                            fill=self.theme.surface_container, width=1)
                        indicator.create_text(12, 12, text=letter,
                                            font=("Segoe UI", self.theme.get_font_size("normal")),
                                            fill=self.theme.on_surface_variant)
                        choice_color = self.theme.on_surface
                    font_size = self.theme.get_font_size("medium")
                    tk.Label(c_frame, text=f"{letter}. {choice}", font=("Segoe UI", font_size),
                            bg=self.theme.surface_container, fg=choice_color,
                            justify="left", wraplength=850).pack(side="left")
                ans_frame = tk.Frame(inner_card, bg=self.theme.surface_container)
                ans_frame.pack(fill="x", pady=(15, 10))
                font_size = self.theme.get_font_size("medium")
                tk.Label(ans_frame, text=f"Your answer: {wrong['user_answer']}",
                        font=("Segoe UI", font_size, "bold"),
                        bg=self.theme.surface_container, fg=self.theme.error).pack(side="left", padx=(0, 20))
                tk.Label(ans_frame, text=f"Correct: {wrong['correct_answer']}",
                        font=("Segoe UI", font_size, "bold"),
                        bg=self.theme.surface_container, fg=self.theme.success).pack(side="left")
                if wrong['explanation'] and self.settings.get("show_explanations", True):
                    exp_frame = tk.Frame(inner_card, bg=self.theme.surface_container)
                    exp_frame.pack(fill="x", pady=(10, 0))
                    font_size = self.theme.get_font_size("medium")
                    tk.Label(exp_frame, text="💡 Explanation:",
                            font=("Segoe UI", font_size, "bold"),
                            bg=self.theme.surface_container, fg=self.theme.primary).pack(anchor="w")
                    font_size = self.theme.get_font_size("normal")
                    tk.Label(exp_frame, text=wrong['explanation'], font=("Segoe UI", font_size),
                            bg=self.theme.surface_container, fg=self.theme.on_surface,
                            justify="left", wraplength=900).pack(anchor="w", pady=(5, 0))
        # Navigation buttons
        nav = tk.Frame(container, bg=self.theme.surface)
        nav.pack(fill="x", pady=20)
        back_btn = self.create_button(nav, "← Back to Menu", self.show_main_menu, "text")
        back_btn.pack(side="left", padx=5)
        if len(self.section_results) < 3:
            next_btn = self.create_button(nav, "Next Section →", self.show_main_menu, "filled")
            next_btn.pack(side="left", padx=5)

    def show_review(self, wrong_list):
        """Show detailed review of wrong answers"""
        for widget in self.root.winfo_children():
            widget.destroy()
        container = tk.Frame(self.root, bg=self.theme.surface)
        container.pack(fill='both', expand=True, padx=40, pady=30)
        # Header
        header = tk.Frame(container, bg=self.theme.surface)
        header.pack(fill="x", pady=(0, 20))
        font_size = self.theme.get_font_size("xxlarge")
        tk.Label(header, text="Review Wrong Answers",
                font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface, fg=self.theme.primary).pack(anchor="w")
        # Back button
        back_btn = self.create_button(header, "← Back", lambda: self.show_section_result(
            self.section_results[self.current_section]["score_pct"],
            self.section_results[self.current_section]["correct"],
            self.section_results[self.current_section]["total"],
            self.section_results[self.current_section]["wrong"]
        ), "text")
        back_btn.pack(side="right")
        # Scrollable content
        canvas = tk.Canvas(container, bg=self.theme.surface, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
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
            # Header with question number and term indicator
            header = tk.Frame(inner_card, bg=self.theme.surface_container)
            header.pack(fill="x", pady=(0, 10))
            font_size = self.theme.get_font_size("large")
            tk.Label(header, text=f"Question {wrong['number']}",
                    font=("Segoe UI", font_size, "bold"),
                    bg=self.theme.surface_container, fg=self.theme.primary).pack(side="left")
            if wrong.get("term"):
                tk.Label(header, text="TERM", font=("Segoe UI", self.theme.get_font_size("normal"), "bold"),
                        bg="#2196F3", fg="white", padx=8, pady=2).pack(side="left", padx=(10, 0))
            font_size = self.theme.get_font_size("medium")
            tk.Label(inner_card, text=wrong['stem'], font=("Segoe UI", font_size),
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
                                        font=("Segoe UI", self.theme.get_font_size("normal"), "bold"),
                                        fill=self.theme.on_error)
                    choice_color = self.theme.error
                elif letter == wrong['correct_answer']:
                    indicator.create_oval(2, 2, 22, 22,
                                        outline=self.theme.success,
                                        fill=self.theme.success, width=2)
                    indicator.create_text(12, 12, text="✓",
                                        font=("Segoe UI", self.theme.get_font_size("normal"), "bold"),
                                        fill=self.theme.on_success)
                    choice_color = self.theme.success
                else:
                    indicator.create_oval(2, 2, 22, 22,
                                        outline=self.theme.outline_variant,
                                        fill=self.theme.surface_container, width=1)
                    indicator.create_text(12, 12, text=letter,
                                        font=("Segoe UI", self.theme.get_font_size("normal")),
                                        fill=self.theme.on_surface_variant)
                    choice_color = self.theme.on_surface
                font_size = self.theme.get_font_size("medium")
                tk.Label(c_frame, text=f"{letter}. {choice}", font=("Segoe UI", font_size),
                        bg=self.theme.surface_container, fg=choice_color,
                        justify="left", wraplength=850).pack(side="left")
            ans_frame = tk.Frame(inner_card, bg=self.theme.surface_container)
            ans_frame.pack(fill="x", pady=(15, 10))
            font_size = self.theme.get_font_size("medium")
            tk.Label(ans_frame, text=f"Your answer: {wrong['user_answer']}",
                    font=("Segoe UI", font_size, "bold"),
                    bg=self.theme.surface_container, fg=self.theme.error).pack(side="left", padx=(0, 20))
            tk.Label(ans_frame, text=f"Correct: {wrong['correct_answer']}",
                    font=("Segoe UI", font_size, "bold"),
                    bg=self.theme.surface_container, fg=self.theme.success).pack(side="left")
            if wrong['explanation'] and self.settings.get("show_explanations", True):
                exp_frame = tk.Frame(inner_card, bg=self.theme.surface_container)
                exp_frame.pack(fill="x", pady=(10, 0))
                font_size = self.theme.get_font_size("medium")
                tk.Label(exp_frame, text="💡 Explanation:",
                        font=("Segoe UI", font_size, "bold"),
                        bg=self.theme.surface_container, fg=self.theme.primary).pack(anchor="w")
                font_size = self.theme.get_font_size("normal")
                tk.Label(exp_frame, text=wrong['explanation'], font=("Segoe UI", font_size),
                        bg=self.theme.surface_container, fg=self.theme.on_surface,
                        justify="left", wraplength=900).pack(anchor="w", pady=(5, 0))

    def show_all_questions(self):
        """Show all questions in the section for review"""
        for widget in self.root.winfo_children():
            widget.destroy()
        container = tk.Frame(self.root, bg=self.theme.surface)
        container.pack(fill='both', expand=True, padx=40, pady=30)
        # Header
        header = tk.Frame(container, bg=self.theme.surface)
        header.pack(fill="x", pady=(0, 20))
        font_size = self.theme.get_font_size("xxlarge")
        tk.Label(header, text="All Questions Review",
                font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface, fg=self.theme.primary).pack(anchor="w")
        # Back button
        back_btn = self.create_button(header, "← Back", lambda: self.show_section_result(
            self.section_results[self.current_section]["score_pct"],
            self.section_results[self.current_section]["correct"],
            self.section_results[self.current_section]["total"],
            self.section_results[self.current_section]["wrong"]
        ), "text")
        back_btn.pack(side="right")
        # Scrollable content
        canvas = tk.Canvas(container, bg=self.theme.surface, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg=self.theme.surface)
        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.bind_mousewheel(canvas)
        # Show all questions
        for i, q in enumerate(self.section_questions):
            user_ans = self.all_answers[self.current_section][i]
            correct_ans = q["correct_answer"]
            is_correct = user_ans == correct_ans
            card = self.create_elevation(scrollable, level=1)
            card.pack(fill="x", pady=10)
            inner_card = tk.Frame(card, bg=self.theme.surface_container, padx=25, pady=25)
            inner_card.pack(fill="both", expand=True)
            # Header with question number and status
            header = tk.Frame(inner_card, bg=self.theme.surface_container)
            header.pack(fill="x", pady=(0, 10))
            font_size = self.theme.get_font_size("large")
            status_text = "✓" if is_correct else "✗"
            status_color = self.theme.success if is_correct else self.theme.error
            tk.Label(header, text=f"Question {i+1} {status_text}",
                    font=("Segoe UI", font_size, "bold"),
                    bg=self.theme.surface_container, fg=status_color).pack(side="left")
            # Tags
            tags = tk.Frame(header, bg=self.theme.surface_container)
            tags.pack(side="left", padx=(15, 0))
            difficulty = q.get("difficulty")
            if difficulty:
                diff_text = {1: "Easy", 2: "Medium", 3: "Hard"}.get(difficulty, "")
                diff_color = {"Easy": "#4CAF50", "Medium": "#FF9800", "Hard": "#F44336"}.get(diff_text, "#999")
                if diff_text:
                    tk.Label(tags, text=diff_text, font=("Segoe UI", self.theme.get_font_size("normal"), "bold"),
                            bg=diff_color, fg="white", padx=8, pady=2).pack(side="left", padx=2)
            if q.get("term"):
                tk.Label(tags, text="TERM", font=("Segoe UI", self.theme.get_font_size("normal"), "bold"),
                        bg="#2196F3", fg="white", padx=8, pady=2).pack(side="left", padx=2)
            # Question text
            font_size = self.theme.get_font_size("medium")
            tk.Label(inner_card, text=q['stem'], font=("Segoe UI", font_size),
                    bg=self.theme.surface_container, fg=self.theme.on_surface,
                    justify="left", wraplength=900).pack(anchor="w", pady=(0, 15))
            # Choices
            for j, choice in enumerate(q["choices"]):
                letter = chr(65 + j)
                c_frame = tk.Frame(inner_card, bg=self.theme.surface_container)
                c_frame.pack(fill="x", pady=4)
                indicator = tk.Canvas(c_frame, width=24, height=24,
                                     bg=self.theme.surface_container, highlightthickness=0)
                indicator.pack(side="left", padx=(0, 10))
                if letter == user_ans and letter != correct_ans:
                    # User's wrong answer
                    indicator.create_oval(2, 2, 22, 22,
                                        outline=self.theme.error,
                                        fill=self.theme.error, width=2)
                    indicator.create_text(12, 12, text="✗",
                                        font=("Segoe UI", self.theme.get_font_size("normal"), "bold"),
                                        fill=self.theme.on_error)
                    choice_color = self.theme.error
                elif letter == correct_ans:
                    # Correct answer
                    indicator.create_oval(2, 2, 22, 22,
                                        outline=self.theme.success,
                                        fill=self.theme.success, width=2)
                    indicator.create_text(12, 12, text="✓",
                                        font=("Segoe UI", self.theme.get_font_size("normal"), "bold"),
                                        fill=self.theme.on_success)
                    choice_color = self.theme.success
                elif letter == user_ans:
                    # User's correct answer
                    indicator.create_oval(2, 2, 22, 22,
                                        outline=self.theme.primary,
                                        fill=self.theme.primary, width=2)
                    indicator.create_text(12, 12, text=letter,
                                        font=("Segoe UI", self.theme.get_font_size("normal"), "bold"),
                                        fill=self.theme.on_primary)
                    choice_color = self.theme.primary
                else:
                    # Unselected option
                    indicator.create_oval(2, 2, 22, 22,
                                        outline=self.theme.outline_variant,
                                        fill=self.theme.surface_container, width=1)
                    indicator.create_text(12, 12, text=letter,
                                        font=("Segoe UI", self.theme.get_font_size("normal")),
                                        fill=self.theme.on_surface_variant)
                    choice_color = self.theme.on_surface
                font_size = self.theme.get_font_size("medium")
                tk.Label(c_frame, text=f"{letter}. {choice}", font=("Segoe UI", font_size),
                        bg=self.theme.surface_container, fg=choice_color,
                        justify="left", wraplength=850).pack(side="left")
            # Answer summary
            ans_frame = tk.Frame(inner_card, bg=self.theme.surface_container)
            ans_frame.pack(fill="x", pady=(15, 10))
            font_size = self.theme.get_font_size("medium")
            if user_ans:
                ans_color = self.theme.success if is_correct else self.theme.error
                tk.Label(ans_frame, text=f"Your answer: {user_ans}",
                        font=("Segoe UI", font_size, "bold"),
                        bg=self.theme.surface_container, fg=ans_color).pack(side="left", padx=(0, 20))
            else:
                tk.Label(ans_frame, text="Your answer: Not answered",
                        font=("Segoe UI", font_size, "bold"),
                        bg=self.theme.surface_container, fg=self.theme.on_surface_variant).pack(side="left", padx=(0, 20))
            tk.Label(ans_frame, text=f"Correct: {correct_ans}",
                    font=("Segoe UI", font_size, "bold"),
                    bg=self.theme.surface_container, fg=self.theme.success).pack(side="left")
            # Explanation
            if q.get("explanation") and self.settings.get("show_explanations", True):
                exp_frame = tk.Frame(inner_card, bg=self.theme.surface_container)
                exp_frame.pack(fill="x", pady=(10, 0))
                font_size = self.theme.get_font_size("medium")
                tk.Label(exp_frame, text="💡 Explanation:",
                        font=("Segoe UI", font_size, "bold"),
                        bg=self.theme.surface_container, fg=self.theme.primary).pack(anchor="w")
                font_size = self.theme.get_font_size("normal")
                tk.Label(exp_frame, text=q['explanation'], font=("Segoe UI", font_size),
                        bg=self.theme.surface_container, fg=self.theme.on_surface,
                        justify="left", wraplength=900).pack(anchor="w", pady=(5, 0))

    def show_final_results(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        # Top bar
        topbar = tk.Frame(self.root, bg=self.theme.primary, height=64)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)
        font_size = self.theme.get_font_size("xlarge")
        tk.Label(topbar, text="Final Examination Results",
                font=("Segoe UI", font_size, "bold"),
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
        font_size = self.theme.get_font_size("xxlarge")
        tk.Label(inner, text=status_text, font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface_container, fg=status_color).pack()
        font_size = self.theme.get_font_size("xlarge")
        tk.Label(inner, text=f"Weighted Average: {wa:.2f}%",
                font=("Segoe UI", font_size),
                bg=self.theme.surface_container, fg=self.theme.on_surface).pack(pady=(15, 0))
        # Performance breakdown
        breakdown_frame = tk.Frame(inner, bg=self.theme.surface_container)
        breakdown_frame.pack(fill="x", pady=(20, 0))
        # Total correct
        total_correct = sum(self.section_results[s]["correct"] for s in self.section_results)
        total_questions = sum(self.section_results[s]["total"] for s in self.section_results)
        correct_frame = tk.Frame(breakdown_frame, bg=self.theme.surface_container)
        correct_frame.pack(side="left", fill="both", expand=True, padx=10)
        font_size = self.theme.get_font_size("medium")
        tk.Label(correct_frame, text="Total Correct",
                font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface_container, fg=self.theme.success).pack()
        font_size = self.theme.get_font_size("xlarge")
        tk.Label(correct_frame, text=f"{total_correct}/{total_questions}",
                font=("Segoe UI", font_size, "bold"),
                bg=self.theme.surface_container, fg=self.theme.success).pack()
        # Section breakdown
        font_size = self.theme.get_font_size("xlarge")
        tk.Label(container, text="Section Breakdown",
                font=("Segoe UI", font_size, "bold"),
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
                font_size = self.theme.get_font_size("large")
                tk.Label(inner_card, text=section, font=("Segoe UI", font_size, "bold"),
                        bg=self.theme.surface_container, fg=self.theme.on_surface).pack()
                font_size = self.theme.get_font_size("xlarge")
                tk.Label(inner_card, text=f"{score:.1f}%", font=("Segoe UI", font_size, "bold"),
                        bg=self.theme.surface_container, fg=color).pack(pady=(10, 5))
                font_size = self.theme.get_font_size("medium")
                tk.Label(inner_card, text=f"{icon} {self.section_results[section]['correct']}/{self.section_results[section]['total']}",
                        font=("Segoe UI", font_size),
                        bg=self.theme.surface_container, fg=self.theme.on_surface_variant).pack()
                # Progress bar
                progress_bg = tk.Frame(inner_card, bg=self.theme.outline_variant, height=6)
                progress_bg.pack(fill="x", pady=(10, 0))
                progress_fill = tk.Frame(progress_bg, bg=color, height=6)
                progress_fill.place(relx=0, rely=0, relwidth=score/100, relheight=1)
        # Navigation
        nav = tk.Frame(container, bg=self.theme.surface)
        nav.pack(fill="x", pady=20)
        menu_btn = self.create_button(nav, "← Back to Menu", self.show_main_menu, "text")
        menu_btn.pack(side="left", padx=5)
        restart_btn = self.create_button(nav, "🔄 Start New Exam", self.confirm_reset, "filled")
        restart_btn.pack(side="left", padx=5)
        export_btn = self.create_button(nav, "📄 Export Results", self.export_results, "text")
        export_btn.pack(side="left", padx=5)

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