# app/components/habit_card.py
import flet as ft
from datetime import date
from app.config.theme import get_current_scheme
from app.services.ai_categorization_service import CATEGORY_DEFINITIONS


class HabitCard(ft.Container):
    """Reusable habit card component"""
    
    def __init__(self, habit, app_state, on_toggle=None, on_refresh=None, show_stats=False):
        self.habit = habit
        self.app_state = app_state
        self.on_toggle = on_toggle
        self.on_refresh = on_refresh  # Callback to refresh the list after edit/delete
        self.show_stats = show_stats
        self.scheme = get_current_scheme(app_state)
        
        # Get category info
        category_name = habit.get('category', 'Other') if hasattr(habit, 'get') else (habit['category'] if 'category' in habit.keys() else 'Other')
        self.category_info = CATEGORY_DEFINITIONS.get(category_name, CATEGORY_DEFINITIONS['Other'])
        self.category_name = category_name
        
        # Calculate stats if needed
        if show_stats:
            self.stats = app_state.analytics_service.get_habit_summary(habit['id'])
        
        # Check completion status
        self.is_completed = app_state.habit_service.is_completed(habit['id'], date.today())
        
        # Get streak
        self.streak = self.stats.get('current_streak', 0) if show_stats else 0
        
        # Card styling based on completion
        card_bg = "#ECFDF5" if self.is_completed and not app_state.dark_mode else (
            ft.Colors.with_opacity(0.1, "#10B981") if self.is_completed else self.scheme.surface
        )
        # Use green for completed, theme primary color for not completed
        card_border = "#10B981" if self.is_completed else self.scheme.primary
        
        super().__init__(
            content=self._build_content(),
            bgcolor=card_bg,
            border=ft.border.all(1.5, card_border),
            border_radius=12,
            padding=ft.padding.symmetric(horizontal=15, vertical=12),
        )
    
    def _build_content(self):
        """Build card content with minimalist design"""
        
        # Three-dot menu for edit/delete with minimalist style
        menu_anchor = ft.PopupMenuButton(
            items=[
                ft.PopupMenuItem(
                    content=ft.Row([
                        ft.Icon(ft.Icons.EDIT_OUTLINED, size=18, color=self.scheme.primary),
                        ft.Container(width=8),
                        ft.Text("Edit", size=14, weight=ft.FontWeight.W_500, color=self.scheme.on_surface),
                    ], spacing=0),
                    on_click=lambda _: self._handle_edit(),
                ),
                ft.PopupMenuItem(
                    content=ft.Row([
                        ft.Icon(ft.Icons.DELETE_OUTLINE, size=18, color="#EF4444"),
                        ft.Container(width=8),
                        ft.Text("Delete", size=14, weight=ft.FontWeight.W_500, color="#EF4444"),
                    ], spacing=0),
                    on_click=lambda _: self._handle_delete(),
                ),
            ],
            icon=ft.Icons.MORE_VERT,
            icon_size=20,
            icon_color="#9CA3AF",
            menu_position=ft.PopupMenuPosition.UNDER,
            shape=ft.RoundedRectangleBorder(radius=12),
            bgcolor=self.scheme.surface,
            shadow_color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            elevation=4,
        )
        
        # Build the minimalist card
        return ft.Row(
            controls=[
                # Left side: Habit info
                ft.Column(
                    controls=[
                        # Title row with Done badge
                        ft.Row([
                            ft.Text(
                                self.habit['name'],
                                size=15,
                                weight=ft.FontWeight.W_600,
                                color=self.scheme.on_surface,
                            ),
                            # Done badge (only show if completed)
                            ft.Container(
                                content=ft.Row([
                                    ft.Text("✓", size=11, color="#10B981", weight=ft.FontWeight.BOLD),
                                    ft.Text("Done", size=11, color="#10B981", weight=ft.FontWeight.W_500),
                                ], spacing=2),
                                bgcolor="#D1FAE5" if not self.app_state.dark_mode else ft.Colors.with_opacity(0.2, "#10B981"),
                                border_radius=12,
                                padding=ft.padding.symmetric(horizontal=8, vertical=3),
                                visible=self.is_completed,
                            ),
                        ], spacing=8),
                        # Streak, frequency, and category row
                        ft.Row([
                            # Streak badge
                            ft.Row([
                                ft.Text("🔥", size=11),
                                ft.Text(
                                    f"{self.streak} day streak",
                                    size=11,
                                    color="#F59E0B",
                                ),
                            ], spacing=3),
                            # Frequency badge
                            ft.Container(
                                content=ft.Text(
                                    self.habit['frequency'],
                                    size=10,
                                    color="#6B7280" if not self.app_state.dark_mode else "#9CA3AF",
                                ),
                                bgcolor="#F3F4F6" if not self.app_state.dark_mode else "#374151",
                                border_radius=10,
                                padding=ft.padding.symmetric(horizontal=8, vertical=3),
                            ),
                            # Category badge
                            ft.Container(
                                content=ft.Row([
                                    ft.Text(self.category_info.get('icon', '📌'), size=10),
                                    ft.Text(
                                        self._short_category_name(),
                                        size=10,
                                        color=self.category_info.get('color', '#6B7280'),
                                    ),
                                ], spacing=2, tight=True),
                                bgcolor=ft.Colors.with_opacity(0.15, self.category_info.get('color', '#6B7280')),
                                border_radius=10,
                                padding=ft.padding.symmetric(horizontal=8, vertical=3),
                            ),
                        ], spacing=8),
                    ],
                    spacing=6,
                    expand=True,
                ),
                # Right side: Menu
                menu_anchor if self.show_stats else ft.Container(),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
    
    def _build_right_content(self):
        """Build right side content (checkbox or stats indicator)"""
        if not self.show_stats:
            # Completion checkbox
            return ft.Checkbox(
                value=self.is_completed,
                on_change=self._handle_toggle,
                active_color=self.habit['color'] if 'color' in self.habit.keys() else "#1E1E2E"
            )
        else:
            # Completion rate badge
            rate = self.stats.get('completion_rate', 0)
            return ft.Container(
                content=ft.Text(
                    f"{rate:.0f}%",
                    size=14,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE
                ),
                bgcolor=self._get_rate_color(rate),
                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                border_radius=20
            )
    
    def _build_stats_row(self):
        """Build statistics row"""
        current_streak = self.stats.get('current_streak', 0)
        longest_streak = self.stats.get('longest_streak', 0)
        total = self.stats.get('total_completions', 0)
        
        return ft.Row(
            controls=[
                self._stat_chip("🔥", f"{current_streak} day streak"),
                self._stat_chip("📈", f"{longest_streak} best"),
                self._stat_chip("✓", f"{total} total"),
            ],
            spacing=8
        )
    
    def _stat_chip(self, icon, text):
        """Create a small stat chip"""
        return ft.Container(
            content=ft.Text(
                f"{icon} {text}",
                size=12,
                color="#6B7280"
            ),
            bgcolor="#F3F4F6",
            padding=ft.padding.symmetric(horizontal=8, vertical=4),
            border_radius=6
        )
    
    def _get_rate_color(self, rate):
        """Get color based on completion rate"""
        if rate >= 80:
            return "#10B981"  # Green
        elif rate >= 60:
            return "#F59E0B"  # Orange
        else:
            return "#EF4444"  # Red
    
    def _short_category_name(self):
        """Get shortened category name for display"""
        short_names = {
            "Health & Fitness": "Fitness",
            "Learning & Education": "Learning",
            "Sleep & Rest": "Sleep",
            "Self-Care": "Self-Care",
            "Mindfulness": "Mindful",
            "Productivity": "Productive",
            "Nutrition": "Nutrition",
            "Social": "Social",
            "Finance": "Finance",
            "Creative": "Creative",
            "Other": "Other",
        }
        return short_names.get(self.category_name, self.category_name[:8])
    
    def _handle_toggle(self, e):
        """Handle checkbox toggle"""
        success = self.app_state.toggle_habit_completion(self.habit['id'])
        self.is_completed = not self.is_completed
        
        if self.on_toggle:
            self.on_toggle(self.habit['id'], self.is_completed)
    
    def _handle_click(self, e):
        """Handle card click (for navigation to detail)"""
        # Could navigate to habit detail page
        pass
    
    def _handle_edit(self):
        """Handle edit button click - show edit dialog"""
        page = self.app_state.page
        
        # Get current theme
        scheme = get_current_scheme(self.app_state)
        text_color = scheme.on_surface
        muted_color = "#374151" if not self.app_state.dark_mode else "#9CA3AF"
        border_color = scheme.primary
        
        # Create form fields pre-filled with habit data
        name_field = ft.TextField(
            hint_text="Enter habit name",
            value=self.habit['name'],
            border_radius=12,
            bgcolor=scheme.surface,
            color=text_color,
            border_color=border_color,
            focused_border_color=border_color,
            text_style=ft.TextStyle(color=text_color, size=14),
            hint_style=ft.TextStyle(color=muted_color, size=14),
            cursor_color=border_color,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=14),
        )
        
        # Frequency selector buttons
        current_freq = self.habit.get('frequency', 'Daily') if hasattr(self.habit, 'get') else self.habit['frequency']
        selected_frequency = {"value": current_freq}
        
        def create_freq_btn(label, icon):
            is_selected = selected_frequency["value"] == label
            btn = ft.Container(
                content=ft.Column([
                    ft.Icon(icon, size=18, color=border_color if is_selected else muted_color),
                    ft.Text(label, size=10, color=text_color if is_selected else muted_color, 
                           weight=ft.FontWeight.W_500 if is_selected else ft.FontWeight.NORMAL),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
                bgcolor=ft.Colors.with_opacity(0.1, border_color) if is_selected else "transparent",
                border=ft.border.all(1.5, border_color) if is_selected else ft.border.all(1, ft.Colors.with_opacity(0.3, muted_color)),
                border_radius=12,
                padding=ft.padding.symmetric(horizontal=20, vertical=10),
                expand=True,
                on_click=lambda e, f=label: select_freq(f),
                data=label,
            )
            return btn
        
        daily_btn = create_freq_btn("Daily", ft.Icons.TODAY)
        weekly_btn = create_freq_btn("Weekly", ft.Icons.DATE_RANGE)
        
        freq_row = ft.Row([daily_btn, weekly_btn], spacing=10)
        
        def select_freq(freq):
            selected_frequency["value"] = freq
            # Update button styles
            for btn in [daily_btn, weekly_btn]:
                is_sel = btn.data == freq
                btn.bgcolor = ft.Colors.with_opacity(0.1, border_color) if is_sel else "transparent"
                btn.border = ft.border.all(1.5, border_color) if is_sel else ft.border.all(1, ft.Colors.with_opacity(0.3, muted_color))
                col = btn.content
                if col and col.controls:
                    col.controls[0].color = border_color if is_sel else muted_color
                    col.controls[1].color = text_color if is_sel else muted_color
                    col.controls[1].weight = ft.FontWeight.W_500 if is_sel else ft.FontWeight.NORMAL
            page.update()
        
        error_text = ft.Text(value="", color="#EF4444", size=12, weight=ft.FontWeight.W_500)
        
        def save_changes(e):
            if not name_field.value or not name_field.value.strip():
                error_text.value = "Please enter a habit name"
                page.update()
                return
            
            # Update habit in database using update_habit_fields method
            success = self.app_state.habit_service.update_habit_fields(
                self.habit['id'],
                name=name_field.value.strip(),
                frequency=selected_frequency["value"]
            )
            
            if success:
                page.close(edit_dialog)
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("✓ Habit updated!", color="#FFFFFF"),
                    bgcolor="#10B981",
                )
                page.snack_bar.open = True
                page.update()
                
                # Refresh the list
                if self.on_refresh:
                    self.on_refresh()
            else:
                error_text.value = "Failed to update habit"
                page.update()
        
        def close_dialog(e):
            page.close(edit_dialog)
        
        edit_dialog = ft.AlertDialog(
            modal=True,
            bgcolor=scheme.background,
            shape=ft.RoundedRectangleBorder(radius=20),
            title=ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.EDIT, size=18, color="#FFFFFF"),
                        width=36,
                        height=36,
                        bgcolor=border_color,
                        border_radius=10,
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(width=10),
                    ft.Column([
                        ft.Text("Edit Habit", weight=ft.FontWeight.BOLD, color=text_color, size=18),
                        ft.Text("Update your habit details", size=12, color=muted_color),
                    ], spacing=0, expand=True),
                ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.only(bottom=5),
            ),
            content=ft.Container(
                content=ft.Column([
                    ft.Text("HABIT NAME", size=10, color=muted_color, weight=ft.FontWeight.BOLD),
                    name_field,
                    ft.Container(height=10),
                    ft.Text("FREQUENCY", size=10, color=muted_color, weight=ft.FontWeight.BOLD),
                    freq_row,
                    error_text,
                ], spacing=6, tight=True),
                padding=ft.padding.only(top=5),
            ),
            actions=[
                ft.Container(
                    content=ft.Row([
                        ft.TextButton(
                            content=ft.Text("Cancel", size=13, color=muted_color),
                            on_click=close_dialog,
                        ),
                        ft.Container(width=8),
                        ft.ElevatedButton(
                            content=ft.Row([
                                ft.Icon(ft.Icons.CHECK, size=16, color="#FFFFFF"),
                                ft.Text("Save Changes", size=13, weight=ft.FontWeight.W_600, color="#FFFFFF"),
                            ], spacing=6),
                            on_click=save_changes,
                            bgcolor=border_color,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=12),
                                padding=ft.padding.symmetric(horizontal=20, vertical=12),
                            ),
                        ),
                    ], alignment=ft.MainAxisAlignment.END),
                    padding=ft.padding.only(top=10),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        page.open(edit_dialog)
    
    def _handle_delete(self):
        """Handle delete button click - show confirmation dialog"""
        page = self.app_state.page
        scheme = get_current_scheme(self.app_state)
        text_color = scheme.on_surface
        muted_color = "#374151" if not self.app_state.dark_mode else "#9CA3AF"
        
        def confirm_delete(e):
            # Delete the habit (returns tuple: success, message)
            result = self.app_state.habit_service.delete_habit(self.habit['id'])
            success = result[0] if isinstance(result, tuple) else result
            if success:
                page.close(delete_dialog)
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Habit deleted", color="#FFFFFF"),
                    bgcolor="#EF4444",
                )
                page.snack_bar.open = True
                page.update()
                
                # Refresh the list immediately
                if self.on_refresh:
                    self.on_refresh()
        
        def cancel_delete(e):
            page.close(delete_dialog)
        
        delete_dialog = ft.AlertDialog(
            modal=True,
            bgcolor=scheme.background,
            shape=ft.RoundedRectangleBorder(radius=20),
            title=ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.DELETE_FOREVER, size=20, color="#FFFFFF"),
                        width=40,
                        height=40,
                        bgcolor="#EF4444",
                        border_radius=12,
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(width=12),
                    ft.Column([
                        ft.Text("Delete Habit?", weight=ft.FontWeight.BOLD, color=text_color, size=18),
                        ft.Text("This cannot be undone", size=12, color="#EF4444"),
                    ], spacing=0, expand=True),
                ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.only(bottom=5),
            ),
            content=ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Text("📌", size=16),
                                ft.Text(
                                    self.habit['name'],
                                    size=14,
                                    weight=ft.FontWeight.W_600,
                                    color=text_color,
                                ),
                            ], spacing=8),
                            ft.Container(height=8),
                            ft.Text(
                                "All completion history and statistics for this habit will be permanently deleted.",
                                size=12,
                                color=muted_color,
                            ),
                        ]),
                        bgcolor=ft.Colors.with_opacity(0.1, "#EF4444"),
                        border=ft.border.all(1, ft.Colors.with_opacity(0.3, "#EF4444")),
                        border_radius=12,
                        padding=15,
                    ),
                ], spacing=10, tight=True),
                padding=ft.padding.only(top=5),
            ),
            actions=[
                ft.Container(
                    content=ft.Row([
                        ft.TextButton(
                            content=ft.Text("Cancel", size=13, color=muted_color),
                            on_click=cancel_delete,
                        ),
                        ft.Container(width=8),
                        ft.ElevatedButton(
                            content=ft.Row([
                                ft.Icon(ft.Icons.DELETE, size=16, color="#FFFFFF"),
                                ft.Text("Delete", size=13, weight=ft.FontWeight.W_600, color="#FFFFFF"),
                            ], spacing=6),
                            on_click=confirm_delete,
                            bgcolor="#EF4444",
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=12),
                                padding=ft.padding.symmetric(horizontal=20, vertical=12),
                            ),
                        ),
                    ], alignment=ft.MainAxisAlignment.END),
                    padding=ft.padding.only(top=10),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        page.open(delete_dialog)

