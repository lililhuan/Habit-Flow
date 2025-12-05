# app/views/auth_view.py
import flet as ft
import re
from app.config.theme import LIGHT_SCHEMES, DARK_SCHEMES


def validate_password(password):
    """Validate password requirements"""
    checks = {
        'length': len(password) >= 8,
        'number': bool(re.search(r'\d', password)),
        'uppercase': bool(re.search(r'[A-Z]', password))
    }
    return checks


def SignUpView(page, app_state):
    """Sign Up screen - Minimalist Design"""
    scheme = LIGHT_SCHEMES["Default"]
    
    # Colors
    text_color = "#1F2937"
    muted_color = "#6B7280"
    border_color = scheme.primary
    bg_color = "#F9FAFB"
    surface_color = "#FFFFFF"
    
    # Form fields with minimalist style
    email_field = ft.TextField(
        hint_text="Enter your email",
        keyboard_type=ft.KeyboardType.EMAIL,
        border_radius=12,
        bgcolor=surface_color,
        color=text_color,
        border_color=border_color,
        focused_border_color=border_color,
        text_style=ft.TextStyle(color=text_color, size=14),
        hint_style=ft.TextStyle(color=muted_color, size=14),
        cursor_color=border_color,
        content_padding=ft.padding.symmetric(horizontal=16, vertical=14),
        prefix_icon=ft.Icons.EMAIL_OUTLINED,
    )
    
    password_field = ft.TextField(
        hint_text="Create a password",
        password=True,
        can_reveal_password=True,
        border_radius=12,
        bgcolor=surface_color,
        color=text_color,
        border_color=border_color,
        focused_border_color=border_color,
        text_style=ft.TextStyle(color=text_color, size=14),
        hint_style=ft.TextStyle(color=muted_color, size=14),
        cursor_color=border_color,
        content_padding=ft.padding.symmetric(horizontal=16, vertical=14),
        prefix_icon=ft.Icons.LOCK_OUTLINED,
    )
    
    confirm_password_field = ft.TextField(
        hint_text="Confirm your password",
        password=True,
        can_reveal_password=True,
        border_radius=12,
        bgcolor=surface_color,
        color=text_color,
        border_color=border_color,
        focused_border_color=border_color,
        text_style=ft.TextStyle(color=text_color, size=14),
        hint_style=ft.TextStyle(color=muted_color, size=14),
        cursor_color=border_color,
        content_padding=ft.padding.symmetric(horizontal=16, vertical=14),
        prefix_icon=ft.Icons.LOCK_OUTLINED,
    )
    
    # Password requirement indicators with minimalist design
    def create_check_row(text):
        return ft.Row([
            ft.Icon(ft.Icons.CIRCLE_OUTLINED, size=14, color=muted_color),
            ft.Text(text, size=11, color=muted_color),
        ], spacing=8)
    
    length_check = create_check_row("At least 8 characters")
    number_check = create_check_row("Contains a number")
    uppercase_check = create_check_row("Contains uppercase letter")
    
    error_text = ft.Text("", color="#EF4444", size=12, weight=ft.FontWeight.W_500)
    
    def update_password_checks(e):
        """Update password requirement indicators"""
        checks = validate_password(password_field.value or "")
        
        length_check.controls[0].name = ft.Icons.CHECK_CIRCLE if checks['length'] else ft.Icons.CIRCLE_OUTLINED
        length_check.controls[0].color = "#10B981" if checks['length'] else muted_color
        length_check.controls[1].color = "#10B981" if checks['length'] else muted_color
        
        number_check.controls[0].name = ft.Icons.CHECK_CIRCLE if checks['number'] else ft.Icons.CIRCLE_OUTLINED
        number_check.controls[0].color = "#10B981" if checks['number'] else muted_color
        number_check.controls[1].color = "#10B981" if checks['number'] else muted_color
        
        uppercase_check.controls[0].name = ft.Icons.CHECK_CIRCLE if checks['uppercase'] else ft.Icons.CIRCLE_OUTLINED
        uppercase_check.controls[0].color = "#10B981" if checks['uppercase'] else muted_color
        uppercase_check.controls[1].color = "#10B981" if checks['uppercase'] else muted_color
        
        page.update()
    
    password_field.on_change = update_password_checks
    
    def create_account(e):
        """Handle sign up"""
        error_text.value = ""
        
        if not email_field.value or not password_field.value:
            error_text.value = "Please fill all fields"
            page.update()
            return
        
        if password_field.value != confirm_password_field.value:
            error_text.value = "Passwords do not match"
            page.update()
            return
        
        checks = validate_password(password_field.value)
        if not all(checks.values()):
            error_text.value = "Password does not meet requirements"
            page.update()
            return
        
        success, message = app_state.sign_up(email_field.value, password_field.value)
        
        if success:
            page.go("/habits")
        else:
            error_text.value = message
            page.update()
    
    def go_to_signin(e):
        page.go("/signin")
    
    def go_back(e):
        page.go("/")
    
    return ft.View(
        "/signup",
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[
                        # Back button - minimalist
                        ft.Container(
                            content=ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK_IOS_NEW,
                                    icon_size=18,
                                    icon_color=text_color,
                                    on_click=go_back,
                                ),
                            ]),
                            padding=ft.padding.only(top=10),
                        ),
                        
                        ft.Container(height=20),
                        
                        # Header with icon
                        ft.Container(
                            content=ft.Column([
                                ft.Container(
                                    content=ft.Icon(ft.Icons.PERSON_ADD, size=28, color="#FFFFFF"),
                                    width=56,
                                    height=56,
                                    bgcolor=border_color,
                                    border_radius=14,
                                    alignment=ft.alignment.center,
                                ),
                                ft.Container(height=15),
                                ft.Text(
                                    "Create Account",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=text_color,
                                ),
                                ft.Text(
                                    "Start your habit journey today",
                                    size=13,
                                    color=muted_color,
                                ),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                        ),
                        
                        ft.Container(height=30),
                        
                        # Form container with border
                        ft.Container(
                            content=ft.Column([
                                ft.Text("EMAIL", size=10, color=muted_color, weight=ft.FontWeight.BOLD),
                                email_field,
                                ft.Container(height=12),
                                
                                ft.Text("PASSWORD", size=10, color=muted_color, weight=ft.FontWeight.BOLD),
                                password_field,
                                ft.Container(height=12),
                                
                                ft.Text("CONFIRM PASSWORD", size=10, color=muted_color, weight=ft.FontWeight.BOLD),
                                confirm_password_field,
                                ft.Container(height=15),
                                
                                # Password requirements in a box
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("Password must have:", size=11, weight=ft.FontWeight.W_500, color=text_color),
                                        ft.Container(height=6),
                                        length_check,
                                        number_check,
                                        uppercase_check,
                                    ], spacing=4),
                                    bgcolor=ft.Colors.with_opacity(0.05, border_color),
                                    border=ft.border.all(1, ft.Colors.with_opacity(0.2, border_color)),
                                    border_radius=10,
                                    padding=12,
                                ),
                                
                                ft.Container(height=15),
                                error_text,
                                
                                # Create Account button
                                ft.Container(
                                    content=ft.Row([
                                        ft.Icon(ft.Icons.PERSON_ADD, size=18, color="#FFFFFF"),
                                        ft.Text("Create Account", size=14, weight=ft.FontWeight.W_600, color="#FFFFFF"),
                                    ], spacing=8, alignment=ft.MainAxisAlignment.CENTER),
                                    bgcolor=border_color,
                                    height=48,
                                    border_radius=12,
                                    on_click=create_account,
                                    ink=True,
                                ),
                            ], spacing=4),
                            bgcolor=surface_color,
                            border=ft.border.all(1.5, border_color),
                            border_radius=16,
                            padding=20,
                        ),
                        
                        ft.Container(height=20),
                        
                        # Sign in link
                        ft.Row([
                            ft.Text("Already have an account?", size=13, color=muted_color),
                            ft.TextButton(
                                content=ft.Text("Sign In", size=13, weight=ft.FontWeight.W_600, color=border_color),
                                on_click=go_to_signin,
                            ),
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=0),
                        
                        ft.Container(height=30),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO,
                ),
                padding=20,
                expand=True,
            )
        ],
        bgcolor=bg_color,
        padding=0,
    )


def SignInView(page, app_state):
    """Sign In screen - Minimalist Design"""
    scheme = LIGHT_SCHEMES["Default"]
    
    # Colors
    text_color = "#1F2937"
    muted_color = "#6B7280"
    border_color = scheme.primary
    bg_color = "#F9FAFB"
    surface_color = "#FFFFFF"
    
    # Form fields with minimalist style
    email_field = ft.TextField(
        hint_text="Enter your email",
        keyboard_type=ft.KeyboardType.EMAIL,
        border_radius=12,
        bgcolor=surface_color,
        color=text_color,
        border_color=border_color,
        focused_border_color=border_color,
        text_style=ft.TextStyle(color=text_color, size=14),
        hint_style=ft.TextStyle(color=muted_color, size=14),
        cursor_color=border_color,
        content_padding=ft.padding.symmetric(horizontal=16, vertical=14),
        prefix_icon=ft.Icons.EMAIL_OUTLINED,
    )
    
    password_field = ft.TextField(
        hint_text="Enter your password",
        password=True,
        can_reveal_password=True,
        border_radius=12,
        bgcolor=surface_color,
        color=text_color,
        border_color=border_color,
        focused_border_color=border_color,
        text_style=ft.TextStyle(color=text_color, size=14),
        hint_style=ft.TextStyle(color=muted_color, size=14),
        cursor_color=border_color,
        content_padding=ft.padding.symmetric(horizontal=16, vertical=14),
        prefix_icon=ft.Icons.LOCK_OUTLINED,
    )
    
    error_text = ft.Text("", color="#EF4444", size=12, weight=ft.FontWeight.W_500)
    
    def sign_in(e):
        """Handle sign in"""
        error_text.value = ""
        
        if not email_field.value or not password_field.value:
            error_text.value = "Please fill all fields"
            page.update()
            return
        
        success, message = app_state.sign_in(email_field.value, password_field.value)
        
        if success:
            # Redirect to admin panel if admin, otherwise habits
            if app_state.is_admin():
                page.go("/admin")
            else:
                page.go("/habits")
        else:
            error_text.value = message
            page.update()
    
    def go_to_signup(e):
        page.go("/signup")
    
    def go_back(e):
        page.go("/")
    
    return ft.View(
        "/signin",
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[
                        # Back button - minimalist
                        ft.Container(
                            content=ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK_IOS_NEW,
                                    icon_size=18,
                                    icon_color=text_color,
                                    on_click=go_back,
                                ),
                            ]),
                            padding=ft.padding.only(top=10),
                        ),
                        
                        ft.Container(height=40),
                        
                        # Header with icon
                        ft.Container(
                            content=ft.Column([
                                ft.Container(
                                    content=ft.Icon(ft.Icons.LOGIN, size=28, color="#FFFFFF"),
                                    width=56,
                                    height=56,
                                    bgcolor=border_color,
                                    border_radius=14,
                                    alignment=ft.alignment.center,
                                ),
                                ft.Container(height=15),
                                ft.Text(
                                    "Welcome Back",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=text_color,
                                ),
                                ft.Text(
                                    "Sign in to continue your journey",
                                    size=13,
                                    color=muted_color,
                                ),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                        ),
                        
                        ft.Container(height=40),
                        
                        # Form container with border
                        ft.Container(
                            content=ft.Column([
                                ft.Text("EMAIL", size=10, color=muted_color, weight=ft.FontWeight.BOLD),
                                email_field,
                                ft.Container(height=15),
                                
                                ft.Text("PASSWORD", size=10, color=muted_color, weight=ft.FontWeight.BOLD),
                                password_field,
                                
                                ft.Container(height=20),
                                error_text,
                                
                                # Sign In button
                                ft.Container(
                                    content=ft.Row([
                                        ft.Icon(ft.Icons.LOGIN, size=18, color="#FFFFFF"),
                                        ft.Text("Sign In", size=14, weight=ft.FontWeight.W_600, color="#FFFFFF"),
                                    ], spacing=8, alignment=ft.MainAxisAlignment.CENTER),
                                    bgcolor=border_color,
                                    height=48,
                                    border_radius=12,
                                    on_click=sign_in,
                                    ink=True,
                                ),
                            ], spacing=4),
                            bgcolor=surface_color,
                            border=ft.border.all(1.5, border_color),
                            border_radius=16,
                            padding=20,
                        ),
                        
                        ft.Container(height=25),
                        
                        # Sign up link
                        ft.Row([
                            ft.Text("Don't have an account?", size=13, color=muted_color),
                            ft.TextButton(
                                content=ft.Text("Sign Up", size=13, weight=ft.FontWeight.W_600, color=border_color),
                                on_click=go_to_signup,
                            ),
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=0),
                        
                        ft.Container(height=30),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO,
                ),
                padding=20,
                expand=True,
            )
        ],
        bgcolor=bg_color,
        padding=0,
    )
