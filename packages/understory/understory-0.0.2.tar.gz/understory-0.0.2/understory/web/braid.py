"""Braid support."""

import time

from gevent import spawn
from gevent.queue import Queue
import requests

from .framework.util import header, tx, json, JSONEncoder, Headers
from .response import OK, NoContent, Subscription

__all__ = ["publish", "subscribe", "braidify"]


def publish(url, patch_range, patch_body):
    """Publish a patch to a local or web resource using Braid."""
    if url.startswith("/"):
        tx.kv.db.publish(url, JSONEncoder().encode({"range": patch_range,
                                                    "body": patch_body}))
    else:
        requests.put(url, json={"Patches": 1})  # TODO


def subscribe(url):
    """Subscribe to a web resource using Braid."""
    return requests.get(url, headers={"Subscribe": "keep-alive"}, stream=True)


def multi_subscribe(path, *urls):
    """Yield patches from multiple subscriptions."""
    queue = Queue()

    def producer(url):
        def _producer():
            for patch in subscribe(url):
                queue.put_nowait(patch)
            queue.put_nowait("COMPLETED")
        return _producer

    for url in urls:
        spawn(producer(url))
    completed = 0
    while True:
        patch = queue.get(timeout=5)
        if patch == "COMPLETED":
            completed += 1
            if completed == len(urls):
                break
            continue
        tx.kv.db.publish(path, patch)
        # XXX yield patch + b"\n"


def braidify(handler, app):
    """Handle Braid Pub/Sub."""
    path = f"/{tx.request.uri.path}"
    method = tx.request.method
    headers = tx.request.headers
    controller = tx.request.controller
    if method == "OPTIONS":  # allow CORS FIXME secure with IndieAuth?
        header("Access-Control-Allow-Origin", "*")
        header("Access-Control-Allow-Methods", "GET,PUT")
        header("Access-Control-Allow-Headers",
               "credentials,subscribe,patches,client")
        header("Vary", "Origin")
        raise NoContent()
    if method == "GET" and headers.get("Subscribe") == "keep-alive":
        header("Access-Control-Allow-Origin", "*")
        header("Subscribe", "keep-alive")
        header("Content-Type", "application/json")
        header("X-Accel-Buffering", "no")
        try:
            subscription = controller._subscribe()
        except AttributeError:
            subscription = Braid(path)
        tx.response.naked = True
        raise Subscription(subscription)
    if method == "PUT" and headers.get("Patches"):
        # TODO handle multiple patches
        raw_headers, _, patch_body = tx.request.body.decode().partition("\n\n")
        patch_headers = Headers.from_lines(raw_headers)
        # version = patch_headers.get("version")
        # parents = patch_headers.get("parents")
        # merge_type = patch_headers.get("merge-type")
        patches = [(patch_headers, patch_body)]
        # TODO add patch to db for current path, give version hash
        # TODO merge patch and cache current in kv
        for patch_headers, patch_body in patches:
            print(patch_headers)
            print(patch_body)
            print()
            patch_range = str(patch_headers["content-range"]).partition("=")[2]
            publish(path, patch_range, json.loads(patch_body))
        header("Access-Control-Allow-Origin", "*")
        header("Patches", "OK")
        raise OK(b"")
    yield


class Braid:
    """A Braid subscription."""

    def __init__(self, path):
        """Create Redis subscription to resource at given path."""
        self.p = tx.kv.pubsub(ignore_subscribe_messages=True)
        self.p.subscribe(path)

    def __next__(self):
        """Serve patches to client when received from Redis subscription."""
        while True:
            message = self.p.get_message()
            if message is None:
                time.sleep(0.001)
                continue
            patch = json.loads(message["data"])
            body = JSONEncoder().encode(patch["body"])
            return bytes(f"Content-Length: {len(body)}\n"
                         f"Content-Range: json={patch['range']}\n"
                         f"\n"
                         f"{body}\n"
                         f"\n", "utf-8")

    def __iter__(self):  # TODO XXX use iter() on Braid object above?
        """Identify and function as an iterator."""
        return self
