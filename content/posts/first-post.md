---
title: "Hugo博客搭建指南"
date: 2025-02-10T10:00:00+08:00
draft: false
author: "作者"
categories: ["技术"]
tags: ["Hugo", "博客", "教程"]
summary: "详细介绍如何使用Hugo搭建个人博客，包括安装、配置、主题选择等。"
---

# Hugo博客搭建指南

Hugo是一个快速、现代化的静态网站生成器，非常适合用来搭建个人博客。

## 安装Hugo

### Windows系统

1. 访问[Hugo官网](https://gohugo.io/)
2. 下载适合你系统的安装包
3. 运行安装程序

### 验证安装

打开命令行，输入：

```bash
hugo version
```

如果显示版本信息，说明安装成功。

## 创建新站点

```bash
hugo new site myblog
cd myblog
```

## 添加主题

Hugo有丰富的主题可选，我选择了Blowfish主题：

```bash
git submodule add https://github.com/nunocoracao/blowfish.git themes/blowfish
```

## 创建内容

```bash
hugo new posts/my-first-post.md
```

## 启动服务器

```bash
hugo server -D
```

访问 http://localhost:1313 查看你的博客！

## 总结

Hugo非常轻量级且功能强大，适合用来快速搭建个人博客。
