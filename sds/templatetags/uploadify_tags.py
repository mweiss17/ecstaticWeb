from django import template

from teste import settings 

register = template.Library()

@register.inclusion_tag('uploadify/multi_file_upload.html', takes_context=True)

    def multi_file_upload(context, upload_complete_url):
        """
        * filesUploaded - The total number of files uploaded
        * errors - The total number of errors while uploading
        * allBytesLoaded - The total number of bytes uploaded
        * speed - The average speed of all uploaded files
        """
        return {
            'upload_complete_url' : upload_complete_url,
            'uploadify_path' : settings.UPLOADIFY_PATH, # checar essa linha
            'upload_path' : settings.UPLOADIFY_UPLOAD_PATH,
        }    

