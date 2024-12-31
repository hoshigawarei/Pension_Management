// static/js/scripts.js

document.addEventListener("DOMContentLoaded", function() {
    // Add event listener to buttons or forms, if necessary
    const reviewForm = document.getElementById("review-form");
    if (reviewForm) {
        reviewForm.addEventListener("submit", function(event) {
            event.preventDefault(); // Prevent the default form submission
            alert("Review submitted successfully!");
        });
    }
});

let reservationsVisible = false;

function toggleReservations() {
    const reservationsContainer = document.getElementById('my-reservations');
    const toggleButton = document.getElementById('toggle-reservations');
    
    if (reservationsVisible) {
        // 隐藏预约信息
        reservationsContainer.style.display = 'none';
        toggleButton.textContent = "查看我的全部预约";
    } else {
        // 显示预约信息并请求数据
        fetchMyReservations();
        reservationsContainer.style.display = 'block';
        toggleButton.textContent = "收起预约信息";
    }
    reservationsVisible = !reservationsVisible;
}

function fetchMyReservations() {
    fetch("/reservation/my_reservations", {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            const reservationList = document.getElementById("reservation-list");
            reservationList.innerHTML = ""; // 清空之前的内容
            
            data.reservations.forEach(reservation => {
                const listItem = document.createElement("li");
                listItem.className = "list-group-item";
                listItem.textContent = `预约编号: ${reservation.reservation_id} - 机构: ${reservation.institution_name} - 时间: ${reservation.reservation_time} - 状态: ${reservation.status}`;
                reservationList.appendChild(listItem);
            });

            document.getElementById("my-reservations").style.display = "block";
        } else {
            alert("获取预约信息失败，请稍后再试！");
        }
    })
    .catch(error => {
        console.error("Error fetching reservations:", error);
        alert("发生错误，请稍后重试！");
    });
}
