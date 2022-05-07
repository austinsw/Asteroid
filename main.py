import flask
from flask import request
import json
from itertools import groupby
app = flask.Flask(__name__)

output = []

def RmChar(s, i):
  l = list(s)
  del(l[i])
  return "".join(l)

def multi(size):
  if size <= 6: return size
  elif size >= 10: return size * 2
  else: return size * 1.5

def getScore(s):
  i = 0
  Highest = 0
  Origin = 0
  for c in s:
    new_str = RmChar(s,i)
    score = 1
    groups = groupby(new_str)
    ast = [(label, sum(1 for _ in group)) for label, group in groups]
    #print(ast)
    idx = 0
    detail = {}
    for a in ast:
      detail[idx] = a
      idx += 1
    #print(detail)
    key = 0
    new_pos = i
    for label, count in ast:
      #print(label, count)
      new_pos -= count
      if new_pos <= 0: 
        a = label
        size = count
        score += multi(size)
        break
      else: key += 1
    #print("key", key)
    n = 1
    while (True):
      try: 
        L_letter, L_size = detail[key-n]
        R_letter, R_size = detail[key+n]
        if L_letter == R_letter:
          size = L_size + R_size
          score += multi(size)
          n += 1
        else: break
      except: break
    if Highest < score:
      Highest = score
      Origin = i
    i += 1
    #print(Highest, Origin)
    #print("score", score)
  return int(Highest), Origin

@app.route("/")
def index():
  return "Hello, world!"

@app.route("/asteroid", methods=["POST"])
def asteroid():
  inputJson = request.get_json()
  tests = inputJson.get("test_cases")
  for test in tests:
    HighestScore, Origin = getScore(test)
    result = {}
    result["input"] = test
    result["score"] = HighestScore
    result["origin"] = Origin
    output.append(result)
  #print(output)
  return json.dumps(output)

app.run(host = '0.0.0.0', port = 8080)