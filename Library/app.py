
import calendar
from datetime import date

from flask import Flask, abort, render_template, request

app = Flask(__name__)

ANNOUNCEMENTS = [
    {
        "title": "FINAL EXAMINATION",
        "date": "NOVEMBER 17-20",
        "details": (
            "All students are encouraged to prepare ahead, review "
            "their lessons, and take note of their examination schedules. "
            "As the semester comes to a close, give your best, stay "
            "focused, and finish strong!"
        ),
        "highlight": (
            "Good luck, UNIANs! May your hard work bring you "
            "the results you deserve."
        ),
        "image": "img/exam.jpg",
        "alt": "Final Examination",
    },
    {
        "title": "INTRAMURALS",
        "date": "OCTOBER 19-22",
        "details": (
            "The Tribu Dalubsahakan remained on their throne "
            "as they won the 2026 Intramurals!"
        ),
        "highlight": "",
        "image": "img/announcements/intrams.jpg",
        "alt": "Intramurals sports event",
    },
]

EVENTS = [
    # {"date": "2026-11-20", "title": "Signing of clearances"},
]

CONTACT = {
    "address": "Address here",
    "email": "Email here",
    "phone": "Phone here",
}

ABOUT = {
    "history": ["Text here", "Text here"],
    "mission": "Text here",
    "vision": "Text here",
    "functions": [
        {"name": "Instruction", "text": "Text here"},
        {"name": "Research", "text": "Text here"},
        {"name": "Production", "text": "Text here"},
        {"name": "Extension", "text": "Text here"},
    ],
}

# UNIVERSITY OF ABRA CAMPUSES



CAMPUSES = {
    "bangued": {
        "name": "Bangued Campus",
        "image": "img/campuses/bangued.jpeg",
        "type": "Extension Campus",
        "location": "Bangued, Abra",
        "description": "The Bangued Campus offers programs in teacher education, arts and sciences, and engineering and industrial technology.",
        "programs": [
            "Teacher Education",
            "Arts and Sciences",
            "English Language",
            "Engineering",
            "Industrial Technology"
        ]
    },

    "lagangilang": {
        "name": "Lagangilang Main Campus",
        "image": "img/campuses/lagangilang.jpeg",
        "type": "Main Campus",
        "location": "Lagangilang, Abra",
        "description": "The main campus offers programs in education, technology, agriculture, forestry, and other fields.",
        "programs": [
            "Teacher Education",
            "Home Technology",
            "Mathematics",
            "Computing Sciences",
            "Agriculture",
            "Forestry",
            "Cooperatives",
            "Fisheries",
            "Hospitality Management"
        ]
    },

    "lapaz": {
        "name": "La Paz Extension Campus",
        "image": "img/campuses/lapaz.jpg",
        "type": "Extension Campus",
        "location": "La Paz, Abra",
        "description": "The La Paz Campus offers programs in criminal justice, social services, and political science.",
        "programs": [
            "Criminology (Criminal Justice)",
            "Social Work",
            "Political Science"
        ]
    }
}




@app.context_processor
def shared():
    return {
        "contact": CONTACT,
        "year": date.today().year
    }


def month_view(year, month):
    events_by_day = {}

    for event in EVENTS:
        d = date.fromisoformat(event["date"])

        if (d.year, d.month) == (year, month):
            events_by_day.setdefault(d.day, []).append(
                event["title"]
            )

    today = date.today()
    weeks = []

    for week in calendar.Calendar(
        firstweekday=6
    ).monthdayscalendar(year, month):

        weeks.append([
            {
                "day": d,
                "events": events_by_day.get(d, []),
                "today": (
                    d != 0 and date(year, month, d) == today
                ),
            }
            for d in week
        ])

    prev_y, prev_m = (
        (year - 1, 12) if month == 1
        else (year, month - 1)
    )

    next_y, next_m = (
        (year + 1, 1) if month == 12
        else (year, month + 1)
    )

    return {
        "label": date(year, month, 1).strftime("%B %Y"),
        "weeks": weeks,
        "prev": f"{prev_y}-{prev_m:02d}",
        "next": f"{next_y}-{next_m:02d}",
        "listing": [
            {"day": d, "title": title}
            for d in sorted(events_by_day)
            for title in events_by_day[d]
        ],
    }


@app.route("/")
def cover():
    return render_template("cover.html")


@app.route("/home")
def home():
    today = date.today()

    try:
        year, month = map(
            int,
            request.args.get("month", "").split("-")
        )
        date(year, month, 1)

    except (ValueError, TypeError):
        year, month = today.year, today.month

    return render_template(
        "home.html",
        announcements=ANNOUNCEMENTS,
        cal=month_view(year, month),
        weekdays=[
            "Sun", "Mon", "Tue", "Wed",
            "Thu", "Fri", "Sat"
        ],
    )


@app.route("/about")
def about():
    return render_template(
        "about.html",
        about=ABOUT
    )


@app.route("/campus")
def campus():
    return render_template(
        "campus.html",
        campuses=CAMPUSES
    )


@app.route("/campus/<campus_slug>")
def campus_detail(campus_slug):
    campus = CAMPUSES.get(campus_slug)

    if campus is None:
        abort(404)

    return render_template("campus_detail.html", campus=campus)

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/student-login")
def student_login():
    return render_template("student_login.html")


@app.route("/admin-login")
def admin_login():
    return render_template("admin_login.html")
if __name__ == "__main__":
    app.run(debug=True)
