const bar = document.getElementById('bar');
const close = document.getElementById('close');
const nav = document.getElementById('navbar');

if (bar) {
  bar.addEventListener('click', () => {
    nav.classList.add('active');
  });
}

if (close) {
  close.addEventListener('click', () => {
    nav.classList.remove('active');
  });
}

document.addEventListener("DOMContentLoaded", function () {
  const sizeButtons = document.querySelectorAll(".size-btn");
  const priceElement = document.getElementById("price");

  sizeButtons.forEach(button => {
      button.addEventListener("click", function () {
          // Remove 'active' class from all buttons
          sizeButtons.forEach(btn => btn.classList.remove("active"));
          
          // Add 'active' class to the clicked button
          this.classList.add("active");

          // Update price
          const selectedPrice = this.getAttribute("data-price");
          priceElement.textContent = `$${selectedPrice} TWD`;
      });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const container = document.getElementById("product-container");
  const products = Array.from(container.children); // Get all products as an array

  // Shuffle function (Fisher-Yates Algorithm)
  function shuffle(array) {
      for (let i = array.length - 1; i > 0; i--) {
          const j = Math.floor(Math.random() * (i + 1));
          [array[i], array[j]] = [array[j], array[i]]; // Swap elements
      }
  }

  shuffle(products); // Shuffle products

  // Clear and re-append shuffled products
  container.innerHTML = "";
  products.forEach(product => container.appendChild(product));
});
