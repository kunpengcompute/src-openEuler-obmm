#!/bin/bash
set -euo pipefail

# 检查参数质量
if [ $# -ne 2 ]; then
  echo "用法: $0 <pkg_name> <pkg_version>"
  echo "示例: $0 libobmm 1.0.1"
  exit 1
fi

# 接收参数
pkg_name="$1"
pkg_version="$2"

# 定义文件名和目录名
orig_tar="${pkg_name}_${pkg_version}.orig.tar.gz"
source_dir="${pkg_name}-${pkg_version}"

# 重命名源码包
if [ -f "${pkg_name}.tar.gz" ]; then
  echo "重命名源码包为: ${orig_tar}"
  cp -f "${pkg_name}.tar.gz" "${orig_tar}"
else
  echo "错误: 未找到源码包 ${pkg_name}.tar.gz"
  exit 1
fi

# 创建并进入源码目录
echo "创建源码目录: ${source_dir}"
mkdir -p "${source_dir}"
pushd "${source_dir}" > /dev/null

# 解压源码包
echo "解压源码包到当前目录"
tar -zxf "../${orig_tar}" --strip-components=2

# 执行dh_make生成debian目录框架
echo "生成debian目录结构"
rm -rf ./debian/
dh_make -y -l

# 拷贝上层目录的debian自定义配置
if [ -d "../debian" ]; then
  echo "拷贝自定义debian配置"
  cp -ar ../debian/* ./debian/
else
  echo "警告: 上层目录未找到debian目录, 将使用默认配置"
fi

# 构建deb包
echo "开始构建deb包"
dpkg-buildpackage -rfakeroot -us -uc -b -include-removal

# 退出源码目录
popd > /dev/null

echo "打包完成, 生成的包文件在当前目录"