
def save_images(files, upload_folder, db_insert_function):
    """
    دالة عامة لرفع صورة أو عدة صور وإرجاع المفتاح الرئيسي لكل سجل.

    Args:
        files (list): قائمة بملفات الصور.
        upload_folder (str): مسار المجلد الذي سيتم حفظ الصور فيه.
        db_insert_function (function): دالة لإضافة البيانات إلى قاعدة البيانات.

    Returns:
        dict: يحتوي على قائمة الصور التي تم رفعها مع المفاتيح الرئيسية أو الأخطاء.
    """
    # التأكد من أن المجلد موجود
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # السماح بامتدادات معينة فقط
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

    uploaded_files = []
    errors = []

    for file in files:
        if file and allowed_file(file.filename):
            filename = file.filename
            filepath = os.path.join(upload_folder, filename)

            try:
                # حفظ الملف في المجلد
                file.save(filepath)

                # تجهيز البيانات للإدخال في قاعدة البيانات
                data = {
                    'img_name': filename,
                    'img_path': filepath
                }

                # استدعاء دالة الإدخال والحصول على المفتاح الرئيسي
                record_id = db_insert_function('images', data)

                if record_id is not None:
                    uploaded_files.append({
                        'img_name': filename,
                        'img_path': filepath,
                        'img_id': record_id
                    })
                else:
                    errors.append(f"Failed to save {filename} in database.")
            except Exception as e:
                errors.append(f"Failed to upload {filename}: {str(e)}")
        else:
            errors.append(f"Invalid file: {file.filename if file else 'Unknown'}")

    return {
        "uploaded_files": uploaded_files,
        "errors": errors
    }
