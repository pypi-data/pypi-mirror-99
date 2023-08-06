# -*- coding:utf-8 -*-
# CREATED BY: bohuai jiang 
# CREATED ON: 2020/8/12 4:42 PM
# LAST MODIFIED ON:
# AIM:
import re

SYMBOLS = {
    'quotation_left': re.compile('([“])'),
    'quotation_en': re.compile('(["])'),
    'quotation_right': re.compile('([”])'),
    'bracket_left': re.compile('([<{\[\(（【「])'),
    'bracket_right': re.compile('([\)\]}」】）>])'),
    'book_left': re.compile('([《])'),
    'book_right': re.compile('([》])'),
    'comma': re.compile('([,，;])'),
    'end_symbols': re.compile('([?\!…;？！。])'),
    'en_dot': re.compile('\.'),
    'all_symbols': re.compile('([\]\(【\?】。,！[”，\!\.「<>？"（“…《）}》」;:：\){\)\'\s])')
}


SYMBOLS_EN = {
    'quotation_left': re.compile('([“])'),
    'quotation_en': re.compile('(["])'),
    'quotation_right': re.compile('([”])'),
    'all_quota': re.compile('([“"”])'),
    'bracket_left': re.compile('([<{\[\(（【「])'),
    'bracket_right': re.compile('([\)\]}」】）>])'),
    'book_left': re.compile('([《])'),
    'book_right': re.compile('([》])'),
    'comma': re.compile('([,，;])'),
    'end_symbols': re.compile('([?\!…;？！。])'),
    'en_dot': re.compile('\.'),
    'all_symbols': re.compile('([\]\(【\?】。,！[”，\!\.「<>？"（“…《）}》」;:：\){\)\'\s])')
}
