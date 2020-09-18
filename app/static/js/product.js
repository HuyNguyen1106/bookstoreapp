function add_to_cart(id, title, author, price) {
    fetch("/api/cart", {
        method: "post",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            id: id,
            title: title,
            author: author,
            price: price
        })
    }).then(res => res.json()).then(data => {
        var cart = document.getElementById("cartId")
        cart.innerText = data.quantity
        var amount = document.getElementById("cartAmount")
        amount.innerText = data.sum_cart + " VND"
    })
}

function delete_book(bookId) {
    var c = confirm("Ban chac chan xoa khong?");
    if (c == true) {
        fetch("/api/books/" + bookId, {
            method: "delete"
        }).then(function(res) {
            return res.json();
        }).then(function(data) {
            console.info(data);
            var bId = data.data.book_id;
            var p = document.getElementById("book" + bId);
            p.style.display = "none";
        }).catch(function(err) {
            console.error(err);
        });
    }
}

function pay() {
    if (confirm("Bạn chắc chắn thanh toán?") == true) {
        fetch("/api/pay", {
            "method": "post",
            "headers": {
                "Content-Type": "application/json"
            }
        }).then(res => res.json()).then(data => {
            if (data.status == 200) {
                location.reload()
            } else {
                alert("Thanh toán thất bại")
            }
        }).catch(err => alert("HỆ THỐNG LỖI!!!"))
    }
}
function payByPaypal() {
    if (confirm("Bạn chắc chắn thanh toán?") == true) {
        email = document.getElementById("email")
        fetch("https://svcs.sandbox.paypal.com/AdaptivePayments/Pay", {
            'actionType' => 'PAY',
            'currencyCode' => 'VND',
            'receiverList' => [
                'receiver' => [
                    [
                        'amount' => '10.0',
                        'email' => 'sb-jasnc3246227@personal.example.com',
                    ]
                ],
            ],
            'returnUrl' => '/success.html', //Link sẽ trả về nếu thanh toán thành công
            'cancelUrl' => '/failure.html', // Link trả về nếu giao dịch bị hủy
            'requestEnvelope' => [
                'errorLanguage' => 'en_US',
                'detailLevel' => 'ReturnAll',
            ]
        }).then(res => res.json()).then(data => {
            if (data.status == 200) {
                location.reload()
            } else {
                alert("Thanh toán thất bại")
            }
        }).catch(err => alert("HỆ THỐNG LỖI!!!"))
    }
}

}