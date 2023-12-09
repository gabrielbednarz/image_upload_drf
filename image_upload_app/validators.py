import magic
from django.core.exceptions import ValidationError

# Removed unnecessary imports: os, settings, default_storage, ContentFile, TMP_DIR

SUPPORTED_IMAGE_TYPES = ['image/jpeg', 'image/png']


def validate_image_file_type(upload) -> None:
    try:
        # Modified to use from_buffer instead of saving and reading from a file
        # This method reads the first few bytes to determine the file type, thus more efficient
        file_type = magic.from_buffer(upload.file.read(), mime=True)

        # Reset file pointer after reading the content, to ensure consistent state
        upload.file.seek(0)

        if file_type not in SUPPORTED_IMAGE_TYPES:
            raise ValidationError(
                f'File type {file_type} not supported. Supported types are: {", ".join(SUPPORTED_IMAGE_TYPES)}')
    except Exception as e:
        # Log the exception based on your project needs, here just re-raising it with a custom message
        raise ValidationError(f"Error validating file type: {e}")
    # Removed the finally block, as we are no longer saving a temporary file
