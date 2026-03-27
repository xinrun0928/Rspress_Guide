#!/usr/bin/env node
/**
 * 批量将指定目录下的 *.md 文件转换为 *.mdx 文件
 *
 * 用法:
 *   node md-to-mdx.js <目标目录>
 *
 * 示例:
 *   node md-to-mdx.js ./docs/guide
 */

import { readdir, stat, rename, readFile, writeFile, access } from 'node:fs/promises';
import { join, resolve } from 'node:path';
import { constants } from 'node:fs';

const [, , targetDir = './docs'] = process.argv;

async function fileExists(path) {
  try {
    await access(path, constants.F_OK);
    return true;
  } catch {
    return false;
  }
}

async function walkDir(dir) {
  const mdFiles = [];
  const entries = await readdir(dir, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = join(dir, entry.name);
    if (entry.isDirectory()) {
      mdFiles.push(...(await walkDir(fullPath)));
    } else if (entry.isFile() && entry.name.endsWith('.md')) {
      mdFiles.push(fullPath);
    }
  }

  return mdFiles;
}

async function convertFile(filePath) {
  const mdxPath = filePath.replace(/\.md$/, '.mdx');

  if (await fileExists(mdxPath)) {
    console.warn(`⚠️  跳过（已存在）: ${mdxPath}`);
    return 'skipped';
  }

  await rename(filePath, mdxPath);
  console.log(`✅ 转换完成: ${filePath} -> ${mdxPath}`);
  return 'converted';
}

async function main() {
  const resolvedDir = resolve(targetDir);

  if (!(await fileExists(resolvedDir))) {
    console.error(`❌ 目录不存在: ${resolvedDir}`);
    process.exit(1);
  }

  console.log(`🔍 正在扫描目录: ${resolvedDir}\n`);

  const mdFiles = await walkDir(resolvedDir);

  if (mdFiles.length === 0) {
    console.log('📭 未找到任何 .md 文件。');
    return;
  }

  console.log(`📄 找到 ${mdFiles.length} 个 .md 文件：\n`);

  let converted = 0;
  let skipped = 0;

  for (const file of mdFiles) {
    const result = await convertFile(file);
    if (result === 'converted') converted++;
    else skipped++;
  }

  console.log(`\n📊 统计：转换 ${converted} 个，跳过 ${skipped} 个。`);
}

main().catch((err) => {
  console.error('❌ 执行出错:', err);
  process.exit(1);
});
