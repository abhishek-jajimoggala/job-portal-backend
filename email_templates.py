def new_job_email(job_title, company_name, location, salary, experience, job_type, skills):
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>New Job Opportunity</title>
</head>

<body style="margin:0; padding:0; background-color:#f4f6f8; font-family:Arial, sans-serif;">

    <div style="max-width:650px; margin:30px auto; background:#ffffff; border-radius:12px; overflow:hidden; box-shadow:0 4px 15px rgba(0,0,0,0.10);">

        <!-- Header -->
        <div style="background:#275DF5; padding:25px; text-align:center;">
            <h1 style="color:white; margin:0; font-size:28px;">
                JobPortal
            </h1>
            <p style="color:#eaf0ff; margin:8px 0 0;">
                Find your next career opportunity
            </p>
        </div>

        <!-- Content -->
        <div style="padding:30px;">

            <h2 style="color:#222; margin-top:0;">
                🎉 New Job Opportunity!
            </h2>

            <p style="color:#555; font-size:15px;">
                A new job has been posted on JobPortal. Check out the details below.
            </p>

            <!-- Job Card -->
            <div style="background:#f8faff; border:1px solid #e2e8f0; border-radius:10px; padding:22px; margin-top:20px;">

                <h2 style="color:#275DF5; margin-top:0;">
                    {job_title}
                </h2>

                <p style="font-size:16px; margin:8px 0;">
                    🏢 <strong>Company:</strong> {company_name}
                </p>

                <p style="font-size:16px; margin:8px 0;">
                    📍 <strong>Location:</strong> {location}
                </p>

                <p style="font-size:16px; margin:8px 0;">
                    💰 <strong>Salary:</strong> {salary}
                </p>

                <p style="font-size:16px; margin:8px 0;">
                    💼 <strong>Job Type:</strong> {job_type}
                </p>

                <p style="font-size:16px; margin:8px 0;">
                    🎓 <strong>Experience:</strong> {experience}
                </p>

                <p style="font-size:16px; margin:8px 0;">
                    🛠️ <strong>Skills:</strong> {skills}
                </p>

            </div>

            <!-- Button -->
            <div style="text-align:center; margin:30px 0 15px;">
                <a href="http://localhost:5173/jobs"
                   style="display:inline-block;
                          background:#275DF5;
                          color:white;
                          text-decoration:none;
                          padding:14px 30px;
                          border-radius:7px;
                          font-size:16px;
                          font-weight:bold;">
                    View Job Opportunities
                </a>
            </div>

            <p style="color:#666; font-size:14px; line-height:1.6;">
                Login to JobPortal to view the complete job description and apply for this opportunity.
            </p>

        </div>

        <!-- Footer -->
        <div style="background:#f1f3f5; padding:20px; text-align:center;">

            <p style="margin:0; color:#555; font-size:14px;">
                © 2026 JobPortal. All rights reserved.
            </p>

            <p style="margin:7px 0 0; color:#888; font-size:12px;">
                This is an automated notification. Please do not reply to this email.
            </p>

        </div>

    </div>

</body>
</html>
"""


def updated_job_email(job_title, company_name, location, salary, experience, job_type, skills):
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Job Updated</title>
</head>

<body style="margin:0; padding:0; background:#f4f6f8; font-family:Arial,sans-serif;">

<div style="max-width:650px; margin:30px auto; background:white; border-radius:12px; overflow:hidden;">

    <div style="background:#275DF5; padding:25px; text-align:center;">
        <h1 style="color:white; margin:0;">JobPortal</h1>
        <p style="color:#eaf0ff;">Job Opportunity Updated</p>
    </div>

    <div style="padding:30px;">

        <h2 style="color:#222;">
            ✏️ Job Updated
        </h2>

        <p style="color:#555;">
            A job opportunity you may be interested in has been updated.
        </p>

        <div style="background:#f8faff; border:1px solid #e2e8f0; border-radius:10px; padding:22px;">

            <h2 style="color:#275DF5;">
                {job_title}
            </h2>

            <p>🏢 <strong>Company:</strong> {company_name}</p>
            <p>📍 <strong>Location:</strong> {location}</p>
            <p>💰 <strong>Salary:</strong> {salary}</p>
            <p>💼 <strong>Job Type:</strong> {job_type}</p>
            <p>🎓 <strong>Experience:</strong> {experience}</p>
            <p>🛠️ <strong>Skills:</strong> {skills}</p>

        </div>

        <div style="text-align:center; margin:30px;">
            <a href="http://localhost:5173/jobs"
               style="background:#275DF5;
                      color:white;
                      text-decoration:none;
                      padding:14px 30px;
                      border-radius:7px;
                      font-weight:bold;">
                View Updated Job
            </a>
        </div>

    </div>

    <div style="background:#f1f3f5; padding:20px; text-align:center;">
        <p style="margin:0; color:#555;">
            © 2026 JobPortal. All rights reserved.
        </p>
    </div>

</div>

</body>
</html>
"""


def shortlisted_email(job_title, company_name, location):
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Application Shortlisted</title>
</head>

<body style="margin:0; padding:0; background:#f4f6f8; font-family:Arial,sans-serif;">

<div style="max-width:650px; margin:30px auto; background:white; border-radius:12px; overflow:hidden;">

    <div style="background:#275DF5; padding:25px; text-align:center;">
        <h1 style="color:white; margin:0;">JobPortal</h1>
    </div>

    <div style="padding:35px; text-align:center;">

        <div style="font-size:55px;">🎉</div>

        <h2 style="color:#198754;">
            Congratulations!
        </h2>

        <p style="color:#555; font-size:16px;">
            Your application has been shortlisted.
        </p>

        <div style="background:#f8faff;
                    border:1px solid #e2e8f0;
                    border-radius:10px;
                    padding:20px;
                    text-align:left;
                    margin-top:25px;">

            <h2 style="color:#275DF5;">
                {job_title}
            </h2>

            <p>🏢 <strong>Company:</strong> {company_name}</p>
            <p>📍 <strong>Location:</strong> {location}</p>

        </div>

        <p style="color:#555; margin-top:25px; line-height:1.6;">
            The employer has reviewed your application and selected
            you for the next stage of the recruitment process.
        </p>

        <a href="http://localhost:5173/my-applications"
           style="display:inline-block;
                  background:#198754;
                  color:white;
                  text-decoration:none;
                  padding:14px 30px;
                  border-radius:7px;
                  font-weight:bold;
                  margin-top:15px;">
            View My Application
        </a>

    </div>

    <div style="background:#f1f3f5; padding:20px; text-align:center;">
        <p style="margin:0; color:#555;">
            © 2026 JobPortal. All rights reserved.
        </p>
    </div>

</div>

</body>
</html>
"""


def rejected_email(job_title, company_name, location):
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Application Update</title>
</head>

<body style="margin:0; padding:0; background:#f4f6f8; font-family:Arial,sans-serif;">

<div style="max-width:650px; margin:30px auto; background:white; border-radius:12px; overflow:hidden;">

    <div style="background:#275DF5; padding:25px; text-align:center;">
        <h1 style="color:white; margin:0;">JobPortal</h1>
    </div>

    <div style="padding:35px;">

        <div style="text-align:center; font-size:50px;">
            📋
        </div>

        <h2 style="text-align:center; color:#333;">
            Application Update
        </h2>

        <p style="color:#555; line-height:1.7;">
            Thank you for taking the time to apply for this position.
            After reviewing your application, the employer has decided
            not to move forward with your application at this time.
        </p>

        <div style="background:#fff5f5;
                    border:1px solid #f1caca;
                    border-radius:10px;
                    padding:20px;
                    margin-top:20px;">

            <h2 style="color:#dc3545;">
                {job_title}
            </h2>

            <p>🏢 <strong>Company:</strong> {company_name}</p>
            <p>📍 <strong>Location:</strong> {location}</p>
            <p>
                ❌ <strong>Status:</strong>
                Application Not Selected
            </p>

        </div>

        <p style="color:#555; line-height:1.7; margin-top:25px;">
            Don't be discouraged. Continue exploring new opportunities
            on JobPortal and keep applying for positions that match your skills.
        </p>

        <div style="text-align:center; margin-top:25px;">
            <a href="http://localhost:5173/jobs"
               style="display:inline-block;
                      background:#275DF5;
                      color:white;
                      text-decoration:none;
                      padding:14px 30px;
                      border-radius:7px;
                      font-weight:bold;">
                Explore More Jobs
            </a>
        </div>

    </div>

    <div style="background:#f1f3f5; padding:20px; text-align:center;">
        <p style="margin:0; color:#555;">
            © 2026 JobPortal. All rights reserved.
        </p>
    </div>

</div>

</body>
</html>
"""

def otp_email_template(username, otp):
    otp_boxes = "".join(
        [f"""
        <td style="
            width:50px;
            height:50px;
            border:2px solid #275DF5;
            border-radius:8px;
            text-align:center;
            font-size:24px;
            font-weight:bold;
            color:#275DF5;
            background:#f8f9ff;
        ">
            {digit}
        </td>
        """ for digit in str(otp)]
    )

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
    </head>
    <body style="
        margin:0;
        padding:0;
        background:#f4f6f9;
        font-family:Arial,sans-serif;
    ">
        <div style="
            max-width:600px;
            margin:30px auto;
            background:#ffffff;
            border-radius:12px;
            overflow:hidden;
            box-shadow:0 4px 10px rgba(0,0,0,0.1);
        ">

            <div style="
                background:#275DF5;
                color:white;
                padding:20px;
                text-align:center;
            ">
                <h2 style="margin:0;">Job Portal</h2>
            </div>

            <div style="padding:30px; text-align:center;">

                <h3>Hello {username},</h3>

                <p>
                    Use the following OTP to verify your account.
                </p>

                <table
                    align="center"
                    cellpadding="5"
                    cellspacing="5"
                    style="margin:20px auto;"
                >
                    <tr>
                        {otp_boxes}
                    </tr>
                </table>

                <p style="color:#666;">
                    This OTP is valid for 5 minutes.
                </p>

                <p style="color:#999; font-size:13px;">
                    Do not share this OTP with anyone.
                </p>

            </div>

            <div style="
                background:#f5f5f5;
                padding:15px;
                text-align:center;
                color:#777;
                font-size:12px;
            ">
                © 2026 Job Portal. All Rights Reserved.
            </div>

        </div>
    </body>
    </html>
    """