import * as path from 'node:path';
import * as url from 'node:url';
import type { RspressPlugin } from '@rspress/core';

const __dirname = path.dirname(url.fileURLToPath(import.meta.url));

export interface MermaidPluginOptions {
  theme?: 'default' | 'forest' | 'dark' | 'neutral' | 'base';
}

const defaultOptions: Required<MermaidPluginOptions> = {
  theme: 'default',
};

/**
 * Mermaid 图表渲染插件
 *
 * 工作原理：
 * 1. 使用 Rspress 内置的 Shiki 代码高亮处理 ```mermaid 代码块
 * 2. 通过 globalUIComponents 注入运行时脚本
 * 3. 运行时脚本查找所有 mermaid 代码块，动态加载 mermaid 并渲染为 SVG
 *
 * 使用方式：
 * ```ts
 * import { pluginMermaid } from './plugins/mermaid';
 *
 * export default defineConfig({
 *   plugins: [pluginMermaid({ theme: 'dark' })],
 * });
 * ```
 */
export function pluginMermaid(options: MermaidPluginOptions = {}): RspressPlugin {
  const mergedOptions = { ...defaultOptions, ...options };

  return {
    name: 'rspress-plugin-mermaid',

    // 全局样式文件
    globalStyles: path.join(__dirname, 'mermaid.css'),

    // 全局 UI 组件（运行时脚本，不渲染任何内容）
    globalUIComponents: [
      [path.join(__dirname, 'MermaidRuntime.tsx'), { defaultTheme: mergedOptions.theme }],
    ],
  };
}
