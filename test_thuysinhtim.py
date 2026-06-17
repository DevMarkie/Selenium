import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# URL của website Thủy Sinh Tím
BASE_URL = "https://thuysinhtim.vn/"

def test_search_success(driver):
    """
    Test Case 1: Kiểm thử chức năng tìm kiếm thành công với từ khóa hợp lệ
    - Truy cập trang chủ
    - Định vị ô tìm kiếm có ID là 'search'
    - Nhập từ khóa 'phân nền' và nhấn Enter
    - Chờ trang kết quả tìm kiếm tải xong (URL chứa '/search')
    - Kiểm tra xem kết quả trả về có chứa sản phẩm hay không (dựa trên class '.line-clamp')
    """
    print("\n--- Starting Test Case 1: Search Success ---", flush=True)
    driver.get(BASE_URL)
    
    # 1. Định vị ô tìm kiếm
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "search"))
    )
    
    # 2. Nhập từ khóa và gửi
    search_keyword = "phân nền"
    search_input.send_keys(search_keyword)
    search_input.send_keys(Keys.ENTER)
    
    # 3. Đợi trang chuyển sang kết quả tìm kiếm
    WebDriverWait(driver, 10).until(EC.url_contains("/search"))
    print(f"Navigated to: {driver.current_url}", flush=True)
    
    # 4. Kiểm tra sự xuất hiện của các phần tử sản phẩm (class '.line-clamp')
    products = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".line-clamp"))
    )
    
    product_count = len(products)
    print(f"Product count: {product_count}", flush=True)
    
    assert product_count > 0, "Tìm kiếm thành công nhưng không hiển thị sản phẩm nào!"
    print("--- Test Case 1: PASSED ---", flush=True)


def test_search_empty(driver):
    """
    Test Case 2: Kiểm thử chức năng tìm kiếm với từ khóa không tồn tại
    - Truy cập trang chủ
    - Định vị ô tìm kiếm
    - Nhập từ khóa ngẫu nhiên không tồn tại (ví dụ: 'xyzabc123999') và nhấn Enter
    - Chờ trang kết quả tìm kiếm tải xong
    - Kiểm tra xem trang có thông báo không tìm thấy kết quả hay không
    """
    print("\n--- Starting Test Case 2: Search Empty ---", flush=True)
    driver.get(BASE_URL)
    
    # 1. Định vị ô tìm kiếm
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "search"))
    )
    
    # 2. Nhập từ khóa không tồn tại
    fake_keyword = "xyzabc123999"
    search_input.send_keys(fake_keyword)
    search_input.send_keys(Keys.ENTER)
    
    # 3. Đợi chuyển đổi URL
    WebDriverWait(driver, 10).until(EC.url_contains("/search"))
    
    # 4. Quét nội dung body để tìm các từ khóa báo rỗng
    body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
    
    # Xác nhận xuất hiện các từ khóa báo lỗi/rỗng như "không tìm thấy" hoặc "không có" hoặc "0 kết quả"
    has_empty_message = any(msg in body_text for msg in ["không tìm thấy", "không có", "0 kết quả", "0 sản phẩm"])
    
    assert has_empty_message or len(driver.find_elements(By.CSS_SELECTOR, ".line-clamp")) == 0, \
        "Vẫn tìm thấy sản phẩm hoặc không hiển thị thông báo rỗng khi tìm kiếm từ khóa không tồn tại!"
    
    print("Empty search message verified.", flush=True)
    print("--- Test Case 2: PASSED ---", flush=True)


def test_add_to_cart(driver):
    """
    Test Case 3: Kiểm thử thêm sản phẩm vào giỏ hàng thành công
    - Đi thẳng đến trang tìm kiếm 'phân nền'
    - Click vào sản phẩm đầu tiên hiển thị ở kết quả tìm kiếm
    - Đợi trang chi tiết sản phẩm hiển thị và lưu lại tên sản phẩm
    - Nhấn nút 'Thêm vào giỏ hàng' sử dụng JavaScript click để tránh lỗi bị popup che khuất
    - Chờ 4 giây cho session giỏ hàng được cập nhật
    - Điều hướng đến trang giỏ hàng (/cart)
    - Xác nhận sản phẩm đã xuất hiện trong giỏ hàng (bằng cách so sánh tên sản phẩm)
    """
    print("\n--- Starting Test Case 3: Add to Cart ---", flush=True)
    
    # 1. Mở trang kết quả tìm kiếm phân nền
    driver.get(f"{BASE_URL}search?query=phan+nen")
    
    # 2. Lấy link và click sản phẩm đầu tiên
    products = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".line-clamp"))
    )
    
    # Tìm liên kết hợp lệ đầu tiên không phải link chính sách
    target_product_lnk = None
    for prod in products:
        href = prod.get_attribute("href")
        if href and "thuysinhtim.vn" in href and not any(pol in href for pol in ["policy", "van-chuyen", "thanh-toan", "don-hang"]):
            target_product_lnk = prod
            break
            
    assert target_product_lnk is not None, "Không tìm thấy sản phẩm hợp lệ nào trong kết quả tìm kiếm!"
    
    expected_product_name = target_product_lnk.text.strip()
    product_url = target_product_lnk.get_attribute("href")
    
    # In ra dạng an toàn ASCII cho log
    safe_name_log = expected_product_name.encode('ascii', 'replace').decode('ascii')
    print(f"Selected product: '{safe_name_log}'", flush=True)
    
    # Click mở trang chi tiết sản phẩm
    driver.get(product_url)
    
    # 3. Định vị nút "Thêm vào giỏ hàng"
    add_to_cart_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn-add-to-cart, button.add_to_cart_2, button.add_to_cart"))
    )
    
    # 4. Thực thi click bằng JavaScript
    driver.execute_script("arguments[0].click();", add_to_cart_btn)
    print("Clicked Add to Cart button via JS.", flush=True)
    
    # Chờ 4 giây để dữ liệu giỏ hàng được đồng bộ ở máy chủ/cookie
    print("Waiting for cart to update...", flush=True)
    time.sleep(4)
    
    # 5. Đi tới trang giỏ hàng
    driver.get(f"{BASE_URL}cart")
    
    # Xác nhận tiêu đề trang chứa chữ 'Giỏ hàng'
    assert "giỏ hàng" in driver.title.lower(), "Không điều hướng được tới trang giỏ hàng!"
    
    # 6. Kiểm tra xem sản phẩm đã có trong giỏ hàng hay chưa
    cart_links = driver.find_elements(By.TAG_NAME, "a")
    product_in_cart = False
    
    for lnk in cart_links:
        lnk_text = lnk.text.strip()
        lnk_href = lnk.get_attribute("href") or ""
        # So sánh tên sản phẩm hoặc đường dẫn sản phẩm
        if product_url in lnk_href or expected_product_name.lower() in lnk_text.lower():
            product_in_cart = True
            break
            
    assert product_in_cart, f"Sản phẩm '{safe_name_log}' không tìm thấy trong giỏ hàng sau khi thêm!"
    print(f"Product '{safe_name_log}' confirmed in cart.", flush=True)
    print("--- Test Case 3: PASSED ---", flush=True)
