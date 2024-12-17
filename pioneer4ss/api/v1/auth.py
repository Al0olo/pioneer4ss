import frappe
import jwt
from datetime import datetime, timedelta
from frappe import _
from frappe.utils import cstr, random_string, validate_email_address
from frappe.auth import LoginManager
from frappe.core.doctype.user.user import test_password_strength
from frappe.utils.password import update_password
from frappe.utils.verified_command import get_signed_params, verify_request

@frappe.whitelist(allow_guest=True)
def login(usr, pwd):
    try:
        login_manager = LoginManager()
        login_manager.authenticate(usr, pwd)
        login_manager.post_login()
        
        # Generate JWT token
        user = frappe.get_doc('User', usr)
        secret_key = frappe.local.conf.get('jwt_secret_key', 'your-secret-key')
        
        token_payload = {
            'user': user.name,
            'exp': datetime.timezone.utc() + timedelta(days=1),
            'iat': datetime.timezone.utc(),
            'roles': [role.role for role in user.roles]
        }
        
        token = jwt.encode(token_payload, secret_key, algorithm='HS256')
        
        return {
            'message': 'Logged in successfully',
            'token': token,
            'user': user.name,
            'roles': [role.role for role in user.roles]
        }
        
    except frappe.AuthenticationError:
        frappe.clear_messages()
        frappe.local.response['message'] = _("Invalid login credentials")
        frappe.local.response['http_status_code'] = 401
        return

@frappe.whitelist(allow_guest=True)
def register(email, full_name, password):
    try:
        # Validate email format
        if not validate_email_address(email):
            frappe.throw(_("Invalid email address"))

        # Check if user already exists
        if frappe.db.exists("User", email):
            frappe.throw(_("Email already registered"))

        # Validate password strength
        test_password_strength(password)

        # Create new user
        user = frappe.get_doc({
            "doctype": "User",
            "email": email,
            "first_name": full_name,
            "send_welcome_email": 0,
            "enabled": 1,
            "new_password": password,
            "user_type": "Website User"
        })
        user.insert(ignore_permissions=True)

        # Add default role
        user.add_roles("Customer")

        # Generate verification key
        verification_key = random_string(32)
        user.verification_key = verification_key
        user.save(ignore_permissions=True)

        # Send verification email
        verification_url = f"{frappe.utils.get_url()}/api/method/your_app.api.verify_email?key={verification_key}"
        
        frappe.sendmail(
            recipients=[email],
            subject="Verify Your Email",
            template="verify_email",
            args={
                "link": verification_url,
                "full_name": full_name
            }
        )

        return {
            "message": "Registration successful. Please check your email to verify your account.",
            "email": email
        }

    except Exception as e:
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

@frappe.whitelist(allow_guest=True)
def verify_email(key):
    user = frappe.db.get_value("User", {"verification_key": key}, "name")
    if not user:
        frappe.throw(_("Invalid or expired verification key"))

    doc = frappe.get_doc("User", user)
    doc.email_verified = 1
    doc.verification_key = None
    doc.save(ignore_permissions=True)

    return {"message": "Email verified successfully"}

@frappe.whitelist(allow_guest=True)
def forgot_password(email):
    try:
        user = frappe.get_doc("User", email)
        if not user or user.enabled == 0:
            frappe.throw(_("User not found or disabled"))

        reset_key = random_string(32)
        user.reset_password_key = reset_key
        user.save(ignore_permissions=True)

        reset_url = f"{frappe.utils.get_url()}/reset-password?key={reset_key}"

        # Send password reset email
        frappe.sendmail(
            recipients=[email],
            subject="Reset Your Password",
            template="reset_password",
            args={
                "link": reset_url,
                "full_name": user.full_name
            }
        )

        return {"message": "Password reset instructions sent to your email"}

    except Exception as e:
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

@frappe.whitelist(allow_guest=True)
def reset_password(key, new_password):
    try:
        user = frappe.db.get_value("User", {"reset_password_key": key}, "name")
        if not user:
            frappe.throw(_("Invalid or expired reset key"))

        # Validate password strength
        test_password_strength(new_password)

        # Update password
        update_password(user, new_password)

        # Clear reset key
        doc = frappe.get_doc("User", user)
        doc.reset_password_key = None
        doc.save(ignore_permissions=True)

        return {"message": "Password updated successfully"}

    except Exception as e:
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

@frappe.whitelist()
def logout():
    try:
        # Get the current user
        user = frappe.session.user
        if user == "Guest":
            frappe.throw(_("Not logged in"))

        # Clear session
        frappe.local.login_manager.logout()
        frappe.db.commit()

        return {"message": "Logged out successfully"}

    except Exception as e:
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

@frappe.whitelist()
def delete_account(password):
    try:
        # Get current user
        user = frappe.session.user
        if user == "Guest":
            frappe.throw(_("Not logged in"))

        # Verify password
        login_manager = LoginManager()
        login_manager.check_password(user, password)

        # Delete user
        user_doc = frappe.get_doc("User", user)
        user_doc.enabled = 0  # First disable the user
        user_doc.save(ignore_permissions=True)
        
        # Optional: You might want to actually delete the user or mark them for deletion
        # frappe.delete_doc("User", user)

        # Clear session
        frappe.local.login_manager.logout()
        frappe.db.commit()

        return {"message": "Account deleted successfully"}

    except Exception as e:
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

def get_token_from_header():
    """Extract JWT token from the Authorization header"""
    auth_header = frappe.get_request_header("Authorization")
    if auth_header and auth_header.startswith('Bearer '):
        return auth_header.split(' ')[1]
    return None

def verify_token():
    """
    Verify JWT token from request header
    Skip verification for web dashboard routes
    """
    try:
        # Skip token verification for web routes
        if frappe.local.request.path.startswith('/app'):
            return
            
        # Get token from header
        token = get_token_from_header()
        if not token:
            return
            
        # Verify token
        secret_key = frappe.local.conf.get('jwt_secret_key', 'your-secret-key')
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        
        # Set session user from token
        frappe.session.user = payload.get('user')
        
        return payload
        
    except jwt.ExpiredSignatureError:
        frappe.throw(_("Token has expired"), frappe.AuthenticationError)
    except jwt.InvalidTokenError:
        frappe.throw(_("Invalid token"), frappe.AuthenticationError)
    except Exception:
        pass  # Allow request to continue for non-API routes