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
 
          sizeButtons.forEach(btn => btn.classList.remove("active"));

          this.classList.add("active");

          const selectedPrice = this.getAttribute("data-price");
          priceElement.textContent = `$${selectedPrice} TWD`;
      });
  });
});

// --- Existing product shuffling for shop.html ---
document.addEventListener("DOMContentLoaded", function () {
  const container = document.getElementById("product-container-shop");
  if (container) {
    const products = Array.from(container.children); 

    // Shuffle function 
    function shuffle(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]]; // Swap elements
        }
    }

    shuffle(products); 

    container.innerHTML = "";
    products.forEach(product => container.appendChild(product));
  }
});

// --- Product lists for related fragrances ---
const allFragrances = [
  // Men's Fragrances
  {
    imgSrc: "products/JPG LbeauLparfum.jpg",
    company: "Jean Paul Gaultier",
    name: "Le Beau Le Parfum Eau De Parfum Intense",
    price: "3250",
    link: "JPG_LeBeau.html",
    gender: "men"
  },
  {
    imgSrc: "products/LeParfum.jpg",
    company: "Jean Paul Gaultier",
    name: "Le Male Le Parfum",
    price: "3000",
    link: "JPG_LeParfum.html",
    gender: "men"
  },
  {
    imgSrc: "products/BDC chanel.jpg",
    company: "Chanel",
    name: "Bleu de Chanel",
    price: "3650",
    link: "JPG_bdc.html", 
    gender: "men"
  },
  {
    imgSrc: "products/Dior Sauvage.jpg",
    company: "Dior",
    name: "Sauvage",
    price: "3100",
    link: "JPG_sauvage.html", 
    gender: "men"
  },
  {
    imgSrc: "products/armani swyabs.jpg",
    company: "Giorgio Armani",
    name: "Stronger With You Absolutely",
    price: "3300",
    link: "armani_swyabs.html",
    gender: "men"
  },
  {
    imgSrc: "products/Valentino borninroma.jpg",
    company: "Valentino",
    name: "Born in Roma Uomo Intense",
    price: "3430",
    link: "JPG_birui.html", 
    gender: "men"
  },
  {
    imgSrc: "products/eros flame.jpg",
    company: "Versace",
    name: "Eros Flame",
    price: "3000",
    link: "JPG_ef.html",
    gender: "men"
  },
  {
    imgSrc: "products/Althair pdm.jpg",
    company: "Parfum De Marly",
    name: "Althair",
    price: "7000",
    link: "Althair_pdm.html", 
    gender: "men"
  },
  {
    imgSrc: "products/DylanBlueVersace.jpg",
    company: "Versace",
    name: "Dylan Blue Pour Homme",
    price: "2300",
    link: "DylanBlueVersace.html", 
    gender: "men"
  },
  {
    imgSrc: "products/acquaarmaniprofondo.jpg",
    company: "Giorgio Armani",
    name: "Acqua Di Gio Profondo",
    price: "4300",
    link: "acquaarmaniprofondo.html", 
    gender: "men"
  },
  {
    imgSrc: "products/YSL.jpg",
    company: "Yves Saint Laurent",
    name: "YSL Y",
    price: "4100",
    link: "YSL.html", 
    gender: "men"
  },
  {
    imgSrc: "products/YSLMYSLF.avif",
    company: "Yves Saint Laurent",
    name: "MYSLF",
    price: "4000",
    link: "YSLMYSLF.html", 
    gender: "men"
  },
  {
    imgSrc: "products/Creedaventus.jpg",
    company: "Creed",
    name: "Aventus",
    price: "11000",
    link: "Creedaventus.html", 
    gender: "men"
  },
  {
    imgSrc: "products/tomfordtobvan.jpg",
    company: "Tom Ford",
    name: "Tobacco Vanille",
    price: "9550",
    link: "tomfordtobvan.html", 
    gender: "men"
  },
  {
    imgSrc: "products/Azzaromostwanted.webp",
    company: "Azzaro",
    name: "The Most Wanted Parfum",
    price: "2000",
    link: "Azzaromostwanted.html", 
    gender: "men"
  },
  {
    imgSrc: "products/pdm_greenley.jpg",
    company: "Parfum De Marly",
    name: "Greenley Eau De Parfum",
    price: "8200",
    link: "pdm_greenley.html",
    gender: "men"
  },
  {
    imgSrc: "products/god_of_fire.webp",
    company: "Stephane Humbert Lucas",
    name: "God Of Fire Eau De Parfum",
    price: "8400",
    link: "god_of_fire.html",
    gender: "men"
  },

  // Women's Fragrances
  {
    imgSrc: "products/libreYSL.jpg",
    company: "Yves Saint Laurent",
    name: "Libre Eau de Parfum",
    price: "4700",
    link: "YSL_Libre.html", 
    gender: "women"
  },
  {
    imgSrc: "products/ggb_carolina.jpg",
    company: "Carolina Herrera",
    name: "Good Girl Blush Eau de Parfum",
    price: "4000",
    link: "ch_ggb.html",
    gender: "women"
  },
  {
    imgSrc: "products/missdior.jpg",
    company: "Dior",
    name: "Miss Dior",
    price: "3999",
    link: "miss_dior.html",
    gender: "women"
  },
  {
    imgSrc: "products/vltn_dbir.jpg",
    company: "Valentino",
    name: "Donna Born In Roma",
    price: "3999",
    link: "vltn_dbir.html", 
    gender: "women"
  },
  {
    imgSrc: "products/coco_chanel.png",
    company: "Chanel",
    name: "Coco Mademoiselle Eau De Parfum",
    price: "3499",
    link: "coco_mademoiselle.html",
    gender: "women"
  },
  {
    imgSrc: "products/gucci_bloom.jpg",
    company: "Gucci",
    name: "Bloom Eau De Toilette",
    price: "3100",
    link: "gucci_bloom.html",
    gender: "women"
  },
   {
    imgSrc: "products/Baccarat540.jpg",
    company: "Maison Francis Kurkdjian",
    name: "Baccarat Rouge 540",
    price: "8999",
    link: "Baccarat540.html", 
    gender: "women" 
  },
     // nek ada Unisex (add here)
];

/**
 * Shuffles an array in place using the Fisher-Yates algorithm.
 * @param {Array} array The array to shuffle.
 */
function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
}

/**
 * Displays a random selection of products in a specified container,
 * filtering by gender and excluding a specific product.
 * @param {Array} productsList The array of product objects to choose from (all fragrances).
 * @param {string} containerId The ID of the HTML element where products will be displayed.
 * @param {number} count The number of random products to display.
 * @param {string} currentProductName The name of the product on the current page to exclude.
 * @param {string} targetGender The gender category to filter by ('men', 'women', or null for all).
 */
function displayRandomProducts(productsList, containerId, count, currentProductName, targetGender = null) {
  const container = document.getElementById(containerId);
  if (!container) {
    console.error(`Product container with ID '${containerId}' not found.`);
    return;
  }
  
  let availableProducts = productsList.filter(product => {
    const matchesGender = targetGender ? product.gender === targetGender : true;
    const isNotCurrentProduct = product.name !== currentProductName;
    return matchesGender && isNotCurrentProduct;
  });

  shuffleArray(availableProducts);

  const selectedProducts = availableProducts.slice(0, count);

  container.innerHTML = "";

  selectedProducts.forEach(product => {
    const productHtml = `
      <div class="product" onclick="window.location.href='${product.link}'">
          <img src="${product.imgSrc}" alt="${product.name}">
          <div class="des">
              <span>${product.company}</span>
              <h5>"${product.name}"</h5>
              <div class="star">
                  <i class="fas fa-star"></i>
                  <i class="fas fa-star"></i>
                  <i class="fas fa-star"></i>
                  <i class="fas fa-star"></i>
                  <i class="fas fa-star"></i>
              </div>
              <h4>$${product.price} TWD</h4>
          </div>
          <a href="#"><i class="fal fa-solid fa-shopping-cart cart"></i></a>
      </div>
    `;
    container.insertAdjacentHTML('beforeend', productHtml);
  });
}

const pageProductMap = {

  
  "JPG_althair.html": { name: "Althair", gender: "men", containerId: "product-container-related-men", title: "Related men's Fragrances"},
  "god_of_fire.html": { name: "God Of Fire Eau De Parfum", gender: "men", containerId: "product-container-related-men", title: "Related men's Fragrances" },
  "JPG_LeBeau.html": { name: "Le Beau Le Parfum Eau De Parfum Intense", gender: "men", containerId: "product-container-related-men", title: "Related men's Fragrances" },
  "JPG_LeParfum.html": { name: "Le Male Le Parfum", gender: "men", containerId: "product-container-related-men", title: "Related men's Fragrances" },
  "pdm_greenley.html": { name: "Greenley Eau De Parfum", gender: "men", containerId: "product-container-related-men", title: "Related men's Fragrances" },
  "JPG_StrongerWith.html": { name: "Stronger With You Absolutely", gender: "men", containerId: "product-container-related-men", title: "Related men's Fragrances" },
  "JPG_sauvage.html": { name: "Sauvage", gender: "men", containerId: "product-container-related-men", title: "Related men's Fragrances" },
  "JPG_ef.html": { name: "Eros Flame", gender: "men", containerId: "product-container-related-men", title: "Related men's Fragrances" },
  "JPG_birui.html": { name: "Born in Roma Uomo Intense", gender: "men", containerId: "product-container-related-men", title: "Related men's Fragrances" },
  "JPG_bdc.html": { name: "Bleu de Chanel", gender: "men", containerId: "product-container-related-men", title: "Related men's Fragrances" },

  

  "ch_ggb.html": { name: "Good Girl Blush Eau de Parfum", gender: "women", containerId: "product-container-related-women", title: "Related women's Fragrances" },
  "coco_mademoiselle.html": { name: "Coco Mademoiselle Eau De Parfum", gender: "women", containerId: "product-container-related-women", title: "Related women's Fragrances" },
  "miss_dior.html": { name: "Miss Dior", gender: "women", containerId: "product-container-related-women", title: "Related women's Fragrances" },
  "gucci_bloom.html": { name: "Bloom Eau De Toilette", gender: "women", containerId: "product-container-related-women", title: "Related women's Fragrances" },
  "YSL_Libre.html": { name: "Libre Eau de Parfum", gender: "women", containerId: "product-container-related-women", title: "Related women's Fragrances" },
  "vltn_dbir.html": { name: "Donna Born In Roma", gender: "women", containerId: "product-container-related-women", title: "Related women's Fragrances" }
  
  // Add like this nek kon mau add product baru
  // "YSL_Libre.html": { name: "Libre Eau de Parfum", gender: "women", containerId: "product-container-related-women", title: "Related women's Fragrances" },
};


document.addEventListener("DOMContentLoaded", function() {
    const currentPageFileName = window.location.pathname.split('/').pop();
    const pageInfo = pageProductMap[currentPageFileName];

    if (pageInfo) {
        const relatedSectionTitle = document.getElementById('related-products-title');
        if (relatedSectionTitle) {
            relatedSectionTitle.textContent = pageInfo.title;
        }
        const relatedSectionParagraph = document.getElementById('related-products-paragraph');
        if (relatedSectionParagraph) {
            relatedSectionParagraph.textContent = "Explore more products you might like";
        }
        
        displayRandomProducts(
            allFragrances,
            pageInfo.containerId,
            4,
            pageInfo.name,
            pageInfo.gender 
        );
    }
});


document.getElementById('page1-btn')?.addEventListener('click', function (e) {
  e.preventDefault();
  document.getElementById('page1-products').style.display = 'flex';
  document.getElementById('page2-products').style.display = 'none';
});

document.getElementById('page2-btn')?.addEventListener('click', function (e) {
  e.preventDefault();
  document.getElementById('page1-products').style.display = 'none';
  document.getElementById('page2-products').style.display = 'flex';
});

