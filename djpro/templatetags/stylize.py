from django.template import Library, Node, resolve_variable
from pygments import highlight as pygments_highlight
from pygments.lexers import get_lexer_by_name, guess_lexer_for_filename
from pygments.formatters import HtmlFormatter

register = Library()

# usage: {% stylize "language" %}...language text...{% endstylize %}
class StylizeNode(Node):
  def __init__(self, nodelist, *varlist):
    self.nodelist, self.vlist = (nodelist, varlist)

  def render(self, context):
    style = 'text'
    if len(self.vlist) > 0:
      style = resolve_variable(self.vlist[0], context)
    return pygments_highlight(self.nodelist.render(context),
                     get_lexer_by_name(style, encoding='UTF-8'), 
                     HtmlFormatter(cssclass='highlight'))

def stylize(parser, token):
  nodelist = parser.parse(('endstylize',))
  parser.delete_first_token()
  return StylizeNode(nodelist, *token.contents.split()[1:])

stylize = register.tag(stylize)

# prints the CSS style of choice into the webpage, for pygments
@register.simple_tag
def pygments_css(style):
  retval = u'<style type="text/css"><!--\n'
  retval += HtmlFormatter(style=style).get_style_defs('.highlight')
  retval += '\n--></style>'
  return retval

# prints the given blob in highlighted mode
@register.simple_tag
def highlight(blob):
  try: lexer = guess_lexer_for_filename(blob.basename, blob.data)
  except: lexer = get_lexer_by_name('text', enconding='UTF-8') 
  return pygments_highlight(blob.data, lexer, 
      HtmlFormatter(cssclass="highlight", linenos="table"))
