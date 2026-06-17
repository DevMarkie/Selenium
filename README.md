# BÁO CÁO THỰC HÀNH: KIỂM THỬ TỰ ĐỘNG VỚI SELENIUM

* **Môn học**: Đánh giá và kiểm định chất lượng phần mềm
* **Đề tài**: Xây dựng bộ ca kiểm thử tự động (Automation Testing Suite) cho website thương mại điện tử
* **Website thử nghiệm**: Thủy Sinh Tím (`https://thuysinhtim.vn/`)
* **Công cụ áp dụng**: Selenium WebDriver & Pytest (Python)

---

## 1. Mục tiêu báo cáo
* Tìm hiểu và ứng dụng công cụ Selenium WebDriver trong việc tự động hóa các thao tác kiểm thử trên trình duyệt web.
* Xây dựng tối thiểu 03 kịch bản kiểm thử tự động (Test Cases) cho các chức năng cốt lõi của website thương mại điện tử thực tế bao gồm: Tìm kiếm sản phẩm thành công, Tìm kiếm không có kết quả và Thêm sản phẩm vào giỏ hàng.
* Chạy thực nghiệm bộ kiểm thử và ghi nhận kết quả làm minh chứng đánh giá chất lượng phần mềm.

---

## 2. Cơ sở lý thuyết áp dụng
Trong bài thực hành này, các kỹ thuật kiểm thử tự động cốt lõi của Selenium đã được áp dụng bao gồm:
* **Selenium WebDriver**: Sử dụng API của Selenium 4 kết hợp với trình điều khiển Microsoft Edge Driver chạy ở chế độ ẩn danh và chạy ngầm (Headless Mode) để tăng tốc độ và tính ổn định.
* **Định vị phần tử (Locators)**: Sử dụng các locator tối ưu:
  * Định vị bằng **ID** (`By.ID, "search"`) cho ô tìm kiếm.
  * Định vị bằng **CSS Selector** (`By.CSS_SELECTOR, ".line-clamp"`) để định vị các phần tử liên kết sản phẩm.
  * Định vị bằng **CSS Selector phức hợp** (`button.btn-add-to-cart, button.add_to_cart_2`) cho nút thêm vào giỏ hàng.
* **Cơ chế đợi (Waits)**: Sử dụng **Explicit Wait** (`WebDriverWait` kết hợp `expected_conditions`) để đợi các phần tử xuất hiện động trên DOM trước khi tương tác, giúp loại bỏ lỗi tải trang không kịp (`NoSuchElementException`).
* **JavaScript Click**: Sử dụng lệnh thực thi script của trình duyệt để click trực tiếp vào phần tử trong DOM, giúp vượt qua các lớp phủ quảng cáo hoặc banner của website thực tế.

---

## 3. Danh sách các ca kiểm thử (Test Cases Specification)

### TC-01: Tìm kiếm sản phẩm thành công với từ khóa hợp lệ
* **Mục tiêu**: Kiểm tra tính đúng đắn của tính năng tìm kiếm khi người dùng nhập từ khóa có tồn tại.
* **Các bước thực hiện**:
  1. Truy cập trang chủ `https://thuysinhtim.vn/`.
  2. Định vị ô tìm kiếm có thuộc tính `id="search"`.
  3. Nhập từ khóa `"phân nền"` và gửi phím `Enter`.
  4. Đợi trang kết quả tìm kiếm tải xong (URL chứa cụm từ `/search`).
  5. Đếm số lượng thẻ sản phẩm có class `.line-clamp`.
* **Kết quả mong đợi**: Hệ thống chuyển hướng thành công và hiển thị danh sách sản phẩm lớn hơn 0.

### TC-02: Tìm kiếm không có kết quả với từ khóa không tồn tại
* **Mục tiêu**: Xác minh tính năng tìm kiếm xử lý chính xác khi người dùng tìm kiếm từ khóa không có trên hệ thống.
* **Các bước thực hiện**:
  1. Truy cập trang chủ `https://thuysinhtim.vn/`.
  2. Nhập từ khóa ngẫu nhiên `"xyzabc123999"` vào ô tìm kiếm và nhấn `Enter`.
  3. Đợi trang kết quả tìm kiếm chuyển đổi thành công.
  4. Kiểm tra sự xuất hiện của thông báo rỗng trong nội dung trang web.
* **Kết quả mong đợi**: Hệ thống hiển thị thông báo không tìm thấy sản phẩm hoặc số lượng sản phẩm trả về bằng 0.

### TC-03: Thêm sản phẩm vào giỏ hàng thành công
* **Mục tiêu**: Kiểm tra luồng nghiệp vụ thêm sản phẩm vào giỏ hàng và kiểm tra tính chính xác của giỏ hàng.
* **Các bước thực hiện**:
  1. Truy cập trực tiếp trang tìm kiếm từ khóa `"phan nen"`.
  2. Click chọn sản phẩm hợp lệ đầu tiên hiển thị trên kết quả.
  3. Hệ thống chuyển hướng tới trang chi tiết sản phẩm. Lưu lại tên sản phẩm.
  4. Tìm nút "Thêm vào giỏ hàng" và click bằng phương thức JavaScript click.
  5. Đợi 4 giây để cookie/session cập nhật dữ liệu.
  6. Truy cập trang giỏ hàng tại `/cart`.
  7. Kiểm tra các liên kết trong giỏ hàng xem có khớp với tên sản phẩm đã thêm.
* **Kết quả mong đợi**: Tên sản phẩm đã chọn xuất hiện chính xác trong trang giỏ hàng.

---

## 4. Cấu trúc mã nguồn dự án
Bộ mã nguồn kiểm thử tự động được tổ chức như sau:
* **`requirements.txt`**: Khai báo các thư viện phụ thuộc (`selenium`, `pytest`).
* **`conftest.py`**: Định nghĩa fixture khởi tạo và đóng trình duyệt WebDriver (Edge/Chrome) tự động sau mỗi ca kiểm thử.
* **`test_thuysinhtim.py`**: Triển khai mã nguồn chi tiết cho 3 ca kiểm thử bằng Python và các assertion kiểm tra điều kiện đầu ra.

---

## 5. Môi trường kiểm thử và Hướng dẫn thực thi

### Môi trường hệ thống:
* **Hệ điều hành**: Windows (10/11)
* **Phiên bản Python**: 3.14.3
* **Thư viện Selenium**: 4.45.0
* **Framework kiểm thử**: pytest (9.1.0)
* **Trình duyệt tự động**: Microsoft Edge (Chế độ Headless - Chạy ngầm)

### Lệnh thực thi kiểm thử:
Để chạy toàn bộ kịch bản kiểm thử và hiển thị báo cáo chi tiết, mở terminal tại thư mục này và chạy lệnh:
```bash
python -m pytest -v -s test_thuysinhtim.py
```

---

## 6. Kết quả thực nghiệm và Minh chứng (Test Execution Results)

Bộ kiểm thử đã được chạy thành công trên máy. Dưới đây là kết quả log chi tiết trả về từ framework pytest làm minh chứng:

```text
============================= test session starts =============================
platform win32 -- Python 3.14.3, pytest-9.1.0, pluggy-1.6.0 -- C:\Python314\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Public\Learn Phenikaa\Third year\Semester 3\Đánh gia và kiểm định chất lượng phần mêm\hu\selenium_testing
collecting ... collected 3 items

test_thuysinhtim.py::test_search_success 
--- Starting Test Case 1: Search Success ---
Navigated to: https://thuysinhtim.vn/search?query=ph%C3%A2n+n%E1%BB%81n
Product count: 12
--- Test Case 1: PASSED ---
PASSED
test_thuysinhtim.py::test_search_empty 
--- Starting Test Case 2: Search Empty ---
Empty search message verified.
--- Test Case 2: PASSED ---
PASSED
test_thuysinhtim.py::test_add_to_cart 
--- Starting Test Case 3: Add to Cart ---
Selected product: 'Phần Nền Akadama Light SS'
Clicked Add to Cart button via JS.
Waiting for cart to update...
Product 'Phần Nền Akadama Light SS' confirmed in cart.
--- Test Case 3: PASSED ---
PASSED

============================= 3 passed in 42.03s ==============================
```

### Đánh giá kết quả:
* **Tỷ lệ thành công**: **100% (3/3 ca kiểm thử vượt qua thành công)**.
* **Thời gian thực thi**: 42.03 giây (Trung bình ~14 giây/test case).
* **Kết luận**: Website Thủy Sinh Tím đáp ứng tốt các chức năng tìm kiếm sản phẩm (thành công & báo lỗi trống) và chức năng thêm sản phẩm vào giỏ hàng hoạt động chính xác trong điều kiện tự động hóa.
