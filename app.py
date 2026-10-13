from datetime import datetime
from flask import Flask, render_template, request
import pytz

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    current_times = {}
    converted_result = None

    # Common global timezones for quick checking
    zones = ["Asia/Kolkata", "UTC", "America/New_York", "Europe/London", "Asia/Tokyo"]
    for zone in zones:
        try:
            tz = pytz.timezone(zone)
            current_times[zone] = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S %Z")
        except Exception:
            pass

    all_timezones = sorted(pytz.all_timezones)

    if request.method == "POST":
        time_str = request.form.get("time_input")
        from_tz = request.form.get("from_tz")
        to_tz = request.form.get("to_tz")

        try:
            naive_dt = datetime.strptime(time_str, "%Y-%m-%dT%H:%M")
            source_tz = pytz.timezone(from_tz)
            target_tz = pytz.timezone(to_tz)

            localized_dt = source_tz.localize(naive_dt)
            target_dt = localized_dt.astimezone(target_tz)

            converted_result = {
                "original": localized_dt.strftime("%Y-%m-%d %H:%M:%S %Z"),
                "converted": target_dt.strftime("%Y-%m-%d %H:%M:%S %Z"),
            }
        except Exception as e:
            converted_result = {"error": str(e)}

    return render_template(
        "index.html",
        current_times=current_times,
        all_timezones=all_timezones,
        converted_result=converted_result,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
