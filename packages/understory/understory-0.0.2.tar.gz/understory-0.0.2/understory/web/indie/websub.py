"""WebSub hub and subscriber apps."""

from understory import web
from understory.web import tx


hub = web.application("WebSubHub", mount_prefix="hub", db=False)
subscribers = web.application("WebSubSubscribers", mount_prefix="subscribers",
                              db=False)


def wrap_hub(handler, app):
    """Ensure server links are in head of root document."""
    yield
    if tx.request.uri.path == "" and tx.response.body:
        doc = web.parse(tx.response.body)
        try:
            head = doc.select("head")[0]
        except IndexError:
            pass
        else:
            head.append("<link rel=self href=/>")
            head.append("<link rel=hub href=/hub>")
            tx.response.body = doc.html
        web.header("Link", '</>; rel="self"', add=True)
        web.header("Link", '</hub>; rel="hub"', add=True)


@hub.route(r"")
class Hub:
    """."""

    def _get(self):
        return "hub.."


@subscribers.route(r"")
class Subscriptions:
    """."""

    def _get(self):
        return "subscriptions.."
