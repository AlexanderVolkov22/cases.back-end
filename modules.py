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


async def getinfo(token):
    db = await aiosqlite.connect('base.sqlite')
    c = await db.execute("SELECT shop_id, shop_name, shop_url FROM `shops` WHERE token LIKE ?", [token])
    r = await c.fetchall()
    if r == []:
        resp = "Wrong Token!"
        return resp
    else:
        r = str(r)
        r = r.replace("[(", "")
        r = r.replace(")]", "")
        r = r.replace(", ", ":")
        resp = r.replace("'", "")
        return resp


async def chktoken(token):
    db = await aiosqlite.connect('base.sqlite')
    c = await db.execute("SELECT shop_name FROM `shops` WHERE token LIKE ?", [token])
    r = await c.fetchall()
    if r == []:
        resp = "Wrong Token!"
        return resp
    else:
        resp = r
        return resp


async def addcasemodule(data):
    item = data.split(':')[-3]
    weight = data.split(':')[-2]
    case = data.split(':')[-1]
    db = await aiosqlite.connect('base.sqlite')
    c = await db.execute("SELECT case_name FROM `cases` WHERE case_name LIKE ?", [case])
    r = await c.fetchall()
    if r == []:
        resp = data + ":New Case"
        await db.execute("INSERT INTO cases VALUES(?,?,?)", (item, weight, case))
        await db.commit()
        return resp
    else:
        print(r)
        r = str(r)
        r = r.replace("[('", "")
        r = r.replace("'", "")
        r = r.replace(",)]", "")
        if r == case:
            resp = "Case exists!"
            return resp
        else:
            await db.execute("INSERT INTO cases VALUES(?,?,?)", (item, weight, case))
            await db.commit()
            resp = data
            return resp
