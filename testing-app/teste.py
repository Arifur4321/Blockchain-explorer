import dashboard
script,div, js_resources, css_resources = dashboard.homePageGraph(width=750,height=350, blocks=30,transazioni=57,assets=20)

body = f'''
    <style>
        {css_resources}
    </style>
    
    {js_resources}
    {div}
    '''