import flask
import logging

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

app = flask.Flask(__name__)

# Disable cache-ing, so CSS actually updates whenever I change it.
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Run on port 5000
PORT_NUM = 5000

app.secret_key = "Not a secret, for now"

# Number of panels in the Epic.
MAX_PANELS = 59

@app.route("/")
def index():
    app.logger.debug("Sending index page")
    return flask.render_template("index.html", current_page="Home")


@app.route("/parasite/")
def parasite():
    app.logger.debug("Sending Parasite page")
    return flask.render_template("parasite.html", current_page="Parasite")


@app.route("/linear/")
def comic():
    return flask.redirect("/linear/0/")


@app.route("/more/")
def misc():
    # Fetch the filenames for the comics on the More page
    more_comics_list = []
    with open("more_comics.txt", "r") as more_comics_file:
        for line in more_comics_file:
            if line[0] != "#" and not line.isspace():
                more_comics_list.append(line.strip())
    app.logger.debug("Sending more comics page")
    return flask.render_template("more.html", images=more_comics_list,
                                 list_len=len(more_comics_list),current_page="More")


@app.route("/linear/<int:panel_num>/")
def show_panel(panel_num):

    if panel_num < 0 or panel_num > MAX_PANELS:
        app.logger.debug(f"{panel_num} is an invalid value. Aborting.")
        flask.abort(404)

    # We won't display prev button if first page, or next button if last page
    is_first_panel = (panel_num == 0)
    is_last_panel = (panel_num == MAX_PANELS)

    if panel_num == 0:
        image_file = "linearalgebrapanelstitle.jpg"
    else:
        image_file = f"linearalgebrapanels{panel_num}.jpg"

    app.logger.debug(f"Sending comic: panel: {panel_num}, is_first_panel: {is_first_panel}, "
                     f"is_last_panel: {is_last_panel}.")

    return flask.render_template("panel.html", image_file=image_file, panel_num=panel_num,
                                 is_first_panel=is_first_panel,is_last_panel=is_last_panel,current_page="Linear")


app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print(f"Opening for global access on port {PORT_NUM}")
    app.run(port=PORT_NUM, host="0.0.0.0")
