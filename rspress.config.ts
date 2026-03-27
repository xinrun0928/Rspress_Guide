// 导入 Node.js 路径处理模块，用于拼接文件绝对路径
import * as path from 'node:path';
// 导入 Rspress 核心配置定义函数，提供类型提示和配置校验
import { defineConfig } from '@rspress/core';

// Rspress 文档站点核心配置导出
export default defineConfig({
  // ==============================================
  // 基础站点配置（站点根目录、全局资源、基础信息）
  // ==============================================

  /**
   * 文档根目录
   * 配置 Rspress 读取 Markdown 文档的根文件夹
   * 所有 .md / .mdx 文档都必须放在该目录下
   */
  root: path.join(__dirname, 'docs'),

  /**
   * 全局样式文件
   * 配置全局 CSS 样式文件路径，会自动注入到所有页面
   * 可用于统一修改主题色、字体、布局等全局样式
   */
  globalStyles: path.join(__dirname, 'styles/global.css'),

  /**
   * 网站标题
   * 显示在浏览器标签页、导航栏、SEO 标题中
   * 是站点的核心名称标识
   */
  title: 'Guide',

  /**
   * 网站描述
   * 用于 SEO 搜索引擎优化，提升站点被搜索概率
   * 简洁概括站点内容，便于搜索引擎收录
   */
  description: '系统梳理 Java 后端核心知识，覆盖面试高频考点，助你从容应对技术面试',

  /**
   * 网站 favicon 图标（浏览器标签小图标）
   * 路径相对于项目的 public 目录
   * 支持 png / svg / ico 格式
   */
  icon: '/images/logo.png',

  /**
   * 暗黑模式开关
   * true：页面顶部显示「日间/暗黑模式」切换按钮
   * false：隐藏切换按钮，固定使用默认主题
   */
  darkMode: true,

  /**
   * 网站 Logo 配置
   * 支持根据主题模式（亮色/暗色）自动切换不同 Logo
   * 路径均相对于 public 目录
   */
  logo: {
    // 亮色主题下显示的 Logo
    light: '/images/logo.png',
    // 暗色主题下显示的 Logo
    dark: '/images/logo.png',
  },

  // ==============================================
  // 主题外观配置（导航、侧边栏、搜索、页脚等）
  // ==============================================
  themeConfig: {

    /**
     * 搜索框开关
     * true：在顶部导航栏显示文档搜索框（支持全文搜索）
     * false：隐藏搜索功能
     */
    search: true,

    /**
     * 社交链接配置
     * 在页面顶部展示社交媒体/代码仓库图标入口
     * 支持 github / twitter / gitlab 等内置图标
     */
    socialLinks: [
      {
        // 使用 Rspress 内置的 GitHub 图标
        icon: 'github',
        // 链接模式：link = 跳转到外部链接
        mode: 'link',
        // 点击图标跳转的目标 URL
        content: 'https://github.com/xinrun0928/Repress_Guide',
      },
    ],

    /**
     * 「下一篇」按钮文字
     * 文档底部翻页区域的「下一篇」按钮显示文本
     */
    nextPageText: "下一篇",

    /**
     * 滚动到顶部按钮开关
     * true：页面滚动时右下角显示「回到顶部」按钮
     * false：隐藏该功能按钮
     */
    enableScrollToTop: true,

    /**
     * 文档编辑链接
     * 在文档页面显示「编辑此页」按钮，跳转到 Git 仓库对应文件
     * 方便用户直接在 GitHub/GitLab 上提交文档修改
     */
    editLink: {
      // 文档在 Git 仓库中的根目录 URL
      docRepoBaseUrl: 'https://github.com/xinrun0928/Repress_Guide/tree/main/website/docs',
    },

    /**
     * 页脚配置
     * 控制文档站点最底部的版权信息、链接等
     * 支持 HTML 标签，可插入链接、样式等
     */
    footer: {
      message: 'Copyright © 2025-2026 <a href="https://github.com/xinrun0928/Repress_Guide">Guide</a>',
    }
  },

  // ==============================================
  // Markdown 渲染配置
  // ==============================================
  markdown: {
    /**
     * 代码块行号显示
     * true：所有代码块默认显示行号，便于定位代码行数
     * false：隐藏代码块行号
     */
    showLineNumbers: true,
  },

  // ==============================================
  // 路由与 URL 配置
  // ==============================================
  route: {
    /**
     * 简洁 URL 模式
     * true：生成无 .html 后缀的 URL（如 /java/base）
     * false：URL 保留 .html 后缀（如 /java/base.html）
     * 开启后 URL 更美观，更符合现代网站规范
     */
    cleanUrls: true,
  },

  // ==============================================
  // 页面头部标签配置（SEO、meta 标签、自定义 head）
  // 用于向 HTML <head> 中注入自定义标签
  // ==============================================
  head: [
    // 写法 1：直接传入 HTML 字符串
    '<meta name="author" content="Mr.zhang">'
  ],
});