# get_data.py (V13 - High-Efficiency Resume)

import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- 配置区 (保持不变) ---
BASE_URL = "https://love-live.fandom.com"
START_URL = "https://love-live.fandom.com/wiki/Category:SIF_Chika_Takami" 
SAVE_DIR = "aqours_chika_takami_images"

# --- 功能函数 (保持不变) ---
def get_gallery_links(url):
    print("正在从主列表页获取所有图集链接...")
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        # 禁用代理以避免代理连接错误
        proxies = {'http': None, 'https': None}
        response = requests.get(url, headers=headers, proxies=proxies, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.select('li.category-page__member a.category-page__member-link')
        gallery_links = [BASE_URL + link['href'] for link in links]
        print(f"成功找到 {len(gallery_links)} 个图集链接。")
        return gallery_links
    except requests.RequestException as e:
        print(f"获取图集链接失败: {e}")
        return []

def download_image(url, save_path):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        print(f"  正在下载: {url}")
        # 禁用代理以避免代理连接错误
        proxies = {'http': None, 'https': None}
        response = requests.get(url, headers=headers, proxies=proxies, stream=True, timeout=30)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"  成功保存到: {save_path}")
    except Exception as e:
        print(f"  下载图片失败: {e}")

def get_hd_image_url(driver, detail_page_url):
    try:
        driver.get(detail_page_url)
        wait = WebDriverWait(driver, 20)
        try:
            cookie_wait = WebDriverWait(driver, 3) 
            accept_button = cookie_wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
            accept_button.click()
            time.sleep(0.5)
        except Exception:
            pass
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.media img")))
        raw_url = element.get_attribute('src')
        return raw_url.split("/revision/latest")[0] if "/revision/latest" in raw_url else raw_url
    except Exception as e:
        print(f"  获取页面信息失败: {e}")
        return None

def main():
    """主函数 - 采用高效的前置检查策略"""
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
        print(f"创建目录: {SAVE_DIR}")

    # 步骤1: 快速获取全量信息
    print("正在检查已下载的文件...")
    try:
        existing_files = set(os.listdir(SAVE_DIR))
        print(f"发现 {len(existing_files)} 个已存在的文件。")
    except OSError as e:
        print(f"错误：无法读取目录 {SAVE_DIR}，程序退出: {e}")
        return

    gallery_links = get_gallery_links(START_URL)
    if not gallery_links:
        print("未能获取任何图集链接，程序退出。")
        return

    # 步骤2: 智能过滤 - 在启动浏览器前完成
    print("\n正在过滤列表，只找出需要下载的缺失图片...")
    urls_to_process = []
    for url in gallery_links:
        try:
            # 直接从详情页URL推断出文件名
            potential_filename = requests.utils.unquote(url.split('File:')[1])
            if potential_filename not in existing_files:
                urls_to_process.append(url)
        except IndexError:
            # 如果某个URL不含'File:'，作为异常情况，还是加入处理列表
            urls_to_process.append(url) 

    total_to_process = len(urls_to_process)
    print(f"过滤完成。共有 {len(gallery_links)} 张图片，其中 {total_to_process} 张需要下载。")

    if total_to_process == 0:
        print("\n所有图片均已下载。任务完成！")
        return

    # 步骤3: 精准执行 - 只对过滤后的列表启动Selenium
    print("\n正在启动 Selenium 浏览器驱动...")
    options = EdgeOptions()
    options.page_load_strategy = 'eager'
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")
    options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
    
    driver = None
    try:
        service = EdgeService(executable_path="msedgedriver.exe", service_args=['--log-level=OFF'])
        driver = webdriver.Edge(service=service, options=options)
        
        print(f"Selenium 浏览器驱动已启动，开始处理 {total_to_process} 个任务...\n")

        for i, detail_url in enumerate(urls_to_process):
            print(f"--- 处理缺失图片 {i+1}/{total_to_process}: {detail_url} ---")
            
            hd_image_url = get_hd_image_url(driver, detail_url)
            
            if hd_image_url:
                filename = requests.utils.unquote(hd_image_url.split('/')[-1])
                save_path = os.path.join(SAVE_DIR, filename)
                download_image(hd_image_url, save_path)
            else:
                print(f"未能获取高清图URL，请在下次运行时重试。")
            
            time.sleep(0.5)
            
    except Exception as e:
        print(f"\n程序主流程发生严重错误: {e}")
    finally:
        if driver:
            driver.quit()
            print("\nSelenium 浏览器驱动已关闭。")
            
    print("\n所有任务完成！")

if __name__ == '__main__':
    main()
