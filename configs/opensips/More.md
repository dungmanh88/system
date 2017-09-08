https://www.youtube.com/watch?v=gDpe1fyRaZw

Got stuck:
opensips.org
users@opensips.org
opensips tag on stackoverflow.com
#opensips on freenode

Routing opensips to FS node
- stateless routing:
pros
- Fast
- Không cần giám sát nhiều, dễ cài đặt

cons:
- Mất cân bằng phân tải cuộc gọi
- Mất cân bằng phân bố tài nguyên

- stateful routing:
Nó nhận thức được các kênh (video, call, text)
Nó cân bằng đều hơn stateless routing, opensips sẽ forward call đến FS hiện đang
xử lý ít cuộc gọi hơn

Nhưng vấn đề xử lý ít việc nhưng việc nào cũng nặng thì server FS đó không phải là lựa
chọn tốt để route.

-> do đó hai vấn đề thách thức với opensips là
- CPU (giám sát tải của FS backend)
- session (giám sát số call đang xử lý của FS backend)

Bằng cách nào opensips biết các thông tin này, FS phải phản hồi lại các thông tin này
để FS biết

-> về mặt kỹ thuật opensips sẽ subscribe các event trên FS để đưa ra các quyết định route.
các event tra về opensips qua các heartbeat msg. FS cần cài đặt event socket module
để có thêm một event socket layer, opensips sẽ liên tục lắng nghe event từ event socket
port 8021

subscribe, giống như đăng ký việc cập nhật internal state sẽ do FS chủ động đẩy về
cho đối tượng subscribe (nhận tin thụ động)

Các thông tin quan trọng nhất là:
- Idle CPU: giá trị CPU
- Max-session: số session tối đa
- Session-Count: số session hiện tại

Opensips dispatcher - stateless routing and balancing
- Algorithm:
+ random
+ weighted rr
+ hash (call-id, from, to, R-URI - là cái gì)

Chỉ cần opensips load được driver ESL và kết nối đến Event socket port trên FS là xong.

Opensisp loadbalancer - stateful routing and balancing

Chiến nào:
