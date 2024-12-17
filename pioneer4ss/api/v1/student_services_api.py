# student_services_api.py
import frappe
from frappe import _
from datetime import datetime, timedelta
from frappe.model.document import Document

# Event APIs
@frappe.whitelist()
def create_event(**kwargs):
    """
    Create a new event.
    Required fields:
    - title: Event title
    - start_date: Start date and time
    - end_date: End date and time
    - venue: Event venue
    - category: Category (Academic/Cultural/Sports/Other)
    - organizer: Organizing department/club
    - max_participants: Maximum participants (optional)
    """
    try:
        if not frappe.has_permission("Event", "create"):
            frappe.throw(_("Not permitted to create Event"))

        event = frappe.get_doc({
            "doctype": "Event",
            "status": "Upcoming",
            **kwargs
        })
        
        event.insert()
        frappe.db.commit()

        return {
            "message": "Event created successfully",
            "event": event.as_dict()
        }
    except Exception as e:
        frappe.db.rollback()
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

@frappe.whitelist()
def register_for_event(event_name):
    try:
        event = frappe.get_doc("Event", event_name)
        
        # Check if event is full
        if event.max_participants and len(event.participants) >= event.max_participants:
            frappe.throw(_("Event is already full"))
            
        # Check if user is already registered
        if any(p.user == frappe.session.user for p in event.participants):
            frappe.throw(_("Already registered for this event"))
            
        event.append("participants", {
            "user": frappe.session.user,
            "registration_date": datetime.now()
        })
        
        event.save()
        frappe.db.commit()

        return {
            "message": "Successfully registered for event",
            "event": event.as_dict()
        }
    except Exception as e:
        frappe.db.rollback()
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

@frappe.whitelist()
def list_events(filters=None, fields=None, limit_start=0, limit_page_length=20):
    try:
        if not frappe.has_permission("Event", "read"):
            frappe.throw(_("Not permitted to view events"))

        filters = frappe.parse_json(filters) if filters else {}
        fields = frappe.parse_json(fields) if fields else ["*"]

        events = frappe.get_list(
            "Event",
            filters=filters,
            fields=fields,
            start=limit_start,
            page_length=limit_page_length,
            order_by="start_date asc"
        )

        return {
            "events": events,
            "total": frappe.db.count("Event", filters=filters)
        }
    except Exception as e:
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

# Accommodation APIs
@frappe.whitelist()
def create_accommodation_listing(**kwargs):
    """
    Create a new accommodation listing.
    Required fields:
    - name: Property name
    - type: Type (Dormitory/Apartment/House)
    - address: Address
    - rent: Monthly rent
    - available_from: Available date
    - features: List of features
    - description: Property description
    """
    try:
        if not frappe.has_permission("Accommodation", "create"):
            frappe.throw(_("Not permitted to create accommodation listing"))

        accommodation = frappe.get_doc({
            "doctype": "Accommodation",
            "status": "Available",
            **kwargs
        })
        
        accommodation.insert()
        frappe.db.commit()

        return {
            "message": "Accommodation listing created successfully",
            "accommodation": accommodation.as_dict()
        }
    except Exception as e:
        frappe.db.rollback()
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

@frappe.whitelist()
def apply_for_accommodation(accommodation_name, **kwargs):
    """
    Apply for accommodation.
    Required fields:
    - preferred_move_in: Preferred move-in date
    - duration: Intended duration of stay
    - additional_notes: Any additional requirements
    """
    try:
        accommodation = frappe.get_doc("Accommodation", accommodation_name)
        
        if accommodation.status != "Available":
            frappe.throw(_("This accommodation is not available"))
            
        application = frappe.get_doc({
            "doctype": "AccommodationApplication",
            "accommodation": accommodation_name,
            "applicant": frappe.session.user,
            "application_date": datetime.now(),
            "status": "Pending",
            **kwargs
        })
        
        application.insert()
        frappe.db.commit()

        return {
            "message": "Application submitted successfully",
            "application": application.as_dict()
        }
    except Exception as e:
        frappe.db.rollback()
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

@frappe.whitelist()
def search_accommodation(filters=None):
    try:
        if not frappe.has_permission("Accommodation", "read"):
            frappe.throw(_("Not permitted to view accommodations"))

        filters = frappe.parse_json(filters) if filters else {}
        filters["status"] = "Available"

        accommodations = frappe.get_list(
            "Accommodation",
            filters=filters,
            fields=["*"],
            order_by="creation desc"
        )

        return {
            "accommodations": accommodations,
            "total": len(accommodations)
        }
    except Exception as e:
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

# Admission Application APIs
@frappe.whitelist()
def create_admission_application(**kwargs):
    """
    Create a new admission application.
    Required fields:
    - program: Desired program/major
    - term: Term (Fall/Spring/Summer)
    - year: Academic year
    - personal_info: Personal information
    - education_history: Previous education details
    - documents: Required documents
    """
    try:
        if not frappe.has_permission("AdmissionApplication", "create"):
            frappe.throw(_("Not permitted to create admission application"))

        application = frappe.get_doc({
            "doctype": "AdmissionApplication",
            "applicant": frappe.session.user,
            "application_date": datetime.now(),
            "status": "Draft",
            **kwargs
        })
        
        application.insert()
        frappe.db.commit()

        return {
            "message": "Admission application created successfully",
            "application": application.as_dict()
        }
    except Exception as e:
        frappe.db.rollback()
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

@frappe.whitelist()
def update_admission_application(name, **kwargs):
    try:
        application = frappe.get_doc("AdmissionApplication", name)
        
        if application.status not in ["Draft", "Revision Required"]:
            frappe.throw(_("Cannot update application in current status"))
            
        application.update(kwargs)
        application.save()
        frappe.db.commit()

        return {
            "message": "Application updated successfully",
            "application": application.as_dict()
        }
    except Exception as e:
        frappe.db.rollback()
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

@frappe.whitelist()
def submit_admission_application(name):
    try:
        application = frappe.get_doc("AdmissionApplication", name)
        
        if application.status != "Draft":
            frappe.throw(_("Only draft applications can be submitted"))
            
        # Validate required documents
        if not application.validate_required_documents():
            frappe.throw(_("All required documents must be uploaded"))
            
        application.status = "Submitted"
        application.submission_date = datetime.now()
        application.save()
        frappe.db.commit()

        # Notify admissions office
        frappe.enqueue(
            'your_app.utils.notify_admissions_office',
            application=application.name
        )

        return {
            "message": "Application submitted successfully",
            "application": application.as_dict()
        }
    except Exception as e:
        frappe.db.rollback()
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

@frappe.whitelist()
def track_admission_application(name):
    try:
        if not frappe.has_permission("AdmissionApplication", "read"):
            frappe.throw(_("Not permitted to view application"))

        application = frappe.get_doc("AdmissionApplication", name)
        
        return {
            "application": application.as_dict(),
            "timeline": frappe.get_all(
                "AdmissionApplicationActivity",
                filters={"application": name},
                fields=["activity_type", "description", "creation"],
                order_by="creation desc"
            )
        }
    except Exception as e:
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}