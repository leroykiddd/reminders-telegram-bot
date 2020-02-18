import threading

import telebot, time

TOKEN = 'token'

bot = telebot.TeleBot(TOKEN)


def thread_function(user_id, time_sleep, reminder):
    time.sleep(time_sleep)
    bot.send_message(user_id, reminder)


def text_reminder(msg):
    try:
        return msg[msg.index(':') + 1:len(msg)].strip()
    except:
        return 'Вы что-то хотели сделать!'


def time_reminder(msg):
    res = 0
    l = len(str(msg))
    integ = []
    i = 0
    while i < l:
        s_int = ''
        a = msg[i]
        while '0' <= a <= '9':
            s_int += a
            i += 1
            if i < l:
                a = msg[i]
            else:
                break
        i += 1
        if s_int != '':
            integ.append(int(s_int))
    try:
        if len(integ) < 3 or ':' not in msg:
            return 'Error'
        else:
            res += (integ[0] * 3600 + integ[1] * 60 + integ[2])
            return res
    except:
        return 'Error'


@bot.message_handler(content_types=['/start'])
def start(message):
    bot.send_message(message.from_user.id, 'Привет, напиши о чем тебе напомнить и через какое время в таком формате "'
                                           'часы минуты секунды: текст напоминания"')
    bot.send_message(message.from_user.id, 'Пример: 0 1 30: тест - бот напишет "тест" через 1 минуту и 30 секунд')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id,
                         'Привет, напиши о чем тебе напомнить и через какое время в таком формате "'
                         'часы минуты секунды: текст напоминания"')
        bot.send_message(message.from_user.id, 'Пример: 0 1 30: тест - бот напишет "тест" через 1 минуту и 30 секунд')
    else:
        tim = time_reminder(str(message.text))
        if tim == 'Error':
            bot.send_message(message.from_user.id, 'Вы неправильно ввели время!')
        else:
            bot.send_message(message.from_user.id, 'Хорошо')
            x = threading.Thread(
                target=thread_function(user_id=message.from_user.id, time_sleep=tim,
                                       reminder=text_reminder(str(message.text))),
                args=(1,), daemon=True)
            x.start()


bot.polling(none_stop=True, interval=0)
