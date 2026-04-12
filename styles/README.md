# 主题配色

本目录包含 Rspress 文档站点的全局 CSS 主题文件，通过 CSS 变量覆盖实现品牌色定制。

## 主题列表

| 文件名 | 主题名称 | 品牌色 | 说明 |
|--------|----------|--------|------|
| `global_aurora.css` | 极光紫蓝 | `#667eea` | 科技感、冷调、适合技术文档 |
| `global_cyber.css` | 赛博朋克 | `#00d4ff` | 亮青、高对比、未来感 |
| `global_earth.css` | 大地棕 | `#8b6914` | 暖棕、自然、适合生活类站点 |
| `global_forest.css` | 森林绿 | `#2e8b57` | 墨绿、清新、适合环保/开源项目 |
| `global_gold.css` | 琥珀金 | `#d4a017` | 暖金、商务、适合金融/咨询类站点 |
| `global_lavender.css` | 薰衣草紫 | `#8b5cf6` | 柔和紫、优雅、适合创意类站点 |
| `global_mint.css` | 薄荷绿 | `#10b981` | 青绿、清爽、适合健康/工具类站点 |
| `global_night.css` | 午夜深蓝 | `#1e3a8a` | 深蓝、沉稳、适合企业/专业文档 |
| `global_ocean.css` | 海洋蓝 | `#0097b2` | 蔚蓝、专业、适合出海/多语言站点 |
| `global_rose.css` | 玫瑰红 | `#e63946` | 玫红、活力、适合营销/产品站点 |
| `global_sakura.css` | 樱花粉 | `#ff6b9d` | 粉色、少女、适合个人博客/女性向 |
| `global_steel.css` | 钢铁灰蓝 | `#4a6fa5` | 钢蓝、中性、适合默认/通用场景 |
| `global_default.css` | 默认主题 | — | 使用 Rspress 默认配色 |

## 变量说明

每个主题文件通过 CSS 变量覆盖 Rspress 默认样式，核心变量如下：

### 品牌色（必需）

```css
--rp-c-brand:        /* 主品牌色，用于导航背景、链接 hover 等 */
--rp-c-brand-light:  /* 品牌色浅色，用于 hover 状态 */
--rp-c-brand-lighter:/* 品牌色极浅，用于 badge / tag 背景 */
--rp-c-brand-dark:   /* 品牌色深色，用于文字链接 */
--rp-c-brand-darker: /* 品牌色最深，用于 active / focus 状态 */
--rp-c-brand-tint:   /* 品牌色透明色，用于代码块背景等 */
```

### 亮色模式（`html:not(.rp-dark)`）

```css
--rp-c-bg:           /* 页面背景色 */
--rp-c-bg-soft:      /* 次级背景（侧边栏、代码块等） */
--rp-c-bg-mute:      /* 静音背景（disabled、placeholder 等） */
--rp-c-bg-alt:       /* 可选背景（卡片、弹窗等） */

--rp-c-divider:      /* 分隔线（主） */
--rp-c-divider-light:/* 分隔线（次） */

--rp-c-text-0:       /* 主文本色 */
--rp-c-text-1:       /* 文本色（标题等） */
--rp-c-text-2:       /* 文本色（正文） */
--rp-c-text-3:       /* 文本色（辅助说明） */
--rp-c-text-4:       /* 文本色（占位符等） */

--rp-c-link:         /* 链接色 */

--rp-c-gray:         /* 灰色中性色基准 */
--rp-c-gray-light-1 ~ -5: /* 灰度渐变，从深到浅 */
```

### 暗色模式（`html.rp-dark`）

暗色模式在 `html.rp-dark` 下定义，与亮色模式对应，通常将背景调深、文本调浅。

### 阴影

```css
--rp-shadow-1:       /* 卡片轻微阴影 */
--rp-shadow-2:       /* 浮层阴影（如下拉菜单） */
--rp-shadow-3:       /* 弹窗/模态框阴影 */
--rp-shadow-4:       /* 大阴影（特殊浮层） */
```

### 圆角

```css
--rp-radius-sm:      /* 小圆角（badge、tag） */
--rp-radius-md:      /* 中圆角（按钮、输入框） */
--rp-radius-lg:      /* 大圆角（卡片、弹窗） */
```

## 使用方式

在 `rspress.config.ts` 的 `globalStyles` 中指定路径：

```ts
import { defineConfig } from 'rspress/config';
import path from 'node:path';

export default defineConfig({
  globalStyles: path.join(__dirname, 'styles/global_steel.css'),
});
```

## 切换主题

可参考 [Rspress 主题切换插件](https://rspress.dev/zh/guide/advanced/custom-theme#%E6%8F%92%E4%BB%B6) 自定义主题切换组件，通过动态切换 `globalStyles` 路径实现多主题切换功能。

## 主题设计规范

1. **品牌色层次** — 同一色相应有 5 个以上梯度（lighter / light / base / dark / darker），确保各状态下可辨识
2. **对比度** — 文本与背景 WCAG 对比度应 ≥ 4.5:1（正文）/ 3:1（大字号）
3. **暗色模式** — 避免使用纯黑 `#000` / 纯白 `#fff`，推荐背景使用 `#121212` ~ `#1e1e1e`，文本使用 `#e0e0e0`
4. **变量前缀** — Rspress 所有主题变量均以 `rp-` 开头，自定义变量请使用其他前缀避免冲突
