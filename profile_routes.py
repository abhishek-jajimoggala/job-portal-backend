from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import mysql.connector
import os

profile_bp = Blueprint("profile_bp", __name__)
PROFILE_FOLDER = "uploads/profile_images"
RESUME_FOLDER = "uploads/resumes"
os.makedirs(PROFILE_FOLDER, exist_ok=True)
os.makedirs(RESUME_FOLDER, exist_ok=True)
ALLOWED_IMAGES = {"png", "jpg", "jpeg", "webp"}
ALLOWED_RESUMES = {"pdf", "doc", "docx"}

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Abhishek@2004",
    database="jobportaldb"
)
def allowed_file(filename, allowed_extensions):
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in allowed_extensions
    )


# ======================================
# GET PROFILE
# ======================================
@profile_bp.route("/profile/<int:user_id>", methods=["GET"])
def get_profile(user_id):
    try:
        cursor = db.cursor()
        cursor.execute("""
            SELECT
                id,username,email,phone,country,state,city,skills,tenth,intermediate,degree,
                college,branch, passout_year,experience,linkedin,github,profile_image,resume_path
            FROM users WHERE id=%s""", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        if not user:
            return jsonify({"success": False,"message": "User not found"}), 404
        return jsonify({
            "success": True,
            "user": {
                "id": user[0],"username": user[1], "email": user[2], "phone": user[3], "country": user[4],
                "state": user[5],"city": user[6],"skills": user[7],"tenth": user[8],
                "intermediate": user[9],"degree": user[10],"college": user[11],"branch": user[12],
                "passout_year": user[13],"experience": user[14], "linkedin": user[15], "github": user[16],
                "profile_image": user[17],"resume_path": user[18]}})
    except Exception as e:
        return jsonify({"success": False,"message": str(e)}), 500


# ======================================
# UPDATE PROFILE
# ======================================
@profile_bp.route("/profile/<int:user_id>", methods=["PUT"])
def update_profile(user_id):
    try:
        data = request.get_json()
        cursor = db.cursor()
        cursor.execute("""UPDATE users SET
                username=%s,phone=%s,country=%s,state=%s,city=%s,skills=%s,
                tenth=%s,intermediate=%s,degree=%s,college=%s,branch=%s,
                passout_year=%s,experience=%s,linkedin=%s,github=%s WHERE id=%s
        """, (
            data.get("username"),data.get("phone"),data.get("country"),
            data.get("state"),data.get("city"),data.get("skills"),
            data.get("tenth"),data.get("intermediate"),data.get("degree"),
            data.get("college"),data.get("branch"),data.get("passout_year"),
            data.get("experience"),data.get("linkedin"),data.get("github"),user_id
        ))
        db.commit()
        cursor.close()
        return jsonify({"success": True,"message": "Profile Updated Successfully"
        })
    except Exception as e:
        return jsonify({"success": False,"message": str(e)}), 500

# ======================================
# UPLOAD PROFILE IMAGE
# ======================================
@profile_bp.route("/profile/<int:user_id>/image", methods=["POST"])
def upload_profile_image(user_id):
    try:
        # Check image
        if "image" not in request.files:
            return jsonify({
                "success": False,
                "message": "No image uploaded"
            }), 400

        image = request.files["image"]

        if image.filename == "":
            return jsonify({
                "success": False,
                "message": "Please select image"
            }), 400

        # Check extension
        if not allowed_file(image.filename, ALLOWED_IMAGES):
            return jsonify({
                "success": False,
                "message": "Only JPG, PNG, JPEG, WEBP allowed"
            }), 400

        # -----------------------------------------
        # GET OLD IMAGE PATH
        # -----------------------------------------

        cursor = db.cursor()

        cursor.execute(
            "SELECT profile_image FROM users WHERE id=%s",
            (user_id,)
        )

        result = cursor.fetchone()

        old_image_path = result[0] if result else None

        # -----------------------------------------
        # CREATE NEW UNIQUE FILE NAME
        # -----------------------------------------

        import uuid

        extension = image.filename.rsplit(".", 1)[1].lower()

        filename = f"user_{user_id}_{uuid.uuid4().hex}.{extension}"

        image_path = os.path.join(
            PROFILE_FOLDER,
            filename
        ).replace("\\", "/")

        # -----------------------------------------
        # SAVE NEW IMAGE
        # -----------------------------------------

        image.save(image_path)

        # -----------------------------------------
        # UPDATE DATABASE
        # -----------------------------------------

        cursor.execute(
            """
            UPDATE users
            SET profile_image=%s
            WHERE id=%s
            """,
            (image_path, user_id)
        )

        db.commit()

        cursor.close()

        # -----------------------------------------
        # DELETE OLD IMAGE
        # -----------------------------------------

        if old_image_path:

            old_image_path = old_image_path.replace(
                "\\",
                "/"
            )

            if os.path.exists(old_image_path):

                os.remove(old_image_path)

        # -----------------------------------------
        # RESPONSE
        # -----------------------------------------

        return jsonify({
            "success": True,
            "message": "Profile Image Updated Successfully",
            "image_url": image_path
        }), 200

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
# ======================================
# UPLOAD RESUME
# ======================================
@profile_bp.route("/profile/<int:user_id>/resume", methods=["POST"])
def upload_resume(user_id):
    try:
        # =========================
        # CHECK FILE
        # =========================
        if "resume" not in request.files:
            return jsonify({"success": False,"message": "No resume uploaded"
            }), 400

        resume = request.files["resume"]

        if resume.filename == "":
            return jsonify({"success": False,"message": "Please select resume"
            }), 400

        # =========================
        # CHECK FILE TYPE
        # =========================
        if not allowed_file(resume.filename, ALLOWED_RESUMES):
            return jsonify({"success": False,"message": "Only PDF, DOC, DOCX allowed"
            }), 400

        cursor = db.cursor()

        # =========================
        # GET OLD RESUME PATH
        # =========================
        cursor.execute(
            """ SELECT resume_path FROM users WHERE id=%s
            """,
            (user_id,)
        )

        user = cursor.fetchone()

        if not user:
            cursor.close()

            return jsonify({
                "success": False,
                "message": "User Not Found"
            }), 404

        old_resume_path = user[0]

        # =========================
        # DELETE OLD RESUME FILE
        # =========================
        if old_resume_path:

            # Convert Windows \ to /
            old_resume_path = old_resume_path.replace("\\", "/")
            if os.path.exists(old_resume_path):
                try:
                    os.remove(old_resume_path)
                except Exception as e:
                    print("Old resume delete error:", e)

        # =========================
        # NEW RESUME FILENAME
        # =========================
        filename = secure_filename(resume.filename)

        resume_path = os.path.join(
            RESUME_FOLDER,
            filename
        )

        # =========================
        # SAVE NEW RESUME
        # =========================
        resume.save(resume_path)

        # =========================
        # UPDATE DATABASE
        # =========================
        cursor.execute(
            """ UPDATE users SET resume_path=%s WHERE id=%s
            """,
            (resume_path, user_id)
        )

        db.commit()

        cursor.close()

        # =========================
        # SUCCESS RESPONSE
        # =========================
        return jsonify({"success": True,"message": "Resume Uploaded Successfully",
            "resume_url": resume_path
        }), 200

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
