# Fraunhofer data feed parser bots

## Source

The source feed provides a stream of newline separated JSON objects.
Each line represents a single event observed by DDoS C&C trackers, e.g. attack
commands. The feed can be retrieved with either the generic HTTP Stream
Collector Bot for a streaming live feed or with the generic HTTP Collector Bot
for a polled feed.

## The Bots

The parser bots generate c&c events and ddos events, depending on the
information retrieved from the feed. The feed delivers reports with different
message types and different C&C types based on the type of tracked C&C servers
and the type of commands received. If the c&c parser bot receives a report with
a known C&C type but with an unknown message type, it generates a C&C event
with an adjusted feed.accuracy given by the parameter
unknown_messagetype_accuracy, if set. This feature can be used to lower the
accuracy of events in case of unknown behavior of the tracked C&Cs, while
keeping a high accuracy otherwise. For this feature to work, set the default
feed.accuracy of the collector bot feeding this parser bot to a high value,
while setting the value of the c&c parser bot's unknown_messagetype_accuracy
to a lower value. The c&c parser bot will not change the feed.accuracy value
if the tracker was able to interpret the C&C communication, giving a high
chance, that the tracked server is actually a real live C&C server.
If the tracker was not able to completely interpret the C&C communication, the
feed.accuracy will be set to the lower value of the
unknown_messagetype_accuracy parameter. There is still a certain probability
that the tracked server is a real C&C, but it could not be confirmed.
The target parser bot generates one ddos event for every target found in the
attack commands of the tracked C&C server, which could be more than one for a
single event from the tracker feed. 

### Parameters

 * unknown_messagetype_accuracy: A float between 0 an 100 representing the
 accuracy of a c&c event for reports with unknown message types. Replaces the
 feed.accuracy with the given value for these events.
