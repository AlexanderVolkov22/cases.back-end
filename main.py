import secrets

from aiogram.utils import json
from aiohttp import web
import aiosqlite

import modules


async def case1(request):
    resp_obj = {'status': 'ok'}
    return web.Response(text=json.dumps(resp_obj))


async def help(request):
    return web.Response(text="https://github.com/AlexanderVolkov22/cases.back-end/blob/master/README.md")


async def api_get_me(request):
    db = await aiosqlite.connect('base.sqlite')
    token = request.match_info['token']
    c = await db.execute("SELECT shop_id, shop_name, shop_url FROM `shops` WHERE token LIKE ?", [token])
    r = await c.fetchall()
    if r == []:
        resp_obj = {'status': 'Wrong Token!'}
        return web.Response(text=json.dumps(resp_obj))
    else:
        r = str(r)
        r = r.replace("[(", "")
        r = r.replace(")]", "")
        r = r.replace(", ", ":")
        r = r.replace("'", "")
        shop_url = r.split(':')[-1]
        shop_name = r.split(':')[-2]
        shop_id = r.split(':')[-3]
        resp_obj = {'status': 'ok', 'shop_id': shop_id, 'shop_name': shop_name, 'shop_url': shop_url}
        return web.Response(text=json.dumps(resp_obj))


async def opencase(request):
    db = await aiosqlite.connect('base.sqlite')
    token = request.match_info['token']
    c = await db.execute("SELECT shop_name FROM `shops` WHERE token LIKE ?", [token])
    r = await c.fetchall()
    if r == []:
        resp_obj = {'status': 'Wrong Token!'}
        return web.Response(text=json.dumps(resp_obj))
    else:
        case = request.match_info['case']
        resp = await modules.caserand(case)
        if resp == "Wrong Case!":
            resp_obj = {'status': 'Wrong Case!'}
            return web.Response(text=json.dumps(resp_obj))
        else:
            resp_obj = {'status': 'ok', 'case':case, 'item':resp}
            return web.Response(text=json.dumps(resp_obj))



app = web.Application()
app.add_routes([web.get('/', case1)])
app.add_routes([web.get('/help', help)])
app.add_routes([web.get('/{token}/get_me', api_get_me)])
app.add_routes([web.get('/{token}/open/{case}', opencase)])
web.run_app(app)
