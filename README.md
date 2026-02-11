# 我的Hugo博客

一个使用Hugo和Blowfish主题创建的精美个人博客。

## 特性

- 🎨 柔美的背景和优雅的手写字体
- ✨ 精美的界面设计
- 🎆 鼠标点击烟花波纹效果
- ⭐ 鼠标移动星星拖尾效果
- 🕸️ 动态蜘蛛网背景特效
- 🌓 亮色/暗色主题切换
- 📱 响应式布局
- 🎭 过场动画效果
- 📊 文章统计和分类

## 布局说明

- **顶部导航栏**: 包含logo、菜单和主题切换按钮
- **左侧边栏**: 作者头像、简介、统计信息、快捷链接
- **右侧边栏**: 随机文章、热门标签
- **中心内容区**: 文章列表和详情（2-3倍宽度）

## 快速开始

### 启动开发服务器

```bash
hugo server -D
```

访问 http://localhost:1313 查看博客

### 构建静态网站

```bash
hugo
```

生成的静态文件在 `public/` 目录

### 创建新文章

```bash
hugo new posts/your-post-name.md
```

## 配置文件

### 主配置文件

- `hugo.yml` - 站点主配置
- `config/_default/languages.zh.yml` - 语言配置
- `config/_default/menus.zh.yml` - 菜单配置
- `config/_default/params.yml` - 参数配置

### 自定义文件

- `static/css/custom.css` - 自定义样式
- `static/js/effects.js` - 烟花波纹和星星拖尾特效
- `static/js/spider.js` - 蜘蛛网特效
- `layouts/_default/` - 自定义布局模板

## 主题切换

点击顶部导航栏的"暗色/亮色"按钮切换主题

## 修改作者信息

编辑 `hugo.yml` 文件中的 `author` 部分：

```yaml
author:
  name: "你的名字"
  image: "/img/avatar.svg"
  bio: "你的简介"
  links:
    - name: "GitHub"
      icon: "fa-brands fa-github"
      url: "https://github.com/yourusername"
```

## 替换头像

将你的头像文件放到 `static/img/` 目录，并修改 `hugo.yml` 中的 `avatarURL` 路径

## 添加菜单项

编辑 `hugo.yml` 或 `config/_default/menus.zh.yml`：

```yaml
menu:
  main:
    - name: "菜单名"
      url: "/your-url/"
      weight: 数字
      pre: '<i class="fa-solid fa-icon"></i>'
```

## 创建分类和标签

在文章的front matter中添加：

```yaml
---
title: "文章标题"
categories: ["分类名"]
tags: ["标签1", "标签2"]
---
```

## Font Awesome图标

博客使用Font Awesome图标库，参考：https://fontawesome.com/icons

## 字体说明

- 标题字体：Dancing Script（手写字体）
- 正文字体：Handlee（手写字体）
- 其他字体：Patrick Hand、Indie Flower、Caveat

## 调整颜色

编辑 `static/css/custom.css` 中的 `:root` 部分：

```css
:root {
  --bg-primary: #faf9f6;      /* 主背景色 */
  --text-primary: #4a4a4a;    /* 主文本色 */
  --accent-color: #d4a574;    /* 强调色 */
  /* 更多颜色变量... */
}
```

## 部署

### GitHub Pages

1. 将代码推送到GitHub仓库
2. 在仓库设置中启用GitHub Pages
3. 选择 `gh-pages` 分支作为源

### 其他平台

将 `public/` 目录的内容部署到任何静态网站托管平台

## 资源链接

- Hugo官网: https://gohugo.io
- Blowfish主题: https://github.com/nunocoracao/blowfish
- Font Awesome: https://fontawesome.com
- Google Fonts: https://fonts.google.com

## 许可

MIT License
# fengkc.github.io
