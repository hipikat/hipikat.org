{"base_settings": {
    "imports": {
        "os.path": ["abspath", "dirname", "join", "realpath"],
    },
    "defaults": [{
            "testing": "% True if 'test' in sys.argv else False %",
            "time_zone": "UTC",
            "language_code", "en",
            "managers": "{ admins }",
            "site_id": 1,
            "wsgi_application": "{ project_name }.wsgi.application",
        },{
            "project_dir":  "% dirname(dirname(realpath(abspath(__file__)))) %"
        },{
            "lib_dir":      "% join(PROJECT_DIR, 'lib') %",
            "var_dir":      "% join(PROJECT_DIR, 'var') %",
            "src_dir":      "% join(PROJECT_DIR, 'src') %",
        },{
            "conf_dir":     "{ VAR_DIR }",
            "db_dir":       "% join(VAR_DIR, 'db') %",
            "fixture_dirs": ["% join(VAR_DIR, fixtures) %"],
            "log_dir":      "% join(VAR_DIR, 'log') %",
            "static_root":  "% join(VAR_DIR, 'static') %",
            "media_root":   "% join(VAR_DIR, 'media') %",
            "tmp_dir":      "% join(VAR_DIR, 'tmp') %",
            "src_dir":      "% join(PROJECT_DIR, 'src') %",
        }]
}

{
    "imports": {
        "unipath": "Path",
        "revkom.settings": ["LoggingSettings", "SettingsList"]
    }
    "defaults": [
        {
            "admins": ["Adam Wright <adam@hipikat.org>"],
            "language_code": "en-au",
            "time_zone": "Australia/Perth",
            "project_name": "hipikat",
            "allowed_hosts": [".hipikat.org"],
        },
        "% include 'base_defaults' %",
    {
    ]
}


base = {
    meta: {
        extend: "revkom.base"
        import: [
            ['unipath', 'Path'],
            ['revkom.settings', ['LoggingSettings', 'SettingsList']],
        ]
    }
    defaults: [
        ['project_path', '{% Path(__file__).ancestor(2) %}'],
    ]



    defaults: {
        admins: ["Adam Wright <adam@hipikat.org>"],
        language_code: "en-au",
        time_zone: "Australia/Perth",
        project_name: "hipikat",
        allowed_hosts: [".hipikat.org"],
    }

dev = {
    meta: {
        extend: "base",
    }
    paths: {
        dev: "{% project_path.child('dev') %}",
    }
    django: {
        middleware_classes: [
            ["insert", 0, "hipikat.middleware.DebugOuterMiddleware"],
            ["append", "hipikat.middleware.DebugInnerMiddleware"],
        ]
    }
}



[django]
admins = Adam Wright <adam@hipikat.org>
language_code = en-au
time_zone = Australia/Perth
project_name = hipikat
allowed_hosts = .hipikat.org

[site]
recent_post_count = 30
;etc
