const totalSalesBox = document.getElementById("total-sales");
const totalOrdersBox = document.getElementById("total-orders");
const maxOrderValueBox = document.getElementById("max-order-value");
const totalProductsSoldBox = document.getElementById("total-products-sold");
const averageOrderValue = document.getElementById("average-order-value")

function updateDashboard() {
    fetch("/metrics")
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            totalSalesBox.querySelector(".metric-value").innerHTML = `$${parseFloat(
                data.total_sales
            ).toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2,
            })}`;
            totalOrdersBox.querySelector(".metric-value").textContent =
                data.total_orders.toLocaleString();
            maxOrderValueBox.querySelector(
                ".metric-value"
            ).innerHTML = `$${parseFloat(data.max_order_value).toLocaleString(
                undefined,
                { minimumFractionDigits: 2, maximumFractionDigits: 2 }
            )}`;
            totalProductsSoldBox.querySelector(".metric-value").textContent =
                data.total_products_sold.toLocaleString();
            averageOrderValue.querySelector(
                ".metric-value"
            ).innerHTML = `$${parseFloat(data.average_order_value).toLocaleString(
                undefined,
                { minimumFractionDigits: 2, maximumFractionDigits: 2 }
            )}`;
        })
        .catch((error) => {
            console.error("Error fetching metrics:", error);
        });
}

function animateBoxes() {
    const metricBoxes = document.querySelectorAll(".metric-box");
    metricBoxes.forEach((box, index) => {
        const delay = parseFloat(box.dataset.delay) || 0;
        setTimeout(() => {
            box.classList.add("animate-up");
        }, delay * 500);
    });
}

window.onload = () => {
    animateBoxes();
    updateDashboard(); // Initial data load
    setInterval(updateDashboard, 500); // Poll every 500 ms
};
