## 治理文件(Governance Document)
wax社区对其项目治理使用[GD.1](https://github.com/wax-api/rfcs/blob/main/GD.1.md)流程

## 项目结构(Project Structure)
* `waxapi/rfcs`: RFC文档
* `waxapi/frontend`: 前端界面
* `waxapi/backend`: 后端接口
  * `reference`: openapi文档目录
  * `requirements.txt`: 依赖包列表
  * `config`: 默认配置目录。配置文件采用toml语法
  * `start.py`: 启动入口文件。启动命令是`python start.py`，可通过`python start.py --help`查看启动选项。
  * 数据库：PostgreSQL

## 贡献者
感谢所有wax的贡献者！
