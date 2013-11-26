
// i: globals (window)
// s: doc (document)
// o: str_script ('script')
// g: analystics_js_url ('//www.goog...')
// r: str_ga ('ga')
// a: ? -- ga_script
// m: ? -- first_script

(function(globals, doc, str_script, analytics_js_url, str_ga, a, m){
    globals['GoogleAnalyticsObject'] = str_ga
    globals[str_ga] = globals[str_ga] || function() {
        (globals[str_ga].q = globals[str_ga].q || []).push(arguments)
    },
    globals[str_ga].l = 1 * new Date()
    ga_script = doc.createElement(str_script),
    first_script = doc.getElementsByTagName(str_script)[0]
    ga_script.async = 1
    ga_script.src = analytics_js_url
    first_script.parentNode.insertBefore(ga_script, first_script)
})(window, document, 'script', '//www.google-analytics.com/analytics.js', 'ga');



