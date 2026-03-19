#!/usr/bin/env python3
import sys
import urllib.request
import urllib.error
import re

def fetch_url(url):
    # 使用本地代理绕过 Fake-IP 解析问题
    # 代理地址取自 openclaw.json 的 http_proxy 配置
    proxy_handler = urllib.request.ProxyHandler({
        'http': 'http://127.0.0.1:8890',
        'https': 'http://127.0.0.1:8890'
    })
    opener = urllib.request.build_opener(proxy_handler)
    
    # 伪装成浏览器请求
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    )
    
    try:
        response = opener.open(req, timeout=15)
        html = response.read().decode('utf-8', errors='ignore')
        
        # 简单粗暴的去除 HTML 标签，保留纯文本供 AI 阅读
        text = re.sub(r'<style.*?>.*?</style>', '', html, flags=re.IGNORECASE|re.DOTALL)
        text = re.sub(r'<script.*?>.*?</script>', '', text, flags=re.IGNORECASE|re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        # 截断过长内容，避免 Token 爆炸 (保留前 20000 字符)
        return text[:20000]
    
    except Exception as e:
        return f"Error fetching {url}: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch_tool.py <URL>")
        sys.exit(1)
    
    target_url = sys.argv[1]
    print(fetch_url(target_url))