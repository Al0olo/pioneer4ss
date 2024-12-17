# swagger.py
import frappe
import os
import json
import yaml

@frappe.whitelist(allow_guest=True)
def docs():
    """Serve Swagger UI for API documentation"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        swagger_file = os.path.join(current_dir, 'swagger_docs.yaml')
        
        with open(swagger_file, 'r') as f:
            swagger_doc = yaml.safe_load(f)
        
        # Update server URL for local development
        if frappe.local.site:
            for server in swagger_doc['servers']:
                server['url'] = f'http://localhost:8000{server["url"]}'
        
        context = {
            'swagger_doc': json.dumps(swagger_doc)
        }
        
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>API Documentation</title>
            <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.15.5/swagger-ui.min.css">
            <style>
                body {
                    margin: 0;
                    padding: 0;
                }
                #swagger-ui {
                    max-width: 1460px;
                    margin: 0 auto;
                    padding: 20px;
                }
            </style>
        </head>
        <body>
            <div id="swagger-ui"></div>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.15.5/swagger-ui-bundle.min.js"></script>
            <script>
                window.onload = function() {
                    SwaggerUIBundle({
                        spec: %s,
                        dom_id: '#swagger-ui',
                        deepLinking: true,
                        presets: [
                            SwaggerUIBundle.presets.apis,
                            SwaggerUIBundle.SwaggerUIStandalonePreset
                        ],
                    })
                }
            </script>
        </body>
        </html>
        """ % context['swagger_doc']
        
        frappe.local.response.update({
            "type": "page",
            "http_status_code": "200",
            "body": html_content,
            "route": "api/docs"
        })
        
    except Exception as e:
        frappe.log_error(f"Swagger UI Error: {str(e)}")
        raise e