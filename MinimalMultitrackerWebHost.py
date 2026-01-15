
import itertools
import datetime
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler, HTTPStatus
from threading import Thread

from settings import get_settings

def start_minimal_multitracker_web_host(ctx):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(HTTPStatus.OK)
            self.end_headers()
            self.wfile.write(render(ctx).encode("utf8"))
        def log_message(self, format, *args):
            pass # Silence please
    main_port = get_settings().server_options.port
    port = main_port - 38281 + 1231
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    def run():
        print("serving: http://0.0.0.0:{}/".format(port))
        server.serve_forever()
    Thread(target=run, daemon=True).start()

template = """\
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf8">
  </head>
  <body>
    <p>This page is designed to provide information for <a href="https://cheesetrackers.theincrediblewheelofchee.se/">Cheese Trackers</a>. You, a human, may look at it too if you like, although it's optimized for machines to read.</p>
    <table id=checks-table>
      <thead><tr><th>#</th><th>Name</th><th>Game</th><th>Status</th><th>Checks</th><th>&percnt;</th><th>Last<br>Activity</th></tr></thead>
      <tbody>{checks_body}</tbody>
    </table>
    <table id=hints-table>
      <thead><tr><th>Finder</th><th>Receiver</th><th>Item</th><th>Location</th><th>Game</th><th>Entrance</th><th>Found</th></tr></thead>
      <tbody>{hints_body}</tbody>
    </table>
  </body>
</html>
"""

def render(ctx):
    return template.format(
        checks_body="".join(check_template.format(**check_info) for check_info in get_check_infos(ctx)),
        hints_body="".join(hint_template.format(**hint) for hint in get_hints(ctx)),
    )

check_template = """
  <tr>
    <td><a href="#">{n}</a></td>
    <td>{name}</td>
    <td>{game}</td>
    <td>{status}</td>
    <td>{found}/{total}</td>
    <td>{percent}</td>
    <td>{last_activity}</td>
  </tr>
"""
def get_check_infos(ctx):
    for slot_id, slot_info in ctx.slot_info.items():
        team_id = 0 # teams are only partially implemented.
        try:
            last_activity = (
                datetime.datetime.utcnow() -
                datetime.datetime.utcfromtimestamp(ctx.client_activity_timers[(team_id, slot_id)].timestamp())
            ).total_seconds()
        except KeyError:
            last_activity = "None"
        yield dict(
            n=slot_id,
            name=slot_info.name,
            game=slot_info.game,
            status={
                # This mapping is copied from the multitracker.html templating logic.
                0: "Disconnected",
                5: "Connected",
                10: "Ready",
                20: "Playing",
                30: "Goal Completed"
            }.get(ctx.client_game_state[(team_id, slot_id)], "Unknown State"),
            found=len(ctx.location_checks[(team_id, slot_id)]),
            total=len(ctx.locations[slot_id]),
            percent="-", # i don't think this is needed. do the division yourself.
            last_activity=last_activity,
        )

hint_template = """
  <tr>
    <td>{finder}</td>
    <td>{receiver}</td>
    <td>{item}</td>
    <td>{location}</td>
    <td>{game}</td>
    <td>{entrance}</td>
    <td>{found}</td>
  </tr>
"""
def get_hints(ctx):
    for hint in set(itertools.chain(*ctx.hints.values())):
        game = ctx.slot_info[hint.finding_player].game
        yield dict(
            finder=ctx.slot_info[hint.finding_player].name,
            receiver=ctx.slot_info[hint.receiving_player].name,
            item=ctx.item_names[ctx.slot_info[hint.receiving_player].game][hint.item],
            location=ctx.location_names[game][hint.location],
            game=game,
            entrance=hint.entrance or "Vanilla",
            found="✔" if hint.found else "",
        )
