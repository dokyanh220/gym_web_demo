import os
import re

replacements = {
    # Menu & General
    ">Home<": ">Trang chủ<",
    ">About Us<": ">Về chúng tôi<",
    ">Classes<": ">Lớp học<",
    ">Services<": ">Dịch vụ<",
    ">Our Team<": ">Đội ngũ<",
    ">Pages<": ">Trang<",
    ">About us<": ">Về chúng tôi<",
    ">Classes timetable<": ">Lịch học<",
    ">Bmi calculate<": ">Tính BMI<",
    ">Our team<": ">Đội ngũ<",
    ">Gallery<": ">Thư viện ảnh<",
    ">Our blog<": ">Blog<",
    ">Contact<": ">Liên hệ<",
    
    # Header & Footer text
    "333 Middle Winchendon Rd, Rindge,<br/> NH 03461": "333 Đường Nguyễn Trãi, Quận 1,<br/> TP. Hồ Chí Minh",
    "125-711-811": "0912 345 678",
    "125-668-886": "0987 654 321",
    "Support.gymcenter@gmail.com": "hotro.gymcenter@gmail.com",
    ">Useful links<": ">Liên kết hữu ích<",
    ">About<": ">Giới thiệu<",
    ">Blog<": ">Blog<",
    ">Login<": ">Đăng nhập<",
    ">My account<": ">Tài khoản của tôi<",
    ">Subscribe<": ">Đăng ký<",
    ">Tips & Guides<": ">Mẹo & Hướng dẫn<",
    ">Physical fitness may help prevent depression, anxiety<": ">Tập thể dục có thể giúp ngăn ngừa trầm cảm, lo âu<",
    ">3 min read<": ">3 phút đọc<",
    ">20 Comment<": ">20 Bình luận<",
    ">Fitness: The best exercise to lose belly fat and tone up...<": ">Thể hình: Bài tập tốt nhất để giảm mỡ bụng và săn chắc...<",
    "Search here.....": "Tìm kiếm tại đây.....",
    
    # Dates and common words
    "by Admin": "bởi Quản trị viên",
    "Aug,15, 2019": "15 Thg 8, 2019",
    "Aug 20, 2019": "20 Thg 8, 2019",
    "Aug 15, 2019": "15 Thg 8, 2019",
    
    # Categories & Tags
    ">Categories<": ">Danh mục<",
    ">Yoga ": ">Yoga ",
    ">Runing ": ">Chạy bộ ",
    ">Weightloss ": ">Giảm cân ",
    ">Cario ": ">Cardio ",
    ">Body buiding ": ">Thể hình ",
    ">Nutrition ": ">Dinh dưỡng ",
    ">Feature posts<": ">Bài viết nổi bật<",
    ">Latest posts<": ">Bài viết mới nhất<",
    ">Popular tags<": ">Thẻ phổ biến<",
    ">Gyming<": ">Tập Gym<",
    ">Body buidling<": ">Thể hình<",
    ">Body buiding<": ">Thể hình<",
    ">Weightloss<": ">Giảm cân<",
    ">Proffeponal<": ">Chuyên nghiệp<",
    ">Streching<": ">Giãn cơ<",
    ">Cardio<": ">Cardio<",
    ">Karate<": ">Karate<",
    ">Yoga<": ">Yoga<",
    
    # Names
    "Lena Mollein": "Lan Lê",
    "Brandon Kelley": "Bình Khang",
    "MEIKE PETERS": "MAI PHƯƠNG",
    "Athart Rachel": "An Như",
    "RLefew D. Loee": "Lê Đăng Khôi",
    "Keaf Shen": "Kiên Sơn",
    "Kimberly Stone": "Kim Oanh",
    "Rachel Adam": "Thảo Anh",
    "Robert Cage": "Quốc Cường",
    "Donald Grey": "Đức Giang",
    
    # blog-details.html
    ">Workout nutrition explained. What to eat before, during, and after exercise.<": ">Giải thích về dinh dưỡng khi tập luyện. Ăn gì trước, trong và sau khi tập.<",
    ">You Can Buy For Less Than A College Degree<": ">Bạn Có Thể Mua Với Giá Rẻ Hơn Một Bằng Đại Học<",
    ">The whole family of tiny legumes, whether red, green, yellow, or black, offers so many possibilities to create an exciting lunch.<": ">Toàn bộ các loại đậu nhỏ, dù đỏ, xanh, vàng hay đen, đều mang đến nhiều khả năng để tạo ra một bữa trưa thú vị.<",
    ">Share<": ">Chia sẻ<",
    ">Comment<": ">Bình luận<",
    ">Leave a comment<": ">Để lại bình luận<",
    'placeholder="Name"': 'placeholder="Tên"',
    'placeholder="Email"': 'placeholder="Email"',
    'placeholder="Website"': 'placeholder="Trang web"',
    'placeholder="Comment"': 'placeholder="Bình luận"',
    ">Submit<": ">Gửi<",
    
    # blog.html
    ">Our Blog<": ">Blog của chúng tôi<",
    ">Vegan White Peach Mug Cobbler With Cardam Vegan White Peach Mug Cobbler...<": ">Bánh Đào Trắng Thuần Chay Với Bạch Đậu Khấu...<",
    ">Next<": ">Tiếp theo<",
    ">This Japanese Way of Making Iced Coffee Is a Game...<": ">Cách Pha Cà Phê Đá Của Người Nhật Này Sẽ Thay Đổi...<",
    ">Grilled Potato and Green Bean Salad<": ">Salad Khoai Tây Nướng và Đậu Cô Ve<",
    ">The $8 French Rosé I Buy in Bulk Every Summer<": ">Chai Vang Hồng Pháp 190.000 VNĐ Tôi Mua Số Lượng Lớn Mỗi Mùa Hè<",
    ">Ina Garten's Skillet-Roasted Lemon Chicken<": ">Gà Nướng Chanh Bằng Chảo Của Ina Garten<",
    ">The Best Weeknight Baked Potatoes, 3 Creative Ways<": ">Khoai Tây Nướng Cho Bữa Tối Tuyệt Nhất, 3 Cách Sáng Tạo<",
    
    # bmi-calculator.html
    ">BMI calculator<": ">Công cụ tính BMI<",
    ">check your body<": ">kiểm tra cơ thể bạn<",
    ">BMI CALCULATOR CHART<": ">BẢNG TÍNH BMI<",
    ">Bmi<": ">BMI<",
    ">WEIGHT STATUS<": ">TÌNH TRẠNG CÂN NẶNG<",
    ">Below 18.5<": ">Dưới 18.5<",
    ">Underweight<": ">Thiếu cân<",
    ">Healthy<": ">Khỏe mạnh<",
    ">Overweight<": ">Thừa cân<",
    ">30.0 - and Above<": ">30.0 - trở lên<",
    ">Obese<": ">Béo phì<",
    ">CALCULATE YOUR BMI<": ">TÍNH BMI CỦA BẠN<",
    'placeholder="Height / cm"': 'placeholder="Chiều cao / cm"',
    'placeholder="Weight / kg"': 'placeholder="Cân nặng / kg"',
    'placeholder="Age"': 'placeholder="Tuổi"',
    'placeholder="Sex"': 'placeholder="Giới tính"',
    ">Calculate<": ">Tính toán<",
    
    # class-details.html
    ">Classes detail<": ">Chi tiết lớp học<",
    ">Trainer<": ">Huấn luyện viên<",
    ">Gym Trainer<": ">Huấn luyện viên Gym<",
    ">Age<": ">Tuổi<",
    ">Weight<": ">Cân nặng<",
    "148lbs": "67kg",
    ">Height<": ">Chiều cao<",
    "10' 2``": "1m88",
    ">Occupation<": ">Nghề nghiệp<",
    "no-founder": "đồng sáng lập",
    ">Monday<": ">Thứ Hai<",
    ">Tuesday<": ">Thứ Ba<",
    ">Wednesday<": ">Thứ Tư<",
    ">Thursday<": ">Thứ Năm<",
    ">Friday<": ">Thứ Sáu<",
    ">Saturday<": ">Thứ Bảy<",
    ">Sunday<": ">Chủ Nhật<",
    ">WEIGHT LOOSE<": ">Giảm Cân<",
    ">Fitness<": ">Thể Hình<",
    ">Boxing<": ">Boxing<",
    ">Body Building<": ">Thể Hình<"
}

# Apply replacements to dummy text paragraphs too.
lorem_replacements = {
    ">Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua accusantium doloremque laudantium. Excepteur sint occaecat cupidatat non proident sculpa .<": ">Chào mừng bạn đến với trung tâm thể hình của chúng tôi. Chúng tôi cung cấp các dịch vụ tập luyện tốt nhất với cơ sở vật chất hiện đại và đội ngũ huấn luyện viên chuyên nghiệp. Hãy tham gia cùng chúng tôi để đạt được mục tiêu sức khỏe của bạn.<",
    ">laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat anim id est laborum.<": ">Chúng tôi cam kết mang đến cho bạn những trải nghiệm tập luyện tuyệt vời nhất. Các chương trình đa dạng từ cơ bản đến nâng cao phù hợp với mọi lứa tuổi và trình độ.<",
    ">Dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur officia deserunt mollit.<": ">Tập luyện đều đặn không chỉ giúp cải thiện vóc dáng mà còn tăng cường sức khỏe tinh thần. Đừng ngần ngại, hãy bắt đầu hành trình của bạn ngay hôm nay.<",
    ">Dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.<": ">Chúng tôi hiểu rằng mỗi người có một cơ địa khác nhau. Do đó, các bài tập sẽ được thiết kế riêng biệt để đảm bảo hiệu quả tối đa và an toàn tuyệt đối cho bạn.<",
    ">Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in. . Sed ut perspiciatis unde omnis iste natus error sit voluptatem.<": ">Khám phá sức mạnh tiềm ẩn trong bạn. Bằng sự quyết tâm và kiên trì, không có mục tiêu nào là không thể đạt được. Chúng tôi sẽ đồng hành cùng bạn.<",
    ">laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed eiusmod tempor incididunt laboris nisi ut aliquip commodo consequat. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Mauris vel magna ex. Integer gravida tincidunt accumsan. Vestibulum nulla mauris, condimentum id felis ac, volutpat volutpat mi qui dolorem.<": ">Chế độ dinh dưỡng kết hợp cùng các bài tập chuẩn khoa học sẽ tạo ra sự khác biệt lớn. Hãy tham khảo ý kiến chuyên gia của chúng tôi để có thực đơn phù hợp nhất.<",
    ">Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation.<": ">Chuyên gia dinh dưỡng và huấn luyện viên cá nhân với hơn 10 năm kinh nghiệm.<",
    ">Neque porro quisquam est, qui dolorem ipsum dolor sit amet, consectetur, adipisci velit dolore.<": ">Bài viết rất hữu ích. Cảm ơn bạn đã chia sẻ những thông tin này.<",
    ">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore dolore magna aliqua endisse ultrices gravida lorem.<": ">Khởi đầu hành trình thay đổi bản thân cùng chúng tôi. Trung tâm tập thể hình hàng đầu với trang thiết bị hiện đại và đội ngũ chuyên nghiệp.<",
    ">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed eiusmod tempor incididunt ut labore et dolore magna aliqua accumsan lacus facilisis.<": ">Một bài viết tuyệt vời về phong cách sống lành mạnh và những thói quen tốt cần duy trì hàng ngày để có sức khỏe dẻo dai.<",
    ">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Quis ipsum suspendisse ultrices gravida. Risus commodo viverra maecenas accumsan lacus vel facilisis.<": ">Công cụ tính BMI của chúng tôi sẽ giúp bạn theo dõi tình trạng cơ thể một cách chính xác. Từ đó đưa ra những điều chỉnh phù hợp trong ăn uống và tập luyện.<",
    ">Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua accusantium doloremque laudantium. Excepteur sint occaecat cupidatat non proident sculpa.<": ">Lớp thể hình được thiết kế dành riêng cho những ai muốn phát triển cơ bắp và tăng cường sức mạnh. Các bài tập tạ kết hợp cùng máy móc chuyên dụng sẽ giúp bạn đạt kết quả nhanh chóng.<",
    ">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua viverra maecenas lacus vel facilisis.<": ">Với hơn 10 năm kinh nghiệm huấn luyện, tôi tự tin sẽ giúp bạn thay đổi vóc dáng và sức khỏe tốt nhất.<",
    ">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua viverra maecenas lacus vel facilisis. <": ">Sự hài lòng của học viên chính là thành công lớn nhất của tôi. Hãy cùng nhau chinh phục thử thách mới.<"
}

files_to_process = [
    r"C:\workspace\gym.com\blog-details.html",
    r"C:\workspace\gym.com\blog.html",
    r"C:\workspace\gym.com\bmi-calculator.html",
    r"C:\workspace\gym.com\class-details.html"
]

for file_path in files_to_process:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Apply general replacements
    for k, v in replacements.items():
        content = content.replace(k, v)

    # Apply lorem replacements
    for k, v in lorem_replacements.items():
        content = content.replace(k, v)
        
    # Replace "By Admin" variations not caught
    content = content.replace("by Admin", "bởi Quản trị viên")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Translation completed successfully.")
