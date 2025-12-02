"""
Theme color definitions using colors from dependencies/dependencies.py

Themes:
- Light: Monochromatic Minimalism - Clean grays and whites
- Dark: Reverse of Monochromatic Minimalism - Dark grays and blacks
- Warm Tones: Warm beige, coral, and golden accents
"""
from dependencies.dependencies import colors

THEMES = {
    "Light": {
        # Monochromatic Minimalism - Light theme
        "bg": colors['pure white (Neon Highlights Text)'],  # Pure white background
        "fg": colors['charcoal black (Monochromatic Background)'],  # Charcoal black text
        "secondary_bg": "#F5F5F5",  # Very light gray
        "accent": colors['soft gray (Monochromatic Accent)'],  # Soft gray accent
        "accent_hover": "#666666",  # Darker gray on hover
        "border": "#E0E0E0",  # Light gray borders
        "text_secondary": colors['medium gray (Monochromatic Secondary Text)'],  # Medium gray secondary text
        "listbox_bg": colors['pure white (Neon Highlights Text)'],  # White listbox
        "listbox_fg": colors['charcoal black (Monochromatic Background)'],  # Charcoal text
        "listbox_select": colors['soft gray (Monochromatic Accent)'],  # Soft gray selection
        "button_bg": colors['soft gray (Monochromatic Accent)'],  # Soft gray buttons
        "button_fg": colors['pure white (Neon Highlights Text)'],  # White button text
        "text_bg": colors['pure white (Neon Highlights Text)'],  # White text areas
        "text_fg": colors['charcoal black (Monochromatic Background)'],  # Charcoal text
    },
    "Dark": {
        # Reverse of Monochromatic Minimalism - Dark theme
        "bg": colors['charcoal black (Monochromatic Background)'],  # Charcoal black background
        "fg": colors['light gray (Monochromatic Text)'],  # Light gray text
        "secondary_bg": "#1E1E1E",  # Slightly lighter than bg
        "accent": colors['soft gray (Monochromatic Accent)'],  # Soft gray accent
        "accent_hover": "#AAAAAA",  # Lighter gray on hover
        "border": colors['dark gray (Monochromatic Borders/Dividers)'],  # Dark gray borders
        "text_secondary": colors['medium gray (Monochromatic Secondary Text)'],  # Medium gray secondary text
        "listbox_bg": "#1E1E1E",  # Dark gray listbox
        "listbox_fg": colors['light gray (Monochromatic Text)'],  # Light gray text
        "listbox_select": colors['soft gray (Monochromatic Accent)'],  # Soft gray selection
        "button_bg": colors['soft gray (Monochromatic Accent)'],  # Soft gray buttons
        "button_fg": colors['charcoal black (Monochromatic Background)'],  # Dark button text
        "text_bg": "#1E1E1E",  # Dark text areas
        "text_fg": colors['light gray (Monochromatic Text)'],  # Light gray text
    },
    "Warm Tones": {
        # Warm Tones - Beige, coral, and golden accents
        "bg": colors['soft black (Warm Tones Background)'],  # Soft black background
        "fg": colors['warm beige (Warm Tones Text)'],  # Warm beige text
        "secondary_bg": "#2A2A2A",  # Slightly lighter background
        "accent": colors['muted coral (Warm Tones Accent 1)'],  # Muted coral accent
        "accent_hover": colors['burnt orange (Warm Tones Hover Effects)'],  # Burnt orange on hover
        "border": "#3A3A3A",  # Dark warm border
        "text_secondary": colors['golden yellow (Warm Tones Accent 2)'],  # Golden yellow secondary text
        "listbox_bg": "#2A2A2A",  # Dark warm listbox
        "listbox_fg": colors['warm beige (Warm Tones Text)'],  # Warm beige text
        "listbox_select": colors['muted coral (Warm Tones Accent 1)'],  # Muted coral selection
        "button_bg": colors['muted coral (Warm Tones Accent 1)'],  # Muted coral buttons
        "button_fg": colors['soft black (Warm Tones Background)'],  # Dark button text
        "text_bg": "#2A2A2A",  # Dark warm text areas
        "text_fg": colors['warm beige (Warm Tones Text)'],  # Warm beige text
    },
}

