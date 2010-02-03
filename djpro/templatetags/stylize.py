from django.template import Library
from pygments import highlight as pygments_highlight
from pygments.lexers import get_lexer_by_name, guess_lexer_for_filename
from pygments.formatters import HtmlFormatter

register = Library()

# prints the CSS style of choice into the webpage, for pygments
@register.simple_tag
def pygments_css(style):
  retval = u'<style type="text/css"><!--\n'
  retval += HtmlFormatter(style=style).get_style_defs('.highlight')
  retval += '\n--></style>'
  return retval

@register.simple_tag
def highlight(type, text):
  """Prints the given text in a selectable highlight mode."""
  return pygments_highlight(text, get_lexer_by_name(type, encoding='UTF-8'), 
      HtmlFormatter(cssclass="highlight", linenos="table"))

@register.simple_tag
def auto_highlight(blob):
  """Prints the given blob in highlighted mode."""
  try: lexer = guess_lexer_for_filename(blob.basename, blob.data)
  except: lexer = get_lexer_by_name('text', enconding='UTF-8') 
  return pygments_highlight(blob.data, lexer, 
      HtmlFormatter(cssclass="highlight", linenos="table"))

