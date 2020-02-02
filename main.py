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
    token = request.match_info['token']
    resp = await modules.getinfo(token)
    resp = str(resp)
    if resp == "Wrong Token!":
        resp_obj = {'status': resp}
        return web.Response(text=json.dumps(resp_obj))
    else:
        shop_url = resp.split(':')[-1]
        shop_name = resp.split(':')[-2]
        shop_id = resp.split(':')[-3]
        resp_obj = {'status': 'ok', 'shop_id': shop_id, 'shop_name': shop_name, 'shop_url': shop_url}
        return web.Response(text=json.dumps(resp_obj))


async def opencase(request):
    token = request.match_info['token']
    resp = modules.chktoken(token)
    if resp == "Wrong Token!":
        resp_obj = {'status': resp}
        return web.Response(text=json.dumps(resp_obj))
    else:
        case = request.match_info['case']
        resp = await modules.caserand(case)
        if resp == "Wrong Case!":
            resp_obj = {'status': 'Wrong Case!'}
            return web.Response(text=json.dumps(resp_obj))
        else:
            resp_obj = {'status': 'ok', 'case': case, 'item': resp}
            return web.Response(text=json.dumps(resp_obj))


async def addcase(request):
    token = request.match_info['token']
    resp = await modules.chktoken(token)
    if resp == "Wrong Token!":
        resp_obj = {'status': resp}
        return web.Response(text=json.dumps(resp_obj))
    else:
        item = request.match_info['item']
        weight = request.match_info['weight']
        case = request.match_info['case']
        data = item + ":" + weight + ":" + case
        print(data)
        resp = await modules.addcasemodule(data)
        if resp == "Case exists!":
            resp_obj = {'status': resp}
            return web.Response(text=json.dumps(resp_obj))
        else:
            newcase = resp.split(':')[-1]
            if newcase == "New Case":
                item = resp.split(':')[-4]
                weight = resp.split(':')[-3]
                case = resp.split(':')[-2]
                resp_obj = {'status': 'ok', 'case': case, 'weight': weight, 'item': item}
                return web.Response(text=json.dumps(resp_obj))
            else:
                item = resp.split(':')[-3]
                weight = resp.split(':')[-2]
                case = resp.split(':')[-1]
                resp_obj = {'status': 'ok', 'case': case, 'weight': weight, 'item': item}
                return web.Response(text=json.dumps(resp_obj))


app = web.Application()
app.add_routes([web.get('/', case1)])
app.add_routes([web.get('/help', help)])
app.add_routes([web.get('/{token}/get_me', api_get_me)])
app.add_routes([web.get('/{token}/open/{case}', opencase)])
app.add_routes([web.get('/{token}/add_to/{case}/item/{item}/with/{weight}', addcase)])
web.run_app(app)
