# -*- coding: utf-8 -*-
'''
@author: yaleimeng@sina.com
@license: (C) Copyright 2017
@desc:  python3 版本中文Alice，暂时简单添加空格
@DateTime: Created on 2017/11/15，at  10:20       '''

import aiml

alice = aiml.Kernel()
alice.learn("/Users/caoxiaojie/Notebooks/AIStudy/知识图谱/知识问答/AIML/Example/test.aiml")

while True:
    text = input('Alice请您提问...>>')
    print(alice.respond(text))
