# -*- coding: utf-8 -*-
import logging
from .mirror_argparser import build_parser

log = logging.getLogger('streamlink.liveproxy-server')


# copy of - from .utils import ignored
@contextmanager
def ignored(*exceptions):
    try:
        yield
    except exceptions:
        pass


def setup_args(parser, arglist=[], config_files=[], ignore_unknown=True):
    '''Parses arguments.'''

    # Load arguments from config files
    for config_file in filter(os.path.isfile, config_files):
        arglist.insert(0, '@' + config_file)

    args, unknown = parser.parse_known_args(arglist)
    if unknown and not ignore_unknown:
        msg = gettext('unrecognized arguments: %s')
        parser.error(msg % ' '.join(unknown))

    # Force lowercase to allow case-insensitive lookup
    if args.stream:
        args.stream = [stream.lower() for stream in args.stream]

    if not args.url and args.url_param:
        args.url = args.url_param
    return args


def setup_config_args(session, args, parser, arglist):
    config_files = []

    if args.url:
        with ignored(NoPluginError):
            plugin = session.resolve_url(args.url)
            config_files += ['{0}.{1}'.format(fn, plugin.module) for fn in CONFIG_FILES]

    if args.config:
        # We want the config specified last to get highest priority
        config_files += list(reversed(args.config))
    else:
        # Only load first available default config
        for config_file in filter(os.path.isfile, CONFIG_FILES):
            config_files.append(config_file)
            break

    if config_files:
        args = setup_args(parser, arglist, config_files, ignore_unknown=True)
    return args


def setup_http_session(session, args):
    '''Sets the global HTTP settings, such as proxy and headers.'''
    if args.http_proxy:
        session.set_option('http-proxy', args.http_proxy)

    if args.https_proxy:
        session.set_option('https-proxy', args.https_proxy)

    if args.http_cookie:
        session.set_option('http-cookies', dict(args.http_cookie))

    if args.http_header:
        session.set_option('http-headers', dict(args.http_header))

    if args.http_query_param:
        session.set_option('http-query-params', dict(args.http_query_param))

    if args.http_ignore_env:
        session.set_option('http-trust-env', False)

    if args.http_no_ssl_verify:
        session.set_option('http-ssl-verify', False)

    if args.http_disable_dh:
        session.set_option('http-disable-dh', True)

    if args.http_ssl_cert:
        session.set_option('http-ssl-cert', args.http_ssl_cert)

    if args.http_ssl_cert_crt_key:
        session.set_option('http-ssl-cert', tuple(args.http_ssl_cert_crt_key))

    if args.http_timeout:
        session.set_option('http-timeout', args.http_timeout)

    if args.http_cookies:
        session.set_option('http-cookies', args.http_cookies)

    if args.http_headers:
        session.set_option('http-headers', args.http_headers)

    if args.http_query_params:
        session.set_option('http-query-params', args.http_query_params)


def setup_options(session, args):
    '''Sets streamlink options.'''
    if args.hls_live_edge:
        session.set_option('hls-live-edge', args.hls_live_edge)

    if args.hls_segment_attempts:
        session.set_option('hls-segment-attempts', args.hls_segment_attempts)

    if args.hls_playlist_reload_attempts:
        session.set_option('hls-playlist-reload-attempts', args.hls_playlist_reload_attempts)

    if args.hls_segment_threads:
        session.set_option('hls-segment-threads', args.hls_segment_threads)

    if args.hls_segment_timeout:
        session.set_option('hls-segment-timeout', args.hls_segment_timeout)

    if args.hls_segment_ignore_names:
        session.set_option('hls-segment-ignore-names', args.hls_segment_ignore_names)

    if args.hls_timeout:
        session.set_option('hls-timeout', args.hls_timeout)

    if args.hls_audio_select:
        session.set_option('hls-audio-select', args.hls_audio_select)

    if args.hls_start_offset:
        session.set_option('hls-start-offset', args.hls_start_offset)

    if args.hls_duration:
        session.set_option('hls-duration', args.hls_duration)

    if args.hls_live_restart:
        session.set_option('hls-live-restart', args.hls_live_restart)

    if args.hds_live_edge:
        session.set_option('hds-live-edge', args.hds_live_edge)

    if args.hds_segment_attempts:
        session.set_option('hds-segment-attempts', args.hds_segment_attempts)

    if args.hds_segment_threads:
        session.set_option('hds-segment-threads', args.hds_segment_threads)

    if args.hds_segment_timeout:
        session.set_option('hds-segment-timeout', args.hds_segment_timeout)

    if args.hds_timeout:
        session.set_option('hds-timeout', args.hds_timeout)

    if args.http_stream_timeout:
        session.set_option('http-stream-timeout', args.http_stream_timeout)

    if args.ringbuffer_size:
        session.set_option('ringbuffer-size', args.ringbuffer_size)

    if args.rtmp_proxy:
        session.set_option('rtmp-proxy', args.rtmp_proxy)

    if args.rtmp_rtmpdump:
        session.set_option('rtmp-rtmpdump', args.rtmp_rtmpdump)

    if args.rtmp_timeout:
        session.set_option('rtmp-timeout', args.rtmp_timeout)

    if args.stream_segment_attempts:
        session.set_option('stream-segment-attempts', args.stream_segment_attempts)

    if args.stream_segment_threads:
        session.set_option('stream-segment-threads', args.stream_segment_threads)

    if args.stream_segment_timeout:
        session.set_option('stream-segment-timeout', args.stream_segment_timeout)

    if args.stream_timeout:
        session.set_option('stream-timeout', args.stream_timeout)

    if args.ffmpeg_ffmpeg:
        session.set_option('ffmpeg-ffmpeg', args.ffmpeg_ffmpeg)
    if args.ffmpeg_verbose:
        session.set_option('ffmpeg-verbose', args.ffmpeg_verbose)
    if args.ffmpeg_verbose_path:
        session.set_option('ffmpeg-verbose-path', args.ffmpeg_verbose_path)
    if args.ffmpeg_video_transcode:
        session.set_option('ffmpeg-video-transcode', args.ffmpeg_video_transcode)
    if args.ffmpeg_audio_transcode:
        session.set_option('ffmpeg-audio-transcode', args.ffmpeg_audio_transcode)

    session.set_option('subprocess-errorlog', args.subprocess_errorlog)
    session.set_option('subprocess-errorlog-path', args.subprocess_errorlog_path)
    session.set_option('locale', args.locale)


def setup_plugin_args(session, parser):
    '''Sets Streamlink plugin options.'''

    plugin_args = parser.add_argument_group('Plugin options')
    for pname, plugin in session.plugins.items():
        defaults = {}
        for parg in plugin.arguments:
            plugin_args.add_argument(parg.argument_name(pname), **parg.options)
            defaults[parg.dest] = parg.default

        plugin.options = PluginOptions(defaults)


def setup_plugin_options(session, args, plugin):
    '''Sets Streamlink plugin options.'''
    pname = plugin.module
    required = OrderedDict({})
    for parg in plugin.arguments:
        if parg.required:
            required[parg.name] = parg
        value = getattr(args, parg.namespace_dest(pname))
        session.set_plugin_option(pname, parg.dest, value)
        # if the value is set, check to see if any of the required arguments are not set
        if parg.required or value:
            try:
                for rparg in plugin.arguments.requires(parg.name):
                    required[rparg.name] = rparg
            except RuntimeError:
                log.error('{0} plugin has a configuration error and the arguments '
                          'cannot be parsed'.format(pname))
                break
    if required:
        for req in required.values():
            if not session.get_plugin_option(pname, req.dest):
                log.error('Missing required {0} for {1}'.format(req.name, pname))


class HTTPRequest(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        log.debug('%s - %s\n' % (self.address_string(), format % args))

    def _headers(self, status, content):
        self.send_response(status)
        self.send_header('Server', 'LiveProxy')
        self.send_header('Content-type', content)
        self.end_headers()

    def do_HEAD(self):
        '''Respond to a HEAD request.'''
        self._headers(404, 'text/html')

    def do_GET(self):
        '''Respond to a GET request.'''
        if self.path.startswith('/play/'):
            main_play(self)
        elif self.path.startswith('/301/'):
            main_play(self, redirect=True)
        else:
            self._headers(404, 'text/html')


class Server(HTTPServer):
    '''HTTPServer class with timeout.'''
    timeout = 5


class ThreadedHTTPServer(ThreadingMixIn, Server):
    '''Handle requests in a separate thread.'''
    daemon_threads = True


__all__ = [
    'HTTPRequest',
    'ThreadedHTTPServer',
]
