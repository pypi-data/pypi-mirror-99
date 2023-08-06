from pydantic import BaseModel, Field

from .wp import WPReadMe

__all__ = ["WPProject"]


class WPProject(BaseModel):
    name: str = Field(..., title="项目名称")
    revision: int = Field(..., title="当前版本")
    date: str = Field(..., title="更新时间")
    readme: WPReadMe = Field(..., title="ReadMe")
