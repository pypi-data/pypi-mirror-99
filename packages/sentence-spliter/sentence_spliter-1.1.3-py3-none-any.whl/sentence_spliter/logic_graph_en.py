# -*- coding:utf-8 -*-
# CREATED BY: jiangbohuai
# CREATED ON: 2021/1/21 5:23 PM
# LAST MODIFIED ON:
# AIM:
import attrdict

from .automata import condition, operation
from .automata import symbols

SYMBOLS = symbols.SYMBOLS_EN


def init_nodes(**kwargs):
    max_len = kwargs.get('max_len', 25)
    min_len = kwargs.get('min_len', 5)
    # hard_max = kwargs.get('hard_max', 200)

    # --- initialize condition & operation --- #
    edges = attrdict.AttrDict({
        'is_end_symbol': condition.IsEndSymbolEN(SYMBOLS),
        'is_bracket_close': condition.IsBracketClose(SYMBOLS),
        'is_book_close': condition.IsBookClose(SYMBOLS),
        'is_quote_close': condition.IsQuoteClose(SYMBOLS),
        'is_end_state': condition.IsEndState(SYMBOLS),
        'is_long_sentence': condition.IsLongSentence(SYMBOLS, max_len=max_len),
        'is_not_short_sentence': condition.IsShortSentence(SYMBOLS, min_len=min_len, reverse=True),
        'is_next_with_space': condition.IsNextWithSpace(SYMBOLS),

        # --- sepcial Condition --- #
        'special_ends': condition.SpecialEnds(),
        'not_in_white_list': condition.NotInWhitelistDotEn(),
        'is_empty': condition.IsSpace(SYMBOLS),
        'is_left_quota': condition.IsLeftQuotaEn(SYMBOLS),
        'is_right_quota': condition.IsRightQuotaEn(SYMBOLS)
    })

    nodes = attrdict.AttrDict({
        'do_cut': operation.Normal(SYMBOLS),
        'cut_pre_idx': operation.CutPreIdx(SYMBOLS),
        'long_handler': operation.LongHandlerEN(SYMBOLS, min_sentence_length=min_len),
        'init': operation.Indolent(SYMBOLS),
        'quota_handler': operation.Indolent(SYMBOLS),
        'end': operation.EndState(SYMBOLS)
    })
    return edges, nodes


def long_cuter_en(**kwargs):
    edges, nodes = init_nodes(**kwargs)
    return {
        nodes.init: [
            {'edge': edges.is_end_state,
             'node': nodes.end},

            {'edge': edges.is_long_sentence,
             'node': nodes.long_handler},

            # -- "..." "..."  -- #
            {'edge': edges.is_right_quota,
             'node': nodes.quota_handler},

            {'edge': edges.special_ends,
             'node': nodes.do_cut},

            # -- normal cut -- #
            {'edge': [
                edges.is_not_short_sentence,
                edges.is_next_with_space,
                edges.is_end_symbol,
                edges.is_bracket_close,
                edges.is_quote_close,
                edges.not_in_white_list
            ],
                'args': all,
                'node': nodes.do_cut},

        ],

        nodes.quota_handler: [
            {'edge': edges.is_end_state,
             'node': nodes.end},

            {'edge': [
                edges.is_not_short_sentence,
                edges.is_left_quota,
            ],
                'args': all,
                'node': nodes.cut_pre_idx},

            {'edge': edges.is_empty,
             'node': nodes.quota_handler},

            {'edge': [
                edges.is_not_short_sentence,
                edges.is_end_symbol,
                edges.is_bracket_close,
                edges.is_book_close,
                edges.is_quote_close],
                'args': all,
                'node': nodes.do_cut},

            {'edge': None,
             'node': nodes.init}
        ],

        nodes.cut_pre_idx: [
            {'edge': edges.is_end_state,
             'node': nodes.end},

            {'edge': None,  # else 状态
             'node': nodes.init},
        ],

        nodes.do_cut: [
            {'edge': edges.is_end_state,
             'node': nodes.end},

            {'edge': None,  # else 状态
             'node': nodes.init},
        ],
        nodes.long_handler: [
            {'edge': edges.is_end_state,
             'node': nodes.end},

            {'edge': None,  # else 状态
             'node': nodes.init},
        ]
    }
