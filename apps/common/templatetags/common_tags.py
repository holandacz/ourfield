# -*- coding: utf-8 -*-
from django import template
import settings
register = template.Library()


class ShowGoogleAnalyticsJS(context):

    def render(self, context):
        if settings.DEBUG:
            return "<!-- ShowGoogleAnalyticsJS not included because you are in Debug mode! -->"

        return '''
        <script type="text/javascript">
          var _gaq = _gaq || [];
          _gaq.push(['_setAccount', "{{ %s }}"]);
          _gaq.push(['_trackPageview']);
        
          (function() {
            var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
            ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
            var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
          })();
        </script>           
	        ''' % GOOGLE_ANALYTICS_CODE

    context['google_analytics_js'] = settings.GOOGLE_ANALYTICS_CODE

    return {}

def googleanalyticsjs(parser, token):
    return ShowGoogleAnalyticsJS()

show_common_data = register.tag(googleanalyticsjs)
