# campus_life_api.py
import frappe
from frappe import _
from datetime import datetime, timedelta
from frappe.model.document import Document

# Task APIs
@frappe.whitelist()
def create_task(**kwargs):
    """
    Create a new task.
    Required fields:
    - title: Task title
    - description: Task description
    - due_date: Due date
    - priority: Low/Medium/High
    - assigned_to: User ID
    - status: New/In Progress/Completed
    """
    try:
        if not frappe.has_permission("Task", "create"):
            frappe.throw(_("Not permitted to create Task"))

        task = frappe.get_doc({
            "doctype": "Task",
            "status": "New",
            **kwargs
        })
        
        task.insert()
        frappe.db.commit()

        return {
            "message": "Task created successfully",
            "task": task.as_dict()
        }
    except Exception as e:
        frappe.db.rollback()
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

@frappe.whitelist()
def list_tasks(filters=None, fields=None, limit_start=0, limit_page_length=20):
    try:
        if not frappe.has_permission("Task", "read"):
            frappe.throw(_("Not permitted to read Tasks"))

        filters = frappe.parse_json(filters) if filters else {}
        fields = frappe.parse_json(fields) if fields else ["*"]

        tasks = frappe.get_list(
            "Task",
            filters=filters,
            fields=fields,
            start=limit_start,
            page_length=limit_page_length,
            order_by="due_date asc"
        )

        return {
            "tasks": tasks,
            "total": frappe.db.count("Task", filters=filters)
        }
    except Exception as e:
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

# Car APIs
@frappe.whitelist()
def register_car(**kwargs):
    """
    Register a new car.
    Required fields:
    - license_plate: Car license plate
    - make: Car make
    - model: Car model
    - year: Car year
    - owner: User ID
    - parking_permit: Permit number
    """
    try:
        if not frappe.has_permission("Car", "create"):
            frappe.throw(_("Not permitted to register car"))

        car = frappe.get_doc({
            "doctype": "Car",
            **kwargs
        })
        
        car.insert()
        frappe.db.commit()

        return {
            "message": "Car registered successfully",
            "car": car.as_dict()
        }
    except Exception as e:
        frappe.db.rollback()
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

@frappe.whitelist()
def list_cars(filters=None, fields=None, limit_start=0, limit_page_length=20):
    try:
        if not frappe.has_permission("Car", "read"):
            frappe.throw(_("Not permitted to view cars"))

        filters = frappe.parse_json(filters) if filters else {}
        fields = frappe.parse_json(fields) if fields else ["*"]

        cars = frappe.get_list(
            "Car",
            filters=filters,
            fields=fields,
            start=limit_start,
            page_length=limit_page_length
        )

        return {
            "cars": cars,
            "total": frappe.db.count("Car", filters=filters)
        }
    except Exception as e:
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

# Bills APIs
@frappe.whitelist()
def create_bill(**kwargs):
    """
    Create a new bill.
    Required fields:
    - title: Bill title
    - amount: Bill amount
    - due_date: Due date
    - category: Category (Tuition/Housing/Books/Other)
    - status: Unpaid/Paid
    - student: Student ID
    """
    try:
        if not frappe.has_permission("Bill", "create"):
            frappe.throw(_("Not permitted to create bill"))

        bill = frappe.get_doc({
            "doctype": "Bill",
            "status": "Unpaid",
            **kwargs
        })
        
        bill.insert()
        frappe.db.commit()

        return {
            "message": "Bill created successfully",
            "bill": bill.as_dict()
        }
    except Exception as e:
        frappe.db.rollback()
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

@frappe.whitelist()
def mark_bill_as_paid(name):
    try:
        if not frappe.has_permission("Bill", "write"):
            frappe.throw(_("Not permitted to update bill"))

        bill = frappe.get_doc("Bill", name)
        bill.status = "Paid"
        bill.payment_date = datetime.now()
        bill.save()
        frappe.db.commit()

        return {
            "message": "Bill marked as paid",
            "bill": bill.as_dict()
        }
    except Exception as e:
        frappe.db.rollback()
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

# Urgent Case APIs
@frappe.whitelist()
def report_urgent_case(**kwargs):
    """
    Report an urgent case.
    Required fields:
    - type: Emergency type
    - location: Location details
    - description: Situation description
    - reporter: User ID
    - severity: High/Medium/Low
    """
    try:
        if not frappe.has_permission("UrgentCase", "create"):
            frappe.throw(_("Not permitted to report urgent case"))

        case = frappe.get_doc({
            "doctype": "UrgentCase",
            "status": "New",
            "report_time": datetime.now(),
            **kwargs
        })
        
        case.insert()
        frappe.db.commit()

        # Notify relevant personnel
        frappe.enqueue(
            'your_app.utils.notify_emergency_contacts',
            case=case.name,
            emergency_type=case.type
        )

        return {
            "message": "Urgent case reported successfully",
            "case": case.as_dict()
        }
    except Exception as e:
        frappe.db.rollback()
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

@frappe.whitelist()
def update_urgent_case_status(name, status, resolution_notes=None):
    try:
        if not frappe.has_permission("UrgentCase", "write"):
            frappe.throw(_("Not permitted to update urgent case"))

        case = frappe.get_doc("UrgentCase", name)
        case.status = status
        if resolution_notes:
            case.resolution_notes = resolution_notes
        if status == "Resolved":
            case.resolution_time = datetime.now()
        
        case.save()
        frappe.db.commit()

        return {
            "message": "Urgent case updated successfully",
            "case": case.as_dict()
        }
    except Exception as e:
        frappe.db.rollback()
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

# Best Spots APIs
@frappe.whitelist()
def add_best_spot(**kwargs):
    """
    Add a new best spot on campus.
    Required fields:
    - name: Spot name
    - category: Category (Study/Food/Recreation/Parking)
    - location: Location details
    - description: Spot description
    - features: List of features
    - rating: Initial rating
    """
    try:
        if not frappe.has_permission("BestSpot", "create"):
            frappe.throw(_("Not permitted to add best spot"))

        spot = frappe.get_doc({
            "doctype": "BestSpot",
            **kwargs
        })
        
        spot.insert()
        frappe.db.commit()

        return {
            "message": "Best spot added successfully",
            "spot": spot.as_dict()
        }
    except Exception as e:
        frappe.db.rollback()
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

@frappe.whitelist()
def rate_spot(name, rating, review=None):
    try:
        if not frappe.has_permission("BestSpot", "write"):
            frappe.throw(_("Not permitted to rate spot"))

        spot = frappe.get_doc("BestSpot", name)
        
        # Add new rating
        spot.append("ratings", {
            "user": frappe.session.user,
            "rating": rating,
            "review": review,
            "date": datetime.now()
        })
        
        # Update average rating
        total_ratings = len(spot.ratings)
        spot.average_rating = sum(r.rating for r in spot.ratings) / total_ratings
        
        spot.save()
        frappe.db.commit()

        return {
            "message": "Rating added successfully",
            "spot": spot.as_dict()
        }
    except Exception as e:
        frappe.db.rollback()
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

@frappe.whitelist()
def search_spots(category=None, features=None, min_rating=None):
    try:
        if not frappe.has_permission("BestSpot", "read"):
            frappe.throw(_("Not permitted to view spots"))

        filters = {}
        if category:
            filters["category"] = category
        if min_rating:
            filters["average_rating"] = [">=", float(min_rating)]
        
        spots = frappe.get_list(
            "BestSpot",
            filters=filters,
            fields=["*"],
            order_by="average_rating desc"
        )

        if features:
            features = frappe.parse_json(features)
            spots = [
                spot for spot in spots
                if all(feature in spot.features for feature in features)
            ]

        return {
            "spots": spots,
            "total": len(spots)
        }
    except Exception as e:
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}