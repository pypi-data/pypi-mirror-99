"""Sphinx extension for showing the Doctr Versions Menu."""
import os
import shutil
import tempfile
from pathlib import Path

from sphinx.util.template import SphinxRenderer


class _JS(str):
    """Javascript code wrapper.

    The default ``doctr-versions-menu.jt_t`` template renders variables via
    their __repr__. Normal strings have a quoted __repr__, this :class:`JS`
    wrapper does not.
    """

    def __repr__(self):
        return self


def add_versions_menu_js_file(app):
    """Add doctr-versions-menu.js file as a static js file to Sphinx."""
    tmpdir = tempfile.mkdtemp()
    app.config._doctr_versions_menu_temp_dir = tmpdir
    js_file_name = 'doctr-versions-menu.js'
    template_path = [
        os.path.join(app.confdir, folder)
        for folder in app.config.templates_path
    ]
    template_path.append(str(Path(__file__).parent / '_template'))
    renderer = SphinxRenderer(template_path=template_path)
    context = dict(
        json_file=_JS(
            '"/" + window.location.pathname.split("/")[1] + "/versions.json"'
        ),
        github_project_url=_JS('getGithubProjectUrl()'),
        current_folder=_JS('getGhPagesCurrentFolder()'),
        badge_only=(app.config.html_theme != 'sphinx_rtd_theme'),
        menu_title="Doctr",
    )
    context.update(app.config.doctr_versions_menu_conf)
    js_file_path = Path(tmpdir) / js_file_name
    template_name = 'doctr-versions-menu.js_t'
    template = renderer.env.get_template(template_name)
    print(
        "creating %s from template %s for doctr-versions-menu"
        % (js_file_name, template.filename)
    )
    with js_file_path.open('w') as js_file:
        js_file.write(template.render(**context))
    app.config.html_static_path.append(tmpdir)
    app.add_js_file(js_file_name)
    if context['badge_only']:
        app.config.html_static_path.extend(
            [
                str(Path(__file__).parent / '_css'),
                str(Path(__file__).parent / '_fonts'),
            ]
        )
        app.add_css_file('badge_only.css')


def cleanup(app, exception):
    """Remove temporary files."""
    shutil.rmtree(app.config._doctr_versions_menu_temp_dir)
