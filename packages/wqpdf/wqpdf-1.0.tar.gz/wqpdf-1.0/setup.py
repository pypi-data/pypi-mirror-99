import setuptools
from pathlib import Path

setuptools.setup(
    name="wqpdf",
    version=1.0,
    long_description=Path("README.md").read_text(),
    # 'where':是要搜索包的根目录.'exclude'是要排除的包名序列.'include'是要包含的包名的序列
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
