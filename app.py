from flask import Flask, render_template, request, redirect, session
from database import get_connection

app = Flask(__name__)

app.secret_key = "sih26044_secret_key"


@app.route("/")
def home():
    return render_template("index.html")


# ---------------- STUDENT REGISTRATION ----------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        department = request.form["department"]

        connection = get_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO students
        (name, email, password, department)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (name, email, password, department)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return "Registration Successful!"

    return render_template("register.html")


# ---------------- STUDENT LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT * FROM students
        WHERE email = %s AND password = %s
        """

        cursor.execute(query, (email, password))

        student = cursor.fetchone()

        cursor.close()
        connection.close()

        if student:

            session["student_id"] = student["id"]
            session["student_name"] = student["name"]

            return redirect("/dashboard")

        return "Invalid Email or Password"

    return render_template("login.html")
# ---------------- COMPANY REGISTRATION ----------------

@app.route("/company/register", methods=["GET", "POST"])
def company_register():

    if request.method == "POST":

        company_name = request.form["company_name"]
        email = request.form["email"]
        password = request.form["password"]
        industry = request.form["industry"]
        requirements = request.form["requirements"]

        connection = get_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO companies
        (company_name, email, password, industry, requirements)
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                company_name,
                email,
                password,
                industry,
                requirements
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        return "Company Registration Successful!"

    return render_template("company_register.html")
# ---------------- COMPANY LOGIN ----------------

@app.route("/company/login", methods=["GET", "POST"])
def company_login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT * FROM companies
        WHERE email = %s AND password = %s
        """

        cursor.execute(query, (email, password))

        company = cursor.fetchone()

        cursor.close()
        connection.close()

        if company:

            session["company_id"] = company["id"]
            session["company_name"] = company["company_name"]

            return redirect("/company/dashboard")

        return "Invalid Company Email or Password"

    return render_template("company_login.html")
# ---------------- COMPANY DASHBOARD ----------------

@app.route("/company/dashboard")
def company_dashboard():

    if "company_id" not in session:
        return redirect("/company/login")

    return render_template(
        "company_dashboard.html",
        name=session["company_name"]
    )
# ---------------- POST INTERNSHIP ----------------

@app.route("/company/post-internship", methods=["GET", "POST"])
def post_internship():

    if "company_id" not in session:
        return redirect("/company/login")

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        required_skills = request.form["required_skills"]
        location = request.form["location"]
        duration = request.form["duration"]
        stipend = request.form["stipend"]

        connection = get_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO internships
        (company_id, title, description, required_skills,
         location, duration, stipend)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                session["company_id"],
                title,
                description,
                required_skills,
                location,
                duration,
                stipend
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        return "Internship Posted Successfully!"

    return render_template("company_post_internship.html")
# ---------------- POST JOB ----------------

@app.route("/company/post-job", methods=["GET", "POST"])
def post_job():

    if "company_id" not in session:
        return redirect("/company/login")

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        required_skills = request.form["required_skills"]
        location = request.form["location"]
        salary = request.form["salary"]

        connection = get_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO jobs
        (company_id, title, description, required_skills,
         location, salary)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                session["company_id"],
                title,
                description,
                required_skills,
                location,
                salary
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        return "Job Posted Successfully!"

    return render_template("company_post_job.html")
# ---------------- STUDENT JOBS ----------------

@app.route("/jobs")
def jobs():

    if "student_id" not in session:
        return redirect("/login")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT jobs.*, companies.company_name
    FROM jobs
    JOIN companies
    ON jobs.company_id = companies.id
    ORDER BY jobs.created_at DESC
    """

    cursor.execute(query)

    job_list = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "student_jobs.html",
        jobs=job_list
    )
# ---------------- APPLY FOR JOB ----------------

@app.route("/apply-job/<int:job_id>")
def apply_job(job_id):

    if "student_id" not in session:
        return redirect("/login")

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO job_applications
    (student_id, job_id)
    VALUES (%s, %s)
    """

    cursor.execute(
        query,
        (session["student_id"], job_id)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return "Job Application Submitted Successfully!"

# ---------------- STUDENT DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():

    if "student_id" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        name=session["student_name"]
    )
# ---------------- STUDENT INTERNSHIPS ----------------

@app.route("/internships")
def internships():

    if "student_id" not in session:
        return redirect("/login")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT internships.*, companies.company_name
    FROM internships
    JOIN companies
    ON internships.company_id = companies.id
    ORDER BY internships.created_at DESC
    """

    cursor.execute(query)

    internship_list = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "student_internships.html",
        internships=internship_list
    )
# ---------------- SKILL ASSESSMENT ----------------

@app.route("/assessment", methods=["GET", "POST"])
def assessment():

    if "student_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        skill = request.form["skill"]
        score = int(request.form["score"])

        if score <= 3:
            level = "Beginner"
        elif score <= 7:
            level = "Intermediate"
        else:
            level = "Advanced"

        connection = get_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO assessments
        (student_id, skill, score, level)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                session["student_id"],
                skill,
                score,
                level
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        return "Assessment Submitted Successfully! Level: " + level

    return render_template("assessment.html")
# ---------------- SKILL GAP ANALYSIS ----------------

@app.route("/skill-gap")
def skill_gap():

    if "student_id" not in session:
        return redirect("/login")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT skill, score, level
    FROM assessments
    WHERE student_id = %s
    ORDER BY created_at DESC
    """

    cursor.execute(
        query,
        (session["student_id"],)
    )

    assessment_list = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "skill_gap.html",
        assessments=assessment_list
    )
# ---------------- LEARNING RECOMMENDATIONS ----------------

@app.route("/recommendations")
def recommendations():

    if "student_id" not in session:
        return redirect("/login")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT skill, score, level
    FROM assessments
    WHERE student_id = %s
    ORDER BY created_at DESC
    """

    cursor.execute(
        query,
        (session["student_id"],)
    )

    assessment_list = cursor.fetchall()

    cursor.close()
    connection.close()

    recommendation_list = []

    for assessment in assessment_list:

        if assessment["score"] < 5:
            recommendation = "Practice this skill regularly and complete beginner-level courses."

        elif assessment["score"] < 8:
            recommendation = "Improve this skill by completing projects and intermediate courses."

        else:
            recommendation = "Continue advanced learning and build real-world projects."

        recommendation_list.append({
            "skill": assessment["skill"],
            "score": assessment["score"],
            "level": assessment["level"],
            "recommendation": recommendation
        })

    return render_template(
        "recommendations.html",
        recommendations=recommendation_list
    )
# ---------------- INTERNSHIP SKILL MATCHING ----------------

@app.route("/matching")
def matching():

    if "student_id" not in session:
        return redirect("/login")

    connection = get_connection()

    # Get student's skills
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT skills
        FROM students
        WHERE id = %s
        """,
        (session["student_id"],)
    )

    student = cursor.fetchone()

    # Get all internships
    cursor.execute(
        """
        SELECT internships.*, companies.company_name
        FROM internships
        JOIN companies
        ON internships.company_id = companies.id
        ORDER BY internships.created_at DESC
        """
    )

    internship_list = cursor.fetchall()

    cursor.close()
    connection.close()

    # Student skills
    student_skills = []

    if student and student["skills"]:
        student_skills = [
            skill.strip().lower()
            for skill in student["skills"].split(",")
        ]

    matching_list = []

    for internship in internship_list:

        required_skills = [
            skill.strip().lower()
            for skill in internship["required_skills"].split(",")
        ]

        matching_skills = []

        for skill in required_skills:
            if skill in student_skills:
                matching_skills.append(skill)

        if len(required_skills) > 0:
            match_score = int(
                (len(matching_skills) / len(required_skills)) * 100
            )
        else:
            match_score = 0

        if match_score > 0:
            internship["matching_skills"] = ", ".join(matching_skills)
            internship["match_score"] = match_score

            matching_list.append(internship)

    return render_template(
        "student_matching.html",
        internships=matching_list
    )
# ---------------- APPLY FOR INTERNSHIP ----------------

@app.route("/apply/<int:internship_id>")
def apply_internship(internship_id):

    if "student_id" not in session:
        return redirect("/login")

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO applications
    (student_id, internship_id)
    VALUES (%s, %s)
    """

    cursor.execute(
        query,
        (
            session["student_id"],
            internship_id
        )
    )

    connection.commit()

    cursor.close()
    connection.close()

    return "Application Submitted Successfully!"
# ---------------- COMPANY APPLICATIONS ----------------

@app.route("/company/applications")
def company_applications():

    if "company_id" not in session:
        return redirect("/company/login")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT
        applications.id,
        students.name AS student_name,
        students.email,
        students.skills,
        internships.title,
        applications.status
    FROM applications
    JOIN students
        ON applications.student_id = students.id
    JOIN internships
        ON applications.internship_id = internships.id
    WHERE internships.company_id = %s
    ORDER BY applications.applied_at DESC"""
    

    cursor.execute(
        query,
        (session["company_id"],)
    )

    application_list = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "company_applications.html",
        applications=application_list
    )
# ---------------- STUDENT PROFILE ----------------

@app.route("/profile", methods=["GET", "POST"])
def profile():

    if "student_id" not in session:
        return redirect("/login")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":

        skills = request.form["skills"]
        projects = request.form["projects"]
        certificates = request.form["certificates"]

        query = """
        UPDATE students
        SET skills=%s,
            projects=%s,
            certificates=%s
        WHERE id=%s
        """

        cursor.execute(
            query,
            (
                skills,
                projects,
                certificates,
                session["student_id"]
            )
        )

        connection.commit()

    query = """
    SELECT * FROM students
    WHERE id=%s
    """

    cursor.execute(query, (session["student_id"],))

    student = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template(
        "profile.html",
        student=student
    )
# ---------------- COMPANY LOGOUT ----------------

@app.route("/company/logout")
def company_logout():

    session.pop("company_id", None)
    session.pop("company_name", None)

    return redirect("/company/login")


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# ---------------- RUN APPLICATION ----------------

if __name__ == "__main__":
    app.run(debug=True)