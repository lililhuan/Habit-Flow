# app/views/welcome_view.py
import flet as ft
from app.config.theme import get_current_scheme, LIGHT_SCHEMES


def WelcomeView(page, app_state):
    """Landing page with app features and auth buttons"""
    # Use default light scheme for welcome (user not logged in yet)
    scheme = LIGHT_SCHEMES["Default"]
    
    def go_to_signup(e):
        page.go("/signup")
    
    def go_to_signin(e):
        page.go("/signin")
    
    def create_feature_card(icon, icon_color, bg_color, title, description):
        """Create a minimalist feature card"""
        return ft.Container(
            content=ft.Row(
                controls=[
                    # Icon container
                    ft.Container(
                        content=ft.Icon(icon, size=22, color=icon_color),
                        width=48,
                        height=48,
                        bgcolor=bg_color,
                        border_radius=12,
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(width=16),
                    # Text content
                    ft.Column(
                        controls=[
                            ft.Text(
                                title,
                                size=15,
                                weight=ft.FontWeight.W_600,
                                color=scheme.on_background,
                            ),
                            ft.Text(
                                description,
                                size=13,
                                color="#6B7280",
                            ),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                ],
                spacing=0,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=16,
            border_radius=12,
            bgcolor=scheme.surface,
            border=ft.border.all(1, "#E5E7EB"),
        )
    
    return ft.View(
        "/",
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(height=20),
                        
                        # Logo with minimalist design
                        ft.Container(
                            content=ft.Icon(
                                ft.Icons.ALBUM_ROUNDED,
                                size=56,
                                color=scheme.on_primary,
                            ),
                            width=90,
                            height=90,
                            bgcolor=scheme.primary,
                            border_radius=22,
                            alignment=ft.alignment.center,
                            shadow=ft.BoxShadow(
                                spread_radius=0,
                                blur_radius=20,
                                color=ft.Colors.with_opacity(0.2, scheme.primary),
                                offset=ft.Offset(0, 8),
                            ),
                        ),
                        
                        ft.Container(height=24),
                        
                        # App name
                        ft.Text(
                            "HabitFlow",
                            size=32,
                            weight=ft.FontWeight.BOLD,
                            color=scheme.on_background,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        
                        ft.Container(height=4),
                        
                        # Tagline
                        ft.Text(
                            "Track your habits. Stay consistent.",
                            size=15,
                            color="#6B7280",
                            text_align=ft.TextAlign.CENTER,
                        ),
                        
                        ft.Container(height=32),
                        
                        # Features section
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    create_feature_card(
                                        ft.Icons.CALENDAR_TODAY_OUTLINED,
                                        "#F59E0B",
                                        "#FEF3C7",
                                        "Daily Tracking",
                                        "Mark habits as complete each day",
                                    ),
                                    ft.Container(height=12),
                                    create_feature_card(
                                        ft.Icons.TRENDING_UP_ROUNDED,
                                        "#10B981",
                                        "#D1FAE5",
                                        "Streak Building",
                                        "Build momentum with streak tracking",
                                    ),
                                    ft.Container(height=12),
                                    create_feature_card(
                                        ft.Icons.ANALYTICS_OUTLINED,
                                        scheme.primary,
                                        ft.Colors.with_opacity(0.1, scheme.primary),
                                        "Progress Analytics",
                                        "Visualize your growth over time",
                                    ),
                                ],
                                spacing=0,
                            ),
                            padding=ft.padding.symmetric(horizontal=4),
                        ),
                        
                        ft.Container(height=32),
                        
                        # Buttons container
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    # Create Account button
                                    ft.Container(
                                        content=ft.Row(
                                            controls=[
                                                ft.Text(
                                                    "Create Account",
                                                    size=16,
                                                    weight=ft.FontWeight.W_600,
                                                    color=scheme.on_primary,
                                                ),
                                            ],
                                            alignment=ft.MainAxisAlignment.CENTER,
                                        ),
                                        height=52,
                                        bgcolor=scheme.primary,
                                        border_radius=12,
                                        on_click=go_to_signup,
                                        ink=True,
                                    ),
                                    
                                    ft.Container(height=12),
                                    
                                    # Sign In button
                                    ft.Container(
                                        content=ft.Row(
                                            controls=[
                                                ft.Text(
                                                    "Sign In",
                                                    size=16,
                                                    weight=ft.FontWeight.W_600,
                                                    color=scheme.primary,
                                                ),
                                            ],
                                            alignment=ft.MainAxisAlignment.CENTER,
                                        ),
                                        height=52,
                                        bgcolor=scheme.surface,
                                        border_radius=12,
                                        border=ft.border.all(1.5, scheme.primary),
                                        on_click=go_to_signin,
                                        ink=True,
                                    ),
                                ],
                                spacing=0,
                                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                            ),
                            padding=ft.padding.symmetric(horizontal=4),
                        ),
                        
                        ft.Container(height=24),
                        
                        # Footer text
                        ft.Text(
                            "Start building better habits today",
                            size=13,
                            color="#9CA3AF",
                            text_align=ft.TextAlign.CENTER,
                        ),
                        
                        ft.Container(height=20),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0,
                    scroll=ft.ScrollMode.AUTO,
                ),
                padding=ft.padding.symmetric(vertical=20, horizontal=24),
                expand=True,
            )
        ],
        bgcolor=scheme.background,
    )