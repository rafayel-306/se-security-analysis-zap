#!/usr/bin/env python3
"""
ZAP 自动化扫描示例
使用 ZAP Python API 启动主动扫描并生成报告
"""

import time
from zapv2 import ZAPv2

# ZAP API 配置（默认地址和端口）
zap = ZAPv2(apikey='', proxies={'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'})

# 目标 URL（替换为你的测试目标）
target = 'http://localhost/dvwa/'

def main():
    print('访问目标站点...')
    zap.urlopen(target)
    time.sleep(2)

    print('开始主动扫描...')
    scan_id = zap.ascan.scan(target, recurse=True, inscopeonly=False)

    # 等待扫描完成
    while int(zap.ascan.status(scan_id)) < 100:
        print(f'扫描进度: {zap.ascan.status(scan_id)}%')
        time.sleep(5)

    print('扫描完成！')

    # 输出告警数量
    alerts = zap.core.alerts(baseurl=target)
    print(f'发现告警数量: {len(alerts)}')

    # 生成 HTML 报告
    print('生成报告...')
    report = zap.core.htmlreport()
    with open('zap_report.html', 'w', encoding='utf-8') as f:
        f.write(report)
    print('报告已保存为 zap_report.html')

if __name__ == '__main__':
    main()
