let globalProducts = [];
let stores = [];

// DOM Elements
const resultsGrid = document.getElementById('resultsGrid');
const storeFiltersContainer = document.getElementById('storeFilters');
const categoryRadios = document.querySelectorAll('input[name="category"]');
const searchInput = document.getElementById('searchInput');
const searchButton = document.getElementById('searchButton');
const sortSelect = document.getElementById('sortSelect');
const loader = document.getElementById('loader');
const resultsTitle = document.getElementById('resultsTitle');

// State
let currentState = {
    query: '',
    category: 'all',
    selectedStores: new Set(),
    sortBy: 'price-asc'
};

// Initialize
async function init() {
    loader.classList.remove('hidden');
    resultsGrid.style.display = 'none';
    
    try {
        const response = await fetch('data.json');
        if (!response.ok) throw new Error('No se pudo cargar data.json');
        
        globalProducts = await response.json();
        stores = [...new Set(globalProducts.map(p => p.store))];
        currentState.selectedStores = new Set(stores);
        
        renderStoreFilters();
        renderProducts();
        setupEventListeners();
    } catch (error) {
        console.error(error);
        resultsGrid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; color: #ff003c; padding: 2rem;">Error cargando datos: ${error.message}</div>`;
        loader.classList.add('hidden');
        resultsGrid.style.display = 'grid';
    }
}

// Render Store Filters dynamically
function renderStoreFilters() {
    storeFiltersContainer.innerHTML = stores.map(store => `
        <label class="custom-radio">
            <input type="checkbox" name="store" value="${store}" checked>
            <span class="radio-btn" style="border-radius: 4px;"></span> ${store}
        </label>
    `).join('');

    // Update checkboxes to have square style by changing the CSS class dynamically or using inline style
    const style = document.createElement('style');
    style.textContent = `
        input[type="checkbox"] + .radio-btn { border-radius: 4px; }
        input[type="checkbox"]:checked + .radio-btn::after { border-radius: 2px; }
    `;
    document.head.appendChild(style);
}

// Format Price to ARS
const formatPrice = (price) => {
    return new Intl.NumberFormat('es-AR', {
        style: 'currency',
        currency: 'ARS',
        maximumFractionDigits: 0
    }).format(price);
};

// Filter and Sort Products
function getFilteredProducts() {
    return globalProducts
        .filter(p => {
            const matchesQuery = p.name.toLowerCase().includes(currentState.query.toLowerCase());
            const matchesCategory = currentState.category === 'all' || p.type === currentState.category;
            const matchesStore = currentState.selectedStores.has(p.store);
            return matchesQuery && matchesCategory && matchesStore;
        })
        .sort((a, b) => {
            if (currentState.sortBy === 'price-asc') return a.price - b.price;
            if (currentState.sortBy === 'price-desc') return b.price - a.price;
            return 0;
        });
}

// Render Products
function renderProducts() {
    resultsGrid.style.display = 'none';
    loader.classList.remove('hidden');

    // Simulate API delay
    setTimeout(() => {
        const filtered = getFilteredProducts();
        
        if (filtered.length === 0) {
            resultsGrid.innerHTML = `
                <div style="grid-column: 1/-1; text-align: center; padding: 3rem; color: var(--text-muted);">
                    <h3>No se encontraron resultados</h3>
                    <p>Prueba con otros términos de búsqueda o filtros.</p>
                </div>
            `;
        } else {
            // Find the minimum price among filtered products
            const minPrice = Math.min(...filtered.map(p => p.price));

            resultsGrid.innerHTML = filtered.map(p => {
                const isBestChoice = p.price === minPrice;
                return `
                <div class="card ${isBestChoice ? 'best-choice' : ''}">
                    ${isBestChoice ? `
                    <div class="best-price-badge">
                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                        Mejor Precio
                    </div>
                    ` : ''}
                    <div class="store-badge">${p.store}</div>
                    <div class="card-img-placeholder">
                        <img src="${p.image}" alt="${p.name}">
                    </div>
                    <h3 class="card-title">${p.name}</h3>
                    <div class="card-price">${formatPrice(p.price)}</div>
                    <a href="${p.storeUrl}" target="_blank" rel="noopener noreferrer" class="card-btn">Ver en Tienda</a>
                </div>
            `}).join('');
        }

        // Update title
        const resultsCount = filtered.length;
        resultsTitle.textContent = currentState.query 
            ? `Resultados para "${currentState.query}" (${resultsCount})`
            : `Todos los productos (${resultsCount})`;

        loader.classList.add('hidden');
        resultsGrid.style.display = 'grid';
    }, 600); // 600ms fake delay for effect
}

// Event Listeners
function setupEventListeners() {
    // Search
    const handleSearch = () => {
        currentState.query = searchInput.value;
        renderProducts();
    };

    searchButton.addEventListener('click', handleSearch);
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSearch();
    });

    // Category Filters
    categoryRadios.forEach(radio => {
        radio.addEventListener('change', (e) => {
            currentState.category = e.target.value;
            renderProducts();
        });
    });

    // Store Filters
    storeFiltersContainer.addEventListener('change', (e) => {
        if (e.target.name === 'store') {
            if (e.target.checked) {
                currentState.selectedStores.add(e.target.value);
            } else {
                currentState.selectedStores.delete(e.target.value);
            }
            renderProducts();
        }
    });

    // Sort
    sortSelect.addEventListener('change', (e) => {
        currentState.sortBy = e.target.value;
        renderProducts();
    });
}

// Start app
init();
