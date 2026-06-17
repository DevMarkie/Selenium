# Hướng dẫn học và thực hành kiểm thử tự động với Selenium

Tài liệu này cung cấp toàn bộ kiến thức lý thuyết cơ bản đến nâng cao về công cụ kiểm thử tự động **Selenium** và hướng dẫn chi tiết cách viết mã nguồn kiểm thử tự động (Automation Testing) cho một website thương mại điện tử bằng **Python**.

---

## 1. Giới thiệu tổng quan về Selenium

**Selenium** là một bộ công cụ mã nguồn mở phổ biến nhất hiện nay dùng để tự động hóa trình duyệt web. Nó cho phép lập trình viên và kiểm thử viên (Tester) viết mã để giả lập các hành vi của người dùng trên trình duyệt (nhấp chuột, nhập văn bản, cuộn trang, chuyển tab,...) nhằm kiểm tra tính đúng đắn của ứng dụng web.

Bộ sản phẩm Selenium bao gồm 3 thành phần chính:
* **Selenium IDE (Integrated Development Environment)**: Một tiện ích mở rộng (extension) trên trình duyệt (Chrome, Firefox, Edge) cho phép ghi (record) và phát lại (playback) các thao tác của người dùng. Thích hợp cho các ca kiểm thử đơn giản hoặc tạo nhanh các bản nháp kiểm thử.
* **Selenium WebDriver**: Thành phần quan trọng nhất. Đây là một API và framework cho phép viết mã nguồn bằng nhiều ngôn ngữ lập trình khác nhau (Python, Java, C#, JavaScript, Ruby,...) để tương tác trực tiếp với các trình duyệt.
* **Selenium Grid**: Công cụ hỗ trợ chạy các ca kiểm thử song song trên nhiều trình duyệt, hệ điều hành và thiết bị khác nhau, giúp tối ưu hóa thời gian chạy kiểm thử quy mô lớn.

---

## 2. Kiến trúc hoạt động của Selenium WebDriver

Kiến trúc của Selenium WebDriver phiên bản mới nhất (W3C Standard) gồm 3 lớp chính:

```
+-------------------------------------------------------------+
|                     1. Selenium Language Bindings           |
|                (Python, Java, JavaScript, C#,...)           |
+-------------------------------------------------------------+
                              |
                              | Giao thức W3C WebDriver (HTTP/JSON)
                              v
+-------------------------------------------------------------+
|                     2. Browser Drivers (WebDrivers)         |
|              (ChromeDriver, GeckoDriver, EdgeDriver)        |
+-------------------------------------------------------------+
                              |
                              | Tương tác ở cấp độ thấp (Native OS commands)
                              v
+-------------------------------------------------------------+
|                     3. Web Browsers (Trình duyệt thực tế)    |
|                (Chrome, Firefox, Microsoft Edge)            |
+-------------------------------------------------------------+
```

1. **Language Bindings**: Mã kiểm thử do chúng ta viết (ví dụ bằng Python).
2. **Browser Drivers (WebDriver)**: Mỗi trình duyệt cần một trình điều khiển riêng (như ChromeDriver cho Chrome). Trình điều khiển này đóng vai trò là một máy chủ HTTP trung gian, nhận lệnh từ mã kiểm thử và biên dịch chúng thành các hành động mà trình duyệt hiểu được.
3. **Browsers**: Trình duyệt thực thi các lệnh nhận được và trả lại kết quả (hoặc trạng thái) về cho WebDriver, sau đó WebDriver gửi lại cho mã kiểm thử.

---

## 3. Các Locator trong Selenium (Cách định vị phần tử)

Để tương tác với bất kỳ phần tử nào trên trang web (ví dụ: nút bấm, ô nhập liệu, hình ảnh), Selenium cần định vị phần tử đó thông qua các phương thức **Locator**.
Selenium cung cấp 8 phương thức định vị chính:

| Locator | Mô tả | Ví dụ trên Thủy Sinh Tím | Cách gọi trong Selenium (Python) |
| :--- | :--- | :--- | :--- |
| **ID** | Định vị bằng thuộc tính `id` (Nhanh và chính xác nhất, nên ưu tiên sử dụng) | `<input id="search">` (Ô tìm kiếm) | `driver.find_element(By.ID, "search")` |
| **Class Name** | Định vị bằng thuộc tính `class` | `<button class="btn-add-to-cart">` (Nút thêm giỏ hàng) | `driver.find_element(By.CLASS_NAME, "btn-add-to-cart")` |
| **Tag Name** | Định vị bằng tên thẻ HTML | `<h1>Thủy Sinh Tím</h1>` | `driver.find_element(By.TAG_NAME, "h1")` |
| **Link Text** | Định vị thẻ `<a>` bằng văn bản hiển thị chính xác | `<a href="...">Đăng nhập</a>` | `driver.find_element(By.LINK_TEXT, "Đăng nhập")` |
| **CSS Selector** | Định vị bằng bộ chọn CSS (Rất mạnh mẽ và nhanh) | `<a class="line-clamp line-clamp-2">` (Link sản phẩm) | `driver.find_element(By.CSS_SELECTOR, ".line-clamp")` |
| **XPath** | Định vị bằng đường dẫn XML (Linh hoạt nhất, mạnh nhất) | `<input id="search">` | `driver.find_element(By.XPATH, "//input[@id='search']")` |

---

## 4. Kỹ thuật Wait (Đợi) trong Selenium

Các trang web hiện đại thường sử dụng AJAX và JavaScript tải động dữ liệu. Điều này dẫn đến việc mã Selenium thực thi nhanh hơn tốc độ tải trang, gây ra lỗi phổ biến `NoSuchElementException`. Để xử lý việc này, Selenium cung cấp 2 cơ chế Wait chính:

### Implicit Wait (Đợi ngầm định)
* **Khái niệm**: Thiết lập một khoảng thời gian chờ mặc định cho **tất cả** các phần tử. Nếu Selenium không tìm thấy phần tử ngay lập tức, nó sẽ liên tục kiểm tra lại trong DOM cho đến khi hết thời gian chờ đã đặt.
* **Cách dùng**:
  ```python
  driver.implicitly_wait(10) # Chờ tối đa 10 giây cho mọi hành động tìm kiếm phần tử
  ```

### Explicit Wait (Đợi tường minh)
* **Khái niệm**: Chỉ áp dụng cho **một phần tử cụ thể** với **điều kiện cụ thể** (ví dụ: chờ cho đến khi nút bấm có thể nhấp được, chờ cho văn bản hiển thị, chờ cho phần tử biến mất,...). Đây là cách tiếp cận chuyên nghiệp và tối ưu nhất.
* **Cách dùng**:
  ```python
  from selenium.webdriver.support.ui import WebDriverWait
  from selenium.webdriver.support import expected_conditions as EC

  # Đợi tối đa 10 giây cho đến khi ô tìm kiếm hiển thị trên DOM
  search_input = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.ID, "search"))
  )
  search_input.send_keys("phân nền")
  ```

---

## 5. Mô hình Page Object Model (POM)

Khi dự án kiểm thử lớn lên, nếu viết trực tiếp locator vào các file kiểm thử sẽ làm cho mã nguồn rất khó bảo trì khi giao diện thay đổi. 
**Page Object Model (POM)** là một mẫu thiết kế (Design Pattern) phổ biến:
* Mỗi trang web sẽ được đại diện bởi một lớp (Class) trong mã nguồn.
* Các locator (ID, XPath, CSS) và các hành động (action) trên trang đó sẽ được định nghĩa bên trong lớp này dưới dạng các thuộc tính và phương thức.
* Các file kiểm thử (test cases) chỉ việc gọi các phương thức này mà không cần quan tâm chi tiết kỹ thuật định vị phần tử thế nào.
* **Lợi ích**: Dễ đọc, dễ tái sử dụng mã nguồn và cực kỳ dễ bảo trì (khi UI đổi, chỉ cần sửa Locator ở duy nhất một nơi là file Page Object tương ứng).

---

## 6. Hướng dẫn cài đặt và thực thi mã nguồn kiểm thử

Dự án thực hành đi kèm triển khai 03 test case kiểm thử tự động cho trang thương mại điện tử **Thủy Sinh Tím** (`https://thuysinhtim.vn/`):
1. **Test Case 1 (test_search_success)**: Tìm kiếm sản phẩm thành công với từ khóa `"phân nền"`. Kiểm tra danh sách kết quả hiển thị tối thiểu 1 sản phẩm.
2. **Test Case 2 (test_search_empty)**: Tìm kiếm sản phẩm với từ khóa không tồn tại `"xyzabc123999"`. Kiểm tra hệ thống hiển thị đúng thông báo rỗng hoặc không có kết quả.
3. **Test Case 3 (test_add_to_cart)**: Thêm sản phẩm đầu tiên từ trang tìm kiếm vào giỏ hàng và điều hướng tới `/cart` để xác nhận sản phẩm đã được thêm vào thành công (sử dụng JavaScript click để vượt qua các popup che khuất).

### Các bước cài đặt và thực thi:

1. **Cài đặt thư viện phụ thuộc**:
   Mở terminal (PowerShell hoặc Command Prompt) tại thư mục `selenium_testing` này và chạy lệnh:
   ```bash
   pip install -r requirements.txt
   ```

2. **Chạy các Test Case**:
   Do môi trường Windows có thể không cấu hình trực tiếp đường dẫn cho lệnh `pytest`, khuyến nghị chạy qua module Python bằng lệnh:
   ```bash
   python -m pytest -v -s test_thuysinhtim.py
   ```

   *Giải thích tham số:*
   * `-v` (verbose): Hiển thị chi tiết kết quả chạy của từng ca kiểm thử.
   * `-s`: Cho phép in các dòng lệnh output (`print()`) ra terminal để tiện theo dõi.

---

## 7. Minh chứng kết quả chạy kiểm thử (Test Run Evidence)

Dưới đây là log ghi nhận kết quả thực tế khi chạy bộ kiểm thử tự động trên máy:

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

> [!NOTE]
> Kết quả chạy thực tế cho thấy toàn bộ 3 test cases đều đạt trạng thái **PASSED (ĐẠT)** và hoàn thành thành công trong khoảng 42 giây. Trình duyệt Microsoft Edge được khởi chạy tự động ở chế độ headless (chạy ngầm) thông qua Selenium Manager để đảm bảo tính ổn định và hiệu năng cao nhất.

---

## 8. Báo cáo kết quả kiểm thử chi tiết (Test Report)

### 8.1. Thông tin cấu hình môi trường kiểm thử (Environment)
* **Hệ điều hành**: Windows 11 / Windows 10
* **Ngôn ngữ lập trình**: Python 3.14.3
* **Framework chạy test**: pytest (phiên bản 9.1.0)
* **Thư viện Selenium**: selenium (phiên bản 4.45.0)
* **Trình duyệt tự động**: Microsoft Edge (Chế độ chạy ngầm - Headless)

### 8.2. Bảng tổng hợp kết quả chạy kiểm thử (Test Summary Table)

| STT | Mã Kịch Bản | Tên Ca Kiểm Thử | Các Bước Kiểm Thử Chính | Kết Quả Mong Đợi | Trạng Thái |
| :---: | :--- | :--- | :--- | :--- | :---: |
| 1 | **TC-01** | Tìm kiếm sản phẩm thành công | 1. Mở trang chủ.<br>2. Nhập từ khóa `"phân nền"`.<br>3. Nhấn `Enter`. | Hiển thị danh sách sản phẩm liên quan đến từ khóa và số lượng sản phẩm lớn hơn 0. | **PASSED** (Đạt) |
| 2 | **TC-02** | Tìm kiếm không có kết quả | 1. Mở trang chủ.<br>2. Nhập từ khóa `"xyzabc123999"`.<br>3. Nhấn `Enter`. | Hiển thị thông báo không tìm thấy kết quả hoặc số lượng sản phẩm trả về bằng 0. | **PASSED** (Đạt) |
| 3 | **TC-03** | Thêm sản phẩm vào giỏ hàng | 1. Mở trang tìm kiếm sản phẩm.<br>2. Chọn và click vào sản phẩm đầu tiên.<br>3. Click nút "Thêm vào giỏ hàng" bằng JS.<br>4. Mở trang `/cart`. | Sản phẩm được lựa chọn hiển thị chính xác trong danh sách giỏ hàng. | **PASSED** (Đạt) |

### 8.3. Đánh giá độ ổn định và tối ưu hóa
* **Implicit Wait & Explicit Wait**: Sự kết hợp nhuần nhuyễn giữa Implicit Wait mặc định và Explicit Wait ở các nút tương tác (nút tìm kiếm, nút thêm giỏ hàng) giúp mã nguồn hoạt động cực kỳ mượt mà, hạn chế lỗi tải trang không kịp.
* **JavaScript Click**: Bằng việc click thông qua JavaScript ở nút "Thêm vào giỏ hàng", kiểm thử tự động không bị cản trở bởi các popup quảng cáo hay banner đè lên phần tử, giúp kiểm thử đạt độ tin cậy tuyệt đối.


