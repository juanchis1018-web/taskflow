"""TaskFlow: aplicación web de gestión de usuarios y tareas (proyecto de semestre)."""
import os
from functools import wraps

from flask import (
    Flask,
    abort,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from . import db, services
from .validators import ValidationError


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-taskflow-cambiar-en-produccion"),
        DATABASE=os.path.join(app.instance_path, "taskflow.sqlite"),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
    )
    if test_config:
        app.config.update(test_config)
    os.makedirs(app.instance_path, exist_ok=True)
    db.init_app(app)

    # ------------------------------------------------------------ helpers
    @app.before_request
    def load_user():
        uid = session.get("user_id")
        g.user = services.get_user(uid) if uid else None

    def login_required(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if g.user is None:
                if request.path.startswith("/api/"):
                    return jsonify(error="No autenticado"), 401
                return redirect(url_for("login"))
            return view(*args, **kwargs)

        return wrapped

    def admin_required(view):
        @wraps(view)
        @login_required
        def wrapped(*args, **kwargs):
            if g.user["role"] != "admin":
                abort(403)
            return view(*args, **kwargs)

        return wrapped

    @app.after_request
    def security_headers(resp):
        resp.headers["X-Content-Type-Options"] = "nosniff"
        resp.headers["X-Frame-Options"] = "DENY"
        return resp

    # --------------------------------------------------------------- auth
    @app.route("/")
    def index():
        return redirect(url_for("dashboard" if g.user else "login"))

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            try:
                services.register_user(
                    request.form.get("username"),
                    request.form.get("email"),
                    request.form.get("password"),
                )
                flash("Registro exitoso. Ahora puede iniciar sesión.", "ok")
                return redirect(url_for("login"))
            except ValidationError as err:
                flash(str(err), "error")
                return render_template("register.html"), 400
        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            user = services.authenticate(
                request.form.get("username"), request.form.get("password")
            )
            if user is None:
                flash("Usuario o contraseña incorrectos.", "error")
                return render_template("login.html"), 401
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("dashboard"))
        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("login"))

    # -------------------------------------------------------------- tareas
    @app.route("/dashboard")
    @login_required
    def dashboard():
        q = request.args.get("q", "").strip()
        return render_template(
            "dashboard.html",
            tasks=services.list_tasks(g.user["id"], q or None),
            stats=services.task_stats(g.user["id"]),
            q=q,
        )

    @app.route("/tasks/new", methods=["POST"])
    @login_required
    def task_new():
        try:
            services.create_task(
                g.user["id"],
                request.form.get("title"),
                request.form.get("description"),
                request.form.get("priority", "media"),
                request.form.get("due_date") or None,
            )
            flash("Tarea creada.", "ok")
        except ValidationError as err:
            flash(str(err), "error")
        return redirect(url_for("dashboard"))

    @app.route("/tasks/<int:task_id>/toggle", methods=["POST"])
    @login_required
    def task_toggle(task_id):
        if not services.toggle_task(task_id, g.user["id"]):
            abort(404)
        return redirect(url_for("dashboard"))

    @app.route("/tasks/<int:task_id>/delete", methods=["POST"])
    @login_required
    def task_delete(task_id):
        if not services.delete_task(task_id, g.user["id"]):
            abort(404)
        flash("Tarea eliminada.", "ok")
        return redirect(url_for("dashboard"))

    # -------------------------------------------------------------- perfil
    @app.route("/profile", methods=["GET", "POST"])
    @login_required
    def profile():
        if request.method == "POST":
            try:
                services.update_profile(
                    g.user["id"],
                    request.form.get("email"),
                    request.form.get("new_password") or None,
                )
                flash("Perfil actualizado.", "ok")
                return redirect(url_for("profile"))
            except ValidationError as err:
                flash(str(err), "error")
        return render_template("profile.html")

    @app.route("/profile/delete", methods=["POST"])
    @login_required
    def profile_delete():
        services.delete_user(g.user["id"])
        session.clear()
        flash("Su cuenta fue eliminada.", "ok")
        return redirect(url_for("login"))

    # --------------------------------------------------------------- admin
    @app.route("/admin/users")
    @admin_required
    def admin_users():
        return render_template("admin.html", users=services.list_users())

    # ----------------------------------------------------------------- API
    @app.get("/api/tasks")
    @login_required
    def api_list():
        return jsonify([dict(t) for t in services.list_tasks(g.user["id"])])

    @app.post("/api/tasks")
    @login_required
    def api_create():
        data = request.get_json(silent=True) or {}
        try:
            tid = services.create_task(
                g.user["id"],
                data.get("title"),
                data.get("description", ""),
                data.get("priority", "media"),
                data.get("due_date"),
            )
        except ValidationError as err:
            return jsonify(error=str(err)), 400
        return jsonify(dict(services.get_task(tid, g.user["id"]))), 201

    @app.get("/api/tasks/<int:task_id>")
    @login_required
    def api_get(task_id):
        task = services.get_task(task_id, g.user["id"])
        if task is None:
            return jsonify(error="Tarea no encontrada"), 404
        return jsonify(dict(task))

    @app.put("/api/tasks/<int:task_id>")
    @login_required
    def api_update(task_id):
        data = request.get_json(silent=True) or {}
        try:
            ok = services.update_task(
                task_id,
                g.user["id"],
                data.get("title"),
                data.get("description", ""),
                data.get("priority", "media"),
                data.get("due_date"),
                data.get("done", False),
            )
        except ValidationError as err:
            return jsonify(error=str(err)), 400
        if not ok:
            return jsonify(error="Tarea no encontrada"), 404
        return jsonify(dict(services.get_task(task_id, g.user["id"])))

    @app.delete("/api/tasks/<int:task_id>")
    @login_required
    def api_delete(task_id):
        if not services.delete_task(task_id, g.user["id"]):
            return jsonify(error="Tarea no encontrada"), 404
        return "", 204

    @app.get("/api/stats")
    @login_required
    def api_stats():
        return jsonify(services.task_stats(g.user["id"]))

    return app
