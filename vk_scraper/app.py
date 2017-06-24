# -*- coding: utf-8 -*-
import getopt
import sys
import vk_api

short_options = 'u:p:f:d:nt:ql:'
long_options = ['username=',
                'password',
                'filename=',
                'destination=',
                'retain_username',
                'media_types=',
                'latest',
                'quiet',
                'limit=',
                ]


def main():
    username, password = process_args(sys.argv[1:])

    if username is None or password is None:
        sys.exit("No username / password")

    vk_session = vk_api.VkApi(
        username, password,
        auth_handler=two_factor_handler,
        captcha_handler=captcha_handler
    )

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()

    response = vk.wall.get(count=1)

    if response['items']:
        print(response['items'][0])


def process_args(args):
    username = None
    password = None

    options, remainder = getopt.getopt(args, short_options, long_options)
    print('OPTIONS   :', options)
    print('REMAINING :', remainder)

    for opt, arg in options:
        if opt in ('-u', '--username'):
            username = arg
        elif opt in ('-p', '--password'):
            password = True
        elif opt in ('-q', '--quiet'):
            quiet = True

    return username, password


def two_factor_handler():
    key = input("Enter authentication code: ")
    remember_device = True

    return key, remember_device


def captcha_handler(captcha):
    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()

    return captcha.try_again(key)


if __name__ == '__main__':
    main()
