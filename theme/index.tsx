import { Layout as BasicLayout } from '@rspress/core/theme-original';
import { EcosystemButton } from './components/EcosystemButton';

export { Nav } from './components/Nav';

const Layout = () => (
  <BasicLayout
    /* 导航栏 Logo 左侧区域 */
    beforeNavTitle={<EcosystemButton />}
  />
);

export { Layout };
export * from '@rspress/core/theme-original';
