"""
Simple plugin that registers the BabelJSX filter with Jinja2
"""
from dukpy.webassets import BabelJSX
from webassets.filter import register_filter


def register():
    register_filter(BabelJSX)
