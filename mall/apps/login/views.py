from urllib.parse import urlencode
# Create your views here.
import wego
from django.http import HttpResponse
from wego import WeChatApi as WeixinWeChatApi
from mall import settings


# 重写父类的get_code_url方法
class WeChatApi(WeixinWeChatApi):
    def get_code_url(self, redirect_url, state):
        # base_url
        base_url = "https://open.weixin.qq.com/connect/qrconnect?"
        # 将微信文档规定的参数放在字典中
        params = {
            'appid': settings.WEIXIN_APP_ID,
            'redirect_uri': settings.WEIXIN_REGISTER_URL,
            'response_type': 'code',
            'scope': 'snsapi_login',
            'state':settings.WEIXIN_STATE
        }
        # 使用urlencode将query字典转换为url路径中的查询字符串
        auth_url = base_url + urlencode(params) + "#wechat_redirect"
        return auth_url


wego.WeChatApi = WeChatApi
# wego 初始化, 对应信息可以登录微信公众平台获取
w = wego.init(
    # 应用ID (开发 -> 基本配置)
    APP_ID='wxb50677cc17a892c1',
    # 应用密钥 (开发 -> 基本配置)
    APP_SECRET='796c98b2368811b7baaed4209f363323',
    # 注册域名, 微信公众平台左侧: 接口权限-> 网页授权获取用户基本信息内配置, 需加上 http(s):// 以 / 结尾
    REGISTER_URL='http://test.wegox.net/',
    # WEGO 助手
    HELPER='wego.helpers.official.DjangoHelper',
    # 用户信息缓存过期时间, 单位秒
    USERINFO_EXPIRE=86400,
    )

@w.login_required
def login(request):
    nickname = request.wx_user.nickname
    return HttpResponse(nickname)


