# education_api.py
import frappe
from frappe import _
from frappe.model.document import Document

# College APIs
@frappe.whitelist()
def create_college(**kwargs):
    """
    Create a new college record.
    Required fields:
    - name: College name
    - university: Link to University doctype
    - address: College address
    - dean: Dean's name
    """
    try:
        if not frappe.has_permission("College", "create"):
            frappe.throw(_("Not permitted to create College"))

        college = frappe.get_doc({
            "doctype": "College",
            **kwargs
        })
        
        college.insert()
        frappe.db.commit()

        return {
            "message": "College created successfully",
            "college": college.as_dict()
        }
    
    except Exception as e:
        frappe.db.rollback()
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

@frappe.whitelist()
def get_college(name):
    try:
        if not frappe.has_permission("College", "read"):
            frappe.throw(_("Not permitted to read College"))

        college = frappe.get_doc("College", name)
        return {"college": college.as_dict()}

    except frappe.DoesNotExistError:
        frappe.local.response['http_status_code'] = 404
        return {"message": "College not found"}
    except Exception as e:
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

@frappe.whitelist()
def list_colleges(filters=None, fields=None, limit_start=0, limit_page_length=20):
    try:
        if not frappe.has_permission("College", "read"):
            frappe.throw(_("Not permitted to read College"))

        filters = frappe.parse_json(filters) if filters else {}
        fields = frappe.parse_json(fields) if fields else ["*"]

        colleges = frappe.get_list(
            "College",
            filters=filters,
            fields=fields,
            start=limit_start,
            page_length=limit_page_length,
            order_by="creation desc"
        )

        return {
            "colleges": colleges,
            "total": frappe.db.count("College", filters=filters),
            "limit_start": limit_start,
            "limit_page_length": limit_page_length
        }

    except Exception as e:
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

@frappe.whitelist()
def update_college(name, **kwargs):
    try:
        if not frappe.has_permission("College", "write"):
            frappe.throw(_("Not permitted to update College"))

        college = frappe.get_doc("College", name)
        college.update(kwargs)
        college.save()
        frappe.db.commit()

        return {
            "message": "College updated successfully",
            "college": college.as_dict()
        }

    except Exception as e:
        frappe.db.rollback()
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

@frappe.whitelist()
def delete_college(name):
    try:
        if not frappe.has_permission("College", "delete"):
            frappe.throw(_("Not permitted to delete College"))

        frappe.delete_doc("College", name)
        frappe.db.commit()
        return {"message": "College deleted successfully"}

    except Exception as e:
        frappe.db.rollback()
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

# Major APIs
@frappe.whitelist()
def create_major(**kwargs):
    """
    Create a new major.
    Required fields:
    - name: Major name
    - college: Link to College doctype
    - description: Major description
    - duration: Duration in years
    """
    try:
        if not frappe.has_permission("Major", "create"):
            frappe.throw(_("Not permitted to create Major"))

        major = frappe.get_doc({
            "doctype": "Major",
            **kwargs
        })
        
        major.insert()
        frappe.db.commit()

        return {
            "message": "Major created successfully",
            "major": major.as_dict()
        }
    
    except Exception as e:
        frappe.db.rollback()
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

@frappe.whitelist()
def get_major(name):
    try:
        if not frappe.has_permission("Major", "read"):
            frappe.throw(_("Not permitted to read Major"))

        major = frappe.get_doc("Major", name)
        return {"major": major.as_dict()}

    except frappe.DoesNotExistError:
        frappe.local.response['http_status_code'] = 404
        return {"message": "Major not found"}
    except Exception as e:
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

@frappe.whitelist()
def list_majors(filters=None, fields=None, limit_start=0, limit_page_length=20):
    try:
        if not frappe.has_permission("Major", "read"):
            frappe.throw(_("Not permitted to read Major"))

        filters = frappe.parse_json(filters) if filters else {}
        fields = frappe.parse_json(fields) if fields else ["*"]

        majors = frappe.get_list(
            "Major",
            filters=filters,
            fields=fields,
            start=limit_start,
            page_length=limit_page_length,
            order_by="creation desc"
        )

        return {
            "majors": majors,
            "total": frappe.db.count("Major", filters=filters),
            "limit_start": limit_start,
            "limit_page_length": limit_page_length
        }

    except Exception as e:
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

@frappe.whitelist()
def update_major(name, **kwargs):
    try:
        if not frappe.has_permission("Major", "write"):
            frappe.throw(_("Not permitted to update Major"))

        major = frappe.get_doc("Major", name)
        major.update(kwargs)
        major.save()
        frappe.db.commit()

        return {
            "message": "Major updated successfully",
            "major": major.as_dict()
        }

    except Exception as e:
        frappe.db.rollback()
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

@frappe.whitelist()
def delete_major(name):
    try:
        if not frappe.has_permission("Major", "delete"):
            frappe.throw(_("Not permitted to delete Major"))

        frappe.delete_doc("Major", name)
        frappe.db.commit()
        return {"message": "Major deleted successfully"}

    except Exception as e:
        frappe.db.rollback()
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

# Course APIs
@frappe.whitelist()
def create_course(**kwargs):
    """
    Create a new course.
    Required fields:
    - name: Course code/name
    - major: Link to Major doctype
    - title: Course title
    - credits: Number of credits
    - description: Course description
    - prerequisites: List of prerequisite courses (optional)
    """
    try:
        if not frappe.has_permission("Course", "create"):
            frappe.throw(_("Not permitted to create Course"))

        course = frappe.get_doc({
            "doctype": "Course",
            **kwargs
        })
        
        course.insert()
        frappe.db.commit()

        return {
            "message": "Course created successfully",
            "course": course.as_dict()
        }
    
    except Exception as e:
        frappe.db.rollback()
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

@frappe.whitelist()
def get_course(name):
    try:
        if not frappe.has_permission("Course", "read"):
            frappe.throw(_("Not permitted to read Course"))

        course = frappe.get_doc("Course", name)
        return {"course": course.as_dict()}

    except frappe.DoesNotExistError:
        frappe.local.response['http_status_code'] = 404
        return {"message": "Course not found"}
    except Exception as e:
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

@frappe.whitelist()
def list_courses(filters=None, fields=None, limit_start=0, limit_page_length=20):
    try:
        if not frappe.has_permission("Course", "read"):
            frappe.throw(_("Not permitted to read Course"))

        filters = frappe.parse_json(filters) if filters else {}
        fields = frappe.parse_json(fields) if fields else ["*"]

        courses = frappe.get_list(
            "Course",
            filters=filters,
            fields=fields,
            start=limit_start,
            page_length=limit_page_length,
            order_by="creation desc"
        )

        return {
            "courses": courses,
            "total": frappe.db.count("Course", filters=filters),
            "limit_start": limit_start,
            "limit_page_length": limit_page_length
        }

    except Exception as e:
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

@frappe.whitelist()
def update_course(name, **kwargs):
    try:
        if not frappe.has_permission("Course", "write"):
            frappe.throw(_("Not permitted to update Course"))

        course = frappe.get_doc("Course", name)
        course.update(kwargs)
        course.save()
        frappe.db.commit()

        return {
            "message": "Course updated successfully",
            "course": course.as_dict()
        }

    except Exception as e:
        frappe.db.rollback()
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}

@frappe.whitelist()
def delete_course(name):
    try:
        if not frappe.has_permission("Course", "delete"):
            frappe.throw(_("Not permitted to delete Course"))

        frappe.delete_doc("Course", name)
        frappe.db.commit()
        return {"message": "Course deleted successfully"}

    except Exception as e:
        frappe.db.rollback()
        frappe.local.response['http_status_code'] = 400
        return {"message": str(e)}