from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.embed import file_html
from bokeh.resources import CDN

def homePageGraph(width, height,blocks,transazioni,assets):
    legend = ['Numero Transazioni', 'Transazioni', 'Dettagli Transazioni']
    fig = figure(
                title ="Dati Transazioni:",
                x_range = legend, 
                plot_width=int(width), plot_height=int(height),
                toolbar_location=None)
    top = [blocks,transazioni,assets]
    fig.vbar(
        x = legend,
        width=0.5,
        bottom=0,
        top= top,
        color='navy',
    )

    fig.title.text = "Dati Transazioni:"
    fig.title.align = "right"
    fig.title.text_color = "darkblue"
    fig.title.text_font_size = "25px"
    #fig.legend.location = "top_center"
    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    script, div = components(fig)
    html = f'''
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta http-equiv="content-type" content="text/html; charset=utf-8">
            <title>Embed Demo</title>
            { js_resources }
            { css_resources }
            { script}
        </head>
        <body>
            {div}
        </body>
        </html>
    '''
    #htmlFile = file_html(fig, (js_resources, css_resources), "dashboard.html")
    #html = render_template(
    #    'index.html',
    #    plot_script=script,
    #    plot_div=div,
    #    js_resources=js_resources,
    #    css_resources=css_resources,
    #)
    return script,div, js_resources, css_resources,html
