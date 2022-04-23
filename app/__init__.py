# encoding: utf-8
"""
@author: lileilei
@site: 
@file: __init__.py
@time: 2017/7/13 16:38
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from config import lod
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from config import jobstores, executors
from flask_admin import Admin
from flask_moment import Moment
from flask_restplus import Api, reqparse

from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

pagination_arguments = reqparse.RequestParser()
pagination_arguments.add_argument('page', type=int, required=False, default=1, help='Page number')
api = Api(version='1.0', title='系统api',
          description='系统对外api', doc='/api', license_url="/api")
app = Flask(__name__)
conf = lod()
api.init_app(app)
loginManager = LoginManager(app)
app.config.from_object(conf)
bootstrap = Bootstrap(app)
loginManager.session_protection = "strong"
loginManager.login_view = 'home.login'
loginManager.login_message = u'FXTest测试平台必须登录，请登录您的FXTest平台账号！'
db = SQLAlchemy(app)
moment = Moment(app)
admin = Admin(app, name=u'FXTest系统管理后台')
from app import views, models, url, apiadmin


def listerner(event):
    if event.exception:
        print('任务出错了！')
    else:
        print('任务正常运行中...')


sched = BackgroundScheduler(jobstores=jobstores, executors=executors)
sched.add_listener(listerner, EVENT_JOB_ERROR | EVENT_JOB_EXECUTED)

try:
    sched.start()
except Exception as e:
    print(e)
