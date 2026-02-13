#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hugo 博客快速提交工具
支持：新建文章、新建分类、新建标签
"""

import os
import sys
import argparse
import subprocess
import json
from datetime import datetime
from pathlib import Path

# 尝试导入交互式界面库
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    console = None

# 配置
CONTENT_DIR = "content/posts"
CATEGORIES_DIR = "content/categories"
TAGS_DIR = "content/tags"
ARCHETYPE = "archetypes/default.md"
CONFIG_FILE = "hugo_cli_config.json"

# 默认配置
DEFAULT_CONFIG = {
    "auto_push": False,
    "commit_message": "Update: {type} - {name}"
}

# 加载配置
def load_config():
    """加载配置文件"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  配置文件加载失败，使用默认配置: {e}")
            return DEFAULT_CONFIG
    return DEFAULT_CONFIG

# 保存配置
def save_config(config):
    """保存配置文件"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"✅ 配置已保存到 {CONFIG_FILE}")
        return True
    except Exception as e:
        print(f"❌ 配置保存失败: {e}")
        return False

# 获取配置
def get_config():
    """获取配置，如果不存在则创建默认配置"""
    config = load_config()
    if not os.path.exists(CONFIG_FILE):
        save_config(config)
    return config


def slugify(text):
    """将中文转换为拼音或保持英文，用于文件名"""
    # 简单处理：保留中文、英文、数字，空格替换为-
    import re
    text = re.sub(r'[^\w\s\u4e00-\u9fff-]', '', text)
    text = re.sub(r'[\s]+', '-', text.strip())
    return text.lower()


def git_push(content_type, name):
    """推送到 GitHub"""
    config = get_config()

    if not config.get('auto_push', False):
        return True  # 未启用自动推送，跳过

    print(f"\n📤 正在推送到 GitHub...")

    try:
        # 添加所有更改
        result = subprocess.run(
            ["git", "add", "."],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8',
            errors='ignore'
        )
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Git add 失败: {e.stderr}")
        return False
    except FileNotFoundError:
        print("⚠️  未找到 git 命令")
        return False

    # 提交更改
    commit_msg = config.get('commit_message', 'Update: {type} - {name}').format(
        type=content_type,
        name=name
    )
    try:
        result = subprocess.run(
            ["git", "commit", "-m", commit_msg],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8',
            errors='ignore'
        )
        print(f"✅ Git 提交成功: {commit_msg}")
    except subprocess.CalledProcessError as e:
        # 可能是没有更改需要提交
        if "nothing to commit" in e.stderr.lower():
            print("ℹ️  没有新的更改需要提交")
            return True
        print(f"⚠️  Git 提交失败: {e.stderr}")
        return False
    except FileNotFoundError:
        print("⚠️  未找到 git 命令")
        return False

    # 推送到远程仓库
    try:
        result = subprocess.run(
            ["git", "push"],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8',
            errors='ignore'
        )
        print("✅ 推送到 GitHub 成功！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Git push 失败: {e.stderr}")
        return False
    except FileNotFoundError:
        print("⚠️  未找到 git 命令")
        return False


def run_hugo_new(path, kind=""):
    """运行 hugo new 命令"""
    cmd = ["hugo", "new", path]
    if kind:
        cmd.extend(["--kind", kind])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8', errors='ignore')
        print(f"✅ 创建成功: {path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 创建失败: {e.stderr}")
        return False
    except FileNotFoundError:
        print("❌ 错误: 未找到 hugo 命令，请确保 Hugo 已安装并添加到 PATH")
        return False


def new_post(title, categories=None, tags=None, draft=True):
    """创建新文章"""
    slug = slugify(title)
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{CONTENT_DIR}/{date_str}-{slug}.md"
    
    # 检查文件是否已存在
    if os.path.exists(filename):
        print(f"⚠️  文件已存在: {filename}")
        overwrite = input("是否覆盖? (y/N): ").lower()
        if overwrite != 'y':
            print("已取消")
            return False
    
    # 构建 front matter
    front_matter = f"""---
title: "{title}"
date: {datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")}
draft: {str(draft).lower()}
"""
    
    if categories:
        front_matter += f"categories:\n"
        for cat in categories:
            front_matter += f"  - {cat}\n"
    
    if tags:
        front_matter += f"tags:\n"
        for tag in tags:
            front_matter += f"  - {tag}\n"
    
    front_matter += """---

"""
    
    # 确保目录存在
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # 写入文件
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(front_matter)

    print(f"✅ 文章创建成功: {filename}")
    print(f"   标题: {title}")
    if categories:
        print(f"   分类: {', '.join(categories)}")
    if tags:
        print(f"   标签: {', '.join(tags)}")

    # 自动推送到 GitHub
    git_push("文章", title)

    return True


def new_category(name, description=""):
    """创建新分类"""
    slug = slugify(name)
    filename = f"{CATEGORIES_DIR}/{slug}/index.md"
    
    # 确保目录存在
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # 构建 front matter（仅包含标题和描述，不需要内容）
    content = f"""---
title: "{name}"
description: "{description or name}"
---

这里是标记为 **{name}** 的所有文章。
"""
    
    # 检查文件是否已存在
    if os.path.exists(filename):
        print(f"⚠️  分类已存在: {filename}")
        return False
    
    # 写入文件
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ 分类创建成功: {filename}")
    print(f"   名称: {name}")
    print(f"   提示: 分类文件在 content/categories/ 目录，不会影响 public/")

    # 自动推送到 GitHub
    git_push("分类", name)

    return True


def new_tag(name, description=""):
    """创建新标签"""
    slug = slugify(name)
    filename = f"{TAGS_DIR}/{slug}/index.md"
    
    # 确保目录存在
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # 构建 front matter（仅包含标题和描述，不需要内容）
    content = f"""---
title: "{name}"
description: "{description or name}"
---

这里是标记为 **{name}** 的所有文章。
"""
    
    # 检查文件是否已存在
    if os.path.exists(filename):
        print(f"⚠️  标签已存在: {filename}")
        return False
    
    # 写入文件
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ 标签创建成功: {filename}")
    print(f"   名称: {name}")
    print(f"   提示: 标签文件在 content/tags/ 目录，不会影响 public/")

    # 自动推送到 GitHub
    git_push("标签", name)

    return True


def build_site():
    """构建 Hugo 站点"""
    print("🔨 正在构建站点...")
    try:
        result = subprocess.run(["hugo", "--minify"], capture_output=True, text=True, check=True, encoding='utf-8', errors='ignore')
        print("✅ 构建成功!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e.stderr}")
        return False
    except FileNotFoundError:
        print("❌ 错误: 未找到 hugo 命令")
        return False


def deploy_site():
    """部署站点（执行 deploy.sh 或 deploy.bat）"""
    if os.name == 'nt':  # Windows
        script = "deploy.bat"
    else:  # Linux/Mac
        script = "./deploy.sh"
    
    if not os.path.exists(script):
        print(f"❌ 未找到部署脚本: {script}")
        return False
    
    print(f"🚀 正在执行部署脚本: {script}")
    try:
        result = subprocess.run([script], capture_output=True, text=True, check=True, shell=True, encoding='utf-8', errors='ignore')
        print("✅ 部署成功!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 部署失败: {e.stderr}")
        return False


def print_menu():
    """打印交互式菜单"""
    if RICH_AVAILABLE:
        console.print(Panel.fit(
            "[bold cyan]Hugo 博客管理工具[/bold cyan]\n"
            "[dim]快速创建文章、分类、标签[/dim]",
            title="📝",
            border_style="cyan"
        ))
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("选项", style="cyan", justify="center")
        table.add_column("功能", style="green")
        table.add_column("说明", style="dim")
        
        table.add_row("1", "新建文章", "创建一篇新的博客文章")
        table.add_row("2", "新建分类", "创建一个新的文章分类")
        table.add_row("3", "新建标签", "创建一个新的文章标签")
        table.add_row("4", "构建站点", "运行 hugo 构建命令")
        table.add_row("5", "部署站点", "执行部署脚本")
        table.add_row("6", "一键发布", "创建文章并立即部署")
        table.add_row("7", "设置", "配置自动推送等选项")
        table.add_row("0", "退出", "退出程序")
        
        console.print(table)
    else:
        print("\n" + "=" * 50)
        print("       Hugo 博客管理工具")
        print("=" * 50)
        print("\n  1. 新建文章    - 创建一篇新的博客文章")
        print("  2. 新建分类    - 创建一个新的文章分类")
        print("  3. 新建标签    - 创建一个新的文章标签")
        print("  4. 构建站点    - 运行 hugo 构建命令")
        print("  5. 部署站点    - 执行部署脚本")
        print("  6. 一键发布    - 创建文章并立即部署")
        print("  7. 设置        - 配置自动推送等选项")
        print("  0. 退出        - 退出程序")
        print("=" * 50)


def settings_mode():
    """设置管理"""
    config = load_config()

    while True:
        if RICH_AVAILABLE:
            console.print(Panel.fit(
                "[bold cyan]配置管理[/bold cyan]\n"
                "[dim]配置文件的自动推送等选项[/dim]",
                title="⚙️",
                border_style="cyan"
            ))

            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("选项", style="cyan", justify="center")
            table.add_column("设置项", style="green")
            table.add_column("当前值", style="yellow")

            table.add_row("1", "自动推送", "开启" if config.get('auto_push', False) else "关闭")
            table.add_row("2", "提交消息模板", config.get('commit_message', 'Update: {type} - {name}'))
            table.add_row("0", "返回主菜单", "")

            console.print(table)
        else:
            print("\n" + "=" * 50)
            print("       配置管理")
            print("=" * 50)
            print(f"\n  1. 自动推送        {'开启' if config.get('auto_push', False) else '关闭'}")
            print(f"  2. 提交消息模板   {config.get('commit_message', 'Update: {{type}} - {{name}}')}")
            print("  0. 返回主菜单")
            print("=" * 50)

        if RICH_AVAILABLE:
            choice = Prompt.ask("\n请选择操作", choices=["0", "1", "2"], default="0")
        else:
            choice = input("\n请选择操作 (0-2): ").strip()

        if choice == "1":
            # 切换自动推送
            current = config.get('auto_push', False)
            config['auto_push'] = not current
            if save_config(config):
                if RICH_AVAILABLE:
                    console.print(f"✅ 自动推送已 {'开启' if config['auto_push'] else '关闭'}", style="green")
                else:
                    print(f"✅ 自动推送已 {'开启' if config['auto_push'] else '关闭'}")

        elif choice == "2":
            # 修改提交消息模板
            if RICH_AVAILABLE:
                new_msg = Prompt.ask(
                    "请输入提交消息模板（使用 {type} 和 {name} 占位符）",
                    default=config.get('commit_message', 'Update: {type} - {name}')
                )
            else:
                new_msg = input(
                    f"请输入提交消息模板（使用 {{type}} 和 {{name}} 占位符） [当前: {config.get('commit_message', 'Update: {{type}} - {{name}}')}]: "
                ).strip() or config.get('commit_message', 'Update: {type} - {name}')

            config['commit_message'] = new_msg
            if save_config(config):
                if RICH_AVAILABLE:
                    console.print("✅ 提交消息模板已更新", style="green")
                else:
                    print("✅ 提交消息模板已更新")

        elif choice == "0":
            break


def interactive_mode():
    """交互式命令行模式"""
    # 切换到脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    while True:
        print_menu()

        if RICH_AVAILABLE:
            choice = Prompt.ask("\n请选择操作", choices=["0", "1", "2", "3", "4", "5", "6", "7"], default="0")
        else:
            choice = input("\n请选择操作 (0-7): ").strip()
        
        if choice == "1":
            # 新建文章
            if RICH_AVAILABLE:
                title = Prompt.ask("请输入文章标题")
                categories_str = Prompt.ask("请输入分类（多个用逗号分隔，可选）", default="")
                tags_str = Prompt.ask("请输入标签（多个用逗号分隔，可选）", default="")
                is_draft = not Confirm.ask("是否直接发布？", default=False)
            else:
                title = input("请输入文章标题: ").strip()
                categories_str = input("请输入分类（多个用逗号分隔，可选）: ").strip()
                tags_str = input("请输入标签（多个用逗号分隔，可选）: ").strip()
                is_draft = input("是否保存为草稿? (Y/n): ").strip().lower() != 'n'
            
            categories = [c.strip() for c in categories_str.split(",") if c.strip()] if categories_str else None
            tags = [t.strip() for t in tags_str.split(",") if t.strip()] if tags_str else None
            new_post(title, categories, tags, draft=is_draft)
        
        elif choice == "2":
            # 新建分类
            if RICH_AVAILABLE:
                name = Prompt.ask("请输入分类名称")
                description = Prompt.ask("请输入分类描述（可选）", default="")
            else:
                name = input("请输入分类名称: ").strip()
                description = input("请输入分类描述（可选）: ").strip()
            new_category(name, description or "")
        
        elif choice == "3":
            # 新建标签
            if RICH_AVAILABLE:
                name = Prompt.ask("请输入标签名称")
                description = Prompt.ask("请输入标签描述（可选）", default="")
            else:
                name = input("请输入标签名称: ").strip()
                description = input("请输入标签描述（可选）: ").strip()
            new_tag(name, description or "")
        
        elif choice == "4":
            build_site()
        
        elif choice == "5":
            deploy_site()
        
        elif choice == "6":
            # 一键发布
            if RICH_AVAILABLE:
                title = Prompt.ask("请输入文章标题")
                categories_str = Prompt.ask("请输入分类（多个用逗号分隔，可选）", default="")
                tags_str = Prompt.ask("请输入标签（多个用逗号分隔，可选）", default="")
            else:
                title = input("请输入文章标题: ").strip()
                categories_str = input("请输入分类（多个用逗号分隔，可选）: ").strip()
                tags_str = input("请输入标签（多个用逗号分隔，可选）: ").strip()

            categories = [c.strip() for c in categories_str.split(",") if c.strip()] if categories_str else None
            tags = [t.strip() for t in tags_str.split(",") if t.strip()] if tags_str else None

            if new_post(title, categories, tags, draft=False):
                if build_site():
                    deploy_site()

        elif choice == "7":
            # 设置
            settings_mode()

        elif choice == "0":
            if RICH_AVAILABLE:
                console.print("\n[dim]再见！[/dim] 👋")
            else:
                print("\n再见！")
            break
        
        else:
            print("无效的选择，请重试。")
        
        input("\n按回车键继续...")


def main():
    parser = argparse.ArgumentParser(
        description="Hugo 博客快速提交工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python hugo_cli.py              # 启动交互式界面
  python hugo_cli.py post "我的新文章" -c 技术 -t python,hugo
  python hugo_cli.py category "技术分享" -d "分享技术文章"
  python hugo_cli.py tag "教程" -d "教程类文章"
  python hugo_cli.py build
  python hugo_cli.py deploy
  python hugo_cli.py settings      # 配置自动推送等选项
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 新建文章
    post_parser = subparsers.add_parser('post', help='创建新文章')
    post_parser.add_argument('title', help='文章标题')
    post_parser.add_argument('-c', '--categories', help='分类，多个用逗号分隔')
    post_parser.add_argument('-t', '--tags', help='标签，多个用逗号分隔')
    post_parser.add_argument('--publish', action='store_true', help='直接发布（非草稿）')
    
    # 新建分类
    cat_parser = subparsers.add_parser('category', help='创建新分类')
    cat_parser.add_argument('name', help='分类名称')
    cat_parser.add_argument('-d', '--description', help='分类描述')
    
    # 新建标签
    tag_parser = subparsers.add_parser('tag', help='创建新标签')
    tag_parser.add_argument('name', help='标签名称')
    tag_parser.add_argument('-d', '--description', help='标签描述')
    
    # 构建站点
    subparsers.add_parser('build', help='构建 Hugo 站点')
    
    # 部署站点
    subparsers.add_parser('deploy', help='部署站点')
    
    # 一键发布（创建文章+构建+部署）
    publish_parser = subparsers.add_parser('publish', help='一键发布文章')
    publish_parser.add_argument('title', help='文章标题')
    publish_parser.add_argument('-c', '--categories', help='分类，多个用逗号分隔')
    publish_parser.add_argument('-t', '--tags', help='标签，多个用逗号分隔')
    
    # 交互式界面
    subparsers.add_parser('interactive', help='启动交互式菜单界面')

    # 设置命令
    subparsers.add_parser('settings', help='配置管理')

    args = parser.parse_args()
    
    # 切换到脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # 如果没有命令或指定了 interactive，启动交互式界面
    if not args.command or args.command == 'interactive':
        interactive_mode()
        return
    
    if args.command == 'post':
        categories = args.categories.split(',') if args.categories else None
        tags = args.tags.split(',') if args.tags else None
        new_post(args.title, categories, tags, draft=not args.publish)
    
    elif args.command == 'category':
        new_category(args.name, args.description)
    
    elif args.command == 'tag':
        new_tag(args.name, args.description)
    
    elif args.command == 'build':
        build_site()
    
    elif args.command == 'deploy':
        deploy_site()
    
    elif args.command == 'publish':
        categories = args.categories.split(',') if args.categories else None
        tags = args.tags.split(',') if args.tags else None

        if new_post(args.title, categories, tags, draft=False):
            if build_site():
                deploy_site()

    elif args.command == 'settings':
        settings_mode()


if __name__ == '__main__':
    main()
