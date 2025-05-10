import os
import csv

# Nhập đường dẫn folder chứa file .txt
root_folder = input("Nhập đường dẫn folder chứa file .txt: ")
csv_path = input("Nhập đường dẫn file .csv muốn xuất ra: ")

# Danh sách tên file cần lọc (ở đây chỉ xử lý passwords.txt)
allowed_filenames = {"passwords.txt"}

# Các trường dữ liệu cố định (các cột bạn cần)
fields = ["File Name", "File Path", "Soft", "Host", "Login", "Password"]

with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
    # Sử dụng DictWriter để đảm bảo mỗi key của record được ghi vào cột tương ứng
    writer = csv.DictWriter(csv_file, fieldnames=fields, delimiter=',')
    writer.writeheader()  # Ghi dòng tiêu đề

    # Duyệt qua tất cả thư mục và file trong root_folder
    for foldername, subfolders, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith('.txt') and filename in allowed_filenames:
                txt_path = os.path.join(foldername, filename)
                # Khởi tạo bản ghi với File Name và File Path
                record = {"File Name": filename, 
                          "File Path": os.path.relpath(txt_path, root_folder)}
                
                try:
                    with open(txt_path, 'r', encoding='utf-8') as txt_file:
                        for line in txt_file:
                            # Lấy line đã cắt khoảng trắng đầu và cuối
                            stripped_line = line.strip()
                            
                            # Nếu line có định dạng "Key: Value", thêm vào record
                            if ": " in stripped_line:
                                key, value = stripped_line.split(": ", 1)
                                record[key] = value
                            # Nếu gặp dòng trống (hoặc dòng không chứa ': '), coi như ranh giới kết thúc một record
                            elif stripped_line == "":
                                # Nếu bản ghi hiện có chứa một số thông tin (ví dụ: trường "Soft" đã có), ghi record ra CSV
                                if any(record.get(field, "") for field in fields[2:]):
                                    writer.writerow({field: record.get(field, "") for field in fields})
                                # Sau đó, reset record để xử lý nhóm thông tin tiếp theo,
                                # giữ lại File Name và File Path đã cho sẵn
                                record = {"File Name": filename, 
                                          "File Path": os.path.relpath(txt_path, root_folder)}
                        # Sau khi đọc hết file, nếu record chứa thông tin (không trống) thì ghi vào CSV
                        if any(record.get(field, "") for field in fields[2:]):
                            writer.writerow({field: record.get(field, "") for field in fields})
                    print(f"✔ Đã xử lý: {txt_path}")
                except Exception as e:
                    print(f"❌ Lỗi khi đọc {txt_path}: {e}")

print(f"\n🎉 Hoàn tất! Đã xuất dữ liệu sang: {csv_path}")
