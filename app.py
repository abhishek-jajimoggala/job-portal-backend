from flask import Flask, request, jsonify, send_file, send_from_directory, session
from flask_cors import CORS
from email_templates import (new_job_email,updated_job_email,shortlisted_email,rejected_email)
from flask_bcrypt import Bcrypt
from email_templates import otp_email_template
from profile_routes import profile_bp
from datetime import datetime, timedelta
import mysql.connector
from otp import genotp
from cmail import send_mail
import io
import os
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.secret_key = "jobportal_secret_key"
CORS(app,supports_credentials=True,origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ]
)
bcrypt = Bcrypt(app)
UPLOAD_FOLDER = "uploads/profile_images"
RESUME_FOLDER = "uploads/resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESUME_FOLDER, exist_ok=True)
mydb = mysql.connector.connect(host="localhost",user="root",password="Abhishek@2004",database="jobportaldb")
app.register_blueprint(profile_bp,url_prefix="/api")
@app.route('/')
def home():
    return jsonify({"status": "success","message": "Welcome Job Portal Application"})

@app.route('/api/register', methods=['POST'])
def register():
    cursor = None
    try:
        data = request.get_json()
        username = data.get('name')
        useremail = data.get('email')
        userpassword = data.get('password')
        confirmpassword = data.get('confirmPassword')
        if userpassword != confirmpassword:
            return jsonify({"status": "failed","message": "Passwords Do Not Match"}), 400
        hash_password = bcrypt.generate_password_hash(userpassword).decode('utf-8')
        otp = genotp()
        otp_expiry_time = (datetime.now() +timedelta(minutes=5))
        mydb.ping(reconnect=True)
        cursor = mydb.cursor(buffered=True)
        cursor.execute('select email from users where email=%s',[useremail])
        user = cursor.fetchone()
        if user:
            return jsonify({"status": "failed","message": "User Already Exists"}), 400
        cursor.execute('''insert into users(username, email, password, otp, otp_expiry_time, account_status)values
            (%s,%s,%s,%s,%s,%s)''',
            [username,useremail,hash_password,otp,otp_expiry_time,'inactive' ])
        mydb.commit()
        subject = "Job Portal Verification OTP"

        html_body = otp_email_template(username,otp)

        send_mail(to=useremail,subject=subject,body=f"Your OTP is {otp}",html_body=html_body)
        return jsonify({"status": "success","message": "OTP Sent Successfully"}), 200
    except Exception as e:
        if mydb.is_connected():
            mydb.rollback()
        return jsonify({"status": "failed","message": str(e)}), 500
    finally:
        if cursor:
            cursor.close()

@app.route('/api/verify-otp', methods=['POST'])
def verifyotp():
    cursor = None
    try:
        data = request.get_json()
        email = data.get('email')
        otp = str(data.get('otp'))
        mydb.ping(reconnect=True)
        cursor = mydb.cursor(buffered=True)
        cursor.execute("SELECT otp, otp_expiry_time, account_status FROM users WHERE email=%s",[email])
        user = cursor.fetchone()
        if not user:
            return jsonify({"status": "failed","message": "User Not Found"}), 400
        # Already verified
        if user[2] == "active":
            return jsonify({"status": "failed","message": "Account Already Verified"}), 400
        # OTP not available
        if user[0] is None or user[1] is None:
            return jsonify({"status": "failed","message": "OTP Not Available"}), 400
        # OTP Expiry Check
        if datetime.now() > user[1]:
            return jsonify({ "status": "failed", "message": "OTP Expired"}), 400
        # OTP Match Check
        if str(user[0]) != otp:
            return jsonify({"status": "failed","message": "Invalid OTP"}), 400
        cursor.execute(
            """ UPDATE users SET otp=NULL, otp_expiry_time=NULL,account_status='active'WHERE email=%s""",[email])
        mydb.commit()
        return jsonify({"status": "success","message": "OTP Verified Successfully"}), 200
    except Exception as e:
        if mydb.is_connected():
            mydb.rollback()
        return jsonify({"status": "failed","message": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
            
@app.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    cursor = None
    try:
        data = request.get_json()
        email = data.get('email')
        mydb.ping(reconnect=True)
        cursor = mydb.cursor(buffered=True)
        cursor.execute("SELECT email FROM users WHERE email=%s",[email])
        user = cursor.fetchone()
        if not user:
            return jsonify({"status": "failed","message": "User Not Found"}), 400
        otp = genotp()
        otp_expiry_time = (datetime.now() +timedelta(minutes=5))
        cursor.execute(
            """ UPDATE users SET otp=%s, otp_expiry_time=%s WHERE email=%s """,[otp, otp_expiry_time, email])
        mydb.commit()
        subject = "Password Reset OTP"

        html_body = otp_email_template("User",otp)

        send_mail(to=email,subject=subject,body=f"Your Password Reset OTP is {otp}",html_body=html_body)
        return jsonify({"status": "success","message": "OTP Sent Successfully"}), 200
    except Exception as e:
        if mydb.is_connected():
            mydb.rollback()
        return jsonify({"status": "failed","message": str(e)}), 500
    finally:
        if cursor:
            cursor.close()

@app.route('/api/reset-password', methods=['POST'])
def reset_password():
    cursor = None
    try:
        data = request.get_json()
        email = data.get('email')
        otp = str(data.get('otp'))
        newpassword = data.get('newPassword')
        confirmpassword = data.get('confirmPassword')
        if newpassword != confirmpassword:
            return jsonify({"status": "failed","message": "Passwords Do Not Match"}), 400
        mydb.ping(reconnect=True)
        cursor = mydb.cursor(buffered=True)
        cursor.execute("SELECT otp, otp_expiry_time FROM users WHERE email=%s",[email])
        user = cursor.fetchone()
        if not newpassword:
            return jsonify({"status": "failed","message": "Password Required"}), 400
        if not user:
            return jsonify({"status": "failed","message": "User Not Found" }), 400
        if len(newpassword) < 6:
            return jsonify({"status": "failed","message": "Password must be at least 6 characters"}), 400
        # OTP not generated
        if user[0] is None or user[1] is None:
            return jsonify({"status": "failed","message": "Please Generate OTP First"}), 400
        # OTP expired
        if datetime.now() > user[1]:
            return jsonify({ "status": "failed", "message": "OTP Expired"}), 400

        # OTP mismatch
        if str(user[0]) != otp:
            return jsonify({"status": "failed", "message": "Invalid OTP"}), 400
        hash_password = bcrypt.generate_password_hash(newpassword).decode('utf-8')
        cursor.execute("""UPDATE users SET password=%s,otp=NULL, otp_expiry_time=NULL WHERE email=%s """,[hash_password, email])
        mydb.commit()
        return jsonify({"status": "success","message": "Password Reset Successful"}), 200
    except Exception as e:
        if mydb.is_connected():
            mydb.rollback()
        return jsonify({"status": "failed","message": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
            
@app.route('/api/login', methods=['POST'])
def login():
    cursor = None
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        mydb.ping(reconnect=True)
        cursor = mydb.cursor(buffered=True)
        cursor.execute("""SELECT id, username, email, password, account_status
            FROM users WHERE email=%s
        """, [email])

        user = cursor.fetchone()
        if not user:
            return jsonify({"status": "failed","message": "User Not Found"
            }), 400

        if user[4] != "active":
            return jsonify({"status": "failed","message": "Please Verify OTP First"
            }), 400

        if not bcrypt.check_password_hash(user[3], password):
            return jsonify({"status": "failed","message": "Invalid Password"
            }), 400
        
        
        # IMPORTANT
        session["user_id"] = user[0]
        session["username"] = user[1]
        session["email"] = user[2]
        print("SESSION AFTER LOGIN =", dict(session))
        return jsonify({"status": "success","message": "Login Successful",
            "id": user[0],"username": user[1],"email": user[2]
        }), 200

    except Exception as e:
        return jsonify({"status": "failed","message": str(e)
        }), 500

    finally:
        if cursor:
            cursor.close()
            
            
@app.route('/api/logout', methods=['POST'])
def logout():
    return jsonify({"status": "success", "message": "Logout Successful"}), 200

#-------------------------Admin Navigation-------------------------------
@app.route('/api/admin-register', methods=['POST'])
def admin_register():
    cursor = None
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        if not username or not email or not password:
            return jsonify({"status": "failed","message": "All Fields Required"}), 400
        mydb.ping(reconnect=True)
        cursor = mydb.cursor(buffered=True)
        # Check admin already exists
        cursor.execute("SELECT email FROM admins WHERE email=%s",[email])
        admin = cursor.fetchone()
        if admin:
            return jsonify({"status": "failed","message": "Admin Already Exists"}), 400
        # Hash password
        hash_password = bcrypt.generate_password_hash( password).decode('utf-8')
        # Insert admin
        cursor.execute("""INSERT INTO admins(username, email, password)VALUES (%s, %s, %s)""",[username, email, hash_password])
        mydb.commit()
        return jsonify({
            "status": "success",
            "message": "Admin Registered Successfully"
        }), 200
    except Exception as e:
        if mydb.is_connected():
            mydb.rollback()
        return jsonify({"status": "failed","message": str(e) }), 500
    finally:
        if cursor:
            cursor.close()
        

@app.route("/uploads/profile_images/<filename>")
def uploaded_profile_image(filename):
    return send_from_directory(UPLOAD_FOLDER,filename)

@app.route('/api/admin-login', methods=['POST'])
def admin_login():
    cursor = None
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return jsonify({"status": "failed","message": "Email and Password Required"}), 400
        mydb.ping(reconnect=True)
        cursor = mydb.cursor(buffered=True)
        cursor.execute("""SELECT id, username, password FROM admins WHERE email=%s""", [email])
        admin = cursor.fetchone()
        if not admin:
            return jsonify({"status": "failed", "message": "Admin Not Found"
            }), 400

        check_password = bcrypt.check_password_hash(admin[2],password)
        if not check_password:
            return jsonify({"status": "failed","message": "Invalid Password"}), 400

        # ADMIN SESSION
        session["admin_logged_in"] = True
        session["admin_id"] = admin[0]
        session["admin_name"] = admin[1]

        return jsonify({"status": "success","message": "Admin Login Successful","id": admin[0],"username": admin[1]}), 200
    except Exception as e:
        return jsonify({"status": "failed", "message": str(e)}), 500
    finally:
        if cursor:
            cursor.close()

@app.route("/api/admin-logout", methods=["POST"])
def admin_logout():
    session.pop("admin_logged_in", None)
    session.pop("admin_id", None)
    session.pop("admin_name", None)
    return jsonify({"status": "success","message": "Logout Successful"}), 200


@app.route('/api/add-job', methods=['POST'])
def admin_add_job():
    cursor = None
    user_cursor = None

    try:

        # =========================
        # ADMIN LOGIN CHECK
        # =========================

        if not session.get("admin_logged_in"):
            return jsonify({
                "status": "failed",
                "message": "Please Login As Admin"
            }), 401

        admin_id = session.get("admin_id")

        if not admin_id:
            return jsonify({
                "status": "failed",
                "message": "Admin ID Not Found"
            }), 401

        # =========================
        # GET DATA
        # =========================

        mydb.ping(reconnect=True)

        cursor = mydb.cursor()

        data = request.get_json() or {}

        job_title = data.get("job_title")
        company_name = data.get("company_name")
        location = data.get("location")
        salary = data.get("salary")
        experience = data.get("experience")
        job_type = data.get("job_type")
        description = data.get("description")
        skills = data.get("skills")

        # =========================
        # REQUIRED FIELDS
        # =========================

        if not job_title or not company_name or not location:
            return jsonify({
                "status": "failed",
                "message": "Required Fields Missing"
            }), 400

        # =========================
        # INSERT JOB
        # =========================

        cursor.execute("""
            INSERT INTO jobs
            (
                admin_id,
                job_title,
                company_name,
                location,
                salary,
                experience,
                job_type,
                description,
                skills
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            admin_id,
            job_title,
            company_name,
            location,
            salary,
            experience,
            job_type,
            description,
            skills
        ))

        job_id = cursor.lastrowid

        mydb.commit()

        # =========================
        # GET NORMAL USERS
        # =========================

        user_cursor = mydb.cursor(dictionary=True)

        user_cursor.execute("""
            SELECT id, username, email
            FROM users
            WHERE account_status = 'active'
              AND email IS NOT NULL
              AND email != ''
        """)

        users = user_cursor.fetchall()

        # =========================
        # EMAIL COUNTS
        # =========================

        email_sent_count = 0
        email_failed_count = 0

        subject = "New Job Opportunity - JobPortal"

        body = (
            "A new job opportunity has been posted on JobPortal.\n\n"
            f"Job Title: {job_title}\n"
            f"Company: {company_name}\n"
            f"Location: {location}\n"
        )

        # =========================
        # CREATE HTML ONCE
        # =========================

        html_content = new_job_email(job_title,company_name,location,salary or "Not Mentioned",
            experience or "Not Mentioned", job_type or "Not Mentioned",
            skills or "Not Mentioned"
        )

        # =========================
        # SEND EMAIL TO USERS
        # =========================

        for user in users:
            user_email = user["email"]

            try:
                result = send_mail(user_email,subject,body,html_content )

                if result:
                    email_sent_count += 1
                    print(f"New job email sent to: {user_email}")

                else:
                    email_failed_count += 1
                    print( f"Mail failed for {user_email}")

            except Exception as mail_error:
                email_failed_count += 1
                print(f"Mail failed for {user_email}: {mail_error}")

        # =========================
        # SUCCESS RESPONSE
        # =========================

        return jsonify({"status": "success","message": "Job Added Successfully",
            "job_id": job_id,"admin_id": admin_id,"emails_sent": email_sent_count,
            "emails_failed": email_failed_count
        }), 201

    # =========================
    # ERROR
    # =========================

    except Exception as e:

        if mydb.is_connected():
            mydb.rollback()

        print("ADD JOB ERROR:", str(e))

        return jsonify({"status": "failed","message": str(e)
        }), 500

    # =========================
    # CLOSE CURSORS
    # =========================

    finally:

        if cursor:
            cursor.close()
            
        if user_cursor:
            user_cursor.close()
            
@app.route('/api/jobs', methods=['GET'])
def get_jobs():

    cursor = None

    try:

        mydb.ping(reconnect=True)

        cursor = mydb.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id,
                admin_id,
                job_title,
                company_name,
                location,
                salary,
                experience,
                job_type,
                description,
                skills,
                created_at
            FROM jobs
            ORDER BY created_at DESC
        """)

        jobs = cursor.fetchall()

        return jsonify({
            "status": "success",
            "count": len(jobs),
            "jobs": jobs
        }), 200

    except Exception as e:

        print("GET JOBS ERROR:", str(e))

        return jsonify({
            "status": "failed",
            "message": str(e)
        }), 500

    finally:

        if cursor:
            cursor.close()


@app.route('/api/job/<int:id>', methods=['GET'])
def get_job(id):
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM jobs WHERE id=%s",[id])
    job = cursor.fetchone()
    if not job:
        return jsonify({ "status": "failed", "message": "Job Not Found"}), 404
    return jsonify({"status": "success","job": job}), 200

@app.route("/api/profile/<int:user_id>", methods=["GET"])
def get_profile(user_id):
    cursor = None
    try:
        mydb.ping(reconnect=True)
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, username, email,phone,country,state,city,skills,
                tenth,intermediate,degree,college,branch,passout_year,
                experience,linkedin,github,profile_image,resume_path
            FROM users WHERE id=%s
        """, (user_id,))

        user = cursor.fetchone()

        if not user:
            return jsonify({"success": False,"message": "User Not Found"}), 404
        return jsonify({"success": True, "user": user
        }), 200

    except Exception as e:
        return jsonify({"success": False,"message": str(e)
        }), 500

    finally:
        if cursor:
            cursor.close()

@app.route("/api/profile/<email>", methods=["PUT"])
def update_profile(email):
    cursor = None
    try:
        data = request.form
        mydb.ping(reconnect=True)
        cursor = mydb.cursor()
        query = """UPDATE users SET username=%s,
            phone=%s,country=%s,state=%s,city=%s,skills=%s,tenth=%s,intermediate=%s,degree=%s,college=%s,branch=%s,passout_year=%s,
            experience=%s,linkedin=%s,github=%s WHERE email=%s
        """
        values = (
            data.get("username"),data.get("phone"), data.get("country"),
            data.get("state"),data.get("city"),data.get("skills"),
            data.get("tenth"),data.get("intermediate"),data.get("degree"),
            data.get("college"),data.get("branch"),data.get("passout_year"),
            data.get("experience"),data.get("linkedin"),data.get("github"),email)
        cursor.execute(query, values)
        mydb.commit()
        return jsonify({ "status": "success", "message": "Profile Updated Successfully"})
    except Exception as e:
        return jsonify({"status": "failed","message": str(e)}), 500
    finally:
        if cursor:
            cursor.close()



# ============================================================
# UPDATE JOB
# ALL ADMINS CAN EDIT ALL JOBS
# ============================================================

@app.route("/api/jobs/<int:id>", methods=["PUT"])
def update_job(id):

    cursor = None

    try:

        # =========================
        # ADMIN LOGIN CHECK
        # =========================
        if not session.get("admin_logged_in"):
            return jsonify({
                "status": "failed",
                "message": "Please Login As Admin"
            }), 401

        # =========================
        # ADMIN ID CHECK
        # =========================
        admin_id = session.get("admin_id")

        if not admin_id:
            return jsonify({
                "status": "failed",
                "message": "Admin ID Not Found"
            }), 401

        # =========================
        # DATABASE
        # =========================
        mydb.ping(reconnect=True)

        cursor = mydb.cursor(dictionary=True)

        # =========================
        # CHECK JOB EXISTS
        # =========================
        cursor.execute("""
            SELECT id
            FROM jobs
            WHERE id=%s
        """, (id,))

        job = cursor.fetchone()

        if not job:
            return jsonify({
                "status": "failed",
                "message": "Job Not Found"
            }), 404

        # =========================
        # GET FORM DATA
        # =========================
        data = request.get_json()

        job_title = data.get("job_title")
        company_name = data.get("company_name")
        location = data.get("location")
        salary = data.get("salary")
        experience = data.get("experience")
        job_type = data.get("job_type")
        skills = data.get("skills")
        description = data.get("description")

        # =========================
        # REQUIRED FIELDS
        # =========================
        if not job_title or not company_name or not location:

            return jsonify({
                "status": "failed",
                "message": "Required Fields Missing"
            }), 400

        # =========================
        # UPDATE JOB
        # =========================
        cursor.execute("""
            UPDATE jobs
            SET
                job_title=%s,
                company_name=%s,
                location=%s,
                salary=%s,
                experience=%s,
                job_type=%s,
                skills=%s,
                description=%s
            WHERE id=%s
        """, (
            job_title,
            company_name,
            location,
            salary,
            experience,
            job_type,
            skills,
            description,
            id
        ))

        mydb.commit()

        return jsonify({
            "status": "success",
            "message": "Job Updated Successfully"
        }), 200

    except Exception as e:

        if mydb.is_connected():
            mydb.rollback()

        print("UPDATE JOB ERROR:", e)

        return jsonify({
            "status": "failed",
            "message": str(e)
        }), 500

    finally:

        if cursor:
            cursor.close()


# ============================================================
# DELETE JOB
# ALL ADMINS CAN DELETE ALL JOBS
# ============================================================

@app.route("/api/jobs/<int:id>", methods=["DELETE"])
def delete_job(id):

    cursor = None

    try:

        # =========================
        # ADMIN LOGIN CHECK
        # =========================
        if not session.get("admin_logged_in"):
            return jsonify({
                "status": "failed",
                "message": "Please Login As Admin"
            }), 401

        # =========================
        # ADMIN ID CHECK
        # =========================
        admin_id = session.get("admin_id")

        if not admin_id:
            return jsonify({
                "status": "failed",
                "message": "Admin ID Not Found"
            }), 401

        # =========================
        # DATABASE
        # =========================
        mydb.ping(reconnect=True)

        cursor = mydb.cursor(dictionary=True)

        # =========================
        # CHECK JOB EXISTS
        # =========================
        cursor.execute("""
            SELECT id
            FROM jobs
            WHERE id=%s
        """, (id,))

        job = cursor.fetchone()

        if not job:

            return jsonify({
                "status": "failed",
                "message": "Job Not Found"
            }), 404

        # ====================================================
        # DELETE RELATED SAVED JOBS
        # ====================================================

        cursor.execute("""
            DELETE FROM saved_jobs
            WHERE job_id=%s
        """, (id,))

        # ====================================================
        # DELETE RELATED APPLICATIONS
        # ====================================================

        cursor.execute("""
            DELETE FROM applications
            WHERE job_id=%s
        """, (id,))

        # ====================================================
        # DELETE JOB
        # ====================================================

        cursor.execute("""
            DELETE FROM jobs
            WHERE id=%s
        """, (id,))

        mydb.commit()

        return jsonify({
            "status": "success",
            "message": "Job Deleted Successfully"
        }), 200

    except Exception as e:

        if mydb.is_connected():
            mydb.rollback()

        print("DELETE JOB ERROR:", e)

        return jsonify({
            "status": "failed",
            "message": str(e)
        }), 500

    finally:

        if cursor:
            cursor.close()


@app.route('/api/update-job/<int:job_id>', methods=['PUT'])
def update_job_admin(job_id):
    cursor = None

    try:
        # =========================
        # GET REQUEST DATA
        # =========================
        data = request.get_json() or {}

        job_title = data.get('job_title')
        company_name = data.get('company_name')
        location = data.get('location')
        salary = data.get('salary')
        experience = data.get('experience')
        job_type = data.get('job_type')
        description = data.get('description')
        skills = data.get('skills')

        # =========================
        # DATABASE CONNECTION
        # =========================
        mydb.ping(reconnect=True)

        cursor = mydb.cursor(
            dictionary=True,
            buffered=True
        )

        # =========================
        # CHECK JOB EXISTS
        # =========================
        cursor.execute(
            "SELECT id FROM jobs WHERE id=%s",
            (job_id,)
        )

        job = cursor.fetchone()

        if not job:
            return jsonify({
                "status": "failed",
                "message": "Job Not Found"
            }), 404

        # =========================
        # UPDATE JOB
        # =========================
        cursor.execute("""
            UPDATE jobs
            SET
                job_title=%s,
                company_name=%s,
                location=%s,
                salary=%s,
                experience=%s,
                job_type=%s,
                description=%s,
                skills=%s
            WHERE id=%s
        """, (
            job_title,
            company_name,
            location,
            salary,
            experience,
            job_type,
            description,
            skills,
            job_id
        ))

        mydb.commit()

        print("Job updated successfully:", job_id)

        # =========================
        # GET ALL ACTIVE USERS
        # =========================
        cursor.execute("""
            SELECT email
            FROM users
            WHERE account_status='active'
              AND email IS NOT NULL
              AND email != ''
        """)

        users = cursor.fetchall()

        print("Active users found:", len(users))

        # =========================
        # CREATE EMAIL TEMPLATE
        # =========================
        html_body = updated_job_email(
            job_title,
            company_name,
            location,
            salary or "Not Mentioned",
            experience or "Not Mentioned",
            job_type or "Not Mentioned",
            skills or "Not Mentioned"
        )

        body = "A job opportunity has been updated on JobPortal."

        # =========================
        # SEND EMAILS
        # =========================
        email_sent_count = 0
        email_failed_count = 0

        for user in users:

            user_email = user["email"]

            try:
                email_result = send_mail(
                    user_email,
                    "Job Updated - JobPortal",
                    body,
                    html_body
                )

                if email_result:
                    email_sent_count += 1

                    print(
                        f"Job update email sent to: {user_email}"
                    )

                else:
                    email_failed_count += 1

                    print(
                        f"Job update email failed for: {user_email}"
                    )

            except Exception as mail_error:

                email_failed_count += 1

                print(
                    f"EMAIL FAILED for {user_email}:",
                    mail_error
                )

        # =========================
        # SUCCESS RESPONSE
        # =========================
        return jsonify({
            "status": "success",
            "message": "Job Updated Successfully",
            "emails_sent": email_sent_count,
            "emails_failed": email_failed_count
        }), 200

    # =========================
    # ERROR
    # =========================
    except Exception as e:

        if mydb.is_connected():
            mydb.rollback()

        print(
            "UPDATE JOB ERROR:",
            str(e)
        )

        return jsonify({
            "status": "failed",
            "message": str(e)
        }), 500

    # =========================
    # CLOSE CURSOR
    # =========================
    finally:

        if cursor:
            cursor.close()
@app.route('/api/saved-jobs', methods=["GET"])
def get_saved_jobs():
    cursor = None
    try:
        print("SESSION =", dict(session))
        print("USER_ID =", session.get("user_id"))
        user_id = session.get("user_id")
        if not user_id:
            return jsonify({"status": "failed","message": "Please Login First"
            }), 401

        mydb.ping(reconnect=True)
        cursor = mydb.cursor(dictionary=True)

        cursor.execute(""" SELECT s.id AS saved_id, j.* FROM saved_jobs s
            JOIN jobs j ON s.job_id = j.id WHERE s.user_id = %s ORDER BY s.id DESC
        """, (user_id,))

        jobs = cursor.fetchall()
        return jsonify({"status": "success","jobs": jobs
        }), 200

    except Exception as e:
        return jsonify({"status": "failed","message": str(e)
        }), 500

    finally:
        if cursor:
            cursor.close()

@app.route("/api/save-job", methods=["POST"])
def add_save_job():
    cursor = None
    try:
        user_id = session.get("user_id")
        if not user_id:
            return jsonify({"status": "failed","message": "Please Login First"
            }), 401

        data = request.get_json()
        job_id = data.get("job_id")
        mydb.ping(reconnect=True)
        cursor = mydb.cursor()
        cursor.execute("SELECT id FROM saved_jobs WHERE user_id=%s AND job_id=%s",(user_id, job_id)
        )

        if cursor.fetchone():
            return jsonify({"status": "failed","message": "Job Already Saved"
            }), 400

        cursor.execute(
            "INSERT INTO saved_jobs(user_id, job_id) VALUES(%s,%s)", (user_id, job_id)
        )

        mydb.commit()

        return jsonify({"status": "success","message": "Job Saved Successfully"
        }), 200

    except Exception as e:
        return jsonify({ "status": "failed", "message": str(e)
        }), 500

    finally:
        if cursor:
            cursor.close()
@app.route("/api/upload-resume/<int:user_id>", methods=["POST"])
def upload_resume(user_id):
    cursor = None
    try:
        resume = request.files.get("resume")
        if not resume:
            return jsonify({"status": "failed","message": "Resume Required"}), 400
        filename = secure_filename(resume.filename)
        filepath = os.path.join(RESUME_FOLDER,filename)
        resume.save(filepath)
        mydb.ping(reconnect=True)
        cursor = mydb.cursor()
        cursor.execute("""UPDATE users SET resume_path=%s WHERE id=%s""", (filepath, user_id))
        mydb.commit()
        return jsonify({
            "status": "success","message": "Resume Uploaded Successfully","resume_url": filepath}), 200
    except Exception as e:
        return jsonify({"status": "failed","message": str(e)}), 500
    finally:
        if cursor:
            cursor.close()

@app.route('/uploads/resumes/<filename>')
def serve_resume(filename):
    return send_from_directory(RESUME_FOLDER,filename)
      

@app.route('/api/apply-job', methods=['POST'])
def apply_job():
    cursor = None

    try:
        data = request.get_json()

        user_id = data.get("user_id")
        job_id = data.get("job_id")
        resume = data.get("resume")

        print("DATA =", data)
        print("USER_ID =", user_id)
        print("JOB_ID =", job_id)
        print("RESUME =", resume)

        mydb.ping(reconnect=True)
        cursor = mydb.cursor(buffered=True)

        # Check User
        cursor.execute(
            "SELECT id FROM users WHERE id=%s",
            (user_id,)
        )

        if not cursor.fetchone():
            return jsonify({
                "status": "failed",
                "message": "User Not Found"
            }), 404

        # Check Job
        cursor.execute(
            "SELECT id FROM jobs WHERE id=%s",
            (job_id,)
        )

        if not cursor.fetchone():
            return jsonify({
                "status": "failed",
                "message": "Job Not Found"
            }), 404

        # Already Applied Check
        cursor.execute(
            """
            SELECT id
            FROM applications
            WHERE user_id=%s AND job_id=%s
            """,
            (user_id, job_id)
        )

        if cursor.fetchone():
            return jsonify({
                "status": "failed",
                "message": "Already Applied"
            }), 400

        # Insert Application
        cursor.execute(
            """
            INSERT INTO applications
            (user_id, job_id, resume)
            VALUES (%s, %s, %s)
            """,
            (user_id, job_id, resume)
        )

        mydb.commit()

        return jsonify({
            "status": "success",
            "message": "Job Applied Successfully"
        }), 201

    except Exception as e:
        print("ERROR =", str(e))

        return jsonify({
            "status": "failed",
            "message": str(e)
        }), 500

    finally:
        if cursor:
            cursor.close()
            
@app.route('/api/my-applications/<int:user_id>', methods=['GET'])
def my_applications(user_id):
    cursor = None
    try:
        mydb.ping(reconnect=True)
        cursor = mydb.cursor(dictionary=True)
        cursor.execute(""" SELECT a.id, a.user_id, a.job_id,a.resume,
                a.status,a.applied_date,j.job_title,j.company_name,j.location,j.salary,j.experience FROM applications a INNER JOIN jobs j ON a.job_id = j.id WHERE a.user_id = %s ORDER BY a.applied_date DESC """, [user_id])
        applications = cursor.fetchall()
        return jsonify({ "status": "success","applications": applications}), 200
    except Exception as e:
        return jsonify({"status": "failed","message": str(e)}), 500
    finally:
        if cursor:
            cursor.close()    

@app.route('/api/all-applications', methods=['GET'])
def all_applications():

    cursor = None

    try:
        # Admin login check
        if not session.get("admin_logged_in"):
            return jsonify({
                "status": "failed",
                "message": "Please Login As Admin"
            }), 401

        # Get logged-in admin ID
        admin_id = session.get("admin_id")

        if not admin_id:
            return jsonify({
                "status": "failed",
                "message": "Admin ID Not Found"
            }), 401

        mydb.ping(reconnect=True)

        cursor = mydb.cursor(dictionary=True)

        # Get all applications
        cursor.execute("""
            SELECT a.id,a.user_id,a.job_id,a.resume,a.status,a.applied_date,

                u.username,u.email,u.phone,
                j.job_title,j.company_name,j.location,j.salary,j.experience,
                j.job_type,j.admin_id AS job_admin_id
            FROM applications a
            INNER JOIN users u ON a.user_id = u.id
            INNER JOIN jobs j ON a.job_id = j.id
            ORDER BY a.applied_date DESC
        """)

        applications = cursor.fetchall()

        return jsonify({"status": "success","admin_id": admin_id,"applications": applications
        }), 200

    except Exception as e:

        print("ALL APPLICATIONS ERROR:", str(e))

        return jsonify({
            "status": "failed",
            "message": str(e)
        }), 500

    finally:

        if cursor:
            cursor.close()





@app.route("/api/admin/rejected-candidates", methods=["GET"])
def get_rejected_candidates():
    cursor = None
    try:
        if not session.get("admin_logged_in"):
            return jsonify({"status": "failed","message": "Please Login As Admin"}), 401
        mydb.ping(reconnect=True)
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("""
            SELECT a.id, a.status, a.applied_date,
                u.id AS user_id,u.username,u.email,u.phone,u.state,
                u.skills,u.tenth,u.intermediate,u.degree,u.college,u.branch,
                u.profile_image,u.resume_path
            FROM applications a JOIN users u ON a.user_id = u.id
            WHERE a.status = 'Rejected'
            ORDER BY a.applied_date DESC """)
        candidates = cursor.fetchall()
        return jsonify({"status": "success","candidates": candidates}), 200
    except Exception as e:
        return jsonify({"status": "failed","message": str(e)}), 500
    finally:
        if cursor:
            cursor.close()

@app.route('/api/update-application-status/<int:application_id>', methods=['PUT'])
def update_application_status(application_id):
    cursor = None
    try:
        
        # ADMIN LOGIN CHECK
        if not session.get("admin_logged_in"):
            return jsonify({"status": "failed","message": "Please Login As Admin"
            }), 401
        # GET ADMIN ID
        admin_id = session.get("admin_id")
        if not admin_id:
            return jsonify({"status": "failed","message": "Admin ID Not Found"
            }), 401

        
        # GET REQUEST DATA
        

        data = request.get_json() or {}
        new_status = data.get("status")
        if new_status not in ["Shortlisted", "Rejected"]:
            return jsonify({"status": "failed","message": "Invalid Status"
            }), 400

        
        # DATABASE CONNECTION

        mydb.ping(reconnect=True)
        cursor = mydb.cursor(dictionary=True)
        # GET APPLICATION DETAILS

        cursor.execute("""
            SELECT a.id,a.status,a.user_id,a.job_id,u.email AS candidate_email,
                j.admin_id AS job_admin_id,j.job_title,j.company_name,j.location
            FROM applications a INNER JOIN users u ON a.user_id = u.id
            INNER JOIN jobs j ON a.job_id = j.id
            WHERE a.id = %s """, (application_id,))
        application = cursor.fetchone()
        if not application:
            return jsonify({"status": "failed","message": "Application Not Found"
            }), 404

        # =========================
        # CHECK JOB OWNER
        # =========================

        if int(application["job_admin_id"]) != int(admin_id):
            return jsonify({"status": "failed","message": "You can manage applications only for your own jobs"
            }), 403

        # =========================
        # PREVENT DUPLICATE PROCESSING
        # =========================

        if application["status"] in ["Shortlisted", "Rejected"]:
            return jsonify({"status": "failed","message": "Application Already Processed"
            }), 400

        # =========================
        # CHECK CANDIDATE EMAIL
        # =========================

        candidate_email = application["candidate_email"]

        if not candidate_email:
            return jsonify({"status": "failed","message": "Candidate Email Not Found"
            }), 400

        # =========================
        # UPDATE APPLICATION STATUS
        # =========================

        cursor.execute("""UPDATE applications SET status = %s WHERE id = %s
        """, (new_status, application_id))

        mydb.commit()

        # GET JOB DETAILS
        

        job_title = application["job_title"] or "Job Position"
        company_name = application["company_name"] or "Company"
        location = application["location"] or "Not Mentioned"

       
        # SEND EMAIL

        email_sent = False

        # =========================
        # SHORTLISTED EMAIL
        # =========================

        if new_status == "Shortlisted":

            subject = "🎉 Application Shortlisted - JobPortal"

            # Get complete HTML from email_templates.py
            html_body = shortlisted_email(job_title,company_name,location
            )

            # Plain text fallback
            body = "Your application has been shortlisted on JobPortal."

            email_sent = send_mail(candidate_email,subject,body,html_body )

        
        # REJECTED EMAIL

        elif new_status == "Rejected":
            subject = "Application Update - JobPortal"
            # Get complete HTML from email_templates.py
            html_body = rejected_email(job_title,company_name,location)

            # Plain text fallback
            body = "Your application status has been updated on JobPortal."

            email_sent = send_mail(candidate_email,subject,body,html_body
            )

        # =========================
        # SUCCESS RESPONSE
        # =========================

        return jsonify({"status": "success","message": f"Application {new_status} Successfully","application_status": new_status,
            "email_sent": bool(email_sent)
        }), 200

    # =========================
    # ERROR
    # =========================

    except Exception as e:

        if mydb.is_connected():
            mydb.rollback()

        print( "UPDATE APPLICATION STATUS ERROR:", str(e)
        )

        return jsonify({"status": "failed","message": str(e)
        }), 500

    # =========================
    # CLOSE CURSOR
    # =========================

    finally:

        if cursor:
            cursor.close()
            
#---------------------Admin Dashboard---------
@app.route('/api/admin/dashboard', methods=['GET'])
def dashboard():
    cursor = None

    try:
        mydb.ping(reconnect=True)
        cursor = mydb.cursor(dictionary=True)

        # ==========================================
        # TOTAL USERS
        # ==========================================
        cursor.execute(""" SELECT COUNT(*) AS total_users FROM users """)

        total_users = cursor.fetchone()["total_users"]
        # TOTAL JOBS
       
        cursor.execute(""" SELECT COUNT(*) AS total_jobs FROM jobs
        """)

        total_jobs = cursor.fetchone()["total_jobs"]

        # ==========================================
        # TOTAL APPLICATIONS
        # ==========================================
        cursor.execute(""" SELECT COUNT(*) AS total_applications FROM applications
        """)

        total_applications = cursor.fetchone()["total_applications"]

        # ==========================================
        # SHORTLISTED CANDIDATES
        # ==========================================
        cursor.execute("""
            SELECT COUNT(*) AS selected_candidates FROM applications WHERE status = 'Shortlisted'
        """)

        selected_candidates = cursor.fetchone()["selected_candidates"]

        # ==========================================
        # REJECTED CANDIDATES
        # ==========================================
        cursor.execute("""
            SELECT COUNT(*) AS rejected_candidates FROM applications
            WHERE status = 'Rejected'
        """)

        rejected_candidates = cursor.fetchone()["rejected_candidates"]

        # ==========================================
        # RESPONSE
        # ==========================================
        return jsonify({
            "status": "success",
            "dashboard": {
                "total_users": total_users,
                "total_jobs": total_jobs,
                "total_applications": total_applications,
                "selected_candidates": selected_candidates,
                "rejected_candidates": rejected_candidates
            }
        }), 200

    except Exception as e:

        print("DASHBOARD ERROR:", e)

        return jsonify({
            "status": "failed",
            "message": str(e)
        }), 500

    finally:

        if cursor:
            cursor.close() 
            
@app.route('/api/upload-profile/<int:user_id>', methods=['POST'])
def upload_profile(user_id):
    cursor = None
    try:
        photo = request.files.get('photo')
        resume = request.files.get('resume')
        if not photo and not resume:
            return jsonify({"status": "failed","message": "No File Uploaded"}), 400
        photo_data = photo.read() if photo else None
        resume_data = resume.read() if resume else None
        mydb.ping(reconnect=True)
        cursor = mydb.cursor(buffered=True)
        cursor.execute("""UPDATE users SET photo=%s, resume=%s WHERE id=%s """, [photo_data, resume_data,user_id])
        mydb.commit()
        return jsonify({"status": "success","message": "Profile Updated Successfully"}), 200
    except Exception as e:
        return jsonify({"status": "failed","message": str(e)}), 500
    finally:
        if cursor:
            cursor.close() 
            
@app.route("/api/upload-profile-image/<email>", methods=["POST"])
def upload_profile_image(email):
    cursor = None
    try:
        image = request.files.get("profile_image")
        if not image:
            return jsonify({"status": "failed", "message": "Image Required"}), 400
        filename = secure_filename(image.filename)
        filepath = os.path.join(UPLOAD_FOLDER,filename)
        image.save(filepath)
        mydb.ping(reconnect=True)
        cursor = mydb.cursor()
        cursor.execute("""UPDATE users SET profile_image=%s WHERE email=%s
        """, (filepath, email))
        mydb.commit()
        return jsonify({"status": "success","message": "Profile Image Uploaded","image": filepath}), 200
    except Exception as e:
        return jsonify({"status": "failed", "message": str(e)}), 500
    finally:
        if cursor:
            cursor.close()

@app.route('/api/download-resume/<int:user_id>', methods=['GET'])
def download_resume(user_id):
    cursor = None
    try:
        mydb.ping(reconnect=True)
        cursor = mydb.cursor()
        cursor.execute("SELECT resume FROM users WHERE id=%s",[user_id])
        result = cursor.fetchone()
        if not result or result[0] is None:
            return jsonify({"status": "failed", "message": "Resume Not Found"}), 404
        return send_file(io.BytesIO(result[0]),as_attachment=True,download_name="resume.pdf",mimetype="application/pdf")
    except Exception as e:
        return jsonify({"status": "failed","message": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
            
@app.route('/uploads/profile_images/<filename>')
def serve_profile_image(filename):
    return send_from_directory(UPLOAD_FOLDER,filename)

@app.route('/api/view-photo/<int:user_id>', methods=['GET'])
def view_photo(user_id):
    cursor = None
    try:
        mydb.ping(reconnect=True)
        cursor = mydb.cursor()
        cursor.execute("SELECT photo FROM users WHERE id=%s",[user_id])
        result = cursor.fetchone()
        if not result or result[0] is None:
            return jsonify({"status": "failed","message": "Photo Not Found"}), 404
        return send_file(io.BytesIO(result[0]),mimetype="image/jpeg")
    except Exception as e:
        return jsonify({
            "status": "failed","message": str(e)}), 500
    finally:
        if cursor:
            cursor.close()




@app.route("/api/remove-saved-job/<int:saved_id>", methods=["DELETE"])
def remove_saved_job(saved_id):
    cursor = None
    try:
        user_id = session.get("user_id")
        if not user_id:
            return jsonify({"status": "failed","message": "Please Login First"}), 401
        mydb.ping(reconnect=True)
        cursor = mydb.cursor()
        cursor.execute("""DELETE FROM saved_jobs WHERE id=%s AND user_id=%s
        """, (saved_id, user_id))
        mydb.commit()
        return jsonify({"status": "success", "message": "Saved Job Removed Successfully"}), 200
    except Exception as e:
        return jsonify({ "status": "failed", "message": str(e)}), 500
    finally:
        if cursor:
            cursor.close()

@app.route("/api/admin-profile", methods=["GET"])
def admin_profile():
    if not session.get("admin_logged_in"):
        return jsonify({"status": "failed","message": "Please Login As Admin"}), 401
    return jsonify({"status": "success",
                    "admin": {"id": session.get("admin_id"),"username": session.get("admin_name")}
    }), 200


@app.route("/api/jobs", methods=["POST"])
def add_job():
    try:
        data = request.get_json()
        cursor = mydb.cursor()
        cursor.execute("""
            INSERT INTO jobs
            (job_title,company_name,location,salary,experience,job_type,
                skills,description
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            data["job_title"],data["company_name"],data["location"],
            data["salary"],data["experience"],data["job_type"],
            data["skills"],data["description"]))
        mydb.commit()
        cursor.close()
        return jsonify({ "status": "success", "message": "Job Added Successfully"
        }), 201

    except Exception as e:
        return jsonify({"status": "failed","message": str(e)
        }), 500

@app.route("/api/admin/shortlisted-candidates", methods=["GET"])
def get_shortlisted_candidates():
    cursor = None
    try:
        if not session.get("admin_logged_in"):
            return jsonify({ "status": "failed", "message": "Please Login As Admin"}), 401
        mydb.ping(reconnect=True)
        cursor = mydb.cursor(dictionary=True)
        cursor.execute(""" SELECT
                a.id,a.status,a.applied_date,a.job_id,u.id AS user_id,
                u.username,u.email,u.phone,u.state,
                u.skills,u.tenth,u.intermediate,
                u.degree,u.college,u.branch,u.profile_image,u.resume_path
            FROM applications a JOIN users u ON a.user_id = u.id
            WHERE a.status='Shortlisted'ORDER BY a.applied_date DESC """)
        candidates = cursor.fetchall()
        return jsonify({"status": "success","candidates": candidates
        }), 200

    except Exception as e:
        return jsonify({"status": "failed","message": str(e)
        }), 500

    finally:
        if cursor:
            cursor.close()

@app.route("/api/admin/users", methods=["GET"])
def get_all_users():
    cursor = None
    try:
        # Check Admin Login
        if not session.get("admin_logged_in"):
            return jsonify({"status": "failed","message": "Please Login As Admin"
            }), 401

        # Reconnect Database
        mydb.ping(reconnect=True)
        cursor = mydb.cursor(dictionary=True)
        # Get ALL Users
        cursor.execute("""
            SELECT id, username, email,phone,state,skills,tenth,intermediate,
                degree,college,branch,profile_image,resume_path
            FROM users ORDER BY id DESC
        """)

        users = cursor.fetchall()
        return jsonify({"status": "success","users": users
        }), 200

    except Exception as e:
        return jsonify({ "status": "failed", "message": str(e)
        }), 500

    finally:

        if cursor:
            cursor.close()



@app.route('/api/search-jobs', methods=['GET'])
def search_jobs():
    cursor = None
    try:
        keyword = request.args.get('keyword', '')
        mydb.ping(reconnect=True)
        cursor = mydb.cursor(dictionary=True)
        cursor.execute(""" SELECT * FROM jobs WHERE title LIKE %s OR company LIKE %s OR location LIKE %s """, [f"%{keyword}%",f"%{keyword}%",f"%{keyword}%"])
        jobs = cursor.fetchall()
        return jsonify({"status": "success","jobs": jobs}), 200
    except Exception as e:
        return jsonify({"status": "failed", "message": str(e)}), 500
    finally:
        if cursor:
            cursor.close()

@app.route('/api/filter-jobs', methods=['GET'])
def filter_jobs():
    cursor = None
    try:
        location = request.args.get('location')
        company = request.args.get('company')
        mydb.ping(reconnect=True)
        cursor = mydb.cursor(dictionary=True)
        query = "SELECT * FROM jobs WHERE 1=1"
        values = []
        if location:
            query += " AND location=%s" 
            values.append(location)
        if company:
            query += " AND company=%s"
            values.append(company)
        cursor.execute(query, values)
        jobs = cursor.fetchall()
        return jsonify({
            "status": "success","jobs": jobs}), 200
    except Exception as e:
        return jsonify({"status": "failed","message": str(e)}), 500
    finally:
        if cursor:
            cursor.close()

@app.route('/api/recent-jobs', methods=['GET'])
def recent_jobs():
    cursor = None
    try:
        mydb.ping(reconnect=True)
        cursor = mydb.cursor(dictionary=True)
        cursor.execute(""" SELECT * FROM jobs ORDER BY created_at DESC LIMIT 10""")
        jobs = cursor.fetchall()
        return jsonify({"status": "success","jobs": jobs}), 200
    except Exception as e:
        return jsonify({"status": "failed","message": str(e)}), 500
    finally:
        if cursor:
            cursor.close() 
            
@app.route('/api/add-category', methods=['POST'])
def add_category():
    cursor = None
    try:
        data = request.get_json()
        category_name = data.get('category_name')
        mydb.ping(reconnect=True)
        cursor = mydb.cursor(buffered=True)
        cursor.execute("INSERT INTO categories(category_name) VALUES(%s)",[category_name])
        mydb.commit()
        return jsonify({"status":"success","message":"Category Added Successfully"}), 201
    except Exception as e:
        return jsonify({"status":"failed","message":str(e)}), 500
    finally:
        if cursor:
            cursor.close()

@app.route('/api/categories', methods=['GET'])
def categories():
    cursor = None
    try:
        mydb.ping(reconnect=True)
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM categories ORDER BY category_name")
        categories = cursor.fetchall()
        return jsonify({"status":"success","categories":categories}), 200
    except Exception as e:
        return jsonify({"status":"failed","message":str(e)}), 500
    finally:
        if cursor:
            cursor.close()

print(app.url_map)

@app.route("/api/test-session")
def test_session():
    return {
        "user_id": session.get("user_id"),
        "username": session.get("username"),
        "email": session.get("email")
    }
                                                    
if __name__ == '__main__':
    app.run(
        debug=True,
        port=5000
    )