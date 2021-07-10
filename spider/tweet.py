#!/usr/bin/env python3

import twint
import html
import traceback
from config import ROOT
from os.path import join, exists
from os import makedirs
import re

HTTP = re.compile(r'https?:\/\/[^\s]+', flags=re.MULTILINE)
TWITTER_USERNAME_RE = re.compile(r'@([A-Za-z0-9_]+)')

TXT = join(ROOT,"txt/tweet")
makedirs(TXT,exist_ok=True)

EXIST = set()

def fetch_user(username):
  EXIST.add(username)

  out = join(TXT,username+".txt")
  if exists(out):
    return

  c = twint.Config()

  c.Username = username
  c.Store_object = True
  c.Limit = 10000
  twint.run.Search(c)
  tweets = twint.output.tweets_list

  with open(out,"w") as f:
    for i in tweets:
      if i.type == "tweet":
        tweet = html.unescape(i.tweet)

        for user in TWITTER_USERNAME_RE.findall(tweet):
          if user not in EXIST:
            EXIST.add(user)
            yield user

        tweet = TWITTER_USERNAME_RE.sub("", tweet)
        tweet = HTTP.sub("https://", tweet).strip()
        if tweet:
          f.write(tweet+"\n")

from fire import Fire

@Fire
def main(first="sagacity"):
  tofetch = [first]

  while 1:

    if not tofetch:
      return

    username = tofetch.pop()

    try:
      for i in fetch_user(username):
        print(i)
        if len(tofetch) < 1024:
          tofetch.append(i)
    except Exception:
      traceback.print_exc()

