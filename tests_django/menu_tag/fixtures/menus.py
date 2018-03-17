import re

absent = '<ul id="meniu0">Menu meniu0 is absent in DB</ul>'

empty = '<ul id="meniu1">The menu meniu1 does not contain items</ul>'

no_subbranches = \
    '''
    <ul id="meniu2">
        <li><a href="http://testserver/menu_tag/?item=meniu2-punkt1">меню2 пункт1</a></li>
        <li><a href="http://testserver/menu_tag/?item=meniu2-punkt2">меню2 пункт2</a></li>
        <li><a href="http://testserver/menu_tag/?item=meniu2-punkt3">меню2 пункт3</a></li>
    </ul>
    '''

single_subbranch1 = \
    '''
    <ul id="meniu3">
        <li><a href="http://testserver/menu_tag/?item=meniu3-punkt1">меню3 пункт1</a>
            <ul>
                <li><a href="http://testserver/menu_tag/?item=meniu3-punkt1-podpunkt1">меню3 пункт1 подпункт1</a></li>
            </ul>
        </li>
        <li><a href="http://testserver/menu_tag/?item=meniu3-punkt2">меню3 пункт2</a></li>
        <li><a href="http://testserver/menu_tag/?item=meniu3-punkt3">меню3 пункт3</a></li>
    </ul>
    '''

single_subbranch2 = \
    '''
    <ul id="meniu4">
        <li><a href="http://testserver/menu_tag/?item=meniu4-punkt1">меню4 пункт1</a></li>
        <li>
            <a href="http://testserver/menu_tag/?item=meniu4-punkt2">меню4 пункт2</a>
            <ul>
                <li><a href="http://testserver/menu_tag/?item=meniu4-punkt2-podpunkt1">меню4 пункт2 подпункт1</a></li>
            </ul>
        </li>
        <li><a href="http://testserver/menu_tag/?item=meniu4-punkt3">меню4 пункт3</a></li>
    </ul>
    '''

single_subbranch3 = \
    '''
    <ul id="meniu5">
        <li><a href="http://testserver/menu_tag/?item=meniu5-punkt1">меню5 пункт1</a></li>
        <li><a href="http://testserver/menu_tag/?item=meniu5-punkt2">меню5 пункт2</a></li>
        <li>
            <a href="http://testserver/menu_tag/?item=meniu5-punkt3">меню5 пункт3</a>
            <ul>
                <li><a href="http://testserver/menu_tag/?item=meniu5-punkt3-podpunkt1">меню5 пункт3 подпункт1</a></li>
            </ul>
        </li>
    </ul>    
    '''

multiple_subbranches1 = \
    '''
    <ul id="meniu6">
        <li><a href="http://testserver/menu_tag/?item=meniu6-punkt1">меню6 пункт1</a></li>
        <li>
            <a href="http://testserver/menu_tag/?item=meniu6-punkt2">меню6 пункт2</a>
            <ul>
                <li><a href="http://testserver/menu_tag/?item=meniu6-punkt2-podpunkt1">меню6 пункт2 подпункт1</a></li>
                <li><a href="http://testserver/menu_tag/?item=meniu6-punkt2-podpunkt2">меню6 пункт2 подпункт2</a></li>
            </ul>
        </li>
        <li><a href="http://testserver/menu_tag/?item=meniu6-punkt3">меню6 пункт3</a></li>
    </ul>    
    '''

multiple_subbranches2 = \
    '''
    <ul id="meniu6">
        <li><a href="http://testserver/menu_tag/?item=meniu6-punkt1">меню6 пункт1</a></li>
        <li><a href="http://testserver/menu_tag/?item=meniu6-punkt2">меню6 пункт2</a></li>
        <li>
            <a href="http://testserver/menu_tag/?item=meniu6-punkt3">меню6 пункт3</a>
            <ul>
                <li><a href="http://testserver/menu_tag/?item=meniu6-punkt3-podpunkt1">меню6 пункт3 подпункт1</a></li>
                <li><a href="http://testserver/menu_tag/?item=meniu6-punkt3-podpunkt2">меню6 пункт3 подпункт2</a></li>
                <li><a href="http://testserver/menu_tag/?item=meniu6-punkt3-podpunkt3">меню6 пункт3 подпункт3</a></li>
            </ul>
        </li>
    </ul>
    '''

menus = [no_subbranches,
         single_subbranch1,
         single_subbranch2,
         single_subbranch3,
         multiple_subbranches1,
         multiple_subbranches2]

no_subbranches, \
single_subbranch1, \
single_subbranch2, \
single_subbranch3, \
multiple_subbranches1, \
multiple_subbranches2 = [re.sub(">\s*<", "><", x).strip() for x in menus]
