/**
 * Honda Atlas Pakistan - Autonomous Neural Concierge & Voice Intelligence System
 * Client-Side Core: Web Speech STT/TTS Pipeline, Dynamic Audio Wave Visualizer,
 * Multilingual Chat Orchestrator, Virtual Showroom Matrix & Interactive Finance Engine.
 */

// Global Application State
const state = {
  sessionId: 'session-' + Math.random().toString(36).substring(2, 9),
  chatHistory: [],
  isRecording: false,
  isSpeaking: false,
  voiceEnabled: true,
  currentCategory: 'all',
  vehicles: [],
  selectedComparison: [],
  selectedVehicleForFinance: null,
  recognition: null,
  synthesis: window.speechSynthesis,
  currentVoice: null
};

// ============================================================================
// 1. DYNAMIC AUDIO WAVE VISUALIZER (CANVAS)
// ============================================================================
const canvas = document.getElementById('audio-visualizer-canvas');
const ctx = canvas ? canvas.getContext('2d') : null;
let visualizerAnimationId = null;
let wavePhase = 0;

function initVisualizer() {
  if (!canvas || !ctx) return;
  
  function resizeCanvas() {
    canvas.width = canvas.parentElement.clientWidth;
    canvas.height = 48;
  }
  resizeCanvas();
  window.addEventListener('resize', resizeCanvas);

  function renderWave() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const width = canvas.width;
    const height = canvas.height;
    const midY = height / 2;

    // Determine visualizer activity level
    const isActive = state.isRecording || state.isSpeaking;
    const amplitude = isActive ? (state.isRecording ? 18 : 14) : 4;
    const frequency = isActive ? 0.04 : 0.015;
    const speed = isActive ? 0.12 : 0.03;

    wavePhase += speed;

    // Draw primary glowing red wave (Honda Championship Red)
    ctx.beginPath();
    ctx.lineWidth = 2.5;
    ctx.strokeStyle = isActive ? '#E40521' : 'rgba(228, 5, 33, 0.4)';
    ctx.shadowBlur = isActive ? 12 : 4;
    ctx.shadowColor = '#E40521';

    for (let x = 0; x < width; x++) {
      const y = midY + Math.sin(x * frequency + wavePhase) * amplitude * Math.sin(x / width * Math.PI);
      if (x === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();

    // Draw secondary cyan electric wave (Honda Hybrid Intelligence)
    ctx.beginPath();
    ctx.lineWidth = 1.5;
    ctx.strokeStyle = isActive ? '#00e5ff' : 'rgba(0, 229, 255, 0.3)';
    ctx.shadowBlur = isActive ? 8 : 2;
    ctx.shadowColor = '#00e5ff';

    for (let x = 0; x < width; x++) {
      const y = midY + Math.cos(x * (frequency * 1.3) - wavePhase) * (amplitude * 0.75) * Math.sin(x / width * Math.PI);
      if (x === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();

    visualizerAnimationId = requestAnimationFrame(renderWave);
  }

  renderWave();
}

// ============================================================================
// 2. BIDIRECTIONAL REAL-TIME VOICE PIPELINE (STT & TTS)
// ============================================================================
function initVoicePipeline() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  
  if (SpeechRecognition) {
    state.recognition = new SpeechRecognition();
    state.recognition.continuous = false;
    state.recognition.interimResults = false;
    state.recognition.lang = 'en-US'; // Supports Roman Urdu & English

    state.recognition.onstart = () => {
      state.isRecording = true;
      const micBtn = document.getElementById('mic-btn');
      if (micBtn) {
        micBtn.classList.add('mic-recording');
        micBtn.title = 'Listening to your voice... Speak now!';
      }
      updateVisualizerStatus('Listening actively (Microphone engaged)...');
    };

    state.recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      const input = document.getElementById('chat-input');
      if (input) {
        input.value = transcript;
        sendMessage();
      }
    };

    state.recognition.onerror = (event) => {
      console.warn('Speech recognition status:', event.error);
      stopListening();
    };

    state.recognition.onend = () => {
      stopListening();
    };
  } else {
    console.info('Web Speech Recognition not supported in this browser.');
    const micBtn = document.getElementById('mic-btn');
    if (micBtn) micBtn.style.opacity = '0.5';
  }

  // Load and select high quality synthesis voice
  if (state.synthesis) {
    function pickVoice() {
      const voices = state.synthesis.getVoices();
      // Try to find natural English or Urdu/Hindi voice
      state.currentVoice = voices.find(v => v.lang.includes('ur') || v.lang.includes('hi')) ||
                           voices.find(v => v.lang.includes('en') && (v.name.includes('Google') || v.name.includes('Natural') || v.name.includes('David') || v.name.includes('George'))) ||
                           voices[0];
    }
    pickVoice();
    if (speechSynthesis.onvoiceschanged !== undefined) {
      speechSynthesis.onvoiceschanged = pickVoice;
    }
  }
}

function toggleSpeechRecognition() {
  if (!state.recognition) {
    alert('Voice recognition is supported on modern browsers (Google Chrome, Microsoft Edge, Safari).');
    return;
  }
  if (state.isRecording) {
    stopListening();
  } else {
    // Stop any ongoing assistant speech first
    stopSpeaking();
    try {
      state.recognition.start();
    } catch (e) {
      console.error(e);
    }
  }
}

function stopListening() {
  state.isRecording = false;
  const micBtn = document.getElementById('mic-btn');
  if (micBtn) {
    micBtn.classList.remove('mic-recording');
    micBtn.title = 'Click to activate voice input';
  }
  updateVisualizerStatus('Neural Concierge Ready');
}

function speakText(text) {
  if (!state.voiceEnabled || !state.synthesis) return;

  stopSpeaking();

  // Strip markdown formatting for natural voice playback
  const cleanText = text
    .replace(/[#*_`~>•-]/g, ' ')
    .replace(/\bPKR\b/g, 'Pakistani Rupees')
    .replace(/KM\/L/g, 'kilometers per liter')
    .replace(/\n+/g, '. ')
    .slice(0, 450); // Concise executive summary for voice

  const utterance = new SpeechSynthesisUtterance(cleanText);
  if (state.currentVoice) utterance.voice = state.currentVoice;
  utterance.rate = 1.0;
  utterance.pitch = 1.0;

  utterance.onstart = () => {
    state.isSpeaking = true;
    updateVisualizerStatus('Executive Director Speaking...');
    const stopVoiceBtn = document.getElementById('stop-voice-btn');
    if (stopVoiceBtn) stopVoiceBtn.classList.remove('hidden');
  };

  utterance.onend = () => {
    stopSpeaking();
  };

  utterance.onerror = () => {
    stopSpeaking();
  };

  state.synthesis.speak(utterance);
}

function stopSpeaking() {
  if (state.synthesis) {
    state.synthesis.cancel();
  }
  state.isSpeaking = false;
  updateVisualizerStatus('Neural Concierge Ready');
  const stopVoiceBtn = document.getElementById('stop-voice-btn');
  if (stopVoiceBtn) stopVoiceBtn.classList.add('hidden');
}

function toggleVoiceOutput() {
  state.voiceEnabled = !state.voiceEnabled;
  const voiceToggleBtn = document.getElementById('voice-toggle-btn');
  if (voiceToggleBtn) {
    if (state.voiceEnabled) {
      voiceToggleBtn.innerHTML = '<i class="fas fa-volume-up text-red-500"></i> Voice Active';
      voiceToggleBtn.classList.remove('opacity-60');
    } else {
      stopSpeaking();
      voiceToggleBtn.innerHTML = '<i class="fas fa-volume-mute text-zinc-500"></i> Voice Muted';
      voiceToggleBtn.classList.add('opacity-60');
    }
  }
}

function updateVisualizerStatus(statusText) {
  const el = document.getElementById('visualizer-status-text');
  if (el) el.innerText = statusText;
}

// ============================================================================
// 3. NEURAL CHAT STREAM & CONVERSATION ORCHESTRATION
// ============================================================================
async function sendMessage(presetText = null) {
  const input = document.getElementById('chat-input');
  const message = (presetText || (input ? input.value : '')).trim();

  if (!message) return;

  if (input) input.value = '';

  // Append User Bubble
  appendChatMessage('user', message);

  // Show typing loader
  const typingId = showTypingIndicator();

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: message,
        session_id: state.sessionId,
        history: state.chatHistory.slice(-6)
      })
    });

    removeTypingIndicator(typingId);

    if (!res.ok) throw new Error('API communication error');

    const data = await res.json();
    const assistantText = data.response;

    // Append Assistant Bubble
    appendChatMessage('assistant', assistantText, data.language, data.engine_used);

    // Speak Assistant Response
    speakText(assistantText);

    // If purchase intent detected or triggered, suggest Lead Booking Modal
    if (data.trigger_lead_modal) {
      renderChatActionHook('Book a VIP Test Drive', () => {
        openTestDriveModal(data.matched_car);
      });
    }

    // Scroll to bottom
    scrollChatToBottom();

  } catch (err) {
    removeTypingIndicator(typingId);
    appendChatMessage('assistant', 'Sorry, I encountered a temporary network delay. Please repeat your query or select from the quick prompt options below.', 'en');
  }
}

function appendChatMessage(role, text, lang = 'en', engine = null) {
  const chatStream = document.getElementById('chat-stream');
  if (!chatStream) return;

  state.chatHistory.push({ role, text });

  const msgDiv = document.createElement('div');
  msgDiv.className = `flex flex-col ${role === 'user' ? 'items-end' : 'items-start'} mb-4 animate-fade-in`;

  const bubble = document.createElement('div');
  bubble.className = `max-w-[92%] sm:max-w-[85%] rounded-2xl p-4 text-sm leading-relaxed shadow-lg ${
    role === 'user' ? 'chat-bubble-user text-white' : 'chat-bubble-assistant text-zinc-100'
  }`;

  // Formatter for Markdown (bold, lists, code, headers)
  bubble.innerHTML = formatMarkdown(text);

  // Metadata footer
  const meta = document.createElement('div');
  meta.className = 'text-[10px] text-zinc-400 mt-1.5 flex items-center gap-2 px-1';
  const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  if (role === 'assistant') {
    const langLabel = lang === 'ur' ? 'اردو' : (lang === 'roman_ur' ? 'Roman Urdu' : 'English');
    meta.innerHTML = `<span><i class="fas fa-shield-alt text-red-500 mr-1"></i>Honda Executive AI</span> • <span>${time}</span> • <span class="text-zinc-300 font-medium">${langLabel}</span>`;
  } else {
    meta.innerHTML = `<span>You</span> • <span>${time}</span>`;
  }

  msgDiv.appendChild(bubble);
  msgDiv.appendChild(meta);
  chatStream.appendChild(msgDiv);

  scrollChatToBottom();
}

function renderChatActionHook(buttonText, onClick) {
  const chatStream = document.getElementById('chat-stream');
  if (!chatStream) return;

  const container = document.createElement('div');
  container.className = 'flex justify-start mb-3 animate-fade-in';

  const btn = document.createElement('button');
  btn.className = 'px-4 py-2 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-500 hover:to-red-600 text-white font-medium rounded-xl text-xs flex items-center gap-2 shadow-lg border border-red-500/30 transition-all transform hover:scale-[1.02]';
  btn.innerHTML = `<i class="fas fa-calendar-check"></i> ${buttonText}`;
  btn.onclick = onClick;

  container.appendChild(btn);
  chatStream.appendChild(container);
  scrollChatToBottom();
}

function showTypingIndicator() {
  const chatStream = document.getElementById('chat-stream');
  if (!chatStream) return null;

  const id = 'typing-' + Date.now();
  const el = document.createElement('div');
  el.id = id;
  el.className = 'flex items-center gap-2 mb-4 text-zinc-400 text-xs px-2 animate-pulse';
  el.innerHTML = `
    <div class="w-6 h-6 rounded-full bg-red-600/30 flex items-center justify-center text-red-500 text-[10px]">
      <i class="fas fa-microchip"></i>
    </div>
    <span>Senior Sales Director is synthesizing response...</span>
  `;
  chatStream.appendChild(el);
  scrollChatToBottom();
  return id;
}

function removeTypingIndicator(id) {
  if (!id) return;
  const el = document.getElementById(id);
  if (el) el.remove();
}

function scrollChatToBottom() {
  const chatStream = document.getElementById('chat-stream');
  if (chatStream) {
    chatStream.scrollTo({ top: chatStream.scrollHeight, behavior: 'smooth' });
  }
}

function formatMarkdown(content) {
  if (!content) return '';
  return content
    .replace(/^### (.*$)/gim, '<h4 class="font-bold text-red-400 mt-2 mb-1">$1</h4>')
    .replace(/^## (.*$)/gim, '<h3 class="font-bold text-white text-base mt-2 mb-1">$1</h3>')
    .replace(/\*\*(.*?)\*\*/gim, '<strong class="text-white font-semibold">$1</strong>')
    .replace(/\*(.*?)\*/gim, '<em>$1</em>')
    .replace(/• (.*$)/gim, '<li class="ml-4 list-disc text-zinc-200">$1</li>')
    .replace(/\n/gim, '<br>');
}

// ============================================================================
// 4. VIRTUAL SHOWROOM & INVENTORY MATRIX CONTROLLER
// ============================================================================
async function loadVehicles() {
  try {
    const res = await fetch('/api/inventory');
    const data = await res.json();
    if (data.status === 'success') {
      state.vehicles = data.cars;
      renderVehicleGrid();
    }
  } catch (e) {
    console.error('Failed to load inventory matrix:', e);
  }
}

function filterCategory(category) {
  state.currentCategory = category;

  // Update button active state
  document.querySelectorAll('.cat-pill').forEach(btn => {
    if (btn.dataset.category === category) {
      btn.classList.add('bg-red-600', 'text-white', 'border-red-500');
      btn.classList.remove('bg-zinc-800/60', 'text-zinc-300', 'border-zinc-700/60');
    } else {
      btn.classList.remove('bg-red-600', 'text-white', 'border-red-500');
      btn.classList.add('bg-zinc-800/60', 'text-zinc-300', 'border-zinc-700/60');
    }
  });

  renderVehicleGrid();
}

function renderVehicleGrid() {
  const container = document.getElementById('vehicles-grid');
  if (!container) return;

  const searchQuery = (document.getElementById('search-input')?.value || '').toLowerCase();
  const sortValue = document.getElementById('sort-select')?.value || 'default';

  let filtered = state.vehicles.filter(car => {
    const matchesCat = state.currentCategory === 'all' || 
                       car.category.toLowerCase().includes(state.currentCategory.toLowerCase());
    const matchesSearch = car.name.toLowerCase().includes(searchQuery) ||
                          car.transmission.toLowerCase().includes(searchQuery) ||
                          car.fuel_economy.toLowerCase().includes(searchQuery);
    return matchesCat && matchesSearch;
  });

  if (sortValue === 'price-asc') {
    filtered.sort((a, b) => a.price - b.price);
  } else if (sortValue === 'price-desc') {
    filtered.sort((a, b) => b.price - a.price);
  } else if (sortValue === 'stock-desc') {
    filtered.sort((a, b) => b.stock - a.stock);
  }

  if (filtered.length === 0) {
    container.innerHTML = `
      <div class="col-span-full py-16 text-center text-zinc-400">
        <i class="fas fa-car-crash text-3xl mb-3 text-red-500"></i>
        <p class="text-base font-medium">No Honda vehicles match your specific filter criteria.</p>
        <button onclick="resetFilters()" class="mt-3 text-xs text-red-400 underline">Reset all filters</button>
      </div>
    `;
    return;
  }

  container.innerHTML = filtered.map(car => `
    <div class="glass-card rounded-2xl overflow-hidden flex flex-col group border border-zinc-800 hover:border-red-600/40 transition-all duration-300">
      <!-- High-Resolution Image Container with Dynamic Zoom -->
      <div class="relative h-48 bg-zinc-950 overflow-hidden">
        <img 
          src="${car.image_url}" 
          alt="${car.name}" 
          class="w-full h-full object-cover object-center group-hover:scale-105 transition-transform duration-500 opacity-90 group-hover:opacity-100"
          loading="lazy"
          onerror="this.src='/static/images/honda_civic_standard.jpg'"
        />
        <div class="absolute inset-0 bg-gradient-to-t from-zinc-950 via-zinc-950/20 to-transparent"></div>
        
        <!-- Live Stock Availability Badge -->
        <div class="absolute top-3 left-3">
          <span class="badge-stock ${
            car.stock >= 3 
              ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40' 
              : (car.stock > 0 
                  ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40' 
                  : 'bg-rose-500/20 text-rose-400 border border-rose-500/40')
          } backdrop-blur-md">
            <span class="inline-block w-1.5 h-1.5 rounded-full mr-1.5 ${
              car.stock >= 3 ? 'bg-emerald-400' : (car.stock > 0 ? 'bg-amber-400 animate-pulse' : 'bg-rose-400')
            }"></span>
            ${car.stock_status}
          </span>
        </div>

        <!-- Model Category Pill -->
        <div class="absolute top-3 right-3">
          <span class="text-[10px] uppercase font-bold tracking-wider px-2.5 py-1 rounded bg-black/60 text-zinc-300 backdrop-blur-md border border-white/10">
            ${car.category}
          </span>
        </div>

        <!-- Price Display Overlay -->
        <div class="absolute bottom-3 left-3 right-3 flex items-end justify-between">
          <div>
            <div class="text-[10px] uppercase text-zinc-400 tracking-wider font-medium">Ex-Factory Price</div>
            <div class="text-xl font-extrabold text-white tracking-tight">${car.formatted_price}</div>
          </div>
          <button 
            onclick="triggerFinanceForCar('${car.slug}')" 
            class="text-[11px] bg-red-600/20 hover:bg-red-600 text-red-300 hover:text-white px-2.5 py-1 rounded-lg border border-red-500/30 transition-all font-medium flex items-center gap-1"
            title="Calculate monthly installment"
          >
            <i class="fas fa-calculator text-[10px]"></i> EMI Plan
          </button>
        </div>
      </div>

      <!-- Vehicle Specifications Matrix Body -->
      <div class="p-4 flex-1 flex flex-col justify-between">
        <div>
          <div class="flex items-center justify-between gap-2 mb-1">
            <h3 class="font-bold text-white text-base tracking-tight group-hover:text-red-400 transition-colors">
              ${car.name}
            </h3>
            <button 
              onclick="toggleCompareCar('${car.slug}')" 
              class="text-xs text-zinc-400 hover:text-white transition-colors p-1"
              title="Add to comparison"
            >
              <i class="fas fa-balance-scale"></i>
            </button>
          </div>
          <p class="text-xs text-zinc-400 line-clamp-1 mb-3">${car.tagline || car.description}</p>

          <!-- Core Technical Specifications Chips Grid -->
          <div class="grid grid-cols-2 gap-2 text-xs mb-3">
            <div class="bg-zinc-900/80 p-2 rounded-xl border border-zinc-800 flex items-center gap-2">
              <i class="fas fa-horse-head text-red-500 text-xs"></i>
              <div>
                <div class="text-[9px] text-zinc-400">Power</div>
                <div class="font-semibold text-zinc-200 truncate">${car.horsepower.split('@')[0]}</div>
              </div>
            </div>
            <div class="bg-zinc-900/80 p-2 rounded-xl border border-zinc-800 flex items-center gap-2">
              <i class="fas fa-gas-pump text-emerald-500 text-xs"></i>
              <div>
                <div class="text-[9px] text-zinc-400">Mileage</div>
                <div class="font-semibold text-zinc-200">${car.fuel_economy}</div>
              </div>
            </div>
            <div class="bg-zinc-900/80 p-2 rounded-xl border border-zinc-800 flex items-center gap-2">
              <i class="fas fa-cogs text-blue-400 text-xs"></i>
              <div>
                <div class="text-[9px] text-zinc-400">Transmission</div>
                <div class="font-semibold text-zinc-200 truncate">${car.transmission.split(' ')[0]}</div>
              </div>
            </div>
            <div class="bg-zinc-900/80 p-2 rounded-xl border border-zinc-800 flex items-center gap-2">
              <i class="fas fa-shield-alt text-amber-400 text-xs"></i>
              <div>
                <div class="text-[9px] text-zinc-400">Safety</div>
                <div class="font-semibold text-zinc-200 truncate">${car.airbags.split(' ')[0]} Airbags</div>
              </div>
            </div>
          </div>

          <!-- Color Swatches & Boot Space -->
          <div class="flex items-center justify-between text-[11px] text-zinc-400 border-t border-zinc-800/80 pt-2 mb-4">
            <div class="flex items-center gap-1">
              <i class="fas fa-palette text-zinc-500"></i>
              <span class="truncate max-w-[140px] text-zinc-300">${car.colors.join(', ')}</span>
            </div>
            <div class="flex items-center gap-1 text-zinc-400">
              <i class="fas fa-suitcase"></i> ${car.boot_capacity}
            </div>
          </div>
        </div>

        <!-- Action CTAs -->
        <div class="grid grid-cols-2 gap-2 mt-auto">
          <button 
            onclick="consultCarWithAI('${car.name}', '${car.formatted_price}')" 
            class="w-full py-2 px-3 rounded-xl bg-zinc-800 hover:bg-zinc-700 text-zinc-200 text-xs font-medium transition-all flex items-center justify-center gap-1.5 border border-zinc-700/50"
          >
            <i class="fas fa-robot text-red-500"></i> Ask Concierge
          </button>
          <button 
            onclick="openTestDriveModal('${car.slug}')" 
            class="w-full py-2 px-3 rounded-xl bg-red-600 hover:bg-red-500 text-white text-xs font-semibold shadow-md transition-all flex items-center justify-center gap-1.5"
          >
            <i class="fas fa-key"></i> Book Test Drive
          </button>
        </div>
      </div>
    </div>
  `).join('');
}

function resetFilters() {
  const search = document.getElementById('search-input');
  if (search) search.value = '';
  filterCategory('all');
}

function consultCarWithAI(carName, price) {
  const prompt = `Tell me more about the ${carName} (${price}). What is the available stock, fuel economy, and 3-year installment breakdown?`;
  sendMessage(prompt);
}

// ============================================================================
// 5. INTERACTIVE AUTO-FINANCE & INSTALLMENT CALCULATOR
// ============================================================================
function openFinanceModal(carSlug = null) {
  const modal = document.getElementById('finance-modal');
  if (!modal) return;

  const select = document.getElementById('finance-car-select');
  if (select) {
    select.innerHTML = state.vehicles.map(c => `
      <option value="${c.slug}" ${carSlug === c.slug ? 'selected' : ''}>
        ${c.name} - ${c.formatted_price}
      </option>
    `).join('');
  }

  updateFinanceCalculations();
  modal.classList.remove('hidden');
}

function closeFinanceModal() {
  const modal = document.getElementById('finance-modal');
  if (modal) modal.classList.add('hidden');
}

function triggerFinanceForCar(carSlug) {
  openFinanceModal(carSlug);
}

function updateFinanceCalculations() {
  const select = document.getElementById('finance-car-select');
  const dpSlider = document.getElementById('finance-dp-slider');
  const tenureSlider = document.getElementById('finance-tenure-slider');
  const markupSlider = document.getElementById('finance-markup-slider');

  if (!select) return;

  const selectedSlug = select.value;
  const car = state.vehicles.find(c => c.slug === selectedSlug) || state.vehicles[0];
  if (!car) return;

  const price = car.price;
  const dpPct = parseFloat(dpSlider ? dpSlider.value : 25);
  const tenureYears = parseInt(tenureSlider ? tenureSlider.value : 5);
  const markupRate = parseFloat(markupSlider ? markupSlider.value : 17.5);

  // Update slider labels
  const dpLabel = document.getElementById('finance-dp-label');
  const tenureLabel = document.getElementById('finance-tenure-label');
  const markupLabel = document.getElementById('finance-markup-label');

  if (dpLabel) dpLabel.innerText = `${dpPct}%`;
  if (tenureLabel) tenureLabel.innerText = `${tenureYears} Years (${tenureYears * 12} Months)`;
  if (markupLabel) markupLabel.innerText = `${markupRate}% APR (KIBOR + Spread)`;

  // Calculations
  const downPayment = Math.round(price * (dpPct / 100.0));
  const financedAmount = price - downPayment;
  const totalMarkup = Math.round(financedAmount * (markupRate / 100.0) * tenureYears);
  const totalPayable = financedAmount + totalMarkup;
  const monthly = Math.round(totalPayable / (tenureYears * 12));

  // Display outputs
  document.getElementById('calc-car-price').innerText = `PKR ${price.toLocaleString()}`;
  document.getElementById('calc-down-payment').innerText = `PKR ${downPayment.toLocaleString()}`;
  document.getElementById('calc-financed-amount').innerText = `PKR ${financedAmount.toLocaleString()}`;
  document.getElementById('calc-monthly-installment').innerText = `PKR ${monthly.toLocaleString()} / mo`;
  document.getElementById('calc-total-markup').innerText = `PKR ${totalMarkup.toLocaleString()}`;
}

function sendFinancePlanToChat() {
  const select = document.getElementById('finance-car-select');
  const dpSlider = document.getElementById('finance-dp-slider');
  const tenureSlider = document.getElementById('finance-tenure-slider');
  
  const car = state.vehicles.find(c => c.slug === select.value);
  if (!car) return;

  const dpPct = dpSlider.value;
  const tenure = tenureSlider.value;
  const monthly = document.getElementById('calc-monthly-installment').innerText;

  closeFinanceModal();
  const prompt = `I am interested in leasing the ${car.name} with ${dpPct}% down payment over a ${tenure}-year period (calculated at approx ${monthly}). Please advise on bank processing, delivery timelines, and required documents.`;
  sendMessage(prompt);
}

// ============================================================================
// 6. SIDE-BY-SIDE MODEL COMPARISON MATRIX
// ============================================================================
function toggleCompareCar(slug) {
  const idx = state.selectedComparison.indexOf(slug);
  if (idx > -1) {
    state.selectedComparison.splice(idx, 1);
  } else {
    if (state.selectedComparison.length >= 3) {
      alert('You can compare a maximum of 3 Honda models simultaneously.');
      return;
    }
    state.selectedComparison.push(slug);
  }
  updateCompareBadge();
}

function updateCompareBadge() {
  const badge = document.getElementById('compare-count-badge');
  if (badge) {
    badge.innerText = state.selectedComparison.length;
    badge.classList.toggle('hidden', state.selectedComparison.length === 0);
  }
}

function openComparisonModal() {
  const modal = document.getElementById('comparison-modal');
  if (!modal) return;

  // If none selected, default to Civic RS vs HR-V Hybrid vs City Aspire
  if (state.selectedComparison.length === 0) {
    state.selectedComparison = ['honda-civic-rs', 'honda-hr-v-ehev-hybrid'];
    updateCompareBadge();
  }

  const comparedCars = state.vehicles.filter(c => state.selectedComparison.includes(c.slug));
  const container = document.getElementById('comparison-matrix-content');

  if (!container) return;

  container.innerHTML = `
    <div class="overflow-x-auto">
      <table class="w-full text-left text-xs border-collapse">
        <thead>
          <tr class="border-b border-zinc-800">
            <th class="p-3 text-zinc-400 font-semibold uppercase tracking-wider w-40">Specification</th>
            ${comparedCars.map(c => `
              <th class="p-3 text-white font-bold text-sm min-w-[200px]">
                <div class="flex items-center justify-between mb-2">
                  <span>${c.name}</span>
                  <button onclick="toggleCompareCar('${c.slug}'); openComparisonModal();" class="text-zinc-500 hover:text-red-400 text-xs">
                    <i class="fas fa-times"></i>
                  </button>
                </div>
                <img src="${c.image_url}" class="h-24 w-full object-cover rounded-xl mb-2 border border-zinc-800">
                <div class="text-red-400 font-extrabold text-base">${c.formatted_price}</div>
              </th>
            `).join('')}
          </tr>
        </thead>
        <tbody class="divide-y divide-zinc-800/60">
          <tr>
            <td class="p-3 text-zinc-400 font-medium">Category</td>
            ${comparedCars.map(c => `<td class="p-3 text-zinc-200">${c.category}</td>`).join('')}
          </tr>
          <tr>
            <td class="p-3 text-zinc-400 font-medium">Warehouse Stock</td>
            ${comparedCars.map(c => `<td class="p-3 font-semibold ${c.stock > 0 ? 'text-emerald-400' : 'text-rose-400'}">${c.stock} units (${c.stock_status})</td>`).join('')}
          </tr>
          <tr>
            <td class="p-3 text-zinc-400 font-medium">Horsepower</td>
            ${comparedCars.map(c => `<td class="p-3 text-zinc-200 font-semibold">${c.horsepower}</td>`).join('')}
          </tr>
          <tr>
            <td class="p-3 text-zinc-400 font-medium">Torque</td>
            ${comparedCars.map(c => `<td class="p-3 text-zinc-200">${c.torque}</td>`).join('')}
          </tr>
          <tr>
            <td class="p-3 text-zinc-400 font-medium">Transmission</td>
            ${comparedCars.map(c => `<td class="p-3 text-zinc-200">${c.transmission}</td>`).join('')}
          </tr>
          <tr>
            <td class="p-3 text-zinc-400 font-medium">Fuel Economy</td>
            ${comparedCars.map(c => `<td class="p-3 text-emerald-400 font-bold">${c.fuel_economy}</td>`).join('')}
          </tr>
          <tr>
            <td class="p-3 text-zinc-400 font-medium">Safety Airbags</td>
            ${comparedCars.map(c => `<td class="p-3 text-zinc-200">${c.airbags}</td>`).join('')}
          </tr>
          <tr>
            <td class="p-3 text-zinc-400 font-medium">Boot Space</td>
            ${comparedCars.map(c => `<td class="p-3 text-zinc-200">${c.boot_capacity}</td>`).join('')}
          </tr>
          <tr>
            <td class="p-3 text-zinc-400 font-medium">Colors Ready</td>
            ${comparedCars.map(c => `<td class="p-3 text-zinc-300">${c.colors.join(', ')}</td>`).join('')}
          </tr>
          <tr>
            <td class="p-3 text-zinc-400 font-medium">Actions</td>
            ${comparedCars.map(c => `
              <td class="p-3">
                <button onclick="closeComparisonModal(); openTestDriveModal('${c.slug}');" class="w-full py-2 bg-red-600 hover:bg-red-500 text-white rounded-lg font-semibold text-xs transition-all">
                  Book Test Drive
                </button>
              </td>
            `).join('')}
          </tr>
        </tbody>
      </table>
    </div>
  `;

  modal.classList.remove('hidden');
}

function closeComparisonModal() {
  const modal = document.getElementById('comparison-modal');
  if (modal) modal.classList.add('hidden');
}

// ============================================================================
// 7. VIP TEST DRIVE & CRM LEAD BOOKING MODAL
// ============================================================================
function openTestDriveModal(carSlug = null) {
  const modal = document.getElementById('test-drive-modal');
  if (!modal) return;

  const select = document.getElementById('lead-car-select');
  if (select && state.vehicles.length > 0) {
    select.innerHTML = state.vehicles.map(c => `
      <option value="${c.name}" ${carSlug === c.slug ? 'selected' : ''}>
        ${c.name} (${c.formatted_price})
      </option>
    `).join('');
  }

  // Pre-fill tomorrow's date
  const dateInput = document.getElementById('lead-date');
  if (dateInput) {
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    dateInput.value = tomorrow.toISOString().split('T')[0];
  }

  modal.classList.remove('hidden');
}

function closeTestDriveModal() {
  const modal = document.getElementById('test-drive-modal');
  if (modal) modal.classList.add('hidden');
}

async function handleLeadFormSubmit(event) {
  event.preventDefault();

  const name = document.getElementById('lead-name').value.trim();
  const phone = document.getElementById('lead-phone').value.trim();
  const email = document.getElementById('lead-email').value.trim();
  const city = document.getElementById('lead-city').value;
  const car_model = document.getElementById('lead-car-select').value;
  const dealership = document.getElementById('lead-dealership').value;
  const preferred_date = document.getElementById('lead-date').value;
  const preferred_time = document.getElementById('lead-time').value;
  const notes = document.getElementById('lead-notes').value.trim();

  if (!name || !phone) {
    alert('Please provide your Full Name and Mobile Number.');
    return;
  }

  const submitBtn = document.getElementById('lead-submit-btn');
  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i> Confirming Reservation...';
  }

  try {
    const res = await fetch('/api/leads', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name, phone, email, city, car_model, dealership,
        preferred_date, preferred_time, notes,
        source: 'Virtual Showroom VIP Modal'
      })
    });

    const data = await res.json();

    if (res.ok && data.status === 'success') {
      closeTestDriveModal();
      showCelebrationAlert(`VIP Test Drive Reserved for ${name}!`, `Reference #${data.lead_id} logged. A senior Honda sales consultant from ${dealership} will contact you at ${phone}.`);
      
      // Notify chat concierge
      appendChatMessage('assistant', `Test Drive Booking Confirmed! We have reserved your VIP test drive for the **${car_model}** at **${dealership}** for ${preferred_date}. Reference ID: #${data.lead_id}. Looking forward to hosting you!`, 'en');
      speakText(`Thank you ${name}. Your VIP test drive reservation for the ${car_model} has been recorded.`);
    } else {
      alert('Unable to log reservation. Please check your network and try again.');
    }
  } catch (e) {
    console.error(e);
    alert('Network error while booking test drive.');
  } finally {
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.innerHTML = '<i class="fas fa-check-circle mr-2"></i> Confirm VIP Reservation';
    }
  }
}

function showCelebrationAlert(title, message) {
  const alertBox = document.createElement('div');
  alertBox.className = 'fixed top-6 right-6 z-50 glass-modal border-l-4 border-red-600 p-5 rounded-2xl shadow-2xl max-w-md animate-fade-in text-white';
  alertBox.innerHTML = `
    <div class="flex items-start gap-3">
      <div class="w-10 h-10 rounded-full bg-red-600/20 text-red-500 flex items-center justify-center shrink-0">
        <i class="fas fa-check-double text-lg"></i>
      </div>
      <div>
        <h4 class="font-bold text-sm text-white mb-1">${title}</h4>
        <p class="text-xs text-zinc-300 leading-relaxed">${message}</p>
      </div>
      <button onclick="this.parentElement.parentElement.remove()" class="text-zinc-500 hover:text-white ml-auto">
        <i class="fas fa-times"></i>
      </button>
    </div>
  `;
  document.body.appendChild(alertBox);
  setTimeout(() => alertBox.remove(), 7000);
}

// ============================================================================
// 8. EVENT LISTENERS & INITIALIZATION
// ============================================================================
document.addEventListener('DOMContentLoaded', () => {
  initVisualizer();
  initVoicePipeline();
  loadVehicles();

  // Enter key to send chat
  const chatInput = document.getElementById('chat-input');
  if (chatInput) {
    chatInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    });
  }

  // Search input real-time filtering
  const searchInput = document.getElementById('search-input');
  if (searchInput) {
    searchInput.addEventListener('input', () => renderVehicleGrid());
  }

  // Sort select
  const sortSelect = document.getElementById('sort-select');
  if (sortSelect) {
    sortSelect.addEventListener('change', () => renderVehicleGrid());
  }

  // Finance slider listeners
  ['finance-car-select', 'finance-dp-slider', 'finance-tenure-slider', 'finance-markup-slider'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.addEventListener('input', updateFinanceCalculations);
  });

  // Lead Form
  const leadForm = document.getElementById('test-drive-form');
  if (leadForm) {
    leadForm.addEventListener('submit', handleLeadFormSubmit);
  }
});
