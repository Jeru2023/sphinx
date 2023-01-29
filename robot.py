from WorkWeixinRobot.work_weixin_robot import WWXRobot
import configparser as cp

config = cp.ConfigParser()
config.read('sphinx.config', encoding='utf-8-sig')

webhook = config.get('robot', 'webhook')
rbt = WWXRobot(key=webhook)

# 发送一个字符串作为文本消息
def send_text(content): 
    rbt.send_text(content)

'''
content = '\n'.join([
    '# 企业微信群机器人',
    '#### WorkWeixinRobot', 
    '[GitHub地址](https://github.com/seoktaehyeon/work-weixin-robot)'
])

'''
def send_markdown(content):    
    rbt.send_markdown(content=content)