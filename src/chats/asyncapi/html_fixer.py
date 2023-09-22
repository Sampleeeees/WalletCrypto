# -*- coding: utf-8 -*-
"""
HTML fixer to fix the HTML generated by the asyncapi library.
"""

# open html file in asynapi_docs/index.html
with open("templates/chat/asyncapi/index.html", "r") as f:
    html_data = f.read()

# after all '<link href="' add '/static/'
html_data = html_data.replace('<link href="', '<link href="/static/async_api/')

# after all '<script src="' add '/static/'
html_data = html_data.replace('<script src="', '<script src="/static/async_api/')

# write fixed html to file
with open("templates/chat/asyncapi/index.html", "w") as f:
    f.write(html_data)