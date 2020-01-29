import ast
import random
import secrets

import aiosqlite
import numpy as np


async def caserand(case):
    db = await aiosqlite.connect('base.sqlite')
    print(case)
    c = await db.execute("SELECT item FROM cases WHERE case_name LIKE ?", [case])
    items = await c.fetchall()
    c = await db.execute("SELECT weight FROM cases WHERE case_name LIKE ?", [case])
    weights = await c.fetchall()
    if weights == []:
        resp = "Wrong Case!"
        return resp
    else:
        items = str(items)
        items = items.replace("(", "")
        items = items.replace(",)", "")
        items = items.replace(",)", "")
        items = items.replace("(", "")
        weights = str(weights)
        weights = weights.replace("(", "")
        weights = weights.replace(",)", "")
        weights = weights.replace("'", "")
        items = ast.literal_eval(items)
        weights = ast.literal_eval(weights)
        print(weights)
        print(items)
        item = random.choices(items, weights)
        item = str(item)
        item = item.replace("['", "")
        item = item.replace("']", "")
        print(item)
        resp = item
        return resp