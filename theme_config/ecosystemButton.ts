/**
 * 生态导航配置
 *
 * 数据定义在此文件，供以下两处引用：
 *  - rspress.config.ts（themeConfig 中声明来源，仅作文档注释）
 *  - theme/components/EcosystemButton/index.tsx（实际读取使用）
 *
 * 如需修改生态导航列表，直接编辑本文件即可。
 */
export interface EcosystemItem {
  name: string;
  description: string;
  /** 站内路径或外部链接（以 http 开头则新窗口打开） */
  link: string;
  icon: string;
}

export const ecosystemButton: EcosystemItem[] = [
  {
    name: 'Java 面试指南',
    description: '覆盖面试高频考点，助你从容应对技术面试',
    link: 'https://guide.docs.zxinrun.cn/',
    icon: '🧭',
  }
];
