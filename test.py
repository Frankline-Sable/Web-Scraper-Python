import re, pprint

'''
        
        #"src: url('../fonts/fontawesome-webfont.eot?#iefix&v=4.7.0') format('embedded-opentype'), url('../fonts/fontawesome-webfont.woff2?",
        
    
            

'''
list = [
"background-image: url('../images/crowdy1.jpg');",
    "background-image: url ( '../images/cro wdy2.jpgb');nmhj",
    "background-image:       url('../images/crowdy3.jpg'bn)h;",
    'background-image: url(  "../images/crowdy4.jpg"  );'
    "background-image: url (    '../images/crowdy5.jpg');",
    "background-image:       url('../images/crowdy.jpg'     );",
    " url('../fonts/fontawesome-webfont.eot?v=4.7.0');",
    "src: url('../../Fonts/Alexana Neue.ttf') format('opentype');",
    "url(n)",
    "src: url('../fonts/fontawesome-webfont.eot?#iefix&v=4.7.0') format('embedded-opentype'), url('../fonts/fontawesome-webfont.woff2?v=4.7.0') format('woff2'), url('../fonts/fontawesome-webfont.woff?v=4.7.0') format('woff'), url('../fonts/fontawesome-webfont.ttf?v=4.7.0') format('truetype'), url('../fonts/fontawesome-webfont.svg?v=4.7.0#fontawesomeregular') format('svg');"
]
for lt in list:
    # pattern = re.compile(r"url( )?\(((\w*\d*\S*\s*)*)\)")
    pattern = re.compile(r"url( )?\(((\w*\d*\S*\s*)*)\)*")
    search = pattern.search(lt)

    if search != None:

        grp = search.group()
        arr1 = grp.split('format(')
        arr=[]
        for x in arr1:
            arr2 = x.split('url(')
            arr3 = []
            for y in arr2:
                tr = y.split("?")[0]
                tr = tr.replace("'", "")
                tr = tr.replace('"', '')
                tr = tr.split(')')[0]
                if len(tr)>10:
                    print(tr)
    else:
        print("\n no match\n")
    '''
        test2 = " src: url('../fonts/fontawesome-webfont.eot?#iefix&v=4.7.0') format('embedded-opentype'), url('../fonts/fontawesome-webfont.woff2?v=4.7.0') format('woff2'), url('../fonts/fontawesome-webfont.woff?v=4.7.0') format('woff'), url('../fonts/fontawesome-webfont.ttf?v=4.7.0') format('truetype'), url('../fonts/fontawesome-webfont.svg?v=4.7.0#fontawesomeregular') format('svg');"
        pattern = re.compile(r"url( )?\(((\w*\d*\S*\s*)*)\)*")
        search = pattern.search(test2)
        grp = search.group()
        arr1 = grp.split('format(')
        for x in arr1:
            arr2 = x.split('url(')
            for y in arr2:
                arr3 = y.split("?")
            print(arr3)
        '''
