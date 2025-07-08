# 解密软件守护与管理系统

## 项目简介
本项目是一套集“文件解密安全守护”、“加密文件管理”、“多用户权限控制”于一体的综合性系统。系统包含解密守护程序、简易解密工具、Web管理后台、数据库及相关自动化脚本，适用于需要对加密文件进行安全解密、分发、权限管理的场景。

## 系统组成
- **解密守护程序**：实时监控解密软件运行，防止内容泄露。
- **简易解密工具**：自动识别并解密特定格式的加密文件，支持设备绑定与一次性解密。
- **Web后端与管理后台**：提供文件上传、分发、权限、设备、用户、日志等管理功能。
- **数据库模型**：定义用户、文件、加密文件、设备、解密记录、通知等核心数据结构。
- **自动化脚本**：如初始化数据库、创建管理员、批量清理会话、文件验证修复等。
- **前端模板**：含dashboard、admin等管理页面。
- **静态资源**：前端样式与脚本。

## 目录结构说明
- `app.py`、`routes.py`、`models.py`：主后端逻辑
- `templates/`：前端页面模板
- `static/`：静态资源（JS、CSS、图片等）
- `uploads/`：用户上传及加密文件（已在.gitignore中，生产环境需手动创建）
- `utils/`、`extensions.py`：工具函数与扩展
- `migrations/`：数据库迁移脚本
- 各类脚本：如`init_db.py`、`create_admin.py`、`verify_encrypted_files.py`等
- `README.md`、`deployment_docs.md`：文档说明
- `requirements.txt`、`pyproject.toml`：依赖声明

## 安装与部署
### 依赖环境
- Python >= 3.11
- 推荐操作系统：Windows 10/11 或 Linux
- 依赖包详见 `requirements.txt` 或 `pyproject.toml`

### 安装步骤
1. 克隆本项目到本地：
   ```bash
   git clone <your-repo-url>
   cd <project-root>
   ```
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 初始化数据库及管理员：
   ```bash
   python init_db.py
   python create_admin.py
   ```
4. 启动Web服务：
   ```bash
   python app.py
   # 或
   gunicorn -c gunicorn_config.py main:app
   ```
5. （可选）打包解密工具/守护程序：
   ```bash
   python build_simple_decrypt_tool.py
   ```

### 部署注意事项
- 确保 `uploads/` 和 `uploads/encrypted/` 目录存在且权限正确。
- 数据库可用（默认sqlite，生产建议PostgreSQL，需配置DATABASE_URL）。
- 详细部署与常见问题见 `deployment_docs.md`。

## 无用文件清理建议
- **临时/历史目录**：`temp_repo/`、`feature_update/`、`dist/`（如无用可直接删除）
- **临时/备份文件**：`debug.log`、`dashboard_new.html`、`simple_decrypt_tool.py.bak`、`temp_edit.html`、`generated-icon.png`（如非正式logo）
- **平台相关文件**：`.replit`、`replit.nix`（仅Replit平台需要，其他环境可删）
- **临时代码片段**：`choices_fix.txt`（如无用可删）
- **虚拟环境和缓存**：`.venv/`、`__pycache__/`（建议在.gitignore中忽略）

> **删除前请做好备份，防止误删重要内容。**

## 常见问题与FAQ
- **Q: 解密工具提示设备未授权？**
  A: 将设备ID发送给管理员授权。
- **Q: 文件已被解密过无法再次解密？**
  A: 每个加密文件仅允许一次解密，需清理 `.sportsbet/decrypt_history.json` 后再试。
- **Q: Web端文件下载失败？**
  A: 检查 `uploads/` 目录权限、数据库记录与实际文件是否匹配，详见 `deployment_docs.md`。
- **Q: 守护程序未启动？**
  A: 请以管理员身份运行解密工具，确保杀毒软件未拦截。

## 安全注意事项
- 守护程序需管理员权限以终止进程。
- 文件、数据库、日志等敏感数据请妥善备份与保护。
- 生产环境建议使用HTTPS、强密码、定期审计日志。

## 维护与支持
- 如需定制开发、功能扩展或技术支持，请联系项目维护者。
- 详细部署、升级、迁移等请参考 `deployment_docs.md`。

---

如有疑问或建议，欢迎反馈！
