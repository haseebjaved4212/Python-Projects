// ==========================================================================
// Antigravity Voice Assistant Frontend Script
// ==========================================================================

document.addEventListener('DOMContentLoaded', () => {
    // UI Elements
    const btnToggleSidebar = document.getElementById('btn-toggle-sidebar');
    const sidebar = document.querySelector('.sidebar');
    const inputGeminiKey = document.getElementById('gemini-key');
    const btnToggleKey = document.getElementById('toggle-key-visibility');
    const btnSaveKey = document.getElementById('btn-save-key');
    const voiceSelect = document.getElementById('voice-select');
    const timeDisplay = document.getElementById('time-display');
    const assistantOrb = document.getElementById('assistant-orb');
    const assistantStateLabel = document.getElementById('assistant-state');
    const speechPreview = document.getElementById('speech-preview');
    const consoleBody = document.getElementById('console-body');
    const btnClearConsole = document.getElementById('btn-clear-console');
    const textCommand = document.getElementById('text-command');
    const btnSendCommand = document.getElementById('btn-send-command');
    const btnMic = document.getElementById('btn-mic');
    
    // Canvas Visualizer
    const canvas = document.getElementById('visualizer-canvas');
    const ctx = canvas.getContext('2d');
    
    // Screenshot Lightbox Modal Elements
    const screenshotModal = document.getElementById('screenshot-modal');
    const modalImg = document.getElementById('img-modal-target');
    const closeModal = document.querySelector('.close-modal');

    // Speech APIs State
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition = null;
    let isListening = false;
    let assistantState = 'IDLE'; // IDLE, LISTENING, THINKING, SPEAKING
    let voices = [];
    
    // Initialize Local Storage values
    let geminiKey = localStorage.getItem('gemini_api_key') || '';
    if (geminiKey) {
        inputGeminiKey.value = geminiKey;
    }

    // 1. Time / Date Display
    function updateTime() {
        const now = new Date();
        const options = { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' };
        const dateStr = now.toLocaleDateString('en-US', options);
        const timeStr = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
        timeDisplay.textContent = `${dateStr} | ${timeStr}`;
    }
    setInterval(updateTime, 1000);
    updateTime();

    // 2. Settings Drawer Toggle
    btnToggleSidebar.addEventListener('click', () => {
        sidebar.classList.toggle('collapsed');
    });

    // 3. Toggle Gemini Key Visibility
    btnToggleKey.addEventListener('click', () => {
        const type = inputGeminiKey.type === 'password' ? 'text' : 'password';
        inputGeminiKey.type = type;
        const icon = btnToggleKey.querySelector('i');
        icon.classList.toggle('fa-eye');
        icon.classList.toggle('fa-eye-slash');
    });

    // Save Gemini Key
    btnSaveKey.addEventListener('click', () => {
        const key = inputGeminiKey.value.trim();
        localStorage.setItem('gemini_api_key', key);
        geminiKey = key;
        addConsoleLog('System', `Gemini API key saved! Assistant brain capabilities updated.`, 'system');
        
        // Show success visual feedback on button
        btnSaveKey.textContent = "Saved!";
        btnSaveKey.style.background = "linear-gradient(135deg, #4caf50 0%, #2e7d32 100%)";
        setTimeout(() => {
            btnSaveKey.textContent = "Save Key";
            btnSaveKey.style.background = "";
        }, 1500);
    });

    // 4. Text-To-Speech (SpeechSynthesis)
    function loadVoices() {
        voices = window.speechSynthesis.getVoices();
        voiceSelect.innerHTML = '<option value="">Default System Voice</option>';
        
        // Filter and add English voices or premium ones
        voices.forEach((voice, index) => {
            const option = document.createElement('option');
            option.value = index;
            option.textContent = `${voice.name} (${voice.lang})`;
            
            // Auto-select English voices or Google/Microsoft ones if available
            if (voice.lang.includes('en') && (voice.name.includes('Google') || voice.name.includes('Natural') || voice.name.includes('Zira') || voice.name.includes('David'))) {
                option.textContent += ' [Recommended]';
            }
            voiceSelect.appendChild(option);
        });
    }

    if (window.speechSynthesis) {
        loadVoices();
        if (window.speechSynthesis.onvoiceschanged !== undefined) {
            window.speechSynthesis.onvoiceschanged = loadVoices;
        }
    }

    function speak(text) {
        if (!window.speechSynthesis) return;
        
        // Cancel any ongoing speech
        window.speechSynthesis.cancel();
        
        const utterance = new SpeechSynthesisUtterance(text);
        
        // Select custom voice if saved
        const selectedVoiceIdx = voiceSelect.value;
        if (selectedVoiceIdx !== '') {
            utterance.voice = voices[selectedVoiceIdx];
        }
        
        // Set speech speed/pitch
        utterance.rate = 1.0; 
        utterance.pitch = 1.0;
        
        utterance.onstart = () => {
            setAssistantState('SPEAKING');
        };
        
        utterance.onend = () => {
            setAssistantState('IDLE');
        };
        
        utterance.onerror = () => {
            setAssistantState('IDLE');
        };
        
        window.speechSynthesis.speak(utterance);
    }

    // 5. Speech Recognition Setup
    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = true;
        recognition.lang = 'en-US';

        recognition.onstart = () => {
            isListening = true;
            btnMic.classList.add('active');
            setAssistantState('LISTENING');
            speechPreview.textContent = 'Listening... Speak now';
        };

        recognition.onresult = (event) => {
            let interimTranscript = '';
            let finalTranscript = '';

            for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    finalTranscript += event.results[i][0].transcript;
                } else {
                    interimTranscript += event.results[i][0].transcript;
                }
            }

            // Show real-time transcript preview
            speechPreview.textContent = interimTranscript || finalTranscript || 'Listening...';
            
            if (finalTranscript) {
                processUserCommand(finalTranscript);
            }
        };

        recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            if (event.error !== 'no-speech') {
                addConsoleLog('System', `Speech recognition error: ${event.error}`, 'system');
            }
            stopListening();
        };

        recognition.onend = () => {
            stopListening();
        };
    } else {
        btnMic.style.display = 'none';
        addConsoleLog('System', 'Web Speech API is not supported in this browser. Speech recognition is disabled, but you can type commands.', 'system');
    }

    function startListening() {
        if (!recognition || isListening) return;
        
        // Stop any active speech before starting to listen
        if (window.speechSynthesis) {
            window.speechSynthesis.cancel();
        }
        
        try {
            recognition.start();
        } catch (e) {
            console.error(e);
        }
    }

    function stopListening() {
        if (!isListening) return;
        isListening = false;
        btnMic.classList.remove('active');
        if (recognition) {
            recognition.stop();
        }
        if (assistantState === 'LISTENING') {
            setAssistantState('IDLE');
            speechPreview.textContent = 'Press the microphone or say "Hello" to start';
        }
    }

    btnMic.addEventListener('click', () => {
        if (isListening) {
            stopListening();
        } else {
            startListening();
        }
    });

    // 6. Handle User Input Submission
    function processUserCommand(commandText) {
        if (!commandText.trim()) return;
        
        // Log in chat history
        addConsoleLog('You', commandText, 'user');
        
        // Update UI state
        setAssistantState('THINKING');
        speechPreview.textContent = 'Processing request...';
        
        // Send to backend
        fetch('/api/command', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                command: commandText,
                gemini_key: geminiKey
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Backend response:', data);
            
            // Handle output speech and text
            if (data.message) {
                addConsoleLog('Jarvis', data.message, 'assistant', data);
                speak(data.message);
                speechPreview.textContent = data.message;
            } else {
                setAssistantState('IDLE');
                speechPreview.textContent = 'Awaiting instructions';
            }
        })
        .catch(error => {
            console.error('Error contacting backend:', error);
            const errMsg = 'Error connecting to the voice assistant server.';
            addConsoleLog('System', errMsg, 'system');
            speak(errMsg);
            setAssistantState('IDLE');
        });
    }

    // Text Input Submit
    btnSendCommand.addEventListener('click', () => {
        const cmd = textCommand.value.trim();
        if (cmd) {
            processUserCommand(cmd);
            textCommand.value = '';
        }
    });

    textCommand.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const cmd = textCommand.value.trim();
            if (cmd) {
                processUserCommand(cmd);
                textCommand.value = '';
            }
        }
    });

    // Clear Console History
    btnClearConsole.addEventListener('click', () => {
        consoleBody.innerHTML = '';
        addConsoleLog('System', 'Console cleared.', 'system');
    });

    // 7. Render Console Logs and Special Widgets
    function addConsoleLog(sender, text, type, metaData = null) {
        const log = document.createElement('div');
        log.className = `log-message ${type}`;
        
        const senderEl = document.createElement('div');
        senderEl.className = 'log-sender';
        senderEl.textContent = sender;
        
        const textEl = document.createElement('div');
        textEl.className = 'log-text';
        textEl.textContent = text;
        
        const timeEl = document.createElement('div');
        timeEl.className = 'log-time';
        const now = new Date();
        timeEl.textContent = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
        
        log.appendChild(senderEl);
        log.appendChild(textEl);
        
        // Inline widgets rendering based on payload
        if (metaData) {
            // Screen Capture widget
            if (metaData.type === 'screenshot' && metaData.url) {
                const imgContainer = document.createElement('div');
                imgContainer.className = 'screenshot-preview';
                
                const img = document.createElement('img');
                img.src = metaData.url;
                img.alt = 'System Screenshot';
                
                imgContainer.appendChild(img);
                log.appendChild(imgContainer);
                
                // Add click handler to display in full lightbox
                imgContainer.addEventListener('click', () => {
                    screenshotModal.style.display = "block";
                    modalImg.src = metaData.url;
                });
            }
            
            // System hardware stats widget
            if (metaData.type === 'info' && metaData.data) {
                const stats = metaData.data;
                const widget = document.createElement('div');
                widget.className = 'stats-widget';
                
                // CPU Info
                if (stats.cpu !== undefined) {
                    widget.appendChild(createStatItem('fa-microchip', 'CPU', `${stats.cpu}%`, 'cpu'));
                }
                
                // RAM Info
                if (stats.ram !== undefined) {
                    widget.appendChild(createStatItem('fa-memory', 'RAM', `${stats.ram}%`, 'ram'));
                }
                
                // Battery Info
                if (stats.battery && stats.battery.percent !== null) {
                    const batteryIcon = stats.battery.charging ? 'fa-battery-charging' : 'fa-battery-full';
                    const batText = `${stats.battery.percent}%` + (stats.battery.charging ? ' (Chg)' : '');
                    widget.appendChild(createStatItem(batteryIcon, 'Battery', batText, 'battery'));
                }
                
                log.appendChild(widget);
            }
        }
        
        log.appendChild(timeEl);
        consoleBody.appendChild(log);
        
        // Scroll to bottom
        consoleBody.scrollTop = consoleBody.scrollHeight;
    }

    // Utility helper for rendering system stats items
    function createStatItem(iconClass, label, value, colorClass) {
        const item = document.createElement('div');
        item.className = 'stat-item';
        
        const iconDiv = document.createElement('div');
        iconDiv.className = `stat-icon ${colorClass}`;
        
        const icon = document.createElement('i');
        icon.className = `fa-solid ${iconClass}`;
        iconDiv.appendChild(icon);
        
        const detailDiv = document.createElement('div');
        detailDiv.className = 'stat-detail';
        
        const titleSpan = document.createElement('span');
        titleSpan.className = 'stat-title';
        titleSpan.textContent = label;
        
        const valueSpan = document.createElement('span');
        valueSpan.className = 'stat-value';
        valueSpan.textContent = value;
        
        detailDiv.appendChild(titleSpan);
        detailDiv.appendChild(valueSpan);
        
        item.appendChild(iconDiv);
        item.appendChild(detailDiv);
        return item;
    }

    // 8. Screenshot Lightbox Close
    closeModal.addEventListener('click', () => {
        screenshotModal.style.display = "none";
    });

    window.addEventListener('click', (event) => {
        if (event.target === screenshotModal) {
            screenshotModal.style.display = "none";
        }
    });

    // 9. Manage UI Assistant States
    function setAssistantState(state) {
        assistantState = state;
        assistantStateLabel.textContent = state;
        
        // Remove old state classes
        assistantOrb.classList.remove('listening', 'thinking', 'speaking');
        
        if (state === 'LISTENING') {
            assistantOrb.classList.add('listening');
            assistantStateLabel.style.color = 'var(--secondary)';
            assistantStateLabel.style.textShadow = '0 0 8px var(--secondary-glow)';
        } else if (state === 'THINKING') {
            assistantOrb.classList.add('thinking');
            assistantStateLabel.style.color = 'var(--accent)';
            assistantStateLabel.style.textShadow = '0 0 8px var(--accent-glow)';
        } else if (state === 'SPEAKING') {
            assistantOrb.classList.add('speaking');
            assistantStateLabel.style.color = 'var(--secondary)';
            assistantStateLabel.style.textShadow = '0 0 8px var(--secondary-glow)';
        } else {
            // IDLE
            assistantStateLabel.style.color = 'var(--primary)';
            assistantStateLabel.style.textShadow = '0 0 8px var(--primary-glow)';
        }
    }

    // 10. Siri-like Canvas Waves Visualizer
    function resizeCanvas() {
        canvas.width = canvas.parentElement.clientWidth;
        canvas.height = canvas.parentElement.clientHeight;
    }
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    let wavePhase = 0;
    
    // Wave Object Configuration
    const waves = [
        { amplitude: 0.15, frequency: 0.015, speed: 0.04, color: 'rgba(124, 77, 255, 0.45)' },   // Primary purple
        { amplitude: 0.1, frequency: 0.02, speed: -0.03, color: 'rgba(0, 229, 255, 0.4)' },      // Secondary cyan
        { amplitude: 0.05, frequency: 0.025, speed: 0.05, color: 'rgba(255, 64, 129, 0.35)' }    // Accent pink
    ];

    function animateVisualizer() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        const midY = canvas.height / 2;
        const width = canvas.width;
        
        wavePhase += 0.05;

        // Apply scale factors to waves depending on assistant state
        let ampMultiplier = 1.0;
        let freqMultiplier = 1.0;
        let lineThickness = 1.5;

        if (assistantState === 'LISTENING') {
            ampMultiplier = 2.2;
            freqMultiplier = 1.8;
            lineThickness = 2.0;
        } else if (assistantState === 'SPEAKING') {
            // Simulate speaking speech wave heights using sinusoidal modulation
            ampMultiplier = 1.8 + Math.sin(wavePhase * 2) * 0.8;
            freqMultiplier = 1.3;
            lineThickness = 2.2;
        } else if (assistantState === 'THINKING') {
            // Converge into a fast, low-amplitude vibration
            ampMultiplier = 0.35 + Math.sin(wavePhase * 5) * 0.1;
            freqMultiplier = 3.5;
            lineThickness = 1.0;
        } else {
            // IDLE state - slow, breathing waves
            ampMultiplier = 0.45;
            freqMultiplier = 0.8;
            lineThickness = 1.2;
        }

        // Draw individual waves
        waves.forEach((w) => {
            ctx.beginPath();
            ctx.lineWidth = lineThickness;
            ctx.strokeStyle = w.color;
            ctx.shadowBlur = assistantState !== 'IDLE' ? 12 : 4;
            ctx.shadowColor = w.color;
            
            for (let x = 0; x < width; x++) {
                // Calculate y coordinate based on sine curve
                const angle = x * w.frequency * freqMultiplier + (wavePhase * w.speed * 20);
                
                // Taper waves off at the edges of the canvas to look clean
                const edgeTaper = Math.sin((x / width) * Math.PI);
                
                const y = midY + Math.sin(angle) * (w.amplitude * canvas.height * ampMultiplier) * edgeTaper;
                
                if (x === 0) {
                    ctx.moveTo(x, y);
                } else {
                    ctx.lineTo(x, y);
                }
            }
            
            ctx.stroke();
        });
        
        ctx.shadowBlur = 0; // Reset shadow glow for other drawings
        
        requestAnimationFrame(animateVisualizer);
    }
    
    // Start visualizer animation loop
    animateVisualizer();

    // 11. Custom voice activation shortcut (Press space when input is not active)
    window.addEventListener('keydown', (e) => {
        if (e.code === 'Space' && document.activeElement !== textCommand && document.activeElement !== inputGeminiKey) {
            e.preventDefault();
            btnMic.click();
        }
    });

    // Greet user on load
    setTimeout(() => {
        speak("Welcome, sir. I am online and ready to assist you.");
    }, 1000);
});
