document.getElementById('checkout-form').addEventListener('submit', function (event) {
    const form = event.target;

    const address = form.address.value.trim();
    if (address.length < 5 || address.length > 255) {
        alert("Address must be between 5 and 255 characters.");
        event.preventDefault();
        return;
    }
});
