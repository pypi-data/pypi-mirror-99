##################################
#提供基于api gateway kong的JWT认证和cookie认证
#认证失败时返回401
#################################
from mwauth.base_auth import BaseAuth,User
from flask import request,make_response,g,current_app,session
from functools import wraps
from .redis_session import RedisSessionInterface
import hashlib
class KongAuth(BaseAuth):
    # '''
    # 1，在request前提取 user info
    # '''
    def __set_auth(self):
        '''
        保存用户，jwt等auth info
        :return:
        '''
        if not isinstance(current_app.session_interface,RedisSessionInterface):
            raise Exception('请在app/__init__.py的create_app_swagger方法中增加下列代码：\n app.session_interface = RedisSessionInterface(app, rds)')
        if current_app.config.get('DEVELOPMENT', False):
            g.user_name = current_app.config.get('LOGIN_USER_NAME')  # 'user_dev'
            g.user_id = current_app.config.get('LOGIN_USER_ID')
            g.current_user = User(uid=current_app.config.get('LOGIN_USER_ID'),
                                  uname=current_app.config.get('LOGIN_USER_NAME'),
                                  systemuser=current_app.config.get('LOGIN_USER_SYSTEMUSER', False),
                                  manageuser=current_app.config.get('LOGIN_USER_MANAGEUSER', False),
                                  manageuserid=current_app.config.get('LOGIN_USER_MANAGEUSER_ID'),
                                  companyid=current_app.config.get('LOGIN_USER_COMPANYID',''))
            g.jwt = session.sid
            session.update({'uid':g.current_user.uid,'uname':g.current_user.uname,
                            'systemuser':g.current_user.systemuser,
                            'manageuser':g.current_user.manageuser,
                            'manageuserid':g.current_user.manageuserid})
            return
        # 通过了jwt 认证的 api 一定会回传username和userid，否则视为kong的认证不成功
        g.user_name = request.headers.get('X-Consumer-Username')
        g.user_id = request.headers.get('X-Consumer-Custom-Id')
        # key auth 或jwt auth
        g.jwt = request.args.get('jwt') or request.args.get('apikey')or request.args.get('sessionid') or request.args.get('token')
        if g.jwt is None:
            # jwt header authorization: bearer jwt...
            jwt = request.headers.get('authorization', None)
            if jwt:
                # 去掉前面的bearer
                g.jwt = jwt[7:]
            elif session:
                g.jwt = session.sid
                # session 认证可能不经过kong，但也需保证auth 成功，确保代码兼容
                g.user_name = session.get('uname')
                g.user_id = session.get('uid')
            else:
                # header，query，和cookie中都没有 jwt or sessionid or token or apikey，需要重新认证
                g.user_name = None
                g.user_id = None
                return
        elif session and session.sid!=g.jwt:
            # 如果有传jwt ，就使用jwt的，cookie中的session可能是上一次的，需刷新为jwt的
            session.sid = g.jwt
            mysession = current_app.session_interface.get_session(g.jwt)
            session.update(dict(mysession))
        if not session:
            # 当非session认证时，还需保存session，保证app中的代码的兼容性
            session.sid = g.jwt
            # 临时session 不需要送cookie，避免浪费流量
            session.seend_cookie = False
            mysession = current_app.session_interface.get_session(g.jwt)
            # 如果只通过了Kong 认证，且没有在redis中存该session key ，如：key auth，则写入kong 认证的信息给session
            if request.headers.get('X-Consumer-Username') and request.headers.get('X-Consumer-Custom-Id') and not mysession:
                session.update(dict({'uid':g.user_id ,'uname':g.user_name,
                            'systemuser':False,
                            'manageuser':False,
                            'manageuserid':''}))
            else:
                session.update(dict(mysession))
        g.current_user = User(uid=session.get('uid'),
                              uname=session.get('uname'),
                              systemuser=session.get('systemuser', False),
                              manageuser=session.get('manageuser', False),
                              manageuserid=session.get('manageuserid'),
                              companyid=session.get('companyid',''))
        g.user_name = session.get('uname')
        g.user_id = session.get('uid')


    def __init__(self, app=None):
        super(KongAuth, self).__init__()
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        app.auth = self
        # self.app.register_blueprint(auth)

    def valid_login(self, func):
        @wraps(func)
        def _request_login(*args, **kw):
            # 给g 赋 用户等信息
            self.__set_auth()
            if g.user_name or g.user_id :
                return func(*args, **kw)
            # 没有认证则返回401
            response = make_response()
            response.status_code = 401
            return response
        return _request_login

    def valid_sign(self,func):
        @wraps(func)
        def _request_sign(*args, **kw):
            # json.dumps(json_body)+token+noncestr+timestamp 转md5
            sign = request.headers.get('X-MW-Sign') or request.args.get("sign")
            sign_source_str = f'{request.data.decode()}{g.jwt}' \
                              f'{request.headers.get("X-MW-Noncestr") or request.args.get("noncestr", "")}' \
                              f'{request.headers.get("X-MW-Timestamp") or request.args.get("timestamp", "")}'
            sign_md5 = hashlib.md5(sign_source_str.encode()).hexdigest()
            if sign_md5 == sign:
                return func(*args, **kw)
            # 没有认证则返回400
            response = make_response({ "error": f'sign error,sign:{sign},noncestr:{request.args.get("noncestr", "")},'
                                                f'timestamp:{request.args.get("timestamp", "")}'},
                                     400, {"content-type": "application/json;charset=utf8"})
            response.status_code = 400
            return response
        return _request_sign



