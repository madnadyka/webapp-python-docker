import aiohttp
import aiohttp.web
import model



def setup_middlewares(app):
     app.middlewares.append(session_factory)


async def session_factory(app, next_handler):
     async def middleware(request):
         log = request.app['log']

         def check_path(path):
             result = False
             if path=='/login':
                 return result
             for r in ['/admin']:
                     if path.startswith(r):
                        result = True
                        break
             return result

         if not check_path(request.path):
             response = await next_handler(request)
             return response
             # process other requests
         conn = False
         try:
             # sid = request.cookies['sid']
             # user_id=await model.select_user_session(sid, app['db_pool'])
             # if user_id:
             #     await model.update_user_session(sid, app['db_pool'])
             # else:
             #     raise Exception('session invalid')
             try:
                 response = await next_handler(request)
             except:
                 response = aiohttp.web.HTTPFound('/')

             return response
         except:
             response = aiohttp.web.HTTPFound('/login')
             return response
         finally:
             if conn: conn.close()

     return middleware

