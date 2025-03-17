# 寻仙模型查看器

## 介绍
**寻仙模型查看器**是一个基于 Vue3 和 Three.js 实现的 3D 模型查看工具。用户可以选择预设模型或上传 OBJ 格式模型并在页面中操作。

## 项目目录结构
```
|─backend
|   |─staticfiles
|   |   |─admin (Django 后台静态资源)
|   |   |─assets (CSS/JS 资源)
|   |   |─css
|   |   |─res
|   |─vercel_app (Django 应用源码)
|       |─static (web 前端静态文件)
|       |─templates (HTML 模板)
|─website (Vue3 前端项目)
|   |─dist (Vue 构建后文件)
|   |─node_modules
|   |─public
|   |─src (Vue 源码)
|       |─assets
|       |─components
|       |─router
|       |─style
```

## 使用技术
- **Vue 3** - 前端框架
- **TresJS (@tresjs/core)** - 基于 Three.js 的 Vue 3 3D 工具集
- **Three.js** - 3D 模型渲染库
- **Django** - 后端 API 服务
- **Vercel** - 部署服务

## 部署

### 1. 安装项目依赖

确保您已经安装 Node.js ，然后执行以下命令安装依赖：

```sh
cd website
npm install
```

### 2. 运行 Vue 前端

```sh
npm run dev
```

### 3. 运行 Django 后端

```sh
cd backend/vercel_app
python manage.py runserver
```

### 4. 构建项目

```sh
npm run build
```

## 功能介绍
- 📌 **预设模型选择** - 可以从 Django 提供的 API 列表中选择模型
- 📤 **上传 OBJ 模型** - 可以本地上传 .obj 格式文件
- 🎥 **模型查看与操作** - 支持模型旋转，拖动，缩放

## 操作指南
- 🔄 **按住左键** 旋转模型
- 🤏 **按住右键** 拖动模型
- 🔍 **滑动滚轮** 缩放模型

## 后端 API 配置

请确保 Django 运行并设置正确的静态文件目录：

```python
# settings.py
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]
```

## 项目贡献
欢迎各位开发者提供修正和优化建议，您可以 Fork 本项目并提交 Pull Request。

## 记录
- v1.0.0 - 初始发布，支持 OBJ 模型查看

## 版权声明
本项目遵循 MIT 协议。

