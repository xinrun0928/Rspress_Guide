// ==============================================
// 导入 Rspress 核心依赖
// ==============================================

import * as path from 'node:path';
import { defineConfig } from '@rspress/core';
import { pluginSass } from '@rsbuild/plugin-sass';
import mermaid from 'rspress-plugin-mermaid';
import { nav } from './theme_config/nav';
import { sidebar } from './theme_config/sidebar';
import { transformerNotationHighlight } from '@shikijs/transformers';

// ==============================================
// 经常变化的配置（站点信息、SEO、导航、社交链接等）
// ==============================================

/**
 * 站点基础信息
 */
const siteMeta = {
  /** 网站标题 - 显示在浏览器标签页和导航栏 */
  title: 'Guide',
  /** 网站描述 - 用于 SEO 搜索引擎优化 */
  description: '系统梳理 Java 后端核心知识，覆盖面试高频考点，助你从容应对技术面试',
  /** 作者信息 */
  author: 'Mr.zhang',
  /** 站点关键词 - 根据导航栏目自动生成 */
  keywords: [
    // 面试准备
    '面试准备', 'Java面试', '后端面试', '技术面试', '简历编写', 'STAR法则', '行为面试', '薪资谈判', '大厂面经', 'Offer选择',
    // 计算机基础
    '计算机网络', 'TCP', 'IP', 'HTTP', 'HTTPS', '操作系统', '进程', '线程', '内存管理', 'IO模型', '网络安全', '加密算法', '数据机构', '算法',
    // Java 核心
    'Java', 'JVM', '并发编程', '线程池', '集合框架', 'HashMap', 'Spring', 'Spring Boot', 'MyBatis',
    // 数据库
    'MySQL', 'Redis', 'MongoDB', '索引', '事务', '锁', '缓存', '分布式锁',
    // 分布式与架构
    '分布式', '微服务', 'Spring Cloud', '消息队列', 'Kafka', 'RPC', 'Dubbo', 'Nacos', 'Zookeeper',
    // 高频面试题
    'Java面试题', 'MySQL面试题', 'Redis面试题', 'JVM面试题', '并发编程面试题', '分布式面试题', '系统设计',
    // 核心标签
    '后端开发', '架构设计', '系统架构', '高并发', '高性能', '高可用', '设计模式', '系统设计'
  ],
};

/**
 * GitHub 仓库地址
 */
const gitHubRepo = 'https://github.com/xinrun0928/Rspress_Guide';

// ==============================================
// Rspress 核心配置
// ==============================================

export default defineConfig({
  // ==============================================
  // 插件配置（Rspress 专属插件，如 mermaid、自定义 remark/unified 插件等）
  // 注意：@rsbuild/plugin-sass 属于构建工具插件，应放在 builderConfig.plugins 中
  // ==============================================
  plugins: [
    mermaid({
      mermaidConfig: {
        theme: 'forest',
      },
    }),
  ],

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
  title: siteMeta.title,

  /**
   * 网站描述
   * 用于 SEO 搜索引擎优化，提升站点被搜索概率
   * 简洁概括站点内容，便于搜索引擎收录
   */
  description: siteMeta.description,

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
    light: '/icon.png',
    // 暗色主题下显示的 Logo
    dark: '/icon.png',
  },

  /**
   * 搜索框开关
   * true：在顶部导航栏显示文档搜索框（支持全文搜索）
   * false：隐藏搜索功能
   */
  search: false,

  /**
   * 构建工具配置
   * 用于配置 Rsbuild/Rspack 的构建行为，包括插件、编译器选项等
   * 注意：@rsbuild/plugin-sass 等构建插件必须放在这里，而非顶层 plugins 配置
   */
  builderConfig: {
    plugins: [
      pluginSass(),
    ],
  },

  // ==============================================
  // 主题外观配置（导航、侧边栏、搜索、页脚等）
  // ==============================================
  themeConfig: {

    // 顶部导航栏配置
    nav: nav,

    // 侧边栏配置
    sidebar: sidebar,

    /**
     * 搜索框开关
     * true：在顶部导航栏显示文档搜索框（支持全文搜索）
     * false：隐藏搜索功能
     */
    search: false,

    /**
     * 社交链接配置
     * 在页面顶部展示社交媒体/代码仓库图标入口
     * 支持 github / twitter / gitlab 等内置图标
     */
    socialLinks: [
      {
        icon: 'github',
        mode: 'link',
        content: gitHubRepo,
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
      docRepoBaseUrl: `${gitHubRepo}/blob/main/docs`,
    },

    /**
     * 页脚配置
     * 控制文档站点最底部的版权信息、链接等
     * 支持 HTML 标签，可插入链接、样式等
     */
    footer: {
      message: `Copyright © 2025-2026 <a href="${gitHubRepo}">Guide</a>`,
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
    shiki: {
      transformers: [transformerNotationHighlight()],
    },
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
    `<meta name="author" content="${siteMeta.author}">`,
    `<meta name="keywords" content="${siteMeta.keywords.join(',')}">`,
  ],
});