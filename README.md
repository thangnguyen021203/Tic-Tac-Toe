# Step to A.I

    *Đây là một project nho nhỏ của mình từng bước tham gia vào cộng đồng A.I.*

**Mục đích project:** Củng cố kiến thức về thuật toán q-learning của Reinforce-learning.

**Giới thiệu về project:** 
* Mình làm project này sau khi học lý thuyết về q-learning.
* q-learning: về cơ bản đây là thuật toán ánh xạ (state,action) vào một q-value, từ đó ta có một q-table chứa các q-value. Ở một state ta sẽ chọn ra action có q-value cao nhất để chuyển sang state mới. Sau đó, ta sẽ cập nhật lại giá trị q-value mới cho state đó. Mỗi episode chúng ta train cho modal, q-value trong q-table sẽ hội tụ về giá trị optimal.
* tic-tac-toe: Hay còn gọi là caro. Về nguyên bản đây là trò chơi caro với kích thước 3x3. Nguyên tắc của trò chơi là player có 3 nước liền kề (hàng, cột, đường chéo) sẽ chiến thắng.