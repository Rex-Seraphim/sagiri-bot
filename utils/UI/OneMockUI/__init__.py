import jinja2
from pathlib import Path

from utils.UI.models import *
from utils.html2pic import html_to_pic


env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        Path(__file__).parent
    ),
    enable_async=True,
    autoescape=True,
)


async def gen(form: GenForm) -> bytes:
    template = env.get_template("template.html")
    width = form.calc_body_width()
    html = await template.render_async(**(form.dict()))
    return await html_to_pic(html, wait=0, viewport={"width": width, "height": 1})


# example
"""
form = GenForm(
    columns=[
        Column(
            elements=[
                ColumnTitle(title="column1"),
                ColumnImage(src="src"),
                ColumnList(
                    rows=[
                        ColumnListItem(subtitle="子标题1", content="内容1", right_element=ColumnListItemSwitch(switch=False)),
                        ColumnListItem(subtitle="子标题2", content="内容2", right_element=ColumnListItemSwitch(switch=True)),
                        ColumnListItem(subtitle="子标题3", content="内容3")
                    ]
                ),
                ColumnUserInfo(
                    name="你好",
                    description="我是纱雾",
                    avatar="url"
                )
            ]
        ),
        Column(
            elements=[
                ColumnTitle(title="column2"),
                ColumnImage(src="src"),
                ColumnList(
                    rows=[
                        ColumnListItem(subtitle="子标题1", content="内容1", right_element=ColumnListItemSwitch(switch=False)),
                        ColumnListItem(subtitle="子标题2", content="内容2", right_element=ColumnListItemSwitch(switch=True)),
                        ColumnListItem(subtitle="子标题3", content="内容3")
                    ]
                ),
                ColumnUserInfo(
                    name="你好",
                    description="我是纱雾",
                    avatar="url"
                )
            ]
        )
    ]
)
image_bytes = await gen(form)
"""
