# university_api.py
import frappe
from frappe import _
from frappe.model.document import Document

@frappe.whitelist()
def create_university(**kwargs):
    """
    Create a new university record.
    Required fields should be passed in kwargs:
    - name: University name
    - address: University address
    - country: Country
    - website: University website (optional)
    - established_year: Year established (optional)
    """
    try:
        # Check if user has permissions
        if not frappe.has_permission("University", "create"):
            frappe.throw(_("Not permitted to create University"), frappe.PermissionError)

        # Create new University doc
        university = frappe.get_doc({
            "doctype": "University",
            **kwargs
        })
        
        university.insert()
        frappe.db.commit()

        return {
            "message": "University created successfully",
            "university": university.as_dict()
        }
    
    except Exception as e:
        frappe.db.rollback()
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

@frappe.whitelist()
def get_university(name):
    """
    Retrieve a specific university by name
    """
    try:
        if not frappe.has_permission("University", "read"):
            frappe.throw(_("Not permitted to read University"), frappe.PermissionError)

        university = frappe.get_doc("University", name)
        return {"university": university.as_dict()}

    except frappe.DoesNotExistError:
        frappe.local.response['http_status_code'] = 404
        return {"message": "University not found"}
    except Exception as e:
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

@frappe.whitelist()
def list_universities(filters=None, fields=None, limit_start=0, limit_page_length=20):
    """
    List all universities with optional filtering and pagination
    """
    try:
        if not frappe.has_permission("University", "read"):
            frappe.throw(_("Not permitted to read University"), frappe.PermissionError)

        filters = frappe.parse_json(filters) if filters else {}
        fields = frappe.parse_json(fields) if fields else ["*"]

        universities = frappe.get_list(
            "University",
            filters=filters,
            fields=fields,
            start=limit_start,
            page_length=limit_page_length,
            order_by="creation desc"
        )

        return {
            "universities": universities,
            "total": frappe.db.count("University", filters=filters),
            "limit_start": limit_start,
            "limit_page_length": limit_page_length
        }

    except Exception as e:
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

@frappe.whitelist()
def update_university(name, **kwargs):
    """
    Update an existing university
    """
    try:
        if not frappe.has_permission("University", "write"):
            frappe.throw(_("Not permitted to update University"), frappe.PermissionError)

        university = frappe.get_doc("University", name)
        university.update(kwargs)
        university.save()
        frappe.db.commit()

        return {
            "message": "University updated successfully",
            "university": university.as_dict()
        }

    except frappe.DoesNotExistError:
        frappe.local.response['http_status_code'] = 404
        return {"message": "University not found"}
    except Exception as e:
        frappe.db.rollback()
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

@frappe.whitelist()
def delete_university(name):
    """
    Delete a university
    """
    try:
        if not frappe.has_permission("University", "delete"):
            frappe.throw(_("Not permitted to delete University"), frappe.PermissionError)

        frappe.delete_doc("University", name)
        frappe.db.commit()

        return {"message": "University deleted successfully"}

    except frappe.DoesNotExistError:
        frappe.local.response['http_status_code'] = 404
        return {"message": "University not found"}
    except Exception as e:
        frappe.db.rollback()
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}