import pytest
from selenium import webdriver

@pytest.fixture(scope="function")
def driver():
    """
    Fixture khởi tạo và giải phóng WebDriver sau mỗi ca kiểm thử.
    Sử dụng Selenium Manager mặc định của Selenium 4 (không cần webdriver-manager bên ngoài).
    Thử khởi tạo trình duyệt Edge trước (đã được tối ưu hóa trên Windows), 
    nếu thất bại sẽ chuyển sang Chrome làm dự phòng.
    """
    driver_instance = None
    
    # 1. Cấu hình Microsoft Edge (Mặc định cho Windows)
    edge_options = webdriver.EdgeOptions()
    edge_options.add_argument("--headless=new")
    edge_options.add_argument("--disable-gpu")
    edge_options.add_argument("--no-sandbox")
    edge_options.add_argument("--disable-dev-shm-usage")
    edge_options.add_argument("--window-size=1280,800")
    edge_options.add_argument("--lang=en-US")
    
    # 2. Cấu hình Chrome (Dự phòng)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1280,800")
    chrome_options.add_argument("--lang=en-US")
    
    try:
        # Thử khởi tạo Edge
        driver_instance = webdriver.Edge(options=edge_options)
    except Exception as edge_error:
        print(f"\n[Warning] Không thể khởi tạo Edge Driver: {edge_error}. Đang thử khởi tạo Chrome...")
        try:
            # Thử khởi tạo Chrome làm phương án dự phòng
            driver_instance = webdriver.Chrome(options=chrome_options)
        except Exception as chrome_error:
            raise RuntimeError(
                f"Không thể khởi tạo cả Edge và Chrome WebDriver bằng Selenium Manager.\n"
                f"Lỗi Edge: {edge_error}\n"
                f"Lỗi Chrome: {chrome_error}"
            )
            
    # Thiết lập Implicit Wait (Chờ ngầm định 10 giây)
    driver_instance.implicitly_wait(10)
    
    yield driver_instance
    
    # Đóng trình duyệt sau khi kiểm thử hoàn thành
    if driver_instance:
        driver_instance.quit()
