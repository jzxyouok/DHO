# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from models import Fowler, Dialog, Location, Function

from wechat_sdk import WechatConf, WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage, LocationMessage, EventMessage

# 微信SDK配置
conf = WechatConf(token='dfsdsg1g23s1gs53',
                  appid='wxbc1c4c2e398996f7',
                  appsecret='42b511b04df169de9c90e5b9509a1919',
                  encrypt_mode='normal',
                  )
wechat = WechatBasic(conf=conf)


class Weixin(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(Weixin, self).dispatch(*args, **kwargs)

    def get(self, request):
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)

        if wechat.check_signature(signature, timestamp, nonce):
            return HttpResponse(echostr)

    def post(self, request):
        try:
            wechat.parse_data(request.body)
        except ParseError:
            return HttpResponse('Invalid Body Text')

        id = wechat.message.id              # MsgId
        target = wechat.message.target      # ToUserName
        source = wechat.message.source      # FromUserName
        time = wechat.message.time          # CreateTime
        type = wechat.message.type          # MsgType
        raw = wechat.message.raw            # 原始 XML 文本

        # get_or_create会得到一个tuple (object, created)
        fowler = Fowler.objects.get_or_create(OpenID=source)[0]

        if isinstance(wechat.message, TextMessage):
            keywords = [func.keyword for func in Function.objects.all()]
            content = wechat.message.content                # 对应于 XML 中的 Content
            if content in keywords:
                reply = Function.objects.get(keyword=content).explain
            else:
                reply = '本公众号支持的回复有： \n' + ' '.join(keywords)

            dialog = Dialog(message=content, reply=reply, fowler=fowler)
            dialog.save()
            response_xml = wechat.response_text(content=reply, escape=True)
            return HttpResponse(response_xml)

        elif isinstance(wechat.message, LocationMessage):
            location = wechat.message.location              # Tuple(Location_X, Location_Y)
            scale = wechat.message.scale                    # 地图缩放大小
            label = wechat.message.label                    # 地理位置

            loc = Location(fowler=fowler, x=location[0], y=location[1], label=label)
            loc.save()
            response_xml = wechat.response_text(content='已收到您的地理位置')
            return HttpResponse(response_xml)

        elif isinstance(wechat.message, EventMessage):
            if wechat.message.type == 'subscribe':
                fowler.activate = 1
                fowler.save()
                response_xml = wechat.response_text(content='欢迎关注本公众号 具体功能请回复‘功能’')
                return HttpResponse(response_xml)
            elif wechat.message.type == 'unsubscribe':
                fowler.activate = 0
                fowler.save()
        else:
            response_xml = wechat.response_text(content="回复'功能'了解本公众号提供的查询功能")
            return HttpResponse(response_xml)



