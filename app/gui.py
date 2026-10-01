import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import hashlib

from database import create_connection


# ============================================================
# SMART SERVICE
# Modern Professional Tkinter GUI
# Python + MySQL + Tkinter
# ============================================================

# ----------------------------- COLORS ------------------------

BG = "#F5F7FB"
WHITE = "#FFFFFF"
NAVY = "#102A43"
DARK = "#172B4D"
BLUE = "#2563EB"
BLUE_HOVER = "#1D4ED8"
LIGHT_BLUE = "#E8F0FE"
TEXT = "#172B4D"
MUTED = "#6B7C93"
BORDER = "#D9E2EC"
GREEN = "#16A34A"
LIGHT_GREEN = "#DCFCE7"
ORANGE = "#D97706"
LIGHT_ORANGE = "#FEF3C7"
RED = "#DC2626"
LIGHT_RED = "#FEE2E2"
PURPLE = "#7C3AED"
LIGHT_PURPLE = "#EDE9FE"


class SmartServiceApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Smart Service")
        self.root.geometry("1200x760")
        self.root.minsize(1050, 680)
        self.root.configure(bg=BG)

        self.connection = create_connection()

        if self.connection is None:
            messagebox.showerror(
                "Database Error",
                "Could not connect to MySQL database."
            )
            self.root.destroy()
            return

        self.user = None
        self.provider_id = None

        self.setup_style()
        self.show_login()

    # ========================================================
    # STYLE
    # ========================================================

    def setup_style(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "TFrame",
            background=BG
        )

        style.configure(
            "White.TFrame",
            background=WHITE
        )

        style.configure(
            "Title.TLabel",
            background=BG,
            foreground=NAVY,
            font=("Segoe UI", 28, "bold")
        )

        style.configure(
            "PageTitle.TLabel",
            background=BG,
            foreground=NAVY,
            font=("Segoe UI", 22, "bold")
        )

        style.configure(
            "Heading.TLabel",
            background=BG,
            foreground=NAVY,
            font=("Segoe UI", 16, "bold")
        )

        style.configure(
            "Normal.TLabel",
            background=BG,
            foreground=TEXT,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Muted.TLabel",
            background=BG,
            foreground=MUTED,
            font=("Segoe UI", 9)
        )

        style.configure(
            "CardTitle.TLabel",
            background=WHITE,
            foreground=NAVY,
            font=("Segoe UI", 12, "bold")
        )

        style.configure(
            "CardNumber.TLabel",
            background=WHITE,
            foreground=NAVY,
            font=("Segoe UI", 21, "bold")
        )

        style.configure(
            "Sidebar.TFrame",
            background=NAVY
        )

        style.configure(
            "SidebarTitle.TLabel",
            background=NAVY,
            foreground=WHITE,
            font=("Segoe UI", 17, "bold")
        )

        style.configure(
            "SidebarSub.TLabel",
            background=NAVY,
            foreground="#AFC4DE",
            font=("Segoe UI", 8)
        )

        style.configure(
            "Sidebar.TButton",
            background=NAVY,
            foreground="#DCE7F5",
            borderwidth=0,
            relief="flat",
            font=("Segoe UI", 10),
            padding=(15, 11)
        )

        style.map(
            "Sidebar.TButton",
            background=[
                ("active", "#1D426B"),
                ("pressed", "#2563EB")
            ],
            foreground=[
                ("active", WHITE),
                ("pressed", WHITE)
            ]
        )

        style.configure(
            "Primary.TButton",
            background=BLUE,
            foreground=WHITE,
            borderwidth=0,
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padding=(16, 10)
        )

        style.map(
            "Primary.TButton",
            background=[
                ("active", BLUE_HOVER),
                ("pressed", BLUE_HOVER)
            ]
        )

        style.configure(
            "Secondary.TButton",
            background=WHITE,
            foreground=TEXT,
            bordercolor=BORDER,
            borderwidth=1,
            relief="solid",
            font=("Segoe UI", 10),
            padding=(13, 9)
        )

        style.map(
            "Secondary.TButton",
            background=[
                ("active", LIGHT_BLUE)
            ]
        )

        style.configure(
            "Danger.TButton",
            background=RED,
            foreground=WHITE,
            borderwidth=0,
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padding=(14, 9)
        )

        style.configure(
            "TEntry",
            fieldbackground=WHITE,
            foreground=TEXT,
            bordercolor=BORDER,
            lightcolor=BORDER,
            darkcolor=BORDER,
            padding=8
        )

        style.configure(
            "TCombobox",
            fieldbackground=WHITE,
            background=WHITE,
            foreground=TEXT,
            bordercolor=BORDER,
            padding=7
        )

        style.configure(
            "Treeview",
            background=WHITE,
            fieldbackground=WHITE,
            foreground=TEXT,
            rowheight=38,
            bordercolor=BORDER,
            font=("Segoe UI", 9)
        )

        style.configure(
            "Treeview.Heading",
            background="#EEF3F8",
            foreground=NAVY,
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            padding=9
        )

        style.map(
            "Treeview",
            background=[
                ("selected", "#DCE9FF")
            ],
            foreground=[
                ("selected", NAVY)
            ]
        )

    # ========================================================
    # GENERAL HELPERS
    # ========================================================

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_card(self, parent, padx=20, pady=20):
        card = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        card.pack_propagate(False)
        return card

    def make_icon(self, parent, text, bg=LIGHT_BLUE, fg=BLUE, size=28):
        label = tk.Label(
            parent,
            text=text,
            bg=bg,
            fg=fg,
            font=("Segoe UI Symbol", 14, "bold"),
            width=2,
            height=1
        )
        return label

    def create_page_header(self, title, subtitle="", back_command=None):
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=30, pady=(24, 15))

        if back_command:
            ttk.Button(
                header,
                text="← Back",
                style="Secondary.TButton",
                command=back_command
            ).pack(side="left", padx=(0, 18))

        text_frame = tk.Frame(header, bg=BG)
        text_frame.pack(side="left")

        tk.Label(
            text_frame,
            text=title,
            bg=BG,
            fg=NAVY,
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w")

        if subtitle:
            tk.Label(
                text_frame,
                text=subtitle,
                bg=BG,
                fg=MUTED,
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(3, 0))

    def create_tree(self, columns, parent=None):
        if parent is None:
            parent = self.root

        frame = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        frame.pack(
            expand=True,
            fill="both",
            padx=30,
            pady=(5, 25)
        )

        column_names = [column[0] for column in columns]

        tree = ttk.Treeview(
            frame,
            columns=column_names,
            show="headings",
            selectmode="browse"
        )

        for name, width in columns:
            tree.heading(name, text=name)
            tree.column(
                name,
                width=width,
                minwidth=60,
                anchor="center"
            )

        y_scroll = ttk.Scrollbar(
            frame,
            orient="vertical",
            command=tree.yview
        )
        x_scroll = ttk.Scrollbar(
            frame,
            orient="horizontal",
            command=tree.xview
        )

        tree.configure(
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set
        )

        tree.pack(
            side="left",
            expand=True,
            fill="both",
            padx=(8, 0),
            pady=(8, 0)
        )

        y_scroll.pack(
            side="right",
            fill="y",
            pady=8
        )

        x_scroll.pack(
            side="bottom",
            fill="x",
            padx=8
        )

        return tree

    def dashboard_button(self, parent, text, command, row, column, icon="•"):
        card = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        card.grid(
            row=row,
            column=column,
            padx=8,
            pady=8,
            sticky="nsew"
        )

        icon_label = tk.Label(
            card,
            text=icon,
            bg=LIGHT_BLUE,
            fg=BLUE,
            font=("Segoe UI Symbol", 14, "bold"),
            width=3,
            height=1
        )
        icon_label.pack(anchor="w", padx=16, pady=(16, 8))

        tk.Label(
            card,
            text=text,
            bg=WHITE,
            fg=NAVY,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", padx=16)

        tk.Button(
            card,
            text="Open  →",
            command=command,
            bg=WHITE,
            fg=BLUE,
            activebackground=WHITE,
            activeforeground=BLUE_HOVER,
            bd=0,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2"
        ).pack(anchor="w", padx=16, pady=(8, 16))

        card.bind("<Button-1>", lambda e: command())
        icon_label.bind("<Button-1>", lambda e: command())

        return card

    def sidebar_button(self, parent, text, command, icon="•"):
        frame = tk.Frame(parent, bg=NAVY)
        frame.pack(fill="x", padx=12, pady=2)

        button = tk.Button(
            frame,
            text=f"  {icon}   {text}",
            command=command,
            anchor="w",
            bg=NAVY,
            fg="#DCE7F5",
            activebackground="#1D426B",
            activeforeground=WHITE,
            bd=0,
            relief="flat",
            font=("Segoe UI", 10),
            padx=12,
            pady=10,
            cursor="hand2"
        )
        button.pack(fill="x")
        return button

    # ========================================================
    # LOGIN
    # ========================================================

    def show_login(self):
        self.clear_window()

        outer = tk.Frame(self.root, bg=BG)
        outer.pack(expand=True, fill="both")

        # Left branding section
        left = tk.Frame(
            outer,
            bg=NAVY,
            width=470
        )
        left.pack(
            side="left",
            fill="both",
            expand=True
        )

        brand = tk.Frame(left, bg=NAVY)
        brand.place(relx=0.12, rely=0.18, relwidth=0.76)

        tk.Label(
            brand,
            text="⌂",
            bg=NAVY,
            fg=WHITE,
            font=("Segoe UI Symbol", 48, "bold")
        ).pack(anchor="w")

        tk.Label(
            brand,
            text="SMART SERVICE",
            bg=NAVY,
            fg=WHITE,
            font=("Segoe UI", 27, "bold")
        ).pack(anchor="w")

        tk.Label(
            brand,
            text="BOOK TRUSTED SERVICES EASILY",
            bg=NAVY,
            fg="#60A5FA",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(0, 45))

        tk.Label(
            brand,
            text="Your Home\nServices,\nSimplified.",
            bg=NAVY,
            fg=WHITE,
            justify="left",
            font=("Segoe UI", 27, "bold")
        ).pack(anchor="w")

        benefits = [
            ("✓", "Verified professionals"),
            ("⚡", "Quick & easy booking"),
            ("▣", "Track & manage bookings"),
            ("★", "Reliable & affordable")
        ]

        for icon, text in benefits:
            row = tk.Frame(brand, bg=NAVY)
            row.pack(anchor="w", pady=8)

            tk.Label(
                row,
                text=icon,
                bg=NAVY,
                fg="#60A5FA",
                font=("Segoe UI", 12, "bold"),
                width=3
            ).pack(side="left")

            tk.Label(
                row,
                text=text,
                bg=NAVY,
                fg="#DCE7F5",
                font=("Segoe UI", 10)
            ).pack(side="left")

        # Right login section
        right = tk.Frame(
            outer,
            bg="#F8FAFC",
            width=600
        )
        right.pack(
            side="right",
            fill="both",
            expand=True
        )

        card = tk.Frame(
            right,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        card.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            relwidth=0.72,
            relheight=0.68
        )

        tk.Label(
            card,
            text="Welcome Back",
            bg=WHITE,
            fg=NAVY,
            font=("Segoe UI", 25, "bold")
        ).pack(pady=(42, 5))

        tk.Label(
            card,
            text="Login to your Smart Service account",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 10)
        ).pack(pady=(0, 30))

        form = tk.Frame(card, bg=WHITE)
        form.pack(fill="x", padx=42)

        tk.Label(
            form,
            text="Email address",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", pady=(0, 6))

        self.email_entry = ttk.Entry(form)
        self.email_entry.pack(fill="x", ipady=3, pady=(0, 17))

        tk.Label(
            form,
            text="Password",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", pady=(0, 6))

        self.password_entry = ttk.Entry(
            form,
            show="•"
        )
        self.password_entry.pack(fill="x", ipady=3, pady=(0, 12))

        options = tk.Frame(form, bg=WHITE)
        options.pack(fill="x", pady=(0, 18))

        remember = tk.BooleanVar(value=True)

        tk.Checkbutton(
            options,
            text="Remember me",
            variable=remember,
            bg=WHITE,
            fg=MUTED,
            activebackground=WHITE,
            activeforeground=MUTED,
            selectcolor=WHITE,
            bd=0,
            font=("Segoe UI", 8)
        ).pack(side="left")

        tk.Label(
            options,
            text="Secure login",
            bg=WHITE,
            fg=BLUE,
            font=("Segoe UI", 8, "bold")
        ).pack(side="right")

        tk.Button(
            form,
            text="LOGIN   →",
            command=self.login,
            bg=BLUE,
            fg=WHITE,
            activebackground=BLUE_HOVER,
            activeforeground=WHITE,
            bd=0,
            font=("Segoe UI", 10, "bold"),
            pady=11,
            cursor="hand2"
        ).pack(fill="x")

        tk.Label(
            card,
            text="Online Service Booking Platform",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 8)
        ).pack(side="bottom", pady=18)

        self.email_entry.focus_set()

        self.password_entry.bind(
            "<Return>",
            lambda event: self.login()
        )

    # ========================================================
    # LOGIN
    # ========================================================

    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not email or not password:
            messagebox.showwarning(
                "Login",
                "Please enter email and password."
            )
            return

        password_hash = hashlib.sha256(
            password.encode()
        ).hexdigest()

        cursor = self.connection.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT
                    user_id,
                    name,
                    email,
                    role
                FROM users
                WHERE email = %s
                  AND password_hash = %s
            """, (
                email,
                password_hash
            ))

            user = cursor.fetchone()
        finally:
            cursor.close()

        if not user:
            messagebox.showerror(
                "Login Failed",
                "Invalid email or password."
            )
            return

        self.user = user

        if user["role"] == "customer":
            self.show_customer_dashboard()

        elif user["role"] == "provider":
            cursor = self.connection.cursor()

            try:
                cursor.execute("""
                    SELECT provider_id
                    FROM providers
                    WHERE user_id = %s
                """, (user["user_id"],))

                provider = cursor.fetchone()
            finally:
                cursor.close()

            if not provider:
                messagebox.showerror(
                    "Error",
                    "Provider profile not found."
                )
                return

            self.provider_id = provider[0]
            self.show_provider_dashboard()

        else:
            messagebox.showerror(
                "Error",
                "Unknown user role."
            )

    # ========================================================
    # CUSTOMER LAYOUT
    # ========================================================

    def build_customer_layout(self):
        self.clear_window()

        sidebar = tk.Frame(
            self.root,
            bg=NAVY,
            width=235
        )
        sidebar.pack(
            side="left",
            fill="y"
        )
        sidebar.pack_propagate(False)

        brand = tk.Frame(sidebar, bg=NAVY)
        brand.pack(fill="x", padx=22, pady=(28, 25))

        tk.Label(
            brand,
            text="⌂  SMART",
            bg=NAVY,
            fg=WHITE,
            font=("Segoe UI", 17, "bold")
        ).pack(anchor="w")

        tk.Label(
            brand,
            text="SERVICE",
            bg=NAVY,
            fg="#60A5FA",
            font=("Segoe UI", 17, "bold")
        ).pack(anchor="w", padx=28)

        tk.Frame(
            sidebar,
            bg="#29476A",
            height=1
        ).pack(fill="x", padx=20, pady=(0, 15))

        self.sidebar_button(
            sidebar, "Dashboard",
            self.show_customer_dashboard,
            "⌂"
        )
        self.sidebar_button(
            sidebar, "Service Categories",
            self.show_categories_gui,
            "▦"
        )
        self.sidebar_button(
            sidebar, "View Services",
            self.show_services_gui,
            "▤"
        )
        self.sidebar_button(
            sidebar, "Find Providers",
            self.show_providers_gui,
            "♙"
        )
        self.sidebar_button(
            sidebar, "Create Booking",
            self.create_booking_gui,
            "▣"
        )
        self.sidebar_button(
            sidebar, "My Bookings",
            self.show_customer_bookings,
            "◷"
        )
        self.sidebar_button(
            sidebar, "Cancel Booking",
            self.cancel_booking_gui,
            "×"
        )
        self.sidebar_button(
            sidebar, "Reschedule",
            self.reschedule_booking_gui,
            "↻"
        )

        bottom = tk.Frame(sidebar, bg=NAVY)
        bottom.pack(side="bottom", fill="x", pady=18)

        tk.Frame(
            bottom,
            bg="#29476A",
            height=1
        ).pack(fill="x", padx=20, pady=10)

        self.sidebar_button(
            bottom,
            "Logout",
            self.logout,
            "↪"
        )

        content = tk.Frame(
            self.root,
            bg=BG
        )
        content.pack(
            side="left",
            expand=True,
            fill="both"
        )

        return content

    # ========================================================
    # CUSTOMER DASHBOARD
    # ========================================================

    def show_customer_dashboard(self):
        content = self.build_customer_layout()

        top = tk.Frame(content, bg=BG)
        top.pack(fill="x", padx=30, pady=(24, 10))

        left = tk.Frame(top, bg=BG)
        left.pack(side="left")

        tk.Label(
            left,
            text="Customer Dashboard",
            bg=BG,
            fg=NAVY,
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w")

        tk.Label(
            left,
            text=f"Welcome back, {self.user['name']}",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(3, 0))

        user_badge = tk.Frame(
            top,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        user_badge.pack(side="right")

        tk.Label(
            user_badge,
            text=(self.user["name"][:1] or "S").upper(),
            bg=BLUE,
            fg=WHITE,
            font=("Segoe UI", 10, "bold"),
            width=3,
            height=1
        ).pack(side="left", padx=10, pady=8)

        tk.Label(
            user_badge,
            text=self.user["name"],
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 9, "bold")
        ).pack(side="left", padx=(0, 12))

        # Hero
        hero = tk.Frame(
            content,
            bg="#E8F1FF",
            highlightbackground="#C7D9F7",
            highlightthickness=1
        )
        hero.pack(fill="x", padx=30, pady=12)

        hero_left = tk.Frame(hero, bg="#E8F1FF")
        hero_left.pack(side="left", padx=25, pady=22)

        tk.Label(
            hero_left,
            text="FIND TRUSTED PROFESSIONALS",
            bg="#E8F1FF",
            fg=BLUE,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w")

        tk.Label(
            hero_left,
            text="for your service needs",
            bg="#E8F1FF",
            fg=NAVY,
            font=("Segoe UI", 19, "bold")
        ).pack(anchor="w", pady=(3, 2))

        tk.Label(
            hero_left,
            text="Book home services quickly and easily.",
            bg="#E8F1FF",
            fg=MUTED,
            font=("Segoe UI", 9)
        ).pack(anchor="w")

        search_frame = tk.Frame(
            hero_left,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        search_frame.pack(
            fill="x",
            pady=(15, 0)
        )

        search_entry = ttk.Entry(
            search_frame
        )
        search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=10,
            ipady=3
        )

        ttk.Button(
            search_frame,
            text="Search",
            style="Primary.TButton",
            command=self.show_services_gui
        ).pack(side="right", padx=4, pady=4)

        tk.Label(
            hero,
            text="⚒",
            bg="#E8F1FF",
            fg=BLUE,
            font=("Segoe UI Symbol", 55, "bold")
        ).pack(side="right", padx=55, pady=15)

        # Action cards
        actions = tk.Frame(content, bg=BG)
        actions.pack(fill="x", padx=30, pady=10)

        actions.columnconfigure((0, 1, 2, 3), weight=1)

        self.dashboard_button(
            actions,
            "Service Categories",
            self.show_categories_gui,
            0, 0, "⚙"
        )
        self.dashboard_button(
            actions,
            "View Services",
            self.show_services_gui,
            0, 1, "▦"
        )
        self.dashboard_button(
            actions,
            "Find Providers",
            self.show_providers_gui,
            0, 2, "♙"
        )
        self.dashboard_button(
            actions,
            "Create Booking",
            self.create_booking_gui,
            0, 3, "▣"
        )

        # Popular services
        section = tk.Frame(content, bg=BG)
        section.pack(fill="x", padx=30, pady=(18, 0))

        tk.Label(
            section,
            text="Popular Service Categories",
            bg=BG,
            fg=NAVY,
            font=("Segoe UI", 13, "bold")
        ).pack(side="left")

        tk.Button(
            section,
            text="View All →",
            command=self.show_services_gui,
            bg=BG,
            fg=BLUE,
            activebackground=BG,
            activeforeground=BLUE_HOVER,
            bd=0,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2"
        ).pack(side="right")

        popular = tk.Frame(content, bg=BG)
        popular.pack(fill="x", padx=30, pady=12)

        services = [
            ("⚡", "Electrical", "Services", "#FEF3C7", ORANGE),
            ("⚙", "Plumbing", "Services", "#E0F2FE", "#0284C7"),
            ("❄", "AC Service", "& Repair", "#EDE9FE", PURPLE),
            ("▰", "Painting", "Services", "#FCE7F3", "#DB2777"),
            ("⌂", "Carpentry", "Services", "#F3E8FF", "#9333EA"),
            ("✦", "Cleaning", "Services", "#DCFCE7", GREEN)
        ]

        for i, (icon, title, sub, icon_bg, icon_fg) in enumerate(services):
            popular.columnconfigure(i, weight=1)

            card = tk.Frame(
                popular,
                bg=WHITE,
                highlightbackground=BORDER,
                highlightthickness=1
            )
            card.grid(
                row=0,
                column=i,
                padx=5,
                sticky="nsew"
            )

            tk.Label(
                card,
                text=icon,
                bg=icon_bg,
                fg=icon_fg,
                font=("Segoe UI Symbol", 14, "bold"),
                width=3,
                height=1
            ).pack(anchor="w", padx=12, pady=(12, 8))

            tk.Label(
                card,
                text=title,
                bg=WHITE,
                fg=TEXT,
                font=("Segoe UI", 9, "bold")
            ).pack(anchor="w", padx=12)

            tk.Label(
                card,
                text=sub,
                bg=WHITE,
                fg=MUTED,
                font=("Segoe UI", 8)
            ).pack(anchor="w", padx=12, pady=(0, 12))

    # ========================================================
    # CUSTOMER - CATEGORIES
    # ========================================================

    def show_categories_gui(self):
        self.build_customer_layout()

        self.create_page_header(
            "Service Categories",
            "Browse available service categories",
            self.show_customer_dashboard
        )

        tree = self.create_tree(
            [
                ("ID", 80),
                ("Category", 280),
                ("Description", 650)
            ]
        )

        cursor = self.connection.cursor()

        try:
            cursor.execute("""
                SELECT
                    category_id,
                    category_name,
                    description
                FROM service_categories
                ORDER BY category_id
            """)

            rows = cursor.fetchall()
        finally:
            cursor.close()

        for row in rows:
            tree.insert("", "end", values=row)

    # ========================================================
    # SERVICES
    # ========================================================

    def show_services_gui(self):
        self.build_customer_layout()

        self.create_page_header(
            "Available Services",
            "Choose a service and find a suitable provider",
            self.show_customer_dashboard
        )

        tree = self.create_tree(
            [
                ("ID", 60),
                ("Service", 240),
                ("Description", 400),
                ("Duration", 100),
                ("Price", 100)
            ]
        )

        cursor = self.connection.cursor()

        try:
            cursor.execute("""
                SELECT
                    service_id,
                    service_name,
                    description,
                    estimated_duration,
                    price
                FROM services
                WHERE is_active = 1
                ORDER BY service_id
            """)

            rows = cursor.fetchall()
        finally:
            cursor.close()

        for row in rows:
            tree.insert(
                "",
                "end",
                values=(
                    row[0],
                    row[1],
                    row[2],
                    f"{row[3]} min",
                    f"₹{row[4]}"
                )
            )

    # ========================================================
    # PROVIDERS
    # ========================================================

    def show_providers_gui(self):
        self.build_customer_layout()

        self.create_page_header(
            "Find Providers",
            "Search professionals by service",
            self.show_customer_dashboard
        )

        top = tk.Frame(
            self.root,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        top.pack(fill="x", padx=30, pady=(0, 10))

        tk.Label(
            top,
            text="Select Service",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 9, "bold")
        ).pack(side="left", padx=(18, 8), pady=14)

        cursor = self.connection.cursor()

        try:
            cursor.execute("""
                SELECT
                    service_id,
                    service_name
                FROM services
                WHERE is_active = 1
                ORDER BY service_id
            """)
            services = cursor.fetchall()
        finally:
            cursor.close()

        service_map = {
            f"{row[0]} - {row[1]}": row[0]
            for row in services
        }

        combo = ttk.Combobox(
            top,
            values=list(service_map.keys()),
            width=42,
            state="readonly"
        )
        combo.pack(side="left", padx=8, pady=10)

        tree = self.create_tree(
            [
                ("Provider", 330),
                ("Location", 250),
                ("Price", 150)
            ]
        )

        def load_providers():
            for item in tree.get_children():
                tree.delete(item)

            selected = combo.get()

            if not selected:
                messagebox.showwarning(
                    "Find Providers",
                    "Please select a service."
                )
                return

            service_id = service_map[selected]

            cursor = self.connection.cursor()

            try:
                cursor.execute("""
                    SELECT
                        p.business_name,
                        p.location,
                        ps.price
                    FROM provider_services ps
                    JOIN providers p
                        ON ps.provider_id = p.provider_id
                    WHERE ps.service_id = %s
                      AND ps.is_available = 1
                """, (service_id,))

                providers = cursor.fetchall()
            finally:
                cursor.close()

            for provider in providers:
                tree.insert(
                    "",
                    "end",
                    values=(
                        provider[0],
                        provider[1],
                        f"₹{provider[2]}"
                    )
                )

            if not providers:
                messagebox.showinfo(
                    "Providers",
                    "No providers are currently available."
                )

        ttk.Button(
            top,
            text="Search",
            command=load_providers,
            style="Primary.TButton"
        ).pack(side="left", padx=8, pady=7)

    # ========================================================
    # CREATE BOOKING
    # ========================================================

    def create_booking_gui(self):
        self.build_customer_layout()

        self.create_page_header(
            "Create Booking",
            "Book a trusted professional in a few steps",
            self.show_customer_dashboard
        )

        outer = tk.Frame(
            self.root,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        outer.pack(
            padx=30,
            pady=5,
            fill="both",
            expand=True
        )

        frame = tk.Frame(outer, bg=WHITE)
        frame.pack(padx=45, pady=25, anchor="nw")

        def label(text, row):
            tk.Label(
                frame,
                text=text,
                bg=WHITE,
                fg=TEXT,
                font=("Segoe UI", 9, "bold")
            ).grid(
                row=row,
                column=0,
                sticky="w",
                padx=(0, 25),
                pady=10
            )

        label("Service", 0)

        cursor = self.connection.cursor()

        try:
            cursor.execute("""
                SELECT
                    service_id,
                    service_name,
                    price
                FROM services
                WHERE is_active = 1
                ORDER BY service_id
            """)
            services = cursor.fetchall()
        finally:
            cursor.close()

        service_map = {
            f"{row[1]} - ₹{row[2]}": row[0]
            for row in services
        }

        service_combo = ttk.Combobox(
            frame,
            values=list(service_map.keys()),
            width=48,
            state="readonly"
        )
        service_combo.grid(row=0, column=1, pady=10)

        label("Provider", 1)

        provider_combo = ttk.Combobox(
            frame,
            width=48,
            state="readonly"
        )
        provider_combo.grid(row=1, column=1, pady=10)

        provider_map = {}

        def load_providers(event=None):
            provider_combo.set("")

            selected = service_combo.get()
            if not selected:
                return

            service_id = service_map[selected]

            cursor = self.connection.cursor()

            try:
                cursor.execute("""
                    SELECT
                        p.provider_id,
                        p.business_name,
                        p.location,
                        ps.price
                    FROM provider_services ps
                    JOIN providers p
                        ON ps.provider_id = p.provider_id
                    WHERE ps.service_id = %s
                      AND ps.is_available = 1
                """, (service_id,))

                providers = cursor.fetchall()
            finally:
                cursor.close()

            provider_map.clear()
            values = []

            for provider in providers:
                display = (
                    f"{provider[1]} | "
                    f"{provider[2]} | "
                    f"₹{provider[3]}"
                )
                values.append(display)
                provider_map[display] = provider

            provider_combo["values"] = values

        service_combo.bind(
            "<<ComboboxSelected>>",
            load_providers
        )

        label("Booking Date", 2)

        date_entry = ttk.Entry(frame, width=51)
        date_entry.grid(row=2, column=1, pady=10)
        date_entry.insert(0, date.today().isoformat())

        label("Time Slot", 3)

        slot_combo = ttk.Combobox(
            frame,
            width=48,
            state="readonly"
        )
        slot_combo.grid(row=3, column=1, pady=10)

        slot_map = {}

        def load_slots():
            slot_combo.set("")
            slot_map.clear()

            selected_provider = provider_combo.get()
            booking_date = date_entry.get().strip()

            if not selected_provider or not booking_date:
                messagebox.showwarning(
                    "Missing Information",
                    "Select provider and enter date."
                )
                return

            provider = provider_map[selected_provider]
            provider_id = provider[0]

            cursor = self.connection.cursor()

            try:
                cursor.execute("""
                    SELECT
                        availability_id,
                        start_time,
                        end_time
                    FROM availability
                    WHERE provider_id = %s
                      AND available_date = %s
                      AND is_available = 1
                    ORDER BY start_time
                """, (
                    provider_id,
                    booking_date
                ))

                slots = cursor.fetchall()
            finally:
                cursor.close()

            values = []

            for slot in slots:
                display = f"{slot[1]} - {slot[2]}"
                values.append(display)
                slot_map[display] = slot

            slot_combo["values"] = values

            if not values:
                messagebox.showinfo(
                    "Availability",
                    "No available slots for this date."
                )

        ttk.Button(
            frame,
            text="Check Availability",
            command=load_slots,
            style="Secondary.TButton"
        ).grid(row=4, column=1, sticky="w", pady=6)

        label("Customer Note", 5)

        note_entry = ttk.Entry(frame, width=51)
        note_entry.grid(row=5, column=1, pady=10)

        def book():
            selected_service = service_combo.get()
            selected_provider = provider_combo.get()
            selected_slot = slot_combo.get()
            booking_date = date_entry.get().strip()
            note = note_entry.get().strip()

            if not selected_service:
                messagebox.showwarning(
                    "Booking",
                    "Please select a service."
                )
                return

            if not selected_provider:
                messagebox.showwarning(
                    "Booking",
                    "Please select a provider."
                )
                return

            if not selected_slot:
                messagebox.showwarning(
                    "Booking",
                    "Please select a time slot."
                )
                return

            if not booking_date:
                messagebox.showwarning(
                    "Booking",
                    "Please enter booking date."
                )
                return

            provider = provider_map[selected_provider]
            slot = slot_map[selected_slot]

            provider_id = provider[0]
            price = provider[3]
            availability_id = slot[0]
            booking_time = slot[1]
            service_id = service_map[selected_service]

            try:
                cursor = self.connection.cursor()

                cursor.execute("""
                    INSERT INTO bookings
                    (
                        customer_id,
                        provider_id,
                        service_id,
                        availability_id,
                        booking_date,
                        booking_time,
                        customer_email,
                        status,
                        customer_note,
                        price
                    )
                    VALUES
                    (
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s
                    )
                """, (
                    self.user["user_id"],
                    provider_id,
                    service_id,
                    availability_id,
                    booking_date,
                    booking_time,
                    self.user["email"],
                    "pending",
                    note,
                    price
                ))

                booking_id = cursor.lastrowid

                cursor.execute("""
                    UPDATE availability
                    SET is_available = 0
                    WHERE availability_id = %s
                """, (availability_id,))

                self.connection.commit()
                cursor.close()

                messagebox.showinfo(
                    "Booking Successful",
                    f"Booking created successfully!\n\n"
                    f"Booking ID: {booking_id}\n"
                    f"Provider: {provider[1]}\n"
                    f"Date: {booking_date}\n"
                    f"Time: {booking_time}\n"
                    f"Price: ₹{price}\n"
                    f"Status: pending"
                )

                self.show_customer_dashboard()

            except Exception as error:
                self.connection.rollback()

                messagebox.showerror(
                    "Booking Failed",
                    str(error)
                )

        ttk.Button(
            frame,
            text="CREATE BOOKING",
            command=book,
            style="Primary.TButton"
        ).grid(
            row=6,
            column=1,
            sticky="w",
            pady=22
        )

    # ========================================================
    # CUSTOMER BOOKINGS
    # ========================================================

    def show_customer_bookings(self):
        self.build_customer_layout()

        self.create_page_header(
            "My Bookings",
            "View and track all your service bookings",
            self.show_customer_dashboard
        )

        tree = self.create_tree(
            [
                ("ID", 60),
                ("Service", 220),
                ("Provider", 220),
                ("Date", 110),
                ("Time", 100),
                ("Price", 100),
                ("Status", 120)
            ]
        )

        cursor = self.connection.cursor()

        try:
            cursor.execute("""
                SELECT
                    b.booking_id,
                    s.service_name,
                    p.business_name,
                    b.booking_date,
                    b.booking_time,
                    b.price,
                    b.status
                FROM bookings b
                JOIN services s
                    ON b.service_id = s.service_id
                JOIN providers p
                    ON b.provider_id = p.provider_id
                WHERE b.customer_id = %s
                ORDER BY b.booking_date DESC
            """, (self.user["user_id"],))

            bookings = cursor.fetchall()
        finally:
            cursor.close()

        for booking in bookings:
            tree.insert(
                "",
                "end",
                values=(
                    booking[0],
                    booking[1],
                    booking[2],
                    booking[3],
                    booking[4],
                    f"₹{booking[5]}",
                    booking[6]
                )
            )

    # ========================================================
    # CANCEL BOOKING
    # ========================================================

    def cancel_booking_gui(self):
        self.build_customer_layout()

        self.create_page_header(
            "Cancel Booking",
            "Cancel an active booking using its ID",
            self.show_customer_dashboard
        )

        card = tk.Frame(
            self.root,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        card.pack(
            padx=30,
            pady=10,
            anchor="nw"
        )

        tk.Label(
            card,
            text="Booking ID",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 9, "bold")
        ).grid(row=0, column=0, padx=25, pady=25)

        booking_entry = ttk.Entry(card, width=32)
        booking_entry.grid(row=0, column=1, padx=10, pady=25)

        def cancel():
            booking_id = booking_entry.get().strip()

            if not booking_id:
                messagebox.showwarning(
                    "Cancel",
                    "Enter Booking ID."
                )
                return

            cursor = self.connection.cursor()

            try:
                cursor.execute("""
                    SELECT
                        availability_id,
                        status
                    FROM bookings
                    WHERE booking_id = %s
                      AND customer_id = %s
                """, (
                    booking_id,
                    self.user["user_id"]
                ))

                booking = cursor.fetchone()

                if not booking:
                    messagebox.showerror(
                        "Error",
                        "Booking not found."
                    )
                    return

                availability_id = booking[0]
                status = booking[1]

                if status in (
                    "completed",
                    "cancelled",
                    "rejected"
                ):
                    messagebox.showwarning(
                        "Cannot Cancel",
                        f"Booking is already {status}."
                    )
                    return

                cursor.execute("""
                    UPDATE bookings
                    SET status = 'cancelled'
                    WHERE booking_id = %s
                      AND customer_id = %s
                """, (
                    booking_id,
                    self.user["user_id"]
                ))

                cursor.execute("""
                    UPDATE availability
                    SET is_available = 1
                    WHERE availability_id = %s
                """, (availability_id,))

                self.connection.commit()

            except Exception as error:
                self.connection.rollback()
                messagebox.showerror("Error", str(error))
                return
            finally:
                cursor.close()

            messagebox.showinfo(
                "Success",
                "Booking cancelled successfully."
            )

            self.show_customer_dashboard()

        ttk.Button(
            card,
            text="CANCEL BOOKING",
            command=cancel,
            style="Danger.TButton"
        ).grid(
            row=1,
            column=0,
            columnspan=2,
            pady=(0, 25)
        )

    # ========================================================
    # RESCHEDULE BOOKING
    # ========================================================

    def reschedule_booking_gui(self):
        self.build_customer_layout()

        self.create_page_header(
            "Reschedule Booking",
            "Choose a new available date and time",
            self.show_customer_dashboard
        )

        card = tk.Frame(
            self.root,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        card.pack(
            padx=30,
            pady=5,
            fill="x"
        )

        frame = tk.Frame(card, bg=WHITE)
        frame.pack(padx=35, pady=25, anchor="w")

        labels = [
            "Booking ID",
            "New Date",
            "New Time Slot"
        ]

        for row, text in enumerate(labels):
            tk.Label(
                frame,
                text=text,
                bg=WHITE,
                fg=TEXT,
                font=("Segoe UI", 9, "bold")
            ).grid(
                row=row,
                column=0,
                sticky="w",
                padx=(0, 25),
                pady=10
            )

        booking_entry = ttk.Entry(frame, width=40)
        booking_entry.grid(row=0, column=1, pady=10)

        date_entry = ttk.Entry(frame, width=40)
        date_entry.grid(row=1, column=1, pady=10)
        date_entry.insert(0, date.today().isoformat())

        slot_combo = ttk.Combobox(
            frame,
            width=37,
            state="readonly"
        )
        slot_combo.grid(row=2, column=1, pady=10)

        slot_map = {}
        booking_data = {}

        def load_slots():
            booking_id = booking_entry.get().strip()
            new_date = date_entry.get().strip()

            if not booking_id or not new_date:
                messagebox.showwarning(
                    "Reschedule",
                    "Enter booking ID and date."
                )
                return

            cursor = self.connection.cursor()

            try:
                cursor.execute("""
                    SELECT
                        provider_id,
                        availability_id,
                        status
                    FROM bookings
                    WHERE booking_id = %s
                      AND customer_id = %s
                """, (
                    booking_id,
                    self.user["user_id"]
                ))

                booking = cursor.fetchone()

                if not booking:
                    messagebox.showerror(
                        "Error",
                        "Booking not found."
                    )
                    return

                if booking[2] in (
                    "completed",
                    "cancelled",
                    "rejected",
                    "in_progress"
                ):
                    messagebox.showwarning(
                        "Cannot Reschedule",
                        f"Booking is {booking[2]}."
                    )
                    return

                booking_data["provider_id"] = booking[0]
                booking_data["old_slot"] = booking[1]

                cursor.execute("""
                    SELECT
                        availability_id,
                        start_time,
                        end_time
                    FROM availability
                    WHERE provider_id = %s
                      AND available_date = %s
                      AND is_available = 1
                    ORDER BY start_time
                """, (
                    booking[0],
                    new_date
                ))

                slots = cursor.fetchall()

            finally:
                cursor.close()

            slot_map.clear()
            values = []

            for slot in slots:
                display = f"{slot[1]} - {slot[2]}"
                values.append(display)
                slot_map[display] = slot

            slot_combo["values"] = values

            if not values:
                messagebox.showinfo(
                    "Availability",
                    "No available slots."
                )

        ttk.Button(
            frame,
            text="Check Available Slots",
            command=load_slots,
            style="Secondary.TButton"
        ).grid(
            row=3,
            column=1,
            sticky="w",
            pady=12
        )

        def reschedule():
            booking_id = booking_entry.get().strip()
            new_date = date_entry.get().strip()
            selected = slot_combo.get()

            if not booking_id or not new_date or not selected:
                messagebox.showwarning(
                    "Reschedule",
                    "Complete all fields."
                )
                return

            slot = slot_map[selected]
            new_slot_id = slot[0]
            new_time = slot[1]
            old_slot_id = booking_data["old_slot"]

            try:
                cursor = self.connection.cursor()

                cursor.execute("""
                    UPDATE bookings
                    SET
                        availability_id = %s,
                        booking_date = %s,
                        booking_time = %s,
                        status = 'pending'
                    WHERE booking_id = %s
                      AND customer_id = %s
                """, (
                    new_slot_id,
                    new_date,
                    new_time,
                    booking_id,
                    self.user["user_id"]
                ))

                cursor.execute("""
                    UPDATE availability
                    SET is_available = 0
                    WHERE availability_id = %s
                """, (new_slot_id,))

                cursor.execute("""
                    UPDATE availability
                    SET is_available = 1
                    WHERE availability_id = %s
                """, (old_slot_id,))

                self.connection.commit()
                cursor.close()

                messagebox.showinfo(
                    "Success",
                    "Booking rescheduled successfully."
                )

                self.show_customer_dashboard()

            except Exception as error:
                self.connection.rollback()
                messagebox.showerror(
                    "Error",
                    str(error)
                )

        ttk.Button(
            frame,
            text="RESCHEDULE BOOKING",
            command=reschedule,
            style="Primary.TButton"
        ).grid(
            row=4,
            column=1,
            sticky="w",
            pady=20
        )

    # ========================================================
    # PROVIDER LAYOUT
    # ========================================================

    def build_provider_layout(self, provider_name="", location=""):
        self.clear_window()

        sidebar = tk.Frame(
            self.root,
            bg=NAVY,
            width=235
        )
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        brand = tk.Frame(sidebar, bg=NAVY)
        brand.pack(fill="x", padx=22, pady=(28, 20))

        tk.Label(
            brand,
            text="⌂  SMART",
            bg=NAVY,
            fg=WHITE,
            font=("Segoe UI", 17, "bold")
        ).pack(anchor="w")

        tk.Label(
            brand,
            text="SERVICE",
            bg=NAVY,
            fg="#60A5FA",
            font=("Segoe UI", 17, "bold")
        ).pack(anchor="w", padx=28)

        tk.Frame(
            sidebar,
            bg="#29476A",
            height=1
        ).pack(fill="x", padx=20, pady=(0, 15))

        self.sidebar_button(
            sidebar,
            "Dashboard",
            self.show_provider_dashboard,
            "⌂"
        )
        self.sidebar_button(
            sidebar,
            "My Bookings",
            self.provider_bookings_gui,
            "◷"
        )
        self.sidebar_button(
            sidebar,
            "Pending Bookings",
            self.provider_pending_gui,
            "!"
        )
        self.sidebar_button(
            sidebar,
            "Update Status",
            self.provider_status_gui,
            "✓"
        )

        bottom = tk.Frame(sidebar, bg=NAVY)
        bottom.pack(side="bottom", fill="x", pady=18)

        tk.Frame(
            bottom,
            bg="#29476A",
            height=1
        ).pack(fill="x", padx=20, pady=10)

        self.sidebar_button(
            bottom,
            "Logout",
            self.logout,
            "↪"
        )

        content = tk.Frame(self.root, bg=BG)
        content.pack(
            side="left",
            expand=True,
            fill="both"
        )

        return content

    # ========================================================
    # PROVIDER DASHBOARD
    # ========================================================

    def show_provider_dashboard(self):
        cursor = self.connection.cursor()

        try:
            cursor.execute("""
                SELECT
                    business_name,
                    location
                FROM providers
                WHERE provider_id = %s
            """, (self.provider_id,))

            provider = cursor.fetchone()
        finally:
            cursor.close()

        if not provider:
            messagebox.showerror(
                "Error",
                "Provider profile not found."
            )
            return

        content = self.build_provider_layout(
            provider[0],
            provider[1]
        )

        top = tk.Frame(content, bg=BG)
        top.pack(fill="x", padx=30, pady=(24, 12))

        left = tk.Frame(top, bg=BG)
        left.pack(side="left")

        tk.Label(
            left,
            text="Provider Dashboard",
            bg=BG,
            fg=NAVY,
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w")

        tk.Label(
            left,
            text=f"{provider[0]}  |  {provider[1]}",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(3, 0))

        badge = tk.Frame(top, bg=WHITE)
        badge.pack(side="right")

        tk.Label(
            badge,
            text=(self.user["name"][:1] or "P").upper(),
            bg=BLUE,
            fg=WHITE,
            font=("Segoe UI", 10, "bold"),
            width=3,
            height=1
        ).pack(side="left", padx=8, pady=7)

        tk.Label(
            badge,
            text=self.user["name"],
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 9, "bold")
        ).pack(side="left", padx=(0, 10))

        # Statistics
        stats = self.get_provider_stats()

        stats_frame = tk.Frame(content, bg=BG)
        stats_frame.pack(fill="x", padx=30, pady=8)

        cards = [
            ("▣", "Total Bookings", stats["total"], BLUE, LIGHT_BLUE),
            ("◷", "Pending", stats["pending"], ORANGE, LIGHT_ORANGE),
            ("✓", "Completed", stats["completed"], GREEN, LIGHT_GREEN),
            ("★", "Active Services", stats["services"], PURPLE, LIGHT_PURPLE)
        ]

        for i, (icon, title, number, fg, icon_bg) in enumerate(cards):
            stats_frame.columnconfigure(i, weight=1)

            card = tk.Frame(
                stats_frame,
                bg=WHITE,
                highlightbackground=BORDER,
                highlightthickness=1
            )
            card.grid(
                row=0,
                column=i,
                padx=5,
                sticky="nsew"
            )

            tk.Label(
                card,
                text=icon,
                bg=icon_bg,
                fg=fg,
                font=("Segoe UI Symbol", 13, "bold"),
                width=3
            ).pack(anchor="w", padx=15, pady=(15, 7))

            tk.Label(
                card,
                text=str(number),
                bg=WHITE,
                fg=NAVY,
                font=("Segoe UI", 20, "bold")
            ).pack(anchor="w", padx=15)

            tk.Label(
                card,
                text=title,
                bg=WHITE,
                fg=MUTED,
                font=("Segoe UI", 8)
            ).pack(anchor="w", padx=15, pady=(2, 15))

        tk.Label(
            content,
            text="Quick Actions",
            bg=BG,
            fg=NAVY,
            font=("Segoe UI", 13, "bold")
        ).pack(anchor="w", padx=30, pady=(22, 8))

        actions = tk.Frame(content, bg=BG)
        actions.pack(fill="x", padx=30)

        actions.columnconfigure((0, 1, 2), weight=1)

        self.dashboard_button(
            actions,
            "My Bookings",
            self.provider_bookings_gui,
            0, 0,
            "▣"
        )

        self.dashboard_button(
            actions,
            "Pending Bookings",
            self.provider_pending_gui,
            0, 1,
            "!"
        )

        self.dashboard_button(
            actions,
            "Update Booking Status",
            self.provider_status_gui,
            0, 2,
            "✓"
        )

        tk.Label(
            content,
            text="Recent Bookings",
            bg=BG,
            fg=NAVY,
            font=("Segoe UI", 13, "bold")
        ).pack(anchor="w", padx=30, pady=(22, 8))

        self.provider_recent_table(content)

    # ========================================================
    # PROVIDER STATS
    # ========================================================

    def get_provider_stats(self):
        stats = {
            "total": 0,
            "pending": 0,
            "completed": 0,
            "services": 0
        }

        cursor = self.connection.cursor()

        try:
            cursor.execute("""
                SELECT COUNT(*)
                FROM bookings
                WHERE provider_id = %s
            """, (self.provider_id,))
            stats["total"] = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(*)
                FROM bookings
                WHERE provider_id = %s
                  AND status = 'pending'
            """, (self.provider_id,))
            stats["pending"] = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(*)
                FROM bookings
                WHERE provider_id = %s
                  AND status = 'completed'
            """, (self.provider_id,))
            stats["completed"] = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(*)
                FROM provider_services
                WHERE provider_id = %s
                  AND is_available = 1
            """, (self.provider_id,))
            stats["services"] = cursor.fetchone()[0]

        finally:
            cursor.close()

        return stats

    # ========================================================
    # PROVIDER RECENT TABLE
    # ========================================================

    def provider_recent_table(self, parent):
        tree = self.create_tree(
            [
                ("ID", 60),
                ("Customer", 150),
                ("Service", 210),
                ("Date", 110),
                ("Time", 100),
                ("Status", 120)
            ],
            parent
        )

        # Limit height for dashboard
        tree.configure(height=6)

        cursor = self.connection.cursor()

        try:
            cursor.execute("""
                SELECT
                    b.booking_id,
                    u.name,
                    s.service_name,
                    b.booking_date,
                    b.booking_time,
                    b.status
                FROM bookings b
                JOIN users u
                    ON b.customer_id = u.user_id
                JOIN services s
                    ON b.service_id = s.service_id
                WHERE b.provider_id = %s
                ORDER BY b.booking_date DESC,
                         b.booking_time DESC
                LIMIT 6
            """, (self.provider_id,))

            bookings = cursor.fetchall()
        finally:
            cursor.close()

        for booking in bookings:
            tree.insert(
                "",
                "end",
                values=(
                    booking[0],
                    booking[1],
                    booking[2],
                    booking[3],
                    booking[4],
                    booking[5]
                )
            )

    # ========================================================
    # PROVIDER BOOKINGS
    # ========================================================

    def provider_bookings_gui(self):
        self.build_provider_layout()

        self.create_page_header(
            "My Bookings",
            "All bookings assigned to your business",
            self.show_provider_dashboard
        )

        tree = self.create_tree(
            [
                ("ID", 60),
                ("Service", 220),
                ("Date", 110),
                ("Time", 100),
                ("Price", 100),
                ("Status", 120),
                ("Note", 250)
            ]
        )

        cursor = self.connection.cursor()

        try:
            cursor.execute("""
                SELECT
                    b.booking_id,
                    s.service_name,
                    b.booking_date,
                    b.booking_time,
                    b.price,
                    b.status,
                    b.customer_note
                FROM bookings b
                JOIN services s
                    ON b.service_id = s.service_id
                WHERE b.provider_id = %s
                ORDER BY b.booking_date DESC
            """, (self.provider_id,))

            bookings = cursor.fetchall()
        finally:
            cursor.close()

        for booking in bookings:
            tree.insert(
                "",
                "end",
                values=(
                    booking[0],
                    booking[1],
                    booking[2],
                    booking[3],
                    f"₹{booking[4]}",
                    booking[5],
                    booking[6]
                )
            )

    # ========================================================
    # PROVIDER PENDING
    # ========================================================

    def provider_pending_gui(self):
        self.build_provider_layout()

        self.create_page_header(
            "Pending Bookings",
            "Bookings waiting for your response",
            self.show_provider_dashboard
        )

        tree = self.create_tree(
            [
                ("ID", 70),
                ("Customer", 150),
                ("Service", 220),
                ("Date", 110),
                ("Time", 100),
                ("Price", 100),
                ("Note", 250)
            ]
        )

        cursor = self.connection.cursor()

        try:
            cursor.execute("""
                SELECT
                    b.booking_id,
                    u.name,
                    s.service_name,
                    b.booking_date,
                    b.booking_time,
                    b.price,
                    b.customer_note
                FROM bookings b
                JOIN users u
                    ON b.customer_id = u.user_id
                JOIN services s
                    ON b.service_id = s.service_id
                WHERE b.provider_id = %s
                  AND b.status = 'pending'
                ORDER BY b.booking_date,
                         b.booking_time
            """, (self.provider_id,))

            bookings = cursor.fetchall()
        finally:
            cursor.close()

        for booking in bookings:
            tree.insert(
                "",
                "end",
                values=(
                    booking[0],
                    booking[1],
                    booking[2],
                    booking[3],
                    booking[4],
                    f"₹{booking[5]}",
                    booking[6]
                )
            )

    # ========================================================
    # PROVIDER STATUS
    # ========================================================

    def provider_status_gui(self):
        self.build_provider_layout()

        self.create_page_header(
            "Update Booking Status",
            "Manage the current status of your bookings",
            self.show_provider_dashboard
        )

        card = tk.Frame(
            self.root,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        card.pack(
            padx=30,
            pady=5,
            anchor="nw"
        )

        frame = tk.Frame(card, bg=WHITE)
        frame.pack(padx=35, pady=30)

        tk.Label(
            frame,
            text="Booking ID",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 9, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 25),
            pady=12
        )

        booking_entry = ttk.Entry(frame, width=35)
        booking_entry.grid(row=0, column=1, pady=12)

        tk.Label(
            frame,
            text="New Status",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 9, "bold")
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=(0, 25),
            pady=12
        )

        status_map = {
            "Accept": "accepted",
            "Reject": "rejected",
            "In Progress": "in_progress",
            "Completed": "completed",
            "Cancel": "cancelled"
        }

        status_combo = ttk.Combobox(
            frame,
            values=list(status_map.keys()),
            width=32,
            state="readonly"
        )
        status_combo.grid(row=1, column=1, pady=12)

        def update_status():
            booking_id = booking_entry.get().strip()
            selected_status = status_combo.get()

            if not booking_id or not selected_status:
                messagebox.showwarning(
                    "Status",
                    "Enter booking ID and select status."
                )
                return

            new_status = status_map[selected_status]

            cursor = self.connection.cursor()

            try:
                cursor.execute("""
                    SELECT
                        status,
                        availability_id
                    FROM bookings
                    WHERE booking_id = %s
                      AND provider_id = %s
                """, (
                    booking_id,
                    self.provider_id
                ))

                booking = cursor.fetchone()

                if not booking:
                    messagebox.showerror(
                        "Error",
                        "Booking not found."
                    )
                    return

                current_status = booking[0]
                availability_id = booking[1]

                valid = True

                if current_status == "pending":
                    valid = new_status in (
                        "accepted",
                        "rejected",
                        "cancelled"
                    )
                elif current_status == "accepted":
                    valid = new_status in (
                        "in_progress",
                        "cancelled"
                    )
                elif current_status == "in_progress":
                    valid = new_status == "completed"
                else:
                    valid = False

                if not valid:
                    messagebox.showwarning(
                        "Invalid Status",
                        f"Cannot change booking from "
                        f"{current_status} to {new_status}."
                    )
                    return

                cursor.execute("""
                    UPDATE bookings
                    SET status = %s
                    WHERE booking_id = %s
                      AND provider_id = %s
                """, (
                    new_status,
                    booking_id,
                    self.provider_id
                ))

                if new_status in (
                    "rejected",
                    "cancelled"
                ):
                    cursor.execute("""
                        UPDATE availability
                        SET is_available = 1
                        WHERE availability_id = %s
                    """, (availability_id,))

                self.connection.commit()

            except Exception as error:
                self.connection.rollback()
                messagebox.showerror("Error", str(error))
                return
            finally:
                cursor.close()

            messagebox.showinfo(
                "Success",
                f"Booking status updated to:\n{new_status}"
            )

            self.show_provider_dashboard()

        ttk.Button(
            frame,
            text="UPDATE STATUS",
            command=update_status,
            style="Primary.TButton"
        ).grid(
            row=2,
            column=0,
            columnspan=2,
            pady=22
        )

    # ========================================================
    # LOGOUT
    # ========================================================

    def logout(self):
        self.user = None
        self.provider_id = None
        self.show_login()

    # ========================================================
    # CLOSE APPLICATION
    # ========================================================

    def close_app(self):
        try:
            if self.connection:
                self.connection.close()
        except Exception:
            pass

        self.root.destroy()


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartServiceApp(root)

    root.protocol(
        "WM_DELETE_WINDOW",
        app.close_app
    )

    root.mainloop()
