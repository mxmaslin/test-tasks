absent = {'ul': {'#id': 'meniu0', '': 'Menu meniu0 is absent in DB'}}

empty = {'ul': {'': 'The menu "meniu1" does not contain items', '#id': 'meniu1'}}

no_subbranches = {'ul': {'': '',
                         '#id': 'meniu2',
                         'li': [{'': '',
                                 'a': {'': 'меню2 пункт1',
                                       '#href': 'http://testserver/menu_tag/?item=meniu2-punkt1'}},
                                {'': '',
                                 'a': {'': 'меню2 пункт2',
                                       '#href': 'http://testserver/menu_tag/?item=meniu2-punkt2'}},
                                {'': '',
                                 'a': {'': 'меню2 пункт3',
                                       '#href': 'http://testserver/menu_tag/?item=meniu2-punkt3'}}]}}

single_subbranch1 = {'ul': {'': '',
                            '#id': 'meniu3',
                            'li': [{'': '',
                                    'a': {'': 'меню3 пункт1',
                                          '#href': 'http://testserver/menu_tag/?item=meniu3-punkt1'}},
                                   {'': '',
                                    'a': {'': 'меню3 пункт2',
                                          '#href': 'http://testserver/menu_tag/?item=meniu3-punkt2'}},
                                   {'': '',
                                    'a': {'': 'меню3 пункт3',
                                          '#href': 'http://testserver/menu_tag/?item=meniu3-punkt3'}}]}}

single_subbranch2 = {'ul': {'': '',
                            '#id': 'meniu4',
                            'li': [{'': '',
                                    'a': {'': 'меню4 пункт1',
                                          '#href': 'http://testserver/menu_tag/?item=meniu4-punkt1'}},
                                   {'': '',
                                    'a': {'': 'меню4 пункт2',
                                          '#href': 'http://testserver/menu_tag/?item=meniu4-punkt2'}},
                                   {'': '',
                                    'a': {'': 'меню4 пункт3',
                                          '#href': 'http://testserver/menu_tag/?item=meniu4-punkt3'}}]}}

single_subbranch3 = {'ul': {'': '',
                            '#id': 'meniu5',
                            'li': [{'': '',
                                    'a': {'': 'меню5 пункт1',
                                          '#href': 'http://testserver/menu_tag/?item=meniu5-punkt1'}},
                                   {'': '',
                                    'a': {'': 'меню5 пункт2',
                                          '#href': 'http://testserver/menu_tag/?item=meniu5-punkt2'}},
                                   {'': '',
                                    'a': {'': 'меню5 пункт3',
                                          '#href': 'http://testserver/menu_tag/?item=meniu5-punkt3'}}]}}

multiple_subbranches = {'ul': {'': '',
                               '#id': 'meniu6',
                               'li': [{'': '',
                                       'a': {'': 'меню6 пункт1',
                                             '#href': 'http://testserver/menu_tag/?item=meniu6-punkt1'}},
                                      {'': '',
                                       'a': {'': 'меню6 пункт2',
                                             '#href': 'http://testserver/menu_tag/?item=meniu6-punkt2'}},
                                      {'': '',
                                       'a': {'': 'меню6 пункт3',
                                             '#href': 'http://testserver/menu_tag/?item=meniu6-punkt3'}}]}}
