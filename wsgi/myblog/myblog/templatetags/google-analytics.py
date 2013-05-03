from django import template
from django.conf import settings
register = template.Library()

# Usage:
# Define GOOGLE_ANALYTICS_CODE in your settings. 
# In your base template put: {% google_analytics %}

@register.simple_tag
def google_analytics():
    code =  getattr(settings, "GOOGLE_ANALYTICS_ID", False)
    
    if not code:
        return "<!-- Goggle Analytics not included because no Google Analytics ID is defined -->"

    return u"""
    <script type="text/javascript">
      var _gaq = _gaq || [];
      _gaq.push(['_setAccount', '%s']);
      _gaq.push(['_trackPageview']);
      (function() {
        var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
        ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
        var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
      })();
    </script>
    """ % code