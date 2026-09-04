prefix_rules = [
    # 常用前缀（直接拼接）
    ('anti', lambda w: f"anti{w}" if len(w)>4 else None),
    ('auto', lambda w: f"auto{w}"),
    ('bi', lambda w: f"bi{w}" if len(w)>3 else None),
    ('counter', lambda w: f"counter{w}"),
    ('de', lambda w: f"de{w}"),
    ('dis', lambda w: f"dis{w}"),
    ('extra', lambda w: f"extra-{w}" if len(w)>5 else f"extra{w}"),
    ('hyper', lambda w: f"hyper{w}"),
    ('il', lambda w: f"il{w}" if w.startswith('l') else None),
    ('im', lambda w: f"im{w}" if w.startswith(('m','p','b')) else None),
    ('in', lambda w: f"in{w}"),
    ('inter', lambda w: f"inter{w}"),
    ('ir', lambda w: f"ir{w}" if w.startswith('r') else None),
    ('macro', lambda w: f"macro{w}"),
    ('micro', lambda w: f"micro{w}"),
    ('mid', lambda w: f"mid-{w}" if len(w)>4 else f"mid{w}"),
    ('mis', lambda w: f"mis{w}"),
    ('mono', lambda w: f"mono{w}"),
    ('multi', lambda w: f"multi{w}"),
    ('non', lambda w: f"non-{w}" if len(w)>4 else f"non{w}"),
    ('over', lambda w: f"over{w}"),
    ('poly', lambda w: f"poly{w}"),
    ('post', lambda w: f"post-{w}" if len(w)>4 else f"post{w}"),
    ('pre', lambda w: f"pre{w}"),
    ('pro', lambda w: f"pro{w}"),
    ('re', lambda w: f"re{w}"),
    ('semi', lambda w: f"semi{w}"),
    ('sub', lambda w: f"sub{w}"),
    ('super', lambda w: f"super{w}"),
    ('trans', lambda w: f"trans{w}"),
    ('tri', lambda w: f"tri{w}"),
    ('ultra', lambda w: f"ultra{w}"),
    ('un', lambda w: f"un{w}"),
    ('under', lambda w: f"under{w}"),
    ('uni', lambda w: f"uni{w}")
]

suffix_rules = [
    # 名词后缀
    ('acy', [
        lambda w: w[:-3] + 'acy' if w.endswith('ate') else None,  # private → privacy
        lambda w: w[:-3] + 'acy' if w.endswith('tic') else None  # democratic → democracy
    ]),
    ('al', [
        lambda w: w + 'al',
        lambda w: w[:-2] + 'al' if w.endswith('ic') else None,  # logic → logical
        lambda w: w[:-1] + 'al' if w.endswith('e') else None    # culture → cultural
    ]),
    ('ance', [
        lambda w: w + 'ance',
        lambda w: w[:-1] + 'ance' if w.endswith('y') else None  # defy → defiance
    ]),
    ('dom', [lambda w: w + 'dom']),
    ('er', [
        lambda w: w + 'er',  # teach → teacher
        lambda w: w + 'r' if w.endswith('e') else None,  # write → writer
        lambda w: w[:-1] + 'ier' if w.endswith('y') else None,  # happy → happier
        lambda w: w + 'er' if len(w)>=3 and w[-1]==w[-2] else None  # win → winner
    ]),
    ('hood', [lambda w: w + 'hood']),
    ('ion', [
        lambda w: w + 'ion',
        lambda w: w[:-2] + 'ion' if w.endswith('te') else None,  # create → creation
        lambda w: w[:-3] + 'sion' if w.endswith('d') else None,   # decide → decision
        lambda w: w[:-3] + 'ssion' if w.endswith('t') else None  # admit → admission
    ]),
    ('ism', [lambda w: w + 'ism']),
    ('ist', [lambda w: w + 'ist']),
    ('ity', [
        lambda w: w + 'ity',
        lambda w: w[:-1] + 'ity' if w.endswith('l') else None,  # formal → formality
        lambda w: w[:-3] + 'ity' if w.endswith('ble') else None  # possible → possibility
    ]),
    ('ment', [lambda w: w + 'ment']),
    ('ness', [lambda w: w + 'ness']),
    ('or', [
        lambda w: w + 'or',
        lambda w: w[:-1] + 'or' if w.endswith('e') else None  # create → creator
    ]),
    ('ship', [lambda w: w + 'ship']),
    ('sion', [lambda w: w + 'sion']),
    ('tion', [lambda w: w + 'tion']),
    ('tude', [lambda w: w + 'tude']),
    ('ure', [lambda w: w + 'ure']),
    # 形容词后缀
    ('able', [
        lambda w: w + 'able',
        lambda w: w[:-1] + 'able' if w.endswith('e') else None,  # create → creatable
        lambda w: w[:-1] + 'iable' if w.endswith('y') else None,  # envy → enviable
        lambda w: w + 'able' if w.endswith('d') else None        # afford → affordable
    ]),
    ('al', [lambda w: w + 'al']),
    ('ant', [lambda w: w + 'ant']),
    ('ary', [lambda w: w + 'ary']),
    # ('ed', [lambda w: w + 'ed']),
    ('en', [lambda w: w + 'en']),
    ('ent', [lambda w: w + 'ent']),
    ('ful', [lambda w: w + 'ful']),
    ('ible', [
        lambda w: w + 'ible',
        lambda w: w[:-3] + 'ible' if w.endswith('ce') else None  # force → forcible
    ]),
    ('ic', [lambda w: w + 'ic']),
    ('ical', [
        lambda w: w + 'ical',
        lambda w: w[:-2] + 'ical' if w.endswith('ic') else None  # history → historical
    ]),
    # ('ing', [lambda w: w + 'ing']),
    ('ish', [lambda w: w + 'ish']),
    ('ive', [lambda w: w + 'ive']),
    ('less', [lambda w: w + 'less']),
    ('like', [lambda w: w + 'like']),
    ('ly', [
        lambda w: w + 'ly',
        lambda w: w[:-1] + 'ily' if w.endswith('y') else None,   # happy → happily
        lambda w: w + 'ly' if w.endswith('ic') else None,        # basic → basically
        lambda w: w + 'ally' if w.endswith('c') else None        # magic → magically
    ]),
    ('ous', [
        lambda w: w + 'ous',
        lambda w: w[:-1] + 'ous' if w.endswith('e') else None,   # fame → famous
        lambda w: w[:-1] + 'ious' if w.endswith('y') else None   # glory → glorious
    ]),
    ('some', [lambda w: w + 'some']),
    ('ward', [lambda w: w + 'ward']),
    ('wise', [lambda w: w + 'wise']),
    ('y', [
        lambda w: w + 'y',
        lambda w: w[:-1] + 'y' if w.endswith('e') else None,     #ice → icy
        lambda w: w + 'ey' if w.endswith('u') else None          #glue → gluey
    ]),
    # 动词后缀
    ('ate', [lambda w: w + 'ate']),
    ('en', [
        lambda w: w + 'en',
        lambda w: w + 'n' if w.endswith('e') else None           #  awake → awaken
    ]),
    ('ify', [
        lambda w: w + 'ify',
        lambda w: w[:-1] + 'ify' if w.endswith('e') else None,   #  pure → purify
        lambda w: w[:-1] + 'cify' if w.endswith('c') else None  #  specific → specify (例外需单独处理)
    ]),
    ('ize', [
        lambda w: w + 'ize',
        lambda w: w[:-1] + 'ize' if w.endswith('y') else None,   #  theory → theorize
        lambda w: w[:-2] + 'ize' if w.endswith('ic') else None   #  critic → criticize
    ])
]

affix_rules = [
    # region 副词后缀（最高优先级）
    ('suffix', 'ly', 2, lambda s: s[:-2]),          # quickly → quick
    ('suffix', 'ward', 4, lambda s: s[:-4]),        # backward → back
    ('suffix', 'wise', 4, lambda s: s[:-4]),        # clockwise → clock
    ('suffix', 'ically', 6, lambda s: s[:-6]+'y'), # terrifically → terrify
    ('suffix', 'ically', 6, lambda s: s[:-6]+'ic'), # economically → economic
    ('suffix', 'ways', 4, lambda s: s[:-4]),        # sideways → side
    # endregion

    # region 形容词后缀
    ('suffix', 'less', 4, lambda s: s[:-4]),        # endless → end
    ('suffix', 'ible', 4, lambda s: s[:-4]),        # possible → poss
    ('suffix', 'able', 4, lambda s: s[:-4]),        # comfortable → comfort
    ('suffix', 'able', 4, lambda s: s[:-4]+'y'),    # equitable → equity
    ('suffix', 'ical', 4, lambda s: s[:-4]+'y'),    # historical → history
    ('suffix', 'ical', 4, lambda s: s[:-4]+'ics'),  # mathematical → mathematics
    ('suffix', 'ous', 3, lambda s: s[:-3]),         # dangerous → danger
    ('suffix', 'ive', 3, lambda s: s[:-3]),         # adaptive → adapt
    ('suffix', 'ful', 3, lambda s: s[:-3]),         # beautiful → beauty
    ('suffix', 'ic', 2, lambda s: s[:-2] + 'y'),    # terrific → terrify
    ('suffix', 'al', 2, lambda s: s[:-2]),          # musical → music
    ('suffix', 'y', 1, lambda s: s[:-1] ),          # cloudy → cloud
    ('suffix', 'ant', 3, lambda s: s[:-3]),         # important → import
    ('suffix', 'ary', 3, lambda s: s[:-3]),         # customary → custom
    ('suffix', 'en', 2, lambda s: s[:-2]),          # golden → gold
    ('suffix', 'ent', 3, lambda s: s[:-3]),         # different → differ
    ('suffix', 'ish', 3, lambda s: s[:-3]),  
    ('suffix', 'like', 4, lambda s: s[:-4]), 
    ('suffix', 'some', 4, lambda s: s[:-4]), 
    ('suffix', 'ward', 4, lambda s: s[:-4]), 
    ('suffix', 'wise', 4, lambda s: s[:-4]), 
    # endregion

    # region 名词后缀
    ('suffix', 'acy', 3, lambda s: s[:-3]+'ate'),  # privacy → private
    ('suffix', 'acy', 3, lambda s: s[:-3]+'tic'),  # democracy → democratic
    ('suffix', 'al', 2, lambda s: s[:-2]),         # refusal → refuse
    ('suffix', 'al', 2, lambda s: s[:-2]+'ic'),    # logical → logic
    ('suffix', 'al', 2, lambda s: s[:-2]+'e'),     # cultural → culture
    ('suffix', 'ance', 4, lambda s: s[:-4]),       # appearance → appear
    ('suffix', 'ance', 4, lambda s: s[:-4]+'y'),   # defiance → defy
    ('suffix', 'dom', 3, lambda s: s[:-3]),        # freedom → free
    ('suffix', 'er', 2, lambda s: s[:-2]),         # teacher → teach
    ('suffix', 'er', 1, lambda s: s[:-1]+'e'),     # writer → write
    ('suffix', 'ier', 3, lambda s: s[:-3]+'y'),    # happier → happy
    ('suffix', 'er', 2, lambda s: s[:-1] if len(s)>=3 and s[-3]==s[-2] else None), # winner → win
    ('suffix', 'hood', 4, lambda s: s[:-4]),       # childhood → child
    ('suffix', 'ion', 3, lambda s: s[:-3]+'te'),   # creation → create
    ('suffix', 'sion', 5, lambda s: s[:-5]+'d'),   # decision → decide
    ('suffix', 'ssion', 6, lambda s: s[:-6]+'t'),  # admission → admit
    ('suffix', 'tion', 4, lambda s: s[:-4] + 't'),      # action → act
    ('suffix', 'tion', 4, lambda s: s[:-4] + 'te'),     # relation → relate
    ('suffix', 'ization', 7, lambda s: s[:-7] + 'ize'), # organization → organize
    ('suffix', 'ism', 3, lambda s: s[:-3]),        # socialism → social
    ('suffix', 'ism', 3, lambda s: s[:-3] + 'e'),  # escapism → escape
    ('suffix', 'ist', 3, lambda s: s[:-3]),        # artist → art
    ('suffix', 'ist', 3, lambda s: s[:-3] + 'e'),  # typist → type
    ('suffix', 'ity', 3, lambda s: s[:-3]+'l'),    # formality → formal
    ('suffix', 'ity', 3, lambda s: s[:-3]+'ble'),  # possibility → possible
    ('suffix', 'ity', 3, lambda s: s[:-3] + 'e'),  # activity → active
    ('suffix', 'ent', 3, lambda s: s[:-3] + 'e'),  # urgent → urge
    ('suffix', 'ency', 4, lambda s: s[:-4] + 'e'), # urgecy → urge
    ('suffix', 'ian', 3, lambda s: s[:-3]),        # musician → music
    ('suffix', 'ian', 3, lambda s: s[:-3] + 'y'),  # historian → history
    ('suffix', 'ment', 4, lambda s: s[:-4]),       # development → develop
    ('suffix', 'ness', 4, lambda s: s[:-4]),       # happiness → happy
    ('suffix', 'or', 2, lambda s: s[:-2]+'e'),     # creator → create
    ('suffix', 'or', 2, lambda s: s[:-2]),         # actor → act
    ('suffix', 'ship', 4, lambda s: s[:-4]),       # friendship → friend
    ('suffix', 'tude', 4, lambda s: s[:-4]),       # attitude → att
    ('suffix', 'ure', 3, lambda s: s[:-3]),        # failure → fail
    ('suffix', 'ies', 3, lambda s: s[:-3] + 'y'),       # cities → city
    ('suffix', 'es', 2, lambda s: s[:-2]),              # heroes → hero
    ('suffix', 's', 1, lambda s: s[:-1]),               # licenses → license
    # endregion
    
    # region 动词后缀
    ('suffix', 'ingly', 5, lambda s: s[:-5] \
                            + 'y' if len(s)>=5 and s[-5] == s[-6] else None),    # willingly → will
    ('suffix', 'ing', 3, lambda s: s[:-3] \
                            + ('e' if len(s)>=4 and s[-4] == 'e' else s[:-3])),  # seeing → see
    ('suffix', 'ing', 3, lambda s: s[:-3]),                                      # starting → start
    ('suffix', 'ing', 3, lambda s: s[:-3] + 'e'),                                # hoping → hope
    ('suffix', 'ed', 2, lambda s: s[:-2] + \
                            ('e' if len(s)>=3 and s[-3] == 'e' else s[:-2])),    # agreed → agree
    ('suffix', 'ed', 2, lambda s: s[:-2] + 'e'),                                 # danced → dance
    ('suffix', 'ed', 2, lambda s: s[:-2]),                                       # worked → work
    ('suffix', 'ied', 3, lambda s: s[:-3] + 'y'),                                # flied → fly
    ('suffix', 'ify', 3, lambda s: s[:-3] + 'y'),       # simplify → simple
    ('suffix', 'ize', 3, lambda s: s[:-3]),             # realize → real
    ('suffix', 'ized', 4, lambda s: s[:-4]+'y'),        # memorized → memory
    ('suffix', 'en', 2, lambda s: s[:-2]),              # strengthen → strength
    ('suffix', 'ate', 3, lambda s: s[:-3] + 'e'),       # activate → active

    # region 前缀规则
    ('prefix', 'anti', 4, lambda s: s[4:] if len(s[4:])>4 else None),       # antibody → body
    ('prefix', 'auto', 4, lambda s: s[4:]),
    ('prefix', 'bi', 2, lambda s: s[2:] if len(s[2:])>3 else None),
    ('prefix', 'counter', 7, lambda s: s[7:]),  # counterpart → part
    ('prefix', 'de', 2, lambda s: s[2:]),
    ('prefix', 'dis', 3, lambda s: s[3:]),      # dislike → like
    ('prefix', 'extra', 5, lambda s: s[5:] if not s.startswith("extra-") else s[6:]),
    ('prefix', 'hyper', 5, lambda s: s[5:]),
    ('prefix', 'il', 2, lambda s: s[2:] if s[2:].startswith('l') else None),            # illegal → legal
    ('prefix', 'im', 2, lambda s: s[2:] if s[2:].startswith(('m','p','b')) else None),  # impossible → possible
    ('prefix', 'in', 2, lambda s: s[2:]),       # inactive → active
    ('prefix', 'inter', 5, lambda s: s[5:]),
    ('prefix', 'ir', 2, lambda s: s[2:] if s[2:].startswith('r') else None),            # irregular → regular
    ('prefix', 'macro', 5, lambda s: s[5:]),    
    ('prefix', 'micro', 5, lambda s: s[5:]),    # microphone → phone
    ('prefix', 'mid', 3, lambda s: s[3:] if not s.startswith("mid-") else s[4:]),
    ('prefix', 'mis', 3, lambda s: s[3:]),      # mislead → lead
    ('prefix', 'mono', 4, lambda s: s[4:]),
    ('prefix', 'multi', 5, lambda s: s[5:]),
    ('prefix', 'non', 3, lambda s: s[3:] if not s.startswith("non-") else s[4:]),       # nonfiction → fiction
    ('prefix', 'over', 4, lambda s: s[4:]),     # overeat → eat 
    ('prefix', 'poly', 4, lambda s: s[4:]),
    ('prefix', 'post', 4, lambda s: s[4:] if not s.startswith("post-") else s[5:]),
    ('prefix', 'pre', 3, lambda s: s[3:]),      # preview → view
    ('prefix', 'pro', 3, lambda s: s[3:]),
    ('prefix', 're', 2, lambda s: s[2:]),       # rebuild → build
    ('prefix', 'semi', 4, lambda s: s[4:]),
    ('prefix', 'sub', 3, lambda s: s[3:]),      # subgroup → group
    ('prefix', 'super', 5, lambda s: s[5:]),
    ('prefix', 'trans', 5, lambda s: s[5:]),
    ('prefix', 'tri', 3, lambda s: s[3:]),
    ('prefix', 'ultra', 5, lambda s: s[5:]),
    ('prefix', 'un', 2, lambda s: s[2:]),       # unhappy → happy
    ('prefix', 'under', 5, lambda s: s[5:]),    # underestimate → estimate
    ('prefix', 'uni', 3, lambda s: s[3:]),
    ('prefix','ab', 2, lambda s: s[2:]),        # abnormal → normal
    # endregion
]