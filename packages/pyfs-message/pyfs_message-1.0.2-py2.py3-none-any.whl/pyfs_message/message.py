# -*- coding: utf-8 -*-

from pyfs_auth import TenantAccessToken, final_tenant_access_token


class Message(TenantAccessToken):
    def __init__(self, appid=None, secret=None, ticket=None, tenant_key=None, token=None, storage=None):
        super(Message, self).__init__(appid=appid, secret=secret, ticket=ticket, tenant_key=tenant_key, token=token, storage=storage)
        # 发送文本消息, Refer: https://open.feishu.cn/document/ukTMukTMukTM/uUjNz4SN2MjL1YzM
        # 发送图片消息, Refer: https://open.feishu.cn/document/ukTMukTMukTM/uIDMxEjLyATMx4iMwETM
        # 发送富文本消息, Refer: https://open.feishu.cn/document/ukTMukTMukTM/uMDMxEjLzATMx4yMwETM
        # 发送群名片, Refer: https://open.feishu.cn/document/ukTMukTMukTM/ucjMxEjL3ITMx4yNyETM
        # 发送消息卡片 - 新版, Support batch send or not, Refer: https://open.feishu.cn/document/ukTMukTMukTM/uYTNwUjL2UDM14iN1ATN
        self.SEND_MESSAGE = self.OPEN_DOMAIN + '/open-apis/message/v4/send/'
        # 批量发送消息, Refer: https://open.feishu.cn/document/ukTMukTMukTM/ucDO1EjL3gTNx4yN4UTM
        self.BATCH_SEND_MESSAGE = self.OPEN_DOMAIN + '/open-apis/message/v4/batch_send/'
        # 查询消息已读状态, Refer: https://open.feishu.cn/document/ukTMukTMukTM/ukTM2UjL5EjN14SOxYTN
        self.MESSAGE_READ_INFO = self.OPEN_DOMAIN + '/open-apis/message/v4/read_info/'

    # 发送消息
    def send_message(self, data, appid=None, secret=None, ticket=None, tenant_key=None, token=None, storage=None):
        # Update params
        self.update_params(appid=appid, secret=secret, ticket=ticket, tenant_key=tenant_key, storage=storage)
        # Token
        token = final_tenant_access_token(self, appid=appid, secret=secret, ticket=ticket, tenant_key=tenant_key, token=token, storage=storage)
        data['token'] = token
        return self.post(self.SEND_MESSAGE, data=data).get('data', {})

    def send_text_message(self, text, chat_id=None, open_id=None, user_id=None, email=None, root_id=None, appid=None, secret=None, ticket=None, tenant_key=None, token=None, storage=None):
        data = {
            'chat_id': chat_id,
            'open_id': open_id,
            'user_id': user_id,
            'email': email,
            'root_id': root_id,
            'msg_type': 'text',
            'content': {
                'text': text,
            }
        }
        return self.send_message(data, appid=appid, secret=secret, ticket=ticket, tenant_key=tenant_key, token=token, storage=storage)

    def send_image_message(self, image_key, chat_id=None, open_id=None, user_id=None, email=None, root_id=None, appid=None, secret=None, ticket=None, tenant_key=None, token=None, storage=None):
        data = {
            'chat_id': chat_id,
            'open_id': open_id,
            'user_id': user_id,
            'email': email,
            'root_id': root_id,
            'msg_type': 'image',
            'content': {
                'image_key': image_key,
            }
        }
        return self.send_message(data, appid=appid, secret=secret, ticket=ticket, tenant_key=tenant_key, token=token, storage=storage)

    def send_richtext_message(self, post, chat_id=None, open_id=None, user_id=None, email=None, root_id=None, appid=None, secret=None, ticket=None, tenant_key=None, token=None, storage=None):
        data = {
            'chat_id': chat_id,
            'open_id': open_id,
            'user_id': user_id,
            'email': email,
            'root_id': root_id,
            'msg_type': 'post',
            'content': {
                'post': post,
            }
        }
        return self.send_message(data, appid=appid, secret=secret, ticket=ticket, tenant_key=tenant_key, token=token, storage=storage)

    def send_groupcard_message(self, share_chat_id, chat_id=None, open_id=None, user_id=None, email=None, root_id=None, appid=None, secret=None, ticket=None, tenant_key=None, token=None, storage=None):
        data = {
            'chat_id': chat_id,
            'open_id': open_id,
            'user_id': user_id,
            'email': email,
            'root_id': root_id,
            'msg_type': 'share_chat',
            'content': {
                'share_chat_id': share_chat_id,
            }
        }
        return self.send_message(data, appid=appid, secret=secret, ticket=ticket, tenant_key=tenant_key, token=token, storage=storage)

    def send_card_message(self, card_content, chat_id=None, open_id=None, user_id=None, email=None, root_id=None, update_multi=False, appid=None, secret=None, ticket=None, tenant_key=None, token=None, storage=None):
        data = {
            'chat_id': chat_id,
            'open_id': open_id,
            'user_id': user_id,
            'email': email,
            'root_id': root_id,
            'update_multi': update_multi,
            'msg_type': 'interactive',
            'card': card_content
        }
        return self.send_message(data, appid=appid, secret=secret, ticket=ticket, tenant_key=tenant_key, token=token, storage=storage)

    # 批量发送消息
    def batch_send_message(self, data, appid=None, secret=None, ticket=None, tenant_key=None, token=None, storage=None):
        # Update params
        self.update_params(appid=appid, secret=secret, ticket=ticket, tenant_key=tenant_key, storage=storage)
        # Token
        token = final_tenant_access_token(self, appid=appid, secret=secret, ticket=ticket, tenant_key=tenant_key, token=token, storage=storage)
        data['token'] = token
        return self.post(self.BATCH_SEND_MESSAGE, data=data).get('data', {})

    def batch_send_text_message(self, text, department_ids=None, open_ids=None, user_ids=None, appid=None, secret=None, ticket=None, tenant_key=None, token=None, storage=None):
        data = {
            'department_ids': department_ids,
            'open_ids': open_ids,
            'user_ids': user_ids,
            'msg_type': 'text',
            'content': {
                'text': text,
            }
        }
        return self.batch_send_message(data, appid=appid, secret=secret, ticket=ticket, tenant_key=tenant_key, token=token, storage=storage)

    def batch_send_image_message(self, image_key, department_ids=None, open_ids=None, user_ids=None, appid=None, secret=None, ticket=None, tenant_key=None, token=None, storage=None):
        data = {
            'department_ids': department_ids,
            'open_ids': open_ids,
            'user_ids': user_ids,
            'msg_type': 'image',
            'content': {
                'image_key': image_key,
            }
        }
        return self.batch_send_message(data, appid=appid, secret=secret, ticket=ticket, tenant_key=tenant_key, token=token, storage=storage)

    def batch_send_richtext_message(self, post, department_ids=None, open_ids=None, user_ids=None, appid=None, secret=None, ticket=None, tenant_key=None, token=None, storage=None):
        data = {
            'department_ids': department_ids,
            'open_ids': open_ids,
            'user_ids': user_ids,
            'msg_type': 'post',
            'content': {
                'post': post,
            }
        }
        return self.batch_send_message(data, appid=appid, secret=secret, ticket=ticket, tenant_key=tenant_key, token=token, storage=storage)

    def batch_send_groupcard_message(self, share_chat_id, department_ids=None, open_ids=None, user_ids=None, appid=None, secret=None, ticket=None, tenant_key=None, token=None, storage=None):
        data = {
            'department_ids': department_ids,
            'open_ids': open_ids,
            'user_ids': user_ids,
            'msg_type': 'share_chat',
            'content': {
                'share_chat_id': share_chat_id,
            }
        }
        return self.batch_send_message(data, appid=appid, secret=secret, ticket=ticket, tenant_key=tenant_key, token=token, storage=storage)

    # 消息已读状态
    def message_read_info(self, message_id, appid=None, secret=None, ticket=None, tenant_key=None, token=None, storage=None):
        # Update params
        self.update_params(appid=appid, secret=secret, ticket=ticket, tenant_key=tenant_key, storage=storage)
        # Token
        token = final_tenant_access_token(self, appid=appid, secret=secret, ticket=ticket, tenant_key=tenant_key, token=token, storage=storage)
        return self.post(self.MESSAGE_READ_INFO, data={
            'token': token,
            'message_id': message_id,
        }).get('data', {})


message = Message()

send_message = message.send_message
send_text_message = message.send_text_message
send_image_message = message.send_image_message
send_richtext_message = message.send_richtext_message
send_post_message = message.send_richtext_message
send_groupcard_message = message.send_groupcard_message
send_sharechat_message = message.send_groupcard_message
send_card_message = message.send_card_message

batch_send_message = message.batch_send_message
batch_send_text_message = message.batch_send_text_message
batch_send_image_message = message.batch_send_image_message
batch_send_richtext_message = message.batch_send_richtext_message
batch_send_post_message = message.batch_send_richtext_message
batch_send_groupcard_message = message.batch_send_groupcard_message
batch_send_sharechat_message = message.batch_send_groupcard_message

message_read_info = message.message_read_info
