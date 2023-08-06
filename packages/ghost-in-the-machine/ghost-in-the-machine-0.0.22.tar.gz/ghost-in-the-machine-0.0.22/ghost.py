# [`ghost`][1] Copyright @[Angelo Gladding][2] 2020-
# %[Creative Commons Attribution 4.0 International][3]
#
# [1]: https://angelogladding.com/code/ghost
# [2]: https://angelogladding.com
# [3]: https://creativecommons.org/licenses/by/4.0

"""Manage your digital presence."""

import argparse
import base64
import configparser
try:
    import dns.resolver
except ImportError:
    pass
import getpass
import inspect
import json
import os
import pathlib
import random
import shutil
import sys
import textwrap
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
import xml.etree.ElementTree

try:
    import feedparser
    import semver
    from understory import web
    from understory.web import tx
except ImportError:
    web = None

__all__ = ["main", "app", "Ghost"]

LOGO = """\
  _|_|_|  _|                              _|
_|        _|_|_|      _|_|      _|_|_|  _|_|_|_|
_|  _|_|  _|    _|  _|    _|  _|_|        _|
_|    _|  _|    _|  _|    _|      _|_|    _|
  _|_|_|  _|    _|    _|_|    _|_|_|        _|_|"""

STARTED = False
DHPARAM_BITS = 512  # FIXME 4096 for production (perform in bg post install)
SSL_CIPHERS = ":".join(("ECDHE-RSA-AES256-GCM-SHA512",
                        "DHE-RSA-AES256-GCM-SHA512",
                        "ECDHE-RSA-AES256-GCM-SHA384",
                        "DHE-RSA-AES256-GCM-SHA384",
                        "ECDHE-RSA-AES256-SHA384"))
APTITUDE_PACKAGES = (
    "build-essential",  # build tools
    "expect",  # ssh password automation
    "psmisc",  # killall
    "xz-utils", "zip",  # .xz/.zip support
    "git", "fcgiwrap",  # Git w/ HTTP serving
    "supervisor",  # service manager
    "redis-server",  # Redis key-value database
    "haveged",  # produces entropy for faster key generation
    # XXX "sqlite3",  # SQLite flat-file relational database
    "libicu-dev", "python3-icu",  # SQLite unicode collation
    "libsqlite3-dev",  # SQLite Python extension loading
    "libssl-dev",  # uWSGI SSL support
    "cargo",  # rust (pycryptography)
    "libffi-dev",  # rust (pycryptography)
    "zlib1g-dev", "python3-dev",  # Python build dependencies
    "python3-crypto",  # pycrypto
    "python3-libtorrent",  # libtorrent
    "ffmpeg",  # a/v en/de[code]
    "imagemagick",  # heic -> jpeg
    "libsm-dev", "python-opencv",  # opencv
    "libevent-dev",  # Tor
    "pandoc",  # markup translation
    "graphviz",  # graphing
    "libgtk-3-0", "libdbus-glib-1-2",  # Firefox
    "xvfb", "x11-utils",  # browser automation
    "libenchant-dev",  # pyenchant => sopel => bridging IRC
    "ufw",  # an Uncomplicated FireWall
    "tmux",  # automatable terminal multiplexer
)
VERSIONS = {"python": "3.9.2", "nginx": "1.18.0", "tor": "0.4.4.5",
            "firefox": "82.0", "geckodriver": "0.27.0"}


class Ghost:
    """The host of the machine."""

    def __init__(self, home_dir="/home/ghost"):
        """Return the ghost found in `home_dir`."""
        self.home_dir = pathlib.Path(home_dir)
        self.apps_dir = self.home_dir / "apps"
        self.sites_dir = self.home_dir / "sites"
        self.system_dir = self.home_dir / "system"
        self.bin_dir = self.system_dir / "bin"
        self.env_dir = self.system_dir / "env"
        self.etc_dir = self.system_dir / "etc"
        self.src_dir = self.system_dir / "src"
        self.var_dir = self.system_dir / "var"
        self.nginx_dir = self.system_dir / "nginx"

    def spawn(self):
        """Spawn sudoer `ghost`."""
        try:
            sh.adduser("ghost", "--disabled-login", "--gecos", "ghost")
        except sh.ErrorReturnCode_1:
            print("user `ghost` already exists!")
            # TODO test for sudo to provide detailed error message
        else:
            print("spawning sudoer `ghost`..")
            ssh_dir = self.home_dir / ".ssh"
            sh.mkdir(ssh_dir)
            sh.cp(".ssh/authorized_keys", ssh_dir)
            sh.chown("ghost:ghost", ssh_dir, "-R")
            sh.tee(sh.echo("ghost  ALL=NOPASSWD: ALL"),
                   "-a", "/etc/sudoers.d/01_ghost")

    def setup(self, digitalocean_token):
        """Set up the base system."""
        # TODO ensure in home directory
        print("setting up base system..")
        self.upgrade_system()
        self.setup_firewall()
        # XXX sh.sudo("/etc/init.d/redis-server", "stop")
        # XXX sh.sudo("systemctl", "disable", "redis")
        self.etc_dir.mkdir(parents=True, exist_ok=True)
        self.src_dir.mkdir(parents=True, exist_ok=True)
        self.setup_python()
        self.setup_nginx()
        self.setup_supervisor()
        self.setup_ghost(digitalocean_token)
        self.setup_tor()
        self.setup_firefox()
        self.setup_torbrowser()
        self.setup_geckodriver()

    def upgrade_system(self):
        """Upgrade aptitude and install new system-level dependencies."""
        apt = sh.sudo.bake("apt", _env=dict(os.environ,
                                            DEBIAN_FRONTEND="noninteractive"))
        log("updating")
        apt("update")
        log("upgrading")
        apt("dist-upgrade", "-yq")
        log("installing system packages")
        apt("install", "-yq", *APTITUDE_PACKAGES)

    def setup_firewall(self):
        """Wall off everything but SSH and web."""
        allow = sh.sudo.bake("ufw", "allow", "proto", "tcp",
                             "from", "any", "to", "any")
        allow.port("22")
        allow.port("80,443")
        sh.sudo("ufw", "--force", "enable")

    def setup_python(self):
        """
        Install Python (w/ SQLite extensions).

        Additionally create a virtual environment and the web package.

        """
        def get_python_sh():
            py_major_version = f"python{VERSIONS['python'].rpartition('.')[0]}"
            return sh.Command(str(self.bin_dir / py_major_version))

        try:
            get_python_sh()
        except sh.CommandNotFound:
            _version = VERSIONS["python"]
            self._build(f"python.org/ftp/python/{_version}/Python-{_version}"
                        f".tar.xz", "--enable-loadable-sqlite-extensions",
                        f"--prefix={self.system_dir}")

        if self.env_dir.exists():
            return
        log("creating virtual environment")
        get_python_sh()("-m", "venv", self.env_dir)
        sh.echo(textwrap.dedent("""\
            #!/usr/bin/env bash
            VENV=$1
            . ${VENV}/bin/activate
            shift 1
            exec "$@"
            deactivate"""), _out=f"{self.home_dir}/runinenv")
        sh.chmod("+x", self.home_dir / "runinenv")
        sh.sh(self.home_dir / "runinenv", self.env_dir, "pip", "install",
              "sh==1.11")

        log("installing SQLite")
        log("  downloading")
        sh.wget("https://www.sqlite.org/src/tarball/sqlite.tar.gz",
                _cwd=self.src_dir)
        log("  extracting")
        sh.tar("xf", "sqlite.tar.gz", _cwd=self.src_dir)
        sqlite_dir = self.src_dir / "sqlite"
        log("  configuring")
        sh.bash("./configure", _cwd=sqlite_dir)
        sh.make("sqlite3.c", _cwd=sqlite_dir)
        sh.git("clone", "https://github.com/coleifer/pysqlite3",
               _cwd=self.src_dir)
        pysqlite_dir = self.src_dir / "pysqlite3"
        sh.cp(sqlite_dir / "sqlite3.c", ".", _cwd=pysqlite_dir)
        sh.cp(sqlite_dir / "sqlite3.h", ".", _cwd=pysqlite_dir)
        sh.sh(self.home_dir / "runinenv", self.env_dir, "python", "setup.py",
              "build_static", _cwd=pysqlite_dir)
        sh.sh(self.home_dir / "runinenv", self.env_dir, "python", "setup.py",
              "install", _cwd=pysqlite_dir)

        log("installing Ghost")
        sh.sh(self.home_dir / "runinenv", self.env_dir, "pip", "install",
              "ghost-in-the-machine")

    def setup_nginx(self):
        """Install Nginx (w/ TLS, HTTPv2, RTMP) for web serving."""
        nginx_src = f"nginx-{VERSIONS['nginx']}"
        if (self.src_dir / nginx_src).exists():
            return
        sh.wget("https://github.com/sergey-dryabzhinsky/nginx-rtmp-module/"
                "archive/dev.zip", "-O", "nginx-rtmp-module.zip",
                _cwd=self.src_dir)
        sh.unzip("-qq", "nginx-rtmp-module.zip", _cwd=self.src_dir)
        self._build(f"nginx.org/download/{nginx_src}.tar.gz",
                    "--with-http_ssl_module", "--with-http_v2_module",
                    f"--add-module={self.src_dir}/nginx-rtmp-module-dev",
                    f"--prefix={self.nginx_dir}")
        sh.mkdir("-p", self.nginx_dir / "conf/conf.d")
        if not (self.nginx_dir / "conf/dhparam.pem").exists():
            self.generate_dhparam()
        with (self.nginx_dir / "conf/nginx.conf").open("w") as fp:
            fp.write(nginx_conf)

    def generate_dhparam(self):
        """
        Generate a unique Diffie-Hellman prime for Nginx.

        This functionality has been abstracted here in order to allow an
        administrator to regenerate a cloned system's dhparam.

        """
        log("generating a large prime for TLS..")
        sh.openssl("dhparam", "-out", self.nginx_dir / "conf/dhparam.pem",
                   DHPARAM_BITS)

    def setup_supervisor(self):
        """Initialize a supervisor configuration."""
        supervisor = configparser.ConfigParser()
        supervisor["program:nginx"] = {"autostart": "true",
                                       "command": (self.nginx_dir /
                                                   "sbin/nginx"),
                                       "stopsignal": "INT",
                                       "user": "root"}
        command = f"{self.home_dir}/runinenv {self.env_dir} loveliness"
        supervisor["program:loveliness"] = {"autostart": "true",
                                            "command": command,
                                            "stopsignal": "INT",
                                            "user": "ghost"}
        # TODO supervisor[f"program:tor"] = {"autostart": "true",
        # TODO                               "command": bin_dir / "tor",
        # TODO                               "stopsignal": "INT",
        # TODO                               "user": "ghost"}
        self._write_supervisor_conf("servers", supervisor)

    def setup_ghost(self, digitalocean_token):
        """Set up the ghost web app."""
        ip = sh.hostname("-I").split()[0]
        secret = "".join(random.choice("abcdefghjknprstuvxyz23456789")
                         for _ in range(6))
        ghost_app = "ghost:app"
        site_dir = self.sites_dir / ip
        site_dir.mkdir(parents=True, exist_ok=True)

        # use self-signed certificate as Let's Encrypt does not support IPs
        domain_cnf = configparser.ConfigParser()
        domain_cnf.optionxform = str
        domain_cnf["req"] = {"distinguished_name": "req_distinguished_name",
                             "prompt": "no"}
        domain_cnf["req_distinguished_name"] = {
            "countryName": "XX",
            "stateOrProvinceName": "N/A",
            "localityName": "N/A",
            "organizationName": "self-signed",
            "commonName": f"{ip}: self-signed"
        }
        with (site_dir / "domain.cnf").open("w") as fp:
            domain_cnf.write(fp)
        sh.openssl("req", "-x509", "-nodes", "-days", "365",
                   "-newkey", "rsa:2048", "-keyout", site_dir / "domain.key",
                   "-out", site_dir / "domain.crt",
                   "-config", site_dir / "domain.cnf")

        self.save_config({"secret": secret,
                          "tokens": {"digitalocean": digitalocean_token,
                                     "dynadot": "", "github": ""},
                          "websites": {}})
        self.mount_site(ip, ghost_app)
        print()
        print("You may now sign in to your host while installation continues:")
        print(f"    https://{ip}?secret={secret}")
        print()

    def setup_tor(self):
        """Install Tor for anonymous hosting."""
        tor_dir = f"tor-{VERSIONS['tor']}"
        if (self.src_dir / tor_dir).exists():
            return
        self._build(f"dist.torproject.org/{tor_dir}.tar.gz",
                    f"--prefix={self.system_dir}")
        sh.mkdir("-p", self.var_dir / "tor")

    def setup_firefox(self):
        """Install Firefox for web browsing."""
        firefox_dir = f"firefox-{VERSIONS['firefox']}"
        if (self.src_dir / firefox_dir).exists():
            return
        log(f"installing firefox-{VERSIONS['firefox']}")
        sh.wget(f"https://archive.mozilla.org/pub/firefox/releases"
                f"/{VERSIONS['firefox']}/linux-x86_64/en-US"
                f"/{firefox_dir}.tar.bz2", _cwd=self.src_dir)
        sh.tar("xf", f"{firefox_dir}.tar.bz2", _cwd=self.src_dir)
        sh.mv("firefox", firefox_dir, _cwd=self.src_dir)
        sh.ln("-s", self.src_dir / firefox_dir / "firefox", self.bin_dir)

    def setup_torbrowser(self):  # TODO
        """Install Tor Browser for web browsing over Tor."""

    def setup_geckodriver(self):
        """Install geckodriver for driving gecko-based browsers."""
        geckodriver_dir = f"geckodriver-v{VERSIONS['geckodriver']}-linux64"
        if (self.src_dir / geckodriver_dir).exists():
            return
        log(f"installing geckodriver-{VERSIONS['geckodriver']}")
        sh.wget(f"https://github.com/mozilla/geckodriver/releases/download"
                f"/v{VERSIONS['geckodriver']}/{geckodriver_dir}.tar.gz",
                _cwd=self.src_dir)
        sh.tar("xf", f"{geckodriver_dir}.tar.gz", _cwd=self.src_dir)
        sh.mkdir("-p", geckodriver_dir, _cwd=self.src_dir)
        sh.mv("geckodriver", geckodriver_dir, _cwd=self.src_dir)
        sh.ln("-s", self.src_dir / geckodriver_dir / "geckodriver",
              self.bin_dir)

    def mount_site(self, site, app):
        """Instruct Nginx to route requests for `site` to `app`."""
        if app not in get_statuses():
            self.run_app(app)
        config = self.get_config()
        config["websites"][site] = app
        self.save_config(config)
        with (self.nginx_dir / f"conf/conf.d/{site}-app.conf").open("w") as fp:
            fp.write(nginx_site_app_conf.format(site=site,
                                                app=app.replace(":", "-"),
                                                ssl_ciphers=SSL_CIPHERS))
        sh.sudo("supervisorctl", "restart", "nginx")

    def run_app(self, app, workers=2):
        """Instruct Supervisor to run given `app` using gunicorn."""
        supervisor = configparser.ConfigParser()
        name = app.replace(":", "-")
        app_dir = self.apps_dir / name
        app_dir.mkdir(parents=True, exist_ok=True)
        command = (f"{self.home_dir}/runinenv {self.env_dir} gunicorn {app}"
                   f" -k gevent -w {workers} --bind unix:{app_dir}/app.sock")
        supervisor[f"program:{name}"] = {"autostart": "true",
                                         "command": command,
                                         "directory": app_dir,
                                         "environment": "PYTHONUNBUFFERED=1",
                                         "stopsignal": "INT", "user": "ghost"}
        self._write_supervisor_conf(f"app-{name}", supervisor)

    def _build(self, archive_url, *config_args):
        archive_filename = archive_url.rpartition("/")[2]
        archive_stem = archive_filename
        for ext in (".gz", ".xz", ".bz2", ".tar"):
            if archive_stem.endswith(ext):
                archive_stem = archive_stem[:-len(ext)]
        archive_file = self.src_dir / archive_filename
        archive_dir = self.src_dir / archive_stem
        if not (archive_file.exists() and archive_dir.exists()):
            log(f"installing {archive_stem.capitalize().replace('-', ' ')}")
        if not archive_file.exists():
            log("  downloading")
            tries = 0
            while True:
                try:
                    sh.wget(f"https://{archive_url}", _cwd=self.src_dir)
                except sh.ErrorReturnCode_1:
                    tries += 1
                    if tries == 3:
                        raise  # fail with traceback for bug reporting
                    time.sleep(3)
                    continue
                break
        if not archive_dir.exists():
            log("  extracting")
            sh.tar("xf", archive_filename, _cwd=self.src_dir)
            log("  configuring")
            sh.bash("./configure", *config_args, _cwd=archive_dir)
            log("  making")
            sh.make(_cwd=archive_dir)
            log("  installing")
            sh.make("install", _cwd=archive_dir)

    def _write_supervisor_conf(self, name, config):
        conf = self.etc_dir / f"{name}.conf"
        with conf.open("w") as fp:
            config.write(fp)
        sh.sudo("ln", "-sf", conf.resolve(),
                f"/etc/supervisor/conf.d/{name}.conf")
        sh.sudo("supervisorctl", "reread")
        sh.sudo("supervisorctl", "update")

    def get_config(self):
        """Return a dictionary containing ghost configuration."""
        config = pathlib.Path(self.home_dir / "config.json")
        try:
            with config.open() as fp:
                config = json.load(fp)
        except FileNotFoundError:
            config = {}
        return config

    def save_config(self, data):
        """Store `data` as ghost configuration."""
        config = pathlib.Path(self.home_dir / "config.json")
        with config.open("w") as fp:
            json.dump(data, fp)


if web:
    app = web.application("ghost", sessions=True,
                          service=r"(digitalocean|dynadot)",
                          site=r"[a-z0-9-.]{4,128}",
                          pkg=r"[a-z-]+", app_path=r"[a-z0-9-:.]{4,128}")
    app.mount(web.indie.indieauth.client)
    app.wrap(web.indie.indieauth.wrap_server, "post")
else:
    class DummyWebApp:
        def f(self, _):
            return lambda _: None
        wrap = route = f
    app = DummyWebApp()


def get_ip():
    return sh.hostname("-I").split()[0]


lol_html = """$def with (logo)
<!doctype html>
<style>
body {
    background-color: #002b36;
    color: #839496;
    margin: 4em; }
a {
    color: #268bd2; }
</style>
<pre>$logo</pre>
<p><big><code>wget <a href=/ghost.py>gh.ost.lol/ghost.py</a> -q
&& python3 ghost.py</code></big></p>
"""


@app.wrap
def contextualize(handler, app):
    if tx.request.uri.host == "gh.ost.lol":
        if tx.request.uri.path == "":
            web.header("Content-Type", "text/html")
            body = web.template(lol_html)(LOGO)
        elif tx.request.uri.path == "ghost.py":
            web.header("Content-Type", "text/python")
            with open(__file__) as fp:
                body = fp.read()
        else:
            raise web.NotFound()
        raise web.OK(body)
    tx.ghost = Ghost()
    yield


@app.route(r"")
class Main:
    """Admin interface."""

    def _get(self):
        self.handle_auth()
        system_hostname = sh.hostname("--fqdn")
        system_uptime = sh.uptime()
        config = tx.ghost.get_config()
        sites = []
        for site in tx.ghost.sites_dir.iterdir():
            url = web.uri(site.name)
            try:
                a_record = str(dns.resolver.resolve(site.name, "A")[0])
            except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
                a_record = None
            try:
                ns_records = [str(r) for r in
                              dns.resolver.resolve(site.name, "NS")]
            except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
                ns_records = []
            certified = (site / "domain.crt").exists()
            preloaded = web.in_hsts_preload(site.name)
            sites.append((url.suffix, url.domain, url.subdomain, site,
                          a_record, ns_records, certified, preloaded))
        tokens = config["tokens"]
        dynadot_token = tokens.get("dynadot")
        if dynadot_token:
            dynadot_domains = dict(Dynadot(dynadot_token).list_domain())
        else:
            dynadot_domains = {}
        apps = {}
        for package, applications in web.get_apps().items():
            name = package.metadata["Name"]
            current_version = package.metadata["Version"]
            versions = f"https://pypi.org/rss/project/{name}/releases.xml"
            latest_version = feedparser.parse(versions)["entries"][0]["title"]
            update_available = None
            if semver.compare(current_version, latest_version):
                update_available = latest_version
            apps[package] = (update_available, applications)
        return web.template(html)(system_hostname, get_ip(),
                                  system_uptime, sites, dynadot_domains,
                                  apps, get_statuses(), config)

    def handle_auth(self):
        secret = web.form(secret=None).secret
        if secret:
            if secret == tx.ghost.get_config()["secret"]:
                web.tx.user.session["signed_in"] = True
                raise web.SeeOther("/")
            raise web.Unauthorized("bad secret")
        elif not web.tx.user.session.get("signed_in", False):
            raise web.Unauthorized("please sign in with your secret")


def get_statuses():
    statuses = {}
    for line in sh.sudo("supervisorctl", "status"):
        if "STARTING" in str(line):
            time.sleep(.5)
            continue
        try:
            app, status, _, pid = line.split()[:4]
        except ValueError:
            print(f"Can't parse statuses: {line}")
            break
        uptime = line.partition(" uptime ")[2]
        statuses[app.replace("-", ":")] = status, pid, uptime
    return statuses


@app.route(r"tokens/{service}")
class Token:
    """Update the locally cached Dynadot API token."""

    def _post(self):
        token = web.form("token").token
        config = tx.ghost.get_config()
        if token:
            config["tokens"][self.service] = token
        else:
            del config["tokens"][self.service]
        tx.ghost.save_config(config)
        raise web.SeeOther("/")


@app.route(r"sites")
class Websites:
    """Installed sites."""

    def _post(self):
        site = web.form("site").site
        if not web.uri(site).suffix:
            return "unknown suffix"
        (tx.ghost.sites_dir / site).mkdir()
        raise web.SeeOther("/")


@app.route(r"sites/{site}")
class Website:
    """Installed site."""

    def _delete(self):
        shutil.rmtree(tx.ghost.sites_dir / self.site)
        raise web.SeeOther("/")


@app.route(r"sites/{site}/dns")
class WebsiteDNS:
    """Site A record."""

    def _post(self):
        do = DigitalOcean(tx.ghost.get_config()["tokens"]["digitalocean"])
        site = web.uri(self.site)
        domain_name = f"{site.domain}.{site.suffix}"
        ip = get_ip()
        if site.subdomain:
            digitalocean_domains = [d["name"] for d in
                                    do.get_domains()["domains"]]
            if self.site in digitalocean_domains:
                do.create_domain_record(domain_name, site.subdomain, ip)
        else:
            try:
                do.create_domain(domain_name, get_ip())
            except DomainExistsError:
                for record in do.get_domain_records(domain_name):
                    if record["name"] == "@" and record["type"] == "A":
                        break
                do.update_domain_record(domain_name, record["id"], data=ip)
        raise web.SeeOther("/")


@app.route(r"sites/{site}/certificate")
class WebsiteCertificate:
    """Site certificate."""

    def _post(self):
        site_dir = tx.ghost.sites_dir / self.site
        with (tx.ghost.nginx_dir / "conf/conf.d" /
              f"{self.site}.conf").open("w") as fp:
            fp.write(nginx_site_tls_conf.format(site=self.site))
        sh.sudo("supervisorctl", "restart", "nginx")
        web.generate_cert(self.site, site_dir, site_dir)
        raise web.SeeOther("/")


@app.route(r"sites/{site}/mount")
class WebsiteMount:
    """Site mount."""

    def _post(self):
        app = web.form("app").app
        tx.ghost.mount_site(self.site, app)
        raise web.SeeOther("/")


@app.route(r"apps")
class Applications:
    """Installed applications."""

    def _post(self):
        app = web.form("app").app
        # XXX owner, _, name = app.partition("/")
        # XXX app = app.removeprefix("https://")
        # XXX if "." in app.partition("/")[0]:
        # XXX     app_url = f"https://{app}"
        # XXX else:
        # XXX     if "/" in app:
        # XXX         owner, _, name = app.partition("/")
        # XXX     else:
        # XXX         owner = name = app
        # XXX     token = tx.ghost.get_config()["tokens"]["github"]
        # XXX     if token:
        # XXX         token += "@"
        # XXX     app_url = (f"git+https://{token}github.com/{owner}/{name}"
        # XXX                f".git#egg={name}")
        # XXX sh.sh("runinenv", "system/env", "pip", "install", "-e",
        # XXX       app_url, _cwd=tx.ghost.home_dir)
        sh.sh("runinenv", "system/env", "pip", "install", app,
              _cwd=tx.ghost.home_dir)
        sh.sudo("supervisorctl", "restart", "ghost-app", _bg=True)
        raise web.SeeOther("/")


@app.route(r"apps/{pkg}")
class Package:
    """Installed application package."""

    def _post(self):
        sh.sh("runinenv", "system/env", "pip", "install", "-U", self.pkg,
              _cwd=tx.ghost.home_dir)
        sh.sudo("supervisorctl", "restart", "ghost-app", _bg=True)
        raise web.SeeOther("/")


@app.route(r"apps/{app_path}")
class Application:
    """Installed application."""

    def _post(self):
        tx.ghost.run_app(self.app)
        raise web.SeeOther("/")


class DomainExistsError(Exception):
    """Domain already exists."""


nginx_conf = """\
daemon            off;
worker_processes  auto;

events {
    worker_connections  1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;

    types_hash_max_size  2048;
    sendfile             on;
    tcp_nopush           on;
    tcp_nodelay          on;
    keepalive_timeout    65;
    server_tokens        off;

    gzip          on;
    gzip_disable  "msie6";

    access_log  /home/ghost/system/nginx/logs/access.log;
    error_log   /home/ghost/system/nginx/logs/error.log;

    log_format  ghostfmt  '$remote_addr [$time_local] "$request" $status '
                          '$request_time $bytes_sent "$http_referer" '
                          '"$http_user_agent" "$sent_http_set_cookie"';

    include /home/ghost/system/nginx/conf/conf.d/*.conf;
}

rtmp {
    # Define where the HLS files will be written. Viewers will be fetching
    # these files from the browser, so the `location /hls` above points to
    # this folder as well
    hls on;
    hls_path /home/ghost/streaming/hls;
    hls_fragment 5s;

    # Enable recording archived files of each stream
    # Does not need to be publicly accessible, will convert and publish later
    record all;
    record_path /home/ghost/streaming/rec;
    record_suffix _%Y-%m-%d_%H-%M-%S.flv;
    record_lock on;

    # Define the two scripts that will run when recording starts and when
    # it finishes
    exec_publish /home/ghost/streaming/publish.sh;
    exec_record_done /home/ghost/streaming/finished.sh $path $basename.mp4;

    access_log /home/ghost/system/nginx/logs/rtmp_access.log combined;
    access_log on;

    server {
        listen 1935;
        chunk_size 4096;

        application rtmp {
            live on;
            record all;
        }
    }
}"""

nginx_site_tls_conf = """
server {{
    listen       80;
    server_name  {site};

    location  /.well-known/acme-challenge/  {{
        alias      /home/ghost/sites/{site}/;
        try_files  $uri  =404;
    }}
    location  /  {{
        return  308  https://{site}$request_uri;
    }}
}}"""

nginx_site_app_conf = """
server {{
    listen       443  ssl  http2;
    listen       [::]:443  ssl  http2;
    server_name  {site};

    ssl_certificate            /home/ghost/sites/{site}/domain.crt;
    ssl_certificate_key        /home/ghost/sites/{site}/domain.key;
    ssl_protocols              TLSv1.3;
    ssl_prefer_server_ciphers  off;
    ssl_ciphers                {ssl_ciphers};
    ssl_session_cache          shared:SSL:10m;
    ssl_session_timeout        1d;
    ssl_dhparam                /home/ghost/system/nginx/conf/dhparam.pem;
    ssl_ecdh_curve             secp384r1;
    ssl_session_tickets        off;
    ssl_stapling               on;
    ssl_stapling_verify        on;
    resolver                   8.8.8.8  8.8.4.4  valid=300s;  # TODO !google
    resolver_timeout           5s;

    charset     utf-8;
    add_header  X-Powered-By  "canopy";
    add_header  X-Frame-Options  "SAMEORIGIN";
    add_header  X-Content-Type-Options  "nosniff";

    # TODO security headers
    # add_header  Strict-Transport-Security  "max-age=15768000"  always;
    # add_header  Strict-Transport-Security
    #             "max-age=63072000; includeSubDomains; preload";
    # add_header  X-Frame-Options  DENY;
    # add_header  X-XSS-Protection  "1; mode=block";
    # add_header  Content-Security-Policy  "require-sri-for script style;"

    client_max_body_size  100M;
    error_page            403 404          /error/40x.html;
    error_page            500 502 503 504  /error/50x.html;
    access_log            /home/ghost/apps/{app}/access.log  ghostfmt;
    error_log             /home/ghost/apps/{app}/error.log   info;

    # TODO: error and static Nginx locations
    # location  /error/  {{
    #     internal;
    #     alias  ../canopy/;
    # }}
    # location  /static/  {{
    #     add_header  Access-Control-Allow-Origin  *;
    #     root  ../canopy/__web__;
    # }}

    location /X/ {{
        internal;
        alias  /home/ghost/apps/{app}/;
    }}

    location  /  {{
        proxy_set_header  X-Forwarded-Proto  $scheme;
        proxy_set_header  Host  $http_host;
        proxy_set_header  X-Forwarded-For  $proxy_add_x_forwarded_for;
        proxy_redirect  off;
        proxy_pass  http://unix:/home/ghost/apps/{app}/app.sock;

        # XXX uwsgi_param  Host  $http_host;
        # XXX uwsgi_param  X-Real-IP  $remote_addr;
        # XXX uwsgi_param  X-Forwarded-For  $proxy_add_x_forwarded_for;
        # XXX uwsgi_max_temp_file_size  0;
        # XXX uwsgi_pass  unix:/home/ghost/apps/{app}/app.sock;
        # XXX include  /home/ghost/system/nginx/conf/uwsgi_params;
    }}
}}"""

html = """$def with (hostname, ip_address, system_uptime, sites,\
                     dynadot_domains, apps, statuses, config)
<!doctype html>
<style>
body {
    background-color: #002b36;
    color: #839496;
    font-family: Inconsolata, "Ubuntu Mono", monospace;
    margin: 2em; }
header {
    display: grid;
    grid-column-gap: 1em;
    grid-template-columns: auto auto; }
header h1 {
    margin: 0; }
header p {
    margin: 0; }
#tokens {
    text-align: right; }
#tokens > div {
    margin: .25em 0; }
#tokens input[type=text] {
    padding: .075em; }
a:link {
    color: #268bd2; }
a:visited {
    color: #6c71c4; }
a:active {
    color: #dc322f; }
div.button {
    text-align: right; }
button, input, select {
    font-family: Inconsolata, "Ubuntu Mono", monospace; }
button {
    padding: .075em .5em; }
button, select {
    background-color: #2aa198;
    border: 0;
    color: #002b36;
    text-transform: uppercase; }
input[type=text], select {
    background-color: #073642;
    border: 0;
    color: #839496; }
ul {
    list-style: none;
    padding-left: 0; }
#setup {
    display: grid;
    grid-column-gap: 1em;
    grid-template-columns: 1fr 1fr; }
#setup input[type=text] {
    width: 100%; }
#websites li > div {
    display: grid;
    grid-column-gap: 0;
    grid-template-columns: auto auto; }
// div.domain:nth-child(odd) { background-color: #073642; }
// div.domain:nth-child(even) { background: #; }

.input_submit {
    display: grid;
    grid-column-gap: .5em;
    grid-template-columns: auto min-content; }
</style>
<title>$hostname</title>

<header>
<div>
<h1><code>$hostname</code></h1>
<p><code>$ip_address<br><small>$system_uptime</small></code></p>
</div>
<div id=tokens>
<div id=digitalocean>
    <form action=/tokens/digitalocean method=post>
    <label><strong>DigitalOcean</strong>
    <input type=text name=token
        value="$config['tokens']['digitalocean']"></label>
    <button>Set</button>
    </form>
</div>
<div id=dynadot>
    <form action=/tokens/dynadot method=post>
    <label><strong>Dynadot</strong>
    <input type=text name=token value="$config['tokens']['dynadot']"></label>
    <button>Set</button>
    </form>
</div>
<div id=dynadot>
    <form action=/tokens/github method=post>
    <label><strong>GitHub</strong>
    <input type=text name=token value="$config['tokens']['github']"></label>
    <button>Set</button>
    </form>
</div>
</div>
</header>

<section id=setup>

<div id=applications>
<h2>Applications</h2>
<form action=/apps method=post>
    <label for=app><strong>Package</strong><br>
    <small>PyPI (eg. <kbd>canopy</kbd>) or
    Repository URL (eg. <kbd>example.org/foo.git</kbd>) or
    GitHub Path (eg. <kbd>example/foo</kbd>)</small></label>
    <div class=input_submit>
        <input id=app type=text name=app></label>
        <button>Install</button>
    </div>
</form>
$for package, (update_available, applications) in sorted(apps.items()):
    $ meta = package.metadata
    <h3>$meta["Name"] <small>$meta["Version"]</small></h3>
    <p>$meta["Summary"]
    $if "Project-URL" in meta:
        <a href=$meta["Project-URL"]>more</a>
    </p>
    $ license = meta["License"]
    <p><small>By <a href=$meta["Author-email"]>$meta["Author"]</a>, licensed <a
    href=https://spdx.org/licenses/$(license).html>$license</a></small></p>
    $if update_available:
        <form action=/apps/$meta["Name"] method=post>
        <button>Upgrade to $update_available</button>
        </form>
    <ul>
    $for appns, _, mod_name, attrs in applications:
        $ app = f"{mod_name}:{attrs[0]}"
        <li><form action=/apps/$app method=post>
        $appns<br><small>$app</small>
        $if app in statuses:
            <small style=color:#859900>\
            $" ".join(statuses[app]).lower()</small>
        </form></li>
    </ul>
</div>

<div id=websites>
<h2>Websites</h2>
<form action=/sites method=post>
    <label for=site><strong>Hostname</strong><br>
    <small>Domain (eg. <kbd>example.org</kbd>) or
    Subdomain (eg. <kbd>foo.example.org</kbd>)</small></label>
    <div class=input_submit>
        <input id=site type=text name=site>
        <button>Add</button>
    </div>
</form>
<ul>
$for suffix, domain, subdomain, site, a_record, ns_records, \
certified, preloaded in sorted(sites):
    $ show_point_ns = False
    $ show_point_a = False
    $ show_certify = False
    $ show_nothing = False
    <li>
    <h3>$site.name</h3>
    <div>
    <div>
    $ site_app = config["websites"].get(site.name)
    $if site_app:
        <small style=color:#859900>
        $site_app is mounted
        $if preloaded:
            <br><abbr title="HTTP Strict Transport Security">HSTS</abbr>
            is preloaded
        </small>
    $else:
        $ points = a_record == ip_address
        $if points:
            <small style=color:#$("859900" if points else "dc322f");>\\
            <code>$a_record</code></small><br>
            $if certified:
                <small style=color:#859900;><abbr
                title="Transport Layer Security">TLS</abbr>
                enabled</small><br>
                <small style=color:#$("859900" if preloaded else "dc322f")>
                <abbr title="HTTP Strict Transport Security">HSTS</abbr>
                $("" if preloaded else "not") preloaded</small><br>
            $else:
                <small style=color:#dc322f;><abbr
                title="Transport Layer Security">TLS</abbr>
                not enabled</small><br>
                $ show_certify = True
        $else:
            <small style=color:#dc322f>
            $if a_record is None:
                no A record<br>
            $else:
                $a_record<br>
            $if "ns1.digitalocean.com." not in ns_records:
                current nameservers: <code>$", ".join(ns_records)</code><br>
                $if domain + "." + suffix in dynadot_domains:
                    $ show_point_ns = True
                $else:
                    cannot continue (\\
                    $ show_nothing = True
                    $if config["tokens"]["dynadot"]:
                        domain not found in Dynadot account)<br>
                    $else:
                        no Dynadot access)<br>
            $else:
                $ show_point_a = True
            </small>
    </div>
    <div>
        $if show_point_ns:
            <form action=/sites/$site.name/dns method=post>
            <div class=button><button>Point to DigitalOcean</button></div>
            </form>
        $elif show_point_a:
            <form action=/sites/$site.name/dns method=post>
            <div class=button><button>Point here</button></div>
            </form>
        $elif show_certify:
            <form action=/sites/$site.name/certificate method=post>
            <div class=button><button>Certify</button></div>
            </form>
        $elif show_nothing:
            $pass
        $elif not site_app:
            <form action=/sites/$site.name/mount method=post>
            <select name=app required>
            <option value="" disabled selected>Choose application..</option>
            $for package, (_, applications) in sorted(apps.items()):
                $for appns, __, mod_name, attrs in applications:
                    <option value="$(mod_name):$attrs[0]">$appns
                    $if f"{mod_name}:{attrs[0]}" in statuses:
                        (running)
                    </option>
            </select>
            <div class=button><button>Mount</button></div>
            </form>
            $# TODO HSTS preload
        $if site.name != ip_address:
            <form action=/sites/$site.name method=delete>
            <input type=hidden name=_http_method value=delete>
            <div class=button><button>Delete</button></div>
            </form>
    </div>
    </div>
    </li>
</ul>
</div>
</section>
"""


# XXX sh.ssh_copy_id("-f", "-i", "key", "-o", "IdentityFile=sshkeyfile",
# XXX                "root@server.name")


def get_key(do):
    """Return a SSH key, registering it with DigitalOcean if necessary."""
    key_path = pathlib.Path("ghost_key.pub")
    try:
        with key_path.open() as fp:
            key_data = fp.read().strip()
    except FileNotFoundError:
        sh.ssh_keygen("-o", "-a", "100", "-t", "ed25519", "-N", "",
                      "-f", str(key_path)[:-4])
        with key_path.open() as fp:
            key_data = fp.read().strip()
        key = do.add_key("ghost", key_data)
    else:
        for key in do.get_keys()["ssh_keys"]:
            if key["public_key"] == key_data:
                break
        else:
            key = do.add_key("ghost", key_data)
    return key


def get_ssh(user, ip_address):
    """Return a function for executing commands over SSH."""
    def process_out(line):
        if "?secret=" in line:
            secret = line.partition("=")[2]
            # TODO osx appends a trailing newline (?)
            webbrowser.open(f"https://{ip_address}?secret={secret}")
        print(line, end="", flush=True)

    def ssh(*command, env=None):
        kwargs = {}
        if env:
            kwargs["_env"] = env
        # TODO do you need -tt ??
        return sh.ssh("-i", "ghost_key", "-tt", "-o", "IdentitiesOnly=yes",
                      "-o", "StrictHostKeyChecking no", f"{user}@{ip_address}",
                      *command, _out=process_out, **kwargs)

    tries = 20
    while tries:
        if tries == 18:
            print("..waiting for server to come alive..", end="")
            # TODO use log here if possible
        try:
            ssh("true")
        except sh.ErrorReturnCode_255:
            print(".", end="", flush=True)
        else:
            break
        time.sleep(2)
        tries -= 1
    else:
        print(" couldn't connect!")
        # TODO raise an error here instead..
    print()
    return ssh


def wait(do, droplet_id):
    while (do.get_droplet_actions(droplet_id)[0]["status"] == "in-progress"):
        time.sleep(1)


class DigitalOcean:
    """Interface the DigitalOcean service."""

    endpoint = "https://api.digitalocean.com/v2/"

    def __init__(self, key, debug=False):
        self.key = str(key)
        self.debug = debug

    def get_keys(self):
        return self._get("account/keys")

    def add_key(self, name, key_data):
        data = {"name": name, "public_key": key_data}
        return self._post("account/keys", **data)["ssh_key"]

    def get_domains(self):
        return self._get("domains")

    def create_domain(self, domain, address):
        data = {"name": domain, "ip_address": address}
        try:
            response = self._post("domains", **data)
        except urllib.error.HTTPError as err:
            if err.code == 422:
                raise DomainExistsError()
        return response

    def create_domain_record(self, domain, subdomain,
                             record_data, record_type="A"):
        data = {"name": subdomain, "data": record_data, "type": record_type}
        return self._post(f"domains/{domain}/records", **data)

    def get_domain_records(self, domain):
        return self._get(f"domains/{domain}/records")["domain_records"]

    def update_domain_record(self, domain, record, **kwargs):
        return self._put(f"domains/{domain}/records/{record}",
                         **kwargs)["domain_record"]

    def get_droplets(self):
        return self._get("droplets")

    def get_droplet(self, droplet_id):
        return self._get(f"droplets/{droplet_id}")["droplet"]

    def create_droplet(self, name, region="sfo2", size="s-1vcpu-1gb",
                       image="debian-10-x64", ssh_keys=None, tags=None):
        data = {"name": name, "region": region, "size": size,
                "image": image, "ssh_keys": ssh_keys, "tags": tags}
        return self._post("droplets", **data)["droplet"]

    def delete_droplet(self, droplet_id):
        return self._delete(f"droplets/{droplet_id}")

    def get_droplet_actions(self, droplet_id):
        return self._get(f"droplets/{droplet_id}/actions")["actions"]

    def shutdown_droplet(self, droplet_id):
        data = {"type": "shutdown"}
        return self._post(f"droplets/{droplet_id}/actions", **data)["action"]

    def get_snapshots_of_droplets(self):
        return self._get("snapshots", resource_type="droplet")

    def get_droplet_snapshots(self, droplet_id):
        return self._get(f"droplets/{droplet_id}/snapshots")["snapshots"]

    def take_snapshot(self, droplet_id, name):
        data = {"type": "snapshot", "name": name}
        return self._post(f"droplets/{droplet_id}/actions", **data)["action"]

    def get_images(self):
        return self._get("images", per_page=200)

    def _get(self, path, **args):
        return self._request("get", path, data=args)

    def _post(self, path, **args):
        return self._request("post", path, data=args)

    def _put(self, path, **args):
        return self._request("put", path, data=args)

    def _delete(self, path, **args):
        return self._request("delete", path, data=args)

    def _request(self, method, path, data=None):
        """Send an API request."""
        url = self.endpoint + path
        args = {"method": method.upper(),
                "headers": {"Authorization": "Bearer " + self.key}}
        if method in ("post", "put", "delete"):
            args["headers"].update({"Content-Type": "application/json"})
        if data:
            if method == "get":
                url += "?" + urllib.parse.urlencode(data)
            else:
                args["data"] = json.dumps(data).encode()
        req = urllib.request.Request(url, **args)
        response = urllib.request.urlopen(req)
        if method == "delete":
            response = True if response.status == 204 else False
        else:
            response = json.loads(response.read())
        if self.debug:
            print(">>", method, path)
            print(">>", response)
        return response


class Dynadot:
    """Interface the Dynadot service."""

    endpoint = "https://api.dynadot.com/api3.xml"

    def __init__(self, key):
        self.key = key

    def list_domain(self):
        """List currently registered domains."""
        response = self._request()
        domains = []
        for domain in response[1][0]:
            name = domain[0].find("Name").text
            expiration = domain[0].find("Expiration").text
            domains.append((name, expiration))
        return domains

    def search(self, *domains):
        """Search for available of domains."""
        domain_params = {"domain{}".format(n): domain
                         for n, domain in enumerate(domains)}
        response = self._request(show_price="1", **domain_params)
        results = {}
        for result in response:
            # if len(result[0]) == 5:
            # data = {"price": result[0][4].text}
            # results[result[0][1].text] = data
            available = (False if result[0].find("Available").text == "no"
                         else True)
            price = result[0].find("Price")
            if price is None:
                price = 0
            else:
                if " in USD" in price.text:
                    price = float(price.text.partition(" ")[0])
                else:
                    price = "?"
            results[result[0].find("DomainName").text] = (available, price)
        return results

    def register(self, domain, duration=1):
        """Register domain."""
        response = self._request(domain=domain, duration=duration)
        return response

    def account_info(self):
        """Return account information."""
        response = self._request()[1][0]
        return response

    def _request(self, **payload):
        """Send an API request."""
        payload.update(command=inspect.stack()[1].function, key=self.key)
        response = urllib.request.urlopen(self.endpoint + "?" +
                                          urllib.parse.urlencode(payload))
        message = xml.etree.ElementTree.fromstring(response.read())
        if message.find("ResponseCode").text == "-1":
            raise web.BadRequest("bad Dynadot token")
        return message


# `python-sh v1.12.14` Copyright (c) 2011- Andrew Moffat
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

sh_py = """\
IiIiCmh0dHA6Ly9hbW9mZmF0LmdpdGh1Yi5pby9zaC8KIiIiCiM9PT09PT09PT09PT09PT09PT09P
T09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT
09CiMgQ29weXJpZ2h0IChDKSAyMDExLTIwMTcgYnkgQW5kcmV3IE1vZmZhdAojCiMgUGVybWlzc2l
vbiBpcyBoZXJlYnkgZ3JhbnRlZCwgZnJlZSBvZiBjaGFyZ2UsIHRvIGFueSBwZXJzb24gb2J0YWlu
aW5nIGEgY29weQojIG9mIHRoaXMgc29mdHdhcmUgYW5kIGFzc29jaWF0ZWQgZG9jdW1lbnRhdGlvb
iBmaWxlcyAodGhlICJTb2Z0d2FyZSIpLCB0byBkZWFsCiMgaW4gdGhlIFNvZnR3YXJlIHdpdGhvdX
QgcmVzdHJpY3Rpb24sIGluY2x1ZGluZyB3aXRob3V0IGxpbWl0YXRpb24gdGhlIHJpZ2h0cwojIHR
vIHVzZSwgY29weSwgbW9kaWZ5LCBtZXJnZSwgcHVibGlzaCwgZGlzdHJpYnV0ZSwgc3VibGljZW5z
ZSwgYW5kL29yIHNlbGwKIyBjb3BpZXMgb2YgdGhlIFNvZnR3YXJlLCBhbmQgdG8gcGVybWl0IHBlc
nNvbnMgdG8gd2hvbSB0aGUgU29mdHdhcmUgaXMKIyBmdXJuaXNoZWQgdG8gZG8gc28sIHN1YmplY3
QgdG8gdGhlIGZvbGxvd2luZyBjb25kaXRpb25zOgojCiMgVGhlIGFib3ZlIGNvcHlyaWdodCBub3R
pY2UgYW5kIHRoaXMgcGVybWlzc2lvbiBub3RpY2Ugc2hhbGwgYmUgaW5jbHVkZWQgaW4KIyBhbGwg
Y29waWVzIG9yIHN1YnN0YW50aWFsIHBvcnRpb25zIG9mIHRoZSBTb2Z0d2FyZS4KIwojIFRIRSBTT
0ZUV0FSRSBJUyBQUk9WSURFRCAiQVMgSVMiLCBXSVRIT1VUIFdBUlJBTlRZIE9GIEFOWSBLSU5ELC
BFWFBSRVNTIE9SCiMgSU1QTElFRCwgSU5DTFVESU5HIEJVVCBOT1QgTElNSVRFRCBUTyBUSEUgV0F
SUkFOVElFUyBPRiBNRVJDSEFOVEFCSUxJVFksCiMgRklUTkVTUyBGT1IgQSBQQVJUSUNVTEFSIFBV
UlBPU0UgQU5EIE5PTklORlJJTkdFTUVOVC4gSU4gTk8gRVZFTlQgU0hBTEwgVEhFCiMgQVVUSE9SU
yBPUiBDT1BZUklHSFQgSE9MREVSUyBCRSBMSUFCTEUgRk9SIEFOWSBDTEFJTSwgREFNQUdFUyBPUi
BPVEhFUgojIExJQUJJTElUWSwgV0hFVEhFUiBJTiBBTiBBQ1RJT04gT0YgQ09OVFJBQ1QsIFRPUlQ
gT1IgT1RIRVJXSVNFLCBBUklTSU5HIEZST00sCiMgT1VUIE9GIE9SIElOIENPTk5FQ1RJT04gV0lU
SCBUSEUgU09GVFdBUkUgT1IgVEhFIFVTRSBPUiBPVEhFUiBERUFMSU5HUyBJTgojIFRIRSBTT0ZUV
0FSRS4KIz09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT
09PT09PT09PT09PT09PT09PT09PT09PT09PT0KCgpfX3ZlcnNpb25fXyA9ICIxLjEyLjE0IgpfX3B
yb2plY3RfdXJsX18gPSAiaHR0cHM6Ly9naXRodWIuY29tL2Ftb2ZmYXQvc2giCgoKaW1wb3J0IHBs
YXRmb3JtCgppZiAid2luZG93cyIgaW4gcGxhdGZvcm0uc3lzdGVtKCkubG93ZXIoKTogIyBwcmFnb
WE6IG5vIGNvdmVyCiAgICByYWlzZSBJbXBvcnRFcnJvcigic2ggJXMgaXMgY3VycmVudGx5IG9ubH
kgc3VwcG9ydGVkIG9uIGxpbnV4IGFuZCBvc3guIFwKcGxlYXNlIGluc3RhbGwgcGJzIDAuMTEwICh
odHRwOi8vcHlwaS5weXRob24ub3JnL3B5cGkvcGJzKSBmb3Igd2luZG93cyBcCnN1cHBvcnQuIiAl
IF9fdmVyc2lvbl9fKQoKCmltcG9ydCBzeXMKSVNfUFkzID0gc3lzLnZlcnNpb25faW5mb1swXSA9P
SAzCk1JTk9SX1ZFUiA9IHN5cy52ZXJzaW9uX2luZm9bMV0KSVNfUFkyNiA9IHN5cy52ZXJzaW9uX2
luZm9bMF0gPT0gMiBhbmQgTUlOT1JfVkVSID09IDYKCmltcG9ydCB0cmFjZWJhY2sKaW1wb3J0IG9
zCmltcG9ydCByZQppbXBvcnQgdGltZQppbXBvcnQgZ2V0cGFzcwpmcm9tIHR5cGVzIGltcG9ydCBN
b2R1bGVUeXBlLCBHZW5lcmF0b3JUeXBlCmZyb20gZnVuY3Rvb2xzIGltcG9ydCBwYXJ0aWFsCmltc
G9ydCBpbnNwZWN0CmltcG9ydCB0ZW1wZmlsZQppbXBvcnQgc3RhdAppbXBvcnQgZ2xvYiBhcyBnbG
9iX21vZHVsZQppbXBvcnQgYXN0CmZyb20gY29udGV4dGxpYiBpbXBvcnQgY29udGV4dG1hbmFnZXI
KaW1wb3J0IHB3ZAppbXBvcnQgZXJybm8KZnJvbSBpbyBpbXBvcnQgVW5zdXBwb3J0ZWRPcGVyYXRp
b24sIG9wZW4gYXMgZmRvcGVuCgpmcm9tIGxvY2FsZSBpbXBvcnQgZ2V0cHJlZmVycmVkZW5jb2Rpb
mcKREVGQVVMVF9FTkNPRElORyA9IGdldHByZWZlcnJlZGVuY29kaW5nKCkgb3IgIlVURi04IgoKIy
Bub3JtYWxseSBpIHdvdWxkIGhhdGUgdGhpcyBpZGVhIG9mIHVzaW5nIGEgZ2xvYmFsIHRvIHNpZ25
pZnkgd2hldGhlciB3ZSBhcmUKIyBydW5uaW5nIHRlc3RzLCBiZWNhdXNlIGl0IGJyZWFrcyB0aGUg
YXNzdW1wdGlvbiB0aGF0IHdoYXQgaXMgcnVubmluZyBpbiB0aGUKIyB0ZXN0cyBpcyB3aGF0IHdpb
GwgcnVuIGxpdmUsIGJ1dCB3ZSBPTkxZIHVzZSB0aGlzIGluIGEgcGxhY2UgdGhhdCBoYXMgbm8KIy
BzZXJpb3VzIHNpZGUtZWZmZWN0cyB0aGF0IGNvdWxkIGNoYW5nZSBhbnl0aGluZy4gIGFzIGxvbmc
gYXMgd2UgZG8gdGhhdCwgaXQKIyBzaG91bGQgYmUgb2sKUlVOTklOR19URVNUUyA9IGJvb2woaW50
KG9zLmVudmlyb24uZ2V0KCJTSF9URVNUU19SVU5OSU5HIiwgIjAiKSkpCkZPUkNFX1VTRV9TRUxFQ
1QgPSBib29sKGludChvcy5lbnZpcm9uLmdldCgiU0hfVEVTVFNfVVNFX1NFTEVDVCIsICIwIikpKQ
oKaWYgSVNfUFkzOgogICAgZnJvbSBpbyBpbXBvcnQgU3RyaW5nSU8KICAgIGlvU3RyaW5nSU8gPSB
TdHJpbmdJTwogICAgZnJvbSBpbyBpbXBvcnQgQnl0ZXNJTyBhcyBjU3RyaW5nSU8KICAgIGlvY1N0
cmluZ0lPID0gY1N0cmluZ0lPCiAgICBmcm9tIHF1ZXVlIGltcG9ydCBRdWV1ZSwgRW1wdHkKCiAgI
CAjIGZvciBzb21lIHJlYXNvbiwgcHl0aG9uIDMuMSByZW1vdmVkIHRoZSBidWlsdGluICJjYWxsYW
JsZSIsIHd0ZgogICAgaWYgbm90IGhhc2F0dHIoX19idWlsdGluc19fLCAiY2FsbGFibGUiKToKICA
gICAgICBkZWYgY2FsbGFibGUob2IpOgogICAgICAgICAgICByZXR1cm4gaGFzYXR0cihvYiwgIl9f
Y2FsbF9fIikKZWxzZToKICAgIGZyb20gU3RyaW5nSU8gaW1wb3J0IFN0cmluZ0lPCiAgICBmcm9tI
GNTdHJpbmdJTyBpbXBvcnQgT3V0cHV0VHlwZSBhcyBjU3RyaW5nSU8KICAgIGZyb20gaW8gaW1wb3
J0IFN0cmluZ0lPIGFzIGlvU3RyaW5nSU8KICAgIGZyb20gaW8gaW1wb3J0IEJ5dGVzSU8gYXMgaW9
jU3RyaW5nSU8KICAgIGZyb20gUXVldWUgaW1wb3J0IFF1ZXVlLCBFbXB0eQoKSVNfT1NYID0gcGxh
dGZvcm0uc3lzdGVtKCkgPT0gIkRhcndpbiIKVEhJU19ESVIgPSBvcy5wYXRoLmRpcm5hbWUob3Muc
GF0aC5yZWFscGF0aChfX2ZpbGVfXykpClNIX0xPR0dFUl9OQU1FID0gX19uYW1lX18KCgppbXBvcn
QgZXJybm8KaW1wb3J0IHB0eQppbXBvcnQgdGVybWlvcwppbXBvcnQgc2lnbmFsCmltcG9ydCBnYwp
pbXBvcnQgc2VsZWN0CmltcG9ydCB0aHJlYWRpbmcKaW1wb3J0IHR0eQppbXBvcnQgZmNudGwKaW1w
b3J0IHN0cnVjdAppbXBvcnQgcmVzb3VyY2UKZnJvbSBjb2xsZWN0aW9ucyBpbXBvcnQgZGVxdWUKa
W1wb3J0IGxvZ2dpbmcKaW1wb3J0IHdlYWtyZWYKCgojIGEgcmUtZW50cmFudCBsb2NrIGZvciBwdX
NoZC4gIHRoaXMgd2F5LCBtdWx0aXBsZSB0aHJlYWRzIHRoYXQgaGFwcGVuIHRvIHVzZQojIHB1c2h
kIHdpbGwgYWxsIHNlZSB0aGUgY3VycmVudCB3b3JraW5nIGRpcmVjdG9yeSBmb3IgdGhlIGR1cmF0
aW9uIG9mIHRoZQojIHdpdGgtY29udGV4dApQVVNIRF9MT0NLID0gdGhyZWFkaW5nLlJMb2NrKCkKC
gppZiBoYXNhdHRyKGluc3BlY3QsICJnZXRmdWxsYXJnc3BlYyIpOgogICAgZGVmIGdldF9udW1fYX
Jncyhmbik6CiAgICAgICAgcmV0dXJuIGxlbihpbnNwZWN0LmdldGZ1bGxhcmdzcGVjKGZuKS5hcmd
zKQplbHNlOgogICAgZGVmIGdldF9udW1fYXJncyhmbik6CiAgICAgICAgcmV0dXJuIGxlbihpbnNw
ZWN0LmdldGFyZ3NwZWMoZm4pLmFyZ3MpCgppZiBJU19QWTM6CiAgICByYXdfaW5wdXQgPSBpbnB1d
AogICAgdW5pY29kZSA9IHN0cgogICAgYmFzZXN0cmluZyA9IHN0cgogICAgbG9uZyA9IGludAoKCl
91bmljb2RlX21ldGhvZHMgPSBzZXQoZGlyKHVuaWNvZGUoKSkpCgoKSEFTX1BPTEwgPSBoYXNhdHR
yKHNlbGVjdCwgInBvbGwiKQpQT0xMRVJfRVZFTlRfUkVBRCA9IDEKUE9MTEVSX0VWRU5UX1dSSVRF
ID0gMgpQT0xMRVJfRVZFTlRfSFVQID0gNApQT0xMRVJfRVZFTlRfRVJST1IgPSA4CgoKIyBoZXJlI
HdlIHVzZSBhbiB1c2UgYSBwb2xsZXIgaW50ZXJmYWNlIHRoYXQgdHJhbnNwYXJlbnRseSBzZWxlY3
RzIHRoZSBtb3N0CiMgY2FwYWJsZSBwb2xsZXIgKG91dCBvZiBlaXRoZXIgc2VsZWN0LnNlbGVjdCB
vciBzZWxlY3QucG9sbCkuICB0aGlzIHdhcyBhZGRlZAojIGJ5IHpoYW5neWFmZWlraW1pIHdoZW4g
aGUgZGlzY292ZXJlZCB0aGF0IGlmIHRoZSBmZHMgY3JlYXRlZCBpbnRlcm5hbGx5IGJ5IHNoCiMgb
nVtYmVyZWQgPiAxMDI0LCBzZWxlY3Quc2VsZWN0IGZhaWxlZCAoYSBsaW1pdGF0aW9uIG9mIHNlbG
VjdC5zZWxlY3QpLiAgdGhpcwojIGNhbiBoYXBwZW4gaWYgeW91ciBzY3JpcHQgb3BlbnMgYSBsb3Q
gb2YgZmlsZXMKaWYgSEFTX1BPTEwgYW5kIG5vdCBGT1JDRV9VU0VfU0VMRUNUOgogICAgY2xhc3Mg
UG9sbGVyKG9iamVjdCk6CiAgICAgICAgZGVmIF9faW5pdF9fKHNlbGYpOgogICAgICAgICAgICBzZ
WxmLl9wb2xsID0gc2VsZWN0LnBvbGwoKQogICAgICAgICAgICAjIGZpbGUgZGVzY3JpcHRvciA8LT
4gZmlsZSBvYmplY3QgYmlkaXJlY3Rpb25hbCBtYXBzCiAgICAgICAgICAgIHNlbGYuZmRfbG9va3V
wID0ge30KICAgICAgICAgICAgc2VsZi5mb19sb29rdXAgPSB7fQoKICAgICAgICBkZWYgX19ub256
ZXJvX18oc2VsZik6CiAgICAgICAgICAgIHJldHVybiBsZW4oc2VsZi5mZF9sb29rdXApICE9IDAKC
iAgICAgICAgZGVmIF9fbGVuX18oc2VsZik6CiAgICAgICAgICAgIHJldHVybiBsZW4oc2VsZi5mZF
9sb29rdXApCgogICAgICAgIGRlZiBfc2V0X2ZpbGVvYmplY3Qoc2VsZiwgZik6CiAgICAgICAgICA
gIGlmIGhhc2F0dHIoZiwgImZpbGVubyIpOgogICAgICAgICAgICAgICAgZmQgPSBmLmZpbGVubygp
CiAgICAgICAgICAgICAgICBzZWxmLmZkX2xvb2t1cFtmZF0gPSBmCiAgICAgICAgICAgICAgICBzZ
WxmLmZvX2xvb2t1cFtmXSA9IGZkCiAgICAgICAgICAgIGVsc2U6CiAgICAgICAgICAgICAgICBzZW
xmLmZkX2xvb2t1cFtmXSA9IGYKICAgICAgICAgICAgICAgIHNlbGYuZm9fbG9va3VwW2ZdID0gZgo
KICAgICAgICBkZWYgX3JlbW92ZV9maWxlb2JqZWN0KHNlbGYsIGYpOgogICAgICAgICAgICBpZiBo
YXNhdHRyKGYsICJmaWxlbm8iKToKICAgICAgICAgICAgICAgIGZkID0gZi5maWxlbm8oKQogICAgI
CAgICAgICAgICAgZGVsIHNlbGYuZmRfbG9va3VwW2ZkXQogICAgICAgICAgICAgICAgZGVsIHNlbG
YuZm9fbG9va3VwW2ZdCiAgICAgICAgICAgIGVsc2U6CiAgICAgICAgICAgICAgICBkZWwgc2VsZi5
mZF9sb29rdXBbZl0KICAgICAgICAgICAgICAgIGRlbCBzZWxmLmZvX2xvb2t1cFtmXQoKICAgICAg
ICBkZWYgX2dldF9maWxlX2Rlc2NyaXB0b3Ioc2VsZiwgZik6CiAgICAgICAgICAgIHJldHVybiBzZ
WxmLmZvX2xvb2t1cC5nZXQoZikKCiAgICAgICAgZGVmIF9nZXRfZmlsZV9vYmplY3Qoc2VsZiwgZm
QpOgogICAgICAgICAgICByZXR1cm4gc2VsZi5mZF9sb29rdXAuZ2V0KGZkKQoKICAgICAgICBkZWY
gX3JlZ2lzdGVyKHNlbGYsIGYsIGV2ZW50cyk6CiAgICAgICAgICAgICMgZiBjYW4gYmUgYSBmaWxl
IGRlc2NyaXB0b3Igb3IgZmlsZSBvYmplY3QKICAgICAgICAgICAgc2VsZi5fc2V0X2ZpbGVvYmplY
3QoZikKICAgICAgICAgICAgZmQgPSBzZWxmLl9nZXRfZmlsZV9kZXNjcmlwdG9yKGYpCiAgICAgIC
AgICAgIHNlbGYuX3BvbGwucmVnaXN0ZXIoZmQsIGV2ZW50cykKCiAgICAgICAgZGVmIHJlZ2lzdGV
yX3JlYWQoc2VsZiwgZik6CiAgICAgICAgICAgIHNlbGYuX3JlZ2lzdGVyKGYsIHNlbGVjdC5QT0xM
SU4gfCBzZWxlY3QuUE9MTFBSSSkKCiAgICAgICAgZGVmIHJlZ2lzdGVyX3dyaXRlKHNlbGYsIGYpO
gogICAgICAgICAgICBzZWxmLl9yZWdpc3RlcihmLCBzZWxlY3QuUE9MTE9VVCkKCiAgICAgICAgZG
VmIHJlZ2lzdGVyX2Vycm9yKHNlbGYsIGYpOgogICAgICAgICAgICBzZWxmLl9yZWdpc3RlcihmLCB
zZWxlY3QuUE9MTEVSUiB8IHNlbGVjdC5QT0xMSFVQIHwgc2VsZWN0LlBPTExOVkFMKQoKICAgICAg
ICBkZWYgdW5yZWdpc3RlcihzZWxmLCBmKToKICAgICAgICAgICAgZmQgPSBzZWxmLl9nZXRfZmlsZ
V9kZXNjcmlwdG9yKGYpCiAgICAgICAgICAgIHNlbGYuX3BvbGwudW5yZWdpc3RlcihmZCkKICAgIC
AgICAgICAgc2VsZi5fcmVtb3ZlX2ZpbGVvYmplY3QoZikKCiAgICAgICAgZGVmIHBvbGwoc2VsZiw
gdGltZW91dCk6CiAgICAgICAgICAgIGlmIHRpbWVvdXQgaXMgbm90IE5vbmU6CiAgICAgICAgICAg
ICAgICAjIGNvbnZlcnQgZnJvbSBzZWNvbmRzIHRvIG1pbGxpc2Vjb25kcwogICAgICAgICAgICAgI
CAgdGltZW91dCAqPSAxMDAwCiAgICAgICAgICAgIGNoYW5nZXMgPSBzZWxmLl9wb2xsLnBvbGwodG
ltZW91dCkKICAgICAgICAgICAgcmVzdWx0cyA9IFtdCiAgICAgICAgICAgIGZvciBmZCwgZXZlbnR
zIGluIGNoYW5nZXM6CiAgICAgICAgICAgICAgICBmID0gc2VsZi5fZ2V0X2ZpbGVfb2JqZWN0KGZk
KQogICAgICAgICAgICAgICAgaWYgZXZlbnRzICYgKHNlbGVjdC5QT0xMSU4gfCBzZWxlY3QuUE9MT
FBSSSk6CiAgICAgICAgICAgICAgICAgICAgcmVzdWx0cy5hcHBlbmQoKGYsIFBPTExFUl9FVkVOVF
9SRUFEKSkKICAgICAgICAgICAgICAgIGVsaWYgZXZlbnRzICYgKHNlbGVjdC5QT0xMT1VUKToKICA
gICAgICAgICAgICAgICAgICByZXN1bHRzLmFwcGVuZCgoZiwgUE9MTEVSX0VWRU5UX1dSSVRFKSkK
ICAgICAgICAgICAgICAgIGVsaWYgZXZlbnRzICYgKHNlbGVjdC5QT0xMSFVQKToKICAgICAgICAgI
CAgICAgICAgICByZXN1bHRzLmFwcGVuZCgoZiwgUE9MTEVSX0VWRU5UX0hVUCkpCiAgICAgICAgIC
AgICAgICBlbGlmIGV2ZW50cyAmIChzZWxlY3QuUE9MTEVSUiB8IHNlbGVjdC5QT0xMTlZBTCk6CiA
gICAgICAgICAgICAgICAgICAgcmVzdWx0cy5hcHBlbmQoKGYsIFBPTExFUl9FVkVOVF9FUlJPUikp
CiAgICAgICAgICAgIHJldHVybiByZXN1bHRzCmVsc2U6CiAgICBjbGFzcyBQb2xsZXIob2JqZWN0K
ToKICAgICAgICBkZWYgX19pbml0X18oc2VsZik6CiAgICAgICAgICAgIHNlbGYucmxpc3QgPSBbXQ
ogICAgICAgICAgICBzZWxmLndsaXN0ID0gW10KICAgICAgICAgICAgc2VsZi54bGlzdCA9IFtdCgo
gICAgICAgIGRlZiBfX25vbnplcm9fXyhzZWxmKToKICAgICAgICAgICAgcmV0dXJuIGxlbihzZWxm
LnJsaXN0KSArIGxlbihzZWxmLndsaXN0KSArIGxlbihzZWxmLnhsaXN0KSAhPSAwCgogICAgICAgI
GRlZiBfX2xlbl9fKHNlbGYpOgogICAgICAgICAgICByZXR1cm4gbGVuKHNlbGYucmxpc3QpICsgbG
VuKHNlbGYud2xpc3QpICsgbGVuKHNlbGYueGxpc3QpCgogICAgICAgIGRlZiBfcmVnaXN0ZXIoc2V
sZiwgZiwgbCk6CiAgICAgICAgICAgIGlmIGYgbm90IGluIGw6CiAgICAgICAgICAgICAgICBsLmFw
cGVuZChmKQoKICAgICAgICBkZWYgX3VucmVnaXN0ZXIoc2VsZiwgZiwgbCk6CiAgICAgICAgICAgI
GlmIGYgaW4gbDoKICAgICAgICAgICAgICAgIGwucmVtb3ZlKGYpCgogICAgICAgIGRlZiByZWdpc3
Rlcl9yZWFkKHNlbGYsIGYpOgogICAgICAgICAgICBzZWxmLl9yZWdpc3RlcihmLCBzZWxmLnJsaXN
0KQoKICAgICAgICBkZWYgcmVnaXN0ZXJfd3JpdGUoc2VsZiwgZik6CiAgICAgICAgICAgIHNlbGYu
X3JlZ2lzdGVyKGYsIHNlbGYud2xpc3QpCgogICAgICAgIGRlZiByZWdpc3Rlcl9lcnJvcihzZWxmL
CBmKToKICAgICAgICAgICAgc2VsZi5fcmVnaXN0ZXIoZiwgc2VsZi54bGlzdCkKCiAgICAgICAgZG
VmIHVucmVnaXN0ZXIoc2VsZiwgZik6CiAgICAgICAgICAgIHNlbGYuX3VucmVnaXN0ZXIoZiwgc2V
sZi5ybGlzdCkKICAgICAgICAgICAgc2VsZi5fdW5yZWdpc3RlcihmLCBzZWxmLndsaXN0KQogICAg
ICAgICAgICBzZWxmLl91bnJlZ2lzdGVyKGYsIHNlbGYueGxpc3QpCgogICAgICAgIGRlZiBwb2xsK
HNlbGYsIHRpbWVvdXQpOgogICAgICAgICAgICBfaW4sIF9vdXQsIF9lcnIgPSBzZWxlY3Quc2VsZW
N0KHNlbGYucmxpc3QsIHNlbGYud2xpc3QsIHNlbGYueGxpc3QsIHRpbWVvdXQpCiAgICAgICAgICA
gIHJlc3VsdHMgPSBbXQogICAgICAgICAgICBmb3IgZiBpbiBfaW46CiAgICAgICAgICAgICAgICBy
ZXN1bHRzLmFwcGVuZCgoZiwgUE9MTEVSX0VWRU5UX1JFQUQpKQogICAgICAgICAgICBmb3IgZiBpb
iBfb3V0OgogICAgICAgICAgICAgICAgcmVzdWx0cy5hcHBlbmQoKGYsIFBPTExFUl9FVkVOVF9XUk
lURSkpCiAgICAgICAgICAgIGZvciBmIGluIF9lcnI6CiAgICAgICAgICAgICAgICByZXN1bHRzLmF
wcGVuZCgoZiwgUE9MTEVSX0VWRU5UX0VSUk9SKSkKICAgICAgICAgICAgcmV0dXJuIHJlc3VsdHMK
CgpkZWYgZW5jb2RlX3RvX3B5M2J5dGVzX29yX3B5MnN0cihzKToKICAgICIiIiB0YWtlcyBhbnl0a
GluZyBhbmQgYXR0ZW1wdHMgdG8gcmV0dXJuIGEgcHkyIHN0cmluZyBvciBweTMgYnl0ZXMuICB0aG
lzCiAgICBpcyB0eXBpY2FsbHkgdXNlZCB3aGVuIGNyZWF0aW5nIGNvbW1hbmQgKyBhcmd1bWVudHM
gdG8gYmUgZXhlY3V0ZWQgdmlhCiAgICBvcy5leGVjKiAiIiIKCiAgICBmYWxsYmFja19lbmNvZGlu
ZyA9ICJ1dGY4IgoKICAgIGlmIElTX1BZMzoKICAgICAgICAjIGlmIHdlJ3JlIGFscmVhZHkgYnl0Z
XMsIGRvIG5vdGhpbmcKICAgICAgICBpZiBpc2luc3RhbmNlKHMsIGJ5dGVzKToKICAgICAgICAgIC
AgcGFzcwogICAgICAgIGVsc2U6CiAgICAgICAgICAgIHMgPSBzdHIocykKICAgICAgICAgICAgdHJ
5OgogICAgICAgICAgICAgICAgcyA9IGJ5dGVzKHMsIERFRkFVTFRfRU5DT0RJTkcpCiAgICAgICAg
ICAgIGV4Y2VwdCBVbmljb2RlRW5jb2RlRXJyb3I6CiAgICAgICAgICAgICAgICBzID0gYnl0ZXMoc
ywgZmFsbGJhY2tfZW5jb2RpbmcpCiAgICBlbHNlOgogICAgICAgICMgYXR0ZW1wdCB0byBjb252ZX
J0IHRoZSB0aGluZyB0byB1bmljb2RlIGZyb20gdGhlIHN5c3RlbSdzIGVuY29kaW5nCiAgICAgICA
gdHJ5OgogICAgICAgICAgICBzID0gdW5pY29kZShzLCBERUZBVUxUX0VOQ09ESU5HKQogICAgICAg
ICMgaWYgdGhlIHRoaW5nIGlzIGFscmVhZHkgdW5pY29kZSwgb3IgaXQncyBhIG51bWJlciwgaXQgY
2FuJ3QgYmUKICAgICAgICAjIGNvZXJjZWQgdG8gdW5pY29kZSB3aXRoIGFuIGVuY29kaW5nIGFyZ3
VtZW50LCBidXQgaWYgd2UgbGVhdmUgb3V0CiAgICAgICAgIyB0aGUgZW5jb2RpbmcgYXJndW1lbnQ
sIGl0IHdpbGwgY29udmVydCBpdCB0byBhIHN0cmluZywgdGhlbiB0byB1bmljb2RlCiAgICAgICAg
ZXhjZXB0IFR5cGVFcnJvcjoKICAgICAgICAgICAgcyA9IHVuaWNvZGUocykKCiAgICAgICAgIyBub
3cgdGhhdCB3ZSBoYXZlIGd1YXJhbnRlZWQgdW5pY29kZSwgZW5jb2RlIHRvIG91ciBzeXN0ZW0gZW
5jb2RpbmcsCiAgICAgICAgIyBidXQgYXR0ZW1wdCB0byBmYWxsIGJhY2sgdG8gc29tZXRoaW5nCiA
gICAgICAgdHJ5OgogICAgICAgICAgICBzID0gcy5lbmNvZGUoREVGQVVMVF9FTkNPRElORykKICAg
ICAgICBleGNlcHQ6CiAgICAgICAgICAgIHMgPSBzLmVuY29kZShmYWxsYmFja19lbmNvZGluZywgI
nJlcGxhY2UiKQogICAgcmV0dXJuIHMKCgpkZWYgX2luZGVudF90ZXh0KHRleHQsIG51bT00KToKIC
AgIGxpbmVzID0gW10KICAgIGZvciBsaW5lIGluIHRleHQuc3BsaXQoIlxuIik6CiAgICAgICAgbGl
uZSA9ICgiICIgKiBudW0pICsgbGluZQogICAgICAgIGxpbmVzLmFwcGVuZChsaW5lKQogICAgcmV0
dXJuICJcbiIuam9pbihsaW5lcykKCgpjbGFzcyBGb3JrRXhjZXB0aW9uKEV4Y2VwdGlvbik6CiAgI
CBkZWYgX19pbml0X18oc2VsZiwgb3JpZ19leGMpOgogICAgICAgIHRtcGwgPSAiIiIKCk9yaWdpbm
FsIGV4Y2VwdGlvbjoKPT09PT09PT09PT09PT09PT09PQoKJXMKIiIiCiAgICAgICAgbXNnID0gdG1
wbCAlIF9pbmRlbnRfdGV4dChvcmlnX2V4YykKICAgICAgICBFeGNlcHRpb24uX19pbml0X18oc2Vs
ZiwgbXNnKQoKCmNsYXNzIEVycm9yUmV0dXJuQ29kZU1ldGEodHlwZSk6CiAgICAiIiIgYSBtZXRhY
2xhc3Mgd2hpY2ggcHJvdmlkZXMgdGhlIGFiaWxpdHkgZm9yIGFuIEVycm9yUmV0dXJuQ29kZSAob3
IKICAgIGRlcml2ZWQpIGluc3RhbmNlLCBpbXBvcnRlZCBmcm9tIG9uZSBzaCBtb2R1bGUsIHRvIGJ
lIGNvbnNpZGVyZWQgdGhlCiAgICBzdWJjbGFzcyBvZiBFcnJvclJldHVybkNvZGUgZnJvbSBhbm90
aGVyIG1vZHVsZS4gIHRoaXMgaXMgbW9zdGx5IG5lY2Vzc2FyeQogICAgaW4gdGhlIHRlc3RzLCB3a
GVyZSB3ZSBkbyBhc3NlcnRSYWlzZXMsIGJ1dCB0aGUgRXJyb3JSZXR1cm5Db2RlIHRoYXQgdGhlCi
AgICBwcm9ncmFtIHdlJ3JlIHRlc3RpbmcgdGhyb3dzIG1heSBub3QgYmUgdGhlIHNhbWUgY2xhc3M
gdGhhdCB3ZSBwYXNzIHRvCiAgICBhc3NlcnRSYWlzZXMKICAgICIiIgogICAgZGVmIF9fc3ViY2xh
c3NjaGVja19fKHNlbGYsIG8pOgogICAgICAgIG90aGVyX2Jhc2VzID0gc2V0KFtiLl9fbmFtZV9fI
GZvciBiIGluIG8uX19iYXNlc19fXSkKICAgICAgICByZXR1cm4gc2VsZi5fX25hbWVfXyBpbiBvdG
hlcl9iYXNlcyBvciBvLl9fbmFtZV9fID09IHNlbGYuX19uYW1lX18KCgpjbGFzcyBFcnJvclJldHV
ybkNvZGUoRXhjZXB0aW9uKToKICAgIF9fbWV0YWNsYXNzX18gPSBFcnJvclJldHVybkNvZGVNZXRh
CgogICAgIiIiIGJhc2UgY2xhc3MgZm9yIGFsbCBleGNlcHRpb25zIGFzIGEgcmVzdWx0IG9mIGEgY
29tbWFuZCdzIGV4aXQgc3RhdHVzCiAgICBiZWluZyBkZWVtZWQgYW4gZXJyb3IuICB0aGlzIGJhc2
UgY2xhc3MgaXMgZHluYW1pY2FsbHkgc3ViY2xhc3NlZCBpbnRvCiAgICBkZXJpdmVkIGNsYXNzZXM
gd2l0aCB0aGUgZm9ybWF0OiBFcnJvclJldHVybkNvZGVfTk5OIHdoZXJlIE5OTiBpcyB0aGUgZXhp
dAogICAgY29kZSBudW1iZXIuICB0aGUgcmVhc29uIGZvciB0aGlzIGlzIGl0IHJlZHVjZXMgYm9pb
GVyIHBsYXRlIGNvZGUgd2hlbgogICAgdGVzdGluZyBlcnJvciByZXR1cm4gY29kZXM6CiAgICAKIC
AgICAgICB0cnk6CiAgICAgICAgICAgIHNvbWVfY21kKCkKICAgICAgICBleGNlcHQgRXJyb3JSZXR
1cm5Db2RlXzEyOgogICAgICAgICAgICBwcmludCgiY291bGRuJ3QgZG8gWCIpCiAgICAgICAgICAg
IAogICAgdnM6CiAgICAgICAgdHJ5OgogICAgICAgICAgICBzb21lX2NtZCgpCiAgICAgICAgZXhjZ
XB0IEVycm9yUmV0dXJuQ29kZSBhcyBlOgogICAgICAgICAgICBpZiBlLmV4aXRfY29kZSA9PSAxMj
oKICAgICAgICAgICAgICAgIHByaW50KCJjb3VsZG4ndCBkbyBYIikKICAgIAogICAgaXQncyBub3Q
gbXVjaCBvZiBhIHNhdmluZ3MsIGJ1dCBpIGJlbGlldmUgaXQgbWFrZXMgdGhlIGNvZGUgZWFzaWVy
IHRvIHJlYWQgIiIiCgogICAgdHJ1bmNhdGVfY2FwID0gNzUwCgogICAgZGVmIF9faW5pdF9fKHNlb
GYsIGZ1bGxfY21kLCBzdGRvdXQsIHN0ZGVyciwgdHJ1bmNhdGU9VHJ1ZSk6CiAgICAgICAgc2VsZi
5mdWxsX2NtZCA9IGZ1bGxfY21kCiAgICAgICAgc2VsZi5zdGRvdXQgPSBzdGRvdXQKICAgICAgICB
zZWxmLnN0ZGVyciA9IHN0ZGVycgoKICAgICAgICBleGNfc3Rkb3V0ID0gc2VsZi5zdGRvdXQKICAg
ICAgICBpZiB0cnVuY2F0ZToKICAgICAgICAgICAgZXhjX3N0ZG91dCA9IGV4Y19zdGRvdXRbOnNlb
GYudHJ1bmNhdGVfY2FwXQogICAgICAgICAgICBvdXRfZGVsdGEgPSBsZW4oc2VsZi5zdGRvdXQpIC
0gbGVuKGV4Y19zdGRvdXQpCiAgICAgICAgICAgIGlmIG91dF9kZWx0YToKICAgICAgICAgICAgICA
gIGV4Y19zdGRvdXQgKz0gKCIuLi4gKCVkIG1vcmUsIHBsZWFzZSBzZWUgZS5zdGRvdXQpIiAlIG91
dF9kZWx0YSkuZW5jb2RlKCkKCiAgICAgICAgZXhjX3N0ZGVyciA9IHNlbGYuc3RkZXJyCiAgICAgI
CAgaWYgdHJ1bmNhdGU6CiAgICAgICAgICAgIGV4Y19zdGRlcnIgPSBleGNfc3RkZXJyWzpzZWxmLn
RydW5jYXRlX2NhcF0KICAgICAgICAgICAgZXJyX2RlbHRhID0gbGVuKHNlbGYuc3RkZXJyKSAtIGx
lbihleGNfc3RkZXJyKQogICAgICAgICAgICBpZiBlcnJfZGVsdGE6CiAgICAgICAgICAgICAgICBl
eGNfc3RkZXJyICs9ICgiLi4uICglZCBtb3JlLCBwbGVhc2Ugc2VlIGUuc3RkZXJyKSIgJSBlcnJfZ
GVsdGEpLmVuY29kZSgpCgogICAgICAgIG1zZ190bXBsID0gdW5pY29kZSgiXG5cbiAgUkFOOiB7Y2
1kfVxuXG4gIFNURE9VVDpcbntzdGRvdXR9XG5cbiAgU1RERVJSOlxue3N0ZGVycn0iKQoKICAgICA
gICBtc2cgPSBtc2dfdG1wbC5mb3JtYXQoCiAgICAgICAgICAgIGNtZD1zZWxmLmZ1bGxfY21kLAog
ICAgICAgICAgICBzdGRvdXQ9ZXhjX3N0ZG91dC5kZWNvZGUoREVGQVVMVF9FTkNPRElORywgInJlc
GxhY2UiKSwKICAgICAgICAgICAgc3RkZXJyPWV4Y19zdGRlcnIuZGVjb2RlKERFRkFVTFRfRU5DT0
RJTkcsICJyZXBsYWNlIikKICAgICAgICApCgogICAgICAgIHN1cGVyKEVycm9yUmV0dXJuQ29kZSw
gc2VsZikuX19pbml0X18obXNnKQoKCmNsYXNzIFNpZ25hbEV4Y2VwdGlvbihFcnJvclJldHVybkNv
ZGUpOiBwYXNzCmNsYXNzIFRpbWVvdXRFeGNlcHRpb24oRXhjZXB0aW9uKToKICAgICIiIiB0aGUgZ
XhjZXB0aW9uIHRocm93biB3aGVuIGEgY29tbWFuZCBpcyBraWxsZWQgYmVjYXVzZSBhIHNwZWNpZm
llZAogICAgdGltZW91dCAodmlhIF90aW1lb3V0KSB3YXMgaGl0ICIiIgogICAgZGVmIF9faW5pdF9
fKHNlbGYsIGV4aXRfY29kZSk6CiAgICAgICAgc2VsZi5leGl0X2NvZGUgPSBleGl0X2NvZGUKICAg
ICAgICBzdXBlcihFeGNlcHRpb24sIHNlbGYpLl9faW5pdF9fKCkKClNJR05BTFNfVEhBVF9TSE9VT
ERfVEhST1dfRVhDRVBUSU9OID0gc2V0KCgKICAgIHNpZ25hbC5TSUdBQlJULAogICAgc2lnbmFsLl
NJR0JVUywKICAgIHNpZ25hbC5TSUdGUEUsCiAgICBzaWduYWwuU0lHSUxMLAogICAgc2lnbmFsLlN
JR0lOVCwKICAgIHNpZ25hbC5TSUdLSUxMLAogICAgc2lnbmFsLlNJR1BJUEUsCiAgICBzaWduYWwu
U0lHUVVJVCwKICAgIHNpZ25hbC5TSUdTRUdWLAogICAgc2lnbmFsLlNJR1RFUk0sCiAgICBzaWduY
WwuU0lHU1lTLAopKQoKCiMgd2Ugc3ViY2xhc3MgQXR0cmlidXRlRXJyb3IgYmVjYXVzZToKIyBodH
RwczovL2dpdGh1Yi5jb20vaXB5dGhvbi9pcHl0aG9uL2lzc3Vlcy8yNTc3CiMgaHR0cHM6Ly9naXR
odWIuY29tL2Ftb2ZmYXQvc2gvaXNzdWVzLzk3I2lzc3VlY29tbWVudC0xMDYxMDYyOQpjbGFzcyBD
b21tYW5kTm90Rm91bmQoQXR0cmlidXRlRXJyb3IpOiBwYXNzCgoKCgpyY19leGNfcmVnZXggPSByZ
S5jb21waWxlKCIoRXJyb3JSZXR1cm5Db2RlfFNpZ25hbEV4Y2VwdGlvbilfKChcZCspfFNJR1thLX
pBLVpdKykiKQpyY19leGNfY2FjaGUgPSB7fQoKU0lHTkFMX01BUFBJTkcgPSB7fQpmb3Igayx2IGl
uIHNpZ25hbC5fX2RpY3RfXy5pdGVtcygpOgogICAgaWYgcmUubWF0Y2gociJTSUdbYS16QS1aXSsi
LCBrKToKICAgICAgICBTSUdOQUxfTUFQUElOR1t2XSA9IGsKCgpkZWYgZ2V0X2V4Y19mcm9tX25hb
WUobmFtZSk6CiAgICAiIiIgdGFrZXMgYW4gZXhjZXB0aW9uIG5hbWUsIGxpa2U6CgogICAgICAgIE
Vycm9yUmV0dXJuQ29kZV8xCiAgICAgICAgU2lnbmFsRXhjZXB0aW9uXzkKICAgICAgICBTaWduYWx
FeGNlcHRpb25fU0lHSFVQCgogICAgYW5kIHJldHVybnMgdGhlIGNvcnJlc3BvbmRpbmcgZXhjZXB0
aW9uLiAgdGhpcyBpcyBwcmltYXJpbHkgdXNlZCBmb3IKICAgIGltcG9ydGluZyBleGNlcHRpb25zI
GZyb20gc2ggaW50byB1c2VyIGNvZGUsIGZvciBpbnN0YW5jZSwgdG8gY2FwdHVyZSB0aG9zZQogIC
AgZXhjZXB0aW9ucyAiIiIKCiAgICBleGMgPSBOb25lCiAgICB0cnk6CiAgICAgICAgcmV0dXJuIHJ
jX2V4Y19jYWNoZVtuYW1lXQogICAgZXhjZXB0IEtleUVycm9yOgogICAgICAgIG0gPSByY19leGNf
cmVnZXgubWF0Y2gobmFtZSkKICAgICAgICBpZiBtOgogICAgICAgICAgICBiYXNlID0gbS5ncm91c
CgxKQogICAgICAgICAgICByY19vcl9zaWdfbmFtZSA9IG0uZ3JvdXAoMikKCiAgICAgICAgICAgIG
lmIGJhc2UgPT0gIlNpZ25hbEV4Y2VwdGlvbiI6CiAgICAgICAgICAgICAgICB0cnk6CiAgICAgICA
gICAgICAgICAgICAgcmMgPSAtaW50KHJjX29yX3NpZ19uYW1lKQogICAgICAgICAgICAgICAgZXhj
ZXB0IFZhbHVlRXJyb3I6CiAgICAgICAgICAgICAgICAgICAgcmMgPSAtZ2V0YXR0cihzaWduYWwsI
HJjX29yX3NpZ19uYW1lKQogICAgICAgICAgICBlbHNlOgogICAgICAgICAgICAgICAgcmMgPSBpbn
QocmNfb3Jfc2lnX25hbWUpCgogICAgICAgICAgICBleGMgPSBnZXRfcmNfZXhjKHJjKQogICAgcmV
0dXJuIGV4YwoKCmRlZiBnZXRfcmNfZXhjKHJjKToKICAgICIiIiB0YWtlcyBhIGV4aXQgY29kZSBv
ciBuZWdhdGl2ZSBzaWduYWwgbnVtYmVyIGFuZCBwcm9kdWNlcyBhbiBleGNlcHRpb24KICAgIHRoY
XQgY29ycmVzcG9uZHMgdG8gdGhhdCByZXR1cm4gY29kZS4gIHBvc2l0aXZlIHJldHVybiBjb2Rlcy
B5aWVsZAogICAgRXJyb3JSZXR1cm5Db2RlIGV4Y2VwdGlvbiwgbmVnYXRpdmUgcmV0dXJuIGNvZGV
zIHlpZWxkIFNpZ25hbEV4Y2VwdGlvbgoKICAgIHdlIGFsc28gY2FjaGUgdGhlIGdlbmVyYXRlZCBl
eGNlcHRpb24gc28gdGhhdCBvbmx5IG9uZSBzaWduYWwgb2YgdGhhdCB0eXBlCiAgICBleGlzdHMsI
HByZXNlcnZpbmcgaWRlbnRpdHkgIiIiCgogICAgdHJ5OgogICAgICAgIHJldHVybiByY19leGNfY2
FjaGVbcmNdCiAgICBleGNlcHQgS2V5RXJyb3I6CiAgICAgICAgcGFzcwoKICAgIGlmIHJjID4gMDo
KICAgICAgICBuYW1lID0gIkVycm9yUmV0dXJuQ29kZV8lZCIgJSByYwogICAgICAgIGJhc2UgPSBF
cnJvclJldHVybkNvZGUKICAgIGVsc2U6CiAgICAgICAgc2lnbmFtZSA9IFNJR05BTF9NQVBQSU5HW
2FicyhyYyldCiAgICAgICAgbmFtZSA9ICJTaWduYWxFeGNlcHRpb25fIiArIHNpZ25hbWUKICAgIC
AgICBiYXNlID0gU2lnbmFsRXhjZXB0aW9uCgogICAgZXhjID0gRXJyb3JSZXR1cm5Db2RlTWV0YSh
uYW1lLCAoYmFzZSwpLCB7ImV4aXRfY29kZSI6IHJjfSkKICAgIHJjX2V4Y19jYWNoZVtyY10gPSBl
eGMKICAgIHJldHVybiBleGMKCgoKIyB3ZSBtb25rZXkgcGF0Y2ggZ2xvYi4gIGknbSBub3JtYWxse
SBnZW5lcmFsbHkgYWdhaW5zdCBtb25rZXkgcGF0Y2hpbmcsIGJ1dCBpCiMgZGVjaWRlZCB0byBkby
B0aGlzIHJlYWxseSB1bi1pbnRydXNpdmUgcGF0Y2ggYmVjYXVzZSB3ZSBuZWVkIGEgd2F5IHRvIGR
ldGVjdAojIGlmIGEgbGlzdCB0aGF0IHdlIHBhc3MgaW50byBhbiBzaCBjb21tYW5kIHdhcyBnZW5l
cmF0ZWQgZnJvbSBnbG9iLiAgdGhlIHJlYXNvbgojIGJlaW5nIHRoYXQgZ2xvYiByZXR1cm5zIGFuI
GVtcHR5IGxpc3QgaWYgYSBwYXR0ZXJuIGlzIG5vdCBmb3VuZCwgYW5kIHNvCiMgY29tbWFuZHMgd2
lsbCB0cmVhdCB0aGUgZW1wdHkgbGlzdCBhcyBubyBhcmd1bWVudHMsIHdoaWNoIGNhbiBiZSBhIHB
yb2JsZW0sCiMgaWU6CiMKIyAgIGxzKGdsb2IoIioub2pmYXdlIikpCiMKIyBeIHdpbGwgc2hvdyB0
aGUgY29udGVudHMgb2YgeW91ciBob21lIGRpcmVjdG9yeSwgYmVjYXVzZSBpdCdzIGVzc2VudGlhb
Gx5CiMgcnVubmluZyBscyhbXSkgd2hpY2gsIGFzIGEgcHJvY2VzcywgaXMganVzdCAibHMiLgojCi
Mgc28gd2Ugc3ViY2xhc3MgbGlzdCBhbmQgbW9ua2V5IHBhdGNoIHRoZSBnbG9iIGZ1bmN0aW9uLiA
gbm9ib2R5IHNob3VsZCBiZSB0aGUKIyB3aXNlciwgYnV0IHdlJ2xsIGhhdmUgcmVzdWx0cyB0aGF0
IHdlIGNhbiBtYWtlIHNvbWUgZGV0ZXJtaW5hdGlvbnMgb24KX29sZF9nbG9iID0gZ2xvYl9tb2R1b
GUuZ2xvYgoKY2xhc3MgR2xvYlJlc3VsdHMobGlzdCk6CiAgICBkZWYgX19pbml0X18oc2VsZiwgcG
F0aCwgcmVzdWx0cyk6CiAgICAgICAgc2VsZi5wYXRoID0gcGF0aAogICAgICAgIGxpc3QuX19pbml
0X18oc2VsZiwgcmVzdWx0cykKCmRlZiBnbG9iKHBhdGgsICphcmdzLCAqKmt3YXJncyk6CiAgICBl
eHBhbmRlZCA9IEdsb2JSZXN1bHRzKHBhdGgsIF9vbGRfZ2xvYihwYXRoLCAqYXJncywgKiprd2FyZ
3MpKQogICAgcmV0dXJuIGV4cGFuZGVkCgpnbG9iX21vZHVsZS5nbG9iID0gZ2xvYgoKCgoKZGVmIH
doaWNoKHByb2dyYW0sIHBhdGhzPU5vbmUpOgogICAgIiIiIHRha2VzIGEgcHJvZ3JhbSBuYW1lIG9
yIGZ1bGwgcGF0aCwgcGx1cyBhbiBvcHRpb25hbCBjb2xsZWN0aW9uIG9mIHNlYXJjaAogICAgcGF0
aHMsIGFuZCByZXR1cm5zIHRoZSBmdWxsIHBhdGggb2YgdGhlIHJlcXVlc3RlZCBleGVjdXRhYmxlL
iAgaWYgcGF0aHMgaXMKICAgIHNwZWNpZmllZCwgaXQgaXMgdGhlIGVudGlyZSBsaXN0IG9mIHNlYX
JjaCBwYXRocywgYW5kIHRoZSBQQVRIIGVudiBpcyBub3QKICAgIHVzZWQgYXQgYWxsLiAgb3RoZXJ
3aXNlLCBQQVRIIGVudiBpcyB1c2VkIHRvIGxvb2sgZm9yIHRoZSBwcm9ncmFtICIiIgoKICAgIGRl
ZiBpc19leGUoZnBhdGgpOgogICAgICAgIHJldHVybiAob3MucGF0aC5leGlzdHMoZnBhdGgpIGFuZ
AogICAgICAgICAgICAgICAgb3MuYWNjZXNzKGZwYXRoLCBvcy5YX09LKSBhbmQKICAgICAgICAgIC
AgICAgIG9zLnBhdGguaXNmaWxlKG9zLnBhdGgucmVhbHBhdGgoZnBhdGgpKSkKCiAgICBmb3VuZF9
wYXRoID0gTm9uZQogICAgZnBhdGgsIGZuYW1lID0gb3MucGF0aC5zcGxpdChwcm9ncmFtKQoKICAg
ICMgaWYgdGhlcmUncyBhIHBhdGggY29tcG9uZW50LCB0aGVuIHdlJ3ZlIHNwZWNpZmllZCBhIHBhd
GggdG8gdGhlIHByb2dyYW0sCiAgICAjIGFuZCB3ZSBzaG91bGQganVzdCB0ZXN0IGlmIHRoYXQgcH
JvZ3JhbSBpcyBleGVjdXRhYmxlLiAgaWYgaXQgaXMsIHJldHVybgogICAgaWYgZnBhdGg6CiAgICA
gICAgcHJvZ3JhbSA9IG9zLnBhdGguYWJzcGF0aChvcy5wYXRoLmV4cGFuZHVzZXIocHJvZ3JhbSkp
CiAgICAgICAgaWYgaXNfZXhlKHByb2dyYW0pOgogICAgICAgICAgICBmb3VuZF9wYXRoID0gcHJvZ
3JhbQoKICAgICMgb3RoZXJ3aXNlLCB3ZSd2ZSBqdXN0IHBhc3NlZCBpbiB0aGUgcHJvZ3JhbSBuYW
1lLCBhbmQgd2UgbmVlZCB0byBzZWFyY2gKICAgICMgdGhlIHBhdGhzIHRvIGZpbmQgd2hlcmUgaXQ
gYWN0dWFsbHkgbGl2ZXMKICAgIGVsc2U6CiAgICAgICAgcGF0aHNfdG9fc2VhcmNoID0gW10KCiAg
ICAgICAgaWYgaXNpbnN0YW5jZShwYXRocywgKHR1cGxlLCBsaXN0KSk6CiAgICAgICAgICAgIHBhd
GhzX3RvX3NlYXJjaC5leHRlbmQocGF0aHMpCiAgICAgICAgZWxzZToKICAgICAgICAgICAgZW52X3
BhdGhzID0gb3MuZW52aXJvbi5nZXQoIlBBVEgiLCAiIikuc3BsaXQob3MucGF0aHNlcCkKICAgICA
gICAgICAgcGF0aHNfdG9fc2VhcmNoLmV4dGVuZChlbnZfcGF0aHMpCgogICAgICAgIGZvciBwYXRo
IGluIHBhdGhzX3RvX3NlYXJjaDoKICAgICAgICAgICAgZXhlX2ZpbGUgPSBvcy5wYXRoLmpvaW4oc
GF0aCwgcHJvZ3JhbSkKICAgICAgICAgICAgaWYgaXNfZXhlKGV4ZV9maWxlKToKICAgICAgICAgIC
AgICAgIGZvdW5kX3BhdGggPSBleGVfZmlsZQogICAgICAgICAgICAgICAgYnJlYWsKCiAgICByZXR
1cm4gZm91bmRfcGF0aAoKCmRlZiByZXNvbHZlX2NvbW1hbmRfcGF0aChwcm9ncmFtKToKICAgIHBh
dGggPSB3aGljaChwcm9ncmFtKQogICAgaWYgbm90IHBhdGg6CiAgICAgICAgIyBvdXIgYWN0dWFsI
GNvbW1hbmQgbWlnaHQgaGF2ZSBhIGRhc2ggaW4gaXQsIGJ1dCB3ZSBjYW4ndCBjYWxsCiAgICAgIC
AgIyB0aGF0IGZyb20gcHl0aG9uICh3ZSBoYXZlIHRvIHVzZSB1bmRlcnNjb3JlcyksIHNvIHdlJ2x
sIGNoZWNrCiAgICAgICAgIyBpZiBhIGRhc2ggdmVyc2lvbiBvZiBvdXIgdW5kZXJzY29yZSBjb21t
YW5kIGV4aXN0cyBhbmQgdXNlIHRoYXQKICAgICAgICAjIGlmIGl0IGRvZXMKICAgICAgICBpZiAiX
yIgaW4gcHJvZ3JhbToKICAgICAgICAgICAgcGF0aCA9IHdoaWNoKHByb2dyYW0ucmVwbGFjZSgiXy
IsICItIikpCiAgICAgICAgaWYgbm90IHBhdGg6CiAgICAgICAgICAgIHJldHVybiBOb25lCiAgICB
yZXR1cm4gcGF0aAoKCmRlZiByZXNvbHZlX2NvbW1hbmQobmFtZSwgYmFrZWRfYXJncz1Ob25lKToK
ICAgIHBhdGggPSByZXNvbHZlX2NvbW1hbmRfcGF0aChuYW1lKQogICAgY21kID0gTm9uZQogICAga
WYgcGF0aDoKICAgICAgICBjbWQgPSBDb21tYW5kKHBhdGgpCiAgICAgICAgaWYgYmFrZWRfYXJncz
oKICAgICAgICAgICAgY21kID0gY21kLmJha2UoKipiYWtlZF9hcmdzKQogICAgcmV0dXJuIGNtZAo
KCgoKY2xhc3MgTG9nZ2VyKG9iamVjdCk6CiAgICAiIiIgcHJvdmlkZXMgYSBtZW1vcnktaW5leHBl
bnNpdmUgbG9nZ2VyLiAgYSBnb3RjaGEgYWJvdXQgcHl0aG9uJ3MgYnVpbHRpbgogICAgbG9nZ2VyI
GlzIHRoYXQgbG9nZ2VyIG9iamVjdHMgYXJlIG5ldmVyIGdhcmJhZ2UgY29sbGVjdGVkLiAgaWYgeW
91IGNyZWF0ZSBhCiAgICB0aG91c2FuZCBsb2dnZXJzIHdpdGggdW5pcXVlIG5hbWVzLCB0aGV5J2x
sIHNpdCB0aGVyZSBpbiBtZW1vcnkgdW50aWwgeW91cgogICAgc2NyaXB0IGlzIGRvbmUuICB3aXRo
IHNoLCBpdCdzIGVhc3kgdG8gY3JlYXRlIGxvZ2dlcnMgd2l0aCB1bmlxdWUgbmFtZXMgaWYKICAgI
HdlIHdhbnQgb3VyIGxvZ2dlcnMgdG8gaW5jbHVkZSBvdXIgY29tbWFuZCBhcmd1bWVudHMuICBmb3
IgZXhhbXBsZSwgdGhlc2UKICAgIGFyZSBhbGwgdW5pcXVlIGxvZ2dlcnM6CiAgICAgICAgCiAgICA
gICAgICAgIGxzIC1sCiAgICAgICAgICAgIGxzIC1sIC90bXAKICAgICAgICAgICAgbHMgL3RtcAoK
ICAgIHNvIGluc3RlYWQgb2YgY3JlYXRpbmcgdW5pcXVlIGxvZ2dlcnMsIGFuZCB3aXRob3V0IHNhY
3JpZmljaW5nIGxvZ2dpbmcKICAgIG91dHB1dCwgd2UgdXNlIHRoaXMgY2xhc3MsIHdoaWNoIG1haW
50YWlucyBhcyBwYXJ0IG9mIGl0cyBzdGF0ZSwgdGhlIGxvZ2dpbmcKICAgICJjb250ZXh0Iiwgd2h
pY2ggd2lsbCBiZSB0aGUgdmVyeSB1bmlxdWUgbmFtZS4gIHRoaXMgYWxsb3dzIHVzIHRvIGdldCBh
CiAgICBsb2dnZXIgd2l0aCBhIHZlcnkgZ2VuZXJhbCBuYW1lLCBlZzogImNvbW1hbmQiLCBhbmQga
GF2ZSBhIHVuaXF1ZSBuYW1lCiAgICBhcHBlbmRlZCB0byBpdCB2aWEgdGhlIGNvbnRleHQsIGVnOi
AibHMgLWwgL3RtcCIgIiIiCiAgICBkZWYgX19pbml0X18oc2VsZiwgbmFtZSwgY29udGV4dD1Ob25
lKToKICAgICAgICBzZWxmLm5hbWUgPSBuYW1lCiAgICAgICAgc2VsZi5sb2cgPSBsb2dnaW5nLmdl
dExvZ2dlcigiJXMuJXMiICUgKFNIX0xPR0dFUl9OQU1FLCBuYW1lKSkKICAgICAgICBzZWxmLnNld
F9jb250ZXh0KGNvbnRleHQpCgogICAgZGVmIF9mb3JtYXRfbXNnKHNlbGYsIG1zZywgKmFyZ3MpOg
ogICAgICAgIGlmIHNlbGYuY29udGV4dDoKICAgICAgICAgICAgbXNnID0gIiVzOiAlcyIgJSAoc2V
sZi5jb250ZXh0LCBtc2cpCiAgICAgICAgcmV0dXJuIG1zZyAlIGFyZ3MKCiAgICBkZWYgc2V0X2Nv
bnRleHQoc2VsZiwgY29udGV4dCk6CiAgICAgICAgaWYgY29udGV4dDoKICAgICAgICAgICAgY29ud
GV4dCA9IGNvbnRleHQucmVwbGFjZSgiJSIsICIlJSIpCiAgICAgICAgc2VsZi5jb250ZXh0ID0gY2
9udGV4dCBvciAiIgoKICAgIGRlZiBnZXRfY2hpbGQoc2VsZiwgbmFtZSwgY29udGV4dCk6CiAgICA
gICAgbmV3X25hbWUgPSBzZWxmLm5hbWUgKyAiLiIgKyBuYW1lCiAgICAgICAgbmV3X2NvbnRleHQg
PSBzZWxmLmNvbnRleHQgKyAiLiIgKyBjb250ZXh0CiAgICAgICAgbCA9IExvZ2dlcihuZXdfbmFtZ
SwgbmV3X2NvbnRleHQpCiAgICAgICAgcmV0dXJuIGwKCiAgICBkZWYgaW5mbyhzZWxmLCBtc2csIC
phcmdzKToKICAgICAgICBzZWxmLmxvZy5pbmZvKHNlbGYuX2Zvcm1hdF9tc2cobXNnLCAqYXJncyk
pCgogICAgZGVmIGRlYnVnKHNlbGYsIG1zZywgKmFyZ3MpOgogICAgICAgIHNlbGYubG9nLmRlYnVn
KHNlbGYuX2Zvcm1hdF9tc2cobXNnLCAqYXJncykpCgogICAgZGVmIGVycm9yKHNlbGYsIG1zZywgK
mFyZ3MpOgogICAgICAgIHNlbGYubG9nLmVycm9yKHNlbGYuX2Zvcm1hdF9tc2cobXNnLCAqYXJncy
kpCgogICAgZGVmIGV4Y2VwdGlvbihzZWxmLCBtc2csICphcmdzKToKICAgICAgICBzZWxmLmxvZy5
leGNlcHRpb24oc2VsZi5fZm9ybWF0X21zZyhtc2csICphcmdzKSkKCgpkZWYgZGVmYXVsdF9sb2dn
ZXJfc3RyKGNtZCwgY2FsbF9hcmdzLCBwaWQ9Tm9uZSk6CiAgICBpZiBwaWQ6CiAgICAgICAgcyA9I
CI8Q29tbWFuZCAlciwgcGlkICVkPiIgJSAoY21kLCBwaWQpCiAgICBlbHNlOgogICAgICAgIHMgPS
AiPENvbW1hbmQgJXI+IiAlIGNtZAogICAgcmV0dXJuIHMKCgoKY2xhc3MgUnVubmluZ0NvbW1hbmQ
ob2JqZWN0KToKICAgICIiIiB0aGlzIHJlcHJlc2VudHMgYW4gZXhlY3V0aW5nIENvbW1hbmQgb2Jq
ZWN0LiAgaXQgaXMgcmV0dXJuZWQgYXMgdGhlCiAgICByZXN1bHQgb2YgX19jYWxsX18oKSBiZWluZ
yBleGVjdXRlZCBvbiBhIENvbW1hbmQgaW5zdGFuY2UuICB0aGlzIGNyZWF0ZXMgYQogICAgcmVmZX
JlbmNlIHRvIGEgT1Byb2MgaW5zdGFuY2UsIHdoaWNoIGlzIGEgbG93LWxldmVsIHdyYXBwZXIgYXJ
vdW5kIHRoZQogICAgcHJvY2VzcyB0aGF0IHdhcyBleGVjJ2QKCiAgICB0aGlzIGlzIHRoZSBjbGFz
cyB0aGF0IGdldHMgbWFuaXB1bGF0ZWQgdGhlIG1vc3QgYnkgdXNlciBjb2RlLCBhbmQgc28gaXQKI
CAgIGltcGxlbWVudHMgdmFyaW91cyBjb252ZW5pZW5jZSBtZXRob2RzIGFuZCBsb2dpY2FsIG1lY2
hhbmlzbXMgZm9yIHRoZQogICAgdW5kZXJseWluZyBwcm9jZXNzLiAgZm9yIGV4YW1wbGUsIGlmIGE
gdXNlciB0cmllcyB0byBhY2Nlc3MgYQogICAgYmFja2dyb3VuZGVkLXByb2Nlc3MncyBzdGRvdXQv
ZXJyLCB0aGUgUnVubmluZ0NvbW1hbmQgb2JqZWN0IGlzIHNtYXJ0IGVub3VnaAogICAgdG8ga25vd
yB0byB3YWl0KCkgb24gdGhlIHByb2Nlc3MgdG8gZmluaXNoIGZpcnN0LiAgYW5kIHdoZW4gdGhlIH
Byb2Nlc3MKICAgIGZpbmlzaGVzLCBSdW5uaW5nQ29tbWFuZCBpcyBzbWFydCBlbm91Z2ggdG8gdHJ
hbnNsYXRlIGV4aXQgY29kZXMgdG8KICAgIGV4Y2VwdGlvbnMuICIiIgoKICAgICMgdGhlc2UgYXJl
IGF0dHJpYnV0ZXMgdGhhdCB3ZSBhbGxvdyB0byBwYXNzdGhyb3VnaCB0byBPUHJvYyBmb3IKICAgI
F9PUHJvY19hdHRyX3doaXRlbGlzdCA9IHNldCgoCiAgICAgICAgInNpZ25hbCIsCiAgICAgICAgIn
Rlcm1pbmF0ZSIsCiAgICAgICAgImtpbGwiLAogICAgICAgICJraWxsX2dyb3VwIiwKICAgICAgICA
ic2lnbmFsX2dyb3VwIiwKICAgICAgICAicGlkIiwKICAgICAgICAic2lkIiwKICAgICAgICAicGdp
ZCIsCiAgICAgICAgImN0dHkiLAoKICAgICAgICAiaW5wdXRfdGhyZWFkX2V4YyIsCiAgICAgICAgI
m91dHB1dF90aHJlYWRfZXhjIiwKICAgICAgICAiYmdfdGhyZWFkX2V4YyIsCiAgICApKQoKICAgIG
RlZiBfX2luaXRfXyhzZWxmLCBjbWQsIGNhbGxfYXJncywgc3RkaW4sIHN0ZG91dCwgc3RkZXJyKTo
KICAgICAgICAiIiIKICAgICAgICAgICAgY21kIGlzIGFuIGFycmF5LCB3aGVyZSBlYWNoIGVsZW1l
bnQgaXMgZW5jb2RlZCBhcyBieXRlcyAoUFkzKSBvciBzdHIKICAgICAgICAgICAgKFBZMikKICAgI
CAgICAiIiIKCiAgICAgICAgIyBzZWxmLnJhbiBpcyB1c2VkIGZvciBhdWRpdGluZyB3aGF0IGFjdH
VhbGx5IHJhbi4gIGZvciBleGFtcGxlLCBpbgogICAgICAgICMgZXhjZXB0aW9ucywgb3IgaWYgeW9
1IGp1c3Qgd2FudCB0byBrbm93IHdoYXQgd2FzIHJhbiBhZnRlciB0aGUKICAgICAgICAjIGNvbW1h
bmQgcmFuCiAgICAgICAgIwogICAgICAgICMgaGVyZSB3ZSdyZSBtYWtpbmcgYSBjb25zaXN0ZW50I
HVuaWNvZGUgc3RyaW5nIG91dCBpZiBvdXIgY21kLgogICAgICAgICMgd2UncmUgYWxzbyBhc3N1bW
luZyAoY29ycmVjdGx5LCBpIHRoaW5rKSB0aGF0IHRoZSBjb21tYW5kIGFuZCBpdHMKICAgICAgICA
jIGFyZ3VtZW50cyBhcmUgdGhlIGVuY29kaW5nIHdlIHBhc3MgaW50byBfZW5jb2RpbmcsIHdoaWNo
IGZhbGxzIGJhY2sgdG8KICAgICAgICAjIHRoZSBzeXN0ZW0ncyBlbmNvZGluZwogICAgICAgIGVuY
yA9IGNhbGxfYXJnc1siZW5jb2RpbmciXQogICAgICAgIHNlbGYucmFuID0gIiAiLmpvaW4oW2FyZy
5kZWNvZGUoZW5jLCAiaWdub3JlIikgZm9yIGFyZyBpbiBjbWRdKQoKICAgICAgICBzZWxmLmNhbGx
fYXJncyA9IGNhbGxfYXJncwogICAgICAgIHNlbGYuY21kID0gY21kCgogICAgICAgIHNlbGYucHJv
Y2VzcyA9IE5vbmUKICAgICAgICBzZWxmLl9wcm9jZXNzX2NvbXBsZXRlZCA9IEZhbHNlCiAgICAgI
CAgc2hvdWxkX3dhaXQgPSBUcnVlCiAgICAgICAgc3Bhd25fcHJvY2VzcyA9IFRydWUKCiAgICAgIC
AgIyB0aGlzIGlzIHVzZWQgdG8gdHJhY2sgaWYgd2UndmUgYWxyZWFkeSByYWlzZWQgU3RvcEl0ZXJ
hdGlvbiwgYW5kIGlmIHdlCiAgICAgICAgIyBoYXZlLCByYWlzZSBpdCBpbW1lZGlhdGVseSBhZ2Fp
biBpZiB0aGUgdXNlciB0cmllcyB0byBjYWxsIG5leHQoKSBvbgogICAgICAgICMgdXMuICBodHRwc
zovL2dpdGh1Yi5jb20vYW1vZmZhdC9zaC9pc3N1ZXMvMjczCiAgICAgICAgc2VsZi5fc3RvcHBlZF
9pdGVyYXRpb24gPSBGYWxzZQoKICAgICAgICAjIHdpdGggY29udGV4dHMgc2hvdWxkbid0IHJ1biB
hdCBhbGwgeWV0LCB0aGV5IHByZXBlbmQKICAgICAgICAjIHRvIGV2ZXJ5IGNvbW1hbmQgaW4gdGhl
IGNvbnRleHQKICAgICAgICBpZiBjYWxsX2FyZ3NbIndpdGgiXToKICAgICAgICAgICAgc3Bhd25fc
HJvY2VzcyA9IEZhbHNlCiAgICAgICAgICAgIGdldF9wcmVwZW5kX3N0YWNrKCkuYXBwZW5kKHNlbG
YpCgoKICAgICAgICBpZiBjYWxsX2FyZ3NbInBpcGVkIl0gb3IgY2FsbF9hcmdzWyJpdGVyIl0gb3I
gY2FsbF9hcmdzWyJpdGVyX25vYmxvY2siXToKICAgICAgICAgICAgc2hvdWxkX3dhaXQgPSBGYWxz
ZQoKICAgICAgICAjIHdlJ3JlIHJ1bm5pbmcgaW4gdGhlIGJhY2tncm91bmQsIHJldHVybiBzZWxmI
GFuZCBsZXQgdXMgbGF6aWx5CiAgICAgICAgIyBldmFsdWF0ZQogICAgICAgIGlmIGNhbGxfYXJnc1
siYmciXToKICAgICAgICAgICAgc2hvdWxkX3dhaXQgPSBGYWxzZQoKICAgICAgICAjIHJlZGlyZWN
0aW9uCiAgICAgICAgaWYgY2FsbF9hcmdzWyJlcnJfdG9fb3V0Il06CiAgICAgICAgICAgIHN0ZGVy
ciA9IE9Qcm9jLlNURE9VVAoKICAgICAgICBkb25lX2NhbGxiYWNrID0gY2FsbF9hcmdzWyJkb25lI
l0KICAgICAgICBpZiBkb25lX2NhbGxiYWNrOgogICAgICAgICAgICBjYWxsX2FyZ3NbImRvbmUiXS
A9IHBhcnRpYWwoZG9uZV9jYWxsYmFjaywgc2VsZikgCgoKICAgICAgICAjIHNldCB1cCB3aGljaCB
zdHJlYW0gc2hvdWxkIHdyaXRlIHRvIHRoZSBwaXBlCiAgICAgICAgIyBUT0RPLCBtYWtlIHBpcGUg
Tm9uZSBieSBkZWZhdWx0IGFuZCBsaW1pdCB0aGUgc2l6ZSBvZiB0aGUgUXVldWUKICAgICAgICAjI
GluIG9wcm9jLk9Qcm9jCiAgICAgICAgcGlwZSA9IE9Qcm9jLlNURE9VVAogICAgICAgIGlmIGNhbG
xfYXJnc1siaXRlciJdID09ICJvdXQiIG9yIGNhbGxfYXJnc1siaXRlciJdIGlzIFRydWU6CiAgICA
gICAgICAgIHBpcGUgPSBPUHJvYy5TVERPVVQKICAgICAgICBlbGlmIGNhbGxfYXJnc1siaXRlciJd
ID09ICJlcnIiOgogICAgICAgICAgICBwaXBlID0gT1Byb2MuU1RERVJSCgogICAgICAgIGlmIGNhb
GxfYXJnc1siaXRlcl9ub2Jsb2NrIl0gPT0gIm91dCIgb3IgY2FsbF9hcmdzWyJpdGVyX25vYmxvY2
siXSBpcyBUcnVlOgogICAgICAgICAgICBwaXBlID0gT1Byb2MuU1RET1VUCiAgICAgICAgZWxpZiB
jYWxsX2FyZ3NbIml0ZXJfbm9ibG9jayJdID09ICJlcnIiOgogICAgICAgICAgICBwaXBlID0gT1By
b2MuU1RERVJSCgogICAgICAgICMgdGhlcmUncyBjdXJyZW50bHkgb25seSBvbmUgY2FzZSB3aGVyZ
SB3ZSB3b3VsZG4ndCBzcGF3biBhIGNoaWxkCiAgICAgICAgIyBwcm9jZXNzLCBhbmQgdGhhdCdzIG
lmIHdlJ3JlIHVzaW5nIGEgd2l0aC1jb250ZXh0IHdpdGggb3VyIGNvbW1hbmQKICAgICAgICBzZWx
mLl9zcGF3bmVkX2FuZF93YWl0ZWQgPSBGYWxzZQogICAgICAgIGlmIHNwYXduX3Byb2Nlc3M6CiAg
ICAgICAgICAgIGxvZ19zdHJfZmFjdG9yeSA9IGNhbGxfYXJnc1sibG9nX21zZyJdIG9yIGRlZmF1b
HRfbG9nZ2VyX3N0cgogICAgICAgICAgICBsb2dnZXJfc3RyID0gbG9nX3N0cl9mYWN0b3J5KHNlbG
YucmFuLCBjYWxsX2FyZ3MpCiAgICAgICAgICAgIHNlbGYubG9nID0gTG9nZ2VyKCJjb21tYW5kIiw
gbG9nZ2VyX3N0cikKCiAgICAgICAgICAgIHNlbGYubG9nLmluZm8oInN0YXJ0aW5nIHByb2Nlc3Mi
KQoKICAgICAgICAgICAgaWYgc2hvdWxkX3dhaXQ6CiAgICAgICAgICAgICAgICBzZWxmLl9zcGF3b
mVkX2FuZF93YWl0ZWQgPSBUcnVlCgogICAgICAgICAgICAjIHRoaXMgbG9jayBpcyBuZWVkZWQgYm
VjYXVzZSBvZiBhIHJhY2UgY29uZGl0aW9uIHdoZXJlIGEgYmFja2dyb3VuZAogICAgICAgICAgICA
jIHRocmVhZCwgY3JlYXRlZCBpbiB0aGUgT1Byb2MgY29uc3RydWN0b3IsIG1heSB0cnkgdG8gYWNj
ZXNzCiAgICAgICAgICAgICMgc2VsZi5wcm9jZXNzLCBidXQgaXQgaGFzIG5vdCBiZWVuIGFzc2lnb
mVkIHlldAogICAgICAgICAgICBwcm9jZXNzX2Fzc2lnbl9sb2NrID0gdGhyZWFkaW5nLkxvY2soKQ
ogICAgICAgICAgICB3aXRoIHByb2Nlc3NfYXNzaWduX2xvY2s6CiAgICAgICAgICAgICAgICBzZWx
mLnByb2Nlc3MgPSBPUHJvYyhzZWxmLCBzZWxmLmxvZywgY21kLCBzdGRpbiwgc3Rkb3V0LCBzdGRl
cnIsCiAgICAgICAgICAgICAgICAgICAgICAgIHNlbGYuY2FsbF9hcmdzLCBwaXBlLCBwcm9jZXNzX
2Fzc2lnbl9sb2NrKQoKICAgICAgICAgICAgbG9nZ2VyX3N0ciA9IGxvZ19zdHJfZmFjdG9yeShzZW
xmLnJhbiwgY2FsbF9hcmdzLCBzZWxmLnByb2Nlc3MucGlkKQogICAgICAgICAgICBzZWxmLmxvZy5
zZXRfY29udGV4dChsb2dnZXJfc3RyKQogICAgICAgICAgICBzZWxmLmxvZy5pbmZvKCJwcm9jZXNz
IHN0YXJ0ZWQiKQoKICAgICAgICAgICAgaWYgc2hvdWxkX3dhaXQ6CiAgICAgICAgICAgICAgICBzZ
WxmLndhaXQoKQoKCiAgICBkZWYgd2FpdChzZWxmKToKICAgICAgICAiIiIgd2FpdHMgZm9yIHRoZS
BydW5uaW5nIGNvbW1hbmQgdG8gZmluaXNoLiAgdGhpcyBpcyBjYWxsZWQgb24gYWxsCiAgICAgICA
gcnVubmluZyBjb21tYW5kcywgZXZlbnR1YWxseSwgZXhjZXB0IGZvciBvbmVzIHRoYXQgcnVuIGlu
IHRoZSBiYWNrZ3JvdW5kCiAgICAgICAgIiIiCiAgICAgICAgaWYgbm90IHNlbGYuX3Byb2Nlc3NfY
29tcGxldGVkOgogICAgICAgICAgICBzZWxmLl9wcm9jZXNzX2NvbXBsZXRlZCA9IFRydWUKCiAgIC
AgICAgICAgIGV4aXRfY29kZSA9IHNlbGYucHJvY2Vzcy53YWl0KCkKICAgICAgICAgICAgaWYgc2V
sZi5wcm9jZXNzLnRpbWVkX291dDoKICAgICAgICAgICAgICAgICMgaWYgd2UgdGltZWQgb3V0LCBv
dXIgZXhpdCBjb2RlIHJlcHJlc2VudHMgYSBzaWduYWwsIHdoaWNoIGlzCiAgICAgICAgICAgICAgI
CAjIG5lZ2F0aXZlLCBzbyBsZXQncyBtYWtlIGl0IHBvc2l0aXZlIHRvIHN0b3JlIGluIG91cgogIC
AgICAgICAgICAgICAgIyBUaW1lb3V0RXhjZXB0aW9uCiAgICAgICAgICAgICAgICByYWlzZSBUaW1
lb3V0RXhjZXB0aW9uKC1leGl0X2NvZGUpCgogICAgICAgICAgICBlbHNlOgogICAgICAgICAgICAg
ICAgc2VsZi5oYW5kbGVfY29tbWFuZF9leGl0X2NvZGUoZXhpdF9jb2RlKQogICAgICAgIAogICAgI
CAgICAgICAgICAgIyBpZiBhbiBpdGVyYWJsZSBjb21tYW5kIGlzIHVzaW5nIGFuIGluc3RhbmNlIG
9mIE9Qcm9jIGZvciBpdHMgc3RkaW4sCiAgICAgICAgICAgICAgICAjIHdhaXQgb24gaXQuICB0aGU
gcHJvY2VzcyBpcyBwcm9iYWJseSBzZXQgdG8gInBpcGVkIiwgd2hpY2ggbWVhbnMgaXQKICAgICAg
ICAgICAgICAgICMgd29uJ3QgYmUgd2FpdGVkIG9uLCB3aGljaCBtZWFucyBleGNlcHRpb25zIHdvb
id0IHByb3BhZ2F0ZSB1cCB0byB0aGUKICAgICAgICAgICAgICAgICMgbWFpbiB0aHJlYWQuICB0aG
lzIGFsbG93cyB0aGVtIHRvIGJ1YmJsZSB1cAogICAgICAgICAgICAgICAgaWYgc2VsZi5wcm9jZXN
zLl9zdGRpbl9wcm9jZXNzOgogICAgICAgICAgICAgICAgICAgIHNlbGYucHJvY2Vzcy5fc3RkaW5f
cHJvY2Vzcy5jb21tYW5kLndhaXQoKQoKICAgICAgICBzZWxmLmxvZy5pbmZvKCJwcm9jZXNzIGNvb
XBsZXRlZCIpCiAgICAgICAgcmV0dXJuIHNlbGYKCgogICAgZGVmIGhhbmRsZV9jb21tYW5kX2V4aX
RfY29kZShzZWxmLCBjb2RlKToKICAgICAgICAiIiIgaGVyZSB3ZSBkZXRlcm1pbmUgaWYgd2UgaGF
kIGFuIGV4Y2VwdGlvbiwgb3IgYW4gZXJyb3IgY29kZSB0aGF0IHdlCiAgICAgICAgd2VyZW4ndCBl
eHBlY3RpbmcgdG8gc2VlLiAgaWYgd2UgZGlkLCB3ZSBjcmVhdGUgYW5kIHJhaXNlIGFuIGV4Y2Vwd
GlvbgogICAgICAgICIiIgogICAgICAgIGNhID0gc2VsZi5jYWxsX2FyZ3MKICAgICAgICBleGNfY2
xhc3MgPSBnZXRfZXhjX2V4aXRfY29kZV93b3VsZF9yYWlzZShjb2RlLCBjYVsib2tfY29kZSJdLAo
gICAgICAgICAgICAgICAgY2FbInBpcGVkIl0pCiAgICAgICAgaWYgZXhjX2NsYXNzOgogICAgICAg
ICAgICBleGMgPSBleGNfY2xhc3Moc2VsZi5yYW4sIHNlbGYucHJvY2Vzcy5zdGRvdXQsIHNlbGYuc
HJvY2Vzcy5zdGRlcnIsCiAgICAgICAgICAgICAgICAgICAgY2FbInRydW5jYXRlX2V4YyJdKQogIC
AgICAgICAgICByYWlzZSBleGMKCgogICAgQHByb3BlcnR5CiAgICBkZWYgc3Rkb3V0KHNlbGYpOgo
gICAgICAgIHNlbGYud2FpdCgpCiAgICAgICAgcmV0dXJuIHNlbGYucHJvY2Vzcy5zdGRvdXQKCiAg
ICBAcHJvcGVydHkKICAgIGRlZiBzdGRlcnIoc2VsZik6CiAgICAgICAgc2VsZi53YWl0KCkKICAgI
CAgICByZXR1cm4gc2VsZi5wcm9jZXNzLnN0ZGVycgoKICAgIEBwcm9wZXJ0eQogICAgZGVmIGV4aX
RfY29kZShzZWxmKToKICAgICAgICBzZWxmLndhaXQoKQogICAgICAgIHJldHVybiBzZWxmLnByb2N
lc3MuZXhpdF9jb2RlCgoKICAgIGRlZiBfX2xlbl9fKHNlbGYpOgogICAgICAgIHJldHVybiBsZW4o
c3RyKHNlbGYpKQoKICAgIGRlZiBfX2VudGVyX18oc2VsZik6CiAgICAgICAgIiIiIHdlIGRvbid0I
GFjdHVhbGx5IGRvIGFueXRoaW5nIGhlcmUgYmVjYXVzZSBhbnl0aGluZyB0aGF0IHNob3VsZCBoYX
ZlCiAgICAgICAgYmVlbiBkb25lIHdvdWxkIGhhdmUgYmVlbiBkb25lIGluIHRoZSBDb21tYW5kLl9
fY2FsbF9fIGNhbGwuCiAgICAgICAgZXNzZW50aWFsbHkgYWxsIHRoYXQgaGFzIHRvIGhhcHBlbiBp
cyB0aGUgY29tYW5kIGJlIHB1c2hlZCBvbiB0aGUKICAgICAgICBwcmVwZW5kIHN0YWNrLiAiIiIKI
CAgICAgICBwYXNzCgogICAgZGVmIF9faXRlcl9fKHNlbGYpOgogICAgICAgIHJldHVybiBzZWxmCg
ogICAgZGVmIG5leHQoc2VsZik6CiAgICAgICAgIiIiIGFsbG93IHVzIHRvIGl0ZXJhdGUgb3ZlciB
0aGUgb3V0cHV0IG9mIG91ciBjb21tYW5kICIiIgoKICAgICAgICBpZiBzZWxmLl9zdG9wcGVkX2l0
ZXJhdGlvbjoKICAgICAgICAgICAgcmFpc2UgU3RvcEl0ZXJhdGlvbigpCgogICAgICAgICMgd2UgZ
G8gdGhpcyBiZWNhdXNlIGlmIGdldCBibG9ja3MsIHdlIGNhbid0IGNhdGNoIGEgS2V5Ym9hcmRJbn
RlcnJ1cHQKICAgICAgICAjIHNvIHRoZSBzbGlnaHQgdGltZW91dCBhbGxvd3MgZm9yIHRoYXQuCiA
gICAgICAgd2hpbGUgVHJ1ZToKICAgICAgICAgICAgdHJ5OgogICAgICAgICAgICAgICAgY2h1bmsg
PSBzZWxmLnByb2Nlc3MuX3BpcGVfcXVldWUuZ2V0KFRydWUsIDAuMDAxKQogICAgICAgICAgICBle
GNlcHQgRW1wdHk6CiAgICAgICAgICAgICAgICBpZiBzZWxmLmNhbGxfYXJnc1siaXRlcl9ub2Jsb2
NrIl06CiAgICAgICAgICAgICAgICAgICAgcmV0dXJuIGVycm5vLkVXT1VMREJMT0NLCiAgICAgICA
gICAgIGVsc2U6CiAgICAgICAgICAgICAgICBpZiBjaHVuayBpcyBOb25lOgogICAgICAgICAgICAg
ICAgICAgIHNlbGYud2FpdCgpCiAgICAgICAgICAgICAgICAgICAgc2VsZi5fc3RvcHBlZF9pdGVyY
XRpb24gPSBUcnVlCiAgICAgICAgICAgICAgICAgICAgcmFpc2UgU3RvcEl0ZXJhdGlvbigpCiAgIC
AgICAgICAgICAgICB0cnk6CiAgICAgICAgICAgICAgICAgICAgcmV0dXJuIGNodW5rLmRlY29kZSh
zZWxmLmNhbGxfYXJnc1siZW5jb2RpbmciXSwKICAgICAgICAgICAgICAgICAgICAgICAgc2VsZi5j
YWxsX2FyZ3NbImRlY29kZV9lcnJvcnMiXSkKICAgICAgICAgICAgICAgIGV4Y2VwdCBVbmljb2RlR
GVjb2RlRXJyb3I6CiAgICAgICAgICAgICAgICAgICAgcmV0dXJuIGNodW5rCgoKICAgICMgcHl0aG
9uIDMKICAgIF9fbmV4dF9fID0gbmV4dAoKICAgIGRlZiBfX2V4aXRfXyhzZWxmLCB0eXAsIHZhbHV
lLCB0cmFjZWJhY2spOgogICAgICAgIGlmIHNlbGYuY2FsbF9hcmdzWyJ3aXRoIl0gYW5kIGdldF9w
cmVwZW5kX3N0YWNrKCk6CiAgICAgICAgICAgIGdldF9wcmVwZW5kX3N0YWNrKCkucG9wKCkKCiAgI
CBkZWYgX19zdHJfXyhzZWxmKToKICAgICAgICAiIiIgaW4gcHl0aG9uMywgc2hvdWxkIHJldHVybi
B1bmljb2RlLiAgaW4gcHl0aG9uMiwgc2hvdWxkIHJldHVybiBhCiAgICAgICAgc3RyaW5nIG9mIGJ
5dGVzICIiIgogICAgICAgIGlmIElTX1BZMzoKICAgICAgICAgICAgcmV0dXJuIHNlbGYuX191bmlj
b2RlX18oKQogICAgICAgIGVsc2U6CiAgICAgICAgICAgIHJldHVybiB1bmljb2RlKHNlbGYpLmVuY
29kZShzZWxmLmNhbGxfYXJnc1siZW5jb2RpbmciXSkKCiAgICBkZWYgX191bmljb2RlX18oc2VsZi
k6CiAgICAgICAgIiIiIGEgbWFnaWMgbWV0aG9kIGRlZmluZWQgZm9yIHB5dGhvbjIuICBjYWxsaW5
nIHVuaWNvZGUoKSBvbiBhCiAgICAgICAgUnVubmluZ0NvbW1hbmQgb2JqZWN0IHdpbGwgY2FsbCB0
aGlzICIiIgogICAgICAgIGlmIHNlbGYucHJvY2VzcyBhbmQgc2VsZi5zdGRvdXQ6CiAgICAgICAgI
CAgIHJldHVybiBzZWxmLnN0ZG91dC5kZWNvZGUoc2VsZi5jYWxsX2FyZ3NbImVuY29kaW5nIl0sCi
AgICAgICAgICAgICAgICBzZWxmLmNhbGxfYXJnc1siZGVjb2RlX2Vycm9ycyJdKQogICAgICAgIGV
saWYgSVNfUFkzOgogICAgICAgICAgICByZXR1cm4gIiIKICAgICAgICBlbHNlOgogICAgICAgICAg
ICByZXR1cm4gdW5pY29kZSgiIikKCiAgICBkZWYgX19lcV9fKHNlbGYsIG90aGVyKToKICAgICAgI
CByZXR1cm4gdW5pY29kZShzZWxmKSA9PSB1bmljb2RlKG90aGVyKQogICAgX19oYXNoX18gPSBOb2
5lICAjIEF2b2lkIERlcHJlY2F0aW9uV2FybmluZyBpbiBQeXRob24gPCAzCgogICAgZGVmIF9fY29
udGFpbnNfXyhzZWxmLCBpdGVtKToKICAgICAgICByZXR1cm4gaXRlbSBpbiBzdHIoc2VsZikKCiAg
ICBkZWYgX19nZXRhdHRyX18oc2VsZiwgcCk6CiAgICAgICAgIyBsZXQgdGhlc2UgdGhyZWUgYXR0c
mlidXRlcyBwYXNzIHRocm91Z2ggdG8gdGhlIE9Qcm9jIG9iamVjdAogICAgICAgIGlmIHAgaW4gc2
VsZi5fT1Byb2NfYXR0cl93aGl0ZWxpc3Q6CiAgICAgICAgICAgIGlmIHNlbGYucHJvY2VzczoKICA
gICAgICAgICAgICAgIHJldHVybiBnZXRhdHRyKHNlbGYucHJvY2VzcywgcCkKICAgICAgICAgICAg
ZWxzZToKICAgICAgICAgICAgICAgIHJhaXNlIEF0dHJpYnV0ZUVycm9yCgogICAgICAgICMgc2VlI
GlmIHN0cmluZ3MgaGF2ZSB3aGF0IHdlJ3JlIGxvb2tpbmcgZm9yLiAgd2UncmUgbG9va2luZyBhdC
B0aGUKICAgICAgICAjIG1ldGhvZCBuYW1lcyBleHBsaWNpdGx5IGJlY2F1c2Ugd2UgZG9uJ3Qgd2F
udCB0byBldmFsdWF0ZSBzZWxmIHVubGVzcwogICAgICAgICMgd2UgYWJzb2x1dGVseSBoYXZlIHRv
LCB0aGUgcmVhc29uIGJlaW5nLCBpbiBweXRob24yLCBoYXNhdHRyIHN3YWxsb3dzCiAgICAgICAgI
yBleGNlcHRpb25zLCBhbmQgaWYgd2UgdHJ5IHRvIHJ1biBoYXNhdHRyIG9uIGEgY29tbWFuZCB0aG
F0IGZhaWxlZCBhbmQKICAgICAgICAjIGlzIGJlaW5nIHJ1biB3aXRoIF9pdGVyPVRydWUsIHRoZSB
jb21tYW5kIHdpbGwgYmUgZXZhbHVhdGVkLCB0aHJvdyBhbgogICAgICAgICMgZXhjZXB0aW9uLCBi
dXQgaGFzYXR0ciB3aWxsIGRpc2NhcmQgaXQKICAgICAgICBpZiBwIGluIF91bmljb2RlX21ldGhvZ
HM6CiAgICAgICAgICAgIHJldHVybiBnZXRhdHRyKHVuaWNvZGUoc2VsZiksIHApCgogICAgICAgIH
JhaXNlIEF0dHJpYnV0ZUVycm9yCgogICAgZGVmIF9fcmVwcl9fKHNlbGYpOgogICAgICAgICIiIiB
pbiBweXRob24zLCBzaG91bGQgcmV0dXJuIHVuaWNvZGUuICBpbiBweXRob24yLCBzaG91bGQgcmV0
dXJuIGEKICAgICAgICBzdHJpbmcgb2YgYnl0ZXMgIiIiCiAgICAgICAgdHJ5OgogICAgICAgICAgI
CByZXR1cm4gc3RyKHNlbGYpCiAgICAgICAgZXhjZXB0IFVuaWNvZGVEZWNvZGVFcnJvcjoKICAgIC
AgICAgICAgaWYgc2VsZi5wcm9jZXNzOgogICAgICAgICAgICAgICAgaWYgc2VsZi5zdGRvdXQ6CiA
gICAgICAgICAgICAgICAgICAgcmV0dXJuIHJlcHIoc2VsZi5zdGRvdXQpCiAgICAgICAgICAgIHJl
dHVybiByZXByKCIiKQoKICAgIGRlZiBfX2xvbmdfXyhzZWxmKToKICAgICAgICByZXR1cm4gbG9uZ
yhzdHIoc2VsZikuc3RyaXAoKSkKCiAgICBkZWYgX19mbG9hdF9fKHNlbGYpOgogICAgICAgIHJldH
VybiBmbG9hdChzdHIoc2VsZikuc3RyaXAoKSkKCiAgICBkZWYgX19pbnRfXyhzZWxmKToKICAgICA
gICByZXR1cm4gaW50KHN0cihzZWxmKS5zdHJpcCgpKQoKCgpkZWYgb3V0cHV0X3JlZGlyZWN0X2lz
X2ZpbGVuYW1lKG91dCk6CiAgICByZXR1cm4gaXNpbnN0YW5jZShvdXQsIGJhc2VzdHJpbmcpCgoKZ
GVmIGdldF9wcmVwZW5kX3N0YWNrKCk6CiAgICB0bCA9IENvbW1hbmQudGhyZWFkX2xvY2FsCiAgIC
BpZiBub3QgaGFzYXR0cih0bCwgIl9wcmVwZW5kX3N0YWNrIik6CiAgICAgICAgdGwuX3ByZXBlbmR
fc3RhY2sgPSBbXQogICAgcmV0dXJuIHRsLl9wcmVwZW5kX3N0YWNrCgoKZGVmIHNwZWNpYWxfa3dh
cmdfdmFsaWRhdG9yKGt3YXJncywgaW52YWxpZF9saXN0KToKICAgIHMxID0gc2V0KGt3YXJncy5rZ
XlzKCkpCiAgICBpbnZhbGlkX2FyZ3MgPSBbXQoKICAgIGZvciBhcmdzIGluIGludmFsaWRfbGlzdD
oKCiAgICAgICAgaWYgY2FsbGFibGUoYXJncyk6CiAgICAgICAgICAgIGZuID0gYXJncwogICAgICA
gICAgICByZXQgPSBmbihrd2FyZ3MpCiAgICAgICAgICAgIGludmFsaWRfYXJncy5leHRlbmQocmV0
KQoKICAgICAgICBlbHNlOgogICAgICAgICAgICBhcmdzLCBlcnJvcl9tc2cgPSBhcmdzCgogICAgI
CAgICAgICBpZiBzMS5pc3N1cGVyc2V0KGFyZ3MpOgogICAgICAgICAgICAgICAgaW52YWxpZF9hcm
dzLmFwcGVuZCgoYXJncywgZXJyb3JfbXNnKSkKCiAgICByZXR1cm4gaW52YWxpZF9hcmdzCgoKZGV
mIGdldF9maWxlbm8ob2IpOgogICAgIyBpbiBweTIsIHRoaXMgd2lsbCByZXR1cm4gTm9uZS4gIGlu
IHB5MywgaXQgd2lsbCByZXR1cm4gYW4gbWV0aG9kIHRoYXQKICAgICMgcmFpc2VzIHdoZW4gY2Fsb
GVkCiAgICBmaWxlbm9fbWV0aCA9IGdldGF0dHIob2IsICJmaWxlbm8iLCBOb25lKQoKICAgIGZpbG
VubyA9IE5vbmUKICAgIGlmIGZpbGVub19tZXRoOgogICAgICAgICMgcHkzIFN0cmluZ0lPIG9iamV
jdHMgd2lsbCByZXBvcnQgYSBmaWxlbm8sIGJ1dCBjYWxsaW5nIGl0IHdpbGwgcmFpc2UKICAgICAg
ICAjIGFuIGV4Y2VwdGlvbgogICAgICAgIHRyeToKICAgICAgICAgICAgZmlsZW5vID0gZmlsZW5vX
21ldGgoKQogICAgICAgIGV4Y2VwdCBVbnN1cHBvcnRlZE9wZXJhdGlvbjoKICAgICAgICAgICAgcG
FzcwogICAgZWxpZiBpc2luc3RhbmNlKG9iLCAoaW50LGxvbmcpKSBhbmQgb2IgPj0gMDoKICAgICA
gICBmaWxlbm8gPSBvYgoKICAgIHJldHVybiBmaWxlbm8KCgpkZWYgb2JfaXNfdHR5KG9iKToKICAg
ICIiIiBjaGVja3MgaWYgYW4gb2JqZWN0IChsaWtlIGEgZmlsZS1saWtlIG9iamVjdCkgaXMgYSB0d
HkuICAiIiIKICAgIGZpbGVubyA9IGdldF9maWxlbm8ob2IpCiAgICBpc190dHkgPSBGYWxzZQogIC
AgaWYgZmlsZW5vOgogICAgICAgIGlzX3R0eSA9IG9zLmlzYXR0eShmaWxlbm8pCiAgICByZXR1cm4
gaXNfdHR5CgpkZWYgb2JfaXNfcGlwZShvYik6CiAgICBmaWxlbm8gPSBnZXRfZmlsZW5vKG9iKQog
ICAgaXNfcGlwZSA9IEZhbHNlCiAgICBpZiBmaWxlbm86CiAgICAgICAgZmRfc3RhdCA9IG9zLmZzd
GF0KGZpbGVubykKICAgICAgICBpc19waXBlID0gc3RhdC5TX0lTRklGTyhmZF9zdGF0LnN0X21vZG
UpCiAgICByZXR1cm4gaXNfcGlwZQoKCmRlZiB0dHlfaW5fdmFsaWRhdG9yKGt3YXJncyk6CiAgICB
wYWlycyA9ICgoInR0eV9pbiIsICJpbiIpLCAoInR0eV9vdXQiLCAib3V0IikpCiAgICBpbnZhbGlk
ID0gW10KICAgIGZvciB0dHksIHN0ZCBpbiBwYWlyczoKICAgICAgICBpZiB0dHkgaW4ga3dhcmdzI
GFuZCBvYl9pc190dHkoa3dhcmdzLmdldChzdGQsIE5vbmUpKToKICAgICAgICAgICAgYXJncyA9IC
h0dHksIHN0ZCkKICAgICAgICAgICAgZXJyb3IgPSAiYF8lc2AgaXMgYSBUVFkgYWxyZWFkeSwgc28
gc28gaXQgZG9lc24ndCBtYWtlIHNlbnNlIFwKdG8gc2V0IHVwIGEgVFRZIHdpdGggYF8lc2AiICUg
KHN0ZCwgdHR5KQogICAgICAgICAgICBpbnZhbGlkLmFwcGVuZCgoYXJncywgZXJyb3IpKQoKICAgI
HJldHVybiBpbnZhbGlkCgpkZWYgYnVmc2l6ZV92YWxpZGF0b3Ioa3dhcmdzKToKICAgICIiIiBhIH
ZhbGlkYXRvciB0byBwcmV2ZW50IGEgdXNlciBmcm9tIHNheWluZyB0aGF0IHRoZXkgd2FudCBjdXN
0b20KICAgIGJ1ZmZlcmluZyB3aGVuIHRoZXkncmUgdXNpbmcgYW4gaW4vb3V0IG9iamVjdCB0aGF0
IHdpbGwgYmUgb3MuZHVwJ2QgdG8gdGhlCiAgICBwcm9jZXNzLCBhbmQgaGFzIGl0cyBvd24gYnVmZ
mVyaW5nLiAgYW4gZXhhbXBsZSBpcyBhIHBpcGUgb3IgYSB0dHkuICBpdAogICAgZG9lc24ndCBtYW
tlIHNlbnNlIHRvIHRlbGwgdGhlbSB0byBoYXZlIGEgY3VzdG9tIGJ1ZmZlcmluZywgc2luY2UgdGh
lIG9zCiAgICBjb250cm9scyB0aGlzLiAiIiIKICAgIGludmFsaWQgPSBbXQoKICAgIGluX29iID0g
a3dhcmdzLmdldCgiaW4iLCBOb25lKQogICAgb3V0X29iID0ga3dhcmdzLmdldCgib3V0IiwgTm9uZ
SkKCiAgICBpbl9idWYgPSBrd2FyZ3MuZ2V0KCJpbl9idWZzaXplIiwgTm9uZSkKICAgIG91dF9idW
YgPSBrd2FyZ3MuZ2V0KCJvdXRfYnVmc2l6ZSIsIE5vbmUpCgogICAgaW5fbm9fYnVmID0gb2JfaXN
fdHR5KGluX29iKSBvciBvYl9pc19waXBlKGluX29iKQogICAgb3V0X25vX2J1ZiA9IG9iX2lzX3R0
eShvdXRfb2IpIG9yIG9iX2lzX3BpcGUob3V0X29iKQoKICAgIGVyciA9ICJDYW4ndCBzcGVjaWZ5I
GFuIHt0YXJnZXR9IGJ1ZnNpemUgaWYgdGhlIHt0YXJnZXR9IHRhcmdldCBpcyBhIHBpcGUgb3IgVF
RZIgoKICAgIGlmIGluX25vX2J1ZiBhbmQgaW5fYnVmIGlzIG5vdCBOb25lOgogICAgICAgIGludmF
saWQuYXBwZW5kKCgoImluIiwgImluX2J1ZnNpemUiKSwgZXJyLmZvcm1hdCh0YXJnZXQ9ImluIikp
KQoKICAgIGlmIG91dF9ub19idWYgYW5kIG91dF9idWYgaXMgbm90IE5vbmU6CiAgICAgICAgaW52Y
WxpZC5hcHBlbmQoKCgib3V0IiwgIm91dF9idWZzaXplIiksIGVyci5mb3JtYXQodGFyZ2V0PSJvdX
QiKSkpCgogICAgcmV0dXJuIGludmFsaWQKCgpjbGFzcyBDb21tYW5kKG9iamVjdCk6CiAgICAiIiI
gcmVwcmVzZW50cyBhbiB1bi1ydW4gc3lzdGVtIHByb2dyYW0sIGxpa2UgImxzIiBvciAiY2QiLiAg
YmVjYXVzZSBpdAogICAgcmVwcmVzZW50cyB0aGUgcHJvZ3JhbSBpdHNlbGYgKGFuZCBub3QgYSByd
W5uaW5nIGluc3RhbmNlIG9mIGl0KSwgaXQgc2hvdWxkCiAgICBob2xkIHZlcnkgbGl0dGxlIHN0YX
RlLiAgaW4gZmFjdCwgdGhlIG9ubHkgc3RhdGUgaXQgZG9lcyBob2xkIGlzIGJha2VkCiAgICBhcmd
1bWVudHMuCiAgICAKICAgIHdoZW4gYSBDb21tYW5kIG9iamVjdCBpcyBjYWxsZWQsIHRoZSByZXN1
bHQgdGhhdCBpcyByZXR1cm5lZCBpcyBhCiAgICBSdW5uaW5nQ29tbWFuZCBvYmplY3QsIHdoaWNoI
HJlcHJlc2VudHMgdGhlIENvbW1hbmQgcHV0IGludG8gYW4gZXhlY3V0aW9uCiAgICBzdGF0ZS4gIi
IiCiAgICB0aHJlYWRfbG9jYWwgPSB0aHJlYWRpbmcubG9jYWwoKQoKICAgIF9jYWxsX2FyZ3MgPSB
7CiAgICAgICAgImZnIjogRmFsc2UsICMgcnVuIGNvbW1hbmQgaW4gZm9yZWdyb3VuZAoKICAgICAg
ICAjIHJ1biBhIGNvbW1hbmQgaW4gdGhlIGJhY2tncm91bmQuICBjb21tYW5kcyBydW4gaW4gdGhlI
GJhY2tncm91bmQKICAgICAgICAjIGlnbm9yZSBTSUdIVVAgYW5kIGRvIG5vdCBhdXRvbWF0aWNhbG
x5IGV4aXQgd2hlbiB0aGUgcGFyZW50IHByb2Nlc3MKICAgICAgICAjIGVuZHMKICAgICAgICAiYmc
iOiBGYWxzZSwKCiAgICAgICAgIyBhdXRvbWF0aWNhbGx5IHJlcG9ydCBleGNlcHRpb25zIGZvciBi
YWNrZ3JvdW5kIGNvbW1hbmRzCiAgICAgICAgImJnX2V4YyI6IFRydWUsCgogICAgICAgICJ3aXRoI
jogRmFsc2UsICMgcHJlcGVuZCB0aGUgY29tbWFuZCB0byBldmVyeSBjb21tYW5kIGFmdGVyIGl0Ci
AgICAgICAgImluIjogTm9uZSwKICAgICAgICAib3V0IjogTm9uZSwgIyByZWRpcmVjdCBTVERPVVQ
KICAgICAgICAiZXJyIjogTm9uZSwgIyByZWRpcmVjdCBTVERFUlIKICAgICAgICAiZXJyX3RvX291
dCI6IE5vbmUsICMgcmVkaXJlY3QgU1RERVJSIHRvIFNURE9VVAoKICAgICAgICAjIHN0ZGluIGJ1Z
mZlciBzaXplCiAgICAgICAgIyAxIGZvciBsaW5lLCAwIGZvciB1bmJ1ZmZlcmVkLCBhbnkgb3RoZX
IgbnVtYmVyIGZvciB0aGF0IGFtb3VudAogICAgICAgICJpbl9idWZzaXplIjogMCwKICAgICAgICA
jIHN0ZG91dCBidWZmZXIgc2l6ZSwgc2FtZSB2YWx1ZXMgYXMgYWJvdmUKICAgICAgICAib3V0X2J1
ZnNpemUiOiAxLAogICAgICAgICJlcnJfYnVmc2l6ZSI6IDEsCgogICAgICAgICMgdGhpcyBpcyBob
3cgYmlnIHRoZSBvdXRwdXQgYnVmZmVycyB3aWxsIGJlIGZvciBzdGRvdXQgYW5kIHN0ZGVyci4KIC
AgICAgICAjIHRoaXMgaXMgZXNzZW50aWFsbHkgaG93IG11Y2ggb3V0cHV0IHRoZXkgd2lsbCBzdG9
yZSBmcm9tIHRoZSBwcm9jZXNzLgogICAgICAgICMgd2UgdXNlIGEgZGVxdWUsIHNvIGlmIGl0IG92
ZXJmbG93cyBwYXN0IHRoaXMgYW1vdW50LCB0aGUgZmlyc3QgaXRlbXMKICAgICAgICAjIGdldCBwd
XNoZWQgb2ZmIGFzIGVhY2ggbmV3IGl0ZW0gZ2V0cyBhZGRlZC4KICAgICAgICAjCiAgICAgICAgIy
BOT1RJQ0UKICAgICAgICAjIHRoaXMgaXMgbm90IGEgKkJZVEUqIHNpemUsIHRoaXMgaXMgYSAqQ0h
VTksqIHNpemUuLi5tZWFuaW5nLCB0aGF0IGlmCiAgICAgICAgIyB5b3UncmUgYnVmZmVyaW5nIG91
dC9lcnIgYXQgMTAyNCBieXRlcywgdGhlIGludGVybmFsIGJ1ZmZlciBzaXplIHdpbGwKICAgICAgI
CAjIGJlICJpbnRlcm5hbF9idWZzaXplIiBDSFVOS1Mgb2YgMTAyNCBieXRlcwogICAgICAgICJpbn
Rlcm5hbF9idWZzaXplIjogMyAqIDEwMjQgKiogMiwKCiAgICAgICAgImVudiI6IE5vbmUsCiAgICA
gICAgInBpcGVkIjogTm9uZSwKICAgICAgICAiaXRlciI6IE5vbmUsCiAgICAgICAgIml0ZXJfbm9i
bG9jayI6IE5vbmUsCiAgICAgICAgIm9rX2NvZGUiOiAwLAogICAgICAgICJjd2QiOiBOb25lLAoKI
CAgICAgICAjIHRoZSBzZXBhcmF0b3IgZGVsaW1pdGluZyBiZXR3ZWVuIGEgbG9uZy1hcmd1bWVudC
dzIG5hbWUgYW5kIGl0cyB2YWx1ZQogICAgICAgICMgc2V0dGluZyB0aGlzIHRvIE5vbmUgd2lsbCB
jYXVzZSBuYW1lIGFuZCB2YWx1ZSB0byBiZSB0d28gc2VwYXJhdGUKICAgICAgICAjIGFyZ3VtZW50
cywgbGlrZSBmb3Igc2hvcnQgb3B0aW9ucwogICAgICAgICMgZm9yIGV4YW1wbGUsIC0tYXJnPWRlc
nAsICc9JyBpcyB0aGUgbG9uZ19zZXAKICAgICAgICAibG9uZ19zZXAiOiAiPSIsCgogICAgICAgIC
MgdGhlIHByZWZpeCB1c2VkIGZvciBsb25nIGFyZ3VtZW50cwogICAgICAgICJsb25nX3ByZWZpeCI
6ICItLSIsCgogICAgICAgICMgdGhpcyBpcyBmb3IgcHJvZ3JhbXMgdGhhdCBleHBlY3QgdGhlaXIg
aW5wdXQgdG8gYmUgZnJvbSBhIHRlcm1pbmFsLgogICAgICAgICMgc3NoIGlzIG9uZSBvZiB0aG9zZ
SBwcm9ncmFtcwogICAgICAgICJ0dHlfaW4iOiBGYWxzZSwKICAgICAgICAidHR5X291dCI6IFRydW
UsCgogICAgICAgICJlbmNvZGluZyI6IERFRkFVTFRfRU5DT0RJTkcsCiAgICAgICAgImRlY29kZV9
lcnJvcnMiOiAic3RyaWN0IiwKCiAgICAgICAgIyBob3cgbG9uZyB0aGUgcHJvY2VzcyBzaG91bGQg
cnVuIGJlZm9yZSBpdCBpcyBhdXRvLWtpbGxlZAogICAgICAgICJ0aW1lb3V0IjogTm9uZSwKICAgI
CAgICAidGltZW91dF9zaWduYWwiOiBzaWduYWwuU0lHS0lMTCwKCiAgICAgICAgIyBUT0RPIHdyaX
RlIHNvbWUgZG9jcyBvbiAibG9uZy1ydW5uaW5nIHByb2Nlc3NlcyIKICAgICAgICAjIHRoZXNlIGN
vbnRyb2wgd2hldGhlciBvciBub3Qgc3Rkb3V0L2VyciB3aWxsIGdldCBhZ2dyZWdhdGVkIHRvZ2V0
aGVyCiAgICAgICAgIyBhcyB0aGUgcHJvY2VzcyBydW5zLiAgdGhpcyBoYXMgbWVtb3J5IHVzYWdlI
GltcGxpY2F0aW9ucywgc28gc29tZXRpbWVzCiAgICAgICAgIyB3aXRoIGxvbmctcnVubmluZyBwcm
9jZXNzZXMgd2l0aCBhIGxvdCBvZiBkYXRhLCBpdCBtYWtlcyBzZW5zZSB0bwogICAgICAgICMgc2V
0IHRoZXNlIHRvIHRydWUKICAgICAgICAibm9fb3V0IjogRmFsc2UsCiAgICAgICAgIm5vX2VyciI6
IEZhbHNlLAogICAgICAgICJub19waXBlIjogRmFsc2UsCgogICAgICAgICMgaWYgYW55IHJlZGlyZ
WN0aW9uIGlzIHVzZWQgZm9yIHN0ZG91dCBvciBzdGRlcnIsIGludGVybmFsIGJ1ZmZlcmluZwogIC
AgICAgICMgb2YgdGhhdCBkYXRhIGlzIG5vdCBzdG9yZWQuICB0aGlzIGZvcmNlcyBpdCB0byBiZSB
zdG9yZWQsIGFzIGlmCiAgICAgICAgIyB0aGUgb3V0cHV0IGlzIGJlaW5nIFQnZCB0byBib3RoIHRo
ZSByZWRpcmVjdGVkIGRlc3RpbmF0aW9uIGFuZCBvdXIKICAgICAgICAjIGludGVybmFsIGJ1ZmZlc
nMKICAgICAgICAidGVlIjogTm9uZSwKCiAgICAgICAgIyB3aWxsIGJlIGNhbGxlZCB3aGVuIGEgcH
JvY2VzcyB0ZXJtaW5hdGVzIHJlZ2FyZGxlc3Mgb2YgZXhjZXB0aW9uCiAgICAgICAgImRvbmUiOiB
Ob25lLAoKICAgICAgICAjIGEgdHVwbGUgKHJvd3MsIGNvbHVtbnMpIG9mIHRoZSBkZXNpcmVkIHNp
emUgb2YgYm90aCB0aGUgc3Rkb3V0IGFuZAogICAgICAgICMgc3RkaW4gdHR5cywgaWYgdHR5cyBhc
mUgYmVpbmcgdXNlZAogICAgICAgICJ0dHlfc2l6ZSI6ICgyMCwgODApLAoKICAgICAgICAjIHdoZX
RoZXIgb3Igbm90IG91ciBleGNlcHRpb25zIHNob3VsZCBiZSB0cnVuY2F0ZWQKICAgICAgICAidHJ
1bmNhdGVfZXhjIjogVHJ1ZSwKCiAgICAgICAgIyBhIGZ1bmN0aW9uIHRvIGNhbGwgYWZ0ZXIgdGhl
IGNoaWxkIGZvcmtzIGJ1dCBiZWZvcmUgdGhlIHByb2Nlc3MgZXhlY3MKICAgICAgICAicHJlZXhlY
19mbiI6IE5vbmUsCgogICAgICAgICMgVUlEIHRvIHNldCBhZnRlciBmb3JraW5nLiBSZXF1aXJlcy
Byb290IHByaXZpbGVnZXMuIE5vdCBzdXBwb3J0ZWQgb24KICAgICAgICAjIFdpbmRvd3MuCiAgICA
gICAgInVpZCI6IE5vbmUsCgogICAgICAgICMgcHV0IHRoZSBmb3JrZWQgcHJvY2VzcyBpbiBpdHMg
b3duIHByb2Nlc3Mgc2Vzc2lvbj8KICAgICAgICAibmV3X3Nlc3Npb24iOiBUcnVlLAoKICAgICAgI
CAjIHByZS1wcm9jZXNzIGFyZ3MgcGFzc2VkIGludG8gX19jYWxsX18uICBvbmx5IHJlYWxseSB1c2
VmdWwgd2hlbiB1c2VkCiAgICAgICAgIyBpbiAuYmFrZSgpCiAgICAgICAgImFyZ19wcmVwcm9jZXN
zIjogTm9uZSwKCiAgICAgICAgIyBhIGNhbGxhYmxlIHRoYXQgcHJvZHVjZXMgYSBsb2cgbWVzc2Fn
ZSBmcm9tIGFuIGFyZ3VtZW50IHR1cGxlIG9mIHRoZQogICAgICAgICMgY29tbWFuZCBhbmQgdGhlI
GFyZ3MKICAgICAgICAibG9nX21zZyI6IE5vbmUsCiAgICB9CgogICAgIyB0aGlzIGlzIGEgY29sbG
VjdGlvbiBvZiB2YWxpZGF0b3JzIHRvIG1ha2Ugc3VyZSB0aGUgc3BlY2lhbCBrd2FyZ3MgbWFrZQo
gICAgIyBzZW5zZQogICAgX2t3YXJnX3ZhbGlkYXRvcnMgPSAoCiAgICAgICAgKCgiZmciLCAiYmci
KSwgIkNvbW1hbmQgY2FuJ3QgYmUgcnVuIGluIHRoZSBmb3JlZ3JvdW5kIGFuZCBiYWNrZ3JvdW5kI
iksCiAgICAgICAgKCgiZmciLCAiZXJyX3RvX291dCIpLCAiQ2FuJ3QgcmVkaXJlY3QgU1RERVJSIG
luIGZvcmVncm91bmQgbW9kZSIpLAogICAgICAgICgoImVyciIsICJlcnJfdG9fb3V0IiksICJTdGR
lcnIgaXMgYWxyZWFkeSBiZWluZyByZWRpcmVjdGVkIiksCiAgICAgICAgKCgicGlwZWQiLCAiaXRl
ciIpLCAiWW91IGNhbm5vdCBpdGVyYXRlIHdoZW4gdGhpcyBjb21tYW5kIGlzIGJlaW5nIHBpcGVkI
iksCiAgICAgICAgKCgicGlwZWQiLCAibm9fcGlwZSIpLCAiVXNpbmcgYSBwaXBlIGRvZXNuJ3QgbW
FrZSBzZW5zZSBpZiB5b3UndmUgXApkaXNhYmxlZCB0aGUgcGlwZSIpLAogICAgICAgICgoIm5vX29
1dCIsICJpdGVyIiksICJZb3UgY2Fubm90IGl0ZXJhdGUgb3ZlciBvdXRwdXQgaWYgdGhlcmUgaXMg
bm8gXApvdXRwdXQiKSwKICAgICAgICB0dHlfaW5fdmFsaWRhdG9yLAogICAgICAgIGJ1ZnNpemVfd
mFsaWRhdG9yLAogICAgKQoKCiAgICBkZWYgX19pbml0X18oc2VsZiwgcGF0aCwgc2VhcmNoX3BhdG
hzPU5vbmUpOgogICAgICAgIGZvdW5kID0gd2hpY2gocGF0aCwgc2VhcmNoX3BhdGhzKQoKICAgICA
gICBzZWxmLl9wYXRoID0gZW5jb2RlX3RvX3B5M2J5dGVzX29yX3B5MnN0cigiIikKCiAgICAgICAg
IyBpcyB0aGUgY29tbWFuZCBiYWtlZCAoYWthLCBwYXJ0aWFsbHkgYXBwbGllZCk/CiAgICAgICAgc
2VsZi5fcGFydGlhbCA9IEZhbHNlCiAgICAgICAgc2VsZi5fcGFydGlhbF9iYWtlZF9hcmdzID0gW1
0KICAgICAgICBzZWxmLl9wYXJ0aWFsX2NhbGxfYXJncyA9IHt9CgogICAgICAgICMgYnVnZml4IGZ
vciBmdW5jdG9vbHMud3JhcHMuICBpc3N1ZSAjMTIxCiAgICAgICAgc2VsZi5fX25hbWVfXyA9IHN0
cihzZWxmKQoKICAgICAgICBpZiBub3QgZm91bmQ6CiAgICAgICAgICAgIHJhaXNlIENvbW1hbmROb
3RGb3VuZChwYXRoKQoKICAgICAgICAjIHRoZSByZWFzb24gd2h5IHdlIHNldCB0aGUgdmFsdWVzIG
Vhcmx5IGluIHRoZSBjb25zdHJ1Y3RvciwgYW5kIGFnYWluCiAgICAgICAgIyBoZXJlLCBpcyBmb3I
gcGVvcGxlIHdobyBoYXZlIHRvb2xzIHRoYXQgaW5zcGVjdCB0aGUgc3RhY2sgb24KICAgICAgICAj
IGV4Y2VwdGlvbi4gIGlmIENvbW1hbmROb3RGb3VuZCBpcyByYWlzZWQsIHdlIG5lZWQgc2VsZi5fc
GF0aCBhbmQgdGhlCiAgICAgICAgIyBvdGhlciBhdHRyaWJ1dGVzIHRvIGJlIHNldCBjb3JyZWN0bH
ksIHNvIHJlcHIoKSB3b3JrcyB3aGVuIHRoZXkncmUKICAgICAgICAjIGluc3BlY3RpbmcgdGhlIHN
0YWNrLiAgaXNzdWUgIzMwNAogICAgICAgIHNlbGYuX3BhdGggPSBlbmNvZGVfdG9fcHkzYnl0ZXNf
b3JfcHkyc3RyKGZvdW5kKSAKICAgICAgICBzZWxmLl9fbmFtZV9fID0gc3RyKHNlbGYpCgoKICAgI
GRlZiBfX2dldGF0dHJpYnV0ZV9fKHNlbGYsIG5hbWUpOgogICAgICAgICMgY29udmVuaWVuY2UKIC
AgICAgICBnZXRhdHRyID0gcGFydGlhbChvYmplY3QuX19nZXRhdHRyaWJ1dGVfXywgc2VsZikKICA
gICAgICB2YWwgPSBOb25lCgogICAgICAgIGlmIG5hbWUuc3RhcnRzd2l0aCgiXyIpOgogICAgICAg
ICAgICB2YWwgPSBnZXRhdHRyKG5hbWUpCgogICAgICAgIGVsaWYgbmFtZSA9PSAiYmFrZSI6CiAgI
CAgICAgICAgIHZhbCA9IGdldGF0dHIoImJha2UiKQoKICAgICAgICAjIGhlcmUgd2UgaGF2ZSBhIH
dheSBvZiBnZXR0aW5nIHBhc3Qgc2hhZG93ZWQgc3ViY29tbWFuZHMuICBmb3IgZXhhbXBsZSwKICA
gICAgICAjIGlmICJnaXQgYmFrZSIgd2FzIGEgdGhpbmcsIHdlIHdvdWxkbid0IGJlIGFibGUgdG8g
ZG8gYGdpdC5iYWtlKClgCiAgICAgICAgIyBiZWNhdXNlIGAuYmFrZSgpYCBpcyBhbHJlYWR5IGEgb
WV0aG9kLiAgc28gd2UgYWxsb3cgYGdpdC5iYWtlXygpYAogICAgICAgIGVsaWYgbmFtZS5lbmRzd2
l0aCgiXyIpOgogICAgICAgICAgICBuYW1lID0gbmFtZVs6LTFdCgogICAgICAgIGlmIHZhbCBpcyB
Ob25lOgogICAgICAgICAgICB2YWwgPSBnZXRhdHRyKCJiYWtlIikobmFtZSkKCiAgICAgICAgcmV0
dXJuIHZhbAoKCiAgICBAc3RhdGljbWV0aG9kCiAgICBkZWYgX2V4dHJhY3RfY2FsbF9hcmdzKGt3Y
XJncyk6CiAgICAgICAgIiIiIHRha2VzIGt3YXJncyB0aGF0IHdlcmUgcGFzc2VkIHRvIGEgY29tbW
FuZCdzIF9fY2FsbF9fIGFuZCBleHRyYWN0cwogICAgICAgIG91dCB0aGUgc3BlY2lhbCBrZXl3b3J
kIGFyZ3VtZW50cywgd2UgcmV0dXJuIGEgdHVwbGUgb2Ygc3BlY2lhbCBrZXl3b3JkCiAgICAgICAg
YXJncywgYW5kIGt3YXJncyB0aGF0IHdpbGwgZ28gdG8gdGhlIGV4ZWNkIGNvbW1hbmQgIiIiCgogI
CAgICAgIGt3YXJncyA9IGt3YXJncy5jb3B5KCkKICAgICAgICBjYWxsX2FyZ3MgPSB7fQogICAgIC
AgIGZvciBwYXJnLCBkZWZhdWx0IGluIENvbW1hbmQuX2NhbGxfYXJncy5pdGVtcygpOgogICAgICA
gICAgICBrZXkgPSAiXyIgKyBwYXJnCgogICAgICAgICAgICBpZiBrZXkgaW4ga3dhcmdzOgogICAg
ICAgICAgICAgICAgY2FsbF9hcmdzW3BhcmddID0ga3dhcmdzW2tleV0KICAgICAgICAgICAgICAgI
GRlbCBrd2FyZ3Nba2V5XQoKICAgICAgICBpbnZhbGlkX2t3YXJncyA9IHNwZWNpYWxfa3dhcmdfdm
FsaWRhdG9yKGNhbGxfYXJncywKICAgICAgICAgICAgICAgIENvbW1hbmQuX2t3YXJnX3ZhbGlkYXR
vcnMpCgogICAgICAgIGlmIGludmFsaWRfa3dhcmdzOgogICAgICAgICAgICBleGNfbXNnID0gW10K
ICAgICAgICAgICAgZm9yIGFyZ3MsIGVycm9yX21zZyBpbiBpbnZhbGlkX2t3YXJnczoKICAgICAgI
CAgICAgICAgIGV4Y19tc2cuYXBwZW5kKCIgICVyOiAlcyIgJSAoYXJncywgZXJyb3JfbXNnKSkKIC
AgICAgICAgICAgZXhjX21zZyA9ICJcbiIuam9pbihleGNfbXNnKQogICAgICAgICAgICByYWlzZSB
UeXBlRXJyb3IoIkludmFsaWQgc3BlY2lhbCBhcmd1bWVudHM6XG5cbiVzXG4iICUgZXhjX21zZykK
CiAgICAgICAgcmV0dXJuIGNhbGxfYXJncywga3dhcmdzCgoKICAgICMgVE9ETyBuZWVkcyBkb2N1b
WVudGF0aW9uCiAgICBkZWYgYmFrZShzZWxmLCAqYXJncywgKiprd2FyZ3MpOgogICAgICAgIGZuID
0gdHlwZShzZWxmKShzZWxmLl9wYXRoKQogICAgICAgIGZuLl9wYXJ0aWFsID0gVHJ1ZQoKICAgICA
gICBjYWxsX2FyZ3MsIGt3YXJncyA9IHNlbGYuX2V4dHJhY3RfY2FsbF9hcmdzKGt3YXJncykKCiAg
ICAgICAgcHJ1bmVkX2NhbGxfYXJncyA9IGNhbGxfYXJncwogICAgICAgIGZvciBrLCB2IGluIENvb
W1hbmQuX2NhbGxfYXJncy5pdGVtcygpOgogICAgICAgICAgICB0cnk6CiAgICAgICAgICAgICAgIC
BpZiBwcnVuZWRfY2FsbF9hcmdzW2tdID09IHY6CiAgICAgICAgICAgICAgICAgICAgZGVsIHBydW5
lZF9jYWxsX2FyZ3Nba10KICAgICAgICAgICAgZXhjZXB0IEtleUVycm9yOgogICAgICAgICAgICAg
ICAgY29udGludWUKCiAgICAgICAgZm4uX3BhcnRpYWxfY2FsbF9hcmdzLnVwZGF0ZShzZWxmLl9wY
XJ0aWFsX2NhbGxfYXJncykKICAgICAgICBmbi5fcGFydGlhbF9jYWxsX2FyZ3MudXBkYXRlKHBydW
5lZF9jYWxsX2FyZ3MpCiAgICAgICAgZm4uX3BhcnRpYWxfYmFrZWRfYXJncy5leHRlbmQoc2VsZi5
fcGFydGlhbF9iYWtlZF9hcmdzKQogICAgICAgIHNlcCA9IHBydW5lZF9jYWxsX2FyZ3MuZ2V0KCJs
b25nX3NlcCIsIHNlbGYuX2NhbGxfYXJnc1sibG9uZ19zZXAiXSkKICAgICAgICBwcmVmaXggPSBwc
nVuZWRfY2FsbF9hcmdzLmdldCgibG9uZ19wcmVmaXgiLAogICAgICAgICAgICAgICAgc2VsZi5fY2
FsbF9hcmdzWyJsb25nX3ByZWZpeCJdKQogICAgICAgIGZuLl9wYXJ0aWFsX2Jha2VkX2FyZ3MuZXh
0ZW5kKGNvbXBpbGVfYXJncyhhcmdzLCBrd2FyZ3MsIHNlcCwgcHJlZml4KSkKICAgICAgICByZXR1
cm4gZm4KCiAgICBkZWYgX19zdHJfXyhzZWxmKToKICAgICAgICAiIiIgaW4gcHl0aG9uMywgc2hvd
WxkIHJldHVybiB1bmljb2RlLiAgaW4gcHl0aG9uMiwgc2hvdWxkIHJldHVybiBhCiAgICAgICAgc3
RyaW5nIG9mIGJ5dGVzICIiIgogICAgICAgIGlmIElTX1BZMzoKICAgICAgICAgICAgcmV0dXJuIHN
lbGYuX191bmljb2RlX18oKQogICAgICAgIGVsc2U6CiAgICAgICAgICAgIHJldHVybiBzZWxmLl9f
dW5pY29kZV9fKCkuZW5jb2RlKERFRkFVTFRfRU5DT0RJTkcpCgoKICAgIGRlZiBfX2VxX18oc2VsZ
iwgb3RoZXIpOgogICAgICAgIHJldHVybiBzdHIoc2VsZikgPT0gc3RyKG90aGVyKQoKICAgIF9faG
FzaF9fID0gTm9uZSAgIyBBdm9pZCBEZXByZWNhdGlvbldhcm5pbmcgaW4gUHl0aG9uIDwgMwoKCiA
gICBkZWYgX19yZXByX18oc2VsZik6CiAgICAgICAgIiIiIGluIHB5dGhvbjMsIHNob3VsZCByZXR1
cm4gdW5pY29kZS4gIGluIHB5dGhvbjIsIHNob3VsZCByZXR1cm4gYQogICAgICAgIHN0cmluZyBvZ
iBieXRlcyAiIiIKICAgICAgICByZXR1cm4gIjxDb21tYW5kICVyPiIgJSBzdHIoc2VsZikKCgogIC
AgZGVmIF9fdW5pY29kZV9fKHNlbGYpOgogICAgICAgICIiIiBhIG1hZ2ljIG1ldGhvZCBkZWZpbmV
kIGZvciBweXRob24yLiAgY2FsbGluZyB1bmljb2RlKCkgb24gYQogICAgICAgIHNlbGYgd2lsbCBj
YWxsIHRoaXMgIiIiCiAgICAgICAgYmFrZWRfYXJncyA9ICIgIi5qb2luKGl0ZW0uZGVjb2RlKERFR
kFVTFRfRU5DT0RJTkcpIGZvciBpdGVtIGluIHNlbGYuX3BhcnRpYWxfYmFrZWRfYXJncykKICAgIC
AgICBpZiBiYWtlZF9hcmdzOgogICAgICAgICAgICBiYWtlZF9hcmdzID0gIiAiICsgYmFrZWRfYXJ
ncwogICAgICAgIHJldHVybiBzZWxmLl9wYXRoLmRlY29kZShERUZBVUxUX0VOQ09ESU5HKSArIGJh
a2VkX2FyZ3MKCiAgICBkZWYgX19lbnRlcl9fKHNlbGYpOgogICAgICAgIHNlbGYoX3dpdGg9VHJ1Z
SkKCiAgICBkZWYgX19leGl0X18oc2VsZiwgdHlwLCB2YWx1ZSwgdHJhY2ViYWNrKToKICAgICAgIC
BnZXRfcHJlcGVuZF9zdGFjaygpLnBvcCgpCgoKICAgIGRlZiBfX2NhbGxfXyhzZWxmLCAqYXJncyw
gKiprd2FyZ3MpOgoKICAgICAgICBrd2FyZ3MgPSBrd2FyZ3MuY29weSgpCiAgICAgICAgYXJncyA9
IGxpc3QoYXJncykKCiAgICAgICAgIyB0aGlzIHdpbGwgaG9sZCBvdXIgZmluYWwgY29tbWFuZCwga
W5jbHVkaW5nIGFyZ3VtZW50cywgdGhhdCB3aWxsIGJlCiAgICAgICAgIyBleGVjZAogICAgICAgIG
NtZCA9IFtdCgogICAgICAgICMgdGhpcyB3aWxsIGhvbGQgYSBjb21wbGV0ZSBtYXBwaW5nIG9mIGF
sbCBvdXIgc3BlY2lhbCBrZXl3b3JkIGFyZ3VtZW50cwogICAgICAgICMgYW5kIHRoZWlyIHZhbHVl
cwogICAgICAgIGNhbGxfYXJncyA9IENvbW1hbmQuX2NhbGxfYXJncy5jb3B5KCkKCiAgICAgICAgI
yBhZ2dyZWdhdGUgYW55ICd3aXRoJyBjb250ZXh0cwogICAgICAgIGZvciBwcmVwZW5kIGluIGdldF
9wcmVwZW5kX3N0YWNrKCk6CiAgICAgICAgICAgIHBjYWxsX2FyZ3MgPSBwcmVwZW5kLmNhbGxfYXJ
ncy5jb3B5KCkKICAgICAgICAgICAgIyBkb24ndCBwYXNzIHRoZSAnd2l0aCcgY2FsbCBhcmcKICAg
ICAgICAgICAgcGNhbGxfYXJncy5wb3AoIndpdGgiLCBOb25lKQoKICAgICAgICAgICAgY2FsbF9hc
mdzLnVwZGF0ZShwY2FsbF9hcmdzKQogICAgICAgICAgICBjbWQuZXh0ZW5kKHByZXBlbmQuY21kKQ
oKICAgICAgICBjbWQuYXBwZW5kKHNlbGYuX3BhdGgpCgogICAgICAgICMgZG8gd2UgaGF2ZSBhbiB
hcmd1bWVudCBwcmUtcHJvY2Vzc29yPyAgaWYgc28sIHJ1biBpdC4gIHdlIG5lZWQgdG8gZG8KICAg
ICAgICAjIHRoaXMgZWFybHksIHNvIHRoYXQgYXJncywga3dhcmdzIGFyZSBhY2N1cmF0ZQogICAgI
CAgIHByZXByb2Nlc3NvciA9IHNlbGYuX3BhcnRpYWxfY2FsbF9hcmdzLmdldCgiYXJnX3ByZXByb2
Nlc3MiLCBOb25lKQogICAgICAgIGlmIHByZXByb2Nlc3NvcjoKICAgICAgICAgICAgYXJncywga3d
hcmdzID0gcHJlcHJvY2Vzc29yKGFyZ3MsIGt3YXJncykKCiAgICAgICAgIyBoZXJlIHdlIGV4dHJh
Y3QgdGhlIHNwZWNpYWwga3dhcmdzIGFuZCBvdmVycmlkZSBhbnkKICAgICAgICAjIHNwZWNpYWwga
3dhcmdzIGZyb20gdGhlIHBvc3NpYmx5IGJha2VkIGNvbW1hbmQKICAgICAgICBleHRyYWN0ZWRfY2
FsbF9hcmdzLCBrd2FyZ3MgPSBzZWxmLl9leHRyYWN0X2NhbGxfYXJncyhrd2FyZ3MpCgogICAgICA
gIGNhbGxfYXJncy51cGRhdGUoc2VsZi5fcGFydGlhbF9jYWxsX2FyZ3MpCiAgICAgICAgY2FsbF9h
cmdzLnVwZGF0ZShleHRyYWN0ZWRfY2FsbF9hcmdzKQoKCiAgICAgICAgIyBoYW5kbGUgYSBOb25lL
iAgdGhpcyBpcyBhZGRlZCBiYWNrIG9ubHkgdG8gbm90IGJyZWFrIHRoZSBhcGkgaW4gdGhlCiAgIC
AgICAgIyAxLiogdmVyc2lvbi4gIFRPRE8gcmVtb3ZlIHRoaXMgaW4gMi4wLCBhcyAib2tfY29kZSI
sIGlmIHNwZWNpZmllZCwKICAgICAgICAjIHNob3VsZCBhbHdheXMgYmUgYSBkZWZpbml0aXZlIHZh
bHVlIG9yIGxpc3Qgb2YgdmFsdWVzLCBhbmQgTm9uZSBpcwogICAgICAgICMgYW1iaWd1b3VzCiAgI
CAgICAgaWYgY2FsbF9hcmdzWyJva19jb2RlIl0gaXMgTm9uZToKICAgICAgICAgICAgY2FsbF9hcm
dzWyJva19jb2RlIl0gPSAwCgogICAgICAgIGlmIG5vdCBnZXRhdHRyKGNhbGxfYXJnc1sib2tfY29
kZSJdLCAiX19pdGVyX18iLCBOb25lKToKICAgICAgICAgICAgY2FsbF9hcmdzWyJva19jb2RlIl0g
PSBbY2FsbF9hcmdzWyJva19jb2RlIl1dCgoKICAgICAgICAjIGNoZWNrIGlmIHdlJ3JlIHBpcGluZ
yB2aWEgY29tcG9zaXRpb24KICAgICAgICBzdGRpbiA9IGNhbGxfYXJnc1siaW4iXQogICAgICAgIG
lmIGFyZ3M6CiAgICAgICAgICAgIGZpcnN0X2FyZyA9IGFyZ3MucG9wKDApCiAgICAgICAgICAgIGl
mIGlzaW5zdGFuY2UoZmlyc3RfYXJnLCBSdW5uaW5nQ29tbWFuZCk6CiAgICAgICAgICAgICAgICBp
ZiBmaXJzdF9hcmcuY2FsbF9hcmdzWyJwaXBlZCJdOgogICAgICAgICAgICAgICAgICAgIHN0ZGluI
D0gZmlyc3RfYXJnLnByb2Nlc3MKICAgICAgICAgICAgICAgIGVsc2U6CiAgICAgICAgICAgICAgIC
AgICAgc3RkaW4gPSBmaXJzdF9hcmcucHJvY2Vzcy5fcGlwZV9xdWV1ZQoKICAgICAgICAgICAgZWx
zZToKICAgICAgICAgICAgICAgIGFyZ3MuaW5zZXJ0KDAsIGZpcnN0X2FyZykKCiAgICAgICAgcHJv
Y2Vzc2VkX2FyZ3MgPSBjb21waWxlX2FyZ3MoYXJncywga3dhcmdzLCBjYWxsX2FyZ3NbImxvbmdfc
2VwIl0sCiAgICAgICAgICAgICAgICBjYWxsX2FyZ3NbImxvbmdfcHJlZml4Il0pCgogICAgICAgIC
MgbWFrZXMgc3VyZSBvdXIgYXJndW1lbnRzIGFyZSBicm9rZW4gdXAgY29ycmVjdGx5CiAgICAgICA
gc3BsaXRfYXJncyA9IHNlbGYuX3BhcnRpYWxfYmFrZWRfYXJncyArIHByb2Nlc3NlZF9hcmdzCgog
ICAgICAgIGZpbmFsX2FyZ3MgPSBzcGxpdF9hcmdzCgogICAgICAgIGNtZC5leHRlbmQoZmluYWxfY
XJncykKCiAgICAgICAgIyBpZiB3ZSdyZSBydW5uaW5nIGluIGZvcmVncm91bmQgbW9kZSwgd2Ugbm
VlZCB0byBjb21wbGV0ZWx5IGJ5cGFzcwogICAgICAgICMgbGF1bmNoaW5nIGEgUnVubmluZ0NvbW1
hbmQgYW5kIE9Qcm9jIGFuZCBqdXN0IGRvIGEgc3Bhd24KICAgICAgICBpZiBjYWxsX2FyZ3NbImZn
Il06CiAgICAgICAgICAgIGlmIGNhbGxfYXJnc1siZW52Il0gaXMgTm9uZToKICAgICAgICAgICAgI
CAgIGxhdW5jaCA9IGxhbWJkYTogb3Muc3Bhd252KG9zLlBfV0FJVCwgY21kWzBdLCBjbWQpCiAgIC
AgICAgICAgIGVsc2U6CiAgICAgICAgICAgICAgICBsYXVuY2ggPSBsYW1iZGE6IG9zLnNwYXdudmU
ob3MuUF9XQUlULCBjbWRbMF0sIGNtZCwgY2FsbF9hcmdzWyJlbnYiXSkKCiAgICAgICAgICAgIGV4
aXRfY29kZSA9IGxhdW5jaCgpCiAgICAgICAgICAgIGV4Y19jbGFzcyA9IGdldF9leGNfZXhpdF9jb
2RlX3dvdWxkX3JhaXNlKGV4aXRfY29kZSwKICAgICAgICAgICAgICAgICAgICBjYWxsX2FyZ3NbIm
9rX2NvZGUiXSwgY2FsbF9hcmdzWyJwaXBlZCJdKQogICAgICAgICAgICBpZiBleGNfY2xhc3M6CiA
gICAgICAgICAgICAgICBpZiBJU19QWTM6CiAgICAgICAgICAgICAgICAgICAgcmFuID0gIiAiLmpv
aW4oW2FyZy5kZWNvZGUoREVGQVVMVF9FTkNPRElORywgImlnbm9yZSIpIGZvciBhcmcgaW4gY21kX
SkKICAgICAgICAgICAgICAgIGVsc2U6CiAgICAgICAgICAgICAgICAgICAgcmFuID0gIiAiLmpvaW
4oY21kKQogICAgICAgICAgICAgICAgZXhjID0gZXhjX2NsYXNzKHJhbiwgYiIiLCBiIiIsIGNhbGx
fYXJnc1sidHJ1bmNhdGVfZXhjIl0pCiAgICAgICAgICAgICAgICByYWlzZSBleGMKICAgICAgICAg
ICAgcmV0dXJuIE5vbmUKCgogICAgICAgICMgc3Rkb3V0IHJlZGlyZWN0aW9uCiAgICAgICAgc3Rkb
3V0ID0gY2FsbF9hcmdzWyJvdXQiXQogICAgICAgIGlmIG91dHB1dF9yZWRpcmVjdF9pc19maWxlbm
FtZShzdGRvdXQpOgogICAgICAgICAgICBzdGRvdXQgPSBvcGVuKHN0cihzdGRvdXQpLCAid2IiKQo
KICAgICAgICAjIHN0ZGVyciByZWRpcmVjdGlvbgogICAgICAgIHN0ZGVyciA9IGNhbGxfYXJnc1si
ZXJyIl0KICAgICAgICBpZiBvdXRwdXRfcmVkaXJlY3RfaXNfZmlsZW5hbWUoc3RkZXJyKToKICAgI
CAgICAgICAgc3RkZXJyID0gb3BlbihzdHIoc3RkZXJyKSwgIndiIikKICAgIAogICAgICAgIHJldH
VybiBSdW5uaW5nQ29tbWFuZChjbWQsIGNhbGxfYXJncywgc3RkaW4sIHN0ZG91dCwgc3RkZXJyKQo
KCmRlZiBjb21waWxlX2FyZ3MoYXJncywga3dhcmdzLCBzZXAsIHByZWZpeCk6CiAgICAiIiIgdGFr
ZXMgYXJncyBhbmQga3dhcmdzLCBhcyB0aGV5IHdlcmUgcGFzc2VkIGludG8gdGhlIGNvbW1hbmQga
W5zdGFuY2UKICAgIGJlaW5nIGV4ZWN1dGVkIHdpdGggX19jYWxsX18sIGFuZCBjb21wb3NlIHRoZW
0gaW50byBhIGZsYXQgbGlzdCB0aGF0CiAgICB3aWxsIGV2ZW50dWFsbHkgYmUgZmVkIGludG8gZXh
lYy4gIGV4YW1wbGU6CgogICAgd2l0aCB0aGlzIGNhbGw6CgogICAgICAgIHNoLmxzKCItbCIsICIv
dG1wIiwgY29sb3I9Im5ldmVyIikKCiAgICB0aGlzIGZ1bmN0aW9uIHJlY2VpdmVzCgogICAgICAgI
GFyZ3MgPSBbJy1sJywgJy90bXAnXQogICAgICAgIGt3YXJncyA9IHsnY29sb3InOiAnbmV2ZXInfQ
oKICAgIGFuZCBwcm9kdWNlcwoKICAgICAgICBbJy1sJywgJy90bXAnLCAnLS1jb2xvcj1uZXZlcid
dCiAgICAgICAgCiAgICAiIiIKICAgIHByb2Nlc3NlZF9hcmdzID0gW10KICAgIGVuY29kZSA9IGVu
Y29kZV90b19weTNieXRlc19vcl9weTJzdHIKCiAgICAjIGFnZ3JlZ2F0ZSBwb3NpdGlvbmFsIGFyZ
3MKICAgIGZvciBhcmcgaW4gYXJnczoKICAgICAgICBpZiBpc2luc3RhbmNlKGFyZywgKGxpc3QsIH
R1cGxlKSk6CiAgICAgICAgICAgIGlmIGlzaW5zdGFuY2UoYXJnLCBHbG9iUmVzdWx0cykgYW5kIG5
vdCBhcmc6CiAgICAgICAgICAgICAgICBhcmcgPSBbYXJnLnBhdGhdCgogICAgICAgICAgICBmb3Ig
c3ViX2FyZyBpbiBhcmc6CiAgICAgICAgICAgICAgICBwcm9jZXNzZWRfYXJncy5hcHBlbmQoZW5jb
2RlKHN1Yl9hcmcpKQogICAgICAgIGVsaWYgaXNpbnN0YW5jZShhcmcsIGRpY3QpOgogICAgICAgIC
AgICBwcm9jZXNzZWRfYXJncyArPSBhZ2dyZWdhdGVfa2V5d29yZHMoYXJnLCBzZXAsIHByZWZpeCw
gcmF3PVRydWUpCiAgICAgICAgZWxzZToKICAgICAgICAgICAgcHJvY2Vzc2VkX2FyZ3MuYXBwZW5k
KGVuY29kZShhcmcpKQoKICAgICMgYWdncmVnYXRlIHRoZSBrZXl3b3JkIGFyZ3VtZW50cwogICAgc
HJvY2Vzc2VkX2FyZ3MgKz0gYWdncmVnYXRlX2tleXdvcmRzKGt3YXJncywgc2VwLCBwcmVmaXgpCg
ogICAgcmV0dXJuIHByb2Nlc3NlZF9hcmdzCgoKZGVmIGFnZ3JlZ2F0ZV9rZXl3b3JkcyhrZXl3b3J
kcywgc2VwLCBwcmVmaXgsIHJhdz1GYWxzZSk6CiAgICAiIiIgdGFrZSBvdXIga2V5d29yZCBhcmd1
bWVudHMsIGFuZCBhIHNlcGFyYXRvciwgYW5kIGNvbXBvc2UgdGhlIGxpc3Qgb2YKICAgIGZsYXQgb
G9uZyAoYW5kIHNob3J0KSBhcmd1bWVudHMuICBleGFtcGxlCgogICAgICAgIHsnY29sb3InOiAnbm
V2ZXInLCAndCc6IFRydWUsICdzb21ldGhpbmcnOiBUcnVlfSB3aXRoIHNlcCAnPScKCiAgICBiZWN
vbWVzCgogICAgICAgIFsnLS1jb2xvcj1uZXZlcicsICctdCcsICctLXNvbWV0aGluZyddCgogICAg
dGhlIGByYXdgIGFyZ3VtZW50IGluZGljYXRlcyB3aGV0aGVyIG9yIG5vdCB3ZSBzaG91bGQgbGVhd
mUgdGhlIGFyZ3VtZW50CiAgICBuYW1lIGFsb25lLCBvciB3aGV0aGVyIHdlIHNob3VsZCByZXBsYW
NlICJfIiB3aXRoICItIi4gIGlmIHdlIHBhc3MgaW4gYQogICAgZGljdGlvbmFyeSwgbGlrZSB0aGl
zOgoKICAgICAgICBzaC5jb21tYW5kKHsic29tZV9vcHRpb24iOiAxMn0pCgogICAgdGhlbiBgcmF3
YCBnZXRzIHNldCB0byBUcnVlLCBiZWNhdXNlIHdlIHdhbnQgdG8gbGVhdmUgdGhlIGtleSBhcy1pc
ywgdG8KICAgIHByb2R1Y2U6CgogICAgICAgIFsnLS1zb21lX29wdGlvbj0xMiddCgogICAgYnV0IG
lmIHdlIGp1c3QgdXNlIGEgY29tbWFuZCdzIGt3YXJncywgYHJhd2AgaXMgRmFsc2UsIHdoaWNoIG1
lYW5zIHRoaXM6CgogICAgICAgIHNoLmNvbW1hbmQoc29tZV9vcHRpb249MTIpCgogICAgYmVjb21l
czoKCiAgICAgICAgWyctLXNvbWUtb3B0aW9uPTEyJ10KCiAgICBlZXNzZW50aWFsbHksIHVzaW5nI
Gt3YXJncyBpcyBhIGNvbnZlbmllbmNlLCBidXQgaXQgbGFja3MgdGhlIGFiaWxpdHkgdG8KICAgIH
B1dCBhICctJyBpbiB0aGUgbmFtZSwgc28gd2UgZG8gdGhlIHJlcGxhY2VtZW50IG9mICdfJyB0byA
nLScgZm9yIHlvdS4KICAgIGJ1dCB3aGVuIHlvdSByZWFsbHkgZG9uJ3Qgd2FudCB0aGF0IHRvIGhh
cHBlbiwgeW91IHNob3VsZCB1c2UgYQogICAgZGljdGlvbmFyeSBpbnN0ZWFkIHdpdGggdGhlIGV4Y
WN0IG5hbWVzIHlvdSB3YW50CiAgICAiIiIKCiAgICBwcm9jZXNzZWQgPSBbXQogICAgZW5jb2RlID
0gZW5jb2RlX3RvX3B5M2J5dGVzX29yX3B5MnN0cgoKICAgIGZvciBrLCB2IGluIGtleXdvcmRzLml
0ZW1zKCk6CiAgICAgICAgIyB3ZSdyZSBwYXNzaW5nIGEgc2hvcnQgYXJnIGFzIGEga3dhcmcsIGV4
YW1wbGU6CiAgICAgICAgIyBjdXQoZD0iXHQiKQogICAgICAgIGlmIGxlbihrKSA9PSAxOgogICAgI
CAgICAgICBpZiB2IGlzIG5vdCBGYWxzZToKICAgICAgICAgICAgICAgIHByb2Nlc3NlZC5hcHBlbm
QoZW5jb2RlKCItIiArIGspKQogICAgICAgICAgICAgICAgaWYgdiBpcyBub3QgVHJ1ZToKICAgICA
gICAgICAgICAgICAgICBwcm9jZXNzZWQuYXBwZW5kKGVuY29kZSh2KSkKCiAgICAgICAgIyB3ZSdy
ZSBkb2luZyBhIGxvbmcgYXJnCiAgICAgICAgZWxzZToKICAgICAgICAgICAgaWYgbm90IHJhdzoKI
CAgICAgICAgICAgICAgIGsgPSBrLnJlcGxhY2UoIl8iLCAiLSIpCgogICAgICAgICAgICBpZiB2IG
lzIFRydWU6CiAgICAgICAgICAgICAgICBwcm9jZXNzZWQuYXBwZW5kKGVuY29kZSgiLS0iICsgayk
pCiAgICAgICAgICAgIGVsaWYgdiBpcyBGYWxzZToKICAgICAgICAgICAgICAgIHBhc3MKICAgICAg
ICAgICAgZWxpZiBzZXAgaXMgTm9uZSBvciBzZXAgPT0gIiAiOgogICAgICAgICAgICAgICAgcHJvY
2Vzc2VkLmFwcGVuZChlbmNvZGUocHJlZml4ICsgaykpCiAgICAgICAgICAgICAgICBwcm9jZXNzZW
QuYXBwZW5kKGVuY29kZSh2KSkKICAgICAgICAgICAgZWxzZToKICAgICAgICAgICAgICAgIGFyZyA
9IGVuY29kZSgiJXMlcyVzJXMiICUgKHByZWZpeCwgaywgc2VwLCB2KSkKICAgICAgICAgICAgICAg
IHByb2Nlc3NlZC5hcHBlbmQoYXJnKQoKICAgIHJldHVybiBwcm9jZXNzZWQKCgpkZWYgX3N0YXJ0X
2RhZW1vbl90aHJlYWQoZm4sIG5hbWUsIGV4Y19xdWV1ZSwgKmFyZ3MpOgogICAgZGVmIHdyYXAoKm
FyZ3MsICoqa3dhcmdzKToKICAgICAgICB0cnk6CiAgICAgICAgICAgIGZuKCphcmdzLCAqKmt3YXJ
ncykKICAgICAgICBleGNlcHQgRXhjZXB0aW9uIGFzIGU6CiAgICAgICAgICAgIGV4Y19xdWV1ZS5w
dXQoZSkKICAgICAgICAgICAgcmFpc2UKCiAgICB0aHJkID0gdGhyZWFkaW5nLlRocmVhZCh0YXJnZ
XQ9d3JhcCwgbmFtZT1uYW1lLCBhcmdzPWFyZ3MpCiAgICB0aHJkLmRhZW1vbiA9IFRydWUKICAgIH
RocmQuc3RhcnQoKQogICAgcmV0dXJuIHRocmQKCgpkZWYgc2V0d2luc2l6ZShmZCwgcm93c19jb2x
zKToKICAgICIiIiBzZXQgdGhlIHRlcm1pbmFsIHNpemUgb2YgYSB0dHkgZmlsZSBkZXNjcmlwdG9y
LiAgYm9ycm93ZWQgbG9naWMKICAgIGZyb20gcGV4cGVjdC5weSAiIiIKICAgIHJvd3MsIGNvbHMgP
SByb3dzX2NvbHMKICAgIFRJT0NTV0lOU1ogPSBnZXRhdHRyKHRlcm1pb3MsICdUSU9DU1dJTlNaJy
wgLTIxNDY5Mjk1NjEpCgogICAgcyA9IHN0cnVjdC5wYWNrKCdISEhIJywgcm93cywgY29scywgMCw
gMCkKICAgIGZjbnRsLmlvY3RsKGZkLCBUSU9DU1dJTlNaLCBzKQoKZGVmIGNvbnN0cnVjdF9zdHJl
YW1yZWFkZXJfY2FsbGJhY2socHJvY2VzcywgaGFuZGxlcik6CiAgICAiIiIgaGVyZSB3ZSdyZSBjb
25zdHJ1Y3RpbmcgYSBjbG9zdXJlIGZvciBvdXIgc3RyZWFtcmVhZGVyIGNhbGxiYWNrLiAgdGhpcw
ogICAgaXMgdXNlZCBpbiB0aGUgY2FzZSB0aGF0IHdlIHBhc3MgYSBjYWxsYmFjayBpbnRvIF9vdXQ
gb3IgX2VyciwgbWVhbmluZyB3ZQogICAgd2FudCB0byBvdXIgY2FsbGJhY2sgdG8gaGFuZGxlIGVh
Y2ggYml0IG9mIG91dHB1dAoKICAgIHdlIGNvbnN0cnVjdCB0aGUgY2xvc3VyZSBiYXNlZCBvbiBob
3cgbWFueSBhcmd1bWVudHMgaXQgdGFrZXMuICB0aGUgcmVhc29uCiAgICBmb3IgdGhpcyBpcyB0by
BtYWtlIGl0IGFzIGVhc3kgYXMgcG9zc2libGUgZm9yIHBlb3BsZSB0byB1c2UsIHdpdGhvdXQKICA
gIGxpbWl0aW5nIHRoZW0uICBhIG5ldyB1c2VyIHdpbGwgYXNzdW1lIHRoZSBjYWxsYmFjayB0YWtl
cyAxIGFyZ3VtZW50ICh0aGUKICAgIGRhdGEpLiAgYXMgdGhleSBnZXQgbW9yZSBhZHZhbmNlZCwgd
GhleSBtYXkgd2FudCB0byB0ZXJtaW5hdGUgdGhlIHByb2Nlc3MsCiAgICBvciBwYXNzIHNvbWUgc3
RkaW4gYmFjaywgYW5kIHdpbGwgcmVhbGl6ZSB0aGF0IHRoZXkgY2FuIHBhc3MgYSBjYWxsYmFjayB
vZgogICAgbW9yZSBhcmdzICIiIgoKCiAgICAjIGltcGxpZWQgYXJnIHJlZmVycyB0byB0aGUgInNl
bGYiIHRoYXQgbWV0aG9kcyB3aWxsIHBhc3MgaW4uICB3ZSBuZWVkIHRvCiAgICAjIGFjY291bnQgZ
m9yIHRoaXMgaW1wbGllZCBhcmcgd2hlbiBmaWd1cmluZyBvdXQgd2hhdCBmdW5jdGlvbiB0aGUgdX
NlcgogICAgIyBwYXNzZWQgaW4gYmFzZWQgb24gbnVtYmVyIG9mIGFyZ3MKICAgIGltcGxpZWRfYXJ
nID0gMAoKICAgIHBhcnRpYWxfYXJncyA9IDAKICAgIGhhbmRsZXJfdG9faW5zcGVjdCA9IGhhbmRs
ZXIKCiAgICBpZiBpc2luc3RhbmNlKGhhbmRsZXIsIHBhcnRpYWwpOgogICAgICAgIHBhcnRpYWxfY
XJncyA9IGxlbihoYW5kbGVyLmFyZ3MpCiAgICAgICAgaGFuZGxlcl90b19pbnNwZWN0ID0gaGFuZG
xlci5mdW5jCgogICAgaWYgaW5zcGVjdC5pc21ldGhvZChoYW5kbGVyX3RvX2luc3BlY3QpOgogICA
gICAgIGltcGxpZWRfYXJnID0gMQogICAgICAgIG51bV9hcmdzID0gZ2V0X251bV9hcmdzKGhhbmRs
ZXJfdG9faW5zcGVjdCkKCiAgICBlbHNlOgogICAgICAgIGlmIGluc3BlY3QuaXNmdW5jdGlvbihoY
W5kbGVyX3RvX2luc3BlY3QpOgogICAgICAgICAgICBudW1fYXJncyA9IGdldF9udW1fYXJncyhoYW
5kbGVyX3RvX2luc3BlY3QpCgogICAgICAgICMgaXMgYW4gb2JqZWN0IGluc3RhbmNlIHdpdGggX19
jYWxsX18gbWV0aG9kCiAgICAgICAgZWxzZToKICAgICAgICAgICAgaW1wbGllZF9hcmcgPSAxCiAg
ICAgICAgICAgIG51bV9hcmdzID0gZ2V0X251bV9hcmdzKGhhbmRsZXJfdG9faW5zcGVjdC5fX2Nhb
GxfXykKCgogICAgbmV0X2FyZ3MgPSBudW1fYXJncyAtIGltcGxpZWRfYXJnIC0gcGFydGlhbF9hcm
dzCgogICAgaGFuZGxlcl9hcmdzID0gKCkKCiAgICAjIGp1c3QgdGhlIGNodW5rCiAgICBpZiBuZXR
fYXJncyA9PSAxOgogICAgICAgIGhhbmRsZXJfYXJncyA9ICgpCgogICAgIyBjaHVuaywgc3RkaW4K
ICAgIGlmIG5ldF9hcmdzID09IDI6CiAgICAgICAgaGFuZGxlcl9hcmdzID0gKHByb2Nlc3Muc3Rka
W4sKQoKICAgICMgY2h1bmssIHN0ZGluLCBwcm9jZXNzCiAgICBlbGlmIG5ldF9hcmdzID09IDM6Ci
AgICAgICAgIyBub3RpY2Ugd2UncmUgb25seSBzdG9yaW5nIGEgd2Vha3JlZiwgdG8gcHJldmVudCB
jeWNsaWMgcmVmZXJlbmNlcwogICAgICAgICMgKHdoZXJlIHRoZSBwcm9jZXNzIGhvbGRzIGEgc3Ry
ZWFtcmVhZGVyLCBhbmQgYSBzdHJlYW1yZWFkZXIgaG9sZHMgYQogICAgICAgICMgaGFuZGxlci1jb
G9zdXJlIHdpdGggYSByZWZlcmVuY2UgdG8gdGhlIHByb2Nlc3MKICAgICAgICBoYW5kbGVyX2FyZ3
MgPSAocHJvY2Vzcy5zdGRpbiwgd2Vha3JlZi5yZWYocHJvY2VzcykpCgogICAgZGVmIGZuKGNodW5
rKToKICAgICAgICAjIHRoaXMgaXMgcHJldHR5IHVnbHksIGJ1dCB3ZSdyZSBldmFsdWF0aW5nIHRo
ZSBwcm9jZXNzIGF0IGNhbGwtdGltZSwKICAgICAgICAjIGJlY2F1c2UgaXQncyBhIHdlYWtyZWYKI
CAgICAgICBhcmdzID0gaGFuZGxlcl9hcmdzCiAgICAgICAgaWYgbGVuKGFyZ3MpID09IDI6CiAgIC
AgICAgICAgIGFyZ3MgPSAoaGFuZGxlcl9hcmdzWzBdLCBoYW5kbGVyX2FyZ3NbMV0oKSkKICAgICA
gICByZXR1cm4gaGFuZGxlcihjaHVuaywgKmFyZ3MpCgogICAgcmV0dXJuIGZuCgoKZGVmIGdldF9l
eGNfZXhpdF9jb2RlX3dvdWxkX3JhaXNlKGV4aXRfY29kZSwgb2tfY29kZXMsIHNpZ3BpcGVfb2spO
gogICAgZXhjID0gTm9uZQogICAgc3VjY2VzcyA9IGV4aXRfY29kZSBpbiBva19jb2RlcwogICAgYm
FkX3NpZyA9IC1leGl0X2NvZGUgaW4gU0lHTkFMU19USEFUX1NIT1VMRF9USFJPV19FWENFUFRJT04
KCiAgICAjIGlmIHRoaXMgaXMgYSBwaXBlZCBjb21tYW5kLCBTSUdQSVBFIG11c3QgYmUgaWdub3Jl
ZCBieSB1cyBhbmQgbm90IHJhaXNlIGFuCiAgICAjIGV4Y2VwdGlvbiwgc2luY2UgaXQncyBwZXJmZ
WN0bHkgbm9ybWFsIGZvciB0aGUgY29uc3VtZXIgb2YgYSBwcm9jZXNzJ3MKICAgICMgcGlwZSB0by
B0ZXJtaW5hdGUgZWFybHkKICAgIGlmIHNpZ3BpcGVfb2sgYW5kIC1leGl0X2NvZGUgPT0gc2lnbmF
sLlNJR1BJUEU6CiAgICAgICAgYmFkX3NpZyA9IEZhbHNlCiAgICAgICAgc3VjY2VzcyA9IFRydWUK
CiAgICBpZiBub3Qgc3VjY2VzcyBvciBiYWRfc2lnOgogICAgICAgIGV4YyA9IGdldF9yY19leGMoZ
XhpdF9jb2RlKQogICAgcmV0dXJuIGV4YwoKCmRlZiBoYW5kbGVfcHJvY2Vzc19leGl0X2NvZGUoZX
hpdF9jb2RlKToKICAgICIiIiB0aGlzIHNob3VsZCBvbmx5IGV2ZXIgYmUgY2FsbGVkIG9uY2UgZm9
yIGVhY2ggY2hpbGQgcHJvY2VzcyAiIiIKICAgICMgaWYgd2UgZXhpdGVkIGZyb20gYSBzaWduYWws
IGxldCBvdXIgZXhpdCBjb2RlIHJlZmxlY3QgdGhhdAogICAgaWYgb3MuV0lGU0lHTkFMRUQoZXhpd
F9jb2RlKToKICAgICAgICBleGl0X2NvZGUgPSAtb3MuV1RFUk1TSUcoZXhpdF9jb2RlKQogICAgIy
BvdGhlcndpc2UganVzdCBnaXZlIHVzIGEgbm9ybWFsIGV4aXQgY29kZQogICAgZWxpZiBvcy5XSUZ
FWElURUQoZXhpdF9jb2RlKToKICAgICAgICBleGl0X2NvZGUgPSBvcy5XRVhJVFNUQVRVUyhleGl0
X2NvZGUpCiAgICBlbHNlOgogICAgICAgIHJhaXNlIFJ1bnRpbWVFcnJvcigiVW5rbm93biBjaGlsZ
CBleGl0IHN0YXR1cyEiKQoKICAgIHJldHVybiBleGl0X2NvZGUKCgpkZWYgbm9faW50ZXJydXB0KH
N5c2NhbGwsICphcmdzLCAqKmt3YXJncyk6CiAgICAiIiIgYSBoZWxwZXIgZm9yIG1ha2luZyBzeXN
0ZW0gY2FsbHMgaW1tdW5lIHRvIEVJTlRSICIiIgogICAgcmV0ID0gTm9uZQoKICAgIHdoaWxlIFRy
dWU6CiAgICAgICAgdHJ5OgogICAgICAgICAgICByZXQgPSBzeXNjYWxsKCphcmdzLCAqKmt3YXJnc
ykKICAgICAgICBleGNlcHQgT1NFcnJvciBhcyBlOgogICAgICAgICAgICBpZiBlLmVycm5vID09IG
Vycm5vLkVJTlRSOgogICAgICAgICAgICAgICAgY29udGludWUKICAgICAgICAgICAgZWxzZToKICA
gICAgICAgICAgICAgIHJhaXNlCiAgICAgICAgZWxzZToKICAgICAgICAgICAgYnJlYWsKCiAgICBy
ZXR1cm4gcmV0CgoKY2xhc3MgT1Byb2Mob2JqZWN0KToKICAgICIiIiB0aGlzIGNsYXNzIGlzIGluc
3RhbnRpYXRlZCBieSBSdW5uaW5nQ29tbWFuZCBmb3IgYSBjb21tYW5kIHRvIGJlIGV4ZWMnZC4KIC
AgIGl0IGhhbmRsZXMgYWxsIHRoZSBuYXN0eSBidXNpbmVzcyBpbnZvbHZlZCB3aXRoIGNvcnJlY3R
seSBzZXR0aW5nIHVwIHRoZQogICAgaW5wdXQvb3V0cHV0IHRvIHRoZSBjaGlsZCBwcm9jZXNzLiAg
aXQgZ2V0cyBpdHMgbmFtZSBmb3Igc3VicHJvY2Vzcy5Qb3BlbgogICAgKHByb2Nlc3Mgb3BlbikgY
nV0IHdlJ3JlIGNhbGxpbmcgb3VycyBPUHJvYyAob3BlbiBwcm9jZXNzKSAiIiIKCiAgICBfZGVmYX
VsdF93aW5kb3dfc2l6ZSA9ICgyNCwgODApCgogICAgIyB1c2VkIGluIHJlZGlyZWN0aW5nCiAgICB
TVERPVVQgPSAtMQogICAgU1RERVJSID0gLTIKCiAgICBkZWYgX19pbml0X18oc2VsZiwgY29tbWFu
ZCwgcGFyZW50X2xvZywgY21kLCBzdGRpbiwgc3Rkb3V0LCBzdGRlcnIsCiAgICAgICAgICAgIGNhb
GxfYXJncywgcGlwZSwgcHJvY2Vzc19hc3NpZ25fbG9jayk6CiAgICAgICAgIiIiCiAgICAgICAgIC
AgIGNtZCBpcyB0aGUgZnVsbCBzdHJpbmcgdGhhdCB3aWxsIGJlIGV4ZWMnZC4gIGl0IGluY2x1ZGV
zIHRoZSBwcm9ncmFtCiAgICAgICAgICAgIG5hbWUgYW5kIGFsbCBpdHMgYXJndW1lbnRzCgogICAg
ICAgICAgICBzdGRpbiwgc3Rkb3V0LCBzdGRlcnIgYXJlIHdoYXQgdGhlIGNoaWxkIHdpbGwgdXNlI
GZvciBzdGFuZGFyZAogICAgICAgICAgICBpbnB1dC9vdXRwdXQvZXJyCgogICAgICAgICAgICBjYW
xsX2FyZ3MgaXMgYSBtYXBwaW5nIG9mIGFsbCB0aGUgc3BlY2lhbCBrZXl3b3JkIGFyZ3VtZW50cyB
0byBhcHBseQogICAgICAgICAgICB0byB0aGUgY2hpbGQgcHJvY2VzcwogICAgICAgICIiIgogICAg
ICAgIHNlbGYuY29tbWFuZCA9IGNvbW1hbmQKICAgICAgICBzZWxmLmNhbGxfYXJncyA9IGNhbGxfY
XJncwoKICAgICAgICAjIGNvbnZlbmllbmNlCiAgICAgICAgY2EgPSBzZWxmLmNhbGxfYXJncwoKIC
AgICAgICBpZiBjYVsidWlkIl0gaXMgbm90IE5vbmU6CiAgICAgICAgICAgIGlmIG9zLmdldHVpZCg
pICE9IDA6CiAgICAgICAgICAgICAgICByYWlzZSBSdW50aW1lRXJyb3IoIlVJRCBzZXR0aW5nIHJl
cXVpcmVzIHJvb3QgcHJpdmlsZWdlcyIpCgogICAgICAgICAgICB0YXJnZXRfdWlkID0gY2FbInVpZ
CJdCgogICAgICAgICAgICBwd3JlYyA9IHB3ZC5nZXRwd3VpZChjYVsidWlkIl0pCiAgICAgICAgIC
AgIHRhcmdldF9naWQgPSBwd3JlYy5wd19naWQKCiAgICAgICAgIyBJIGhhZCBpc3N1ZXMgd2l0aCB
nZXR0aW5nICdJbnB1dC9PdXRwdXQgZXJyb3IgcmVhZGluZyBzdGRpbicgZnJvbSBkZCwKICAgICAg
ICAjIHVudGlsIEkgc2V0IF90dHlfb3V0PUZhbHNlCiAgICAgICAgaWYgY2FbInBpcGVkIl06CiAgI
CAgICAgICAgIGNhWyJ0dHlfb3V0Il0gPSBGYWxzZQoKICAgICAgICBzZWxmLl9zdGRpbl9wcm9jZX
NzID0gTm9uZQoKCiAgICAgICAgIyBpZiB0aGUgb2JqZWN0cyB0aGF0IHdlIGFyZSBwYXNzaW5nIHR
vIHRoZSBPUHJvYyBoYXBwZW4gdG8gYmUgYQogICAgICAgICMgZmlsZS1saWtlIG9iamVjdCB0aGF0
IGlzIGEgdHR5LCBmb3IgZXhhbXBsZSBgc3lzLnN0ZGluYCwgdGhlbiwgbGF0ZXIKICAgICAgICAjI
G9uIGluIHRoaXMgY29uc3RydWN0b3IsIHdlJ3JlIGdvaW5nIHRvIHNraXAgb3V0IG9uIHNldHRpbm
cgdXAgcGlwZXMKICAgICAgICAjIGFuZCBwc2V1ZG90ZXJtaW5hbHMgZm9yIHRob3NlIGVuZHBvaW5
0cwogICAgICAgIHN0ZGluX2lzX3R0eV9vcl9waXBlID0gb2JfaXNfdHR5KHN0ZGluKSBvciBvYl9p
c19waXBlKHN0ZGluKQogICAgICAgIHN0ZG91dF9pc190dHlfb3JfcGlwZSA9IG9iX2lzX3R0eShzd
GRvdXQpIG9yIG9iX2lzX3BpcGUoc3Rkb3V0KQogICAgICAgIHN0ZGVycl9pc190dHlfb3JfcGlwZS
A9IG9iX2lzX3R0eShzdGRlcnIpIG9yIG9iX2lzX3BpcGUoc3RkZXJyKQoKICAgICAgICB0ZWVfb3V
0ID0gY2FbInRlZSJdIGluIChUcnVlLCAib3V0IikKICAgICAgICB0ZWVfZXJyID0gY2FbInRlZSJd
ID09ICJlcnIiCgogICAgICAgICMgaWYgd2UncmUgcGFzc2luZyBpbiBhIGN1c3RvbSBzdGRvdXQvb
3V0L2VyciB2YWx1ZSwgd2Ugb2J2aW91c2x5IGhhdmUKICAgICAgICAjIHRvIGZvcmNlIG5vdCB1c2
luZyBzaW5nbGVfdHR5CiAgICAgICAgY3VzdG9tX2luX291dF9lcnIgPSBzdGRpbiBvciBzdGRvdXQ
gb3Igc3RkZXJyCgogICAgICAgIHNpbmdsZV90dHkgPSAoY2FbInR0eV9pbiJdIGFuZCBjYVsidHR5
X291dCJdKVwKICAgICAgICAgICAgICAgIGFuZCBub3QgY3VzdG9tX2luX291dF9lcnIKCiAgICAgI
CAgIyB0aGlzIGxvZ2ljIGlzIGEgbGl0dGxlIGNvbnZvbHV0ZWQsIGJ1dCBiYXNpY2FsbHkgdGhpcy
B0b3AtbGV2ZWwKICAgICAgICAjIGlmL2Vsc2UgaXMgZm9yIGNvbnNvbGlkYXRpbmcgaW5wdXQgYW5
kIG91dHB1dCBUVFlzIGludG8gYSBzaW5nbGUKICAgICAgICAjIFRUWS4gIHRoaXMgaXMgdGhlIG9u
bHkgd2F5IHNvbWUgc2VjdXJlIHByb2dyYW1zIGxpa2Ugc3NoIHdpbGwKICAgICAgICAjIG91dHB1d
CBjb3JyZWN0bHkgKGlzIGlmIHN0ZG91dCBhbmQgc3RkaW4gYXJlIGJvdGggdGhlIHNhbWUgVFRZKQ
ogICAgICAgIGlmIHNpbmdsZV90dHk6CiAgICAgICAgICAgIHNlbGYuX3N0ZGluX3JlYWRfZmQsIHN
lbGYuX3N0ZGluX3dyaXRlX2ZkID0gcHR5Lm9wZW5wdHkoKQoKICAgICAgICAgICAgc2VsZi5fc3Rk
b3V0X3JlYWRfZmQgPSBvcy5kdXAoc2VsZi5fc3RkaW5fcmVhZF9mZCkKICAgICAgICAgICAgc2VsZ
i5fc3Rkb3V0X3dyaXRlX2ZkID0gb3MuZHVwKHNlbGYuX3N0ZGluX3dyaXRlX2ZkKQoKICAgICAgIC
AgICAgc2VsZi5fc3RkZXJyX3JlYWRfZmQgPSBvcy5kdXAoc2VsZi5fc3RkaW5fcmVhZF9mZCkKICA
gICAgICAgICAgc2VsZi5fc3RkZXJyX3dyaXRlX2ZkID0gb3MuZHVwKHNlbGYuX3N0ZGluX3dyaXRl
X2ZkKQoKICAgICAgICAjIGRvIG5vdCBjb25zb2xpZGF0ZSBzdGRpbiBhbmQgc3Rkb3V0LiAgdGhpc
yBpcyB0aGUgbW9zdCBjb21tb24gdXNlLQogICAgICAgICMgY2FzZQogICAgICAgIGVsc2U6CiAgIC
AgICAgICAgICMgdGhpcyBjaGVjayBoZXJlIGlzIGJlY2F1c2Ugd2UgbWF5IGJlIGRvaW5nIHBpcGl
uZyBhbmQgc28gb3VyIHN0ZGluCiAgICAgICAgICAgICMgbWlnaHQgYmUgYW4gaW5zdGFuY2Ugb2Yg
T1Byb2MKICAgICAgICAgICAgaWYgaXNpbnN0YW5jZShzdGRpbiwgT1Byb2MpIGFuZCBzdGRpbi5jY
WxsX2FyZ3NbInBpcGVkIl06CiAgICAgICAgICAgICAgICBzZWxmLl9zdGRpbl93cml0ZV9mZCA9IH
N0ZGluLl9waXBlX2ZkCiAgICAgICAgICAgICAgICBzZWxmLl9zdGRpbl9yZWFkX2ZkID0gTm9uZQo
gICAgICAgICAgICAgICAgc2VsZi5fc3RkaW5fcHJvY2VzcyA9IHN0ZGluCgogICAgICAgICAgICBl
bGlmIHN0ZGluX2lzX3R0eV9vcl9waXBlOgogICAgICAgICAgICAgICAgc2VsZi5fc3RkaW5fd3Jpd
GVfZmQgPSBvcy5kdXAoZ2V0X2ZpbGVubyhzdGRpbikpCiAgICAgICAgICAgICAgICBzZWxmLl9zdG
Rpbl9yZWFkX2ZkID0gTm9uZQoKICAgICAgICAgICAgZWxpZiBjYVsidHR5X2luIl06CiAgICAgICA
gICAgICAgICBzZWxmLl9zdGRpbl9yZWFkX2ZkLCBzZWxmLl9zdGRpbl93cml0ZV9mZCA9IHB0eS5v
cGVucHR5KCkKCiAgICAgICAgICAgICMgdHR5X2luPUZhbHNlIGlzIHRoZSBkZWZhdWx0CiAgICAgI
CAgICAgIGVsc2U6CiAgICAgICAgICAgICAgICBzZWxmLl9zdGRpbl93cml0ZV9mZCwgc2VsZi5fc3
RkaW5fcmVhZF9mZCA9IG9zLnBpcGUoKQoKCiAgICAgICAgICAgIGlmIHN0ZG91dF9pc190dHlfb3J
fcGlwZSBhbmQgbm90IHRlZV9vdXQ6CiAgICAgICAgICAgICAgICBzZWxmLl9zdGRvdXRfd3JpdGVf
ZmQgPSBvcy5kdXAoZ2V0X2ZpbGVubyhzdGRvdXQpKQogICAgICAgICAgICAgICAgc2VsZi5fc3Rkb
3V0X3JlYWRfZmQgPSBOb25lCgogICAgICAgICAgICAjIHR0eV9vdXQ9VHJ1ZSBpcyB0aGUgZGVmYX
VsdAogICAgICAgICAgICBlbGlmIGNhWyJ0dHlfb3V0Il06CiAgICAgICAgICAgICAgICBzZWxmLl9
zdGRvdXRfcmVhZF9mZCwgc2VsZi5fc3Rkb3V0X3dyaXRlX2ZkID0gcHR5Lm9wZW5wdHkoKQoKICAg
ICAgICAgICAgZWxzZToKICAgICAgICAgICAgICAgIHNlbGYuX3N0ZG91dF9yZWFkX2ZkLCBzZWxmL
l9zdGRvdXRfd3JpdGVfZmQgPSBvcy5waXBlKCkKCiAgICAgICAgICAgICMgdW5sZXNzIFNUREVSUi
BpcyBnb2luZyB0byBTVERPVVQsIGl0IEFMV0FZUyBuZWVkcyB0byBiZSBhIHBpcGUsCiAgICAgICA
gICAgICMgYW5kIG5ldmVyIGEgUFRZLiAgdGhlIHJlYXNvbiBmb3IgdGhpcyBpcyBub3QgdG90YWxs
eSBjbGVhciB0byBtZSwKICAgICAgICAgICAgIyBidXQgaXQgaGFzIHRvIGRvIHdpdGggdGhlIGZhY
3QgdGhhdCBpZiBTVERFUlIgaXNuJ3Qgc2V0IGFzIHRoZQogICAgICAgICAgICAjIENUVFkgKGJlY2
F1c2UgU1RET1VUIGlzKSwgdGhlIFNUREVSUiBidWZmZXIgd29uJ3QgYWx3YXlzIGZsdXNoCiAgICA
gICAgICAgICMgYnkgdGhlIHRpbWUgdGhlIHByb2Nlc3MgZXhpdHMsIGFuZCB0aGUgZGF0YSB3aWxs
IGJlIGxvc3QuCiAgICAgICAgICAgICMgaSd2ZSBvbmx5IHNlZW4gdGhpcyBvbiBPU1guCiAgICAgI
CAgICAgIGlmIHN0ZGVyciBpcyBPUHJvYy5TVERPVVQ6CiAgICAgICAgICAgICAgICAjIGlmIHN0ZG
VyciBpcyBnb2luZyB0byBzdGRvdXQsIGJ1dCBzdGRvdXQgaXMgYSB0dHkgb3IgYSBwaXBlLAogICA
gICAgICAgICAgICAgIyB3ZSBzaG91bGQgbm90IHNwZWNpZnkgYSByZWFkX2ZkLCBiZWNhdXNlIHN0
ZG91dCBpcyBkdXAnZAogICAgICAgICAgICAgICAgIyBkaXJlY3RseSB0byB0aGUgc3Rkb3V0IGZkI
ChubyBwaXBlKSwgYW5kIHNvIHN0ZGVyciB3b24ndCBoYXZlCiAgICAgICAgICAgICAgICAjIGEgc2
xhdmUgZW5kIG9mIGEgcGlwZSBlaXRoZXIgdG8gZHVwCiAgICAgICAgICAgICAgICBpZiBzdGRvdXR
faXNfdHR5X29yX3BpcGUgYW5kIG5vdCB0ZWVfb3V0OgogICAgICAgICAgICAgICAgICAgIHNlbGYu
X3N0ZGVycl9yZWFkX2ZkID0gTm9uZQogICAgICAgICAgICAgICAgZWxzZToKICAgICAgICAgICAgI
CAgICAgICBzZWxmLl9zdGRlcnJfcmVhZF9mZCA9IG9zLmR1cChzZWxmLl9zdGRvdXRfcmVhZF9mZC
kKICAgICAgICAgICAgICAgIHNlbGYuX3N0ZGVycl93cml0ZV9mZCA9IG9zLmR1cChzZWxmLl9zdGR
vdXRfd3JpdGVfZmQpCgoKICAgICAgICAgICAgZWxpZiBzdGRlcnJfaXNfdHR5X29yX3BpcGUgYW5k
IG5vdCB0ZWVfZXJyOgogICAgICAgICAgICAgICAgc2VsZi5fc3RkZXJyX3dyaXRlX2ZkID0gb3MuZ
HVwKGdldF9maWxlbm8oc3RkZXJyKSkKICAgICAgICAgICAgICAgIHNlbGYuX3N0ZGVycl9yZWFkX2
ZkID0gTm9uZQoKICAgICAgICAgICAgZWxzZToKICAgICAgICAgICAgICAgIHNlbGYuX3N0ZGVycl9
yZWFkX2ZkLCBzZWxmLl9zdGRlcnJfd3JpdGVfZmQgPSBvcy5waXBlKCkKCgogICAgICAgIHBpcGVk
ID0gY2FbInBpcGVkIl0KICAgICAgICBzZWxmLl9waXBlX2ZkID0gTm9uZQogICAgICAgIGlmIHBpc
GVkOgogICAgICAgICAgICBmZF90b191c2UgPSBzZWxmLl9zdGRvdXRfcmVhZF9mZAogICAgICAgIC
AgICBpZiBwaXBlZCA9PSAiZXJyIjoKICAgICAgICAgICAgICAgIGZkX3RvX3VzZSA9IHNlbGYuX3N
0ZGVycl9yZWFkX2ZkCiAgICAgICAgICAgIHNlbGYuX3BpcGVfZmQgPSBvcy5kdXAoZmRfdG9fdXNl
KQoKCiAgICAgICAgbmV3X3Nlc3Npb24gPSBjYVsibmV3X3Nlc3Npb24iXQogICAgICAgIG5lZWRzX
2N0dHkgPSBjYVsidHR5X2luIl0gYW5kIG5ld19zZXNzaW9uCgogICAgICAgIHNlbGYuY3R0eSA9IE
5vbmUKICAgICAgICBpZiBuZWVkc19jdHR5OgogICAgICAgICAgICBzZWxmLmN0dHkgPSBvcy50dHl
uYW1lKHNlbGYuX3N0ZGluX3dyaXRlX2ZkKQoKICAgICAgICAjIHRoaXMgaXMgYSBoYWNrLCBidXQg
d2hhdCB3ZSdyZSBkb2luZyBoZXJlIGlzIGludGVudGlvbmFsbHkgdGhyb3dpbmcgYW4KICAgICAgI
CAjIE9TRXJyb3IgZXhjZXB0aW9uIGlmIG91ciBjaGlsZCBwcm9jZXNzZXMncyBkaXJlY3RvcnkgZG
9lc24ndCBleGlzdCwKICAgICAgICAjIGJ1dCB3ZSdyZSBkb2luZyBpdCBCRUZPUkUgd2UgZm9yay4
gIHRoZSByZWFzb24gZm9yIGJlZm9yZSB0aGUgZm9yayBpcwogICAgICAgICMgZXJyb3IgaGFuZGxp
bmcuICBpJ20gY3VycmVudGx5IHRvbyBsYXp5IHRvIGltcGxlbWVudCB3aGF0CiAgICAgICAgIyBzd
WJwcm9jZXNzLnB5IGRpZCBhbmQgc2V0IHVwIGEgZXJyb3IgcGlwZSB0byBoYW5kbGUgZXhjZXB0aW
9ucyB0aGF0CiAgICAgICAgIyBoYXBwZW4gaW4gdGhlIGNoaWxkIGJldHdlZW4gZm9yayBhbmQgZXh
lYy4gIGl0IGhhcyBvbmx5IGJlZW4gc2VlbiBpbgogICAgICAgICMgdGhlIHdpbGQgZm9yIGEgbWlz
c2luZyBjd2QsIHNvIHdlJ2xsIGhhbmRsZSBpdCBoZXJlLgogICAgICAgIGN3ZCA9IGNhWyJjd2QiX
QogICAgICAgIGlmIGN3ZCBpcyBub3QgTm9uZSBhbmQgbm90IG9zLnBhdGguZXhpc3RzKGN3ZCk6Ci
AgICAgICAgICAgIG9zLmNoZGlyKGN3ZCkKCiAgICAgICAgZ2NfZW5hYmxlZCA9IGdjLmlzZW5hYmx
lZCgpCiAgICAgICAgaWYgZ2NfZW5hYmxlZDoKICAgICAgICAgICAgZ2MuZGlzYWJsZSgpCgogICAg
ICAgICMgZm9yIHN5bmNocm9uaXppbmcKICAgICAgICBzZXNzaW9uX3BpcGVfcmVhZCwgc2Vzc2lvb
l9waXBlX3dyaXRlID0gb3MucGlwZSgpCiAgICAgICAgZXhjX3BpcGVfcmVhZCwgZXhjX3BpcGVfd3
JpdGUgPSBvcy5waXBlKCkKCiAgICAgICAgIyB0aGlzIHBpcGUgaXMgZm9yIHN5bmNocm9uemluZyB
3aXRoIHRoZSBjaGlsZCB0aGF0IHRoZSBwYXJlbnQgaGFzCiAgICAgICAgIyBjbG9zZWQgaXRzIGlu
L291dC9lcnIgZmRzLiAgdGhpcyBpcyBhIGJ1ZyBvbiBPU1ggKGJ1dCBub3QgbGludXgpLAogICAgI
CAgICMgd2hlcmUgd2UgY2FuIGxvc2Ugb3V0cHV0IHNvbWV0aW1lcywgZHVlIHRvIGEgcmFjZSwgaW
Ygd2UgZG8KICAgICAgICAjIG9zLmNsb3NlKHNlbGYuX3N0ZG91dF93cml0ZV9mZCkgaW4gdGhlIHB
hcmVudCBhZnRlciB0aGUgY2hpbGQgc3RhcnRzCiAgICAgICAgIyB3cml0aW5nLgogICAgICAgIGlm
IElTX09TWDoKICAgICAgICAgICAgY2xvc2VfcGlwZV9yZWFkLCBjbG9zZV9waXBlX3dyaXRlID0gb
3MucGlwZSgpCgogICAgICAgICMgc2Vzc2lvbiBpZCwgZ3JvdXAgaWQsIHByb2Nlc3MgaWQKICAgIC
AgICBzZWxmLnNpZCA9IE5vbmUKICAgICAgICBzZWxmLnBnaWQgPSBOb25lCiAgICAgICAgc2VsZi5
waWQgPSBvcy5mb3JrKCkKCiAgICAgICAgIyBjaGlsZAogICAgICAgIGlmIHNlbGYucGlkID09IDA6
ICMgcHJhZ21hOiBubyBjb3ZlcgogICAgICAgICAgICBpZiBJU19PU1g6CiAgICAgICAgICAgICAgI
CBvcy5yZWFkKGNsb3NlX3BpcGVfcmVhZCwgMSkKICAgICAgICAgICAgICAgIG9zLmNsb3NlKGNsb3
NlX3BpcGVfcmVhZCkKICAgICAgICAgICAgICAgIG9zLmNsb3NlKGNsb3NlX3BpcGVfd3JpdGUpCgo
gICAgICAgICAgICB0cnk6CiAgICAgICAgICAgICAgICAjIGlnbm9yaW5nIFNJR0hVUCBsZXRzIHVz
IHBlcnNpc3QgZXZlbiBhZnRlciB0aGUgcGFyZW50IHByb2Nlc3MKICAgICAgICAgICAgICAgICMgZ
XhpdHMuICBvbmx5IGlnbm9yZSBpZiB3ZSdyZSBiYWNrZ3JvdW5kZWQKICAgICAgICAgICAgICAgIG
lmIGNhWyJiZyJdIGlzIFRydWU6CiAgICAgICAgICAgICAgICAgICAgc2lnbmFsLnNpZ25hbChzaWd
uYWwuU0lHSFVQLCBzaWduYWwuU0lHX0lHTikKCiAgICAgICAgICAgICAgICAjIHB5dGhvbiBpZ25v
cmVzIFNJR1BJUEUgYnkgZGVmYXVsdC4gIHdlIG11c3QgbWFrZSBzdXJlIHRvIHB1dAogICAgICAgI
CAgICAgICAgIyB0aGlzIGJlaGF2aW9yIGJhY2sgdG8gdGhlIGRlZmF1bHQgZm9yIHNwYXduZWQgcH
JvY2Vzc2VzLAogICAgICAgICAgICAgICAgIyBvdGhlcndpc2UgU0lHUElQRSB3b24ndCBraWxsIHB
pcGVkIHByb2Nlc3Nlcywgd2hpY2ggaXMgd2hhdCB3ZQogICAgICAgICAgICAgICAgIyBuZWVkLCBz
byB0aGF0IHdlIGNhbiBjaGVjayB0aGUgZXJyb3IgY29kZSBvZiB0aGUga2lsbGVkCiAgICAgICAgI
CAgICAgICAjIHByb2Nlc3MgdG8gc2VlIHRoYXQgU0lHUElQRSBraWxsZWQgaXQKICAgICAgICAgIC
AgICAgIHNpZ25hbC5zaWduYWwoc2lnbmFsLlNJR1BJUEUsIHNpZ25hbC5TSUdfREZMKQoKICAgICA
gICAgICAgICAgICMgcHV0IG91ciBmb3JrZWQgcHJvY2VzcyBpbiBhIG5ldyBzZXNzaW9uPyAgdGhp
cyB3aWxsIHJlbGlucXVpc2gKICAgICAgICAgICAgICAgICMgYW55IGNvbnRyb2wgb2Ygb3VyIGlua
GVyaXRlZCBDVFRZIGFuZCBhbHNvIG1ha2Ugb3VyIHBhcmVudAogICAgICAgICAgICAgICAgIyBwcm
9jZXNzIGluaXQKICAgICAgICAgICAgICAgIGlmIG5ld19zZXNzaW9uOgogICAgICAgICAgICAgICA
gICAgIG9zLnNldHNpZCgpCiAgICAgICAgICAgICAgICAjIGlmIHdlJ3JlIG5vdCBnb2luZyBpbiBh
IG5ldyBzZXNzaW9uLCB3ZSBzaG91bGQgZ28gaW4gYSBuZXcKICAgICAgICAgICAgICAgICMgcHJvY
2VzcyBncm91cC4gIHRoaXMgd2F5LCBvdXIgcHJvY2VzcywgYW5kIGFueSBjaGlsZHJlbiBpdAogIC
AgICAgICAgICAgICAgIyBzcGF3bnMsIGFyZSBhbG9uZSwgY29udGFpbmVkIGVudGlyZWx5IGluIG9
uZSBncm91cC4gIGlmIHdlCiAgICAgICAgICAgICAgICAjIGRpZG4ndCBkbyB0aGlzLCBhbmQgZGlk
bid0IHVzZSBhIG5ldyBzZXNzaW9uLCB0aGVuIG91ciBleGVjJ2QKICAgICAgICAgICAgICAgICMgc
HJvY2VzcyAqY291bGQqIGV4aXN0IGluIHRoZSBzYW1lIGdyb3VwIGFzIG91ciBweXRob24gcHJvY2
VzcywKICAgICAgICAgICAgICAgICMgZGVwZW5kaW5nIG9uIGhvdyB3ZSBsYXVuY2ggdGhlIHByb2N
lc3MgKGZyb20gYSBzaGVsbCwgb3Igc29tZQogICAgICAgICAgICAgICAgIyBvdGhlciB3YXkpCiAg
ICAgICAgICAgICAgICBlbHNlOgogICAgICAgICAgICAgICAgICAgIG9zLnNldHBncnAoKQoKICAgI
CAgICAgICAgICAgIHNpZCA9IG9zLmdldHNpZCgwKQogICAgICAgICAgICAgICAgcGdpZCA9IG9zLm
dldHBnaWQoMCkKICAgICAgICAgICAgICAgIHBheWxvYWQgPSAoIiVkLCVkIiAlIChzaWQsIHBnaWQ
pKS5lbmNvZGUoREVGQVVMVF9FTkNPRElORykKICAgICAgICAgICAgICAgIG9zLndyaXRlKHNlc3Np
b25fcGlwZV93cml0ZSwgcGF5bG9hZCkKCiAgICAgICAgICAgICAgICBpZiBjYVsidHR5X291dCJdI
GFuZCBub3Qgc3Rkb3V0X2lzX3R0eV9vcl9waXBlIGFuZCBub3Qgc2luZ2xlX3R0eToKICAgICAgIC
AgICAgICAgICAgICAjIHNldCByYXcgbW9kZSwgc28gdGhlcmUgaXNuJ3QgYW55IHdlaXJkIHRyYW5
zbGF0aW9uIG9mCiAgICAgICAgICAgICAgICAgICAgIyBuZXdsaW5lcyB0byBcclxuIGFuZCBvdGhl
ciBvZGRpdGllcy4gIHdlJ3JlIG5vdCBvdXRwdXR0aW5nCiAgICAgICAgICAgICAgICAgICAgIyB0b
yBhIHRlcm1pbmFsIGFueXdheXMKICAgICAgICAgICAgICAgICAgICAjCiAgICAgICAgICAgICAgIC
AgICAgIyB3ZSBIQVZFIHRvIGRvIHRoaXMgaGVyZSwgYW5kIG5vdCBpbiB0aGUgcGFyZW50IHByb2N
lc3MsCiAgICAgICAgICAgICAgICAgICAgIyBiZWNhdXNlIHdlIGhhdmUgdG8gZ3VhcmFudGVlIHRo
YXQgdGhpcyBpcyBzZXQgYmVmb3JlIHRoZQogICAgICAgICAgICAgICAgICAgICMgY2hpbGQgcHJvY
2VzcyBpcyBydW4sIGFuZCB3ZSBjYW4ndCBkbyBpdCB0d2ljZS4KICAgICAgICAgICAgICAgICAgIC
B0dHkuc2V0cmF3KHNlbGYuX3N0ZG91dF93cml0ZV9mZCkKCgogICAgICAgICAgICAgICAgIyBpZiB
0aGUgcGFyZW50LXNpZGUgZmQgZm9yIHN0ZGluIGV4aXN0cywgY2xvc2UgaXQuICB0aGUgY2FzZQog
ICAgICAgICAgICAgICAgIyB3aGVyZSBpdCBtYXkgbm90IGV4aXN0IGlzIGlmIHdlJ3JlIHVzaW5nI
HBpcGluZwogICAgICAgICAgICAgICAgaWYgc2VsZi5fc3RkaW5fcmVhZF9mZDoKICAgICAgICAgIC
AgICAgICAgICBvcy5jbG9zZShzZWxmLl9zdGRpbl9yZWFkX2ZkKQoKICAgICAgICAgICAgICAgIGl
mIHNlbGYuX3N0ZG91dF9yZWFkX2ZkOgogICAgICAgICAgICAgICAgICAgIG9zLmNsb3NlKHNlbGYu
X3N0ZG91dF9yZWFkX2ZkKQoKICAgICAgICAgICAgICAgIGlmIHNlbGYuX3N0ZGVycl9yZWFkX2ZkO
gogICAgICAgICAgICAgICAgICAgIG9zLmNsb3NlKHNlbGYuX3N0ZGVycl9yZWFkX2ZkKQoKICAgIC
AgICAgICAgICAgIG9zLmNsb3NlKHNlc3Npb25fcGlwZV9yZWFkKQogICAgICAgICAgICAgICAgb3M
uY2xvc2UoZXhjX3BpcGVfcmVhZCkKCiAgICAgICAgICAgICAgICBpZiBjd2Q6CiAgICAgICAgICAg
ICAgICAgICAgb3MuY2hkaXIoY3dkKQoKICAgICAgICAgICAgICAgIG9zLmR1cDIoc2VsZi5fc3Rka
W5fd3JpdGVfZmQsIDApCiAgICAgICAgICAgICAgICBvcy5kdXAyKHNlbGYuX3N0ZG91dF93cml0ZV
9mZCwgMSkKICAgICAgICAgICAgICAgIG9zLmR1cDIoc2VsZi5fc3RkZXJyX3dyaXRlX2ZkLCAyKQo
KCiAgICAgICAgICAgICAgICAjIHNldCBvdXIgY29udHJvbGxpbmcgdGVybWluYWwsIGJ1dCBvbmx5
IGlmIHdlJ3JlIHVzaW5nIGEgdHR5CiAgICAgICAgICAgICAgICAjIGZvciBzdGRpbi4gIGl0IGRvZ
XNuJ3QgbWFrZSBzZW5zZSB0byBoYXZlIGEgY3R0eSBvdGhlcndpc2UKICAgICAgICAgICAgICAgIG
lmIG5lZWRzX2N0dHk6CiAgICAgICAgICAgICAgICAgICAgdG1wX2ZkID0gb3Mub3Blbihvcy50dHl
uYW1lKDApLCBvcy5PX1JEV1IpCiAgICAgICAgICAgICAgICAgICAgb3MuY2xvc2UodG1wX2ZkKQoK
ICAgICAgICAgICAgICAgIGlmIGNhWyJ0dHlfb3V0Il0gYW5kIG5vdCBzdGRvdXRfaXNfdHR5X29yX
3BpcGU6CiAgICAgICAgICAgICAgICAgICAgc2V0d2luc2l6ZSgxLCBjYVsidHR5X3NpemUiXSkKCi
AgICAgICAgICAgICAgICBpZiBjYVsidWlkIl0gaXMgbm90IE5vbmU6CiAgICAgICAgICAgICAgICA
gICAgb3Muc2V0Z2lkKHRhcmdldF9naWQpCiAgICAgICAgICAgICAgICAgICAgb3Muc2V0dWlkKHRh
cmdldF91aWQpCgogICAgICAgICAgICAgICAgcHJlZXhlY19mbiA9IGNhWyJwcmVleGVjX2ZuIl0KI
CAgICAgICAgICAgICAgIGlmIGNhbGxhYmxlKHByZWV4ZWNfZm4pOgogICAgICAgICAgICAgICAgIC
AgIHByZWV4ZWNfZm4oKQoKCiAgICAgICAgICAgICAgICAjIGRvbid0IGluaGVyaXQgZmlsZSBkZXN
jcmlwdG9ycwogICAgICAgICAgICAgICAgbWF4X2ZkID0gcmVzb3VyY2UuZ2V0cmxpbWl0KHJlc291
cmNlLlJMSU1JVF9OT0ZJTEUpWzBdCiAgICAgICAgICAgICAgICBvcy5jbG9zZXJhbmdlKDMsIG1he
F9mZCkKCiAgICAgICAgICAgICAgICAjIGFjdHVhbGx5IGV4ZWN1dGUgdGhlIHByb2Nlc3MKICAgIC
AgICAgICAgICAgIGlmIGNhWyJlbnYiXSBpcyBOb25lOgogICAgICAgICAgICAgICAgICAgIG9zLmV
4ZWN2KGNtZFswXSwgY21kKQogICAgICAgICAgICAgICAgZWxzZToKICAgICAgICAgICAgICAgICAg
ICBvcy5leGVjdmUoY21kWzBdLCBjbWQsIGNhWyJlbnYiXSkKCiAgICAgICAgICAgICMgd2UgbXVzd
CBlbnN1cmUgdGhhdCB3ZSBjYXJlZnVsbHkgZXhpdCB0aGUgY2hpbGQgcHJvY2VzcyBvbgogICAgIC
AgICAgICAjIGV4Y2VwdGlvbiwgb3RoZXJ3aXNlIHRoZSBwYXJlbnQgcHJvY2VzcyBjb2RlIHdpbGw
gYmUgZXhlY3V0ZWQKICAgICAgICAgICAgIyB0d2ljZSBvbiBleGNlcHRpb24gaHR0cHM6Ly9naXRo
dWIuY29tL2Ftb2ZmYXQvc2gvaXNzdWVzLzIwMgogICAgICAgICAgICAjCiAgICAgICAgICAgICMga
WYgeW91ciBwYXJlbnQgcHJvY2VzcyBleHBlcmllbmNlcyBhbiBleGl0IGNvZGUgMjU1LCBpdCBpcy
Btb3N0CiAgICAgICAgICAgICMgbGlrZWx5IHRoYXQgYW4gZXhjZXB0aW9uIG9jY3VycmVkIGJldHd
lZW4gdGhlIGZvcmsgb2YgdGhlIGNoaWxkCiAgICAgICAgICAgICMgYW5kIHRoZSBleGVjLiAgdGhp
cyBzaG91bGQgYmUgcmVwb3J0ZWQuCiAgICAgICAgICAgIGV4Y2VwdDoKICAgICAgICAgICAgICAgI
CMgc29tZSBoZWxwZnVsIGRlYnVnZ2luZwogICAgICAgICAgICAgICAgdHJ5OgogICAgICAgICAgIC
AgICAgICAgIHRiID0gdHJhY2ViYWNrLmZvcm1hdF9leGMoKS5lbmNvZGUoInV0ZjgiLCAiaWdub3J
lIikKICAgICAgICAgICAgICAgICAgICBvcy53cml0ZShleGNfcGlwZV93cml0ZSwgdGIpCgogICAg
ICAgICAgICAgICAgZmluYWxseToKICAgICAgICAgICAgICAgICAgICBvcy5fZXhpdCgyNTUpCgogI
CAgICAgICMgcGFyZW50CiAgICAgICAgZWxzZToKICAgICAgICAgICAgaWYgZ2NfZW5hYmxlZDoKIC
AgICAgICAgICAgICAgIGdjLmVuYWJsZSgpCgogICAgICAgICAgICBvcy5jbG9zZShzZWxmLl9zdGR
pbl93cml0ZV9mZCkKICAgICAgICAgICAgb3MuY2xvc2Uoc2VsZi5fc3Rkb3V0X3dyaXRlX2ZkKQog
ICAgICAgICAgICBvcy5jbG9zZShzZWxmLl9zdGRlcnJfd3JpdGVfZmQpCgogICAgICAgICAgICAjI
HRlbGwgb3VyIGNoaWxkIHByb2Nlc3MgdGhhdCB3ZSd2ZSBjbG9zZWQgb3VyIHdyaXRlX2Zkcywgc2
8gaXQgaXMKICAgICAgICAgICAgIyBvayB0byBwcm9jZWVkIHRvd2FyZHMgZXhlYy4gIHNlZSB0aGU
gY29tbWVudCB3aGVyZSB0aGlzIHBpcGUgaXMKICAgICAgICAgICAgIyBvcGVuZWQsIGZvciB3aHkg
dGhpcyBpcyBuZWNlc3NhcnkKICAgICAgICAgICAgaWYgSVNfT1NYOgogICAgICAgICAgICAgICAgb
3MuY2xvc2UoY2xvc2VfcGlwZV9yZWFkKQogICAgICAgICAgICAgICAgb3Mud3JpdGUoY2xvc2VfcG
lwZV93cml0ZSwgc3RyKDEpLmVuY29kZShERUZBVUxUX0VOQ09ESU5HKSkKICAgICAgICAgICAgICA
gIG9zLmNsb3NlKGNsb3NlX3BpcGVfd3JpdGUpCgogICAgICAgICAgICBvcy5jbG9zZShleGNfcGlw
ZV93cml0ZSkKICAgICAgICAgICAgZm9ya19leGMgPSBvcy5yZWFkKGV4Y19waXBlX3JlYWQsIDEwM
jQqKjIpCiAgICAgICAgICAgIG9zLmNsb3NlKGV4Y19waXBlX3JlYWQpCiAgICAgICAgICAgIGlmIG
ZvcmtfZXhjOgogICAgICAgICAgICAgICAgZm9ya19leGMgPSBmb3JrX2V4Yy5kZWNvZGUoREVGQVV
MVF9FTkNPRElORykKICAgICAgICAgICAgICAgIHJhaXNlIEZvcmtFeGNlcHRpb24oZm9ya19leGMp
CgogICAgICAgICAgICBvcy5jbG9zZShzZXNzaW9uX3BpcGVfd3JpdGUpCiAgICAgICAgICAgIHNpZ
CwgcGdpZCA9IG9zLnJlYWQoc2Vzc2lvbl9waXBlX3JlYWQsCiAgICAgICAgICAgICAgICAgICAgMT
AyNCkuZGVjb2RlKERFRkFVTFRfRU5DT0RJTkcpLnNwbGl0KCIsIikKICAgICAgICAgICAgb3MuY2x
vc2Uoc2Vzc2lvbl9waXBlX3JlYWQpCiAgICAgICAgICAgIHNlbGYuc2lkID0gaW50KHNpZCkKICAg
ICAgICAgICAgc2VsZi5wZ2lkID0gaW50KHBnaWQpCgogICAgICAgICAgICAjIHVzZWQgdG8gZGV0Z
XJtaW5lIHdoYXQgZXhjZXB0aW9uIHRvIHJhaXNlLiAgaWYgb3VyIHByb2Nlc3Mgd2FzCiAgICAgIC
AgICAgICMga2lsbGVkIHZpYSBhIHRpbWVvdXQgY291bnRlciwgd2UnbGwgcmFpc2Ugc29tZXRoaW5
nIGRpZmZlcmVudCB0aGFuCiAgICAgICAgICAgICMgYSBTSUdLSUxMIGV4Y2VwdGlvbgogICAgICAg
ICAgICBzZWxmLnRpbWVkX291dCA9IEZhbHNlCgogICAgICAgICAgICBzZWxmLnN0YXJ0ZWQgPSB0a
W1lLnRpbWUoKQogICAgICAgICAgICBzZWxmLmNtZCA9IGNtZAoKICAgICAgICAgICAgIyBleGl0IG
NvZGUgc2hvdWxkIG9ubHkgYmUgbWFuaXB1bGF0ZWQgZnJvbSB3aXRoaW4gc2VsZi5fd2FpdF9sb2N
rCiAgICAgICAgICAgICMgdG8gcHJldmVudCByYWNlIGNvbmRpdGlvbnMKICAgICAgICAgICAgc2Vs
Zi5leGl0X2NvZGUgPSBOb25lCgogICAgICAgICAgICBzZWxmLnN0ZGluID0gc3RkaW4gb3IgUXVld
WUoKQoKICAgICAgICAgICAgIyBfcGlwZV9xdWV1ZSBpcyB1c2VkIGludGVybmFsbHkgdG8gaGFuZC
BvZmYgc3Rkb3V0IGZyb20gb25lIHByb2Nlc3MKICAgICAgICAgICAgIyB0byBhbm90aGVyLiAgYnk
gZGVmYXVsdCwgYWxsIHN0ZG91dCBmcm9tIGEgcHJvY2VzcyBnZXRzIGR1bXBlZAogICAgICAgICAg
ICAjIGludG8gdGhpcyBwaXBlIHF1ZXVlLCB0byBiZSBjb25zdW1lZCBpbiByZWFsIHRpbWUgKGhlb
mNlIHRoZQogICAgICAgICAgICAjIHRocmVhZC1zYWZlIFF1ZXVlKSwgb3IgYXQgYSBwb3RlbnRpYW
xseSBsYXRlciB0aW1lCiAgICAgICAgICAgIHNlbGYuX3BpcGVfcXVldWUgPSBRdWV1ZSgpCgogICA
gICAgICAgICAjIHRoaXMgaXMgdXNlZCB0byBwcmV2ZW50IGEgcmFjZSBjb25kaXRpb24gd2hlbiB3
ZSdyZSB3YWl0aW5nIGZvcgogICAgICAgICAgICAjIGEgcHJvY2VzcyB0byBlbmQsIGFuZCB0aGUgT
1Byb2MncyBpbnRlcm5hbCB0aHJlYWRzIGFyZSBhbHNvIGNoZWNraW5nCiAgICAgICAgICAgICMgZm
9yIHRoZSBwcm9jZXNzZXMncyBlbmQKICAgICAgICAgICAgc2VsZi5fd2FpdF9sb2NrID0gdGhyZWF
kaW5nLkxvY2soKQoKICAgICAgICAgICAgIyB0aGVzZSBhcmUgZm9yIGFnZ3JlZ2F0aW5nIHRoZSBz
dGRvdXQgYW5kIHN0ZGVyci4gIHdlIHVzZSBhIGRlcXVlCiAgICAgICAgICAgICMgYmVjYXVzZSB3Z
SBkb24ndCB3YW50IHRvIG92ZXJmbG93CiAgICAgICAgICAgIHNlbGYuX3N0ZG91dCA9IGRlcXVlKG
1heGxlbj1jYVsiaW50ZXJuYWxfYnVmc2l6ZSJdKQogICAgICAgICAgICBzZWxmLl9zdGRlcnIgPSB
kZXF1ZShtYXhsZW49Y2FbImludGVybmFsX2J1ZnNpemUiXSkKCiAgICAgICAgICAgIGlmIGNhWyJ0
dHlfaW4iXSBhbmQgbm90IHN0ZGluX2lzX3R0eV9vcl9waXBlOgogICAgICAgICAgICAgICAgc2V0d
2luc2l6ZShzZWxmLl9zdGRpbl9yZWFkX2ZkLCBjYVsidHR5X3NpemUiXSkKCgogICAgICAgICAgIC
BzZWxmLmxvZyA9IHBhcmVudF9sb2cuZ2V0X2NoaWxkKCJwcm9jZXNzIiwgcmVwcihzZWxmKSkKCgo
gICAgICAgICAgICBzZWxmLmxvZy5kZWJ1Zygic3RhcnRlZCBwcm9jZXNzIikKCiAgICAgICAgICAg
ICMgZGlzYWJsZSBlY2hvaW5nLCBidXQgb25seSBpZiBpdCdzIGEgdHR5IHRoYXQgd2UgY3JlYXRlZ
CBvdXJzZWx2ZXMKICAgICAgICAgICAgaWYgY2FbInR0eV9pbiJdIGFuZCBub3Qgc3RkaW5faXNfdH
R5X29yX3BpcGU6CiAgICAgICAgICAgICAgICBhdHRyID0gdGVybWlvcy50Y2dldGF0dHIoc2VsZi5
fc3RkaW5fcmVhZF9mZCkKICAgICAgICAgICAgICAgIGF0dHJbM10gJj0gfnRlcm1pb3MuRUNITwog
ICAgICAgICAgICAgICAgdGVybWlvcy50Y3NldGF0dHIoc2VsZi5fc3RkaW5fcmVhZF9mZCwgdGVyb
Wlvcy5UQ1NBTk9XLCBhdHRyKQoKICAgICAgICAgICAgIyB3ZSdyZSBvbmx5IGdvaW5nIHRvIGNyZW
F0ZSBhIHN0ZGluIHRocmVhZCBpZmYgd2UgaGF2ZSBwb3RlbnRpYWwKICAgICAgICAgICAgIyBmb3I
gc3RkaW4gdG8gY29tZSBpbi4gIHRoaXMgd291bGQgYmUgdGhyb3VnaCBhIHN0ZG91dCBjYWxsYmFj
ayBvcgogICAgICAgICAgICAjIHRocm91Z2ggYW4gb2JqZWN0IHdlJ3ZlIHBhc3NlZCBpbiBmb3Igc
3RkaW4KICAgICAgICAgICAgcG90ZW50aWFsbHlfaGFzX2lucHV0ID0gY2FsbGFibGUoc3Rkb3V0KS
BvciBzdGRpbgoKICAgICAgICAgICAgIyB0aGlzIHJlcHJlc2VudHMgdGhlIGNvbm5lY3Rpb24gZnJ
vbSBhIFF1ZXVlIG9iamVjdCAob3Igd2hhdGV2ZXIKICAgICAgICAgICAgIyB3ZSdyZSB1c2luZyB0
byBmZWVkIFNURElOKSB0byB0aGUgcHJvY2VzcydzIFNURElOIGZkCiAgICAgICAgICAgIHNlbGYuX
3N0ZGluX3N0cmVhbSA9IE5vbmUKICAgICAgICAgICAgaWYgc2VsZi5fc3RkaW5fcmVhZF9mZCBhbm
QgcG90ZW50aWFsbHlfaGFzX2lucHV0OgogICAgICAgICAgICAgICAgbG9nID0gc2VsZi5sb2cuZ2V
0X2NoaWxkKCJzdHJlYW13cml0ZXIiLCAic3RkaW4iKQogICAgICAgICAgICAgICAgc2VsZi5fc3Rk
aW5fc3RyZWFtID0gIFN0cmVhbVdyaXRlcihsb2csIHNlbGYuX3N0ZGluX3JlYWRfZmQsCiAgICAgI
CAgICAgICAgICAgICAgICAgIHNlbGYuc3RkaW4sIGNhWyJpbl9idWZzaXplIl0sIGNhWyJlbmNvZG
luZyJdLAogICAgICAgICAgICAgICAgICAgICAgICBjYVsidHR5X2luIl0pCgogICAgICAgICAgICB
zdGRvdXRfcGlwZSA9IE5vbmUKICAgICAgICAgICAgaWYgcGlwZSBpcyBPUHJvYy5TVERPVVQgYW5k
IG5vdCBjYVsibm9fcGlwZSJdOgogICAgICAgICAgICAgICAgc3Rkb3V0X3BpcGUgPSBzZWxmLl9wa
XBlX3F1ZXVlCgoKICAgICAgICAgICAgIyB0aGlzIHJlcHJlc2VudHMgdGhlIGNvbm5lY3Rpb24gZn
JvbSBhIHByb2Nlc3MncyBTVERPVVQgZmQgdG8KICAgICAgICAgICAgIyB3aGVyZXZlciBpdCBoYXM
gdG8gZ28sIHNvbWV0aW1lcyBhIHBpcGUgUXVldWUgKHRoYXQgd2Ugd2lsbCB1c2UKICAgICAgICAg
ICAgIyB0byBwaXBlIGRhdGEgdG8gb3RoZXIgcHJvY2Vzc2VzKSwgYW5kIGFsc28gYW4gaW50ZXJuY
WwgZGVxdWUKICAgICAgICAgICAgIyB0aGF0IHdlIHVzZSB0byBhZ2dyZWdhdGUgYWxsIHRoZSBvdX
RwdXQKICAgICAgICAgICAgc2F2ZV9zdGRvdXQgPSBub3QgY2FbIm5vX291dCJdIGFuZCBcCiAgICA
gICAgICAgICAgICAodGVlX291dCBvciBzdGRvdXQgaXMgTm9uZSkKCgogICAgICAgICAgICBwaXBl
X291dCA9IGNhWyJwaXBlZCJdIGluICgib3V0IiwgVHJ1ZSkKICAgICAgICAgICAgcGlwZV9lcnIgP
SBjYVsicGlwZWQiXSBpbiAoImVyciIsKQoKICAgICAgICAgICAgIyBpZiB3ZSdyZSBwaXBpbmcgZG
lyZWN0bHkgaW50byBhbm90aGVyIHByb2Nlc3MncyBmaWxlZGVzY3JpcHRvciwgd2UKICAgICAgICA
gICAgIyBieXBhc3MgcmVhZGluZyBmcm9tIHRoZSBzdGRvdXQgc3RyZWFtIGFsdG9nZXRoZXIsIGJl
Y2F1c2Ugd2UndmUKICAgICAgICAgICAgIyBhbHJlYWR5IGhvb2tlZCB1cCB0aGlzIHByb2Nlc3Nlc
ydzIHN0ZG91dCBmZCB0byB0aGUgb3RoZXIKICAgICAgICAgICAgIyBwcm9jZXNzZXMncyBzdGRpbi
BmZAogICAgICAgICAgICBzZWxmLl9zdGRvdXRfc3RyZWFtID0gTm9uZQogICAgICAgICAgICBpZiB
ub3QgcGlwZV9vdXQgYW5kIHNlbGYuX3N0ZG91dF9yZWFkX2ZkOgogICAgICAgICAgICAgICAgaWYg
Y2FsbGFibGUoc3Rkb3V0KToKICAgICAgICAgICAgICAgICAgICBzdGRvdXQgPSBjb25zdHJ1Y3Rfc
3RyZWFtcmVhZGVyX2NhbGxiYWNrKHNlbGYsIHN0ZG91dCkKICAgICAgICAgICAgICAgIHNlbGYuX3
N0ZG91dF9zdHJlYW0gPSBcCiAgICAgICAgICAgICAgICAgICAgICAgIFN0cmVhbVJlYWRlcigKICA
gICAgICAgICAgICAgICAgICAgICAgICAgICAgICBzZWxmLmxvZy5nZXRfY2hpbGQoInN0cmVhbXJl
YWRlciIsICJzdGRvdXQiKSwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBzZWxmLl9zd
GRvdXRfcmVhZF9mZCwgc3Rkb3V0LCBzZWxmLl9zdGRvdXQsCiAgICAgICAgICAgICAgICAgICAgIC
AgICAgICAgICAgY2FbIm91dF9idWZzaXplIl0sIGNhWyJlbmNvZGluZyJdLAogICAgICAgICAgICA
gICAgICAgICAgICAgICAgICAgIGNhWyJkZWNvZGVfZXJyb3JzIl0sIHN0ZG91dF9waXBlLAogICAg
ICAgICAgICAgICAgICAgICAgICAgICAgICAgIHNhdmVfZGF0YT1zYXZlX3N0ZG91dCkKCiAgICAgI
CAgICAgIGVsaWYgc2VsZi5fc3Rkb3V0X3JlYWRfZmQ6CiAgICAgICAgICAgICAgICBvcy5jbG9zZS
hzZWxmLl9zdGRvdXRfcmVhZF9mZCkKCgogICAgICAgICAgICAjIGlmIHN0ZGVyciBpcyBnb2luZyB
0byBvbmUgcGxhY2UgKGJlY2F1c2UgaXQncyBncm91cGVkIHdpdGggc3Rkb3V0LAogICAgICAgICAg
ICAjIG9yIHdlJ3JlIGRlYWxpbmcgd2l0aCBhIHNpbmdsZSB0dHkpLCB0aGVuIHdlIGRvbid0IGFjd
HVhbGx5IG5lZWQgYQogICAgICAgICAgICAjIHN0cmVhbSByZWFkZXIgZm9yIHN0ZGVyciwgYmVjYX
VzZSB3ZSd2ZSBhbHJlYWR5IHNldCBvbmUgdXAgZm9yCiAgICAgICAgICAgICMgc3Rkb3V0IGFib3Z
lCiAgICAgICAgICAgIHNlbGYuX3N0ZGVycl9zdHJlYW0gPSBOb25lCiAgICAgICAgICAgIGlmIHN0
ZGVyciBpcyBub3QgT1Byb2MuU1RET1VUIGFuZCBub3Qgc2luZ2xlX3R0eSBhbmQgbm90IHBpcGVfZ
XJyIFwKICAgICAgICAgICAgICAgICAgICBhbmQgc2VsZi5fc3RkZXJyX3JlYWRfZmQ6CgogICAgIC
AgICAgICAgICAgc3RkZXJyX3BpcGUgPSBOb25lCiAgICAgICAgICAgICAgICBpZiBwaXBlIGlzIE9
Qcm9jLlNUREVSUiBhbmQgbm90IGNhWyJub19waXBlIl06CiAgICAgICAgICAgICAgICAgICAgc3Rk
ZXJyX3BpcGUgPSBzZWxmLl9waXBlX3F1ZXVlCgogICAgICAgICAgICAgICAgc2F2ZV9zdGRlcnIgP
SBub3QgY2FbIm5vX2VyciJdIGFuZCBcCiAgICAgICAgICAgICAgICAgICAgKGNhWyJ0ZWUiXSBpbi
AoImVyciIsKSBvciBzdGRlcnIgaXMgTm9uZSkKCiAgICAgICAgICAgICAgICBpZiBjYWxsYWJsZSh
zdGRlcnIpOgogICAgICAgICAgICAgICAgICAgIHN0ZGVyciA9IGNvbnN0cnVjdF9zdHJlYW1yZWFk
ZXJfY2FsbGJhY2soc2VsZiwgc3RkZXJyKQoKICAgICAgICAgICAgICAgIHNlbGYuX3N0ZGVycl9zd
HJlYW0gPSBTdHJlYW1SZWFkZXIoTG9nZ2VyKCJzdHJlYW1yZWFkZXIiKSwKICAgICAgICAgICAgIC
AgICAgICAgICAgc2VsZi5fc3RkZXJyX3JlYWRfZmQsIHN0ZGVyciwgc2VsZi5fc3RkZXJyLAogICA
gICAgICAgICAgICAgICAgICAgICBjYVsiZXJyX2J1ZnNpemUiXSwgY2FbImVuY29kaW5nIl0sIGNh
WyJkZWNvZGVfZXJyb3JzIl0sCiAgICAgICAgICAgICAgICAgICAgICAgIHN0ZGVycl9waXBlLCBzY
XZlX2RhdGE9c2F2ZV9zdGRlcnIpCgogICAgICAgICAgICBlbGlmIHNlbGYuX3N0ZGVycl9yZWFkX2
ZkOgogICAgICAgICAgICAgICAgb3MuY2xvc2Uoc2VsZi5fc3RkZXJyX3JlYWRfZmQpCgoKICAgICA
gICAgICAgZGVmIHRpbWVvdXRfZm4oKToKICAgICAgICAgICAgICAgIHNlbGYudGltZWRfb3V0ID0g
VHJ1ZQogICAgICAgICAgICAgICAgc2VsZi5zaWduYWwoY2FbInRpbWVvdXRfc2lnbmFsIl0pCgoKI
CAgICAgICAgICAgc2VsZi5fdGltZW91dF9ldmVudCA9IE5vbmUKICAgICAgICAgICAgc2VsZi5fdG
ltZW91dF90aW1lciA9IE5vbmUKICAgICAgICAgICAgaWYgY2FbInRpbWVvdXQiXToKICAgICAgICA
gICAgICAgIHNlbGYuX3RpbWVvdXRfZXZlbnQgPSB0aHJlYWRpbmcuRXZlbnQoKQogICAgICAgICAg
ICAgICAgc2VsZi5fdGltZW91dF90aW1lciA9IHRocmVhZGluZy5UaW1lcihjYVsidGltZW91dCJdL
AogICAgICAgICAgICAgICAgICAgICAgICBzZWxmLl90aW1lb3V0X2V2ZW50LnNldCkKICAgICAgIC
AgICAgICAgIHNlbGYuX3RpbWVvdXRfdGltZXIuc3RhcnQoKQoKICAgICAgICAgICAgIyB0aGlzIGl
zIGZvciBjYXNlcyB3aGVyZSB3ZSBrbm93IHRoYXQgdGhlIFJ1bm5pbmdDb21tYW5kIHRoYXQgd2Fz
CiAgICAgICAgICAgICMgbGF1bmNoZWQgd2FzIG5vdCAud2FpdCgpZWQgb24gdG8gY29tcGxldGUuI
CBpbiB0aG9zZSB1bmlxdWUgY2FzZXMsCiAgICAgICAgICAgICMgd2UgYWxsb3cgdGhlIHRocmVhZC
B0aGF0IHByb2Nlc3NlcyBvdXRwdXQgdG8gcmVwb3J0IGV4Y2VwdGlvbnMgaW4KICAgICAgICAgICA
gIyB0aGF0IHRocmVhZC4gIGl0J3MgaW1wb3J0YW50IHRoYXQgd2Ugb25seSBhbGxvdyByZXBvcnRp
bmcgb2YgdGhlCiAgICAgICAgICAgICMgZXhjZXB0aW9uLCBhbmQgbm90aGluZyBlbHNlIChsaWtlI
HRoZSBhZGRpdGlvbmFsIHN0dWZmIHRoYXQKICAgICAgICAgICAgIyBSdW5uaW5nQ29tbWFuZC53YW
l0KCkgZG9lcyksIGJlY2F1c2Ugd2Ugd2FudCB0aGUgZXhjZXB0aW9uIHRvIGJlCiAgICAgICAgICA
gICMgcmUtcmFpc2VkIGluIHRoZSBmdXR1cmUsIGlmIHdlIERPIGNhbGwgLndhaXQoKQogICAgICAg
ICAgICBoYW5kbGVfZXhpdF9jb2RlID0gTm9uZQogICAgICAgICAgICBpZiBub3Qgc2VsZi5jb21tY
W5kLl9zcGF3bmVkX2FuZF93YWl0ZWQgYW5kIGNhWyJiZ19leGMiXToKICAgICAgICAgICAgICAgIG
RlZiBmbihleGl0X2NvZGUpOgogICAgICAgICAgICAgICAgICAgIHdpdGggcHJvY2Vzc19hc3NpZ25
fbG9jazoKICAgICAgICAgICAgICAgICAgICAgICAgcmV0dXJuIHNlbGYuY29tbWFuZC5oYW5kbGVf
Y29tbWFuZF9leGl0X2NvZGUoZXhpdF9jb2RlKQogICAgICAgICAgICAgICAgaGFuZGxlX2V4aXRfY
29kZSA9IGZuCgogICAgICAgICAgICBzZWxmLl9xdWl0X3RocmVhZHMgPSB0aHJlYWRpbmcuRXZlbn
QoKQoKICAgICAgICAgICAgdGhyZWFkX25hbWUgPSAiYmFja2dyb3VuZCB0aHJlYWQgZm9yIHBpZCA
lZCIgJSBzZWxmLnBpZAogICAgICAgICAgICBzZWxmLl9iZ190aHJlYWRfZXhjX3F1ZXVlID0gUXVl
dWUoMSkKICAgICAgICAgICAgc2VsZi5fYmFja2dyb3VuZF90aHJlYWQgPSBfc3RhcnRfZGFlbW9uX
3RocmVhZChiYWNrZ3JvdW5kX3RocmVhZCwKICAgICAgICAgICAgICAgICAgICB0aHJlYWRfbmFtZS
wgc2VsZi5fYmdfdGhyZWFkX2V4Y19xdWV1ZSwgdGltZW91dF9mbiwKICAgICAgICAgICAgICAgICA
gICBzZWxmLl90aW1lb3V0X2V2ZW50LCBoYW5kbGVfZXhpdF9jb2RlLCBzZWxmLmlzX2FsaXZlLAog
ICAgICAgICAgICAgICAgICAgIHNlbGYuX3F1aXRfdGhyZWFkcykKCgogICAgICAgICAgICAjIHN0Y
XJ0IHRoZSBtYWluIGlvIHRocmVhZHMuIHN0ZGluIHRocmVhZCBpcyBub3QgbmVlZGVkIGlmIHdlIG
FyZQogICAgICAgICAgICAjIGNvbm5lY3RpbmcgZnJvbSBhbm90aGVyIHByb2Nlc3MncyBzdGRvdXQ
gcGlwZQogICAgICAgICAgICBzZWxmLl9pbnB1dF90aHJlYWQgPSBOb25lCiAgICAgICAgICAgIHNl
bGYuX2lucHV0X3RocmVhZF9leGNfcXVldWUgPSBRdWV1ZSgxKQogICAgICAgICAgICBpZiBzZWxmL
l9zdGRpbl9zdHJlYW06CiAgICAgICAgICAgICAgICBjbG9zZV9iZWZvcmVfdGVybSA9IG5vdCBuZW
Vkc19jdHR5CiAgICAgICAgICAgICAgICB0aHJlYWRfbmFtZSA9ICJTVERJTiB0aHJlYWQgZm9yIHB
pZCAlZCIgJSBzZWxmLnBpZAogICAgICAgICAgICAgICAgc2VsZi5faW5wdXRfdGhyZWFkID0gX3N0
YXJ0X2RhZW1vbl90aHJlYWQoaW5wdXRfdGhyZWFkLAogICAgICAgICAgICAgICAgICAgICAgICB0a
HJlYWRfbmFtZSwgc2VsZi5faW5wdXRfdGhyZWFkX2V4Y19xdWV1ZSwgc2VsZi5sb2csCiAgICAgIC
AgICAgICAgICAgICAgICAgIHNlbGYuX3N0ZGluX3N0cmVhbSwgc2VsZi5pc19hbGl2ZSwgc2VsZi5
fcXVpdF90aHJlYWRzLAogICAgICAgICAgICAgICAgICAgICAgICBjbG9zZV9iZWZvcmVfdGVybSkK
CgogICAgICAgICAgICAjIHRoaXMgZXZlbnQgaXMgZm9yIGNhc2VzIHdoZXJlIHRoZSBzdWJwcm9jZ
XNzIHRoYXQgd2UgbGF1bmNoCiAgICAgICAgICAgICMgbGF1bmNoZXMgaXRzIE9XTiBzdWJwcm9jZX
NzIGFuZCBkdXBzIHRoZSBzdGRvdXQvc3RkZXJyIGZkcyB0byB0aGF0CiAgICAgICAgICAgICMgbmV
3IHN1YnByb2Nlc3MuICBpbiB0aGF0IGNhc2UsIHN0ZG91dCBhbmQgc3RkZXJyIHdpbGwgbmV2ZXIg
RU9GLAogICAgICAgICAgICAjIHNvIG91ciBvdXRwdXRfdGhyZWFkIHdpbGwgbmV2ZXIgZmluaXNoI
GFuZCB3aWxsIGhhbmcuICB0aGlzIGV2ZW50CiAgICAgICAgICAgICMgcHJldmVudHMgdGhhdCBoYW
5naW5nCiAgICAgICAgICAgIHNlbGYuX3N0b3Bfb3V0cHV0X2V2ZW50ID0gdGhyZWFkaW5nLkV2ZW5
0KCkKCiAgICAgICAgICAgIHNlbGYuX291dHB1dF90aHJlYWRfZXhjX3F1ZXVlID0gUXVldWUoMSkK
ICAgICAgICAgICAgdGhyZWFkX25hbWUgPSAiU1RET1VUL0VSUiB0aHJlYWQgZm9yIHBpZCAlZCIgJ
SBzZWxmLnBpZAogICAgICAgICAgICBzZWxmLl9vdXRwdXRfdGhyZWFkID0gX3N0YXJ0X2RhZW1vbl
90aHJlYWQob3V0cHV0X3RocmVhZCwKICAgICAgICAgICAgICAgICAgICB0aHJlYWRfbmFtZSwgc2V
sZi5fb3V0cHV0X3RocmVhZF9leGNfcXVldWUsIHNlbGYubG9nLAogICAgICAgICAgICAgICAgICAg
IHNlbGYuX3N0ZG91dF9zdHJlYW0sIHNlbGYuX3N0ZGVycl9zdHJlYW0sCiAgICAgICAgICAgICAgI
CAgICAgc2VsZi5fdGltZW91dF9ldmVudCwgc2VsZi5pc19hbGl2ZSwgc2VsZi5fcXVpdF90aHJlYW
RzLAogICAgICAgICAgICAgICAgICAgIHNlbGYuX3N0b3Bfb3V0cHV0X2V2ZW50KQoKCiAgICBkZWY
gX19yZXByX18oc2VsZik6CiAgICAgICAgcmV0dXJuICI8UHJvY2VzcyAlZCAlcj4iICUgKHNlbGYu
cGlkLCBzZWxmLmNtZFs6NTAwXSkKCgogICAgIyB0aGVzZSBuZXh0IDMgcHJvcGVydGllcyBhcmUgc
HJpbWFyeSBmb3IgdGVzdHMKICAgIEBwcm9wZXJ0eQogICAgZGVmIG91dHB1dF90aHJlYWRfZXhjKH
NlbGYpOgogICAgICAgIGV4YyA9IE5vbmUKICAgICAgICB0cnk6CiAgICAgICAgICAgIGV4YyA9IHN
lbGYuX291dHB1dF90aHJlYWRfZXhjX3F1ZXVlLmdldChGYWxzZSkKICAgICAgICBleGNlcHQgRW1w
dHk6CiAgICAgICAgICAgIHBhc3MKICAgICAgICByZXR1cm4gZXhjCgogICAgQHByb3BlcnR5CiAgI
CBkZWYgaW5wdXRfdGhyZWFkX2V4YyhzZWxmKToKICAgICAgICBleGMgPSBOb25lCiAgICAgICAgdH
J5OgogICAgICAgICAgICBleGMgPSBzZWxmLl9pbnB1dF90aHJlYWRfZXhjX3F1ZXVlLmdldChGYWx
zZSkKICAgICAgICBleGNlcHQgRW1wdHk6CiAgICAgICAgICAgIHBhc3MKICAgICAgICByZXR1cm4g
ZXhjCgogICAgQHByb3BlcnR5CiAgICBkZWYgYmdfdGhyZWFkX2V4YyhzZWxmKToKICAgICAgICBle
GMgPSBOb25lCiAgICAgICAgdHJ5OgogICAgICAgICAgICBleGMgPSBzZWxmLl9iZ190aHJlYWRfZX
hjX3F1ZXVlLmdldChGYWxzZSkKICAgICAgICBleGNlcHQgRW1wdHk6CiAgICAgICAgICAgIHBhc3M
KICAgICAgICByZXR1cm4gZXhjCgoKICAgIGRlZiBjaGFuZ2VfaW5fYnVmc2l6ZShzZWxmLCBidWYp
OgogICAgICAgIHNlbGYuX3N0ZGluX3N0cmVhbS5zdHJlYW1fYnVmZmVyZXIuY2hhbmdlX2J1ZmZlc
mluZyhidWYpCgogICAgZGVmIGNoYW5nZV9vdXRfYnVmc2l6ZShzZWxmLCBidWYpOgogICAgICAgIH
NlbGYuX3N0ZG91dF9zdHJlYW0uc3RyZWFtX2J1ZmZlcmVyLmNoYW5nZV9idWZmZXJpbmcoYnVmKQo
KICAgIGRlZiBjaGFuZ2VfZXJyX2J1ZnNpemUoc2VsZiwgYnVmKToKICAgICAgICBzZWxmLl9zdGRl
cnJfc3RyZWFtLnN0cmVhbV9idWZmZXJlci5jaGFuZ2VfYnVmZmVyaW5nKGJ1ZikKCgoKICAgIEBwc
m9wZXJ0eQogICAgZGVmIHN0ZG91dChzZWxmKToKICAgICAgICByZXR1cm4gIiIuZW5jb2RlKHNlbG
YuY2FsbF9hcmdzWyJlbmNvZGluZyJdKS5qb2luKHNlbGYuX3N0ZG91dCkKCiAgICBAcHJvcGVydHk
KICAgIGRlZiBzdGRlcnIoc2VsZik6CiAgICAgICAgcmV0dXJuICIiLmVuY29kZShzZWxmLmNhbGxf
YXJnc1siZW5jb2RpbmciXSkuam9pbihzZWxmLl9zdGRlcnIpCgogICAgZGVmIGdldF9wZ2lkKHNlb
GYpOgogICAgICAgICIiIiByZXR1cm4gdGhlIENVUlJFTlQgZ3JvdXAgaWQgb2YgdGhlIHByb2Nlc3
MuIHRoaXMgZGlmZmVycyBmcm9tCiAgICAgICAgc2VsZi5wZ2lkIGluIHRoYXQgdGhpcyByZWZlY3R
zIHRoZSBjdXJyZW50IHN0YXRlIG9mIHRoZSBwcm9jZXNzLCB3aGVyZQogICAgICAgIHNlbGYucGdp
ZCBpcyB0aGUgZ3JvdXAgaWQgYXQgbGF1bmNoICIiIgogICAgICAgIHJldHVybiBvcy5nZXRwZ2lkK
HNlbGYucGlkKQoKICAgIGRlZiBnZXRfc2lkKHNlbGYpOgogICAgICAgICIiIiByZXR1cm4gdGhlIE
NVUlJFTlQgc2Vzc2lvbiBpZCBvZiB0aGUgcHJvY2Vzcy4gdGhpcyBkaWZmZXJzIGZyb20KICAgICA
gICBzZWxmLnNpZCBpbiB0aGF0IHRoaXMgcmVmZWN0cyB0aGUgY3VycmVudCBzdGF0ZSBvZiB0aGUg
cHJvY2Vzcywgd2hlcmUKICAgICAgICBzZWxmLnNpZCBpcyB0aGUgc2Vzc2lvbiBpZCBhdCBsYXVuY
2ggIiIiCiAgICAgICAgcmV0dXJuIG9zLmdldHNpZChzZWxmLnBpZCkKCiAgICBkZWYgc2lnbmFsX2
dyb3VwKHNlbGYsIHNpZyk6CiAgICAgICAgc2VsZi5sb2cuZGVidWcoInNlbmRpbmcgc2lnbmFsICV
kIHRvIGdyb3VwIiwgc2lnKQogICAgICAgIG9zLmtpbGxwZyhzZWxmLmdldF9wZ2lkKCksIHNpZykK
CiAgICBkZWYgc2lnbmFsKHNlbGYsIHNpZyk6CiAgICAgICAgc2VsZi5sb2cuZGVidWcoInNlbmRpb
mcgc2lnbmFsICVkIiwgc2lnKQogICAgICAgIG9zLmtpbGwoc2VsZi5waWQsIHNpZykKCiAgICBkZW
Yga2lsbF9ncm91cChzZWxmKToKICAgICAgICBzZWxmLmxvZy5kZWJ1Zygia2lsbGluZyBncm91cCI
pCiAgICAgICAgc2VsZi5zaWduYWxfZ3JvdXAoc2lnbmFsLlNJR0tJTEwpCgogICAgZGVmIGtpbGwo
c2VsZik6CiAgICAgICAgc2VsZi5sb2cuZGVidWcoImtpbGxpbmciKQogICAgICAgIHNlbGYuc2lnb
mFsKHNpZ25hbC5TSUdLSUxMKQoKICAgIGRlZiB0ZXJtaW5hdGUoc2VsZik6CiAgICAgICAgc2VsZi
5sb2cuZGVidWcoInRlcm1pbmF0aW5nIikKICAgICAgICBzZWxmLnNpZ25hbChzaWduYWwuU0lHVEV
STSkKCgogICAgZGVmIGlzX2FsaXZlKHNlbGYpOgogICAgICAgICIiIiBwb2xscyBpZiBvdXIgY2hp
bGQgcHJvY2VzcyBoYXMgY29tcGxldGVkLCB3aXRob3V0IGJsb2NraW5nLiAgdGhpcwogICAgICAgI
G1ldGhvZCBoYXMgc2lkZS1lZmZlY3RzLCBzdWNoIGFzIHNldHRpbmcgb3VyIGV4aXRfY29kZSwgaW
Ygd2UgaGFwcGVuIHRvCiAgICAgICAgc2VlIG91ciBjaGlsZCBleGl0IHdoaWxlIHRoaXMgaXMgcnV
ubmluZyAiIiIKCiAgICAgICAgaWYgc2VsZi5leGl0X2NvZGUgaXMgbm90IE5vbmU6CiAgICAgICAg
ICAgIHJldHVybiBGYWxzZSwgc2VsZi5leGl0X2NvZGUKCiAgICAgICAgIyB3aGF0IHdlJ3JlIGRva
W5nIGhlcmUgZXNzZW50aWFsbHkgaXMgbWFraW5nIHN1cmUgdGhhdCB0aGUgbWFpbiB0aHJlYWQKIC
AgICAgICAjIChvciBhbm90aGVyIHRocmVhZCksIGlzbid0IGNhbGxpbmcgLndhaXQoKSBvbiB0aGU
gcHJvY2Vzcy4gIGJlY2F1c2UKICAgICAgICAjIC53YWl0KCkgY2FsbHMgb3Mud2FpdHBpZChzZWxm
LnBpZCwgMCksIHdlIGNhbid0IGRvIGFuIG9zLndhaXRwaWQKICAgICAgICAjIGhlcmUuLi5iZWNhd
XNlIGlmIHdlIGRpZCwgYW5kIHRoZSBwcm9jZXNzIGV4aXRlZCB3aGlsZSBpbiB0aGlzCiAgICAgIC
AgIyB0aHJlYWQsIHRoZSBtYWluIHRocmVhZCdzIG9zLndhaXRwaWQoc2VsZi5waWQsIDApIHdvdWx
kIHJhaXNlIE9TRXJyb3IKICAgICAgICAjIChiZWNhdXNlIHRoZSBwcm9jZXNzIGVuZGVkIGluIGFu
b3RoZXIgdGhyZWFkKS4KICAgICAgICAjCiAgICAgICAgIyBzbyBlc3NlbnRpYWxseSB3aGF0IHdlJ
3JlIGRvaW5nIGlzLCB1c2luZyB0aGlzIGxvY2ssIGNoZWNraW5nIGlmCiAgICAgICAgIyB3ZSdyZS
BjYWxsaW5nIC53YWl0KCksIGFuZCBpZiB3ZSBhcmUsIGxldCAud2FpdCgpIGdldCB0aGUgZXhpdCB
jb2RlCiAgICAgICAgIyBhbmQgaGFuZGxlIHRoZSBzdGF0dXMsIG90aGVyd2lzZSBsZXQgdXMgZG8g
aXQuCiAgICAgICAgYWNxdWlyZWQgPSBzZWxmLl93YWl0X2xvY2suYWNxdWlyZShGYWxzZSkKICAgI
CAgICBpZiBub3QgYWNxdWlyZWQ6CiAgICAgICAgICAgIGlmIHNlbGYuZXhpdF9jb2RlIGlzIG5vdC
BOb25lOgogICAgICAgICAgICAgICAgcmV0dXJuIEZhbHNlLCBzZWxmLmV4aXRfY29kZQogICAgICA
gICAgICByZXR1cm4gVHJ1ZSwgc2VsZi5leGl0X2NvZGUKCiAgICAgICAgdHJ5OgogICAgICAgICAg
ICAjIFdOT0hBTkcgaXMganVzdCB0aGF0Li4ud2UncmUgY2FsbGluZyB3YWl0cGlkIHdpdGhvdXQga
GFuZ2luZy4uLgogICAgICAgICAgICAjIGVzc2VudGlhbGx5IHBvbGxpbmcgdGhlIHByb2Nlc3MuIC
B0aGUgcmV0dXJuIHJlc3VsdCBpcyAoMCwgMCkgaWYKICAgICAgICAgICAgIyB0aGVyZSdzIG5vIHB
yb2Nlc3Mgc3RhdHVzLCBzbyB3ZSBjaGVjayB0aGF0IHBpZCA9PSBzZWxmLnBpZCBiZWxvdwogICAg
ICAgICAgICAjIGluIG9yZGVyIHRvIGRldGVybWluZSBob3cgdG8gcHJvY2VlZAogICAgICAgICAgI
CBwaWQsIGV4aXRfY29kZSA9IG5vX2ludGVycnVwdChvcy53YWl0cGlkLCBzZWxmLnBpZCwgb3MuV0
5PSEFORykKICAgICAgICAgICAgaWYgcGlkID09IHNlbGYucGlkOgogICAgICAgICAgICAgICAgc2V
sZi5leGl0X2NvZGUgPSBoYW5kbGVfcHJvY2Vzc19leGl0X2NvZGUoZXhpdF9jb2RlKQogICAgICAg
ICAgICAgICAgc2VsZi5fcHJvY2Vzc19qdXN0X2VuZGVkKCkKCiAgICAgICAgICAgICAgICByZXR1c
m4gRmFsc2UsIHNlbGYuZXhpdF9jb2RlCgogICAgICAgICMgbm8gY2hpbGQgcHJvY2VzcwogICAgIC
AgIGV4Y2VwdCBPU0Vycm9yOgogICAgICAgICAgICByZXR1cm4gRmFsc2UsIHNlbGYuZXhpdF9jb2R
lCiAgICAgICAgZWxzZToKICAgICAgICAgICAgcmV0dXJuIFRydWUsIHNlbGYuZXhpdF9jb2RlCiAg
ICAgICAgZmluYWxseToKICAgICAgICAgICAgc2VsZi5fd2FpdF9sb2NrLnJlbGVhc2UoKQoKCiAgI
CBkZWYgX3Byb2Nlc3NfanVzdF9lbmRlZChzZWxmKToKICAgICAgICBpZiBzZWxmLl90aW1lb3V0X3
RpbWVyOgogICAgICAgICAgICBzZWxmLl90aW1lb3V0X3RpbWVyLmNhbmNlbCgpCgogICAgICAgIGR
vbmVfY2FsbGJhY2sgPSBzZWxmLmNhbGxfYXJnc1siZG9uZSJdCiAgICAgICAgaWYgZG9uZV9jYWxs
YmFjazoKICAgICAgICAgICAgc3VjY2VzcyA9IHNlbGYuZXhpdF9jb2RlIGluIHNlbGYuY2FsbF9hc
mdzWyJva19jb2RlIl0KICAgICAgICAgICAgZG9uZV9jYWxsYmFjayhzdWNjZXNzLCBzZWxmLmV4aX
RfY29kZSkKCiAgICAgICAgIyB0aGlzIGNhbiBvbmx5IGJlIGNsb3NlZCBhdCB0aGUgZW5kIG9mIHR
oZSBwcm9jZXNzLCBiZWNhdXNlIGl0IG1pZ2h0IGJlCiAgICAgICAgIyB0aGUgQ1RUWSwgYW5kIGNs
b3NpbmcgaXQgcHJlbWF0dXJlbHkgd2lsbCBzZW5kIGEgU0lHSFVQLiAgd2UgYWxzbwogICAgICAgI
CMgZG9uJ3Qgd2FudCB0byBjbG9zZSBpdCBpZiB0aGVyZSdzIGEgc2VsZi5fc3RkaW5fc3RyZWFtLC
BiZWNhdXNlIHRoYXQKICAgICAgICAjIGlzIGluIGNoYXJnZSBvZiBjbG9zaW5nIGl0IGFsc28KICA
gICAgICBpZiBzZWxmLl9zdGRpbl9yZWFkX2ZkIGFuZCBub3Qgc2VsZi5fc3RkaW5fc3RyZWFtOgog
ICAgICAgICAgICBvcy5jbG9zZShzZWxmLl9zdGRpbl9yZWFkX2ZkKQoKCiAgICBkZWYgd2FpdChzZ
WxmKToKICAgICAgICAiIiIgd2FpdHMgZm9yIHRoZSBwcm9jZXNzIHRvIGNvbXBsZXRlLCBoYW5kbG
VzIHRoZSBleGl0IGNvZGUgIiIiCgogICAgICAgIHNlbGYubG9nLmRlYnVnKCJhY3F1aXJpbmcgd2F
pdCBsb2NrIHRvIHdhaXQgZm9yIGNvbXBsZXRpb24iKQogICAgICAgICMgdXNpbmcgdGhlIGxvY2sg
aW4gYSB3aXRoLWNvbnRleHQgYmxvY2tzLCB3aGljaCBpcyB3aGF0IHdlIHdhbnQgaWYKICAgICAgI
CAjIHdlJ3JlIHJ1bm5pbmcgd2FpdCgpCiAgICAgICAgd2l0aCBzZWxmLl93YWl0X2xvY2s6CiAgIC
AgICAgICAgIHNlbGYubG9nLmRlYnVnKCJnb3Qgd2FpdCBsb2NrIikKICAgICAgICAgICAgd2l0bmV
zc2VkX2VuZCA9IEZhbHNlCgogICAgICAgICAgICBpZiBzZWxmLmV4aXRfY29kZSBpcyBOb25lOgog
ICAgICAgICAgICAgICAgc2VsZi5sb2cuZGVidWcoImV4aXQgY29kZSBub3Qgc2V0LCB3YWl0aW5nI
G9uIHBpZCIpCiAgICAgICAgICAgICAgICBwaWQsIGV4aXRfY29kZSA9IG5vX2ludGVycnVwdChvcy
53YWl0cGlkLCBzZWxmLnBpZCwgMCkgIyBibG9ja3MKICAgICAgICAgICAgICAgIHNlbGYuZXhpdF9
jb2RlID0gaGFuZGxlX3Byb2Nlc3NfZXhpdF9jb2RlKGV4aXRfY29kZSkKICAgICAgICAgICAgICAg
IHdpdG5lc3NlZF9lbmQgPSBUcnVlCgogICAgICAgICAgICBlbHNlOgogICAgICAgICAgICAgICAgc
2VsZi5sb2cuZGVidWcoImV4aXQgY29kZSBhbHJlYWR5IHNldCAoJWQpLCBubyBuZWVkIHRvIHdhaX
QiLAogICAgICAgICAgICAgICAgICAgICAgICBzZWxmLmV4aXRfY29kZSkKCiAgICAgICAgICAgIHN
lbGYuX3F1aXRfdGhyZWFkcy5zZXQoKQoKICAgICAgICAgICAgIyB3ZSBtYXkgbm90IGhhdmUgYSB0
aHJlYWQgZm9yIHN0ZGluLCBpZiB0aGUgcGlwZSBoYXMgYmVlbiBjb25uZWN0ZWQKICAgICAgICAgI
CAgIyB2aWEgX3BpcGVkPSJkaXJlY3QiCiAgICAgICAgICAgIGlmIHNlbGYuX2lucHV0X3RocmVhZD
oKICAgICAgICAgICAgICAgIHNlbGYuX2lucHV0X3RocmVhZC5qb2luKCkKCiAgICAgICAgICAgICM
gd2FpdCwgdGhlbiBzaWduYWwgdG8gb3VyIG91dHB1dCB0aHJlYWQgdGhhdCB0aGUgY2hpbGQgcHJv
Y2VzcyBpcwogICAgICAgICAgICAjIGRvbmUsIGFuZCB3ZSBzaG91bGQgaGF2ZSBmaW5pc2hlZCByZ
WFkaW5nIGFsbCB0aGUgc3Rkb3V0L3N0ZGVycgogICAgICAgICAgICAjIGRhdGEgdGhhdCB3ZSBjYW
4gYnkgbm93CiAgICAgICAgICAgIHRpbWVyID0gdGhyZWFkaW5nLlRpbWVyKDIuMCwgc2VsZi5fc3R
vcF9vdXRwdXRfZXZlbnQuc2V0KQogICAgICAgICAgICB0aW1lci5zdGFydCgpCgogICAgICAgICAg
ICAjIHdhaXQgZm9yIG91ciBzdGRvdXQgYW5kIHN0ZGVyciBzdHJlYW1yZWFkZXJzIHRvIGZpbmlza
CByZWFkaW5nIGFuZAogICAgICAgICAgICAjIGFnZ3JlZ2F0aW5nIHRoZSBwcm9jZXNzIG91dHB1dA
ogICAgICAgICAgICBzZWxmLl9vdXRwdXRfdGhyZWFkLmpvaW4oKQogICAgICAgICAgICB0aW1lci5
jYW5jZWwoKQoKICAgICAgICAgICAgc2VsZi5fYmFja2dyb3VuZF90aHJlYWQuam9pbigpCgogICAg
ICAgICAgICBpZiB3aXRuZXNzZWRfZW5kOgogICAgICAgICAgICAgICAgc2VsZi5fcHJvY2Vzc19qd
XN0X2VuZGVkKCkKCiAgICAgICAgICAgIHJldHVybiBzZWxmLmV4aXRfY29kZQoKCgpkZWYgaW5wdX
RfdGhyZWFkKGxvZywgc3RkaW4sIGlzX2FsaXZlLCBxdWl0LCBjbG9zZV9iZWZvcmVfdGVybSk6CiA
gICAiIiIgdGhpcyBpcyBydW4gaW4gYSBzZXBhcmF0ZSB0aHJlYWQuICBpdCB3cml0ZXMgaW50byBv
dXIgcHJvY2VzcydzCiAgICBzdGRpbiAoYSBzdHJlYW13cml0ZXIpIGFuZCB3YWl0cyB0aGUgcHJvY
2VzcyB0byBlbmQgQU5EIGV2ZXJ5dGhpbmcgdGhhdAogICAgY2FuIGJlIHdyaXR0ZW4gdG8gYmUgd3
JpdHRlbiAiIiIKCiAgICBkb25lID0gRmFsc2UKICAgIGNsb3NlZCA9IEZhbHNlCiAgICBhbGl2ZSA
9IFRydWUKICAgIHBvbGxlciA9IFBvbGxlcigpCiAgICBwb2xsZXIucmVnaXN0ZXJfd3JpdGUoc3Rk
aW4pCgogICAgd2hpbGUgcG9sbGVyIGFuZCBhbGl2ZToKICAgICAgICBjaGFuZ2VkID0gcG9sbGVyL
nBvbGwoMSkKICAgICAgICBmb3IgZmQsIGV2ZW50cyBpbiBjaGFuZ2VkOgogICAgICAgICAgICBpZi
BldmVudHMgJiAoUE9MTEVSX0VWRU5UX1dSSVRFIHwgUE9MTEVSX0VWRU5UX0hVUCk6CiAgICAgICA
gICAgICAgICBsb2cuZGVidWcoIiVyIHJlYWR5IGZvciBtb3JlIGlucHV0Iiwgc3RkaW4pCiAgICAg
ICAgICAgICAgICBkb25lID0gc3RkaW4ud3JpdGUoKQoKICAgICAgICAgICAgICAgIGlmIGRvbmU6C
iAgICAgICAgICAgICAgICAgICAgcG9sbGVyLnVucmVnaXN0ZXIoc3RkaW4pCiAgICAgICAgICAgIC
AgICAgICAgaWYgY2xvc2VfYmVmb3JlX3Rlcm06CiAgICAgICAgICAgICAgICAgICAgICAgIHN0ZGl
uLmNsb3NlKCkKICAgICAgICAgICAgICAgICAgICAgICAgY2xvc2VkID0gVHJ1ZQoKICAgICAgICBh
bGl2ZSwgXyA9IGlzX2FsaXZlKCkKCiAgICB3aGlsZSBhbGl2ZToKICAgICAgICBxdWl0LndhaXQoM
SkKICAgICAgICBhbGl2ZSwgXyA9IGlzX2FsaXZlKCkKCiAgICBpZiBub3QgY2xvc2VkOgogICAgIC
AgIHN0ZGluLmNsb3NlKCkKCgpkZWYgZXZlbnRfd2FpdChldiwgdGltZW91dD1Ob25lKToKICAgIHR
yaWdnZXJlZCA9IGV2LndhaXQodGltZW91dCkKICAgIGlmIElTX1BZMjY6CiAgICAgICAgdHJpZ2dl
cmVkID0gZXYuaXNfc2V0KCkKICAgIHJldHVybiB0cmlnZ2VyZWQKCgpkZWYgYmFja2dyb3VuZF90a
HJlYWQodGltZW91dF9mbiwgdGltZW91dF9ldmVudCwgaGFuZGxlX2V4aXRfY29kZSwgaXNfYWxpdm
UsCiAgICAgICAgcXVpdCk6CiAgICAiIiIgaGFuZGxlcyB0aGUgdGltZW91dCBsb2dpYyAiIiIKCiA
gICAjIGlmIHRoZXJlJ3MgYSB0aW1lb3V0IGV2ZW50LCBsb29wIAogICAgaWYgdGltZW91dF9ldmVu
dDoKICAgICAgICB3aGlsZSBub3QgcXVpdC5pc19zZXQoKToKICAgICAgICAgICAgdGltZWRfb3V0I
D0gZXZlbnRfd2FpdCh0aW1lb3V0X2V2ZW50LCAwLjEpCiAgICAgICAgICAgIGlmIHRpbWVkX291dD
oKICAgICAgICAgICAgICAgIHRpbWVvdXRfZm4oKQogICAgICAgICAgICAgICAgYnJlYWsKCiAgICA
jIGhhbmRsZV9leGl0X2NvZGUgd2lsbCBiZSBhIGZ1bmN0aW9uIE9OTFkgaWYgb3VyIGNvbW1hbmQg
d2FzIE5PVCB3YWl0ZWQgb24KICAgICMgYXMgcGFydCBvZiBpdHMgc3Bhd25pbmcuICBpbiBvdGhlc
iB3b3JkcywgaXQncyBwcm9iYWJseSBhIGJhY2tncm91bmQKICAgICMgY29tbWFuZAogICAgIwogIC
AgIyB0aGlzIHJlcG9ydHMgdGhlIGV4aXQgY29kZSBleGNlcHRpb24gaW4gb3VyIHRocmVhZC4gIGl
0J3MgcHVyZWx5IGZvciB0aGUKICAgICMgdXNlcidzIGF3YXJlbmVzcywgYW5kIGNhbm5vdCBiZSBj
YXVnaHQgb3IgdXNlZCBpbiBhbnkgd2F5LCBzbyBpdCdzIG9rIHRvCiAgICAjIHN1cHByZXNzIHRoa
XMgZHVyaW5nIHRoZSB0ZXN0cwogICAgaWYgaGFuZGxlX2V4aXRfY29kZSBhbmQgbm90IFJVTk5JTk
dfVEVTVFM6ICMgcHJhZ21hOiBubyBjb3ZlcgogICAgICAgIGFsaXZlID0gVHJ1ZQogICAgICAgIHd
oaWxlIGFsaXZlOgogICAgICAgICAgICBxdWl0LndhaXQoMSkKICAgICAgICAgICAgYWxpdmUsIGV4
aXRfY29kZSA9IGlzX2FsaXZlKCkKCiAgICAgICAgaGFuZGxlX2V4aXRfY29kZShleGl0X2NvZGUpC
goKZGVmIG91dHB1dF90aHJlYWQobG9nLCBzdGRvdXQsIHN0ZGVyciwgdGltZW91dF9ldmVudCwgaX
NfYWxpdmUsIHF1aXQsCiAgICAgICAgc3RvcF9vdXRwdXRfZXZlbnQpOgogICAgIiIiIHRoaXMgZnV
uY3Rpb24gaXMgcnVuIGluIGEgc2VwYXJhdGUgdGhyZWFkLiAgaXQgcmVhZHMgZnJvbSB0aGUKICAg
IHByb2Nlc3MncyBzdGRvdXQgc3RyZWFtIChhIHN0cmVhbXJlYWRlciksIGFuZCB3YWl0cyBmb3Iga
XQgdG8gY2xhaW0gdGhhdAogICAgaXRzIGRvbmUgIiIiCgogICAgcG9sbGVyID0gUG9sbGVyKCkKIC
AgIGlmIHN0ZG91dCBpcyBub3QgTm9uZToKICAgICAgICBwb2xsZXIucmVnaXN0ZXJfcmVhZChzdGR
vdXQpCiAgICBpZiBzdGRlcnIgaXMgbm90IE5vbmU6CiAgICAgICAgcG9sbGVyLnJlZ2lzdGVyX3Jl
YWQoc3RkZXJyKQoKICAgICMgdGhpcyBpcyBvdXIgcG9sbCBsb29wIGZvciBwb2xsaW5nIHN0ZG91d
CBvciBzdGRlcnIgdGhhdCBpcyByZWFkeSB0bwogICAgIyBiZSByZWFkIGFuZCBwcm9jZXNzZWQuIC
BpZiBvbmUgb2YgdGhvc2Ugc3RyZWFtcmVhZGVycyBpbmRpY2F0ZSB0aGF0IGl0CiAgICAjIGlzIGR
vbmUgYWx0b2dldGhlciBiZWluZyByZWFkIGZyb20sIHdlIHJlbW92ZSBpdCBmcm9tIG91ciBsaXN0
IG9mCiAgICAjIHRoaW5ncyB0byBwb2xsLiAgd2hlbiBubyBtb3JlIHRoaW5ncyBhcmUgbGVmdCB0b
yBwb2xsLCB3ZSBsZWF2ZSB0aGlzCiAgICAjIGxvb3AgYW5kIGNsZWFuIHVwCiAgICB3aGlsZSBwb2
xsZXI6CiAgICAgICAgY2hhbmdlZCA9IG5vX2ludGVycnVwdChwb2xsZXIucG9sbCwgMC4xKQogICA
gICAgIGZvciBmLCBldmVudHMgaW4gY2hhbmdlZDoKICAgICAgICAgICAgaWYgZXZlbnRzICYgKFBP
TExFUl9FVkVOVF9SRUFEIHwgUE9MTEVSX0VWRU5UX0hVUCk6CiAgICAgICAgICAgICAgICBsb2cuZ
GVidWcoIiVyIHJlYWR5IHRvIGJlIHJlYWQgZnJvbSIsIGYpCiAgICAgICAgICAgICAgICBkb25lID
0gZi5yZWFkKCkKICAgICAgICAgICAgICAgIGlmIGRvbmU6CiAgICAgICAgICAgICAgICAgICAgcG9
sbGVyLnVucmVnaXN0ZXIoZikKICAgICAgICAgICAgZWxpZiBldmVudHMgJiBQT0xMRVJfRVZFTlRf
RVJST1I6CiAgICAgICAgICAgICAgICAjIGZvciBzb21lIHJlYXNvbiwgd2UgaGF2ZSB0byBqdXN0I
Glnbm9yZSBzdHJlYW1zIHRoYXQgaGF2ZSBoYWQgYW4KICAgICAgICAgICAgICAgICMgZXJyb3IuIC
BpJ20gbm90IGV4YWN0bHkgc3VyZSB3aHksIGJ1dCBkb24ndCByZW1vdmUgdGhpcyB1bnRpbCB3ZQo
gICAgICAgICAgICAgICAgIyBmaWd1cmUgdGhhdCBvdXQsIGFuZCBjcmVhdGUgYSB0ZXN0IGZvciBp
dAogICAgICAgICAgICAgICAgcGFzcwoKICAgICAgICBpZiB0aW1lb3V0X2V2ZW50IGFuZCB0aW1lb
3V0X2V2ZW50LmlzX3NldCgpOgogICAgICAgICAgICBicmVhawoKICAgICAgICBpZiBzdG9wX291dH
B1dF9ldmVudC5pc19zZXQoKToKICAgICAgICAgICAgYnJlYWsKCiAgICAjIHdlIG5lZWQgdG8gd2F
pdCB1bnRpbCB0aGUgcHJvY2VzcyBpcyBndWFyYW50ZWVkIGRlYWQgYmVmb3JlIGNsb3Npbmcgb3Vy
CiAgICAjIG91dHB1dHMsIG90aGVyd2lzZSBTSUdQSVBFCiAgICBhbGl2ZSwgXyA9IGlzX2FsaXZlK
CkKICAgIHdoaWxlIGFsaXZlOgogICAgICAgIHF1aXQud2FpdCgxKQogICAgICAgIGFsaXZlLCBfID
0gaXNfYWxpdmUoKQoKICAgIGlmIHN0ZG91dDoKICAgICAgICBzdGRvdXQuY2xvc2UoKQoKICAgIGl
mIHN0ZGVycjoKICAgICAgICBzdGRlcnIuY2xvc2UoKQoKCmNsYXNzIERvbmVSZWFkaW5nRm9yZXZl
cihFeGNlcHRpb24pOiBwYXNzCmNsYXNzIE5vdFlldFJlYWR5VG9SZWFkKEV4Y2VwdGlvbik6IHBhc
3MKCgpkZWYgZGV0ZXJtaW5lX2hvd190b19yZWFkX2lucHV0KGlucHV0X29iaik6CiAgICAiIiIgZ2
l2ZW4gc29tZSBraW5kIG9mIGlucHV0IG9iamVjdCwgcmV0dXJuIGEgZnVuY3Rpb24gdGhhdCBrbm9
3cyBob3cgdG8KICAgIHJlYWQgY2h1bmtzIG9mIHRoYXQgaW5wdXQgb2JqZWN0LgogICAgCiAgICBl
YWNoIHJlYWRlciBmdW5jdGlvbiBzaG91bGQgcmV0dXJuIGEgY2h1bmsgYW5kIHJhaXNlIGEgRG9uZ
VJlYWRpbmdGb3JldmVyCiAgICBleGNlcHRpb24sIG9yIHJldHVybiBOb25lLCB3aGVuIHRoZXJlJ3
Mgbm8gbW9yZSBkYXRhIHRvIHJlYWQKCiAgICBOT1RFOiB0aGUgZnVuY3Rpb24gcmV0dXJuZWQgZG9
lcyBub3QgbmVlZCB0byBjYXJlIG11Y2ggYWJvdXQgdGhlIHJlcXVlc3RlZAogICAgYnVmZmVyaW5n
IHR5cGUgKGVnLCB1bmJ1ZmZlcmVkIHZzIG5ld2xpbmUtYnVmZmVyZWQpLiAgdGhlIFN0cmVhbUJ1Z
mZlcmVyCiAgICB3aWxsIHRha2UgY2FyZSBvZiB0aGF0LiAgdGhlc2UgZnVuY3Rpb25zIGp1c3Qgbm
VlZCB0byByZXR1cm4gYQogICAgcmVhc29uYWJseS1zaXplZCBjaHVuayBvZiBkYXRhLiAiIiIKCiA
gICBnZXRfY2h1bmsgPSBOb25lCgogICAgaWYgaXNpbnN0YW5jZShpbnB1dF9vYmosIFF1ZXVlKToK
ICAgICAgICBsb2dfbXNnID0gInF1ZXVlIgogICAgICAgIGdldF9jaHVuayA9IGdldF9xdWV1ZV9ja
HVua19yZWFkZXIoaW5wdXRfb2JqKQoKICAgIGVsaWYgY2FsbGFibGUoaW5wdXRfb2JqKToKICAgIC
AgICBsb2dfbXNnID0gImNhbGxhYmxlIgogICAgICAgIGdldF9jaHVuayA9IGdldF9jYWxsYWJsZV9
jaHVua19yZWFkZXIoaW5wdXRfb2JqKQoKICAgICMgYWxzbyBoYW5kbGVzIHN0cmluZ2lvCiAgICBl
bGlmIGhhc2F0dHIoaW5wdXRfb2JqLCAicmVhZCIpOgogICAgICAgIGxvZ19tc2cgPSAiZmlsZSBkZ
XNjcmlwdG9yIgogICAgICAgIGdldF9jaHVuayA9IGdldF9maWxlX2NodW5rX3JlYWRlcihpbnB1dF
9vYmopCgogICAgZWxpZiBpc2luc3RhbmNlKGlucHV0X29iaiwgYmFzZXN0cmluZyk6CiAgICAgICA
gbG9nX21zZyA9ICJzdHJpbmciCiAgICAgICAgZ2V0X2NodW5rID0gZ2V0X2l0ZXJfc3RyaW5nX3Jl
YWRlcihpbnB1dF9vYmopCgogICAgZWxpZiBpc2luc3RhbmNlKGlucHV0X29iaiwgYnl0ZXMpOgogI
CAgICAgIGxvZ19tc2cgPSAiYnl0ZXMiCiAgICAgICAgZ2V0X2NodW5rID0gZ2V0X2l0ZXJfc3RyaW
5nX3JlYWRlcihpbnB1dF9vYmopCgogICAgZWxpZiBpc2luc3RhbmNlKGlucHV0X29iaiwgR2VuZXJ
hdG9yVHlwZSk6CiAgICAgICAgbG9nX21zZyA9ICJnZW5lcmF0b3IiCiAgICAgICAgZ2V0X2NodW5r
ID0gZ2V0X2l0ZXJfY2h1bmtfcmVhZGVyKGl0ZXIoaW5wdXRfb2JqKSkKCiAgICBlbHNlOgogICAgI
CAgIHRyeToKICAgICAgICAgICAgaXQgPSBpdGVyKGlucHV0X29iaikKICAgICAgICBleGNlcHQgVH
lwZUVycm9yOgogICAgICAgICAgICByYWlzZSBFeGNlcHRpb24oInVua25vd24gaW5wdXQgb2JqZWN
0IikKICAgICAgICBlbHNlOgogICAgICAgICAgICBsb2dfbXNnID0gImdlbmVyYWwgaXRlcmFibGUi
CiAgICAgICAgICAgIGdldF9jaHVuayA9IGdldF9pdGVyX2NodW5rX3JlYWRlcihpdCkKCiAgICByZ
XR1cm4gZ2V0X2NodW5rLCBsb2dfbXNnCgoKCmRlZiBnZXRfcXVldWVfY2h1bmtfcmVhZGVyKHN0ZG
luKToKICAgIGRlZiBmbigpOgogICAgICAgIHRyeToKICAgICAgICAgICAgY2h1bmsgPSBzdGRpbi5
nZXQoVHJ1ZSwgMC4xKQogICAgICAgIGV4Y2VwdCBFbXB0eToKICAgICAgICAgICAgcmFpc2UgTm90
WWV0UmVhZHlUb1JlYWQKICAgICAgICBpZiBjaHVuayBpcyBOb25lOgogICAgICAgICAgICByYWlzZ
SBEb25lUmVhZGluZ0ZvcmV2ZXIKICAgICAgICByZXR1cm4gY2h1bmsKICAgIHJldHVybiBmbgoKCm
RlZiBnZXRfY2FsbGFibGVfY2h1bmtfcmVhZGVyKHN0ZGluKToKICAgIGRlZiBmbigpOgogICAgICA
gIHRyeToKICAgICAgICAgICAgZGF0YSA9IHN0ZGluKCkKICAgICAgICBleGNlcHQgRG9uZVJlYWRp
bmdGb3JldmVyOgogICAgICAgICAgICByYWlzZQoKICAgICAgICBpZiBub3QgZGF0YToKICAgICAgI
CAgICAgcmFpc2UgRG9uZVJlYWRpbmdGb3JldmVyCgogICAgICAgIHJldHVybiBkYXRhCgogICAgcm
V0dXJuIGZuCgoKZGVmIGdldF9pdGVyX3N0cmluZ19yZWFkZXIoc3RkaW4pOgogICAgIiIiIHJldHV
ybiBhbiBpdGVyYXRvciB0aGF0IHJldHVybnMgYSBjaHVuayBvZiBhIHN0cmluZyBldmVyeSB0aW1l
IGl0IGlzCiAgICBjYWxsZWQuICBub3RpY2UgdGhhdCBldmVuIHRob3VnaCBidWZzaXplX3R5cGUgb
WlnaHQgYmUgbGluZSBidWZmZXJlZCwgd2UncmUKICAgIG5vdCBkb2luZyBhbnkgbGluZSBidWZmZX
JpbmcgaGVyZS4gIHRoYXQncyBiZWNhdXNlIG91ciBTdHJlYW1CdWZmZXJlcgogICAgaGFuZGxlcyB
hbGwgYnVmZmVyaW5nLiAgd2UganVzdCBuZWVkIHRvIHJldHVybiBhIHJlYXNvbmFibGUtc2l6ZWQg
Y2h1bmsuICIiIgogICAgYnVmc2l6ZSA9IDEwMjQKICAgIGl0ZXJfc3RyID0gKHN0ZGluW2k6aSArI
GJ1ZnNpemVdIGZvciBpIGluIHJhbmdlKDAsIGxlbihzdGRpbiksIGJ1ZnNpemUpKQogICAgcmV0dX
JuIGdldF9pdGVyX2NodW5rX3JlYWRlcihpdGVyX3N0cikKCgpkZWYgZ2V0X2l0ZXJfY2h1bmtfcmV
hZGVyKHN0ZGluKToKICAgIGRlZiBmbigpOgogICAgICAgIHRyeToKICAgICAgICAgICAgaWYgSVNf
UFkzOgogICAgICAgICAgICAgICAgY2h1bmsgPSBzdGRpbi5fX25leHRfXygpCiAgICAgICAgICAgI
GVsc2U6CiAgICAgICAgICAgICAgICBjaHVuayA9IHN0ZGluLm5leHQoKQogICAgICAgICAgICByZX
R1cm4gY2h1bmsKICAgICAgICBleGNlcHQgU3RvcEl0ZXJhdGlvbjoKICAgICAgICAgICAgcmFpc2U
gRG9uZVJlYWRpbmdGb3JldmVyCiAgICByZXR1cm4gZm4KCmRlZiBnZXRfZmlsZV9jaHVua19yZWFk
ZXIoc3RkaW4pOgogICAgYnVmc2l6ZSA9IDEwMjQKCiAgICBkZWYgZm4oKToKICAgICAgICAjIHB5d
GhvbiAzLiogaW5jbHVkZXMgYSBmaWxlbm8gb24gc3RyaW5naW9zLCBidXQgYWNjZXNzaW5nIGl0IH
Rocm93cyBhbgogICAgICAgICMgZXhjZXB0aW9uLiAgdGhhdCBleGNlcHRpb24gaXMgaG93IHdlJ2x
sIGtub3cgd2UgY2FuJ3QgZG8gYSBwb2xsIG9uCiAgICAgICAgIyBzdGRpbgogICAgICAgIGlzX3Jl
YWxfZmlsZSA9IFRydWUKICAgICAgICBpZiBJU19QWTM6CiAgICAgICAgICAgIHRyeToKICAgICAgI
CAgICAgICAgIHN0ZGluLmZpbGVubygpCiAgICAgICAgICAgIGV4Y2VwdCBVbnN1cHBvcnRlZE9wZX
JhdGlvbjoKICAgICAgICAgICAgICAgIGlzX3JlYWxfZmlsZSA9IEZhbHNlCgogICAgICAgICMgdGh
pcyBwb2xsIGlzIGZvciBmaWxlcyB0aGF0IG1heSBub3QgeWV0IGJlIHJlYWR5IHRvIHJlYWQuICB3
ZSB0ZXN0CiAgICAgICAgIyBmb3IgZmlsZW5vIGJlY2F1c2UgU3RyaW5nSU8vQnl0ZXNJTyBjYW5ub
3QgYmUgdXNlZCBpbiBhIHBvbGwKICAgICAgICBpZiBpc19yZWFsX2ZpbGUgYW5kIGhhc2F0dHIoc3
RkaW4sICJmaWxlbm8iKToKICAgICAgICAgICAgcG9sbGVyID0gUG9sbGVyKCkKICAgICAgICAgICA
gcG9sbGVyLnJlZ2lzdGVyX3JlYWQoc3RkaW4pCiAgICAgICAgICAgIGNoYW5nZWQgPSBwb2xsZXIu
cG9sbCgwLjEpCiAgICAgICAgICAgIHJlYWR5ID0gRmFsc2UKICAgICAgICAgICAgZm9yIGZkLCBld
mVudHMgaW4gY2hhbmdlZDoKICAgICAgICAgICAgICAgIGlmIGV2ZW50cyAmIChQT0xMRVJfRVZFTl
RfUkVBRCB8IFBPTExFUl9FVkVOVF9IVVApOgogICAgICAgICAgICAgICAgICAgIHJlYWR5ID0gVHJ
1ZQogICAgICAgICAgICBpZiBub3QgcmVhZHk6CiAgICAgICAgICAgICAgICByYWlzZSBOb3RZZXRS
ZWFkeVRvUmVhZAoKICAgICAgICBjaHVuayA9IHN0ZGluLnJlYWQoYnVmc2l6ZSkKICAgICAgICBpZ
iBub3QgY2h1bms6CiAgICAgICAgICAgIHJhaXNlIERvbmVSZWFkaW5nRm9yZXZlcgogICAgICAgIG
Vsc2U6CiAgICAgICAgICAgIHJldHVybiBjaHVuawoKICAgIHJldHVybiBmbgoKCmRlZiBidWZzaXp
lX3R5cGVfdG9fYnVmc2l6ZShiZl90eXBlKToKICAgICIiIiBmb3IgYSBnaXZlbiBidWZzaXplIHR5
cGUsIHJldHVybiB0aGUgYWN0dWFsIGJ1ZnNpemUgd2Ugd2lsbCByZWFkLgogICAgbm90aWNlIHRoY
XQgYWx0aG91Z2ggMSBtZWFucyAibmV3bGluZS1idWZmZXJlZCIsIHdlJ3JlIHJlYWRpbmcgYSBjaH
VuayBzaXplCiAgICBvZiAxMDI0LiAgdGhpcyBpcyBiZWNhdXNlIHdlIGhhdmUgdG8gcmVhZCBzb21
ldGhpbmcuICB3ZSBsZXQgYQogICAgU3RyZWFtQnVmZmVyZXIgaW5zdGFuY2UgaGFuZGxlIHNwbGl0
dGluZyBvdXIgY2h1bmsgb24gbmV3bGluZXMgIiIiCgogICAgIyBuZXdsaW5lcwogICAgaWYgYmZfd
HlwZSA9PSAxOgogICAgICAgIGJ1ZnNpemUgPSAxMDI0CiAgICAjIHVuYnVmZmVyZWQKICAgIGVsaW
YgYmZfdHlwZSA9PSAwOgogICAgICAgIGJ1ZnNpemUgPSAxCiAgICAjIG9yIGJ1ZmZlcmVkIGJ5IHN
wZWNpZmljIGFtb3VudAogICAgZWxzZToKICAgICAgICBidWZzaXplID0gYmZfdHlwZQoKICAgIHJl
dHVybiBidWZzaXplCgoKCmNsYXNzIFN0cmVhbVdyaXRlcihvYmplY3QpOgogICAgIiIiIFN0cmVhb
VdyaXRlciByZWFkcyBmcm9tIHNvbWUgaW5wdXQgKHRoZSBzdGRpbiBwYXJhbSkgYW5kIHdyaXRlcy
B0byBhIGZkCiAgICAodGhlIHN0cmVhbSBwYXJhbSkuICB0aGUgc3RkaW4gbWF5IGJlIGEgUXVldWU
sIGEgY2FsbGFibGUsIHNvbWV0aGluZyB3aXRoCiAgICB0aGUgInJlYWQiIG1ldGhvZCwgYSBzdHJp
bmcsIG9yIGFuIGl0ZXJhYmxlICIiIgoKICAgIGRlZiBfX2luaXRfXyhzZWxmLCBsb2csIHN0cmVhb
Swgc3RkaW4sIGJ1ZnNpemVfdHlwZSwgZW5jb2RpbmcsIHR0eV9pbik6CgogICAgICAgIHNlbGYuc3
RyZWFtID0gc3RyZWFtCiAgICAgICAgc2VsZi5zdGRpbiA9IHN0ZGluCgogICAgICAgIHNlbGYubG9
nID0gbG9nCiAgICAgICAgc2VsZi5lbmNvZGluZyA9IGVuY29kaW5nCiAgICAgICAgc2VsZi50dHlf
aW4gPSB0dHlfaW4KCiAgICAgICAgc2VsZi5zdHJlYW1fYnVmZmVyZXIgPSBTdHJlYW1CdWZmZXJlc
ihidWZzaXplX3R5cGUsIHNlbGYuZW5jb2RpbmcpCiAgICAgICAgc2VsZi5nZXRfY2h1bmssIGxvZ1
9tc2cgPSBkZXRlcm1pbmVfaG93X3RvX3JlYWRfaW5wdXQoc3RkaW4pCiAgICAgICAgc2VsZi5sb2c
uZGVidWcoInBhcnNlZCBzdGRpbiBhcyBhICVzIiwgbG9nX21zZykKCgogICAgZGVmIGZpbGVubyhz
ZWxmKToKICAgICAgICAiIiIgZGVmaW5pbmcgdGhpcyBhbGxvd3MgdXMgdG8gZG8gcG9sbCBvbiBhb
iBpbnN0YW5jZSBvZiB0aGlzCiAgICAgICAgY2xhc3MgIiIiCiAgICAgICAgcmV0dXJuIHNlbGYuc3
RyZWFtCgoKCiAgICBkZWYgd3JpdGUoc2VsZik6CiAgICAgICAgIiIiIGF0dGVtcHQgdG8gZ2V0IGE
gY2h1bmsgb2YgZGF0YSB0byB3cml0ZSB0byBvdXIgY2hpbGQgcHJvY2VzcydzCiAgICAgICAgc3Rk
aW4sIHRoZW4gd3JpdGUgaXQuICB0aGUgcmV0dXJuIHZhbHVlIGFuc3dlcnMgdGhlIHF1ZXN0aW9uc
yAiYXJlIHdlCiAgICAgICAgZG9uZSB3cml0aW5nIGZvcmV2ZXI/IiAiIiIKCiAgICAgICAgIyBnZX
RfY2h1bmsgbWF5IHNvbWV0aW1lcyByZXR1cm4gYnl0ZXMsIGFuZCBzb21ldGltZXMgcmV0dXJuIHN
0cmluZ3MKICAgICAgICAjIGJlY2F1c2Ugb2YgdGhlIG5hdHVyZSBvZiB0aGUgZGlmZmVyZW50IHR5
cGVzIG9mIFNURElOIG9iamVjdHMgd2UKICAgICAgICAjIHN1cHBvcnQKICAgICAgICB0cnk6CiAgI
CAgICAgICAgIGNodW5rID0gc2VsZi5nZXRfY2h1bmsoKQogICAgICAgICAgICBpZiBjaHVuayBpcy
BOb25lOgogICAgICAgICAgICAgICAgcmFpc2UgRG9uZVJlYWRpbmdGb3JldmVyCgogICAgICAgIGV
4Y2VwdCBEb25lUmVhZGluZ0ZvcmV2ZXI6CiAgICAgICAgICAgIHNlbGYubG9nLmRlYnVnKCJkb25l
IHJlYWRpbmciKQoKICAgICAgICAgICAgaWYgc2VsZi50dHlfaW46CiAgICAgICAgICAgICAgICAjI
EVPRiB0aW1lCiAgICAgICAgICAgICAgICB0cnk6CiAgICAgICAgICAgICAgICAgICAgY2hhciA9IH
Rlcm1pb3MudGNnZXRhdHRyKHNlbGYuc3RyZWFtKVs2XVt0ZXJtaW9zLlZFT0ZdCiAgICAgICAgICA
gICAgICBleGNlcHQ6CiAgICAgICAgICAgICAgICAgICAgY2hhciA9IGNocig0KS5lbmNvZGUoKQoK
ICAgICAgICAgICAgICAgICMgbm9ybWFsbHksIG9uZSBFT0Ygc2hvdWxkIGJlIGVub3VnaCB0byBza
WduYWwgdG8gYW4gcHJvZ3JhbQogICAgICAgICAgICAgICAgIyB0aGF0IGlzIHJlYWQoKWluZywgdG
8gcmV0dXJuIDAgYW5kIGJlIG9uIHlvdXIgd2F5LiAgaG93ZXZlciwKICAgICAgICAgICAgICAgICM
gc29tZSBwcm9ncmFtcyBhcmUgbWlzYmVoYXZlZCwgbGlrZSBweXRob24zLjEgYW5kIHB5dGhvbjMu
Mi4KICAgICAgICAgICAgICAgICMgdGhleSBkb24ndCBzdG9wIHJlYWRpbmcgc29tZXRpbWVzIGFmd
GVyIHJlYWQoKSByZXR1cm5zIDAuCiAgICAgICAgICAgICAgICAjIHRoaXMgY2FuIGJlIGRlbW9uc3
RyYXRlZCB3aXRoIHRoZSBmb2xsb3dpbmcgcHJvZ3JhbToKICAgICAgICAgICAgICAgICMKICAgICA
gICAgICAgICAgICMgaW1wb3J0IHN5cwogICAgICAgICAgICAgICAgIyBzeXMuc3Rkb3V0LndyaXRl
KHN5cy5zdGRpbi5yZWFkKCkpCiAgICAgICAgICAgICAgICAjCiAgICAgICAgICAgICAgICAjIHRoZ
W4gdHlwZSAnYScgZm9sbG93ZWQgYnkgY3RybC1kIDMgdGltZXMuICBpbiBweXRob24KICAgICAgIC
AgICAgICAgICMgMi42LDIuNywzLjMsMy40LDMuNSwzLjYsIGl0IG9ubHkgdGFrZXMgMiBjdHJsLWQ
gdG8gdGVybWluYXRlLgogICAgICAgICAgICAgICAgIyBob3dldmVyLCBpbiBweXRob24gMy4xIGFu
ZCAzLjIsIGl0IHRha2VzIGFsbCAzLgogICAgICAgICAgICAgICAgIwogICAgICAgICAgICAgICAgI
yBzbyBoZXJlIHdlIHNlbmQgYW4gZXh0cmEgRU9GIGFsb25nLCBqdXN0IGluIGNhc2UuICBpIGRvbi
d0CiAgICAgICAgICAgICAgICAjIGJlbGlldmUgaXQgY2FuIGh1cnQgYW55dGhpbmcKICAgICAgICA
gICAgICAgIG9zLndyaXRlKHNlbGYuc3RyZWFtLCBjaGFyKQogICAgICAgICAgICAgICAgb3Mud3Jp
dGUoc2VsZi5zdHJlYW0sIGNoYXIpCgogICAgICAgICAgICByZXR1cm4gVHJ1ZQoKICAgICAgICBle
GNlcHQgTm90WWV0UmVhZHlUb1JlYWQ6CiAgICAgICAgICAgIHNlbGYubG9nLmRlYnVnKCJyZWNlaX
ZlZCBubyBkYXRhIikKICAgICAgICAgICAgcmV0dXJuIEZhbHNlCgogICAgICAgICMgaWYgd2UncmU
gbm90IGJ5dGVzLCBtYWtlIHVzIGJ5dGVzCiAgICAgICAgaWYgSVNfUFkzIGFuZCBoYXNhdHRyKGNo
dW5rLCAiZW5jb2RlIik6CiAgICAgICAgICAgIGNodW5rID0gY2h1bmsuZW5jb2RlKHNlbGYuZW5jb
2RpbmcpCgogICAgICAgIGZvciBwcm9jX2NodW5rIGluIHNlbGYuc3RyZWFtX2J1ZmZlcmVyLnByb2
Nlc3MoY2h1bmspOgogICAgICAgICAgICBzZWxmLmxvZy5kZWJ1ZygiZ290IGNodW5rIHNpemUgJWQ
6ICVyIiwgbGVuKHByb2NfY2h1bmspLAogICAgICAgICAgICAgICAgICAgIHByb2NfY2h1bmtbOjMw
XSkKCiAgICAgICAgICAgIHNlbGYubG9nLmRlYnVnKCJ3cml0aW5nIGNodW5rIHRvIHByb2Nlc3MiK
QogICAgICAgICAgICB0cnk6CiAgICAgICAgICAgICAgICBvcy53cml0ZShzZWxmLnN0cmVhbSwgcH
JvY19jaHVuaykKICAgICAgICAgICAgZXhjZXB0IE9TRXJyb3I6CiAgICAgICAgICAgICAgICBzZWx
mLmxvZy5kZWJ1ZygiT1NFcnJvciB3cml0aW5nIHN0ZGluIGNodW5rIikKICAgICAgICAgICAgICAg
IHJldHVybiBUcnVlCgoKICAgIGRlZiBjbG9zZShzZWxmKToKICAgICAgICBzZWxmLmxvZy5kZWJ1Z
ygiY2xvc2luZywgYnV0IGZsdXNoaW5nIGZpcnN0IikKICAgICAgICBjaHVuayA9IHNlbGYuc3RyZW
FtX2J1ZmZlcmVyLmZsdXNoKCkKICAgICAgICBzZWxmLmxvZy5kZWJ1ZygiZ290IGNodW5rIHNpemU
gJWQgdG8gZmx1c2g6ICVyIiwgbGVuKGNodW5rKSwgY2h1bmtbOjMwXSkKICAgICAgICB0cnk6CiAg
ICAgICAgICAgIGlmIGNodW5rOgogICAgICAgICAgICAgICAgb3Mud3JpdGUoc2VsZi5zdHJlYW0sI
GNodW5rKQoKICAgICAgICBleGNlcHQgT1NFcnJvcjoKICAgICAgICAgICAgcGFzcwoKICAgICAgIC
Bvcy5jbG9zZShzZWxmLnN0cmVhbSkKCgpkZWYgZGV0ZXJtaW5lX2hvd190b19mZWVkX291dHB1dCh
oYW5kbGVyLCBlbmNvZGluZywgZGVjb2RlX2Vycm9ycyk6CiAgICBpZiBjYWxsYWJsZShoYW5kbGVy
KToKICAgICAgICBwcm9jZXNzLCBmaW5pc2ggPSBnZXRfY2FsbGJhY2tfY2h1bmtfY29uc3VtZXIoa
GFuZGxlciwgZW5jb2RpbmcsCiAgICAgICAgICAgICAgICBkZWNvZGVfZXJyb3JzKQoKICAgICMgaW
4gcHkzLCB0aGlzIGlzIHVzZWQgZm9yIGJ5dGVzCiAgICBlbGlmIGlzaW5zdGFuY2UoaGFuZGxlciw
gKGNTdHJpbmdJTywgaW9jU3RyaW5nSU8pKToKICAgICAgICBwcm9jZXNzLCBmaW5pc2ggPSBnZXRf
Y3N0cmluZ2lvX2NodW5rX2NvbnN1bWVyKGhhbmRsZXIpCgogICAgIyBpbiBweTMsIHRoaXMgaXMgd
XNlZCBmb3IgdW5pY29kZQogICAgZWxpZiBpc2luc3RhbmNlKGhhbmRsZXIsIChTdHJpbmdJTywgaW
9TdHJpbmdJTykpOgogICAgICAgIHByb2Nlc3MsIGZpbmlzaCA9IGdldF9zdHJpbmdpb19jaHVua19
jb25zdW1lcihoYW5kbGVyLCBlbmNvZGluZywKICAgICAgICAgICAgICAgIGRlY29kZV9lcnJvcnMp
CgogICAgZWxpZiBoYXNhdHRyKGhhbmRsZXIsICJ3cml0ZSIpOgogICAgICAgIHByb2Nlc3MsIGZpb
mlzaCA9IGdldF9maWxlX2NodW5rX2NvbnN1bWVyKGhhbmRsZXIpCgogICAgZWxzZToKICAgICAgIC
B0cnk6CiAgICAgICAgICAgIGhhbmRsZXIgPSBpbnQoaGFuZGxlcikKICAgICAgICBleGNlcHQgKFZ
hbHVlRXJyb3IsIFR5cGVFcnJvcik6CiAgICAgICAgICAgIHByb2Nlc3MgPSBsYW1iZGEgY2h1bms6
IEZhbHNlCiAgICAgICAgICAgIGZpbmlzaCA9IGxhbWJkYTogTm9uZQogICAgICAgIGVsc2U6CiAgI
CAgICAgICAgIHByb2Nlc3MsIGZpbmlzaCA9IGdldF9mZF9jaHVua19jb25zdW1lcihoYW5kbGVyKQ
oKICAgIHJldHVybiBwcm9jZXNzLCBmaW5pc2gKCgpkZWYgZ2V0X2ZkX2NodW5rX2NvbnN1bWVyKGh
hbmRsZXIpOgogICAgaGFuZGxlciA9IGZkb3BlbihoYW5kbGVyLCAidyIsIGNsb3NlZmQ9RmFsc2Up
CiAgICByZXR1cm4gZ2V0X2ZpbGVfY2h1bmtfY29uc3VtZXIoaGFuZGxlcikKCmRlZiBnZXRfZmlsZ
V9jaHVua19jb25zdW1lcihoYW5kbGVyKToKICAgIGVuY29kZSA9IGxhbWJkYSBjaHVuazogY2h1bm
sKICAgIGlmIGdldGF0dHIoaGFuZGxlciwgImVuY29kaW5nIiwgTm9uZSk6CiAgICAgICAgZW5jb2R
lID0gbGFtYmRhIGNodW5rOiBjaHVuay5kZWNvZGUoaGFuZGxlci5lbmNvZGluZykKCiAgICBmbHVz
aCA9IGxhbWJkYTogTm9uZQogICAgaWYgaGFzYXR0cihoYW5kbGVyLCAiZmx1c2giKToKICAgICAgI
CBmbHVzaCA9IGhhbmRsZXIuZmx1c2gKCiAgICBkZWYgcHJvY2VzcyhjaHVuayk6CiAgICAgICAgaG
FuZGxlci53cml0ZShlbmNvZGUoY2h1bmspKQogICAgICAgICMgd2Ugc2hvdWxkIGZsdXNoIG9uIGF
uIGZkLiAgY2h1bmsgaXMgYWxyZWFkeSB0aGUgY29ycmVjdGx5LWJ1ZmZlcmVkCiAgICAgICAgIyBz
aXplLCBzbyB3ZSBkb24ndCBuZWVkIHRoZSBmZCBidWZmZXJpbmcgYXMgd2VsbAogICAgICAgIGZsd
XNoKCkKICAgICAgICByZXR1cm4gRmFsc2UKCiAgICBkZWYgZmluaXNoKCk6CiAgICAgICAgZmx1c2
goKQoKICAgIHJldHVybiBwcm9jZXNzLCBmaW5pc2gKCmRlZiBnZXRfY2FsbGJhY2tfY2h1bmtfY29
uc3VtZXIoaGFuZGxlciwgZW5jb2RpbmcsIGRlY29kZV9lcnJvcnMpOgogICAgZGVmIHByb2Nlc3Mo
Y2h1bmspOgogICAgICAgICMgdHJ5IHRvIHVzZSB0aGUgZW5jb2RpbmcgZmlyc3QsIGlmIHRoYXQgZ
G9lc24ndCB3b3JrLCBzZW5kCiAgICAgICAgIyB0aGUgYnl0ZXMsIGJlY2F1c2UgaXQgbWlnaHQgYm
UgYmluYXJ5CiAgICAgICAgdHJ5OgogICAgICAgICAgICBjaHVuayA9IGNodW5rLmRlY29kZShlbmN
vZGluZywgZGVjb2RlX2Vycm9ycykKICAgICAgICBleGNlcHQgVW5pY29kZURlY29kZUVycm9yOgog
ICAgICAgICAgICBwYXNzCiAgICAgICAgcmV0dXJuIGhhbmRsZXIoY2h1bmspCgogICAgZGVmIGZpb
mlzaCgpOgogICAgICAgIHBhc3MKCiAgICByZXR1cm4gcHJvY2VzcywgZmluaXNoCgpkZWYgZ2V0X2
NzdHJpbmdpb19jaHVua19jb25zdW1lcihoYW5kbGVyKToKICAgIGRlZiBwcm9jZXNzKGNodW5rKTo
KICAgICAgICBoYW5kbGVyLndyaXRlKGNodW5rKQogICAgICAgIHJldHVybiBGYWxzZQoKICAgIGRl
ZiBmaW5pc2goKToKICAgICAgICBwYXNzCgogICAgcmV0dXJuIHByb2Nlc3MsIGZpbmlzaAoKCmRlZ
iBnZXRfc3RyaW5naW9fY2h1bmtfY29uc3VtZXIoaGFuZGxlciwgZW5jb2RpbmcsIGRlY29kZV9lcn
JvcnMpOgogICAgZGVmIHByb2Nlc3MoY2h1bmspOgogICAgICAgIGhhbmRsZXIud3JpdGUoY2h1bms
uZGVjb2RlKGVuY29kaW5nLCBkZWNvZGVfZXJyb3JzKSkKICAgICAgICByZXR1cm4gRmFsc2UKCiAg
ICBkZWYgZmluaXNoKCk6CiAgICAgICAgcGFzcwoKICAgIHJldHVybiBwcm9jZXNzLCBmaW5pc2gKC
gpjbGFzcyBTdHJlYW1SZWFkZXIob2JqZWN0KToKICAgICIiIiByZWFkcyBmcm9tIHNvbWUgb3V0cH
V0ICh0aGUgc3RyZWFtKSBhbmQgc2VuZHMgd2hhdCBpdCBqdXN0IHJlYWQgdG8gdGhlCiAgICBoYW5
kbGVyLiAgIiIiCiAgICBkZWYgX19pbml0X18oc2VsZiwgbG9nLCBzdHJlYW0sIGhhbmRsZXIsIGJ1
ZmZlciwgYnVmc2l6ZV90eXBlLCBlbmNvZGluZywKICAgICAgICAgICAgZGVjb2RlX2Vycm9ycywgc
GlwZV9xdWV1ZT1Ob25lLCBzYXZlX2RhdGE9VHJ1ZSk6CiAgICAgICAgc2VsZi5zdHJlYW0gPSBzdH
JlYW0KICAgICAgICBzZWxmLmJ1ZmZlciA9IGJ1ZmZlcgogICAgICAgIHNlbGYuc2F2ZV9kYXRhID0
gc2F2ZV9kYXRhCiAgICAgICAgc2VsZi5lbmNvZGluZyA9IGVuY29kaW5nCiAgICAgICAgc2VsZi5k
ZWNvZGVfZXJyb3JzID0gZGVjb2RlX2Vycm9ycwoKICAgICAgICBzZWxmLnBpcGVfcXVldWUgPSBOb
25lCiAgICAgICAgaWYgcGlwZV9xdWV1ZToKICAgICAgICAgICAgc2VsZi5waXBlX3F1ZXVlID0gd2
Vha3JlZi5yZWYocGlwZV9xdWV1ZSkKCiAgICAgICAgc2VsZi5sb2cgPSBsb2cKCiAgICAgICAgc2V
sZi5zdHJlYW1fYnVmZmVyZXIgPSBTdHJlYW1CdWZmZXJlcihidWZzaXplX3R5cGUsIHNlbGYuZW5j
b2RpbmcsCiAgICAgICAgICAgICAgICBzZWxmLmRlY29kZV9lcnJvcnMpCiAgICAgICAgc2VsZi5id
WZzaXplID0gYnVmc2l6ZV90eXBlX3RvX2J1ZnNpemUoYnVmc2l6ZV90eXBlKQoKICAgICAgICBzZW
xmLnByb2Nlc3NfY2h1bmssIHNlbGYuZmluaXNoX2NodW5rX3Byb2Nlc3NvciA9IFwKICAgICAgICA
gICAgICAgIGRldGVybWluZV9ob3dfdG9fZmVlZF9vdXRwdXQoaGFuZGxlciwgZW5jb2RpbmcsIGRl
Y29kZV9lcnJvcnMpCgogICAgICAgIHNlbGYuc2hvdWxkX3F1aXQgPSBGYWxzZQoKCiAgICBkZWYgZ
mlsZW5vKHNlbGYpOgogICAgICAgICIiIiBkZWZpbmluZyB0aGlzIGFsbG93cyB1cyB0byBkbyBwb2
xsIG9uIGFuIGluc3RhbmNlIG9mIHRoaXMKICAgICAgICBjbGFzcyAiIiIKICAgICAgICByZXR1cm4
gc2VsZi5zdHJlYW0KCiAgICBkZWYgY2xvc2Uoc2VsZik6CiAgICAgICAgY2h1bmsgPSBzZWxmLnN0
cmVhbV9idWZmZXJlci5mbHVzaCgpCiAgICAgICAgc2VsZi5sb2cuZGVidWcoImdvdCBjaHVuayBza
XplICVkIHRvIGZsdXNoOiAlciIsIGxlbihjaHVuayksIGNodW5rWzozMF0pCiAgICAgICAgaWYgY2
h1bms6CiAgICAgICAgICAgIHNlbGYud3JpdGVfY2h1bmsoY2h1bmspCgogICAgICAgIHNlbGYuZml
uaXNoX2NodW5rX3Byb2Nlc3NvcigpCgogICAgICAgIGlmIHNlbGYucGlwZV9xdWV1ZSBhbmQgc2Vs
Zi5zYXZlX2RhdGE6CiAgICAgICAgICAgIHNlbGYucGlwZV9xdWV1ZSgpLnB1dChOb25lKQoKICAgI
CAgICBvcy5jbG9zZShzZWxmLnN0cmVhbSkKCgogICAgZGVmIHdyaXRlX2NodW5rKHNlbGYsIGNodW
5rKToKICAgICAgICAjIGluIFBZMywgdGhlIGNodW5rIGNvbWluZyBpbiB3aWxsIGJlIGJ5dGVzLCB
zbyBrZWVwIHRoYXQgaW4gbWluZAoKICAgICAgICBpZiBub3Qgc2VsZi5zaG91bGRfcXVpdDoKICAg
ICAgICAgICAgc2VsZi5zaG91bGRfcXVpdCA9IHNlbGYucHJvY2Vzc19jaHVuayhjaHVuaykKCgogI
CAgICAgIGlmIHNlbGYuc2F2ZV9kYXRhOgogICAgICAgICAgICBzZWxmLmJ1ZmZlci5hcHBlbmQoY2
h1bmspCgogICAgICAgICAgICBpZiBzZWxmLnBpcGVfcXVldWU6CiAgICAgICAgICAgICAgICBzZWx
mLmxvZy5kZWJ1ZygicHV0dGluZyBjaHVuayBvbnRvIHBpcGU6ICVyIiwgY2h1bmtbOjMwXSkKICAg
ICAgICAgICAgICAgIHNlbGYucGlwZV9xdWV1ZSgpLnB1dChjaHVuaykKCgogICAgZGVmIHJlYWQoc
2VsZik6CiAgICAgICAgIyBpZiB3ZSdyZSBQWTMsIHdlJ3JlIHJlYWRpbmcgYnl0ZXMsIG90aGVyd2
lzZSB3ZSdyZSByZWFkaW5nCiAgICAgICAgIyBzdHIKICAgICAgICB0cnk6CiAgICAgICAgICAgIGN
odW5rID0gbm9faW50ZXJydXB0KG9zLnJlYWQsIHNlbGYuc3RyZWFtLCBzZWxmLmJ1ZnNpemUpCiAg
ICAgICAgZXhjZXB0IE9TRXJyb3IgYXMgZToKICAgICAgICAgICAgc2VsZi5sb2cuZGVidWcoImdvd
CBlcnJubyAlZCwgZG9uZSByZWFkaW5nIiwgZS5lcnJubykKICAgICAgICAgICAgcmV0dXJuIFRydW
UKICAgICAgICBpZiBub3QgY2h1bms6CiAgICAgICAgICAgIHNlbGYubG9nLmRlYnVnKCJnb3Qgbm8
gY2h1bmssIGRvbmUgcmVhZGluZyIpCiAgICAgICAgICAgIHJldHVybiBUcnVlCgogICAgICAgIHNl
bGYubG9nLmRlYnVnKCJnb3QgY2h1bmsgc2l6ZSAlZDogJXIiLCBsZW4oY2h1bmspLCBjaHVua1s6M
zBdKQogICAgICAgIGZvciBjaHVuayBpbiBzZWxmLnN0cmVhbV9idWZmZXJlci5wcm9jZXNzKGNodW
5rKToKICAgICAgICAgICAgc2VsZi53cml0ZV9jaHVuayhjaHVuaykKCgoKCmNsYXNzIFN0cmVhbUJ
1ZmZlcmVyKG9iamVjdCk6CiAgICAiIiIgdGhpcyBpcyB1c2VkIGZvciBmZWVkaW5nIGluIGNodW5r
cyBvZiBzdGRvdXQvc3RkZXJyLCBhbmQgYnJlYWtpbmcgaXQgdXAKICAgIGludG8gY2h1bmtzIHRoY
XQgd2lsbCBhY3R1YWxseSBiZSBwdXQgaW50byB0aGUgaW50ZXJuYWwgYnVmZmVycy4gIGZvcgogIC
AgZXhhbXBsZSwgaWYgeW91IGhhdmUgdHdvIHByb2Nlc3Nlcywgb25lIGJlaW5nIHBpcGVkIHRvIHR
oZSBvdGhlciwgYW5kIHlvdQogICAgd2FudCB0aGF0LCBmaXJzdCBwcm9jZXNzIHRvIGZlZWQgbGlu
ZXMgb2YgZGF0YSAoaW5zdGVhZCBvZiB0aGUgY2h1bmtzCiAgICBob3dldmVyIHRoZXkgY29tZSBpb
iksIE9Qcm9jIHdpbGwgdXNlIGFuIGluc3RhbmNlIG9mIHRoaXMgY2xhc3MgdG8gY2hvcCB1cAogIC
AgdGhlIGRhdGEgYW5kIGZlZWQgaXQgYXMgbGluZXMgdG8gYmUgc2VudCBkb3duIHRoZSBwaXBlICI
iIgoKICAgIGRlZiBfX2luaXRfXyhzZWxmLCBidWZmZXJfdHlwZSwgZW5jb2Rpbmc9REVGQVVMVF9F
TkNPRElORywKICAgICAgICAgICAgZGVjb2RlX2Vycm9ycz0ic3RyaWN0Iik6CiAgICAgICAgIyAwI
GZvciB1bmJ1ZmZlcmVkLCAxIGZvciBsaW5lLCBldmVyeXRoaW5nIGVsc2UgZm9yIHRoYXQgYW1vdW
50CiAgICAgICAgc2VsZi50eXBlID0gYnVmZmVyX3R5cGUKICAgICAgICBzZWxmLmJ1ZmZlciA9IFt
dCiAgICAgICAgc2VsZi5uX2J1ZmZlcl9jb3VudCA9IDAKICAgICAgICBzZWxmLmVuY29kaW5nID0g
ZW5jb2RpbmcKICAgICAgICBzZWxmLmRlY29kZV9lcnJvcnMgPSBkZWNvZGVfZXJyb3JzCgogICAgI
CAgICMgdGhpcyBpcyBmb3IgaWYgd2UgY2hhbmdlIGJ1ZmZlcmluZyB0eXBlcy4gIGlmIHdlIGNoYW
5nZSBmcm9tIGxpbmUKICAgICAgICAjIGJ1ZmZlcmVkIHRvIHVuYnVmZmVyZWQsIGl0cyB2ZXJ5IHB
vc3NpYmxlIHRoYXQgb3VyIHNlbGYuYnVmZmVyIGxpc3QKICAgICAgICAjIGhhcyBkYXRhIHRoYXQg
d2FzIGJlaW5nIHNhdmVkIHVwICh3aGlsZSB3ZSBzZWFyY2hlZCBmb3IgYSBuZXdsaW5lKS4KICAgI
CAgICAjIHdlIG5lZWQgdG8gdXNlIHRoYXQgdXAsIHNvIHdlIGRvbid0IGxvc2UgaXQKICAgICAgIC
BzZWxmLl91c2VfdXBfYnVmZmVyX2ZpcnN0ID0gRmFsc2UKCiAgICAgICAgIyB0aGUgYnVmZmVyaW5
nIGxvY2sgaXMgdXNlZCBiZWNhdXNlIHdlIG1pZ2h0IGNoYW5nZSB0aGUgYnVmZmVyaW5nCiAgICAg
ICAgIyB0eXBlcyBmcm9tIGEgZGlmZmVyZW50IHRocmVhZC4gIGZvciBleGFtcGxlLCBpZiB3ZSBoY
XZlIGEgc3Rkb3V0CiAgICAgICAgIyBjYWxsYmFjaywgd2UgbWlnaHQgdXNlIGl0IHRvIGNoYW5nZS
B0aGUgd2F5IHN0ZGluIGJ1ZmZlcnMuICBzbyB3ZQogICAgICAgICMgbG9jawogICAgICAgIHNlbGY
uX2J1ZmZlcmluZ19sb2NrID0gdGhyZWFkaW5nLlJMb2NrKCkKICAgICAgICBzZWxmLmxvZyA9IExv
Z2dlcigic3RyZWFtX2J1ZmZlcmVyIikKCgogICAgZGVmIGNoYW5nZV9idWZmZXJpbmcoc2VsZiwgb
mV3X3R5cGUpOgogICAgICAgICMgVE9ETywgd2hlbiB3ZSBzdG9wIHN1cHBvcnRpbmcgMi42LCBtYW
tlIHRoaXMgYSB3aXRoIGNvbnRleHQKICAgICAgICBzZWxmLmxvZy5kZWJ1ZygiYWNxdWlyaW5nIGJ
1ZmZlcmluZyBsb2NrIGZvciBjaGFuZ2luZyBidWZmZXJpbmciKQogICAgICAgIHNlbGYuX2J1ZmZl
cmluZ19sb2NrLmFjcXVpcmUoKQogICAgICAgIHNlbGYubG9nLmRlYnVnKCJnb3QgYnVmZmVyaW5nI
GxvY2sgZm9yIGNoYW5naW5nIGJ1ZmZlcmluZyIpCiAgICAgICAgdHJ5OgogICAgICAgICAgICBpZi
BuZXdfdHlwZSA9PSAwOgogICAgICAgICAgICAgICAgc2VsZi5fdXNlX3VwX2J1ZmZlcl9maXJzdCA
9IFRydWUKCiAgICAgICAgICAgIHNlbGYudHlwZSA9IG5ld190eXBlCiAgICAgICAgZmluYWxseToK
ICAgICAgICAgICAgc2VsZi5fYnVmZmVyaW5nX2xvY2sucmVsZWFzZSgpCiAgICAgICAgICAgIHNlb
GYubG9nLmRlYnVnKCJyZWxlYXNlZCBidWZmZXJpbmcgbG9jayBmb3IgY2hhbmdpbmcgYnVmZmVyaW
5nIikKCgogICAgZGVmIHByb2Nlc3Moc2VsZiwgY2h1bmspOgogICAgICAgICMgTUFLRSBTVVJFIFR
IQVQgVEhFIElOUFVUIElTIFBZMyBCWVRFUwogICAgICAgICMgVEhFIE9VVFBVVCBJUyBBTFdBWVMg
UFkzIEJZVEVTCgogICAgICAgICMgVE9ETywgd2hlbiB3ZSBzdG9wIHN1cHBvcnRpbmcgMi42LCBtY
WtlIHRoaXMgYSB3aXRoIGNvbnRleHQKICAgICAgICBzZWxmLmxvZy5kZWJ1ZygiYWNxdWlyaW5nIG
J1ZmZlcmluZyBsb2NrIHRvIHByb2Nlc3MgY2h1bmsgKGJ1ZmZlcmluZzogJWQpIiwgc2VsZi50eXB
lKQogICAgICAgIHNlbGYuX2J1ZmZlcmluZ19sb2NrLmFjcXVpcmUoKQogICAgICAgIHNlbGYubG9n
LmRlYnVnKCJnb3QgYnVmZmVyaW5nIGxvY2sgdG8gcHJvY2VzcyBjaHVuayAoYnVmZmVyaW5nOiAlZ
CkiLCBzZWxmLnR5cGUpCiAgICAgICAgdHJ5OgogICAgICAgICAgICAjIHVuYnVmZmVyZWQKICAgIC
AgICAgICAgaWYgc2VsZi50eXBlID09IDA6CiAgICAgICAgICAgICAgICBpZiBzZWxmLl91c2VfdXB
fYnVmZmVyX2ZpcnN0OgogICAgICAgICAgICAgICAgICAgIHNlbGYuX3VzZV91cF9idWZmZXJfZmly
c3QgPSBGYWxzZQogICAgICAgICAgICAgICAgICAgIHRvX3dyaXRlID0gc2VsZi5idWZmZXIKICAgI
CAgICAgICAgICAgICAgICBzZWxmLmJ1ZmZlciA9IFtdCiAgICAgICAgICAgICAgICAgICAgdG9fd3
JpdGUuYXBwZW5kKGNodW5rKQogICAgICAgICAgICAgICAgICAgIHJldHVybiB0b193cml0ZQoKICA
gICAgICAgICAgICAgIHJldHVybiBbY2h1bmtdCgogICAgICAgICAgICAjIGxpbmUgYnVmZmVyZWQK
ICAgICAgICAgICAgZWxpZiBzZWxmLnR5cGUgPT0gMToKICAgICAgICAgICAgICAgIHRvdGFsX3RvX
3dyaXRlID0gW10KICAgICAgICAgICAgICAgIG5sID0gIlxuIi5lbmNvZGUoc2VsZi5lbmNvZGluZy
kKICAgICAgICAgICAgICAgIHdoaWxlIFRydWU6CiAgICAgICAgICAgICAgICAgICAgbmV3bGluZSA
9IGNodW5rLmZpbmQobmwpCiAgICAgICAgICAgICAgICAgICAgaWYgbmV3bGluZSA9PSAtMToKICAg
ICAgICAgICAgICAgICAgICAgICAgYnJlYWsKCiAgICAgICAgICAgICAgICAgICAgY2h1bmtfdG9fd
3JpdGUgPSBjaHVua1s6bmV3bGluZSArIDFdCiAgICAgICAgICAgICAgICAgICAgaWYgc2VsZi5idW
ZmZXI6CiAgICAgICAgICAgICAgICAgICAgICAgIGNodW5rX3RvX3dyaXRlID0gYiIiLmpvaW4oc2V
sZi5idWZmZXIpICsgY2h1bmtfdG9fd3JpdGUKCiAgICAgICAgICAgICAgICAgICAgICAgIHNlbGYu
YnVmZmVyID0gW10KICAgICAgICAgICAgICAgICAgICAgICAgc2VsZi5uX2J1ZmZlcl9jb3VudCA9I
DAKCiAgICAgICAgICAgICAgICAgICAgY2h1bmsgPSBjaHVua1tuZXdsaW5lICsgMTpdCiAgICAgIC
AgICAgICAgICAgICAgdG90YWxfdG9fd3JpdGUuYXBwZW5kKGNodW5rX3RvX3dyaXRlKQoKICAgICA
gICAgICAgICAgIGlmIGNodW5rOgogICAgICAgICAgICAgICAgICAgIHNlbGYuYnVmZmVyLmFwcGVu
ZChjaHVuaykKICAgICAgICAgICAgICAgICAgICBzZWxmLm5fYnVmZmVyX2NvdW50ICs9IGxlbihja
HVuaykKICAgICAgICAgICAgICAgIHJldHVybiB0b3RhbF90b193cml0ZQoKICAgICAgICAgICAgIy
BOIHNpemUgYnVmZmVyZWQKICAgICAgICAgICAgZWxzZToKICAgICAgICAgICAgICAgIHRvdGFsX3R
vX3dyaXRlID0gW10KICAgICAgICAgICAgICAgIHdoaWxlIFRydWU6CiAgICAgICAgICAgICAgICAg
ICAgb3ZlcmFnZSA9IHNlbGYubl9idWZmZXJfY291bnQgKyBsZW4oY2h1bmspIC0gc2VsZi50eXBlC
iAgICAgICAgICAgICAgICAgICAgaWYgb3ZlcmFnZSA+PSAwOgogICAgICAgICAgICAgICAgICAgIC
AgICByZXQgPSAiIi5lbmNvZGUoc2VsZi5lbmNvZGluZykuam9pbihzZWxmLmJ1ZmZlcikgKyBjaHV
uawogICAgICAgICAgICAgICAgICAgICAgICBjaHVua190b193cml0ZSA9IHJldFs6c2VsZi50eXBl
XQogICAgICAgICAgICAgICAgICAgICAgICBjaHVuayA9IHJldFtzZWxmLnR5cGU6XQogICAgICAgI
CAgICAgICAgICAgICAgICB0b3RhbF90b193cml0ZS5hcHBlbmQoY2h1bmtfdG9fd3JpdGUpCiAgIC
AgICAgICAgICAgICAgICAgICAgIHNlbGYuYnVmZmVyID0gW10KICAgICAgICAgICAgICAgICAgICA
gICAgc2VsZi5uX2J1ZmZlcl9jb3VudCA9IDAKICAgICAgICAgICAgICAgICAgICBlbHNlOgogICAg
ICAgICAgICAgICAgICAgICAgICBzZWxmLmJ1ZmZlci5hcHBlbmQoY2h1bmspCiAgICAgICAgICAgI
CAgICAgICAgICAgIHNlbGYubl9idWZmZXJfY291bnQgKz0gbGVuKGNodW5rKQogICAgICAgICAgIC
AgICAgICAgICAgICBicmVhawogICAgICAgICAgICAgICAgcmV0dXJuIHRvdGFsX3RvX3dyaXRlCiA
gICAgICAgZmluYWxseToKICAgICAgICAgICAgc2VsZi5fYnVmZmVyaW5nX2xvY2sucmVsZWFzZSgp
CiAgICAgICAgICAgIHNlbGYubG9nLmRlYnVnKCJyZWxlYXNlZCBidWZmZXJpbmcgbG9jayBmb3Igc
HJvY2Vzc2luZyBjaHVuayAoYnVmZmVyaW5nOiAlZCkiLCBzZWxmLnR5cGUpCgoKICAgIGRlZiBmbH
VzaChzZWxmKToKICAgICAgICBzZWxmLmxvZy5kZWJ1ZygiYWNxdWlyaW5nIGJ1ZmZlcmluZyBsb2N
rIGZvciBmbHVzaGluZyBidWZmZXIiKQogICAgICAgIHNlbGYuX2J1ZmZlcmluZ19sb2NrLmFjcXVp
cmUoKQogICAgICAgIHNlbGYubG9nLmRlYnVnKCJnb3QgYnVmZmVyaW5nIGxvY2sgZm9yIGZsdXNoa
W5nIGJ1ZmZlciIpCiAgICAgICAgdHJ5OgogICAgICAgICAgICByZXQgPSAiIi5lbmNvZGUoc2VsZi
5lbmNvZGluZykuam9pbihzZWxmLmJ1ZmZlcikKICAgICAgICAgICAgc2VsZi5idWZmZXIgPSBbXQo
gICAgICAgICAgICByZXR1cm4gcmV0CiAgICAgICAgZmluYWxseToKICAgICAgICAgICAgc2VsZi5f
YnVmZmVyaW5nX2xvY2sucmVsZWFzZSgpCiAgICAgICAgICAgIHNlbGYubG9nLmRlYnVnKCJyZWxlY
XNlZCBidWZmZXJpbmcgbG9jayBmb3IgZmx1c2hpbmcgYnVmZmVyIikKCgoKZGVmIHdpdGhfbG9jay
hsb2NrKToKICAgIGRlZiB3cmFwcGVkKGZuKToKICAgICAgICBmbiA9IGNvbnRleHRtYW5hZ2VyKGZ
uKQogICAgICAgIEBjb250ZXh0bWFuYWdlcgogICAgICAgIGRlZiB3cmFwcGVkMigqYXJncywgKipr
d2FyZ3MpOgogICAgICAgICAgICB3aXRoIGxvY2s6CiAgICAgICAgICAgICAgICB3aXRoIGZuKCphc
mdzLCAqKmt3YXJncyk6CiAgICAgICAgICAgICAgICAgICAgeWllbGQKICAgICAgICByZXR1cm4gd3
JhcHBlZDIKICAgIHJldHVybiB3cmFwcGVkCgoKQHdpdGhfbG9jayhQVVNIRF9MT0NLKQpkZWYgcHV
zaGQocGF0aCk6CiAgICAiIiIgcHVzaGQgY2hhbmdlcyB0aGUgYWN0dWFsIHdvcmtpbmcgZGlyZWN0
b3J5IGZvciB0aGUgZHVyYXRpb24gb2YgdGhlCiAgICBjb250ZXh0LCB1bmxpa2UgdGhlIF9jd2QgY
XJnIHRoaXMgd2lsbCB3b3JrIHdpdGggb3RoZXIgYnVpbHQtaW5zIHN1Y2ggYXMKICAgIHNoLmdsb2
IgY29ycmVjdGx5ICIiIgogICAgb3JpZ19wYXRoID0gb3MuZ2V0Y3dkKCkKICAgIG9zLmNoZGlyKHB
hdGgpCiAgICB0cnk6CiAgICAgICAgeWllbGQKICAgIGZpbmFsbHk6CiAgICAgICAgb3MuY2hkaXIo
b3JpZ19wYXRoKQoKCkBjb250ZXh0bWFuYWdlcgpkZWYgYXJncygqKmt3YXJncyk6CiAgICAiIiIgY
Wxsb3dzIHVzIHRvIHRlbXBvcmFyaWx5IG92ZXJyaWRlIGFsbCB0aGUgc3BlY2lhbCBrZXl3b3JkIH
BhcmFtZXRlcnMgaW4KICAgIGEgd2l0aCBjb250ZXh0ICIiIgoKICAgIGt3YXJnc19zdHIgPSAiLCI
uam9pbihbIiVzPSVyIiAlIChrLHYpIGZvciBrLHYgaW4ga3dhcmdzLml0ZW1zKCldKQoKICAgIHJh
aXNlIERlcHJlY2F0aW9uV2FybmluZygiIiIKCnNoLmFyZ3MoKSBoYXMgYmVlbiBkZXByZWNhdGVkI
GJlY2F1c2UgaXQgd2FzIG5ldmVyIHRocmVhZCBzYWZlLiAgdXNlIHRoZQpmb2xsb3dpbmcgaW5zdG
VhZDoKCiAgICBzaDIgPSBzaCh7a3dhcmdzfSkKICAgIHNoMi55b3VyX2NvbW1hbmQoKQoKb3IKCiA
gICBzaDIgPSBzaCh7a3dhcmdzfSkKICAgIGZyb20gc2gyIGltcG9ydCB5b3VyX2NvbW1hbmQKICAg
IHlvdXJfY29tbWFuZCgpCgoiIiIuZm9ybWF0KGt3YXJncz1rd2FyZ3Nfc3RyKSkKCgoKY2xhc3MgR
W52aXJvbm1lbnQoZGljdCk6CiAgICAiIiIgdGhpcyBhbGxvd3MgbG9va3VwcyB0byBuYW1lcyB0aG
F0IGFyZW4ndCBmb3VuZCBpbiB0aGUgZ2xvYmFsIHNjb3BlIHRvIGJlCiAgICBzZWFyY2hlZCBmb3I
gYXMgYSBwcm9ncmFtIG5hbWUuICBmb3IgZXhhbXBsZSwgaWYgImxzIiBpc24ndCBmb3VuZCBpbiB0
aGlzCiAgICBtb2R1bGUncyBzY29wZSwgd2UgY29uc2lkZXIgaXQgYSBzeXN0ZW0gcHJvZ3JhbSBhb
mQgdHJ5IHRvIGZpbmQgaXQuCgogICAgd2UgdXNlIGEgZGljdCBpbnN0ZWFkIG9mIGp1c3QgYSByZW
d1bGFyIG9iamVjdCBhcyB0aGUgYmFzZSBjbGFzcyBiZWNhdXNlIHRoZQogICAgZXhlYygpIHN0YXR
lbWVudCB1c2VkIGluIHRoZSBydW5fcmVwbCByZXF1aXJlcyB0aGUgImdsb2JhbHMiIGFyZ3VtZW50
IHRvIGJlIGEKICAgIGRpY3Rpb25hcnkgIiIiCgoKICAgICMgdGhpcyBpcyBhIGxpc3Qgb2YgYWxsI
G9mIHRoZSBuYW1lcyB0aGF0IHRoZSBzaCBtb2R1bGUgZXhwb3J0cyB0aGF0IHdpbGwKICAgICMgbm
90IHJlc29sdmUgdG8gZnVuY3Rpb25zLiAgd2UgZG9uJ3Qgd2FudCB0byBhY2NpZGVudGFsbHkgc2h
hZG93IHJlYWwKICAgICMgY29tbWFuZHMgd2l0aCBmdW5jdGlvbnMvaW1wb3J0cyB0aGF0IHdlIGRl
ZmluZSBpbiBzaC5weS4gIGZvciBleGFtcGxlLAogICAgIyAiaW1wb3J0IHRpbWUiIG1heSBvdmVyc
mlkZSB0aGUgdGltZSBzeXN0ZW0gcHJvZ3JhbQogICAgd2hpdGVsaXN0ID0gc2V0KFsKICAgICAgIC
AiQ29tbWFuZCIsCiAgICAgICAgIlJ1bm5pbmdDb21tYW5kIiwKICAgICAgICAiQ29tbWFuZE5vdEZ
vdW5kIiwKICAgICAgICAiREVGQVVMVF9FTkNPRElORyIsCiAgICAgICAgIkRvbmVSZWFkaW5nRm9y
ZXZlciIsCiAgICAgICAgIkVycm9yUmV0dXJuQ29kZSIsCiAgICAgICAgIk5vdFlldFJlYWR5VG9SZ
WFkIiwKICAgICAgICAiU2lnbmFsRXhjZXB0aW9uIiwKICAgICAgICAiRm9ya0V4Y2VwdGlvbiIsCi
AgICAgICAgIlRpbWVvdXRFeGNlcHRpb24iLAogICAgICAgICJfX3Byb2plY3RfdXJsX18iLAogICA
gICAgICJfX3ZlcnNpb25fXyIsCiAgICAgICAgIl9fZmlsZV9fIiwKICAgICAgICAiYXJncyIsCiAg
ICAgICAgInB1c2hkIiwKICAgICAgICAiZ2xvYiIsCiAgICAgICAgImNvbnRyaWIiLAogICAgXSkKC
gogICAgZGVmIF9faW5pdF9fKHNlbGYsIGdsb2JzLCBiYWtlZF9hcmdzPXt9KToKICAgICAgICAiIi
IgYmFrZWRfYXJncyBhcmUgZGVmYXVsdHMgZm9yIHRoZSAnc2gnIGV4ZWN1dGlvbiBjb250ZXh0LiA
gZm9yCiAgICAgICAgZXhhbXBsZToKICAgICAgICAgICAgCiAgICAgICAgICAgIHRtcCA9IHNoKF9v
dXQ9U3RyaW5nSU8oKSkKCiAgICAgICAgJ291dCcgd291bGQgZW5kIHVwIGluIGhlcmUgYXMgYW4gZ
W50cnkgaW4gdGhlIGJha2VkX2FyZ3MgZGljdCAiIiIKCiAgICAgICAgc2VsZi5nbG9icyA9IGdsb2
JzCiAgICAgICAgc2VsZi5iYWtlZF9hcmdzID0gYmFrZWRfYXJncwogICAgICAgIHNlbGYuZGlzYWJ
sZV93aGl0ZWxpc3QgPSBGYWxzZQoKICAgIGRlZiBfX2dldGl0ZW1fXyhzZWxmLCBrKToKICAgICAg
ICAjIGlmIHdlIGZpcnN0IGltcG9ydCAiX2Rpc2FibGVfd2hpdGVsaXN0IiBmcm9tIHNoLCB3ZSBjY
W4gaW1wb3J0CiAgICAgICAgIyBhbnl0aGluZyBkZWZpbmVkIGluIHRoZSBnbG9iYWwgc2NvcGUgb2
Ygc2gucHkuICB0aGlzIGlzIHVzZWZ1bCBmb3Igb3VyCiAgICAgICAgIyB0ZXN0cwogICAgICAgIGl
mIGsgPT0gIl9kaXNhYmxlX3doaXRlbGlzdCI6CiAgICAgICAgICAgIHNlbGYuZGlzYWJsZV93aGl0
ZWxpc3QgPSBUcnVlCiAgICAgICAgICAgIHJldHVybiBOb25lCgogICAgICAgICMgd2UncmUgdHJ5a
W5nIHRvIGltcG9ydCBzb21ldGhpbmcgcmVhbCAobWF5YmUpLCBzZWUgaWYgaXQncyBpbiBvdXIKIC
AgICAgICAjIGdsb2JhbCBzY29wZQogICAgICAgIGlmIGsgaW4gc2VsZi53aGl0ZWxpc3Qgb3Igc2V
sZi5kaXNhYmxlX3doaXRlbGlzdDoKICAgICAgICAgICAgcmV0dXJuIHNlbGYuZ2xvYnNba10KCiAg
ICAgICAgIyBzb21lYm9keSB0cmllZCB0byBiZSBmdW5ueSBhbmQgZG8gImZyb20gc2ggaW1wb3J0I
CoiCiAgICAgICAgaWYgayA9PSAiX19hbGxfXyI6CiAgICAgICAgICAgIHJhaXNlIFJ1bnRpbWVFcn
JvcigiQ2Fubm90IGltcG9ydCAqIGZyb20gc2guIFwKUGxlYXNlIGltcG9ydCBzaCBvciBpbXBvcnQ
gcHJvZ3JhbXMgaW5kaXZpZHVhbGx5LiIpCgoKICAgICAgICAjIGNoZWNrIGlmIHdlJ3JlIG5hbWlu
ZyBhIGR5bmFtaWNhbGx5IGdlbmVyYXRlZCBSZXR1cm5Db2RlIGV4Y2VwdGlvbgogICAgICAgIGV4Y
yA9IGdldF9leGNfZnJvbV9uYW1lKGspCiAgICAgICAgaWYgZXhjOgogICAgICAgICAgICByZXR1cm
4gZXhjCgoKICAgICAgICAjIGh0dHBzOi8vZ2l0aHViLmNvbS9pcHl0aG9uL2lweXRob24vaXNzdWV
zLzI1NzcKICAgICAgICAjIGh0dHBzOi8vZ2l0aHViLmNvbS9hbW9mZmF0L3NoL2lzc3Vlcy85NyNp
c3N1ZWNvbW1lbnQtMTA2MTA2MjkKICAgICAgICBpZiBrLnN0YXJ0c3dpdGgoIl9fIikgYW5kIGsuZ
W5kc3dpdGgoIl9fIik6CiAgICAgICAgICAgIHJhaXNlIEF0dHJpYnV0ZUVycm9yCgoKICAgICAgIC
AjIGlzIGl0IGEgY3VzdG9tIGJ1aWx0aW4/CiAgICAgICAgYnVpbHRpbiA9IGdldGF0dHIoc2VsZiw
gImJfIiArIGssIE5vbmUpCiAgICAgICAgaWYgYnVpbHRpbjoKICAgICAgICAgICAgcmV0dXJuIGJ1
aWx0aW4KCgogICAgICAgICMgaXMgaXQgYSBjb21tYW5kPwogICAgICAgIGNtZCA9IHJlc29sdmVfY
29tbWFuZChrLCBzZWxmLmJha2VkX2FyZ3MpCiAgICAgICAgaWYgY21kOgogICAgICAgICAgICByZX
R1cm4gY21kCgoKICAgICAgICAjIGhvdyBhYm91dCBhbiBlbnZpcm9ubWVudCB2YXJpYWJsZT8KICA
gICAgICAjIHRoaXMgY2hlY2sgbXVzdCBjb21lIGFmdGVyIHRlc3RpbmcgaWYgaXRzIGEgY29tbWFu
ZCwgYmVjYXVzZSBvbiBzb21lCiAgICAgICAgIyBzeXN0ZW1zLCB0aGVyZSBhcmUgYW4gZW52aXJvb
m1lbnQgdmFyaWFibGVzIHRoYXQgY2FuIGNvbmZsaWN0IHdpdGgKICAgICAgICAjIGNvbW1hbmQgbm
FtZXMuCiAgICAgICAgIyBodHRwczovL2dpdGh1Yi5jb20vYW1vZmZhdC9zaC9pc3N1ZXMvMjM4CiA
gICAgICAgdHJ5OgogICAgICAgICAgICByZXR1cm4gb3MuZW52aXJvbltrXQogICAgICAgIGV4Y2Vw
dCBLZXlFcnJvcjoKICAgICAgICAgICAgcGFzcwoKCiAgICAgICAgIyBub3RoaW5nIGZvdW5kLCByY
WlzZSBhbiBleGNlcHRpb24KICAgICAgICByYWlzZSBDb21tYW5kTm90Rm91bmQoaykKCgogICAgIy
BtZXRob2RzIHRoYXQgYmVnaW4gd2l0aCAiYl8iIGFyZSBjdXN0b20gYnVpbHRpbnMgYW5kIHdpbGw
gb3ZlcnJpZGUgYW55CiAgICAjIHByb2dyYW0gdGhhdCBleGlzdHMgaW4gb3VyIHBhdGguICB0aGlz
IGlzIHVzZWZ1bCBmb3IgdGhpbmdzIGxpa2UKICAgICMgY29tbW9uIHNoZWxsIGJ1aWx0aW5zIHRoY
XQgcGVvcGxlIGFyZSB1c2VkIHRvLCBidXQgd2hpY2ggYXJlbid0IGFjdHVhbGx5CiAgICAjIGZ1bG
wtZmxlZGdlZCBzeXN0ZW0gYmluYXJpZXMKCiAgICBkZWYgYl9jZChzZWxmLCBwYXRoPU5vbmUpOgo
gICAgICAgIGlmIHBhdGg6CiAgICAgICAgICAgIG9zLmNoZGlyKHBhdGgpCiAgICAgICAgZWxzZToK
ICAgICAgICAgICAgb3MuY2hkaXIob3MucGF0aC5leHBhbmR1c2VyKCd+JykpCgogICAgZGVmIGJfd
2hpY2goc2VsZiwgcHJvZ3JhbSwgcGF0aHM9Tm9uZSk6CiAgICAgICAgcmV0dXJuIHdoaWNoKHByb2
dyYW0sIHBhdGhzKQoKCmNsYXNzIENvbnRyaWIoTW9kdWxlVHlwZSk6ICMgcHJhZ21hOiBubyBjb3Z
lcgogICAgQGNsYXNzbWV0aG9kCiAgICBkZWYgX19jYWxsX18oY2xzLCBuYW1lKToKICAgICAgICBk
ZWYgd3JhcHBlcjEoZm4pOgoKICAgICAgICAgICAgQHByb3BlcnR5CiAgICAgICAgICAgIGRlZiBjb
WRfZ2V0dGVyKHNlbGYpOgogICAgICAgICAgICAgICAgY21kID0gcmVzb2x2ZV9jb21tYW5kKG5hbW
UpCgogICAgICAgICAgICAgICAgaWYgbm90IGNtZDoKICAgICAgICAgICAgICAgICAgICByYWlzZSB
Db21tYW5kTm90Rm91bmQobmFtZSkKCiAgICAgICAgICAgICAgICBuZXdfY21kID0gZm4oY21kKQog
ICAgICAgICAgICAgICAgcmV0dXJuIG5ld19jbWQKCiAgICAgICAgICAgIHNldGF0dHIoY2xzLCBuY
W1lLCBjbWRfZ2V0dGVyKQogICAgICAgICAgICByZXR1cm4gZm4KCiAgICAgICAgcmV0dXJuIHdyYX
BwZXIxCgoKbW9kX25hbWUgPSBfX25hbWVfXyArICIuY29udHJpYiIKY29udHJpYiA9IENvbnRyaWI
obW9kX25hbWUpCnN5cy5tb2R1bGVzW21vZF9uYW1lXSA9IGNvbnRyaWIKCgpAY29udHJpYigiZ2l0
IikKZGVmIGdpdChvcmlnKTogIyBwcmFnbWE6IG5vIGNvdmVyCiAgICAiIiIgbW9zdCBnaXQgY29tb
WFuZHMgcGxheSBuaWNlciB3aXRob3V0IGEgVFRZICIiIgogICAgY21kID0gb3JpZy5iYWtlKF90dH
lfb3V0PUZhbHNlKQogICAgcmV0dXJuIGNtZAoKQGNvbnRyaWIoInN1ZG8iKQpkZWYgc3Vkbyhvcml
nKTogIyBwcmFnbWE6IG5vIGNvdmVyCiAgICAiIiIgYSBuaWNlciB2ZXJzaW9uIG9mIHN1ZG8gdGhh
dCB1c2VzIGdldHBhc3MgdG8gYXNrIGZvciBhIHBhc3N3b3JkLCBvcgogICAgYWxsb3dzIHRoZSBma
XJzdCBhcmd1bWVudCB0byBiZSBhIHN0cmluZyBwYXNzd29yZCAiIiIKCiAgICBwcm9tcHQgPSAiW3
N1ZG9dIHBhc3N3b3JkIGZvciAlczogIiAlIGdldHBhc3MuZ2V0dXNlcigpCgogICAgZGVmIHN0ZGl
uKCk6CiAgICAgICAgcHcgPSBnZXRwYXNzLmdldHBhc3MocHJvbXB0PXByb21wdCkgKyAiXG4iCiAg
ICAgICAgeWllbGQgcHcKCgogICAgZGVmIHByb2Nlc3MoYXJncywga3dhcmdzKToKICAgICAgICBwY
XNzd29yZCA9IGt3YXJncy5wb3AoInBhc3N3b3JkIiwgTm9uZSkKCiAgICAgICAgaWYgcGFzc3dvcm
QgaXMgTm9uZToKICAgICAgICAgICAgcGFzc19nZXR0ZXIgPSBzdGRpbigpCiAgICAgICAgZWxzZTo
KICAgICAgICAgICAgcGFzc19nZXR0ZXIgPSBwYXNzd29yZC5yc3RyaXAoIlxuIikgKyAiXG4iCgog
ICAgICAgIGt3YXJnc1siX2luIl0gPSBwYXNzX2dldHRlcgogICAgICAgIHJldHVybiBhcmdzLCBrd
2FyZ3MKCiAgICBjbWQgPSBvcmlnLmJha2UoIi1TIiwgX2FyZ19wcmVwcm9jZXNzPXByb2Nlc3MpCi
AgICByZXR1cm4gY21kCgoKCgpkZWYgcnVuX3JlcGwoZW52KTogIyBwcmFnbWE6IG5vIGNvdmVyCiA
gICBiYW5uZXIgPSAiXG4+PiBzaCB2e3ZlcnNpb259XG4+PiBodHRwczovL2dpdGh1Yi5jb20vYW1v
ZmZhdC9zaFxuIgoKICAgIHByaW50KGJhbm5lci5mb3JtYXQodmVyc2lvbj1fX3ZlcnNpb25fXykpC
iAgICB3aGlsZSBUcnVlOgogICAgICAgIHRyeToKICAgICAgICAgICAgbGluZSA9IHJhd19pbnB1dC
gic2g+ICIpCiAgICAgICAgZXhjZXB0IChWYWx1ZUVycm9yLCBFT0ZFcnJvcik6CiAgICAgICAgICA
gIGJyZWFrCgogICAgICAgIHRyeToKICAgICAgICAgICAgZXhlYyhjb21waWxlKGxpbmUsICI8ZHVt
bXk+IiwgInNpbmdsZSIpLCBlbnYsIGVudikKICAgICAgICBleGNlcHQgU3lzdGVtRXhpdDoKICAgI
CAgICAgICAgYnJlYWsKICAgICAgICBleGNlcHQ6CiAgICAgICAgICAgIHByaW50KHRyYWNlYmFjay
5mb3JtYXRfZXhjKCkpCgogICAgIyBjbGVhbnMgdXAgb3VyIGxhc3QgbGluZQogICAgcHJpbnQoIiI
pCgoKCgojIHRoaXMgaXMgYSB0aGluIHdyYXBwZXIgYXJvdW5kIFRISVMgbW9kdWxlICh3ZSBwYXRj
aCBzeXMubW9kdWxlc1tfX25hbWVfX10pLgojIHRoaXMgaXMgaW4gdGhlIGNhc2UgdGhhdCB0aGUgd
XNlciBkb2VzIGEgImZyb20gc2ggaW1wb3J0IHdoYXRldmVyIgojIGluIG90aGVyIHdvcmRzLCB0aG
V5IG9ubHkgd2FudCB0byBpbXBvcnQgY2VydGFpbiBwcm9ncmFtcywgbm90IHRoZSB3aG9sZQojIHN
5c3RlbSBQQVRIIHdvcnRoIG9mIGNvbW1hbmRzLiAgaW4gdGhpcyBjYXNlLCB3ZSBqdXN0IHByb3h5
IHRoZQojIGltcG9ydCBsb29rdXAgdG8gb3VyIEVudmlyb25tZW50IGNsYXNzCmNsYXNzIFNlbGZXc
mFwcGVyKE1vZHVsZVR5cGUpOgogICAgZGVmIF9faW5pdF9fKHNlbGYsIHNlbGZfbW9kdWxlLCBiYW
tlZF9hcmdzPXt9KToKICAgICAgICAjIHRoaXMgaXMgc3VwZXIgdWdseSB0byBoYXZlIHRvIGNvcHk
gYXR0cmlidXRlcyBsaWtlIHRoaXMsCiAgICAgICAgIyBidXQgaXQgc2VlbXMgdG8gYmUgdGhlIG9u
bHkgd2F5IHRvIG1ha2UgcmVsb2FkKCkgYmVoYXZlCiAgICAgICAgIyBuaWNlbHkuICBpZiBpIG1ha
2UgdGhlc2UgYXR0cmlidXRlcyBkeW5hbWljIGxvb2t1cHMgaW4KICAgICAgICAjIF9fZ2V0YXR0cl
9fLCByZWxvYWQgc29tZXRpbWVzIGNob2tlcyBpbiB3ZWlyZCB3YXlzLi4uCiAgICAgICAgZm9yIGF
0dHIgaW4gWyJfX2J1aWx0aW5zX18iLCAiX19kb2NfXyIsICJfX2ZpbGVfXyIsICJfX25hbWVfXyIs
ICJfX3BhY2thZ2VfXyJdOgogICAgICAgICAgICBzZXRhdHRyKHNlbGYsIGF0dHIsIGdldGF0dHIoc
2VsZl9tb2R1bGUsIGF0dHIsIE5vbmUpKQoKICAgICAgICAjIHB5dGhvbiAzLjIgKDIuNyBhbmQgMy
4zIHdvcmsgZmluZSkgYnJlYWtzIG9uIG9zeCAobm90IHVidW50dSkKICAgICAgICAjIGlmIHdlIHN
ldCB0aGlzIHRvIE5vbmUuICBhbmQgMy4zIG5lZWRzIGEgdmFsdWUgZm9yIF9fcGF0aF9fCiAgICAg
ICAgc2VsZi5fX3BhdGhfXyA9IFtdCiAgICAgICAgc2VsZi5fX3NlbGZfbW9kdWxlID0gc2VsZl9tb
2R1bGUKICAgICAgICBzZWxmLl9fZW52ID0gRW52aXJvbm1lbnQoZ2xvYmFscygpLCBiYWtlZF9hcm
dzPWJha2VkX2FyZ3MpCgogICAgZGVmIF9fZ2V0YXR0cl9fKHNlbGYsIG5hbWUpOgogICAgICAgIHJ
ldHVybiBzZWxmLl9fZW52W25hbWVdCgogICAgZGVmIF9fY2FsbF9fKHNlbGYsICoqa3dhcmdzKToK
ICAgICAgICAiIiIgcmV0dXJucyBhIG5ldyBTZWxmV3JhcHBlciBvYmplY3QsIHdoZXJlIGFsbCBjb
21tYW5kcyBzcGF3bmVkIGZyb20gaXQKICAgICAgICBoYXZlIHRoZSBiYWtlZF9hcmdzIGt3YXJncy
BzZXQgb24gdGhlbSBieSBkZWZhdWx0ICIiIgogICAgICAgIGJha2VkX2FyZ3MgPSBzZWxmLl9fZW5
2LmJha2VkX2FyZ3MuY29weSgpCiAgICAgICAgYmFrZWRfYXJncy51cGRhdGUoa3dhcmdzKQogICAg
ICAgIG5ld19tb2QgPSBzZWxmLl9fY2xhc3NfXyhzZWxmLl9fc2VsZl9tb2R1bGUsIGJha2VkX2FyZ
3MpCgogICAgICAgICMgaW5zcGVjdCB0aGUgbGluZSBpbiB0aGUgcGFyZW50IGZyYW1lIHRoYXQgY2
FsbHMgYW5kIGFzc2lnbnMgdGhlIG5ldyBzaAogICAgICAgICMgdmFyaWFibGUsIGFuZCBnZXQgdGh
lIG5hbWUgb2YgdGhlIG5ldyB2YXJpYWJsZSB3ZSdyZSBhc3NpZ25pbmcgdG8uCiAgICAgICAgIyB0
aGlzIGlzIHZlcnkgYnJpdHRsZSBhbmQgcHJldHR5IG11Y2ggYSBzaW4uICBidXQgaXQgd29ya3Mga
W4gOTklIG9mCiAgICAgICAgIyB0aGUgdGltZSBhbmQgdGhlIHRlc3RzIHBhc3MKICAgICAgICAjCi
AgICAgICAgIyB0aGUgcmVhc29uIHdlIG5lZWQgdG8gZG8gdGhpcyBpcyBiZWNhdXNlIHdlIG5lZWQ
gdG8gcmVtb3ZlIHRoZSBvbGQKICAgICAgICAjIGNhY2hlZCBtb2R1bGUgZnJvbSBzeXMubW9kdWxl
cy4gIGlmIHdlIGRvbid0LCBpdCBnZXRzIHJlLXVzZWQsIGFuZCBhbnkKICAgICAgICAjIG9sZCBiY
WtlZCBwYXJhbXMgZ2V0IHVzZWQsIHdoaWNoIGlzIG5vdCB3aGF0IHdlIHdhbnQKICAgICAgICBwYX
JlbnQgPSBpbnNwZWN0LnN0YWNrKClbMV0KICAgICAgICBjb2RlID0gcGFyZW50WzRdWzBdLnN0cml
wKCkKICAgICAgICBwYXJzZWQgPSBhc3QucGFyc2UoY29kZSkKICAgICAgICBtb2R1bGVfbmFtZSA9
IHBhcnNlZC5ib2R5WzBdLnRhcmdldHNbMF0uaWQKCiAgICAgICAgaWYgbW9kdWxlX25hbWUgPT0gX
19uYW1lX186CiAgICAgICAgICAgIHJhaXNlIFJ1bnRpbWVFcnJvcigiQ2Fubm90IHVzZSB0aGUgbm
FtZSAnc2gnIGFzIGFuIGV4ZWN1dGlvbiBjb250ZXh0IikKCiAgICAgICAgc3lzLm1vZHVsZXMucG9
wKG1vZHVsZV9uYW1lLCBOb25lKQoKICAgICAgICByZXR1cm4gbmV3X21vZAoKCmRlZiBpbl9pbXBv
cnRsaWIoZnJhbWUpOgogICAgIiIiIGhlbHBlciBmb3IgY2hlY2tpbmcgaWYgYSBmaWxlbmFtZSBpc
yBpbiBpbXBvcnRsaWIgZ3V0cyAiIiIKICAgIHJldHVybiBmcmFtZS5mX2NvZGUuY29fZmlsZW5hbW
UgPT0gIjxmcm96ZW4gaW1wb3J0bGliLl9ib290c3RyYXA+IgoKCmRlZiByZWdpc3Rlcl9pbXBvcnR
lcigpOgogICAgIiIiIHJlZ2lzdGVycyBvdXIgZmFuY3kgaW1wb3J0ZXIgdGhhdCBjYW4gbGV0IHVz
IGltcG9ydCBmcm9tIGEgbW9kdWxlIG5hbWUsCiAgICBsaWtlOgoKICAgICAgICBpbXBvcnQgc2gKI
CAgICAgICB0bXAgPSBzaCgpCiAgICAgICAgZnJvbSB0bXAgaW1wb3J0IGxzCiAgICAiIiIKCiAgIC
BkZWYgdGVzdChpbXBvcnRlcik6CiAgICAgICAgcmV0dXJuIGltcG9ydGVyLl9fY2xhc3NfXy5fX25
hbWVfXyA9PSBNb2R1bGVJbXBvcnRlckZyb21WYXJpYWJsZXMuX19uYW1lX18KICAgIGFscmVhZHlf
cmVnaXN0ZXJlZCA9IGFueShbVHJ1ZSBmb3IgaSBpbiBzeXMubWV0YV9wYXRoIGlmIHRlc3QoaSldK
QoKICAgIGlmIG5vdCBhbHJlYWR5X3JlZ2lzdGVyZWQ6CiAgICAgICAgaW1wb3J0ZXIgPSBNb2R1bG
VJbXBvcnRlckZyb21WYXJpYWJsZXMoCiAgICAgICAgICAgIHJlc3RyaWN0X3RvPVsiU2VsZldyYXB
wZXIiXSwKICAgICAgICApCiAgICAgICAgc3lzLm1ldGFfcGF0aC5pbnNlcnQoMCwgaW1wb3J0ZXIp
CgogICAgcmV0dXJuIG5vdCBhbHJlYWR5X3JlZ2lzdGVyZWQKCmRlZiBmZXRjaF9tb2R1bGVfZnJvb
V9mcmFtZShuYW1lLCBmcmFtZSk6CiAgICBtb2QgPSBmcmFtZS5mX2xvY2Fscy5nZXQobmFtZSwgZn
JhbWUuZl9nbG9iYWxzLmdldChuYW1lLCBOb25lKSkKICAgIHJldHVybiBtb2QKCmNsYXNzIE1vZHV
sZUltcG9ydGVyRnJvbVZhcmlhYmxlcyhvYmplY3QpOgogICAgIiIiIGEgZmFuY3kgaW1wb3J0ZXIg
dGhhdCBhbGxvd3MgdXMgdG8gaW1wb3J0IGZyb20gYSB2YXJpYWJsZSB0aGF0IHdhcwogICAgcmVjZ
W50bHkgc2V0IGluIGVpdGhlciB0aGUgbG9jYWwgb3IgZ2xvYmFsIHNjb3BlLCBsaWtlIHRoaXM6Cg
ogICAgICAgIHNoMiA9IHNoKF90aW1lb3V0PTMpCiAgICAgICAgZnJvbSBzaDIgaW1wb3J0IGxzCiA
gICAKICAgICIiIgoKICAgIGRlZiBfX2luaXRfXyhzZWxmLCByZXN0cmljdF90bz1Ob25lKToKICAg
ICAgICBzZWxmLnJlc3RyaWN0X3RvID0gc2V0KHJlc3RyaWN0X3RvIG9yIHNldCgpKQoKCiAgICBkZ
WYgZmluZF9tb2R1bGUoc2VsZiwgbW9kX2Z1bGxuYW1lLCBwYXRoPU5vbmUpOgogICAgICAgICIiIi
Btb2RfZnVsbG5hbWUgZG91YmxlcyBhcyB0aGUgbmFtZSBvZiB0aGUgVkFSSUFCTEUgaG9sZGluZyB
vdXIgbmV3IHNoCiAgICAgICAgY29udGV4dC4gIGZvciBleGFtcGxlOgoKICAgICAgICAgICAgZGVy
cCA9IHNoKCkKICAgICAgICAgICAgZnJvbSBkZXJwIGltcG9ydCBscwoKICAgICAgICBoZXJlLCBtb
2RfZnVsbG5hbWUgd2lsbCBiZSAiZGVycCIuICBrZWVwIHRoYXQgaW4gbWluZCBhcyB3ZSBnbyB0aH
JvdWcKICAgICAgICB0aGUgcmVzdCBvZiB0aGlzIGZ1bmN0aW9uICIiIgoKICAgICAgICBwYXJlbnR
fZnJhbWUgPSBpbnNwZWN0LmN1cnJlbnRmcmFtZSgpLmZfYmFjawogICAgICAgIHdoaWxlIGluX2lt
cG9ydGxpYihwYXJlbnRfZnJhbWUpOgogICAgICAgICAgICBwYXJlbnRfZnJhbWUgPSBwYXJlbnRfZ
nJhbWUuZl9iYWNrCgogICAgICAgICMgdGhpcyBsaW5lIGlzIHNheWluZyAiaGV5LCBkb2VzIG1vZF
9mdWxsbmFtZSBleGlzdCBhcyBhIG5hbWUgd2UndmUKICAgICAgICAjIGRlZmluZCBwcmV2aW91c2x
5PyIgIHRoZSBwdXJwb3NlIG9mIHRoaXMgaXMgdG8gZW5zdXJlIHRoYXQKICAgICAgICAjIG1vZF9m
dWxsbmFtZSBpcyByZWFsbHkgYSB0aGluZyB3ZSd2ZSBkZWZpbmVkLiAgaWYgd2UgaGF2ZW4ndCBkZ
WZpbmVkCiAgICAgICAgIyBpdCBiZWZvcmUsIHRoZW4gd2UgImNhbid0IiBpbXBvcnQgZnJvbSBpdA
ogICAgICAgIG1vZHVsZSA9IGZldGNoX21vZHVsZV9mcm9tX2ZyYW1lKG1vZF9mdWxsbmFtZSwgcGF
yZW50X2ZyYW1lKQogICAgICAgIGlmIG5vdCBtb2R1bGU6CiAgICAgICAgICAgIHJldHVybiBOb25l
CgogICAgICAgICMgbWFrZSBzdXJlIGl0J3MgYSBjbGFzcyB3ZSdyZSBhbGxvd2VkIHRvIGltcG9yd
CBmcm9tCiAgICAgICAgaWYgbW9kdWxlLl9fY2xhc3NfXy5fX25hbWVfXyBub3QgaW4gc2VsZi5yZX
N0cmljdF90bzoKICAgICAgICAgICAgcmV0dXJuIE5vbmUKCiAgICAgICAgcmV0dXJuIHNlbGYKCgo
gICAgZGVmIGxvYWRfbW9kdWxlKHNlbGYsIG1vZF9mdWxsbmFtZSk6CiAgICAgICAgcGFyZW50X2Zy
YW1lID0gaW5zcGVjdC5jdXJyZW50ZnJhbWUoKS5mX2JhY2sKCiAgICAgICAgd2hpbGUgaW5faW1wb
3J0bGliKHBhcmVudF9mcmFtZSk6CiAgICAgICAgICAgIHBhcmVudF9mcmFtZSA9IHBhcmVudF9mcm
FtZS5mX2JhY2sKCiAgICAgICAgbW9kdWxlID0gZmV0Y2hfbW9kdWxlX2Zyb21fZnJhbWUobW9kX2Z
1bGxuYW1lLCBwYXJlbnRfZnJhbWUpCgogICAgICAgICMgd2UgSEFWRSB0byBpbmNsdWRlIHRoZSBt
b2R1bGUgaW4gc3lzLm1vZHVsZXMsIHBlciB0aGUgaW1wb3J0IFBFUC4KICAgICAgICAjIG9sZGVyI
HZlcmlvbnMgb2YgcHl0aG9uIHdlcmUgbW9yZSBsZW5pZW50IGFib3V0IHRoaXMgYmVpbmcgc2V0LC
BidXQKICAgICAgICAjIG5vdCBpbiA+PSBweXRob24zLjMsIHVuZm9ydHVuYXRlbHkuICB0aGlzIHJ
lcXVpcmVtZW50IG5lY2Vzc2l0YXRlcyB0aGUKICAgICAgICAjIHVnbHkgY29kZSBpbiBTZWxmV3Jh
cHBlci5fX2NhbGxfXwogICAgICAgIHN5cy5tb2R1bGVzW21vZF9mdWxsbmFtZV0gPSBtb2R1bGUKI
CAgICAgICBtb2R1bGUuX19sb2FkZXJfXyA9IHNlbGYKCiAgICAgICAgcmV0dXJuIG1vZHVsZQoKCm
RlZiBydW5fdGVzdHMoZW52LCBsb2NhbGUsIGFyZ3MsIHZlcnNpb24sIGZvcmNlX3NlbGVjdCwgKip
leHRyYV9lbnYpOiAjIHByYWdtYTogbm8gY292ZXIKICAgIHB5X3ZlcnNpb24gPSAicHl0aG9uIgog
ICAgcHlfdmVyc2lvbiArPSBzdHIodmVyc2lvbikKCiAgICBweV9iaW4gPSB3aGljaChweV92ZXJza
W9uKQogICAgcmV0dXJuX2NvZGUgPSBOb25lCgogICAgcG9sbGVyID0gInBvbGwiCiAgICBpZiBmb3
JjZV9zZWxlY3Q6CiAgICAgICAgcG9sbGVyID0gInNlbGVjdCIKCiAgICBpZiBweV9iaW46CiAgICA
gICAgcHJpbnQoIlRlc3RpbmcgJXMsIGxvY2FsZSAlciwgcG9sbGVyOiAlcyIgJSAocHlfdmVyc2lv
bi5jYXBpdGFsaXplKCksCiAgICAgICAgICAgIGxvY2FsZSwgcG9sbGVyKSkKCiAgICAgICAgZW52W
yJTSF9URVNUU19VU0VfU0VMRUNUIl0gPSBzdHIoaW50KGZvcmNlX3NlbGVjdCkpCiAgICAgICAgZW
52WyJMQU5HIl0gPSBsb2NhbGUKCiAgICAgICAgZm9yIGssdiBpbiBleHRyYV9lbnYuaXRlbXMoKTo
KICAgICAgICAgICAgZW52W2tdID0gc3RyKHYpCgogICAgICAgIGNtZCA9IFtweV9iaW4sICItVyIs
ICJpZ25vcmUiLCBvcy5wYXRoLmpvaW4oVEhJU19ESVIsICJ0ZXN0LnB5IildICsgYXJnc1sxOl0KI
CAgICAgICBsYXVuY2ggPSBsYW1iZGE6IG9zLnNwYXdudmUob3MuUF9XQUlULCBjbWRbMF0sIGNtZC
wgZW52KQogICAgICAgIHJldHVybl9jb2RlID0gbGF1bmNoKCkKCiAgICByZXR1cm4gcmV0dXJuX2N
vZGUKCgoKIyB3ZSdyZSBiZWluZyBydW4gYXMgYSBzdGFuZC1hbG9uZSBzY3JpcHQKaWYgX19uYW1l
X18gPT0gIl9fbWFpbl9fIjogIyBwcmFnbWE6IG5vIGNvdmVyCiAgICBkZWYgcGFyc2VfYXJncygpO
gogICAgICAgIGZyb20gb3B0cGFyc2UgaW1wb3J0IE9wdGlvblBhcnNlcgoKICAgICAgICBwYXJzZX
IgPSBPcHRpb25QYXJzZXIoKQogICAgICAgIHBhcnNlci5hZGRfb3B0aW9uKCItZSIsICItLWVudnM
iLCBkZXN0PSJlbnZzIiwgYWN0aW9uPSJhcHBlbmQiKQogICAgICAgIHBhcnNlci5hZGRfb3B0aW9u
KCItbCIsICItLWxvY2FsZXMiLCBkZXN0PSJjb25zdHJhaW5fbG9jYWxlcyIsIGFjdGlvbj0iYXBwZ
W5kIikKICAgICAgICBvcHRpb25zLCBhcmdzID0gcGFyc2VyLnBhcnNlX2FyZ3MoKQoKICAgICAgIC
BlbnZzID0gb3B0aW9ucy5lbnZzIG9yIFtdCiAgICAgICAgY29uc3RyYWluX2xvY2FsZXMgPSBvcHR
pb25zLmNvbnN0cmFpbl9sb2NhbGVzIG9yIFtdCgogICAgICAgIHJldHVybiBhcmdzLCBlbnZzLCBj
b25zdHJhaW5fbG9jYWxlcwoKICAgICMgdGhlc2UgYXJlIGVzc2VudGlhbGx5IHJlc3RyaWN0aW9uc
yBvbiB3aGF0IGVudnMvY29uc3RyYWluX2xvY2FsZXMgdG8gcmVzdHJpY3QgdG8gZm9yCiAgICAjIH
RoZSB0ZXN0cy4gIGlmIHRoZXkncmUgZW1wdHkgbGlzdHMsIGl0IG1lYW5zIHVzZSBhbGwgYXZhaWx
hYmxlCiAgICBhcmdzLCBjb25zdHJhaW5fdmVyc2lvbnMsIGNvbnN0cmFpbl9sb2NhbGVzID0gcGFy
c2VfYXJncygpCiAgICBhY3Rpb24gPSBOb25lCiAgICBpZiBhcmdzOgogICAgICAgIGFjdGlvbiA9I
GFyZ3NbMF0KCiAgICBpZiBhY3Rpb24gaW4gKCJ0ZXN0IiwgInRyYXZpcyIpOgogICAgICAgIGltcG
9ydCB0ZXN0CiAgICAgICAgY292ZXJhZ2UgPSBOb25lCiAgICAgICAgaWYgdGVzdC5IQVNfVU5JQ09
ERV9MSVRFUkFMOgogICAgICAgICAgICBpbXBvcnQgY292ZXJhZ2UKCiAgICAgICAgZW52ID0gb3Mu
ZW52aXJvbi5jb3B5KCkKICAgICAgICBlbnZbIlNIX1RFU1RTX1JVTk5JTkciXSA9ICIxIgogICAgI
CAgIGlmIGNvdmVyYWdlOgogICAgICAgICAgICB0ZXN0LmFwcGVuZF9tb2R1bGVfcGF0aChlbnYsIG
NvdmVyYWdlKQoKICAgICAgICAjIGlmIHdlJ3JlIHRlc3RpbmcgbG9jYWxseSwgcnVuIGFsbCB2ZXJ
zaW9ucyBvZiBweXRob24gb24gdGhlIHN5c3RlbQogICAgICAgIGlmIGFjdGlvbiA9PSAidGVzdCI6
CiAgICAgICAgICAgIGFsbF92ZXJzaW9ucyA9ICgiMi42IiwgIjIuNyIsICIzLjEiLCAiMy4yIiwgI
jMuMyIsICIzLjQiLCAiMy41IiwgIjMuNiIpCgogICAgICAgICMgaWYgd2UncmUgdGVzdGluZyBvbi
B0cmF2aXMsIGp1c3QgdXNlIHRoZSBzeXN0ZW0ncyBkZWZhdWx0IHB5dGhvbiwKICAgICAgICAjIHN
pbmNlIHRyYXZpcyB3aWxsIHNwYXduIGEgdm0gcGVyIHB5dGhvbiB2ZXJzaW9uIGluIG91ciAudHJh
dmlzLnltbAogICAgICAgICMgZmlsZQogICAgICAgIGVsaWYgYWN0aW9uID09ICJ0cmF2aXMiOgogI
CAgICAgICAgICB2ID0gc3lzLnZlcnNpb25faW5mbwogICAgICAgICAgICBzeXNfdmVyID0gIiVkLi
VkIiAlICh2WzBdLCB2WzFdKQogICAgICAgICAgICBhbGxfdmVyc2lvbnMgPSAoc3lzX3ZlciwpCgo
gICAgICAgIGFsbF9mb3JjZV9zZWxlY3QgPSBbVHJ1ZV0KICAgICAgICBpZiBIQVNfUE9MTDoKICAg
ICAgICAgICAgYWxsX2ZvcmNlX3NlbGVjdC5hcHBlbmQoRmFsc2UpCgogICAgICAgIGFsbF9sb2Nhb
GVzID0gKCJlbl9VUy5VVEYtOCIsICJDIikKICAgICAgICBpID0gMAogICAgICAgIGZvciBsb2NhbG
UgaW4gYWxsX2xvY2FsZXM6CiAgICAgICAgICAgIGlmIGNvbnN0cmFpbl9sb2NhbGVzIGFuZCBsb2N
hbGUgbm90IGluIGNvbnN0cmFpbl9sb2NhbGVzOgogICAgICAgICAgICAgICAgY29udGludWUKCiAg
ICAgICAgICAgIGZvciB2ZXJzaW9uIGluIGFsbF92ZXJzaW9uczoKICAgICAgICAgICAgICAgIGlmI
GNvbnN0cmFpbl92ZXJzaW9ucyBhbmQgdmVyc2lvbiBub3QgaW4gY29uc3RyYWluX3ZlcnNpb25zOg
ogICAgICAgICAgICAgICAgICAgIGNvbnRpbnVlCgogICAgICAgICAgICAgICAgZm9yIGZvcmNlX3N
lbGVjdCBpbiBhbGxfZm9yY2Vfc2VsZWN0OgogICAgICAgICAgICAgICAgICAgIGVudl9jb3B5ID0g
ZW52LmNvcHkoKQoKICAgICAgICAgICAgICAgICAgICBleGl0X2NvZGUgPSBydW5fdGVzdHMoZW52X
2NvcHksIGxvY2FsZSwgYXJncywgdmVyc2lvbiwKICAgICAgICAgICAgICAgICAgICAgICAgICAgIG
ZvcmNlX3NlbGVjdCwgU0hfVEVTVF9SVU5fSURYPWkpCgogICAgICAgICAgICAgICAgICAgIGlmIGV
4aXRfY29kZSBpcyBOb25lOgogICAgICAgICAgICAgICAgICAgICAgICBwcmludCgiQ291bGRuJ3Qg
ZmluZCAlcywgc2tpcHBpbmciICUgdmVyc2lvbikKCiAgICAgICAgICAgICAgICAgICAgZWxpZiBle
Gl0X2NvZGUgIT0gMDoKICAgICAgICAgICAgICAgICAgICAgICAgcHJpbnQoIkZhaWxlZCBmb3IgJX
MsICVzIiAlICh2ZXJzaW9uLCBsb2NhbGUpKQogICAgICAgICAgICAgICAgICAgICAgICBleGl0KDE
pCgogICAgICAgICAgICAgICAgICAgIGkgKz0gMQoKICAgICAgICByYW5fdmVyc2lvbnMgPSAiLCIu
am9pbihhbGxfdmVyc2lvbnMpCiAgICAgICAgcHJpbnQoIlRlc3RlZCBQeXRob24gdmVyc2lvbnM6I
CVzIiAlIHJhbl92ZXJzaW9ucykKCiAgICBlbHNlOgogICAgICAgIGVudiA9IEVudmlyb25tZW50KG
dsb2JhbHMoKSkKICAgICAgICBydW5fcmVwbChlbnYpCgojIHdlJ3JlIGJlaW5nIGltcG9ydGVkIGZ
yb20gc29tZXdoZXJlCmVsc2U6CiAgICBzZWxmID0gc3lzLm1vZHVsZXNbX19uYW1lX19dCiAgICBz
eXMubW9kdWxlc1tfX25hbWVfX10gPSBTZWxmV3JhcHBlcihzZWxmKQogICAgcmVnaXN0ZXJfaW1wb
3J0ZXIoKQoK"""


try:
    import sh
except ImportError:
    with pathlib.Path("sh.py").open("w") as sh_fp:
        sh_fp.write(base64.b64decode(sh_py).decode())
    import sh


def log(*args, **kwargs):
    if STARTED:
        total_seconds = int(time.time() - STARTED)
        minutes = int(total_seconds / 60)
        seconds = total_seconds % 60
        print(f"{minutes: 3d}:{seconds:02d}", *args, **kwargs)
    else:
        print(*args, **kwargs)


def main(argv=None):
    """Run ghost using command line arguments."""
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers()
    spawn_p = commands.add_parser("spawn", help="spawn sudoer `ghost`")
    spawn_p.set_defaults(command="spawn")
    setup_p = commands.add_parser("setup", help="set up base system")
    setup_p.set_defaults(command="setup")
    setup_p.add_argument("digitalocean_token")
    do_p = commands.add_parser("digitalocean",
                               help="DigitalOcean hosting tools")
    do_p.set_defaults(command="digitalocean")
    do_p.add_argument("token")
    dd_p = commands.add_parser("dynadot", help="Dynadot registrar tools")
    dd_p.set_defaults(command="dynadot")
    dd_p.add_argument("token")

    if argv is None:
        argv = sys.argv[1:]
    args = parser.parse_args(argv)
    command = getattr(args, "command", "init")
    ghost = Ghost()
    if command == "init":
        print()
        print(LOGO)
        print()
        print("spawning a new presence..")
        name = input("presence name: ")
        digitalocean_token = getpass.getpass("digital ocean token: ")
        cli = DigitalOcean(digitalocean_token)
        key = get_key(cli)
        droplet = cli.create_droplet(name, size="1gb", ssh_keys=[key["id"]])
        print("generating droplet..")
        wait(cli, droplet["id"])
        droplet = cli.get_droplet(droplet["id"])
        for ip_details in droplet["networks"]["v4"]:
            if ip_details["type"] == "public":
                break
        ip_address = ip_details["ip_address"]
        print(f"machine initialized at: {ip_address}")
        command = "wget https://gh.ost.lol/ghost.py -q && python3 ghost.py"
        get_ssh("root", ip_address)(f"{command} spawn")
        get_ssh("ghost", ip_address)(f"{command} setup {digitalocean_token}")
    elif command == "spawn":
        ghost.spawn()
    elif command == "setup":
        ghost.setup(args.digitalocean_token)
    elif command == "clean":
        pass  # TODO remove files in src_dir and replace with {filename}.sha256
    elif command == "digitalocean":
        print(DigitalOcean(args.token).get_droplets())
    elif command == "dynadot":
        print(Dynadot(args.token).list_domain())
    else:
        print(f"Unknown command {command}")
        return 1
    return 0


if __name__ == "__main__":
    STARTED = time.time()
    sys.exit(main())
