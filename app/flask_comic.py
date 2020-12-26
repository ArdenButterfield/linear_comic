import flask
import logging

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

app = flask.Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# Disable cache-ing, so CSS actually updates whenever I change it.

app.secret_key = "Not a secret, for now"

max_panels = 49

@app.route("/")
def index():
    app.logger.debug("Sending index page")
    return flask.render_template("index.html")

@app.route("/parasite")
def parasite():
    app.logger.debug("Sending Parasite page")
    return flask.render_template("parasite.html")

@app.route("/linear")
def comic():
    return flask.redirect("/linear/0")

@app.route("/linear/<int:panel_num>")
def show_panel(panel_num):

    if panel_num < 0 or panel_num > max_panels:
        app.logger.debug(f"{panel_num} is an invalid value. Aborting.")
        flask.abort(404)

    next_panel = min(panel_num + 1, max_panels)
    prev_panel = max(panel_num - 1, 0)

    # We won't display prev button if first page, or next button if last page
    first_panel = (panel_num == 0)
    last_panel = (panel_num == max_panels)

    if panel_num == 0:
        image_file = "linearalgebrapanelstitle.jpg"
    else:
        image_file = f"linearalgebrapanels{panel_num}.jpg"

    app.logger.debug(f"panel: {panel_num}, prev: {prev_panel}, next: {next_panel}, first: {first_panel}, last: {last_panel}.")

    return flask.render_template("panel.html", image_file=image_file,
                                 panel_num=panel_num, next_panel=next_panel, prev_panel=prev_panel,
                                 first_panel=first_panel,last_panel=last_panel)

app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print(f"Opening for global access on port {5000}")
    app.run(port=5000, host="0.0.0.0")