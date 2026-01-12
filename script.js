/**
 * DOCWIPING - Advanced Data Sanitization System
 * Iron Man ARC Reactor Theme Edition
 * 
 * A professional data destruction simulator with secure wipe capabilities
 */

const { jsPDF } = window.jspdf;

// ==========================================
// STATE MANAGEMENT
// ==========================================

let lastGeneratedCertificate = null;
const appContainer = document.getElementById('app-container');

const appState = {
    os: null,
    activeDrive: null,
    selectedMethod: null
};

// ==========================================
// DATA DEFINITIONS
// ==========================================

const simulatedDesktopDrives = [
    { 
        id: 'NVME01', 
        type: 'NVMe SSD', 
        model: 'Enterprise NVMe Drive', 
        size: '1.6 TB', 
        bestMethod: 'NVMe Format (Crypto Erase)', 
        standard: 'NIST SP 800-88' 
    },
    { 
        id: 'SATA01', 
        type: 'SATA SSD', 
        model: 'Kingston DC500R', 
        size: '960 GB', 
        bestMethod: 'ATA Secure Erase', 
        standard: 'NIST SP 800-88' 
    },
    { 
        id: 'SATA02', 
        type: 'SATA HDD', 
        model: 'Seagate Exos 7E8', 
        size: '4 TB', 
        bestMethod: 'DoD 5220.22-M (3-pass)', 
        standard: 'DoD 5220.22-M' 
    },
];

const simulatedAndroidStorage = [
    { 
        id: 'INTERNAL', 
        type: 'Internal Storage', 
        model: 'UFS 3.1', 
        size: '256 GB', 
        bestMethod: 'Factory Reset + Crypto Key Wipe' 
    },
    { 
        id: 'SDCARD', 
        type: 'SD Card', 
        model: 'SanDisk Extreme', 
        size: '128 GB', 
        bestMethod: 'Full Overwrite' 
    },
    { 
        id: 'CACHE', 
        type: 'System Cache', 
        model: 'N/A', 
        size: '4 GB', 
        bestMethod: 'Secure Deletion' 
    },
];

const windowsWipeMethods = [
    { 
        id: 'NIST SP 800-88', 
        name: 'NIST SP 800-88 Purge', 
        description: 'Cryptographic erase for SSDs, multi-pass for HDDs.' 
    },
    { 
        id: 'DoD 5220.22-M', 
        name: 'DoD 5220.22-M', 
        description: '3-pass overwrite, common for government use.' 
    },
    { 
        id: 'Gutmann method', 
        name: 'Gutmann method', 
        description: '35-pass overwrite for maximum security.' 
    }
];

const linuxWipeMethods = [
    { 
        id: 'NIST SP 800-88', 
        name: 'NIST SP 800-88 Purge', 
        description: 'Uses cryptographic and block-level overwrite.' 
    },
    { 
        id: 'Crypto Erase', 
        name: 'Crypto Erase', 
        description: 'Uses built-in hardware encryption keys to instantly erase data.' 
    },
    { 
        id: 'n-Wipe', 
        name: 'n-Wipe', 
        description: 'A custom, high-speed single-pass overwrite with verification.' 
    }
];

// ==========================================
// UTILITY FUNCTIONS
// ==========================================

/**
 * Show a specific screen by ID and hide others
 * @param {string} screenId - The ID of the screen to show
 */
function showScreen(screenId) {
    document.querySelectorAll('.app-screen').forEach(screen => 
        screen.classList.remove('active')
    );
    const targetScreen = document.getElementById(screenId);
    if (targetScreen) {
        targetScreen.classList.add('active');
    }
}

/**
 * Reset the application to initial state
 */
function resetApp() {
    appState.os = null;
    appState.activeDrive = null;
    appState.selectedMethod = null;
    showScreen('os-selection-screen');
}

/**
 * Show system information modal
 */
function showSystemInfo() {
    const modal = document.getElementById('system-info-modal');
    const osDisplay = document.getElementById('sys-os');
    
    // Update OS info based on current state
    if (appState.os) {
        osDisplay.textContent = `${appState.os} (Simulated Environment)`;
    } else {
        osDisplay.textContent = 'No OS selected';
    }
    
    modal.style.display = 'flex';
}

/**
 * Select an operating system and begin boot process
 * @param {string} os - Operating system name (Windows, Linux, Android)
 */
function selectOS(os) {
    appState.os = os;
    showScreen('boot-screen');
    simulateBoot(os);
}

// ==========================================
// BOOT SIMULATION
// ==========================================

/**
 * Simulate system boot with progress animation
 * @param {string} os - Operating system name
 */
function simulateBoot(os) {
    const bootLog = document.getElementById('boot-log');
    const bootProgress = document.getElementById('boot-progress');
    bootLog.innerHTML = '';
    bootProgress.style.width = '0%';
    
    const bootMessages = [
        "DOCWIPING Bootloader v2.0...",
        "Initializing kernel modules...",
        "Detecting hardware interfaces...",
        "Loading USB drivers [usb-storage]...",
        "Mounting virtual filesystem [tmpfs]...",
        `Launching DOCWIPING for ${os}...`
    ];

    let i = 0;
    const interval = setInterval(() => {
        if (i < bootMessages.length) {
            const line = document.createElement('p');
            line.className = 'boot-line';
            line.textContent = `[ ◆ ] ${bootMessages[i]}`;
            bootLog.appendChild(line);
            bootProgress.style.width = `${((i + 1) / bootMessages.length) * 100}%`;
            i++;
        } else {
            clearInterval(interval);
            setTimeout(() => {
                if (os === 'Android') {
                    appContainer.className = 'app-container w-full max-w-sm h-full sm:h-[800px] sm:max-h-[90vh] bg-slate-900 text-white rounded-none sm:rounded-3xl shadow-2xl overflow-hidden flex flex-col';
                    populateAndroidStorage();
                    showScreen('android-dashboard-screen');
                } else {
                    appContainer.className = 'app-container w-full max-w-4xl bg-slate-900 text-white rounded-2xl shadow-2xl overflow-hidden flex flex-col';
                    document.getElementById('desktop-os-badge').innerText = `(${os} Environment)`;
                    populateDesktopDrives();
                    showScreen('desktop-dashboard-screen');
                }
            }, 500);
        }
    }, 350);
}

// --- DESKTOP SPECIFIC FUNCTIONS ---
function populateDesktopDrives() {
    const driveList = document.getElementById('desktop-drive-list');
    driveList.innerHTML = '';
    simulatedDesktopDrives.forEach(drive => {
        const driveElement = document.createElement('div');
        driveElement.className = 'drive-item bg-slate-800 p-4 rounded-lg flex items-center justify-between transition-all border border-slate-700/50 hover:border-blue-500/50';
        driveElement.innerHTML = `<div class="flex items-center"><svg class="w-10 h-10 mr-4 text-slate-400" fill="currentColor" viewBox="0 0 24 24"><path d="M4,5V19A2,2 0 0,0 6,21H18A2,2 0 0,0 20,19V5A2,2 0 0,0 18,3H6A2,2 0 0,0 4,5M8,5H10V7H8V5M12,5H14V7H12V5M16,5H18V7H16V5Z" /></svg><div><h3 class="font-bold text-lg">${drive.model} (${drive.id})</h3><p class="text-sm text-slate-400">${drive.size} ${drive.type}</p></div></div><div class="drive-actions opacity-100 sm:opacity-0 sm:transform sm:translateX-4 transition-all duration-300"><button onclick="prepareDesktopWipe('${drive.id}')" class="bg-blue-600 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded-lg button-press glow-shadow">Wipe</button></div>`;
        driveList.appendChild(driveElement);
    });
}

function prepareDesktopWipe(driveId) {
    appState.activeDrive = simulatedDesktopDrives.find(d => d.id === driveId);
    const methods = appState.os === 'Linux' ? linuxWipeMethods : windowsWipeMethods;
    appState.selectedMethod = methods.find(m => m.name === appState.activeDrive.bestMethod) || methods[0];
    document.getElementById('desktop-wipe-process-title').innerText = `Wiping: ${appState.activeDrive.model}`;
    showScreen('desktop-wipe-process-screen');
    showDesktopWipeStep('desktop-analysis-view');
    simulateAnalysis(appState.activeDrive);
}

function simulateAnalysis(drive) {
    const nextBtn = document.getElementById('analysis-next-btn');
    const analysisContainer = document.getElementById('analysis-results-container');
    nextBtn.disabled = true;
    nextBtn.classList.add('opacity-50', 'cursor-not-allowed');
    analysisContainer.innerHTML = `<div class="flex items-center justify-center h-24"><div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-400"></div><p class="ml-4">Analyzing drive, please wait...</p></div>`;

    setTimeout(() => {
        populateAnalysisView(drive);
        nextBtn.disabled = false;
        nextBtn.classList.remove('opacity-50', 'cursor-not-allowed');
    }, 2500);
}

function populateAnalysisView(drive) {
    const resultsContainer = document.getElementById('analysis-results-container');
    const partitions = Math.floor(Math.random() * 3) + 1;
    const hiddenAreas = drive.type.includes('HDD') 
        ? `<span class="font-semibold text-yellow-400">DETECTED</span> <span class="tooltip text-slate-400">(?)<span class="tooltiptext">Host Protected Areas (HPA) or Device Configuration Overlays (DCO) are hidden from the OS. CleanWipe will remove these.</span></span>` 
        : '<span class="font-semibold text-slate-400">NOT APPLICABLE</span>';
    const encryption = Math.random() > 0.5 ? '<span class="font-semibold text-blue-400">BitLocker (Active)</span>' : '<span class="font-semibold text-slate-400">None</span>';

    let analysisHTML = `
        <div class="flex justify-between items-center"><span>S.M.A.R.T. Status:</span><span class="font-semibold text-green-400">HEALTHY</span></div>
        <div class="flex justify-between items-center"><span>Encryption Status:</span>${encryption}</div>
        <div class="flex justify-between items-center"><span>Partitions Found:</span><span class="font-semibold">${partitions}</span></div>
    `;
    if (drive.type.includes('HDD')) {
        analysisHTML += `
        <div class="flex justify-between items-center"><span>Hidden Areas:</span><span class="font-semibold text-yellow-400">DETECTED</span></div>
        <ul class="text-sm text-slate-400 pl-6 list-disc">
            <li>Host Protected Area (HPA)</li>
            <li>Device Configuration Overlay (DCO)</li>
        </ul>
        `;
    }
    resultsContainer.innerHTML = analysisHTML;
}

function showDesktopWipeStep(viewId) {
    ['desktop-analysis-view', 'desktop-method-selection-view', 'desktop-wiping-view'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.classList.add('hidden');
    });
    const activeView = document.getElementById(viewId);
    if (activeView) activeView.classList.remove('hidden');

    const steps = ['desktop-step-1', 'desktop-step-2', 'desktop-step-3'];
    let activeStep = 0;
    if (viewId === 'desktop-method-selection-view') activeStep = 1;
    if (viewId === 'desktop-wiping-view') activeStep = 2;
    
    steps.forEach((id, index) => {
        const el = document.getElementById(id);
        if (!el) return;
        const circle = el.children[0];
        if (index < activeStep) {
            el.classList.add('text-green-400'); el.classList.remove('text-blue-400', 'text-slate-600');
            circle.classList.add('border-green-400', 'bg-green-400/20'); circle.classList.remove('border-blue-400', 'border-slate-700');
            circle.innerHTML = '&#10003;';
        } else if (index === activeStep) {
             el.classList.add('text-blue-400'); el.classList.remove('text-green-400', 'text-slate-600');
            circle.classList.add('border-blue-400'); circle.classList.remove('border-green-400', 'border-slate-700', 'bg-green-400/20');
            circle.innerText = index + 1;
        } else {
            el.classList.add('text-slate-600'); el.classList.remove('text-blue-400', 'text-green-400');
            circle.classList.add('border-slate-700'); circle.classList.remove('border-blue-400', 'border-green-400', 'bg-green-400/20');
            circle.innerText = index + 1;
        }
    });
    if(viewId === 'desktop-method-selection-view') populateDesktopMethods();
}

function populateDesktopMethods() {
    const container = document.getElementById('desktop-method-options');
    container.innerHTML = '';
    const methodsToUse = appState.os === 'Linux' ? linuxWipeMethods : windowsWipeMethods;

    methodsToUse.forEach(method => {
        const isRecommended = method.name === appState.activeDrive.bestMethod;
        const isSelected = method.id === appState.selectedMethod.id;
        const el = document.createElement('div');
        el.className = `p-4 rounded-lg border-2 cursor-pointer transition-all ${isSelected ? 'bg-blue-600/20 border-blue-500' : 'bg-slate-800 border-slate-700 hover:border-blue-500/50'}`;
        el.onclick = () => selectDesktopMethod(method.id);
        el.innerHTML = `<div class="flex justify-between items-center"><h3 class="font-bold text-lg">${method.name}</h3>${isRecommended ? '<span class="text-xs bg-green-500/20 text-green-300 px-2 py-1 rounded-full">Recommended</span>' : ''}</div><p class="text-sm ${isSelected ? 'text-slate-200' : 'text-slate-400'}">${method.description}</p>`;
        container.appendChild(el);
    });
}

function selectDesktopMethod(methodId) {
    const methodsToUse = appState.os === 'Linux' ? linuxWipeMethods : windowsWipeMethods;
    appState.selectedMethod = methodsToUse.find(m => m.id === methodId);
    populateDesktopMethods();
}

// --- ANDROID SPECIFIC FUNCTIONS ---
function populateAndroidStorage() {
    const list = document.getElementById('android-storage-list');
    list.innerHTML = '';
    simulatedAndroidStorage.forEach(item => {
        const el = document.createElement('div');
        el.className = 'bg-slate-800 p-5 rounded-lg border border-slate-700 hover:border-blue-500/50 cursor-pointer button-press';
        el.onclick = () => prepareAndroidWipe(item.id);
        el.innerHTML = `<h3 class="font-bold text-lg">${item.type} (${item.size})</h3><p class="text-sm text-slate-400">${item.bestMethod}</p>`;
        list.appendChild(el);
    });
}

function prepareAndroidWipe(itemId) {
    appState.activeDrive = simulatedAndroidStorage.find(item => item.id === itemId);
    appState.selectedMethod = { name: appState.activeDrive.bestMethod }; // Simplified for Android
    showConfirmation();
}

// --- COMMON WIPE & CERTIFICATE FUNCTIONS ---
function showConfirmation() {
    document.getElementById('confirm-text').innerHTML = `You are about to permanently erase data from <strong class="text-white">${appState.activeDrive.model}</strong> using the <strong class="text-white">${appState.selectedMethod.name}</strong>. This action cannot be undone.`;
    document.getElementById('confirmation-modal').style.display = 'flex';
}

function startWipe() {
    document.getElementById('confirmation-modal').style.display = 'none';
    if (appState.os === 'Android') {
        startAndroidWipe();
    } else {
        startDesktopWipe();
    }
}

function startDesktopWipe() {
    showDesktopWipeStep('desktop-wiping-view');
    
    // Start wipe via API
    startWipeWithAPI();
    
    // Display device name
    document.getElementById('device-name-display').textContent = appState.activeDrive.model;
    
    const progressBar = document.getElementById('desktop-progress-bar');
    const progressText = document.getElementById('desktop-progress-text');
    const logContainer = document.getElementById('desktop-log-container');
    const wipeDataBar = document.getElementById('wipe-data-bar');
    const wipeDataPercent = document.getElementById('wipe-data-percent');
    const speedBar = document.getElementById('speed-bar');
    const wipeSpeed = document.getElementById('wipe-speed');
    
    const logs = [ 
        `Initializing DOCWIPING on ${appState.activeDrive.id}...`, 
        `Target: ${appState.activeDrive.model}`, 
        `Selected Standard: ${appState.selectedMethod.name}`, 
        `Issuing low-level command: ${getWipeCommand(appState.activeDrive)}...`, 
        "Checking for hidden partitions (HPA/DCO)...", 
        "HPA/DCO detected. Removing temporary lock...", 
        "Starting overwrite pass 1...", 
        "Pass 1 complete.", 
        "Starting final pass (Verification)...", 
        "Reading random sectors to verify erasure...", 
        "Verification successful. All sectors zeroed.", 
        "Finalizing logs and preparing certificate...", 
        "Secure wipe complete. Data irrecoverable." 
    ];
    
    runWipeSimulation(progressBar, progressText, logContainer, logs, wipeDataBar, wipeDataPercent, speedBar, wipeSpeed);
}

function startAndroidWipe() {
    showScreen('android-wiping-screen');
    
    // Display device name
    document.getElementById('device-name-display-android').textContent = appState.activeDrive.type;
    document.getElementById('android-wiping-info').innerText = `Erasing ${appState.activeDrive.type} (${appState.activeDrive.size})`;
    
    const progressBar = document.getElementById('android-progress-bar');
    const progressText = document.getElementById('android-progress-text');
    const logContainer = document.getElementById('android-log-container');
    const wipeDataBar = document.getElementById('android-wipe-data-bar');
    const wipeDataPercent = document.getElementById('android-wipe-data-percent');
    
    const logs = [ 
        `Initializing DOCWIPING on ${appState.activeDrive.model}...`, 
        `Target: ${appState.activeDrive.type}`, 
        `Method: ${appState.activeDrive.bestMethod}`, 
        "Destroying cryptographic keys from TrustZone...", 
        "Issuing eMMC block erase command on /data...", 
        "Overwriting user data partition with random data...", 
        "Clearing application caches and dalvik-cache...", 
        "Verification pass on user partition...", 
        "Wipe complete. All data securely destroyed." 
    ];
    
    runWipeSimulation(progressBar, progressText, logContainer, logs, wipeDataBar, wipeDataPercent);
}

function runWipeSimulation(progressBar, progressText, logContainer, logs, wipeDataBar, wipeDataPercent, speedBar, wipeSpeed) {
    progressBar.style.width = '0%';
    progressText.innerText = '0%';
    logContainer.innerHTML = '';
    let progress = 0;
    let logIndex = 0;
    
    // Get drive size in GB
    const driveSize = parseFloat(appState.activeDrive.size);
    
    const interval = setInterval(() => {
        progress += Math.random() * 5;
        if (progress > 100) progress = 100;
        progressBar.style.width = progress + '%';
        progressText.innerText = Math.floor(progress) + '%';
        
        // Update data meter if provided
        if (wipeDataBar && wipeDataPercent) {
            const wipedData = (progress / 100) * driveSize;
            wipeDataBar.style.width = progress + '%';
            wipeDataPercent.textContent = `${wipedData.toFixed(1)} GB / ${driveSize} GB`;
        }
        
        // Update speed meter if provided
        if (speedBar && wipeSpeed) {
            const speed = 50 + Math.random() * 200;
            speedBar.style.width = Math.min(progress + 20, 100) + '%';
            wipeSpeed.textContent = `${speed.toFixed(1)} MB/s`;
        }
        
        if (progress > (logIndex * 12) && logIndex < logs.length) {
            const logLine = document.createElement('p');
            logLine.className = 'log-line';
            logLine.innerText = `[${new Date().toLocaleTimeString()}] ${logs[logIndex]}`;
            logContainer.prepend(logLine);
            logIndex++;
        }
        if (progress >= 100) {
            clearInterval(interval);
            // Complete wipe via API
            completeWipeWithAPI();
            setTimeout(() => showScreen('success-screen'), 1000);
        }
    }, 300);
}

function getWipeCommand(drive) {
    if (drive.type.includes('NVMe')) return 'ioctl(NVME_IOCTL_FORMAT)';
    if (drive.type.includes('SATA')) return 'ioctl(HDIO_DRIVE_CMD, ATA_SECURE_ERASE)';
    if (drive.type.includes('eMMC')) return 'ioctl(MMC_IOC_CMD, MMC_ERASE)';
    return 'dd if=/dev/urandom';
}

function generateCertificate() {
    const doc = new jsPDF();
    const completionDate = new Date();
    const assetId = `DW-${completionDate.getFullYear()}-${Math.random().toString(36).substr(2, 9).toUpperCase()}`;
    lastGeneratedCertificate = { 
        assetId, 
        model: appState.activeDrive.model, 
        timestamp: completionDate.toLocaleString(),
        type: appState.activeDrive.type,
        size: appState.activeDrive.size,
        method: appState.selectedMethod.name
    };
    
    // Update certificate preview
    document.getElementById('cert-device').textContent = appState.activeDrive.model;
    document.getElementById('cert-date').textContent = completionDate.toLocaleDateString();
    
    doc.setFont("helvetica", "bold");
    doc.setFontSize(24);
    doc.setTextColor(0, 212, 255); // Neon Blue
    doc.text("DOCWIPING", 105, 25, null, null, "center");
    
    doc.setFontSize(16);
    doc.setTextColor(0, 255, 255); // Cyan
    doc.text("Certificate of Data Destruction", 105, 35, null, null, "center");
    
    doc.setTextColor(0, 0, 0);
    
    doc.autoTable({
        startY: 45,
        head: [['Parameter', 'Value']],
        body: [
            ['Asset ID', assetId], 
            ['Device Model', appState.activeDrive.model], 
            ['Device Type', appState.activeDrive.type],
            ['Device Size', appState.activeDrive.size], 
            ['Sanitization Standard', appState.selectedMethod.name],
            ['Verification Status', 'Quantum-Grade Verified'], 
            ['Completion Timestamp', completionDate.toLocaleString()],
            ['Software Version', `DOCWIPING v2.1 (${appState.os})`],
            ['Integrity Level', 'CRITICAL'],
        ],
        theme: 'grid',
        headStyles: { fillColor: [0, 212, 255] }
    });

    let finalY = doc.autoTable.previous.finalY;

    doc.autoTable({
        startY: finalY + 10,
        head: [['Chain of Custody', '']],
        body: [
            ['Wiped By', 'DOCWIPING Quantum-Grade Agent'],
            ['Verified By', 'Automated Cryptographic Post-Wipe Verification'],
            ['Classification', 'Professional Quantum-Safe Data Destruction'],
            ['Compliance', 'NIST SP 800-88 | DoD 5220.22-M | ISO 27001']
        ],
        theme: 'grid',
        headStyles: { fillColor: [0, 212, 255] }
    });

    finalY = doc.autoTable.previous.finalY;

    const signature = `SIG-NEON-${Math.random().toString(36).substr(2, 40).toUpperCase()}`;
    doc.setFontSize(8);
    doc.setTextColor(0, 0, 0);
    doc.text("Digital Signature (SHA512-Neon):", 15, finalY + 15);
    doc.setFont("courier", "normal");
    doc.text(signature, 15, finalY + 20);
    
    // QR code placeholder (neon blue)
    doc.setDrawColor(0, 212, 255);
    doc.setFillColor(0, 212, 255);
    for (let i = 0; i < 15; i++) 
        for (let j = 0; j < 15; j++) 
            if (Math.random() > 0.5) 
                doc.rect(160 + (i * 2), finalY + 10 + (j*2), 2, 2, 'F');
    
    doc.setFont("helvetica", "normal");
    doc.setFontSize(10);
    doc.setTextColor(0, 212, 255);
    doc.text("Scan to Verify Quantum-Grade", 175, finalY + 45, null, null, "center");
    
    doc.save(`DOCWIPING-Cert-${assetId}.pdf`);
}

function verifyCertificate(event) {
    const resultDiv = document.getElementById('verification-result');
    resultDiv.innerHTML = `<p class="text-yellow-400">Verifying...</p>`;
    setTimeout(() => {
        if (lastGeneratedCertificate) {
            resultDiv.innerHTML = `<div class="p-4 bg-green-500/10 border border-green-500/30 rounded-lg text-left"><p class="font-bold text-green-300">✅ Verification Successful</p><p class="text-sm mt-2">Asset ID: <span class="font-mono">${lastGeneratedCertificate.assetId}</span></p><p class="text-sm">Device: <span class="font-mono">${lastGeneratedCertificate.model}</span></p><p class="text-sm">Wipe Time: <span class="font-mono">${lastGeneratedCertificate.timestamp}</span></p><p class="text-sm mt-2 text-slate-400">The digital signature is valid. This certificate is authentic.</p></div>`;
        } else {
             resultDiv.innerHTML = `<div class="p-4 bg-red-500/10 border border-red-500/30 rounded-lg text-left"><p class="font-bold text-red-300">❌ Verification Failed</p><p class="text-sm mt-2 text-slate-400">No valid certificate was found for verification. Please generate a certificate first.</p></div>`;
        }
        event.target.value = '';
    }, 2000);
}

window.onload = () => {
    showScreen('os-selection-screen');
    initializeChatbot();
};

// ==========================================
// API CONFIGURATION
// ==========================================

const API_BASE_URL = 'http://localhost:5000/api';

// ==========================================
// CHATBOT FUNCTIONS
// ==========================================

let currentWipeId = null;

function initializeChatbot() {
    console.log('✓ AI Chatbot initialized');
}

function toggleChat() {
    const chatWindow = document.getElementById('chat-window');
    chatWindow.style.display = chatWindow.style.display === 'none' ? 'block' : 'none';
}

async function sendChatMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    const messagesContainer = document.getElementById('chat-messages');
    const language = document.getElementById('chat-language').value;
    
    // Add user message to chat
    const userMsgDiv = document.createElement('div');
    userMsgDiv.className = 'chat-message-user';
    userMsgDiv.innerHTML = `
        <div class="chat-bubble-user">
            <p class="text-sm text-white">${escapeHtml(message)}</p>
        </div>
    `;
    messagesContainer.appendChild(userMsgDiv);
    input.value = '';
    
    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    // Show typing indicator
    const typingDiv = document.createElement('div');
    typingDiv.id = 'typing-indicator';
    typingDiv.className = 'flex items-start gap-2';
    typingDiv.innerHTML = `
        <div class="w-8 h-8 bg-purple-600 rounded-full flex items-center justify-center flex-shrink-0">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><path d="M8 14s1.5 2 4 2 4-2 4-2"></path><line x1="9" y1="9" x2="9.01" y2="9"></line><line x1="15" y1="9" x2="15.01" y2="9"></line></svg>
        </div>
        <div class="bg-purple-600/20 border border-purple-500/30 rounded-lg p-3">
            <div class="flex gap-1">
                <div class="w-2 h-2 bg-purple-400 rounded-full animate-bounce"></div>
                <div class="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                <div class="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
            </div>
        </div>
    `;
    messagesContainer.appendChild(typingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                language: language
            })
        });
        
        const data = await response.json();
        
        // Remove typing indicator
        typingDiv.remove();
        
        // Add bot response
        const botMsgDiv = document.createElement('div');
        botMsgDiv.className = 'flex items-start gap-2';
        botMsgDiv.innerHTML = `
            <div class="w-8 h-8 bg-purple-600 rounded-full flex items-center justify-center flex-shrink-0">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><path d="M8 14s1.5 2 4 2 4-2 4-2"></path><line x1="9" y1="9" x2="9.01" y2="9"></line><line x1="15" y1="9" x2="15.01" y2="9"></line></svg>
            </div>
            <div class="chat-bubble-bot">
                <p class="text-sm text-white">${escapeHtml(data.response)}</p>
            </div>
        `;
        messagesContainer.appendChild(botMsgDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
    } catch (error) {
        console.error('Chat error:', error);
        typingDiv.remove();
        
        // Fallback response if server is not running
        const botMsgDiv = document.createElement('div');
        botMsgDiv.className = 'flex items-start gap-2';
        botMsgDiv.innerHTML = `
            <div class="w-8 h-8 bg-purple-600 rounded-full flex items-center justify-center flex-shrink-0">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><path d="M8 14s1.5 2 4 2 4-2 4-2"></path><line x1="9" y1="9" x2="9.01" y2="9"></line><line x1="15" y1="9" x2="15.01" y2="9"></line></svg>
            </div>
            <div class="chat-bubble-bot">
                <p class="text-sm text-white">I can help you with DOCWIPING features, wipe methods, and security standards. Ask me anything about data sanitization!</p>
            </div>
        `;
        messagesContainer.appendChild(botMsgDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ==========================================
// API INTEGRATION FOR WIPE OPERATIONS
// ==========================================

async function startWipeWithAPI() {
    try {
        const response = await fetch(`${API_BASE_URL}/wipe/start`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                device_id: appState.activeDrive.id,
                device_name: appState.activeDrive.model,
                device_type: appState.activeDrive.type,
                device_size: appState.activeDrive.size,
                wipe_method: appState.selectedMethod.name,
                wipe_standard: appState.activeDrive.standard
            })
        });
        
        const data = await response.json();
        if (data.success) {
            currentWipeId = data.wipe_id;
            console.log('✓ Wipe started, ID:', currentWipeId);
        }
    } catch (error) {
        console.log('API unavailable, continuing offline');
    }
}

async function completeWipeWithAPI() {
    if (!currentWipeId) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/wipe/complete`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                wipe_id: currentWipeId
            })
        });
        
        const data = await response.json();
        if (data.success) {
            console.log('✓ Wipe completed, Certificate Hash:', data.certificate_hash);
        }
    } catch (error) {
        console.log('API unavailable, continuing offline');
    }
}

