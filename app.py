import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import session

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "portfolio.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", os.urandom(32).hex())

db = SQLAlchemy(app)


# ── Models ───────────────────────────────────────────────────────────────────

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    tagline = db.Column(db.String(200))
    bio = db.Column(db.Text)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(30))
    address = db.Column(db.String(200))
    linkedin = db.Column(db.String(300))
    github = db.Column(db.String(300))


class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200))
    start_date = db.Column(db.String(50))
    end_date = db.Column(db.String(50))
    description = db.Column(db.Text)
    sort_order = db.Column(db.Integer, default=0)


class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    degree = db.Column(db.String(200), nullable=False)
    institution = db.Column(db.String(200), nullable=False)
    year = db.Column(db.String(50))
    sort_order = db.Column(db.Integer, default=0)


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    items = db.Column(db.Text, nullable=False)
    sort_order = db.Column(db.Integer, default=0)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    technologies = db.Column(db.String(300))
    url = db.Column(db.String(300))
    sort_order = db.Column(db.Integer, default=0)


class Certification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    issuer = db.Column(db.String(200))
    date_obtained = db.Column(db.String(50))
    sort_order = db.Column(db.Integer, default=0)


class AdminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# ── Auth helpers ─────────────────────────────────────────────────────────────

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated


# ── Public routes ────────────────────────────────────────────────────────────

@app.route("/")
def index():
    profile = Profile.query.first()
    experiences = Experience.query.order_by(Experience.sort_order).all()
    educations = Education.query.order_by(Education.sort_order).all()
    skills = Skill.query.order_by(Skill.sort_order).all()
    projects = Project.query.order_by(Project.sort_order).all()
    certifications = Certification.query.order_by(Certification.sort_order).all()
    return render_template(
        "index.html",
        profile=profile,
        experiences=experiences,
        educations=educations,
        skills=skills,
        projects=projects,
        certifications=certifications,
    )


# ── Admin auth routes ────────────────────────────────────────────────────────

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        user = AdminUser.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session["admin_logged_in"] = True
            flash("Logged in successfully.", "success")
            return redirect(url_for("admin_dashboard"))
        flash("Invalid credentials.", "danger")
    return render_template("admin/login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    flash("Logged out.", "info")
    return redirect(url_for("index"))


# ── Admin dashboard ──────────────────────────────────────────────────────────

@app.route("/admin")
@login_required
def admin_dashboard():
    profile = Profile.query.first()
    experiences = Experience.query.order_by(Experience.sort_order).all()
    educations = Education.query.order_by(Education.sort_order).all()
    skills = Skill.query.order_by(Skill.sort_order).all()
    projects = Project.query.order_by(Project.sort_order).all()
    certifications = Certification.query.order_by(Certification.sort_order).all()
    return render_template(
        "admin/dashboard.html",
        profile=profile,
        experiences=experiences,
        educations=educations,
        skills=skills,
        projects=projects,
        certifications=certifications,
    )


# ── Profile CRUD ─────────────────────────────────────────────────────────────

@app.route("/admin/profile", methods=["GET", "POST"])
@login_required
def admin_profile():
    profile = Profile.query.first()
    if not profile:
        profile = Profile(full_name="")
        db.session.add(profile)
        db.session.commit()
    if request.method == "POST":
        profile.full_name = request.form.get("full_name", "")
        profile.tagline = request.form.get("tagline", "")
        profile.bio = request.form.get("bio", "")
        profile.email = request.form.get("email", "")
        profile.phone = request.form.get("phone", "")
        profile.address = request.form.get("address", "")
        profile.linkedin = request.form.get("linkedin", "")
        profile.github = request.form.get("github", "")
        db.session.commit()
        flash("Profile updated.", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("admin/profile_form.html", profile=profile)


# ── Experience CRUD ──────────────────────────────────────────────────────────

@app.route("/admin/experience/add", methods=["GET", "POST"])
@login_required
def admin_experience_add():
    if request.method == "POST":
        exp = Experience(
            job_title=request.form.get("job_title", ""),
            company=request.form.get("company", ""),
            location=request.form.get("location", ""),
            start_date=request.form.get("start_date", ""),
            end_date=request.form.get("end_date", ""),
            description=request.form.get("description", ""),
            sort_order=int(request.form.get("sort_order", 0)),
        )
        db.session.add(exp)
        db.session.commit()
        flash("Experience added.", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("admin/experience_form.html", experience=None)


@app.route("/admin/experience/edit/<int:id>", methods=["GET", "POST"])
@login_required
def admin_experience_edit(id):
    exp = Experience.query.get_or_404(id)
    if request.method == "POST":
        exp.job_title = request.form.get("job_title", "")
        exp.company = request.form.get("company", "")
        exp.location = request.form.get("location", "")
        exp.start_date = request.form.get("start_date", "")
        exp.end_date = request.form.get("end_date", "")
        exp.description = request.form.get("description", "")
        exp.sort_order = int(request.form.get("sort_order", 0))
        db.session.commit()
        flash("Experience updated.", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("admin/experience_form.html", experience=exp)


@app.route("/admin/experience/delete/<int:id>", methods=["POST"])
@login_required
def admin_experience_delete(id):
    exp = Experience.query.get_or_404(id)
    db.session.delete(exp)
    db.session.commit()
    flash("Experience deleted.", "success")
    return redirect(url_for("admin_dashboard"))


# ── Education CRUD ───────────────────────────────────────────────────────────

@app.route("/admin/education/add", methods=["GET", "POST"])
@login_required
def admin_education_add():
    if request.method == "POST":
        edu = Education(
            degree=request.form.get("degree", ""),
            institution=request.form.get("institution", ""),
            year=request.form.get("year", ""),
            sort_order=int(request.form.get("sort_order", 0)),
        )
        db.session.add(edu)
        db.session.commit()
        flash("Education added.", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("admin/education_form.html", education=None)


@app.route("/admin/education/edit/<int:id>", methods=["GET", "POST"])
@login_required
def admin_education_edit(id):
    edu = Education.query.get_or_404(id)
    if request.method == "POST":
        edu.degree = request.form.get("degree", "")
        edu.institution = request.form.get("institution", "")
        edu.year = request.form.get("year", "")
        edu.sort_order = int(request.form.get("sort_order", 0))
        db.session.commit()
        flash("Education updated.", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("admin/education_form.html", education=edu)


@app.route("/admin/education/delete/<int:id>", methods=["POST"])
@login_required
def admin_education_delete(id):
    edu = Education.query.get_or_404(id)
    db.session.delete(edu)
    db.session.commit()
    flash("Education deleted.", "success")
    return redirect(url_for("admin_dashboard"))


# ── Skills CRUD ──────────────────────────────────────────────────────────────

@app.route("/admin/skill/add", methods=["GET", "POST"])
@login_required
def admin_skill_add():
    if request.method == "POST":
        skill = Skill(
            category=request.form.get("category", ""),
            items=request.form.get("items", ""),
            sort_order=int(request.form.get("sort_order", 0)),
        )
        db.session.add(skill)
        db.session.commit()
        flash("Skill added.", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("admin/skill_form.html", skill=None)


@app.route("/admin/skill/edit/<int:id>", methods=["GET", "POST"])
@login_required
def admin_skill_edit(id):
    skill = Skill.query.get_or_404(id)
    if request.method == "POST":
        skill.category = request.form.get("category", "")
        skill.items = request.form.get("items", "")
        skill.sort_order = int(request.form.get("sort_order", 0))
        db.session.commit()
        flash("Skill updated.", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("admin/skill_form.html", skill=skill)


@app.route("/admin/skill/delete/<int:id>", methods=["POST"])
@login_required
def admin_skill_delete(id):
    skill = Skill.query.get_or_404(id)
    db.session.delete(skill)
    db.session.commit()
    flash("Skill deleted.", "success")
    return redirect(url_for("admin_dashboard"))


# ── Projects CRUD ────────────────────────────────────────────────────────────

@app.route("/admin/project/add", methods=["GET", "POST"])
@login_required
def admin_project_add():
    if request.method == "POST":
        proj = Project(
            title=request.form.get("title", ""),
            description=request.form.get("description", ""),
            technologies=request.form.get("technologies", ""),
            url=request.form.get("url", ""),
            sort_order=int(request.form.get("sort_order", 0)),
        )
        db.session.add(proj)
        db.session.commit()
        flash("Project added.", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("admin/project_form.html", project=None)


@app.route("/admin/project/edit/<int:id>", methods=["GET", "POST"])
@login_required
def admin_project_edit(id):
    proj = Project.query.get_or_404(id)
    if request.method == "POST":
        proj.title = request.form.get("title", "")
        proj.description = request.form.get("description", "")
        proj.technologies = request.form.get("technologies", "")
        proj.url = request.form.get("url", "")
        proj.sort_order = int(request.form.get("sort_order", 0))
        db.session.commit()
        flash("Project updated.", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("admin/project_form.html", project=proj)


@app.route("/admin/project/delete/<int:id>", methods=["POST"])
@login_required
def admin_project_delete(id):
    proj = Project.query.get_or_404(id)
    db.session.delete(proj)
    db.session.commit()
    flash("Project deleted.", "success")
    return redirect(url_for("admin_dashboard"))


# ── Certifications CRUD ─────────────────────────────────────────────────────

@app.route("/admin/certification/add", methods=["GET", "POST"])
@login_required
def admin_certification_add():
    if request.method == "POST":
        cert = Certification(
            title=request.form.get("title", ""),
            issuer=request.form.get("issuer", ""),
            date_obtained=request.form.get("date_obtained", ""),
            sort_order=int(request.form.get("sort_order", 0)),
        )
        db.session.add(cert)
        db.session.commit()
        flash("Certification added.", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("admin/certification_form.html", certification=None)


@app.route("/admin/certification/edit/<int:id>", methods=["GET", "POST"])
@login_required
def admin_certification_edit(id):
    cert = Certification.query.get_or_404(id)
    if request.method == "POST":
        cert.title = request.form.get("title", "")
        cert.issuer = request.form.get("issuer", "")
        cert.date_obtained = request.form.get("date_obtained", "")
        cert.sort_order = int(request.form.get("sort_order", 0))
        db.session.commit()
        flash("Certification updated.", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("admin/certification_form.html", certification=cert)


@app.route("/admin/certification/delete/<int:id>", methods=["POST"])
@login_required
def admin_certification_delete(id):
    cert = Certification.query.get_or_404(id)
    db.session.delete(cert)
    db.session.commit()
    flash("Certification deleted.", "success")
    return redirect(url_for("admin_dashboard"))


# ── Bootstrap DB ─────────────────────────────────────────────────────────────

with app.app_context():
    db.create_all()
    if not AdminUser.query.first():
        admin = AdminUser(username="admin")
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()


if __name__ == "__main__":
    app.run(debug=True, port=5000)
