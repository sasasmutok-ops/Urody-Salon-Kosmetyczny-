"""Single-window Urody salon application."""
from datetime import datetime, timedelta
from pathlib import Path
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from PIL import Image, ImageDraw, ImageEnhance, ImageTk
from calculator import open_calculator
from modules.appointment_logic import load_appointments
from modules.appointment_planner import AppointmentPlanner
from services import SERVICES
BG = '#F4F2EC'
GREEN = '#243D32'
GREEN_DARK = '#172B23'
TEXT = '#25352D'
MUTED = '#7B827B'
WHITE = '#FFFFFF'
BORDER = '#E7E4DA'
GOLD = '#C5A46D'
SAGE = '#E8EDE6'
SUCCESS_BG = '#EAF3EA'
SUCCESS_FG = '#326B45'
ERROR_BG = '#FCECEC'
ERROR_FG = '#9B3D4A'

class RoundedButton(tk.Canvas):
    """A small rounded button made with a Canvas."""

    def __init__(self,
        parent,
        text,
        command,
        bg_color=GREEN,
        fg_color=WHITE,
        hover_color=GREEN_DARK,
        height=42,
        font=('Arial', 10, 'bold'),
        width=None):
        self.text = text
        self.command = command
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.hover_color = hover_color
        self.current_color = bg_color
        self.button_font = tkfont.Font(parent, font=font)
        self.button_height = height
        if width is None:
            width = self.button_font.measure(text) + 36
        self.button_width = width
        super().__init__(parent,
            width=self.button_width,
            height=self.button_height,
            bg=parent.cget('bg'),
            highlightthickness=0,
            bd=0,
            cursor='hand2')
        self.draw_button()
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        self.bind('<Button-1>', self.on_click)

    def draw_button(self):
        """Draw the rounded shape and its text."""
        self.delete('all')
        x1, y1 = (2, 2)
        x2 = self.button_width - 2
        y2 = self.button_height - 2
        radius = 13
        color = self.current_color
        self.create_rectangle(x1 + radius, y1, x2 - radius, y2, fill=color, outline=color)
        self.create_rectangle(x1, y1 + radius, x2, y2 - radius, fill=color, outline=color)
        corners = [(x1, y1, x1 + radius * 2, y1 + radius * 2, 90),
            (x2 - radius * 2, y1, x2, y1 + radius * 2, 0),
            (x2 - radius * 2, y2 - radius * 2, x2, y2, 270),
            (x1, y2 - radius * 2, x1 + radius * 2, y2, 180)]
        for left, top, right, bottom, angle in corners:
            self.create_arc(left, top, right, bottom, start=angle, extent=90, style=tk.PIESLICE, fill=color, outline=color)
        self.create_text(self.button_width / 2, self.button_height / 2, text=self.text, fill=self.fg_color, font=self.button_font)

    def on_enter(self, _event=None):
        self.current_color = self.hover_color
        self.draw_button()

    def on_leave(self, _event=None):
        self.current_color = self.bg_color
        self.draw_button()

    def on_click(self, _event=None):
        if self.command:
            self.command()

class RoundedPanel(tk.Canvas):
    """A simple panel with rounded corners. Its children go inside .content."""

    def __init__(self, parent, bg_color=WHITE, outer_bg=BG, padding=18, radius=20, width=200):
        self.bg_color = bg_color
        self.padding = padding
        self.radius = radius
        self.resize_job = None
        super().__init__(parent, bg=outer_bg, width=width, height=100, highlightthickness=0, bd=0)
        self.content = tk.Frame(self, bg=bg_color)
        self.window_id = self.create_window((padding, padding), window=self.content, anchor='nw')
        self.bind('<Configure>', self._on_resize)
        self.content.bind('<Configure>', self._on_content_resize)
        self.after_idle(self._update_height)

    def _draw_rounded_background(self, width, height):
        self.delete('panel_background')
        left = 2
        top = 2
        right = max(left + 2, width - 2)
        bottom = max(top + 2, height - 2)
        radius = min(self.radius, (right - left) // 3, (bottom - top) // 3)
        color = self.bg_color
        self.create_rectangle(left + radius, top, right - radius, bottom, fill=color, outline=color, tags='panel_background')
        self.create_rectangle(left, top + radius, right, bottom - radius, fill=color, outline=color, tags='panel_background')
        self.create_oval(left, top, left + radius * 2, top + radius * 2, fill=color, outline=color, tags='panel_background')
        self.create_oval(right - radius * 2, top, right, top + radius * 2, fill=color, outline=color, tags='panel_background')
        self.create_oval(left, bottom - radius * 2, left + radius * 2, bottom, fill=color, outline=color, tags='panel_background')
        self.create_oval(right - radius * 2,
            bottom - radius * 2,
            right,
            bottom,
            fill=color,
            outline=color,
            tags='panel_background')
        self.tag_lower('panel_background')

    def _on_resize(self, event):
        content_width = max(1, event.width - self.padding * 2)
        self.itemconfigure(self.window_id, width=content_width)
        self.coords(self.window_id, self.padding, self.padding)
        self._draw_rounded_background(event.width, event.height)

    def _on_content_resize(self, _event=None):
        if self.resize_job is None:
            self.resize_job = self.after_idle(self._update_height)

    def _update_height(self):
        self.resize_job = None
        try:
            needed_height = self.content.winfo_reqheight() + self.padding * 2
            current_height = int(float(self.cget('height')))
            if abs(needed_height - current_height) > 2:
                self.configure(height=needed_height)
        except tk.TclError:
            pass

class UrodyApp:
    NAV_ITEMS = (('guide', 'Poradnik'), ('about', 'O salonie'))

    def __init__(self, root):
        self.root = root
        self.root.title('URODY — Salon Kosmetyczny')
        self.root.geometry('1180x760')
        self.root.minsize(1020, 690)
        self.root.configure(bg=BG)
        self.current_page = 'home'
        self.flash_message = ''
        self.nav_buttons = {}
        self.assets_path = Path(__file__).resolve().parent / 'modules' / 'assets'
        self.image_refs = {}
        self._clock_id = None
        self._configure_styles()
        self.create_header()
        self.create_shell()
        self.show_page('home')

    def _configure_styles(self):
        """Set a clean style for the table and scrollbar."""
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except tk.TclError:
            pass
        style.configure('Treeview',
            background=WHITE,
            fieldbackground=WHITE,
            foreground=TEXT,
            rowheight=34,
            borderwidth=0,
            font=('Arial', 9))
        style.configure('Treeview.Heading',
            background=GREEN,
            foreground=WHITE,
            relief='flat',
            font=('Arial', 9, 'bold'),
            padding=(8, 10))
        style.map('Treeview', background=[('selected', '#DCE7DC')], foreground=[('selected', GREEN_DARK)])
        style.configure('Vertical.TScrollbar', background='#D9DED6', troughcolor=BG, bordercolor=BG, arrowcolor=GREEN)

    def _start_header_clock(self):
        """Update the clock in the top bar every 30 seconds."""

        def update_clock():
            try:
                if not self.root.winfo_exists():
                    return
                self.clock_label.configure(text=datetime.now().strftime('%H:%M'))
                self._clock_id = self.root.after(30000, update_clock)
            except tk.TclError:
                self._clock_id = None
        update_clock()

    def create_header(self):
        header = tk.Frame(self.root, bg=GREEN, height=86)
        header.pack(fill='x')
        header.pack_propagate(False)
        brand = tk.Frame(header, bg=GREEN, cursor='hand2')
        brand.pack(side='left', padx=30, pady=13)
        brand_title = tk.Label(brand, text='URODY', font=('Georgia', 27, 'bold'), bg=GREEN, fg=WHITE, cursor='hand2')
        brand_title.pack(anchor='w')
        brand_subtitle = tk.Label(brand,
            text='BEAUTY  •  CARE  •  RELAX',
            font=('Arial', 8, 'bold'),
            bg=GREEN,
            fg='#D7C9A9',
            cursor='hand2')
        brand_subtitle.pack(anchor='w', pady=(0, 0))
        brand.bind('<Button-1>', lambda _event: self.show_page('home'))
        brand_title.bind('<Button-1>', lambda _event: self.show_page('home'))
        brand_subtitle.bind('<Button-1>', lambda _event: self.show_page('home'))
        right_side = tk.Frame(header, bg=GREEN)
        right_side.pack(side='right', padx=30)
        tk.Label(right_side,
            text='YOUR MOMENT OF BEAUTY',
            font=('Arial', 9, 'bold'),
            bg=GREEN,
            fg='#D8E0D8').pack(side='left',
            padx=(0, 18))
        self.clock_label = tk.Label(right_side, text='', font=('Arial', 10, 'bold'), bg=GREEN, fg='#E8D9B9', padx=0, pady=0)
        self.clock_label.pack(side='left')
        self._start_header_clock()

    def create_shell(self):
        """Create the main content area without the empty left sidebar."""
        shell = tk.Frame(self.root, bg=BG)
        shell.pack(fill='both', expand=True)

        self.page_area = tk.Frame(shell, bg=BG)
        self.page_area.pack(fill='both', expand=True)

        self.page_canvas = tk.Canvas(self.page_area, bg=BG, highlightthickness=0)
        self.page_scrollbar = ttk.Scrollbar(
            self.page_area,
            orient='vertical',
            command=self.page_canvas.yview
        )
        self.page_canvas.configure(yscrollcommand=self.page_scrollbar.set)
        self.page_scrollbar.pack(side='right', fill='y')
        self.page_canvas.pack(side='left', fill='both', expand=True)

        self.page_container = tk.Frame(self.page_canvas, bg=BG, padx=34, pady=28)
        self.page_window = self.page_canvas.create_window(
            (0, 0), window=self.page_container, anchor='nw'
        )
        self.page_container.bind(
            '<Configure>',
            lambda event: self.page_canvas.configure(
                scrollregion=self.page_canvas.bbox('all')
            )
        )
        self.page_canvas.bind(
            '<Configure>',
            lambda event: self.page_canvas.itemconfigure(
                self.page_window, width=event.width
            )
        )
        self.page_canvas.bind_all('<MouseWheel>', self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.page_canvas.yview_scroll(int(-event.delta / 120), 'units')

    def _nav_hover(self, button, hovering):
        """Highlight menu text without drawing a large square behind it."""
        selected = button == self.nav_buttons.get(self.current_page)
        button.configure(fg=GREEN if selected or hovering else TEXT)

    def _set_navigation_state(self):
        for page, button in self.nav_buttons.items():
            selected = page == self.current_page
            button.configure(bg=WHITE, fg=GREEN if selected else TEXT, font=('Arial', 10, 'bold' if selected else 'normal'))

    def _clear_page(self):
        for child in self.page_container.winfo_children():
            child.destroy()

    def show_page(self, page):
        self.current_page = page
        self._set_navigation_state()
        self._clear_page()
        pages = {'home': self.show_home_page,
            'services': self.show_services,
            'calculator': self.show_calculator,
            'planner': self.show_planner,
            'appointments': self.show_appointments,
            'guide': self.show_guide,
            'about': self.show_about}
        pages[page]()
        self.page_canvas.yview_moveto(0)

    def _bind_card_hover(self, card):
        """Cards use a calm static style instead of extra hover effects."""
        return None

    def _page_heading(self, title, subtitle=''):
        top = tk.Frame(self.page_container, bg=BG)
        top.pack(fill='x', pady=(0, 4))
        tk.Label(top, text='URODY  /  BEAUTY STUDIO', font=('Arial', 8, 'bold'),
            bg=BG, fg=GOLD).pack(anchor='w', pady=(0, 6))
        tk.Label(self.page_container, text=title, font=('Georgia', 26, 'bold'),
            bg=BG, fg=GREEN_DARK).pack(anchor='w', pady=(0, 5))
        if subtitle:
            tk.Label(self.page_container, text=subtitle, font=('Arial', 10),
                bg=BG, fg=MUTED).pack(anchor='w', pady=(0, 20))

    def _card(self, parent, padding=18):
        return RoundedPanel(parent, bg_color=WHITE, outer_bg=BG, padding=padding, radius=20)

    def _inline_banner(self, parent, text, error=False):
        tk.Label(parent,
            text=text,
            font=('Arial', 10, 'bold'),
            bg=ERROR_BG if error else SUCCESS_BG,
            fg=ERROR_FG if error else SUCCESS_FG,
            padx=12,
            pady=10,
            anchor='w',
            justify='left',
            wraplength=760).pack(fill='x',
            pady=(0, 14))

    def _action_button(self, parent, label, command):
        return RoundedButton(parent,
            text=label,
            command=command,
            bg_color=GREEN,
            fg_color=WHITE,
            hover_color=GREEN_DARK,
            height=44)

    def _load_image(self, filename, max_width=140, max_height=140):
        """Load a high-quality image and prepare smooth rounded corners."""
        image_path = self.assets_path / filename
        try:
            with Image.open(image_path) as source:
                image = source.convert('RGB')
                image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

                # A little sharpness helps small illustrations look clearer.
                image = ImageEnhance.Sharpness(image).enhance(1.25)
                image = ImageEnhance.Contrast(image).enhance(1.03)
                image = image.convert('RGBA')

                # Draw the corner mask larger, then shrink it for smooth edges.
                scale = 4
                mask = Image.new('L', (image.width * scale, image.height * scale), 0)
                mask_draw = ImageDraw.Draw(mask)
                mask_draw.rounded_rectangle(
                    (0, 0, image.width * scale - 1, image.height * scale - 1),
                    radius=14 * scale,
                    fill=255
                )
                mask = mask.resize(image.size, Image.Resampling.LANCZOS)
                image.putalpha(mask)
                photo = ImageTk.PhotoImage(image)
            return photo
        except (OSError, tk.TclError) as error:
            print(f'Nie można załadować obrazka {image_path}: {error}')
            return None

    def show_home_page(self):
        self._page_heading('Piękno zaczyna się od chwili dla siebie',
            'Witamy w URODY — odkryj zabiegi, zaplanuj wizytę i poczuj się wyjątkowo.')
        if self.flash_message:
            self._inline_banner(self.page_container, self.flash_message)
            self.flash_message = ''
        hero_panel = RoundedPanel(self.page_container, bg_color=GREEN_DARK, outer_bg=BG, padding=25, radius=24)
        hero_panel.pack(fill='x', pady=(0, 25))
        hero = hero_panel.content
        hero_left = tk.Frame(hero, bg=GREEN_DARK)
        hero_left.pack(side='left', fill='both', expand=True)
        hero_caption = tk.Label(hero_left, text='TWÓJ CZAS. TWOJE PIĘKNO.', font=('Arial', 9, 'bold'), bg=GREEN_DARK, fg=GOLD)
        hero_caption.pack(anchor='w', pady=(0, 9))
        tk.Label(hero_left,
            text='Zasługujesz na chwilę\npełną relaksu.',
            font=('Georgia', 21, 'bold'),
            bg=GREEN_DARK,
            fg=WHITE,
            justify='left').pack(anchor='w')
        appointment, storage_error = self._next_appointment()
        if storage_error:
            appointment_text = f'Nie udało się wczytać wizyt: {storage_error}'
        elif appointment is None:
            appointment_text = 'Nie masz jeszcze zaplanowanej wizyty.\nWybierz dogodny termin — zadbamy o resztę.'
        else:
            services = ', '.join((item.get('name', 'Usługa') for item in appointment['services'] if isinstance(item, dict)))
            end_time = appointment['start'] + timedelta(minutes=appointment['data'].get('total_duration', 0))
            appointment_text = f"{appointment['start']:%d.%m.%Y}  ·  {appointment['start']:%H:%M}–{end_time:%H:%M}\n{services}  ·  {appointment['data'].get('total_price', 0)} PLN"
        appointment_panel = RoundedPanel(hero, bg_color='#314A3E', outer_bg=GREEN_DARK, padding=17, radius=18, width=320)
        appointment_panel.pack(side='right', padx=(20, 0), fill='y')
        appointment_box = appointment_panel.content
        tk.Label(appointment_box,
            text='NAJBLIŻSZA WIZYTA',
            font=('Arial', 8, 'bold'),
            bg='#314A3E',
            fg=GOLD).pack(anchor='w',
            pady=(0, 8))
        tk.Label(appointment_box,
            text=appointment_text,
            font=('Arial', 10, 'bold'),
            bg='#314A3E',
            fg=WHITE,
            justify='left',
            wraplength=260).pack(anchor='w',
            pady=(0, 13))
        RoundedButton(appointment_box,
            text='ZAPLANUJ WIZYTĘ  →',
            command=lambda: self.show_page('planner'),
            bg_color=GOLD,
            fg_color=GREEN_DARK,
            hover_color='#D6B982',
            height=40,
            font=('Arial', 9, 'bold')).pack(anchor='w')
        section = tk.Frame(self.page_container, bg=BG)
        section.pack(fill='x', pady=(0, 13))
        tk.Label(section, text='Odkryj URODY', font=('Georgia', 19, 'bold'), bg=BG, fg=GREEN_DARK).pack(side='left')
        tk.Label(section, text='Wybierz coś dla siebie', font=('Arial', 9), bg=BG, fg=MUTED).pack(side='right', pady=(8, 0))
        action_items = (('services', 'manicure.png', 'Katalog usług', 'Zabiegi, ceny i pielęgnacja.'),
            ('calculator', 'calculator.png', 'Kalkulator cen', 'Sprawdź koszt wybranych usług.'),
            ('planner', 'planner.png', 'Planer wizyty', 'Wybierz datę i dogodną godzinę.'),
            ('appointments', 'planner.png', 'Wszystkie wizyty', 'Sprawdź zapisane terminy.'),
            ('guide', 'guide.png', 'Poradnik', 'Poznaj nasze wskazówki beauty.'),
            ('about', 'salon.png', 'O salonie', 'Godziny, adres i kontakt.'))
        actions = tk.Frame(self.page_container, bg=BG)
        actions.pack(fill='x')
        for column in range(3):
            actions.grid_columnconfigure(column, weight=1, uniform='home_cards')
        for index, (page, image_name, title, description) in enumerate(action_items):
            item_panel = RoundedPanel(actions, bg_color=WHITE, outer_bg=BG, padding=15, radius=21)
            item_panel.grid(row=index // 3, column=index % 3, sticky='nsew', padx=6, pady=6)
            item = item_panel.content
            image = self._load_image(image_name, max_width=112, max_height=112)
            if image is not None:
                self.image_refs[page] = image
                tk.Label(item, image=image, bg=WHITE).pack(anchor='w', pady=(0, 10))
            tk.Label(item, text=title, font=('Arial', 11, 'bold'), bg=WHITE, fg=GREEN).pack(anchor='w')
            tk.Label(item,
                text=description,
                font=('Arial', 9),
                bg=WHITE,
                fg=MUTED,
                wraplength=190,
                justify='left').pack(anchor='w',
                pady=(5, 13))
            RoundedButton(item,
                text='Otwórz  →',
                command=lambda selected=page: self.show_page(selected),
                bg_color=SAGE,
                fg_color=GREEN,
                hover_color='#D9E2D8',
                height=36,
                font=('Arial', 9, 'bold')).pack(anchor='w')

    def _next_appointment(self):
        try:
            appointments = load_appointments()
        except (OSError, ValueError) as error:
            return (None, str(error))
        now = datetime.now().replace(second=0, microsecond=0)
        upcoming = []
        for appointment in appointments:
            if not isinstance(appointment, dict):
                continue
            try:
                start = datetime.strptime(f"{appointment['date']} {appointment['time']}", '%d.%m.%Y %H:%M')
            except (KeyError, TypeError, ValueError):
                continue
            if start >= now:
                upcoming.append((start, appointment))
        if not upcoming:
            return (None, None)
        start, appointment = min(upcoming, key=lambda item: item[0])
        return ({'start': start, 'data': appointment, 'services': appointment.get('services', [])}, None)

    def show_services(self):
        self._page_heading('Katalog usług', 'Wybierz swój mały rytuał piękna. Ceny i czas zabiegów znajdziesz na każdej karcie.')
        grid = tk.Frame(self.page_container, bg=BG)
        grid.pack(fill='x')
        for column in range(3):
            grid.grid_columnconfigure(column, weight=1, uniform='service_cards')
        if not SERVICES:
            self._inline_banner(grid, 'Lista usług jest obecnie pusta.')
            return
        symbols = ('✦', '✿', '◇', '❀', '✧', '◈')
        for index, service in enumerate(SERVICES):
            panel = self._card(grid, padding=17)
            panel.grid(row=index // 3, column=index % 3, sticky='nsew', padx=6, pady=6)
            card = panel.content
            top = tk.Frame(card, bg=WHITE)
            top.pack(fill='x', pady=(0, 13))
            tk.Label(top, text=f'{symbols[index % len(symbols)]}  ZABIEG',
                font=('Arial', 8, 'bold'), bg=WHITE, fg=GOLD).pack(side='left')
            tk.Label(top, text=f'{index + 1:02d}', font=('Arial', 9, 'bold'),
                bg=SAGE, fg=GREEN, padx=9, pady=4).pack(side='right')
            tk.Label(card, text=service['name'], font=('Georgia', 15, 'bold'),
                bg=WHITE, fg=GREEN_DARK, wraplength=290, justify='left').pack(anchor='w')
            description = service.get('description', 'Chwila pielęgnacji i relaksu w salonie URODY.')
            tk.Label(card, text=description, font=('Arial', 9), bg=WHITE, fg=MUTED,
                wraplength=290, justify='left').pack(anchor='w', pady=(7, 15))
            details = tk.Frame(card, bg=SAGE, padx=10, pady=8)
            details.pack(fill='x', pady=(0, 13))
            tk.Label(details, text=f"◷  {service['duration']} min", font=('Arial', 9, 'bold'),
                bg=SAGE, fg=GREEN).pack(side='left')
            tk.Label(details, text=f"{service['price']} PLN", font=('Arial', 11, 'bold'),
                bg=SAGE, fg=GREEN_DARK).pack(side='right')
            RoundedButton(card, text='Zaplanuj zabieg  →',
                command=lambda: self.show_page('planner'), bg_color=GREEN,
                fg_color=WHITE, hover_color=GREEN_DARK, height=37,
                font=('Arial', 9, 'bold')).pack(anchor='w')

    def show_appointments(self):
        self._page_heading('Wszystkie wizyty', 'Twoje zaplanowane chwile dla siebie — zapisane lokalnie na tym komputerze.')
        try:
            appointments = load_appointments()
        except (OSError, ValueError) as error:
            self._inline_banner(self.page_container, f'Nie udało się wczytać wizyt: {error}', error=True)
            appointments = []

        def sort_key(item):
            try:
                return datetime.strptime(f"{item.get('date', '')} {item.get('time', '')}", '%d.%m.%Y %H:%M')
            except (TypeError, ValueError):
                return datetime.min
        appointments = sorted((item for item in appointments if isinstance(item, dict)), key=sort_key)
        count_panel = RoundedPanel(self.page_container, bg_color=GREEN_DARK, outer_bg=BG, padding=17, radius=21)
        count_panel.pack(fill='x', pady=(0, 16))
        count = count_panel.content
        tk.Label(count, text='TWOJE REZERWACJE', font=('Arial', 8, 'bold'),
            bg=GREEN_DARK, fg=GOLD).pack(anchor='w')
        row = tk.Frame(count, bg=GREEN_DARK)
        row.pack(fill='x', pady=(4, 0))
        tk.Label(row, text=str(len(appointments)), font=('Georgia', 25, 'bold'),
            bg=GREEN_DARK, fg=WHITE).pack(side='left')
        tk.Label(row, text='zapisanych wizyt', font=('Arial', 10),
            bg=GREEN_DARK, fg='#DCE5DC').pack(side='left', padx=10, pady=(8, 0))
        RoundedButton(row, text='Zaplanuj kolejną  →', command=lambda: self.show_page('planner'),
            bg_color=GOLD, fg_color=GREEN_DARK, hover_color='#D6B982', height=38,
            font=('Arial', 9, 'bold')).pack(side='right')

        if not appointments:
            empty = self._card(self.page_container, padding=24)
            empty.pack(fill='x')
            tk.Label(empty.content, text='Jeszcze nie masz żadnej wizyty',
                font=('Georgia', 17, 'bold'), bg=WHITE, fg=GREEN_DARK).pack(anchor='w')
            tk.Label(empty.content, text='Wybierz zabieg i znajdź termin, który Ci odpowiada.',
                font=('Arial', 10), bg=WHITE, fg=MUTED).pack(anchor='w', pady=(7, 14))
            self._action_button(empty.content, 'Zaplanuj wizytę  →',
                lambda: self.show_page('planner')).pack(anchor='w')
            return

        for index, appointment in enumerate(appointments, start=1):
            panel = self._card(self.page_container, padding=17)
            panel.pack(fill='x', pady=6)
            card = panel.content
            header = tk.Frame(card, bg=WHITE)
            header.pack(fill='x')
            tk.Label(header, text=f'WIZYTA  {index:02d}', font=('Arial', 8, 'bold'),
                bg=WHITE, fg=GOLD).pack(side='left')
            tk.Label(header, text=f"{appointment.get('date', '—')}   ·   {appointment.get('time', '—')}",
                font=('Arial', 10, 'bold'), bg=WHITE, fg=GREEN).pack(side='right')
            services = appointment.get('services', [])
            names = ', '.join(str(item.get('name', 'Usługa')) for item in services if isinstance(item, dict)) or 'Usługi nie określono'
            tk.Label(card, text=names, font=('Georgia', 14, 'bold'), bg=WHITE,
                fg=GREEN_DARK, wraplength=900, justify='left').pack(anchor='w', pady=(10, 13))
            details = tk.Frame(card, bg=SAGE, padx=12, pady=9)
            details.pack(fill='x')
            duration = appointment.get('total_duration', '—')
            price = appointment.get('total_price', '—')
            tk.Label(details, text=f"◷  {duration} min" if duration != '—' else '◷  —',
                font=('Arial', 9, 'bold'), bg=SAGE, fg=GREEN).pack(side='left')
            tk.Label(details, text=f'{price} PLN' if price != '—' else '—',
                font=('Arial', 11, 'bold'), bg=SAGE, fg=GREEN_DARK).pack(side='right')

    def show_calculator(self):
        open_calculator(self.page_container)

    def show_planner(self):
        AppointmentPlanner(self.page_container, on_saved=self._on_appointment_saved)

    def _on_appointment_saved(self, appointment):
        self.flash_message = f"Wizyta zapisana: {appointment['date']} o {appointment['time']}."
        self.show_page('home')

    def show_guide(self):
        self._page_heading('Poradnik pielęgnacyjny', 'Kilka prostych wskazówek, które pomogą Ci zadbać o siebie przed wizytą i po niej.')
        tips = (
            ('01', 'Przed zabiegiem', 'Przyjdź kilka minut wcześniej. Poinformuj kosmetologa o alergiach, wrażliwej skórze i ewentualnych przeciwwskazaniach.'),
            ('02', 'Pielęgnacja skóry', 'Codziennie delikatnie oczyszczaj skórę, stosuj krem nawilżający i pamiętaj o ochronie przeciwsłonecznej SPF.'),
            ('03', 'Dłonie i paznokcie', 'Regularnie nawilżaj dłonie i skórki wokół paznokci. Podczas sprzątania chroń dłonie rękawiczkami.'),
            ('04', 'Pielęgnacja stóp', 'Dbaj o higienę stóp, regularnie je nawilżaj i wybieraj wygodne obuwie.'),
            ('05', 'Po wizycie', 'Stosuj się do zaleceń kosmetologa. Jeśli pojawi się podrażnienie lub niepokojąca reakcja, skontaktuj się ze specjalistą.'),
        )
        grid = tk.Frame(self.page_container, bg=BG)
        grid.pack(fill='x')
        for column in range(2):
            grid.grid_columnconfigure(column, weight=1, uniform='guide_cards')
        for index, (number, title, description) in enumerate(tips):
            panel = self._card(grid, padding=19)
            panel.grid(row=index // 2, column=index % 2, sticky='nsew', padx=6, pady=6)
            card = panel.content
            tk.Label(card, text=number, font=('Georgia', 21, 'bold'),
                bg=WHITE, fg=GOLD).pack(anchor='w')
            tk.Label(card, text=title, font=('Georgia', 14, 'bold'),
                bg=WHITE, fg=GREEN_DARK).pack(anchor='w', pady=(5, 8))
            tk.Label(card, text=description, font=('Arial', 9), bg=WHITE,
                fg=MUTED, wraplength=440, justify='left').pack(anchor='w')

    def show_about(self):
        self._page_heading('O salonie', 'URODY to miejsce, w którym możesz na chwilę zwolnić i zadbać o siebie.')
        hero = RoundedPanel(self.page_container, bg_color=GREEN_DARK, outer_bg=BG, padding=22, radius=23)
        hero.pack(fill='x', pady=(0, 17))
        tk.Label(hero.content, text='YOUR MOMENT OF BEAUTY', font=('Arial', 8, 'bold'),
            bg=GREEN_DARK, fg=GOLD).pack(anchor='w')
        tk.Label(hero.content, text='Piękno, spokój i troska\nw jednym miejscu.',
            font=('Georgia', 21, 'bold'), bg=GREEN_DARK, fg=WHITE,
            justify='left').pack(anchor='w', pady=(7, 0))
        info = (
            ('◷', 'Godziny otwarcia', 'Poniedziałek–piątek\n09:00–18:00'),
            ('⌖', 'Adres', 'ul. Marszałkowska 45\n00-648 Warszawa'),
            ('✉', 'Kontakt', 'Telefon: +48 000 000 000\nE-mail: kontakt@urody-salon.example'),
        )
        grid = tk.Frame(self.page_container, bg=BG)
        grid.pack(fill='x', pady=(0, 17))
        for column in range(3):
            grid.grid_columnconfigure(column, weight=1, uniform='about_cards')
        for index, (symbol, title, description) in enumerate(info):
            panel = self._card(grid, padding=17)
            panel.grid(row=0, column=index, sticky='nsew', padx=6, pady=4)
            card = panel.content
            tk.Label(card, text=symbol, font=('Georgia', 22, 'bold'),
                bg=WHITE, fg=GOLD).pack(anchor='w')
            tk.Label(card, text=title, font=('Arial', 11, 'bold'),
                bg=WHITE, fg=GREEN_DARK).pack(anchor='w', pady=(7, 7))
            tk.Label(card, text=description, font=('Arial', 9), bg=WHITE,
                fg=MUTED, justify='left', wraplength=280).pack(anchor='w')
        tk.Label(self.page_container,
            text='Zapraszamy na manicure, pedicure, zabiegi pielęgnacyjne i stylizację brwi.',
            font=('Arial', 10), bg=BG, fg=MUTED, wraplength=900,
            justify='left').pack(anchor='w', pady=(0, 13))
        self._action_button(self.page_container, 'Zaplanuj wizytę  →',
            lambda: self.show_page('planner')).pack(anchor='w')


def main():
    root = tk.Tk()
    app = UrodyApp(root)

    def close_application():
        if app._clock_id is not None:
            try:
                root.after_cancel(app._clock_id)
            except tk.TclError:
                pass
        root.destroy()
    root.protocol('WM_DELETE_WINDOW', close_application)
    root.mainloop()
if __name__ == '__main__':
    main()
