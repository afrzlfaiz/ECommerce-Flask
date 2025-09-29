/* ========= Utilities ========= */
window.formatIDR = (n) => new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 }).format(n || 0);

// Toast
function showToast(msg, ms=1800) {
  const wrap = document.getElementById('toast');
  const el = document.createElement('div');
  el.className = 'toast';
  el.textContent = msg;
  wrap.appendChild(el);
  setTimeout(()=>{ el.remove(); }, ms);
}

// Theme
window.__initTheme = function() {
  const icon = document.getElementById('theme-icon');
  const setIcon = () => {
    if (icon) {
      icon.textContent = document.documentElement.classList.contains('dark') ? '🌞' : '🌙';
    }
  };
  
  // Set theme based on localStorage or system preference
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
  
  setIcon();
  
  const btn = document.getElementById('theme-toggle');
  if (btn) {
    btn.addEventListener('click', () => {
      const isDark = document.documentElement.classList.toggle('dark');
      localStorage.theme = isDark ? 'dark' : 'light';
      setIcon();
    });
  }
}

// Auth state helpers - check if user is authenticated by checking if session exists
window.__isAuthed = () => {
  // Check if we have user_id in session (simpler check)
  return !!(window.__userSession && window.__userSession.user_id);
};

// Function to fetch user session status
window.__fetchAuthStatus = async () => {
  try {
    const response = await fetch('/api/auth/me', { credentials: 'include' });
    const data = await response.json();
    if (data.success && data.data && data.data.user_id) {
      window.__userSession = data.data;
      updateAuthUI(true); // Update UI to show logged-in state
      return true;
    }
    window.__userSession = null;
    updateAuthUI(false); // Update UI to show logged-out state
    return false;
  } catch (e) {
    window.__userSession = null;
    updateAuthUI(false); // Update UI to show logged-out state
    return false;
  }
};

// Function to update auth UI elements
function updateAuthUI(isAuthenticated) {
  const loginLink = document.getElementById('login-link');
  const logoutLink = document.getElementById('logout-link');
  if (loginLink) loginLink.style.display = isAuthenticated ? 'none' : 'inline';
  if (logoutLink) logoutLink.style.display = isAuthenticated ? 'inline' : 'none';
}

// Call auth status on page load
// Note: Now handled in the DOMContentLoaded event below

window.__logout = async () => {
  try {
    await fetch('/api/auth/logout', { method: 'POST', credentials: 'include' });
    // kosongkan cache auth di client
    window.__userSession = null;
    updateAuthUI(false);
    // reload agar state lain ikut segar (badge cart, dsb)
    window.location.href = '/';
  } catch (e) {
    showToast('Gagal logout');
  }
};

// Cart badge
window.__initCartBadge = async function() {
  try {
    const r = await fetch('/api/cart', { credentials: 'include' });
    if (!r.ok) return;
    const data = await r.json();
    const items = data.items || data.data || [];
    const cnt = Array.isArray(items) ? items.reduce((s, it)=> s + (it.quantity || 1), 0) : 0;
    const b = document.getElementById('cart-badge');
    if (b) b.textContent = cnt;
  } catch(e){}
};

/* ========= Product Cards ========= */
function productCard(p) {
  const price = formatIDR(p.price);
  const discount = p.discount ? `<span class="absolute left-2 top-2 text-xs px-2 py-1 rounded-lg bg-red-600 text-white">-${p.discount}%</span>` : '';
  const rating = '⭐'.repeat(Math.round(p.rating || 0));
  const img = (p.images && p.images[0]) || p.image || '/static/placeholder.png';
  const name = (p.name || '').length > 60 ? p.name.slice(0,57)+'…' : p.name || '';
  return `
  <a href="/products/${encodeURIComponent(p.id)}" class="block card rounded-2xl border border-slate-200 dark:border-slate-800 p-3">
    <div class="aspect-thumb relative">
      ${discount}
      <img src="${img}" loading="lazy" alt="${name}">
    </div>
    <div class="mt-3">
      <div class="text-sm font-medium leading-tight line-clamp-2">${name}</div>
      <div class="mt-1 text-brand font-bold">${price}</div>
      <div class="mt-1 text-xs text-slate-500 dark:text-slate-400">${rating} · ${(p.sold_count || 0)} terjual</div>
    </div>
    <button class="mt-3 w-full px-3 py-2 rounded-lg border border-slate-300 dark:border-slate-700">Detail</button>
  </a>`;
}

/* ========= Fetch Helpers ========= */
async function fetchJSON(url, opts={}) {
  const res = await fetch(url, { ...opts, headers: { 'Content-Type': 'application/json', ...(opts.headers||{}) }, credentials: 'include' });
  if (!res.ok) {
    // Redirect to login if unauthorized
    if (res.status === 401) {
      window.location.href = '/login';
      return;
    }
    throw new Error(await res.text());
  }
  return res.json();
}

/* ========= Home Page Logic ========= */
async function initHome() {
  const grid = document.getElementById('product-grid');
  const searchInput = document.getElementById('search-products');
  const searchBtn = document.getElementById('search-btn');
  const clearBtn = document.getElementById('clear-search');
  
  if (!grid) return;
  
  let page = 1;
  let sort = 'bestseller';
  let brandFilter = null;
  let searchQuery = null;  // Track current search query

  async function load() {
    const qs = new URLSearchParams({ page, sort, limit: 20 });
    if (brandFilter) qs.set('brand', brandFilter);
    
    let apiUrl = '/api/products';
    if (searchQuery) {
      apiUrl = `/api/products/search?q=${encodeURIComponent(searchQuery)}&${qs.toString()}`;
    } else {
      // Only add brand filter to regular products API if not searching
      if (brandFilter) qs.set('brand', brandFilter);
      apiUrl = `/api/products?${qs.toString()}`;
    }
    
    const data = await fetchJSON(apiUrl);
    const items = data.items || data.data || data || [];
    
    if (page === 1) {
      grid.innerHTML = '';
      if (items.length === 0) {
        grid.innerHTML = '<div class="col-span-full text-center py-8 text-slate-500">Produk tidak ditemukan</div>';
        document.getElementById('load-more')?.remove(); // Remove load more button if no items
        return;
      }
    }
    
    grid.insertAdjacentHTML('beforeend', items.map(productCard).join(''));
    
    // Hide load more button if there are no more items
    const hasMore = data.has_more !== undefined ? data.has_more : items.length === 20; // Assuming 20 is the limit
    const loadMoreBtn = document.getElementById('load-more');
    if (loadMoreBtn) {
      if (!hasMore || items.length < 20) {
        loadMoreBtn.style.display = 'none';
      } else {
        loadMoreBtn.style.display = 'inline-flex'; // Show again if needed
      }
    }
  }
  
  await load();

  document.getElementById('load-more')?.addEventListener('click', async ()=>{
    // Check if there might be more items before loading
    const params = new URLSearchParams({ page: page + 1, sort, limit: 20 });
    if (brandFilter) params.set('brand', brandFilter);
    
    let checkUrl = '/api/products';
    if (searchQuery) {
      checkUrl = `/api/products/search?q=${encodeURIComponent(searchQuery)}&${params.toString()}`;
    } else {
      if (brandFilter) params.set('brand', brandFilter);
      checkUrl = `/api/products?${params.toString()}`;
    }
    
    try {
      const checkData = await fetchJSON(checkUrl);
      const checkItems = checkData.items || checkData.data || checkData || [];
      if (checkItems.length > 0) {
        page += 1;
        await load();
      } else {
        // If no more items, hide the load more button
        document.getElementById('load-more')?.remove();
      }
    } catch (e) {
      console.error('Error checking for more items:', e);
    }
  });

  document.getElementById('sort-select')?.addEventListener('change', async (e)=>{
    sort = e.target.value; 
    page = 1; 
    await load();
  });

  // Handle brand filter buttons
  document.querySelectorAll('[data-brand]').forEach(btn => {
    btn.addEventListener('click', async (e)=>{
      brandFilter = btn.dataset.brand;
      searchQuery = null;  // Clear search when filtering by brand
      if (searchInput) searchInput.value = '';
      page = 1; 
      await load();
      
      // Update URL to reflect brand filter
      const url = new URL(window.location);
      url.searchParams.set('brand', brandFilter);
      url.searchParams.delete('q');  // Remove search query from URL
      window.history.pushState({}, '', url);
    });
  });
  
  // Handle search functionality
  searchBtn?.addEventListener('click', async () => {
    const query = searchInput.value.trim();
    if (query) {
      searchQuery = query;
      brandFilter = null;  // Clear brand filter when searching
      page = 1;
      await load();
      
      // Update URL to reflect search
      const url = new URL(window.location);
      url.searchParams.set('q', query);
      url.searchParams.delete('brand');  // Remove brand filter from URL
      window.history.pushState({}, '', url);
    }
  });
  
  // Add Enter key support for search
  searchInput?.addEventListener('keypress', async (e) => {
    if (e.key === 'Enter') {
      const query = searchInput.value.trim();
      if (query) {
        searchQuery = query;
        brandFilter = null;  // Clear brand filter when searching
        page = 1;
        await load();
        
        // Update URL to reflect search
        const url = new URL(window.location);
        url.searchParams.set('q', query);
        url.searchParams.delete('brand');
        window.history.pushState({}, '', url);
      }
    }
  });
  
  // Clear search functionality
  clearBtn?.addEventListener('click', async () => {
    searchInput.value = '';
    searchQuery = null;
    page = 1;
    
    // Check URL for brand parameter
    const urlParams = new URLSearchParams(window.location.search);
    const initialBrand = urlParams.get('brand');
    brandFilter = initialBrand || null;
    
    await load();
    
    // Update URL to remove search query
    const url = new URL(window.location);
    url.searchParams.delete('q');
    if (brandFilter) {
      url.searchParams.set('brand', brandFilter);
    } else {
      url.searchParams.delete('brand');
    }
    window.history.pushState({}, '', url);
  });
  
  // Handle URL parameters on page load
  const urlParams = new URLSearchParams(window.location.search);
  const initialBrand = urlParams.get('brand');
  const initialQuery = urlParams.get('q');
  
  if (initialQuery) {
    searchQuery = initialQuery;
    if (searchInput) searchInput.value = initialQuery;
  } else if (initialBrand) {
    brandFilter = initialBrand;
  }
  
  if (searchQuery || initialBrand) {
    page = 1;
    await load();
  }
}

/* ========= Products Page Logic ========= */
async function initProducts() {
  const grid = document.getElementById('product-grid');
  const prev = document.getElementById('prev-page');
  const next = document.getElementById('next-page');
  const indicator = document.getElementById('page-indicator');
  const searchInput = document.getElementById('search-products');
  const searchBtn = document.getElementById('search-btn');
  const clearBtn = document.getElementById('clear-search');
  
  if (!grid || !prev || !next || !indicator) return;

  let page = 1;
  let searchQuery = null;  // Track current search query

  async function load() {
    let apiUrl = '/api/products';
    const params = new URLSearchParams({ page, limit: 20 }); // Add limit to parameters
    
    if (searchQuery) {
      apiUrl = `/api/products/search?q=${encodeURIComponent(searchQuery)}&${params.toString()}`;
    } else {
      apiUrl = `/api/products?${params.toString()}`;
    }
    
    const data = await fetchJSON(apiUrl);
    const items = data.items || data.data || data || [];
    
    if (items.length === 0 && page === 1) {
      grid.innerHTML = '<div class="col-span-full text-center py-8 text-slate-500">Produk tidak ditemukan</div>';
      indicator.textContent = `Halaman 0`;
      prev.disabled = true;
      next.disabled = true;
      return;
    } else if (items.length === 0 && page > 1) {
      // If no items on a later page, go back to previous page
      page--;
      await load();
      return;
    }
    
    grid.innerHTML = items.map(productCard).join('');
    indicator.textContent = `Halaman ${page}`;
    
    // Check if there are more items to load
    // Use proper check: if items returned is less than limit, there's no next page
    // Or if the server indicates there's no more data
    const hasMore = data.has_more !== undefined ? data.has_more : items.length === 20; // 20 is our default limit
    prev.disabled = page <= 1;
    next.disabled = !hasMore;
  }

  prev.addEventListener('click', async ()=>{ 
    if (page > 1) { 
      page--; 
      await load(); 
    } 
  });
  
  next.addEventListener('click', async ()=>{ 
    // Only go to next page if there might be more results
    const params = new URLSearchParams({ page: page + 1, limit: 20 });
    let checkUrl = '/api/products';
    
    if (searchQuery) {
      checkUrl = `/api/products/search?q=${encodeURIComponent(searchQuery)}&${params.toString()}`;
    } else {
      checkUrl = `/api/products?${params.toString()}`;
    }
    
    try {
      const checkData = await fetchJSON(checkUrl);
      const checkItems = checkData.items || checkData.data || checkData || [];
      if (checkItems.length > 0) {
        page++;
        await load();
      }
    } catch (e) {
      // If there's an error, don't proceed to next page
      console.error('Error checking next page:', e);
    }
  });

  // Handle search functionality
  searchBtn?.addEventListener('click', async () => {
    const query = searchInput.value.trim();
    if (query) {
      searchQuery = query;
      page = 1;
      await load();
      
      // Update URL to reflect search
      const url = new URL(window.location);
      url.searchParams.set('q', query);
      window.history.pushState({}, '', url);
    }
  });
  
  // Add Enter key support for search
  searchInput?.addEventListener('keypress', async (e) => {
    if (e.key === 'Enter') {
      const query = searchInput.value.trim();
      if (query) {
        searchQuery = query;
        page = 1;
        await load();
        
        // Update URL to reflect search
        const url = new URL(window.location);
        url.searchParams.set('q', query);
        window.history.pushState({}, '', url);
      }
    }
  });
  
  // Clear search functionality
  clearBtn?.addEventListener('click', async () => {
    searchInput.value = '';
    searchQuery = null;
    page = 1;
    await load();
    
    // Update URL to remove search query
    const url = new URL(window.location);
    url.searchParams.delete('q');
    window.history.pushState({}, '', url);
  });
  
  // Handle URL parameters on page load
  const urlParams = new URLSearchParams(window.location.search);
  const initialQuery = urlParams.get('q');
  
  if (initialQuery) {
    searchQuery = initialQuery;
    if (searchInput) searchInput.value = initialQuery;
  }
  
  await load();
}

/* ========= Detail Page Logic ========= */
async function initDetail() {
  const nameEl = document.getElementById('p-name');
  if (!nameEl) return;
  const pathParts = location.pathname.split('/');
  const id = pathParts[pathParts.length - 1];
  try {
    const data = await fetchJSON(`/api/products/${id}`);
    // Perbaikan: Produk ada di data.data, bukan data.item atau langsung data
    const p = data.item || data.data || data;
    
    // Check if product data is valid
    if (!p || !p.id) {
      console.error('Invalid product data received:', data);
      nameEl.textContent = 'Produk tidak ditemukan';
      document.getElementById('p-price').textContent = 'Rp0';
      document.getElementById('p-meta').textContent = '⭐ 0 · 0 terjual';
      return;
    }

    nameEl.textContent = p.name || 'Nama produk tidak tersedia';
    document.getElementById('p-price').textContent = formatIDR(p.price);
    const disc = document.getElementById('p-discount');
    if (p.discount && p.discount > 0) { 
      disc.textContent = `-${p.discount}%`; 
      disc.classList.remove('hidden'); 
    } else {
      disc.classList.add('hidden');
    }
    document.getElementById('p-meta').textContent = `⭐ ${p.rating || 0} · ${(p.sold_count || p.sold || 0)} terjual`;

    // carousel
    const imgs = (p.images && Array.isArray(p.images) && p.images.length) ? p.images : (p.image ? [p.image] : []);
    const track = document.getElementById('carousel-track');
    const dots = document.getElementById('carousel-dots');
    if (track && dots) {
      let idx = 0;
      function renderSlides() {
        if (imgs.length === 0) {
          track.innerHTML = '<div class="w-full h-64 flex items-center justify-center text-gray-500">Tidak ada gambar</div>';
          dots.innerHTML = '';
          return;
        }
        
        track.innerHTML = imgs.map(src => `<img src="${src}" class="inline-block w-full object-cover" style="aspect-ratio: 1/1">`).join('');
        dots.innerHTML = imgs.map((_,i)=> `<button data-i="${i}" class="w-2.5 h-2.5 rounded-full ${i===idx?'bg-brand':'bg-slate-300 dark:bg-slate-700'}"></button>`).join('');
        track.style.transform = `translateX(-${idx*100}%)`;
        dots.querySelectorAll('button').forEach(b => b.addEventListener('click', ()=>{ idx = Number(b.dataset.i); renderSlides(); }));
      }
      renderSlides();
      document.getElementById('carousel-prev')?.addEventListener('click', ()=>{ 
        if (imgs.length > 0) {
          idx = (idx-1+imgs.length)%imgs.length; 
          renderSlides(); 
        }
      });
      document.getElementById('carousel-next')?.addEventListener('click', ()=>{ 
        if (imgs.length > 0) {
          idx = (idx+1)%imgs.length; 
          renderSlides(); 
        }
      });
    }

    // add to cart
    const addToCartBtn = document.getElementById('btn-add-cart');
    if (addToCartBtn) {
      addToCartBtn.addEventListener('click', async ()=>{
        try {
          await fetchJSON('/api/cart', { method: 'POST', body: JSON.stringify({ product_id: p.id, quantity: 1 }) });
          showToast('Ditambahkan ke keranjang');
          window.__initCartBadge && window.__initCartBadge();
        } catch(e){
          showToast('Gagal menambah ke keranjang');
        }
      });
    }
  } catch (error) {
    console.error('Error loading product detail:', error);
    nameEl.textContent = 'Gagal memuat produk';
    document.getElementById('p-price').textContent = 'Rp0';
    document.getElementById('p-meta').textContent = '⭐ 0 · 0 terjual';
  }
}

/* ========= Cart Page Logic ========= */
async function initCart() {
  const body = document.getElementById('cart-body');
  const selectAll = document.getElementById('select-all');
  const deleteSelected = document.getElementById('delete-selected');
  const checkoutSelected = document.getElementById('checkout-selected');
  const selectedItemCount = document.getElementById('selected-item-count');
  
  if (!body) return;

  let cartItems = []; // Store current cart items for reference

  async function load() {
    const data = await fetchJSON('/api/cart');
    cartItems = data.items || data.data || [];
    
    body.innerHTML = cartItems.map((it, index) => `
      <tr class="border-t border-slate-200 dark:border-slate-800">
        <td class="px-4 py-3">
          <input type="checkbox" class="item-checkbox rounded border-slate-300 dark:border-slate-700" data-id="${it.product_id || it.id}" ${it.selected ? 'checked' : ''}>
        </td>
        <td class="px-4 py-3 flex items-center gap-3">
          <img src="${(it.image || (it.images && it.images[0]) || '')}" class="w-12 h-12 rounded-lg object-cover" alt="">
          <div>
            <div class="font-medium">${it.name || it.product_name || ''}</div>
            <div class="text-xs text-slate-500">${it.brand || ''}</div>
          </div>
        </td>
        <td class="px-4 py-3">${formatIDR(it.price)}</td>
        <td class="px-4 py-3">
          <div class="flex items-center gap-2">
            <button class="qty-change text-lg" data-id="${it.product_id || it.id}" data-change="-1">-</button>
            <span class="qty-value" data-id="${it.product_id || it.id}">${it.quantity || 1}</span>
            <button class="qty-change text-lg" data-id="${it.product_id || it.id}" data-change="1">+</button>
          </div>
        </td>
        <td class="px-4 py-3 subtotal" data-id="${it.product_id || it.id}">${formatIDR((it.price || 0) * (it.quantity || 1))}</td>
        <td class="px-4 py-3">
          <button data-id="${it.product_id || it.id}" class="btn-remove px-3 py-1.5 rounded-lg border border-slate-300 dark:border-slate-700">Hapus</button>
        </td>
      </tr>
    `).join('');
    
    updateCartSummary();
    
    // Add event listeners for checkboxes
    document.querySelectorAll('.item-checkbox').forEach(checkbox => {
      checkbox.addEventListener('change', handleItemSelection);
    });
    
    // Add event listeners for quantity buttons
    document.querySelectorAll('.qty-change').forEach(btn => {
      btn.addEventListener('click', async (e) => {
        const productId = e.target.dataset.id;
        const change = parseInt(e.target.dataset.change);
        const qtyElement = document.querySelector(`.qty-value[data-id="${productId}"]`);
        let currentQty = parseInt(qtyElement.textContent) || 1;
        let newQty = Math.max(1, currentQty + change); // Prevent going below 1
        
        try {
          // Update quantity on server
          await fetchJSON('/api/cart/' + productId, { 
            method: 'PUT', 
            body: JSON.stringify({ quantity: newQty }) 
          });
          
          // Update UI
          qtyElement.textContent = newQty;
          updateItemSubtotal(productId, newQty);
          await load(); // Reload to update all calculations
          window.__initCartBadge && window.__initCartBadge();
        } catch(e) {
          showToast('Gagal mengubah jumlah barang');
        }
      });
    });
    
    // Add event listeners for remove buttons
    document.querySelectorAll('.btn-remove').forEach(b => {
      b.addEventListener('click', async (e) => {
        const productId = e.target.dataset.id;
        try {
          await fetchJSON('/api/cart/' + productId, { method: 'DELETE' });
          showToast('Item dihapus');
          await load();
          window.__initCartBadge && window.__initCartBadge();
        } catch(e) {
          showToast('Gagal menghapus item');
        }
      });
    });
    
    // Update select all checkbox state
    const allChecked = cartItems.length > 0 && document.querySelectorAll('.item-checkbox:checked').length === cartItems.length;
    selectAll.checked = allChecked;
  }
  
  function updateItemSubtotal(productId, quantity) {
    const item = cartItems.find(i => (i.product_id || i.id) === productId);
    if (item) {
      const subtotal = item.price * quantity;
      const subtotalElement = document.querySelector(`.subtotal[data-id="${productId}"]`);
      if (subtotalElement) {
        subtotalElement.textContent = formatIDR(subtotal);
      }
    }
  }
  
  function updateCartSummary() {
    const selectedItems = document.querySelectorAll('.item-checkbox:checked');
    const selectedCount = selectedItems.length;
    selectedItemCount.textContent = `(${selectedCount} barang dipilih)`;
    
    // Calculate total for selected items
    let total = 0;
    selectedItems.forEach(checkbox => {
      const productId = checkbox.dataset.id;
      const item = cartItems.find(i => (i.product_id || i.id) === productId);
      if (item) {
        total += (item.price || 0) * (item.quantity || 1);
      }
    });
    
    const totalEl = document.getElementById('cart-total');
    if (totalEl) totalEl.textContent = formatIDR(total);
    
    // Enable/disable buttons based on selection
    deleteSelected.disabled = selectedCount === 0;
    checkoutSelected.disabled = selectedCount === 0;
  }
  
  function handleItemSelection() {
    updateCartSummary();
    // Update select all checkbox state
    const allCheckboxes = document.querySelectorAll('.item-checkbox');
    const selectedCheckboxes = document.querySelectorAll('.item-checkbox:checked');
    selectAll.checked = allCheckboxes.length > 0 && allCheckboxes.length === selectedCheckboxes.length;
  }
  
  // Event listener for select all
  selectAll?.addEventListener('change', function() {
    document.querySelectorAll('.item-checkbox').forEach(checkbox => {
      checkbox.checked = this.checked;
    });
    updateCartSummary();
  });
  
  // Event listener for delete selected
  deleteSelected?.addEventListener('click', async () => {
    const selectedItems = document.querySelectorAll('.item-checkbox:checked');
    if (selectedItems.length === 0) return;
    
    // Create a custom confirmation modal instead of using browser confirm
    const modal = document.createElement('div');
    modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4';
    modal.innerHTML = `
      <div class="bg-white dark:bg-slate-800 rounded-2xl p-6 max-w-md w-full border border-slate-200 dark:border-slate-700">
        <h3 class="text-lg font-semibold mb-2">Konfirmasi Hapus</h3>
        <p class="text-slate-600 dark:text-slate-300 mb-6">Hapus ${selectedItems.length} item dari keranjang?</p>
        <div class="flex gap-3 justify-end">
          <button id="cancel-delete" class="px-4 py-2 rounded-lg border border-slate-300 dark:border-slate-700">Batal</button>
          <button id="confirm-delete" class="px-4 py-2 rounded-lg bg-red-500 text-white hover:bg-red-600">Hapus</button>
        </div>
      </div>
    `;
    
    document.body.appendChild(modal);
    
    document.getElementById('cancel-delete')?.addEventListener('click', () => {
      document.body.removeChild(modal);
    });
    
    document.getElementById('confirm-delete')?.addEventListener('click', async () => {
      document.body.removeChild(modal);
      for (const checkbox of selectedItems) {
        const productId = checkbox.dataset.id;
        try {
          await fetchJSON('/api/cart/' + productId, { method: 'DELETE' });
        } catch(e) {
          showToast(`Gagal menghapus item ${productId}`);
        }
      }
      
      showToast(`${selectedItems.length} item dihapus dari keranjang`);
      await load();
      window.__initCartBadge && window.__initCartBadge();
    });
  });
  
  // Event listener for checkout selected
  checkoutSelected?.addEventListener('click', async () => {
    const selectedCheckboxes = document.querySelectorAll('.item-checkbox:checked');
    if (selectedCheckboxes.length === 0) return;
    
    // Store selected product IDs in localStorage
    const selectedProductIds = Array.from(selectedCheckboxes).map(cb => cb.dataset.id);
    localStorage.setItem('selectedCartItems', JSON.stringify(selectedProductIds));
    
    // Redirect to checkout page
    window.location.href = '/checkout';
  });
  
  await load();
}

/* ========= Checkout Page ========= */
async function initCheckout() {
  const totalEl = document.getElementById('summary-total');
  const addressSelect = document.getElementById('address-select');
  const addressForm = document.getElementById('address-form');
  const newAddressForm = document.getElementById('new-address-form');
  const btnAddAddress = document.getElementById('btn-add-address');
  const btnCancelAddress = document.getElementById('btn-cancel-address');
  const btnDeleteAddress = document.getElementById('btn-delete-address');
  
  if (!totalEl) return;
  
  // Store the selected product IDs so we can use them in the checkout button
  let selectedProductIds = null;
  
  try {
    const r = await fetch('/api/cart', { credentials: 'include' });
    const data = await r.json();
    let items = data.items || data.data || [];
    
    // Check if we have selected items from cart page
    const selectedItemsStr = localStorage.getItem('selectedCartItems');
    if (selectedItemsStr) {
      const selectedIds = JSON.parse(selectedItemsStr);
      // Store for later use in checkout
      selectedProductIds = selectedIds;
      // Filter to only show selected items
      items = items.filter(item => selectedIds.includes(item.product_id || item.id));
      // Remove the stored selection after reading it
      localStorage.removeItem('selectedCartItems');
    }
    
    const total = items.reduce((s, it)=> s + (it.price||0)*(it.quantity||1), 0);
    totalEl.textContent = formatIDR(total);
  } catch(e){}
  
  // Load addresses for the dropdown
  async function loadAddresses() {
    try {
      const response = await fetchJSON('/api/address');
      const addresses = response.data || [];
      
      if (addresses.length === 0) {
        addressSelect.innerHTML = '<option value="">Tidak ada alamat ditemukan. Silakan tambah alamat baru.</option>';
        // Disable delete button when no addresses
        if (btnDeleteAddress) {
          btnDeleteAddress.disabled = true;
        }
        return;
      }
      
      addressSelect.innerHTML = addresses.map(addr => {
        const label = addr.is_default ? `${addr.label} (Utama)` : addr.label;
        return `<option value="${addr.id}" data-is-default="${addr.is_default}">${label}: ${addr.address_line}, ${addr.city}</option>`;
      }).join('');
      
      // Try to select default address if available
      const defaultAddr = addresses.find(addr => addr.is_default);
      if (defaultAddr) {
        addressSelect.value = defaultAddr.id;
      }
      
      // Update delete button state based on selection
      updateDeleteButtonState();
    } catch(e) {
      console.error('Gagal memuat alamat:', e);
      addressSelect.innerHTML = '<option value="">Gagal memuat alamat</option>';
      // Disable delete button on error
      if (btnDeleteAddress) {
        btnDeleteAddress.disabled = true;
      }
      showToast('Gagal memuat alamat');
    }
  }
  
  // Function to update delete button state based on selection
  function updateDeleteButtonState() {
    if (btnDeleteAddress) {
      btnDeleteAddress.disabled = !addressSelect.value;
    }
  }
  
  // Add event listener for address selection change to enable/disable delete button
  addressSelect?.addEventListener('change', updateDeleteButtonState);
  
  // Load addresses initially
  loadAddresses();
  
  // Handle address deletion
  btnDeleteAddress?.addEventListener('click', async () => {
    const selectedAddressId = addressSelect.value;
    if (!selectedAddressId) {
      showToast('Silakan pilih alamat yang akan dihapus');
      return;
    }
    
    // Get the selected address text for confirmation
    const selectedOption = addressSelect.options[addressSelect.selectedIndex];
    const addressText = selectedOption ? selectedOption.text : 'alamat';
    
    // Create a custom confirmation modal instead of using browser confirm
    const modal = document.createElement('div');
    modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4';
    modal.innerHTML = `
      <div class="bg-white dark:bg-slate-800 rounded-2xl p-6 max-w-md w-full border border-slate-200 dark:border-slate-700">
        <h3 class="text-lg font-semibold mb-2">Konfirmasi Hapus Alamat</h3>
        <p class="text-slate-600 dark:text-slate-300 mb-6">Hapus alamat: ${addressText}?</p>
        <div class="flex gap-3 justify-end">
          <button id="cancel-address-delete" class="px-4 py-2 rounded-lg border border-slate-300 dark:border-slate-700">Batal</button>
          <button id="confirm-address-delete" class="px-4 py-2 rounded-lg bg-red-500 text-white hover:bg-red-600">Hapus</button>
        </div>
      </div>
    `;
    
    document.body.appendChild(modal);
    
    document.getElementById('cancel-address-delete')?.addEventListener('click', () => {
      document.body.removeChild(modal);
    });
    
    document.getElementById('confirm-address-delete')?.addEventListener('click', async () => {
      document.body.removeChild(modal);
      
      try {
        await fetchJSON(`/api/address/${selectedAddressId}`, {
          method: 'DELETE'
        });
        
        showToast('Alamat berhasil dihapus');
        
        // Reload addresses
        await loadAddresses();
        
        // Clear selection after deletion
        addressSelect.value = '';
      } catch(e) {
        console.error('Gagal menghapus alamat:', e);
        showToast('Gagal menghapus alamat');
      }
    });
  });
  
  // Show/hide address form
  btnAddAddress?.addEventListener('click', () => {
    addressForm.classList.remove('hidden');
  });
  
  btnCancelAddress?.addEventListener('click', () => {
    addressForm.classList.add('hidden');
    // Clear form fields
    document.getElementById('receiver-name').value = '';
    document.getElementById('address-label').value = '';
    document.getElementById('phone').value = '';
    document.getElementById('postal-code').value = '';
    document.getElementById('address-line').value = '';
    document.getElementById('city').value = '';
    document.getElementById('province').value = '';
    document.getElementById('is-default').checked = false;
  });
  
  // Handle new address form submission
  newAddressForm?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const newAddress = {
      label: document.getElementById('address-label').value,
      receiver_name: document.getElementById('receiver-name').value,
      phone: document.getElementById('phone').value,
      address_line: document.getElementById('address-line').value,
      city: document.getElementById('city').value,
      province: document.getElementById('province').value,
      postal_code: document.getElementById('postal-code').value,
      is_default: document.getElementById('is-default').checked
    };
    
    try {
      await fetchJSON('/api/address', {
        method: 'POST',
        body: JSON.stringify(newAddress)
      });
      
      showToast('Alamat berhasil ditambahkan');
      addressForm.classList.add('hidden');
      
      // Reload addresses
      await loadAddresses();
      
      // Clear form
      newAddressForm.reset();
    } catch(e) {
      console.error('Gagal menambah alamat:', e);
      showToast('Gagal menambah alamat');
    }
  });
  
  // Handle checkout button with address
  document.getElementById('btn-confirm')?.addEventListener('click', async ()=>{
    // Check if an address is selected
    const selectedAddressId = addressSelect.value;
    if (!selectedAddressId) {
      showToast('Silakan pilih alamat pengiriman');
      return;
    }
    
    try {
      const payload = {
        address_id: selectedAddressId
      };
      
      // Include selected product IDs if they exist
      if (selectedProductIds && selectedProductIds.length > 0) {
        payload.product_ids = selectedProductIds;
      }
      
      const response = await fetchJSON('/api/checkout', {
        method: 'POST',
        body: JSON.stringify(payload)
      });
      
      // Redirect to the newly created order detail page
      if (response.data && response.data.order && response.data.order.order_id) {
        const orderId = response.data.order.order_id;
        window.location.href = `/orders/${orderId}`;
      } else {
        // Fallback if order ID is not available in response
        document.getElementById('success')?.classList.remove('hidden');
        showToast('Checkout sukses');
        window.__initCartBadge && window.__initCartBadge();
      }
    } catch(e) {
      console.error('Checkout gagal:', e);
      showToast('Checkout gagal');
    }
  });
}

/* ========= Orders Page ========= */
async function initOrders() {
  const body = document.getElementById('orders-body');
  const searchInput = document.getElementById('search-orders');
  const searchBtn = document.getElementById('search-btn');
  const clearBtn = document.getElementById('clear-search');
  
  // Check if we're on the order detail page
  const pathParts = window.location.pathname.split('/');
  const orderIdParam = pathParts[pathParts.length - 1];
  const isDetailPage = pathParts.includes('orders') && orderIdParam && orderIdParam !== 'orders';
  const orderDetailId = isDetailPage ? orderIdParam : null;
  
  if (orderDetailId && body) {
    // We're on an order detail page
    await loadOrderDetail(orderDetailId);
  } else if (body) {
    // We're on the general orders page
    let allOrders = []; // Store all orders to search from
    
    // Function to load and store all orders
    async function loadAllOrders() {
      try {
        const data = await fetchJSON('/api/orders');
        allOrders = data.items || data.data || data || [];
        displayOrders(allOrders); // Show all orders initially
      } catch(e) {
        console.error('Error loading orders:', e);  // Debug log
        body.innerHTML = `<tr><td class="px-4 py-3" colspan="4">Gagal memuat orders</td></tr>`;
      }
    }
    
    // Function to display orders (filter or all)
    function displayOrders(ordersToShow) {
      if (ordersToShow.length === 0) {
        body.innerHTML = '<tr><td class="px-4 py-3 text-center" colspan="5">Tidak ada order ditemukan</td></tr>';
        return;
      }
      
      body.innerHTML = ordersToShow.map(o => {
        const status = (o.status || '').toLowerCase();
        const color = status === 'delivered' ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300'
                    : status === 'paid' ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300'
                    : 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-300';
        
        // Create order items HTML
        let itemsHtml = '';
        if (o.items && o.items.length > 0) {
          itemsHtml = '<div class="mt-2 text-xs text-slate-500 dark:text-slate-400">';
          o.items.forEach(item => {
            const product = item.product_id || {};
            itemsHtml += `<div class="flex justify-between mt-1">
              <span>${product.name || item.product_id} (${item.quantity})</span>
              <span>${formatIDR(item.price)}</span>
            </div>`;
          });
          itemsHtml += '</div>';
        } else {
          itemsHtml = '<div class="mt-2 text-xs text-slate-500 dark:text-slate-400">Tidak ada item</div>';
        }
        
        return `
        <tr class="border-t border-slate-200 dark:border-slate-800">
          <td class="px-4 py-3">
            <div>${o.order_id || o.id}</div>
            ${itemsHtml}
          </td>
          <td class="px-4 py-3">${new Date(o.created_at || o.date || Date.now()).toLocaleString('id-ID')}</td>
          <td class="px-4 py-3">${formatIDR(o.total_price || o.total)}</td>
          <td class="px-4 py-3"><span class="px-2 py-1 text-xs rounded-lg ${color}">${o.status}</span></td>
          <td class="px-4 py-3 text-center">
            <a href="/orders/${o.order_id || o.id}" class="px-3 py-1 rounded-lg border border-slate-300 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 text-sm">Detail</a>
          </td>
        </tr>`
      }).join('');
    }
    
    // Function to filter orders based on search query
    function searchOrders(query) {
      if (!query) {
        displayOrders(allOrders); // Show all if no search query
        return;
      }
      
      const filtered = allOrders.filter(order => 
        (order.order_id && order.order_id.toLowerCase().includes(query.toLowerCase())) ||
        (order.id && order.id.toLowerCase().includes(query.toLowerCase()))
      );
      
      displayOrders(filtered);
    }
    
    // Load all orders initially
    await loadAllOrders();
    
    // Add search functionality
    searchBtn?.addEventListener('click', () => {
      const query = searchInput.value.trim();
      searchOrders(query);
    });
    
    // Add Enter key support for search
    searchInput?.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        const query = searchInput.value.trim();
        searchOrders(query);
      }
    });
    
    // Add clear search functionality
    clearBtn?.addEventListener('click', () => {
      searchInput.value = '';
      displayOrders(allOrders); // Show all orders again
    });
  }
}

// Function to load and display order detail
async function loadOrderDetail(orderId) {
  try {
    const data = await fetchJSON(`/api/orders/${orderId}`);
    const order = data.data;
    
    // Update page title
    document.title = `Order ${orderId} · ShopEasy`;
    
    // Create detailed order view
    const orderDetailHtml = `
    <div class="max-w-4xl mx-auto">
      <h1 class="text-2xl font-semibold mb-6">Detail Pesanan</h1>
      
      <!-- Order Summary -->
      <div class="rounded-2xl border border-slate-200 dark:border-slate-800 p-6 mb-6">
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-4">
          <div>
            <h2 class="text-lg font-medium">Order #${order.order_id}</h2>
            <p class="text-slate-500 dark:text-slate-400 text-sm">${new Date(order.created_at).toLocaleString('id-ID')}</p>
          </div>
          
          <div class="mt-2 md:mt-0">
            <span class="px-3 py-1 rounded-full text-sm font-medium
              ${order.status === 'delivered' ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300' :
                order.status === 'paid' ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300' :
                'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-300'}">
              ${order.status === 'pending' ? 'Menunggu Pembayaran' : 
                order.status === 'paid' ? 'Sudah Dibayar' : 
                order.status === 'delivered' ? 'Sudah Dikirim' : order.status}
            </span>
          </div>
        </div>
        
        <!-- Order Items -->
        <div class="mb-6">
          ${order.items.map(item => {
            const product = item.product_id || {};
            return `
            <div class="flex py-4 border-b border-slate-200 dark:border-slate-800">
              <div class="w-16 h-16 rounded-lg bg-slate-100 dark:bg-slate-800 flex items-center justify-center mr-4 flex-shrink-0">
                <img src="${(product.images && product.images[0]) || '/static/images/placeholder.jpg'}" 
                     alt="${product.name}" class="w-12 h-12 object-contain">
              </div>
              <div class="flex-grow">
                <h3 class="font-medium">${product.name || item.product_id}</h3>
                <p class="text-slate-500 dark:text-slate-400 text-sm">${product.brand}</p>
                <p class="text-slate-500 dark:text-slate-400 text-sm">Qty: ${item.quantity}</p>
              </div>
              <div class="text-right">
                <p class="font-medium">${formatIDR(item.price)}</p>
                <p class="text-slate-500 dark:text-slate-400 text-sm">${formatIDR(item.subtotal)}</p>
              </div>
            </div>
            `;
          }).join('')}
        </div>
        
        <!-- Payment Action Button -->
        <div class="border-t border-slate-200 dark:border-slate-800 pt-4">
          <div class="flex flex-col sm:flex-row justify-between items-center gap-4">
            <div class="text-right">
              <p class="text-slate-500 dark:text-slate-400">Total Pembayaran</p>
              <p class="text-2xl font-bold text-brand">${formatIDR(order.total_price)}</p>
            </div>
            
            ${order.status === 'pending' ? 
              `<a href="/api/pay/${order.order_id}" 
                 class="px-6 py-3 bg-brand text-white rounded-lg hover:bg-blue-600 transition-colors font-medium">
                 Bayar Sekarang
               </a>` : 
              `<span class="px-6 py-3 bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300 rounded-lg font-medium">
                 ${order.status === 'paid' ? 'Pembayaran Berhasil' : 'Pesanan Selesai'}
               </span>`
            }
          </div>
        </div>
      </div>
      
      <!-- Order Status Information -->
      <div class="rounded-2xl border border-slate-200 dark:border-slate-800 p-6">
        <h3 class="font-medium mb-4">Status Pesanan</h3>
        <div class="flex items-center">
          <div class="flex flex-col items-center mr-4">
            <div class="w-8 h-8 rounded-full flex items-center justify-center 
              ${order.status === 'pending' ? 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-300' :
                'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300'}">
              1
            </div>
            <span class="text-xs mt-1 text-slate-500 dark:text-slate-400">Dipesan</span>
          </div>
          
          <div class="h-px w-16 bg-slate-200 dark:bg-slate-700"></div>
          
          <div class="flex flex-col items-center mx-4">
            <div class="w-8 h-8 rounded-full flex items-center justify-center 
              ${order.status === 'pending' ? 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-300' :
                order.status === 'paid' ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300' :
                'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300'}">
              2
            </div>
            <span class="text-xs mt-1 text-slate-500 dark:text-slate-400">Dibayar</span>
          </div>
          
          <div class="h-px w-16 bg-slate-200 dark:bg-slate-700"></div>
          
          <div class="flex flex-col items-center ml-4">
            <div class="w-8 h-8 rounded-full flex items-center justify-center 
              ${order.status === 'delivered' ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300' :
                'bg-slate-100 text-slate-500 dark:bg-slate-800 dark:text-slate-400'}">
              3
            </div>
            <span class="text-xs mt-1 text-slate-500 dark:text-slate-400">Dikirim</span>
          </div>
        </div>
      </div>
    </div>
    `;
    
    // Replace the table container with the detailed view
    const container = document.querySelector('.overflow-x-auto') || document.querySelector('.rounded-2xl.border');
    if (container) {
      container.outerHTML = orderDetailHtml;
    } else {
      // If no specific container found, add to the main content area
      document.querySelector('#orders-body').innerHTML = orderDetailHtml;
    }
    
    // If user just came back from payment, refresh to get updated status
    // Check if there's a parameter indicating return from Xendit
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('from_payment') === 'true') {
      // Refresh the page after a short delay to get updated status
      setTimeout(() => {
        window.location.href = `/orders/${orderId}`;
      }, 3000); // Refresh after 3 seconds
    }
    
  } catch(e) {
    console.error('Error loading order detail:', e);
    document.querySelector('#orders-body').innerHTML = `
      <div class="text-center py-8">
        <h3 class="text-lg font-medium mb-2">Gagal memuat detail pesanan</h3>
        <p class="text-slate-500 dark:text-slate-400">Order dengan ID ${orderId} tidak ditemukan</p>
        <a href="/orders" class="mt-4 inline-block px-4 py-2 bg-brand text-white rounded-lg hover:bg-blue-600">Kembali ke Daftar Pesanan</a>
      </div>
    `;
  }
}

/* ========= Auth Pages ========= */
function initLogin() {
  const form = document.getElementById('login-form');
  if (!form) return;
  form.addEventListener('submit', async (e)=>{
    e.preventDefault();
    const fd = new FormData(form);
    const payload = { email: fd.get('email'), password: fd.get('password') };
    try {
      await fetchJSON('/api/auth/login', { method: 'POST', body: JSON.stringify(payload) });
      // After successful login, reload the page to reflect the new auth state
      window.location.href = '/';  // This will trigger the __fetchAuthStatus on page load
    } catch(e) {
      showToast('Login gagal');
    }
  });
}
function initRegister() {
  const form = document.getElementById('register-form');
  if (!form) return;
  form.addEventListener('submit', async (e)=>{
    e.preventDefault();
    const fd = new FormData(form);
    if (fd.get('password') !== fd.get('password_confirm')) {
      showToast('Password tidak cocok'); return;
    }
    const payload = { email: fd.get('email'), password: fd.get('password') };
    try {
      await fetchJSON('/api/auth/signup', { method: 'POST', body: JSON.stringify(payload) });
      showToast('Daftar berhasil. Cek email konfirmasi.');
      setTimeout(()=> location.href = '/login', 900);
    } catch(e) {
      showToast('Gagal daftar');
    }
  });
}

/* ========= Boot ========= */
document.addEventListener('DOMContentLoaded', async () => {
  // Initialize theme after DOM is loaded (since Alpine x-init runs before JS is loaded)
  window.__initTheme && window.__initTheme();
  await __fetchAuthStatus();  // Fetch auth status before initializing other components
  __initCartBadge();
  initHome();
  initProducts();
  initDetail();
  initCart();
  initCheckout();
  initOrders();
  initLogin();
  initRegister();
});
