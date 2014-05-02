import datetime
import pytz
from django import template
from spy.models import Post

register = template.Library()

timezoneLocal = pytz.timezone('America/Los_Angeles')

#Format the Current Time
def do_current_time(parser, token):
    try:
        tag_name, format_string = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    if not (format_string[0] == format_string[-1] and format_string[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
    return CurrentTimeNode(format_string[1:-1])

class CurrentTimeNode(template.Node):
    def __init__(self, format_string):
        self.format_string = format_string
    def render(self, context):
        return datetime.datetime.now().strftime(self.format_string)

register.tag('current_time', do_current_time)

#Format an Objects DateTimeField Last Update
def do_last_update(parser, token):
    try:
        tag_name, format_string = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    if not (format_string[0] == format_string[-1] and format_string[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
    return FormatTimeNode(format_string[1:-1])

class FormatTimeNode(template.Node):
    def __init__(self, format_string):
        self.date_list = Post.objects.all().order_by("-modified")[:1]
        if self.date_list.exists():
            self.date_to_be_formatted = self.date_list[0].modified.astimezone(timezoneLocal)
        else:
            self.date_to_be_formatted = ''
        self.format_string = format_string
    def render(self, context):
        try:
            actual_date = self.date_to_be_formatted
            return actual_date.strftime(self.format_string)
        except:
            return ''

register.tag('last_update', do_last_update)
