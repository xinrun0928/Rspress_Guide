import { useNav, useSite } from '@rspress/core/runtime';
import {
  NavHamburger,
  NavTitle,
  Search,
  SocialLinks,
  SwitchAppearance,
} from '@rspress/core/theme';
import './index.scss';
import { NavLangs, NavMenu, NavMenuDivider, NavVersions } from './NavMenu';

// slot 模式：允许外部（如 rspress.config.ts 的 themeConfig.navbar）注入自定义内容
// beforeNavTitle/afterNavTitle 插入 Logo 左右，beforeNavMenu/afterNavMenu 插入搜索框左右
export interface NavProps {
  beforeNavTitle?: React.ReactNode;
  navTitle?: React.ReactNode;
  afterNavTitle?: React.ReactNode;

  beforeNavMenu?: React.ReactNode;
  afterNavMenu?: React.ReactNode;
}

export function Nav(props: NavProps) {
  const {
    beforeNavTitle,
    afterNavTitle,
    beforeNavMenu,
    afterNavMenu,
    navTitle,
  } = props;
  // useNav 读取 docs/_nav.json，生成导航项列表
  const navList = useNav();
  const { site } = useSite();
  // darkMode 默认为 true，设置为 false 时隐藏主题切换按钮
  // 条件用 !== false 而非 truthy，是为了让 undefined（未配置）也走默认值
  const hasAppearanceSwitch = site.themeConfig.darkMode !== false;

  return (
    <header className="rp-nav">
      <div className="rp-nav__left">
        {beforeNavTitle}
        {navTitle ?? <NavTitle />}
        {/* desktop：左侧 Logo + 导航主菜单 */}
        <NavMenu menuItems={navList} position="left" />
        {afterNavTitle}
      </div>

      <div className="rp-nav__right">
        {beforeNavMenu}
        {/* <Search /> */}

        {/* desktop：右侧辅助导航（多语言、版本、主题切换、社交链接） */}
        <NavMenu menuItems={navList} position="right" />
        <div className="rp-nav__others">
          <NavMenuDivider />
          <NavLangs />
          <NavVersions />
          {hasAppearanceSwitch && <SwitchAppearance />}
          <SocialLinks />
        </div>

        {/* mobile：导航折叠为汉堡菜单 */}
        <NavHamburger />
        {afterNavMenu}
      </div>
    </header>
  );
}
