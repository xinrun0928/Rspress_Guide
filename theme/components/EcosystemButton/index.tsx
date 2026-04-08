/**
 * 生态导航按钮组件
 *
 * 功能：在导航栏提供下拉入口，快速访问作者的其他文档项目。
 * 点击按钮展开下拉列表，显示所有配置的生态项目链接。
 *
 * 特性：
 * - 点击外部自动关闭
 * - 支持外部链接新窗口打开
 * - 单项时自动切换为单列布局
 */

import { useEffect, useRef, useState } from 'react';
import './index.css';
import { ecosystemButton } from '../../../theme_config/ecosystemButton';

export const EcosystemButton = () => {
  // 组件自管理的展开状态，不依赖外部控制
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // mousedown 而非 click：mousedown 先于 click 触发，
  // 这样点击下拉菜单内的链接时，dropdown 能在点击事件冒泡前关闭，
  // 避免 click 打到关闭的 DOM 上导致导航失效
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className="ecosystem-button-container" ref={dropdownRef}>
      <button
        className="ecosystem-button"
        onClick={() => setIsOpen(!isOpen)}
        aria-label="生态导航"
        aria-expanded={isOpen}
      >
        {/* 2x2 网格图标：暗示多个生态项目 */}
        <svg
          className="ecosystem-button-icon"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <rect x="3" y="3" width="7" height="7" />
          <rect x="14" y="3" width="7" height="7" />
          <rect x="14" y="14" width="7" height="7" />
          <rect x="3" y="14" width="7" height="7" />
        </svg>
      </button>

      <div className={`ecosystem-button-dropdown ${isOpen ? 'open' : ''}`}>
        <div className="ecosystem-button-header">
          <span className="ecosystem-button-title">我的生态</span>
        </div>
        <div className={`ecosystem-button-list ${ecosystemButton.length === 1 ? 'single' : ''}`}>
          {ecosystemButton.map((item) => {
            // 以 http(s):// 开头判定为外部链接，内部链接走前端路由（无协议头）
            const isExternal = item.link.startsWith('http://') || item.link.startsWith('https://');
            return (
              <a
                key={item.name}
                href={item.link}
                className="ecosystem-button-item"
                // 外部链接用 target="_blank" 新窗口打开，内部链接用当前窗口（支持前端路由）
                target={isExternal ? '_blank' : undefined}
                // 新窗口时必须加 noopener noreferrer：防止新页面通过 window.opener 操控本页面
                rel={isExternal ? 'noopener noreferrer' : undefined}
                onClick={() => setIsOpen(false)}
              >
                <span className="ecosystem-button-item-icon">{item.icon}</span>
                <div className="ecosystem-button-item-content">
                  <span className="ecosystem-button-item-name">{item.name}</span>
                  <span className="ecosystem-button-item-desc">{item.description}</span>
                </div>
              </a>
            );
          })}
        </div>
      </div>
    </div>
  );
};
