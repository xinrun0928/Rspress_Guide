import * as path from 'node:path';
import { defineConfig } from '@rspress/core';

export default defineConfig({
  // 文档根目录，指向 docs 文件夹，所有文档内容都放在此目录下
  root: path.join(__dirname, 'docs'),

  // 网站标题，显示在浏览器标签页和导航栏中
  title: 'Guide',

  // 网站描述，用于 SEO 和搜索引擎收录
  description: '系统梳理 Java 后端核心知识，覆盖面试高频考点，助你从容应对技术面试',

  // 浏览器标签页图标，路径相对于 public 目录
  icon: '/images/logo.png',

  // Logo 配置，支持亮色/暗色模式自动切换
  logo: {
    // 亮色模式下显示的 Logo
    light: '/images/logo.png',
    // 暗色模式下显示的 Logo
    dark: '/images/logo.png',
  },

  // 主题配置，用于自定义站点的外观和行为
  themeConfig: {
    // 社交链接配置，用于展示 GitHub、Twitter 等社交媒体入口
    socialLinks: [
      {
        // 使用内置的 GitHub 图标
        icon: 'github',
        // 链接模式：link 表示跳转到外部链接
        mode: 'link',
        // 点击后跳转的目标地址
        content: 'https://github.com/xinrun0928/Guide',
      },
    ],
  },

  markdown: {
    // 所有代码块默认都会显示行号
    showLineNumbers: true,
  },

  route: {
    // 开启后可以生成无 .html 后缀的链接，URL 可以更加简洁。
    cleanUrls: true,
  },
});
