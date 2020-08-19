import aiohttp
import json
import aiohttp_jinja2

async def about(request):
    app=request.app
    app['log'].info('open main page')
    data={}
    response = aiohttp_jinja2.render_template('main.html', request, data)
    return response


async def task(app):
    pass

async def curl(url, method='GET', data=None,headers=None):
    if not headers:
        headers={}
        headers["Content-Type"] = "application/json"
    async with aiohttp.ClientSession(headers=headers) as session:
        if method == 'GET':
            async with session.get(url)as response:
                chunk = await response.json()
        else:
            async with session.post(url, data=json.dumps(data)) as response:
                chunk = await response.json()
        return chunk
