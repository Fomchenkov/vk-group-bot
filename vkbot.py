#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

from flask import Flask
from flask import request
from flask import json


token = '' # Group API token
confirmation_token = '' # Group confirmation token
secret_key = '' # Group secret key
vk_api_url = 'https://api.vk.com/method/'

app = Flask(__name__)


@app.route('/vkbot', methods=['POST'])
def processing():
	data = json.loads(request.data)

	if 'secret' not in data.keys():
		return 'Not VK.'
	elif not data['secret'] == secret_key:
		return 'Bad query.'

	if data['type'] == 'confirmation':
		return confirmation_token
	elif data['type'] == 'group_join':
		request_params = { 
			'message': 'Благодарю за подписку!', 
			'user_id': data['object']['user_id'], 
			'access_token': token, 
			'v': '5.0' 
		}
		requests.post(vk_api_url + 'messages.send', data=request_params)
		return 'ok'
	elif data['type'] == 'group_leave':
		request_params = { 
			'message': 'Ждем тебя снова!', 
			'user_id': data['object']['user_id'], 
			'access_token': token, 
			'v': '5.0' 
		}
		requests.post(vk_api_url + 'messages.send', data=request_params)
		return 'ok'
	elif data['type'] == 'message_new':
		msg = 'Привет! Для того, что бы сделать заказ, или больше узнать о нас, '
		msg += 'посмотрите нашего бота в Telegram\nhttps://t.me/KronverAnimationBot.'
		request_params = {
			'message': msg, 
			'user_id': data['object']['user_id'], 
			'access_token': token, 
			'v': '5.0' 
		}
		requests.post(vk_api_url + 'messages.send', data=request_params)
		return 'ok'
	else:
		return 'ok'


def main():
	app.run(host='0.0.0.0', port=80)


if __name__ == "__main__":
	main()
