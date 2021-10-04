function addToCart(id, name, price) {
    fetch("/api/add-item-cart", {
        method: 'post',
        body: JSON.stringify({
            "product_id": id,
            "name": name,
            "price": price
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(function(res) {
        console.info(res)
        return res.json()
    }).then(function(data) {
        console.info(data)

        let counter = document.getElementById("cartCounter")
        if (counter !== null)
            counter.innerText = data.total_quantity
    })
}