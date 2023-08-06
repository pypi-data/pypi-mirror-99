import conv2eng

data = conv2eng.conve2english.check_word("Currently I have seventy dollar in my account")
print(data)

upd = conv2eng.conve2english.update_word_dict('Seventy','70')
print(upd)

data = conv2eng.conve2english.check_word("Currently I have seventy dollar in my account")
print(data)