#!/usr/bin/python

import argparse
import re
from prettytable import PrettyTable



def cap(s, l):
    return s if len(s)<=l else s[0:l-3]+'...'

import math
def wrap_always(text, width):
    return '\n'.join([ text[width*i:width*(i+1)] \
					  for i in range(int(math.ceil(1.*len(text)/width))) ])


parser = argparse.ArgumentParser()
parser.add_argument("-s", "--server", help="Filter mail incoming from server")
parser.add_argument("-f", "--sender", help="Filter mail from")
parser.add_argument("-t", "--recipient", help="Filter mail to")
parser.add_argument("-r", "--relay_host", help="Filter mail relayed to host")
parser.add_argument("-l", "--logfile", help="Logfile to search", default="/var/log/maillog")
args = parser.parse_args()

if args.server is None and args.recipient is None and args.relay_host is None and args.sender is None:
	parser.error('No action requested')

search_tokens = []
messages_dict = {}

id_regex = re.compile (" [A-F0-9]{7,10}")

client_regex = re.compile (".* client=(.*)$")

from_regex = re.compile (".* from=<(.*?)>, ")

to_regex = re.compile (".* to=<(.*?)>, ")

relay_regex = re.compile (" relay=(.*?(?:\[.*\].?[0-9]*)?), ")

status_regex = re.compile (" status=(.*?) (.*)$")

score_regex = re.compile (" Hits: ([0-9\-\.]+), ")

amavisstatus_regex = re.compile("\([0-9\-]+\)([a-zA-Z\- 0-9]+)")

if args.server:
	search_tokens.append(re.compile(".* client=.*" + args.server + ".*$"))
else:
	search_tokens.append(client_regex)

if args.sender:
	search_tokens.append(re.compile(".* from=<" + args.sender + ">.*"))
	search_tokens.append(re.compile(".*<" + args.sender + "> ->.*"))
elif not args.server:
	search_tokens.append(from_regex)

if args.recipient:
	search_tokens.append(re.compile(".* to=<" + args.recipient + ">.*"))
	search_tokens.append(re.compile(".* -> .*<" + args.recipient + ">.*"))
elif not args.sender and not args.server:
	search_tokens.append(to_regex)

if args.relay_host:
	search_tokens.append(re.compile(".* relay=.*" + args.relay_host + ",.*"))


infile = args.logfile

with open(infile) as f:
	f = f.readlines()

table = PrettyTable(["Message ID", "Status", "From", "To", "Score", "Relay Server", "Sender Server", "Extended Status"])


# Client, from, to + relay
for line in f:
	for phrase in search_tokens:
		if phrase.match(line):
			message_id = None
			message_ids = id_regex.findall(line)
			if message_ids:
				message_id = message_ids[0].lstrip()
				message_id_regex = re.compile(".* " + message_id + "[:,] .*")
				if not message_id_regex in search_tokens:
					if args.server or (args.sender and not client_regex.match(line)) or ((args.recipient or args.relay_host) and (not from_regex.match(line)  and not client_regex.match(line))):
						#print line
						search_tokens.append(message_id_regex)
			if message_id:
				if not message_id in messages_dict:
					messages_dict[message_id] = {}
					messages_dict[message_id]['id'] = message_id
					messages_dict[message_id]['server'] = None
					messages_dict[message_id]['sender'] = None
					messages_dict[message_id]['recipient'] = None
					messages_dict[message_id]['relay'] = None
					messages_dict[message_id]['status'] = None
					messages_dict[message_id]['score'] = "N/A"
				
				client = client_regex.findall(line)
				if client:
					messages_dict[message_id]['server'] = wrap_always(client[0], 14)
					break
				
				sender = from_regex.findall(line)
				if sender:
					messages_dict[message_id]['sender'] = cap(sender[0], 28)
					break
				
				to = to_regex.findall(line)
				if to:
					messages_dict[message_id]['recipient'] = cap(to[0], 28)

				relay = relay_regex.findall(line)
				if relay:
					messages_dict[message_id]['relay'] = wrap_always(relay[0], 16)
					
				score = score_regex.findall(line)
				if score:
					amavisstatus = amavisstatus_regex.findall(line)
					if not amavisstatus:
						amavisstatus = "N/A"
					else:
						amavisstatus = amavisstatus[0].replace(" ", "\n")
					score = "%s\n%s" % (score[0], amavisstatus)
					messages_dict[message_id]['score'] = wrap_always(score, 15).replace("\n\n", "\n")

				status = status_regex.findall(line)
				if status:
					messages_dict[message_id]['status'] = status[0][0]
					messages_dict[message_id]['status_extended'] = wrap_always(status[0][1], 24)
					table.add_row ([messages_dict[message_id]['id'], messages_dict[message_id]['status'], messages_dict[message_id]['sender'], messages_dict[message_id]['recipient'], messages_dict[message_id]['score'], messages_dict[message_id]['relay'], messages_dict[message_id]['server'], messages_dict[message_id]['status_extended']])
					break

			break


print table
