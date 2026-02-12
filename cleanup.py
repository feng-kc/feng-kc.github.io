#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hugo 博客目录清理工具
删除无用文件并整理目录
"""

import os
import shutil
from pathlib import Path


def delete_file(file_path, description):
    """删除文件并报告"""
    try:
        os.remove(file_path)
        print(f"✅ 已删除: {description}")
        print(f"   路径: {file_path}")
        return True
    except FileNotFoundError:
        print(f"⚠️  文件不存在: {file_path}")
        return False
    except Exception as e:
        print(f"❌ 删除失败: {file_path}")
        print(f"   错误: {e}")
        return False


def delete_directory(dir_path, description):
    """删除目录及其内容"""
    try:
        shutil.rmtree(dir_path)
        print(f"✅ 已删除目录: {description}")
        print(f"   路径: {dir_path}")
        return True
    except FileNotFoundError:
        print(f"⚠️  目录不存在: {dir_path}")
        return False
    except Exception as e:
        print(f"❌ 删除失败: {dir_path}")
        print(f"   错误: {e}")
        return False


def delete_html_xml_in_dir(dir_path, dir_name):
    """删除目录中的所有 .html 和 .xml 文件"""
    if not os.path.exists(dir_path):
        print(f"⚠️  目录不存在: {dir_path}")
        return
    
    deleted_count = 0
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.html') or file.endswith('.xml'):
                file_path = os.path.join(root, file)
                if delete_file(file_path, f"{dir_name}/{file}"):
                    deleted_count += 1
    
    if deleted_count > 0:
        print(f"📊 共删除 {deleted_count} 个文件")
    else:
        print(f"ℹ️  没有需要删除的文件")


def move_posts_to_content():
    """将根目录的 posts/ 移动到 content/posts/"""
    root_posts = "posts"
    content_posts = "content/posts"
    
    if not os.path.exists(root_posts):
        print("⚠️  根目录 posts/ 不存在，跳过移动")
        return
    
    if not os.path.exists(content_posts):
        os.makedirs(content_posts)
        print(f"✅ 已创建: {content_posts}")
    
    moved_count = 0
    for item in os.listdir(root_posts):
        src = os.path.join(root_posts, item)
        dst = os.path.join(content_posts, item)
        
        if os.path.exists(dst):
            print(f"⚠️  目标已存在，跳过: {item}")
            continue
        
        try:
            shutil.move(src, dst)
            print(f"✅ 已移动: posts/{item} → content/posts/")
            moved_count += 1
        except Exception as e:
            print(f"❌ 移动失败: {item}")
            print(f"   错误: {e}")
    
    if moved_count > 0:
        # 检查是否为空
        remaining = os.listdir(root_posts)
        if not remaining or all(f.startswith('.') for f in remaining):
            try:
                shutil.rmtree(root_posts)
                print(f"✅ 已删除空的根目录: posts/")
            except Exception as e:
                print(f"❌ 删除空目录失败: {e}")


def main():
    print("=" * 50)
    print("       Hugo 博客目录清理工具")
    print("=" * 50)
    print()
    
    # 1. 删除根目录的无用文件
    print("🗑️  [1/4] 删除根目录的无用文件")
    print("-" * 50)
    
    files_to_delete = [
        ("index.html", "根目录旧的主页文件"),
        ("index.xml", "根目录的旧索引文件"),
    ]
    
    for filename, desc in files_to_delete:
        delete_file(filename, desc)
    
    print()
    
    # 2. 删除 categories/ 中的 .html 和 .xml 文件
    print("🗑️  [2/4] 删除 categories/ 中的生成文件")
    print("-" * 50)
    delete_html_xml_in_dir("categories", "categories")
    print()
    
    # 3. 删除 tags/ 中的 .html 和 .xml 文件
    print("🗑️  [3/4] 删除 tags/ 中的生成文件")
    print("-" * 50)
    delete_html_xml_in_dir("tags", "tags")
    print()
    
    # 4. 整理 posts/ 目录
    print("📦  [4/4] 整理 posts/ 目录")
    print("-" * 50)
    move_posts_to_content()
    print()
    
    # 5. 检查重复文件
    print("🔍  [5/4] 检查重复文件")
    print("-" * 50)
    
    # 检查 css/ 和 static/css/ 是否重复
    if os.path.exists("css/custom.css") and os.path.exists("static/css/custom.css"):
        print("⚠️  发现重复: css/custom.css 和 static/css/custom.css")
        print("   建议删除 css/ 目录，使用 static/css/")
    
    if os.path.exists("js/effects.js") and os.path.exists("static/js/effects.js"):
        print("⚠️  发现重复: js/effects.js 和 static/js/effects.js")
        print("   建议删除 js/ 目录，使用 static/js/")
    
    print()
    print("=" * 50)
    print("✨ 清理完成！")
    print("=" * 50)
    print()
    print("💡 提示：")
    print("   • content/ 目录是源文件目录（持久保存）")
    print("   • public/ 目录是 Hugo 构建输出（自动生成）")
    print("   • 不要手动修改 public/ 目录的内容")


if __name__ == '__main__':
    main()
