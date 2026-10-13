/**
 * Honda Atlas Pakistan - Secure Admin Command Center & Inventory Controller
 * Client-Side JavaScript: Stock Modifiers, CRM Lead Pipeline, Metrics & Authentication.
 */

const adminState = {
  token: sessionStorage.getItem('admin_token') || null,
  vehicles: [],
  leads: [],
  metrics: null
};

document.addEventListener('DOMContentLoaded', () => {
  checkAuth();
});

function checkAuth() {
  const loginModal = document.getElementById('login-modal');
  const dashboardContent = document.getElementById('admin-dashboard');

  if (!adminState.token) {
    if (loginModal) loginModal.classList.remove('hidden');
    if (dashboardContent) dashboardContent.classList.add('hidden');
  } else {
    if (loginModal) loginModal.classList.add('hidden');
    if (dashboardContent) dashboardContent.classList.remove('hidden');
    loadAdminData();
  }
}

async function handleAdminLogin(event) {
  event.preventDefault();
  const userEl = document.getElementById('admin-user');
  const passEl = document.getElementById('admin-pass');
  const errorEl = document.getElementById('login-error');

  const username = userEl.value.trim();
  const password = passEl.value.trim();

  try {
    const res = await fetch('/api/admin/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });

    const data = await res.json();
    if (res.ok && data.status === 'success') {
      adminState.token = data.token;
      sessionStorage.setItem('admin_token', data.token);
      if (errorEl) errorEl.classList.add('hidden');
      checkAuth();
    } else {
      if (errorEl) {
        errorEl.innerText = data.detail || 'Invalid username or password';
        errorEl.classList.remove('hidden');
      }
    }
  } catch (e) {
    if (errorEl) {
      errorEl.innerText = 'Server authentication error';
      errorEl.classList.remove('hidden');
    }
  }
}

function handleAdminLogout() {
  adminState.token = null;
  sessionStorage.removeItem('admin_token');
  checkAuth();
}

async function loadAdminData() {
  await Promise.all([
    fetchMetrics(),
    fetchInventory(),
    fetchLeads()
  ]);
}

async function fetchMetrics() {
  try {
    const res = await fetch('/api/admin/metrics');
    const data = await res.json();
    if (data.status === 'success') {
      adminState.metrics = data.metrics;
      renderMetrics();
    }
  } catch (e) {
    console.error('Failed to load metrics:', e);
  }
}

function renderMetrics() {
  const m = adminState.metrics;
  if (!m) return;

  const fleetValEl = document.getElementById('metric-fleet-val');
  const totalUnitsEl = document.getElementById('metric-total-units');
  const totalLeadsEl = document.getElementById('metric-total-leads');
  const lowStockEl = document.getElementById('metric-low-stock');

  if (fleetValEl) fleetValEl.innerText = m.formatted_valuation;
  if (totalUnitsEl) totalUnitsEl.innerText = `${m.total_units} Units`;
  if (totalLeadsEl) totalLeadsEl.innerText = `${m.total_leads} Inquiries`;
  if (lowStockEl) lowStockEl.innerText = `${m.low_stock_count} Models`;
}

async function fetchInventory() {
  try {
    const res = await fetch('/api/inventory');
    const data = await res.json();
    if (data.status === 'success') {
      adminState.vehicles = data.cars;
      renderInventoryTable();
    }
  } catch (e) {
    console.error('Failed to fetch inventory:', e);
  }
}

function renderInventoryTable() {
  const tbody = document.getElementById('inventory-table-body');
  if (!tbody) return;

  tbody.innerHTML = adminState.vehicles.map(car => `
    <tr class="border-b border-zinc-800 hover:bg-zinc-800/40 transition-colors">
      <td class="p-4 flex items-center gap-3">
        <img src="${car.image_url}" class="w-14 h-10 object-cover rounded-lg border border-zinc-700">
        <div>
          <div class="font-bold text-white text-sm">${car.name}</div>
          <div class="text-[11px] text-zinc-400">${car.category}</div>
        </div>
      </td>
      <td class="p-4">
        <div class="flex items-center gap-1.5">
          <span class="text-xs text-zinc-400">PKR</span>
          <input 
            type="number" 
            id="price-input-${car.id}" 
            value="${car.price}" 
            class="w-28 bg-zinc-900 border border-zinc-700 rounded-lg px-2 py-1 text-xs text-white focus:border-red-500 focus:outline-none"
          />
          <button 
            onclick="savePriceChange(${car.id})" 
            class="text-[10px] bg-zinc-800 hover:bg-red-600 text-zinc-300 hover:text-white px-2 py-1 rounded transition-colors"
            title="Save ex-factory price"
          >
            Save
          </button>
        </div>
      </td>
      <td class="p-4">
        <div class="flex items-center gap-2">
          <button 
            onclick="modifyStock(${car.id}, -1)" 
            class="w-7 h-7 rounded-lg bg-zinc-800 hover:bg-red-600 text-white flex items-center justify-center text-xs transition-colors"
            title="Decrement stock"
          >-</button>
          <span id="stock-val-${car.id}" class="w-8 text-center font-bold text-sm ${car.stock <= 2 ? 'text-amber-400' : 'text-emerald-400'}">
            ${car.stock}
          </span>
          <button 
            onclick="modifyStock(${car.id}, 1)" 
            class="w-7 h-7 rounded-lg bg-zinc-800 hover:bg-emerald-600 text-white flex items-center justify-center text-xs transition-colors"
            title="Increment stock"
          >+</button>
        </div>
      </td>
      <td class="p-4">
        <span class="badge-stock ${
          car.stock >= 3 
            ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40' 
            : (car.stock > 0 
                ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40' 
                : 'bg-rose-500/20 text-rose-400 border border-rose-500/40')
        }">
          ${car.stock_status}
        </span>
      </td>
      <td class="p-4 text-xs text-zinc-400">
        ${car.colors.join(', ')}
      </td>
    </tr>
  `).join('');
}

async function modifyStock(carId, delta) {
  const car = adminState.vehicles.find(c => c.id === carId);
  if (!car) return;

  const newStock = Math.max(0, car.stock + delta);
  try {
    const res = await fetch(`/api/admin/inventory/${carId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ stock: newStock })
    });

    if (res.ok) {
      car.stock = newStock;
      fetchMetrics();
      fetchInventory();
      showToast(`Stock updated: ${car.name} is now ${newStock} units`);
    }
  } catch (e) {
    alert('Failed to update stock');
  }
}

async function savePriceChange(carId) {
  const input = document.getElementById(`price-input-${carId}`);
  if (!input) return;

  const car = adminState.vehicles.find(c => c.id === carId);
  const newPrice = parseInt(input.value);

  if (isNaN(newPrice) || newPrice <= 0) {
    alert('Please enter a valid price in PKR');
    return;
  }

  try {
    const res = await fetch(`/api/admin/inventory/${carId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ stock: car.stock, price: newPrice })
    });

    if (res.ok) {
      car.price = newPrice;
      fetchMetrics();
      fetchInventory();
      showToast(`Price updated for ${car.name}: PKR ${newPrice.toLocaleString()}`);
    }
  } catch (e) {
    alert('Failed to update price');
  }
}

async function fetchLeads() {
  try {
    const res = await fetch('/api/admin/leads');
    const data = await res.json();
    if (data.status === 'success') {
      adminState.leads = data.leads;
      renderLeadsTable();
    }
  } catch (e) {
    console.error('Failed to load leads:', e);
  }
}

function renderLeadsTable() {
  const tbody = document.getElementById('leads-table-body');
  if (!tbody) return;

  if (adminState.leads.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="7" class="py-12 text-center text-zinc-500 text-xs">
          No customer inquiries or test drive bookings logged yet.
        </td>
      </tr>
    `;
    return;
  }

  tbody.innerHTML = adminState.leads.map(lead => {
    // Clean phone number for WhatsApp link
    const cleanPhone = lead.phone.replace(/[^0-9]/g, '');
    const waPhone = cleanPhone.startsWith('0') ? '92' + cleanPhone.substring(1) : cleanPhone;

    return `
      <tr class="border-b border-zinc-800 hover:bg-zinc-800/40 transition-colors">
        <td class="p-4 text-xs text-zinc-400">
          #${lead.id}<br>
          <span class="text-[10px] text-zinc-500">${lead.created_at ? lead.created_at.split(' ')[0] : ''}</span>
        </td>
        <td class="p-4">
          <div class="font-bold text-white text-xs">${lead.name}</div>
          <div class="text-[11px] text-zinc-400">${lead.city}</div>
        </td>
        <td class="p-4">
          <div class="flex items-center gap-2">
            <a href="tel:${lead.phone}" class="text-xs text-zinc-300 hover:text-white flex items-center gap-1 font-mono">
              <i class="fas fa-phone-alt text-[10px] text-blue-400"></i> ${lead.phone}
            </a>
            <a href="https://wa.me/${waPhone}?text=Assalam-o-Alaikum%20${encodeURIComponent(lead.name)},%20Honda%20Atlas%20Pakistan%20regarding%20your%20inquiry%20for%20${encodeURIComponent(lead.car_model)}" target="_blank" class="text-emerald-400 hover:text-emerald-300 text-xs" title="Chat on WhatsApp">
              <i class="fab fa-whatsapp"></i>
            </a>
          </div>
          ${lead.email ? `<div class="text-[10px] text-zinc-500">${lead.email}</div>` : ''}
        </td>
        <td class="p-4">
          <div class="text-xs font-semibold text-red-400">${lead.car_model}</div>
          <div class="text-[10px] text-zinc-400">${lead.dealership}</div>
        </td>
        <td class="p-4 text-xs text-zinc-300">
          <div>${lead.preferred_date || 'ASAP'}</div>
          <div class="text-[10px] text-zinc-500">${lead.preferred_time || 'Standard Slot'}</div>
        </td>
        <td class="p-4">
          <select 
            onchange="updateLeadStatus(${lead.id}, this.value)"
            class="bg-zinc-900 border border-zinc-700 rounded-lg px-2.5 py-1 text-xs text-white focus:border-red-500 focus:outline-none"
          >
            <option value="New" ${lead.status === 'New' ? 'selected' : ''}>New</option>
            <option value="Contacted" ${lead.status === 'Contacted' ? 'selected' : ''}>Contacted</option>
            <option value="Test Drive Scheduled" ${lead.status === 'Test Drive Scheduled' ? 'selected' : ''}>Test Drive Scheduled</option>
            <option value="Converted" ${lead.status === 'Converted' ? 'selected' : ''}>Converted (Sold)</option>
            <option value="Lost" ${lead.status === 'Lost' ? 'selected' : ''}>Lost</option>
          </select>
        </td>
        <td class="p-4 text-xs text-zinc-400 max-w-[150px] truncate" title="${lead.notes || ''}">
          ${lead.notes || '-'}
        </td>
      </tr>
    `;
  }).join('');
}

async function updateLeadStatus(leadId, newStatus) {
  try {
    const res = await fetch(`/api/admin/leads/${leadId}/status`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: newStatus })
    });

    if (res.ok) {
      showToast(`Lead #${leadId} status set to ${newStatus}`);
      fetchMetrics();
    }
  } catch (e) {
    alert('Failed to update lead status');
  }
}

function showToast(message) {
  const toast = document.createElement('div');
  toast.className = 'fixed bottom-6 right-6 z-50 bg-zinc-900 border border-red-500 text-white text-xs px-4 py-2.5 rounded-xl shadow-2xl animate-fade-in flex items-center gap-2';
  toast.innerHTML = `<i class="fas fa-check-circle text-red-500"></i> ${message}`;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 4000);
}
