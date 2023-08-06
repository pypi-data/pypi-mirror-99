import pathlib

import jinja2


def build_webpages(template_dir: pathlib.Path, output_dir: pathlib.Path):
    """Create ancillary pages from templates and copy them to `output_dir`.
    :param template_dir: The path to load page templates from.
    :param output_dir: The path to output generated pages to."""

    template_loader = jinja2.FileSystemLoader(searchpath=template_dir)
    template_env = jinja2.Environment(loader=template_loader)

    template_paths = template_dir.glob("[!_]*.html")

    for path in template_paths:
        template_name = path.name
        jinja_template = template_env.get_template(template_name)
        rendered_page = jinja_template.render()

        with open(output_dir.absolute() / path.name, "w") as result_html:
            result_html.write(rendered_page)
