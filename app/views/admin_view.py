# app/views/admin_view.py - Admin Dashboard
import flet as ft
from datetime import date, datetime
from app.config.theme import LIGHT_SCHEMES, DARK_SCHEMES, get_current_scheme
from app.services.security_logger import security_logger


def AdminView(page: ft.Page, app_state):
    """Admin Dashboard - Only accessible by admin users"""
    scheme = get_current_scheme(app_state)
    
    # Colors
    bg_color = scheme.background
    surface_color = scheme.surface
    text_color = scheme.on_surface
    muted_color = "#9CA3AF" if app_state.dark_mode else "#6B7280"
    primary_color = scheme.primary
    
    # Get all users
    all_users = app_state.db.get_all_users() if hasattr(app_state.db, 'get_all_users') else []
    
    # Calculate app-wide stats
    total_users = len(all_users)
    total_habits = 0
    total_completions = 0
    
    for user in all_users:
        habits = app_state.db.get_user_habits(user['id'])
        total_habits += len(habits)
        for habit in habits:
            completions = app_state.db.get_habit_completions(habit['id'])
            total_completions += len(completions)
    
    def sign_out(e):
        app_state.sign_out()
        page.go("/")
    
    def delete_user(user_id, user_email):
        """Delete a user and their data"""
        def confirm_delete(e):
            # Delete user's habits first
            habits = app_state.db.get_user_habits(user_id)
            for habit in habits:
                app_state.habit_service.delete_habit(habit['id'])
            
            # Delete user
            if hasattr(app_state.db, 'delete_user'):
                app_state.db.delete_user(user_id)
            
            page.close(dialog)
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"User {user_email} deleted", color="#FFFFFF"),
                bgcolor="#EF4444",
            )
            page.snack_bar.open = True
            page.go("/admin")  # Refresh
        
        dialog = ft.AlertDialog(
            modal=True,
            bgcolor=surface_color,
            title=None,
            content=ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Icon(ft.Icons.WARNING_ROUNDED, size=32, color="#EF4444"),
                        bgcolor=ft.Colors.with_opacity(0.1, "#EF4444"),
                        border_radius=50,
                        padding=12,
                    ),
                    ft.Container(height=16),
                    ft.Text("Delete User?", size=20, weight=ft.FontWeight.W_600, color=text_color),
                    ft.Container(height=8),
                    ft.Text(
                        f"Delete {user_email} and all their data?",
                        size=13,
                        color=muted_color,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=24),
                    ft.Row([
                        ft.Container(
                            content=ft.Text("Cancel", size=14, color=muted_color),
                            on_click=lambda e: page.close(dialog),
                            padding=ft.padding.symmetric(horizontal=20, vertical=10),
                        ),
                        ft.Container(
                            content=ft.Text("Delete", size=14, weight=ft.FontWeight.W_500, color="#FFFFFF"),
                            bgcolor="#EF4444",
                            border_radius=8,
                            padding=ft.padding.symmetric(horizontal=24, vertical=10),
                            on_click=confirm_delete,
                        ),
                    ], alignment=ft.MainAxisAlignment.END, spacing=8),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                width=280,
                padding=24,
            ),
            actions=[],
            actions_padding=0,
            content_padding=0,
            shape=ft.RoundedRectangleBorder(radius=16),
        )
        
        page.open(dialog)
    
    def view_user_details(user):
        """View user details in a dialog"""
        habits = app_state.db.get_user_habits(user['id'])
        habit_count = len(habits)
        completion_count = sum(len(app_state.db.get_habit_completions(h['id'])) for h in habits)
        
        dialog = ft.AlertDialog(
            modal=True,
            bgcolor=surface_color,
            title=None,
            content=ft.Container(
                content=ft.Column([
                    # User avatar
                    ft.Container(
                        content=ft.Text(
                            user['email'][0].upper(),
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color="#FFFFFF",
                        ),
                        width=60,
                        height=60,
                        bgcolor=primary_color,
                        border_radius=30,
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(height=16),
                    ft.Text(user['email'], size=16, weight=ft.FontWeight.W_600, color=text_color),
                    ft.Container(height=4),
                    ft.Text(f"User ID: {user['id']}", size=12, color=muted_color),
                    ft.Container(height=20),
                    # Stats
                    ft.Row([
                        ft.Column([
                            ft.Text(str(habit_count), size=24, weight=ft.FontWeight.BOLD, color=primary_color),
                            ft.Text("Habits", size=11, color=muted_color),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                        ft.Container(width=40),
                        ft.Column([
                            ft.Text(str(completion_count), size=24, weight=ft.FontWeight.BOLD, color="#10B981"),
                            ft.Text("Completions", size=11, color=muted_color),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Container(height=24),
                    ft.Container(
                        content=ft.Text("Close", size=14, color=muted_color),
                        on_click=lambda e: page.close(dialog),
                        padding=ft.padding.symmetric(horizontal=20, vertical=10),
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                width=280,
                padding=24,
            ),
            actions=[],
            actions_padding=0,
            content_padding=0,
            shape=ft.RoundedRectangleBorder(radius=16),
        )
        
        page.open(dialog)
    
    def toggle_user_status(user_id, user_email, is_currently_disabled):
        """Enable or disable a user account"""
        new_status = not is_currently_disabled
        app_state.db.disable_user(user_id, new_status)
        
        # Log admin action
        action = "disabled" if new_status else "enabled"
        security_logger.log_admin_action(
            app_state.current_user['email'],
            f"user_{action}",
            user_email
        )
        
        status_msg = "disabled" if new_status else "enabled"
        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"User {user_email} {status_msg}", color="#FFFFFF"),
            bgcolor="#10B981" if not new_status else "#F59E0B",
        )
        page.snack_bar.open = True
        
        # Navigate away and back to force refresh
        page.go("/today")
        page.go("/admin")
    
    # Build user list
    user_cards = []
    for user in all_users:
        user_habits = app_state.db.get_user_habits(user['id'])
        is_admin = app_state.is_admin_email(user['email'])
        is_disabled = app_state.db.is_user_disabled(user['id']) if hasattr(app_state.db, 'is_user_disabled') else False
        
        # Get display name
        display_name = user.get('display_name', None) if isinstance(user, dict) else None
        if not display_name and hasattr(user, 'keys'):
            display_name = user['display_name'] if 'display_name' in user.keys() and user['display_name'] else None
        
        # Avatar initial - use display name first letter if available, otherwise email
        avatar_letter = display_name[0].upper() if display_name else user['email'][0].upper()
        
        user_cards.append(
            ft.Container(
                content=ft.Row([
                    # Avatar
                    ft.Container(
                        content=ft.Text(
                            avatar_letter,
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color="#FFFFFF",
                        ),
                        width=40,
                        height=40,
                        bgcolor=("#9CA3AF" if is_disabled else primary_color) if not is_admin else "#F59E0B",
                        border_radius=20,
                        alignment=ft.alignment.center,
                    ),
                    # Info
                    ft.Column([
                        ft.Row([
                            ft.Text(
                                display_name if display_name else user['email'],
                                size=14,
                                weight=ft.FontWeight.W_500,
                                color=muted_color if is_disabled else text_color,
                            ),
                            ft.Container(
                                content=ft.Text("ADMIN", size=9, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                                bgcolor="#F59E0B",
                                border_radius=4,
                                padding=ft.padding.symmetric(horizontal=6, vertical=2),
                                visible=is_admin,
                            ),
                            ft.Container(
                                content=ft.Text("DISABLED", size=9, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                                bgcolor="#9CA3AF",
                                border_radius=4,
                                padding=ft.padding.symmetric(horizontal=6, vertical=2),
                                visible=is_disabled and not is_admin,
                            ),
                        ], spacing=8),
                        ft.Text(
                            f"{user['email']} • {len(user_habits)} habits" if display_name else f"{len(user_habits)} habits",
                            size=12, 
                            color=muted_color
                        ),
                    ], spacing=2, expand=True),
                    # Actions
                    ft.Row([
                        ft.IconButton(
                            ft.Icons.VISIBILITY_OUTLINED,
                            icon_size=18,
                            icon_color=muted_color,
                            on_click=lambda e, u=user: view_user_details(u),
                            tooltip="View details",
                        ),
                        ft.IconButton(
                            ft.Icons.BLOCK if not is_disabled else ft.Icons.CHECK_CIRCLE_OUTLINE,
                            icon_size=18,
                            icon_color="#F59E0B" if not is_disabled else "#10B981",
                            on_click=lambda e, uid=user['id'], uemail=user['email'], dis=is_disabled: toggle_user_status(uid, uemail, dis),
                            tooltip="Disable user" if not is_disabled else "Enable user",
                            visible=not is_admin,  # Hide for admin users (can't disable admins)
                        ),
                        ft.IconButton(
                            ft.Icons.DELETE_OUTLINE,
                            icon_size=18,
                            icon_color="#EF4444" if not is_admin else muted_color,
                            on_click=lambda e, uid=user['id'], uemail=user['email']: delete_user(uid, uemail) if not app_state.is_admin_email(uemail) else None,
                            tooltip="Delete user" if not is_admin else "Cannot delete admin",
                            disabled=is_admin,
                            visible=not is_admin,  # Hide delete button for admin users too
                        ),
                    ], spacing=0),
                ], spacing=12),
                bgcolor=surface_color,
                border_radius=12,
                padding=16,
                margin=ft.margin.only(bottom=8),
            )
        )
    
    # Build security logs list
    def build_security_logs():
        """Build the security logs view"""
        logs = security_logger.get_recent_logs(100)
        log_entries = []
        
        for log in logs:
            # Parse log: timestamp | level | event_type | details
            parts = log.split(' | ')
            if len(parts) >= 3:
                timestamp = parts[0]
                level = parts[1]
                event_info = ' | '.join(parts[2:])
                
                # Color based on level
                level_color = "#10B981" if level == "INFO" else "#F59E0B" if level == "WARNING" else "#EF4444"
                
                # Icon based on event type
                icon = ft.Icons.LOGIN if "LOGIN" in event_info else \
                       ft.Icons.LOGOUT if "LOGOUT" in event_info else \
                       ft.Icons.LOCK if "LOCKED" in event_info else \
                       ft.Icons.ADMIN_PANEL_SETTINGS if "ADMIN" in event_info else \
                       ft.Icons.SECURITY
                
                log_entries.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(icon, size=18, color=level_color),
                            ft.Column([
                                ft.Text(event_info, size=12, color=text_color, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                                ft.Text(timestamp, size=10, color=muted_color),
                            ], spacing=2, expand=True),
                            ft.Container(
                                content=ft.Text(level, size=9, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                                bgcolor=level_color,
                                border_radius=4,
                                padding=ft.padding.symmetric(horizontal=6, vertical=2),
                            ),
                        ], spacing=12),
                        bgcolor=surface_color,
                        border_radius=8,
                        padding=12,
                        margin=ft.margin.only(bottom=6),
                    )
                )
        
        if not log_entries:
            return ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.SECURITY, size=48, color=muted_color),
                    ft.Text("No security logs yet", color=muted_color),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12),
                padding=40,
                alignment=ft.alignment.center,
            )
        
        return ft.Column(
            controls=log_entries,
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
        )
    
    # Build activity/login history list
    def build_activity_logs():
        """Build the login activity view"""
        logins = app_state.db.get_all_recent_logins(50) if hasattr(app_state.db, 'get_all_recent_logins') else []
        activity_entries = []
        
        for login in logins:
            login_time = login['login_time']
            success = login['success']
            email = login['email']
            
            # Format time
            try:
                if isinstance(login_time, str):
                    dt = datetime.fromisoformat(login_time)
                    time_str = dt.strftime("%b %d, %Y %H:%M")
                else:
                    time_str = str(login_time)
            except:
                time_str = str(login_time)
            
            status_color = "#10B981" if success else "#EF4444"
            status_text = "Success" if success else "Failed"
            
            activity_entries.append(
                ft.Container(
                    content=ft.Row([
                        ft.Icon(
                            ft.Icons.CHECK_CIRCLE if success else ft.Icons.CANCEL,
                            size=18,
                            color=status_color
                        ),
                        ft.Column([
                            ft.Text(email, size=13, color=text_color, weight=ft.FontWeight.W_500),
                            ft.Text(time_str, size=11, color=muted_color),
                        ], spacing=2, expand=True),
                        ft.Container(
                            content=ft.Text(status_text, size=10, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                            bgcolor=status_color,
                            border_radius=4,
                            padding=ft.padding.symmetric(horizontal=8, vertical=3),
                        ),
                    ], spacing=12),
                    bgcolor=surface_color,
                    border_radius=8,
                    padding=12,
                    margin=ft.margin.only(bottom=6),
                )
            )
        
        if not activity_entries:
            return ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.HISTORY, size=48, color=muted_color),
                    ft.Text("No login activity yet", color=muted_color),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12),
                padding=40,
                alignment=ft.alignment.center,
            )
        
        return ft.Column(
            controls=activity_entries,
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
        )
    
    # Tab state
    current_tab = {"value": 0}
    
    def switch_tab(index):
        current_tab["value"] = index
        tabs_container.content = build_tab_content(index)
        tab_users.bgcolor = primary_color if index == 0 else ft.Colors.TRANSPARENT
        tab_users.content.color = "#FFFFFF" if index == 0 else muted_color
        tab_activity.bgcolor = primary_color if index == 1 else ft.Colors.TRANSPARENT
        tab_activity.content.color = "#FFFFFF" if index == 1 else muted_color
        tab_logs.bgcolor = primary_color if index == 2 else ft.Colors.TRANSPARENT
        tab_logs.content.color = "#FFFFFF" if index == 2 else muted_color
        page.update()
    
    def build_tab_content(index):
        if index == 0:
            return ft.Column([
                ft.Text("All Users", size=18, weight=ft.FontWeight.W_600, color=text_color),
                ft.Container(height=12),
                ft.Column(
                    controls=user_cards if user_cards else [
                        ft.Text("No users found", color=muted_color),
                    ],
                    spacing=0,
                    scroll=ft.ScrollMode.AUTO,
                ),
            ])
        elif index == 1:
            return ft.Column([
                ft.Row([
                    ft.Text("Login Activity", size=18, weight=ft.FontWeight.W_600, color=text_color),
                    ft.Container(expand=True),
                    ft.IconButton(
                        ft.Icons.REFRESH,
                        icon_size=18,
                        icon_color=muted_color,
                        on_click=lambda e: switch_tab(1),
                        tooltip="Refresh",
                    ),
                ]),
                ft.Container(height=12),
                build_activity_logs(),
            ])
        else:
            return ft.Column([
                ft.Row([
                    ft.Text("Security Audit Log", size=18, weight=ft.FontWeight.W_600, color=text_color),
                    ft.Container(expand=True),
                    ft.IconButton(
                        ft.Icons.REFRESH,
                        icon_size=18,
                        icon_color=muted_color,
                        on_click=lambda e: switch_tab(2),
                        tooltip="Refresh logs",
                    ),
                ]),
                ft.Container(height=12),
                build_security_logs(),
            ])
    
    # Tab buttons
    tab_users = ft.Container(
        content=ft.Text("Users", size=13, weight=ft.FontWeight.W_500, color="#FFFFFF"),
        bgcolor=primary_color,
        border_radius=8,
        padding=ft.padding.symmetric(horizontal=16, vertical=8),
        on_click=lambda e: switch_tab(0),
    )
    
    tab_activity = ft.Container(
        content=ft.Text("Activity", size=13, weight=ft.FontWeight.W_500, color=muted_color),
        bgcolor=ft.Colors.TRANSPARENT,
        border_radius=8,
        padding=ft.padding.symmetric(horizontal=16, vertical=8),
        on_click=lambda e: switch_tab(1),
    )
    
    tab_logs = ft.Container(
        content=ft.Text("Logs", size=13, weight=ft.FontWeight.W_500, color=muted_color),
        bgcolor=ft.Colors.TRANSPARENT,
        border_radius=8,
        padding=ft.padding.symmetric(horizontal=16, vertical=8),
        on_click=lambda e: switch_tab(2),
    )
    
    tabs_container = ft.Container(
        content=build_tab_content(0),
        expand=True,
    )

    return ft.View(
        "/admin",
        controls=[
            ft.Container(
                content=ft.Column([
                    # Header
                    ft.Container(
                        content=ft.Row([
                            ft.Column([
                                ft.Text("Admin Dashboard", size=28, weight=ft.FontWeight.BOLD, color=text_color),
                                ft.Text(f"Logged in as {app_state.current_user['email']}", size=12, color=muted_color),
                            ], spacing=4),
                            ft.IconButton(
                                ft.Icons.LOGOUT,
                                icon_color="#EF4444",
                                on_click=sign_out,
                                tooltip="Sign Out",
                            ),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        padding=20,
                    ),
                    
                    # Stats Cards
                    ft.Container(
                        content=ft.Row([
                            # Total Users
                            ft.Container(
                                content=ft.Column([
                                    ft.Icon(ft.Icons.PEOPLE_OUTLINED, size=24, color=primary_color),
                                    ft.Text(str(total_users), size=28, weight=ft.FontWeight.BOLD, color=text_color),
                                    ft.Text("Users", size=12, color=muted_color),
                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
                                bgcolor=surface_color,
                                border_radius=16,
                                padding=20,
                                expand=True,
                            ),
                            # Total Habits
                            ft.Container(
                                content=ft.Column([
                                    ft.Icon(ft.Icons.FLAG_OUTLINED, size=24, color="#10B981"),
                                    ft.Text(str(total_habits), size=28, weight=ft.FontWeight.BOLD, color=text_color),
                                    ft.Text("Habits", size=12, color=muted_color),
                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
                                bgcolor=surface_color,
                                border_radius=16,
                                padding=20,
                                expand=True,
                            ),
                            # Total Completions
                            ft.Container(
                                content=ft.Column([
                                    ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINED, size=24, color="#8B5CF6"),
                                    ft.Text(str(total_completions), size=28, weight=ft.FontWeight.BOLD, color=text_color),
                                    ft.Text("Done", size=12, color=muted_color),
                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
                                bgcolor=surface_color,
                                border_radius=16,
                                padding=20,
                                expand=True,
                            ),
                        ], spacing=12),
                        padding=ft.padding.symmetric(horizontal=20),
                    ),
                    
                    ft.Container(height=16),
                    
                    # Tab Bar
                    ft.Container(
                        content=ft.Row([
                            tab_users,
                            tab_activity,
                            tab_logs,
                        ], spacing=8),
                        padding=ft.padding.symmetric(horizontal=20),
                    ),
                    
                    ft.Container(height=12),
                    
                    # Tab Content
                    ft.Container(
                        content=tabs_container,
                        padding=ft.padding.symmetric(horizontal=20),
                        expand=True,
                    ),
                ], spacing=0, expand=True),
                bgcolor=bg_color,
                expand=True,
            ),
        ],
        padding=0,
        bgcolor=bg_color,
    )
