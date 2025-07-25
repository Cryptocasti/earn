import time
import random
import requests
import multiprocessing
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_selenium_instance(link):
    print(f" Starting processing for link: {link}")
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)

    driver.get(link)
    time.sleep(5)

    def safe_click(el):
        try:
            el.click()
        except:
            try:
                driver.execute_script("arguments[0].click();", el)
            except:
                ActionChains(driver).move_to_element(el).click().perform()

    # Step 1: Click overlay
    try:
        print(" Clicking overlay")
        overlay = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[style*='position:fixed'][style*='z-index:2147483647']")))
        safe_click(overlay)
        time.sleep(2)
    except Exception as e:
        print(" Failed to click overlay:", e)

    # Step 2: Click video
    try:
        print(" Clicking video 4 times")
        video_tag = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "video.jw-video")))
        for i in range(4):
            print(f" Click attempt {i+1}")
            safe_click(video_tag)
            time.sleep(1)
    except Exception as e:
        print(" Failed to click video:", e)

    # Step 3: Wait for video to play
    print(" Waiting 240 seconds to simulate video playback...")
    time.sleep(240)

    # Step 4: Take screenshot
    screenshot_path = f"screenshot_{int(time.time())}.png"
    driver.save_screenshot(screenshot_path)
    print(f" Screenshot saved: {screenshot_path}")

    # Step 5: Click download button
    try:
        print("Clicking download button 3 times")
        for i in range(3):
            download_btn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(@href, 'download') and contains(@class, 'submit-btn')]")
            ))
            safe_click(download_btn)
            time.sleep(1)
    except Exception as e:
        print(" Failed to click download button:", e)

    driver.quit()
    print(f"Finished processing link: {link}")

def run_earn_parallel():
    try:
        # URL cũ
        old_url = "https://raw.githubusercontent.com/talblubClouby96/videzz_video/refs/heads/main/link_temp.txt"
        response_old = requests.get(old_url)
        response_old.raise_for_status()
        old_links = response_old.text.strip().splitlines()
        print(f"Loaded {len(old_links)} links from old URL.")

        # URL mới
        new_url = "https://raw.githubusercontent.com/talblubClouby96/videzz_video/refs/heads/main/earnvids.txt"
        response_new = requests.get(new_url)
        response_new.raise_for_status()
        new_links = response_new.text.strip().splitlines()
        print(f"Loaded {len(new_links)} links from new URL.")

        # Lấy 1 link từ old, 2 links từ new
        selected_old = random.sample(old_links, 3)
        selected_new = random.sample(new_links, 3)
        selected_links = selected_old + selected_new

        print(f"Selected {len(selected_links)} links for processing:")
        for link in selected_links:
            print(f" - {link}")

        # Tiếp tục xử lý selected_links với multiprocessing hoặc các bước khác

    except Exception as e:
        print(f"Failed to load link list: {e}")
        return

    #num_processes = 4
    #selected_links = random.sample(link_list, num_processes)

    processes = []
    for link in selected_links:
        p = multiprocessing.Process(target=run_selenium_instance, args=(link,))
        processes.append(p)
        p.start()
        time.sleep(2)

    for p in processes:
        p.join()

    print("All earn processes completed.")
