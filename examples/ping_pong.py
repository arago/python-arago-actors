#!/usr/bin/env python3
from gevent import monkey; monkey.patch_all()
from arago.actors import Actor, Root
import arago.actors.pattern_matching as matching
import logging

logger = logging.getLogger('root')

class PingPong(Actor):
	def serve(self, opponent):
		opponent.tell("Ping", sender=self)

	@matching.match(msg = "Ping", sender = matching.isoftype(Actor))
	def handle(self, msg, payload, sender):
		sender.tell("Pong")

	@matching.match(msg = "Pong", sender = matching.isoftype(Actor))
	def handle(self, msg, payload, sender):
		sender.tell("Ping")

	@matching.default
	def handle(self, msg, payload, sender):
		pass

players = [PingPong(name="Player One"), PingPong(name="Player Two")]

players[0].serve(opponent=players[1])

Root(name="root", children=players)
