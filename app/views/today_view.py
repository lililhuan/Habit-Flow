# app/views/today_view.py - Today's Habits View
import flet as ft
from datetime import date, timedelta
from app.components.bottom_nav import BottomNav
from app.config.theme import get_current_scheme
from app.services.ai_categorization_service import CATEGORY_DEFINITIONS


class TodayView(ft.View):
    def __init__(self, page: ft.Page, app_state):
        self.page = page
        self.app_state = app_state
        self.selected_date = date.today()
        self.scheme = get_current_scheme(app_state)
        self.border_color = self.scheme.primary  # Use theme primary color for borders
        
        # Register refresh callback with app_state
        app_state.refresh_today_view = self.refresh_view
        
        # Get user display name for greeting
        user = app_state.db.get_user_by_id(app_state.current_user_id)
        display_name = None
        if user and 'display_name' in user.keys():
            display_name = user['display_name']
        
        # Build greeting based on time of day
        from datetime import datetime
        hour = datetime.now().hour
        if hour < 12:
            greeting = "Good morning"
        elif hour < 17:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"
        
        # Personalize greeting if display name exists
        if display_name:
            greeting_text = f"{greeting}, {display_name}!"
        else:
            greeting_text = f"{greeting}!"
        
        # Get habits for today
        self.today_habits = app_state.habit_service.get_habits_for_date(
            app_state.current_user_id,
            self.selected_date
        )
        
        # Calculate completion stats
        self.completed_count = sum(1 for h in self.today_habits if h['completed'])
        self.total_count = len(self.today_habits)
        self.completion_percentage = int((self.completed_count / self.total_count * 100)) if self.total_count > 0 else 0
        
        # Date display
        self.date_text = ft.Text(
            self._format_date(self.selected_date),
            size=16,
            weight=ft.FontWeight.BOLD,
            color=self.scheme.on_background,
        )
        
        # Completion stats
        self.stats_text = ft.Text(
            f"{self.completed_count} of {self.total_count} completed ({self.completion_percentage}%)",
            size=14,
            color="#6B7280",
        )
        
        # Habits list
        self.habits_list = ft.Column(
            controls=self._build_today_habits(),
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
        )
        
        super().__init__(
            route="/today",
            controls=[
                ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    # Header with date navigation
                                    ft.Container(
                                        content=ft.Column(
                                            controls=[
                                                ft.Text(
                                                    greeting_text,
                                                    size=24,
                                                    weight=ft.FontWeight.BOLD,
                                                    color=self.scheme.on_background,
                                                ),
                                                ft.Text(
                                                    "Here's your habits for today",
                                                    size=14,
                                                    color="#6B7280",
                                                ),
                                                ft.Container(height=15),
                                                # Date navigation
                                                ft.Container(
                                                    content=ft.Row(
                                                        controls=[
                                                            ft.IconButton(
                                                                icon=ft.Icons.CHEVRON_LEFT,
                                                                on_click=self.previous_day,
                                                                icon_color=self.scheme.on_background,
                                                            ),
                                                            ft.Container(
                                                                content=self.date_text,
                                                                expand=True,
                                                                alignment=ft.alignment.center,
                                                            ),
                                                            ft.IconButton(
                                                                icon=ft.Icons.CHEVRON_RIGHT,
                                                                on_click=self.next_day,
                                                                icon_color=self.scheme.on_background,
                                                            ),
                                                        ],
                                                        alignment=ft.MainAxisAlignment.CENTER,
                                                    ),
                                                    bgcolor=self.scheme.surface,
                                                    border_radius=12,
                                                    padding=5,
                                                ),
                                                ft.Container(height=10),
                                                # Completion stats
                                                self.stats_text,
                                            ],
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        ),
                                        padding=20,
                                    ),
                                    
                                    # Daily Progress Card
                                    ft.Container(
                                        content=self._build_progress_card(),
                                        padding=ft.padding.symmetric(horizontal=20),
                                    ),
                                    
                                    ft.Container(height=16),
                                    
                                    # Habits list or empty state
                                    ft.Container(
                                        content=self.habits_list if self.today_habits else self._build_empty_state(),
                                        padding=ft.padding.symmetric(horizontal=20),
                                        expand=True,
                                    ),
                                ],
                                spacing=0,
                            ),
                            expand=True,
                            bgcolor=self.scheme.background,
                        ),
                        
                        # Bottom navigation
                        BottomNav(page, app_state, current="today", on_add_click=app_state.open_add_habit_dialog),
                    ],
                    spacing=0,
                    expand=True,
                ),
            ],
            padding=0,
            bgcolor=self.scheme.background,
        )
    
    def _format_date(self, d: date) -> str:
        """Format date for display"""
        if d == date.today():
            return "Today"
        elif d == date.today() - timedelta(days=1):
            return "Yesterday"
        elif d == date.today() + timedelta(days=1):
            return "Tomorrow"
        else:
            return d.strftime("%B %d, %Y")
    
    def _build_progress_card(self):
        """Build the Daily Progress card"""
        # Theme-aware colors
        muted_color = "#9CA3AF" if self.app_state.dark_mode else "#6B7280"
        bg_track_color = "#374151" if self.app_state.dark_mode else "#E5E7EB"
        border_color = self.scheme.primary  # Use theme primary for border
        
        # Use theme primary color for progress bar
        progress_color = self.scheme.primary
        
        # Determine message based on completion
        if self.completion_percentage == 100:
            message = "Perfect day! 🎉"
        elif self.completion_percentage >= 75:
            message = "Almost there! 💪"
        elif self.completion_percentage >= 50:
            message = "Halfway done! 🚀"
        elif self.completion_percentage > 0:
            message = "Keep going! ⭐"
        else:
            message = "Let's get started! 🌟"
            progress_color = bg_track_color  # Match track when 0%
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    # Top row: Title and percentage
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        "Daily Progress",
                                        size=16,
                                        weight=ft.FontWeight.W_600,
                                        color=self.scheme.on_surface,
                                        italic=True,
                                    ),
                                    ft.Text(
                                        message,
                                        size=13,
                                        color=muted_color,
                                    ),
                                ],
                                spacing=2,
                            ),
                            ft.Container(expand=True),
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        f"{self.completion_percentage}%",
                                        size=24,
                                        weight=ft.FontWeight.BOLD,
                                        color=self.scheme.primary if self.completion_percentage > 0 else muted_color,
                                    ),
                                    ft.Text(
                                        "Complete",
                                        size=12,
                                        color=muted_color,
                                    ),
                                ],
                                spacing=0,
                                horizontal_alignment=ft.CrossAxisAlignment.END,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Container(height=12),
                    # Progress bar using ProgressBar component for accurate percentage
                    ft.ProgressBar(
                        value=self.completion_percentage / 100,
                        bgcolor=bg_track_color,
                        color=progress_color,
                        bar_height=8,
                        border_radius=4,
                    ),
                ],
                spacing=0,
            ),
            padding=16,
            border_radius=12,
            bgcolor=self.scheme.surface,
            border=ft.border.all(1, border_color),
        )
    
    def _build_today_habits(self):
        """Build list of today's habits with minimalist design"""
        if not self.today_habits:
            return []
        
        cards = []
        for item in self.today_habits:
            habit = item['habit']
            completed = item['completed']
            
            # Get streak for this habit based on TODAY's actual date (not viewed date)
            # This ensures streaks are "legit" and can't be cheated by viewing future dates
            streak, _ = self.app_state.analytics_service.calculate_streak(habit['id'])
            
            # Colors based on completion - use theme primary for not completed
            card_bg = "#ECFDF5" if completed else self.scheme.surface  # Light green when done
            card_border = "#10B981" if completed else self.border_color  # Green when done, theme primary otherwise
            
            # Build the card
            card = ft.Container(
                content=ft.Row(
                    controls=[
                        # Checkbox (minimal style)
                        ft.Checkbox(
                            value=completed,
                            on_change=lambda e, h=habit: self.toggle_completion(h['id'], e),
                            active_color="#10B981",
                            check_color=ft.Colors.WHITE,
                        ),
                        ft.Container(width=8),
                        # Habit info
                        ft.Column(
                            controls=[
                                ft.Text(
                                    habit['name'],
                                    size=15,
                                    weight=ft.FontWeight.W_600,
                                    color=self.scheme.on_surface,
                                ),
                                ft.Row(
                                    controls=[
                                        # Streak badge
                                        ft.Container(
                                            content=ft.Row([
                                                ft.Text("🔥", size=10),
                                                ft.Text(
                                                    f"{streak}",
                                                    size=10,
                                                    color="#F59E0B",
                                                ),
                                            ], spacing=2, tight=True),
                                        ),
                                        # Frequency badge
                                        ft.Container(
                                            content=ft.Text(
                                                habit['frequency'].lower(),
                                                size=9,
                                                color="#6B7280" if not self.app_state.dark_mode else "#9CA3AF",
                                            ),
                                            bgcolor="#F3F4F6" if not self.app_state.dark_mode else "#374151",
                                            border_radius=8,
                                            padding=ft.padding.symmetric(horizontal=6, vertical=2),
                                        ),
                                        # Category badge
                                        self._build_category_badge(habit),
                                    ],
                                    spacing=6,
                                    wrap=True,
                                ),
                            ],
                            spacing=4,
                            expand=True,
                        ),
                        # Done badge or three-dot menu
                        ft.Container(
                            content=ft.Row([
                                ft.Text("✓", size=12, color="#10B981", weight=ft.FontWeight.BOLD),
                                ft.Text("Done", size=12, color="#10B981", weight=ft.FontWeight.W_500),
                            ], spacing=3) if completed else ft.Container(),
                            bgcolor="#D1FAE5" if completed else ft.Colors.TRANSPARENT,
                            border_radius=15,
                            padding=ft.padding.symmetric(horizontal=10, vertical=5) if completed else 0,
                        ),
                    ],
                    spacing=0,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor=card_bg if not self.app_state.dark_mode else (
                    ft.Colors.with_opacity(0.15, "#10B981") if completed else self.scheme.surface
                ),
                border=ft.border.all(1.5, card_border),
                border_radius=12,
                padding=ft.padding.symmetric(horizontal=12, vertical=14),
                on_click=lambda e, h=habit, c=completed: self._quick_toggle(h['id'], c),
            )
            cards.append(card)
        
        # Add bottom padding to account for navigation bar
        cards.append(ft.Container(height=80))
        
        return cards
    
    def _build_category_badge(self, habit):
        """Build category badge for a habit"""
        category_name = habit['category'] if 'category' in habit.keys() else 'Other'
        category_info = CATEGORY_DEFINITIONS.get(category_name, CATEGORY_DEFINITIONS.get('Other', {'icon': '📌', 'color': '#6B7280'}))
        
        # Shorten category name for display
        short_names = {
            'Health & Fitness': 'Health',
            'Learning & Education': 'Learn',
            'Productivity': 'Prod',
            'Mindfulness': 'Mind',
            'Social': 'Social',
            'Finance': 'Finance',
            'Creativity': 'Create',
            'Nutrition': 'Nutri',
            'Other': 'Other',
        }
        short_name = short_names.get(category_name, category_name[:6])
        
        return ft.Container(
            content=ft.Row([
                ft.Text(category_info.get('icon', '📌'), size=9),
                ft.Text(
                    short_name,
                    size=9,
                    color=category_info.get('color', '#6B7280'),
                ),
            ], spacing=2, tight=True),
            bgcolor=ft.Colors.with_opacity(0.15, category_info.get('color', '#6B7280')),
            border_radius=8,
            padding=ft.padding.symmetric(horizontal=6, vertical=2),
        )
    
    def _quick_toggle(self, habit_id, current_status):
        """Quick toggle when clicking the card"""
        self.app_state.toggle_habit_completion(habit_id, self.selected_date)
        self.refresh_view()
    
    def _build_empty_state(self):
        """Build empty state when no habits for selected date"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(
                        ft.Icons.CALENDAR_TODAY,
                        size=60,
                        color="#D1D5DB",
                    ),
                    ft.Container(height=15),
                    ft.Text(
                        "No habits for this date",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=self.scheme.on_background,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "Add some habits to start tracking your progress",
                        size=14,
                        color="#6B7280",
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            expand=True,
            alignment=ft.alignment.center,
        )
    
    def previous_day(self, e):
        """Navigate to previous day"""
        self.selected_date -= timedelta(days=1)
        self.refresh_view()
    
    def next_day(self, e):
        """Navigate to next day"""
        self.selected_date += timedelta(days=1)
        self.refresh_view()
    
    def toggle_completion(self, habit_id, e):
        """Toggle habit completion"""
        self.app_state.toggle_habit_completion(habit_id, self.selected_date)
        self.refresh_view()
    
    def refresh_view(self):
        """Refresh view with new date data"""
        # Update date display
        self.date_text.value = self._format_date(self.selected_date)
        
        # Get updated habits
        self.today_habits = self.app_state.habit_service.get_habits_for_date(
            self.app_state.current_user_id,
            self.selected_date
        )
        
        # Update stats
        self.completed_count = sum(1 for h in self.today_habits if h['completed'])
        self.total_count = len(self.today_habits)
        self.completion_percentage = int((self.completed_count / self.total_count * 100)) if self.total_count > 0 else 0
        
        self.stats_text.value = f"{self.completed_count} of {self.total_count} completed ({self.completion_percentage}%)"
        
        # Rebuild habits list
        self.habits_list.controls = self._build_today_habits()
        
        # Update progress card and content - new structure with progress card
        # controls[0] is ft.Column wrapper
        # controls[0].controls[0] is ft.Container with main content
        # inner_column has: [0]=header, [1]=progress_card, [2]=spacer, [3]=habits_list
        try:
            main_column = self.controls[0]  # ft.Column
            main_container = main_column.controls[0]  # ft.Container
            inner_column = main_container.content  # ft.Column with header and content
            
            # Update progress card (index 1)
            inner_column.controls[1].content = self._build_progress_card()
            
            # Update habits list container (index 3)
            habits_container = inner_column.controls[3]
            if self.today_habits:
                habits_container.content = self.habits_list
            else:
                habits_container.content = self._build_empty_state()
        except Exception as ex:
            print(f"Error updating Today view: {ex}")
        
        # Use app_state.page to ensure we have a valid page reference
        if self.app_state.page:
            self.app_state.page.update()

