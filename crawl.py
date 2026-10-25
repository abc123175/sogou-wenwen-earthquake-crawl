from playwright.sync_api import sync_playwright
import csv
import time

def crawl_sogou_wenwen(keyword="地震", page_num=2):
    res_list = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        for p_idx in range(1, page_num + 1):
            url = f"https://wenwen.sogou.com/s?query={keyword}&page={p_idx}"
            page.goto(url, timeout=30000)
            time.sleep(4)
            cards = page.locator(".q-item").all()
            for card in cards:
                try:
                    q_title = card.locator(".q-title").inner_text(timeout=2000)
                    q_ans = card.locator(".q-answer").inner_text(timeout=2000)
                    res_list.append({
                        "question": q_title,
                        "answer": q_ans
                    })
                except Exception as e:
                    continue
        browser.close()
    with open("earthquake_data.csv", "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["question", "answer"])
        writer.writeheader()
        writer.writerows(res_list)
    print(f"采集完成，一共{len(res_list)}条，保存至earthquake_data.csv")

if __name__ == "__main__":
    crawl_sogou_wenwen(keyword="地震", page_num=2)
