document.addEventListener("DOMContentLoaded", () => {
  const path = window.location.pathname;
  const isIndex = path.endsWith("/") || path.endsWith("/index.html") || (!path.endsWith(".html") && !path.includes("setup") && !path.includes("dashboard"));
  const isSetup = path.includes("setup.html") || (path.includes("setup") && !path.endsWith(".html"));
  const isDashboard = path.includes("dashboard.html") || (path.includes("dashboard") && !path.endsWith(".html"));

  if (!localStorage.getItem("edith_user_admin")) {
    localStorage.setItem("edith_user_admin", "admin"); // Default operator profile
  }

  if (isIndex) {
    const tabLogin = document.getElementById("tab-login");
    const tabRegister = document.getElementById("tab-register");
    const formLogin = document.getElementById("form-login");
    const formRegister = document.getElementById("form-register");
    const loginError = document.getElementById("login-error");
    const registerError = document.getElementById("register-error");
    const registerSuccess = document.getElementById("register-success");

    const existingUser = localStorage.getItem("edith_logged_in_user");
    if (existingUser) {
      const hasKeys = localStorage.getItem("edith_key_groq") || localStorage.getItem("edith_key_mistral");
      window.location.href = hasKeys ? "dashboard.html" : "setup.html";
      return;
    }

    if (tabLogin && tabRegister) {
      tabLogin.addEventListener("click", () => {
        tabLogin.className = "flex-1 text-center py-2 text-sm font-medium border-b-2 border-white/70 text-white transition-all cursor-pointer";
        tabRegister.className = "flex-1 text-center py-2 text-sm font-medium border-b-2 border-transparent text-white/50 hover:text-white/80 transition-all cursor-pointer";
        formLogin.classList.remove("hidden");
        formRegister.classList.add("hidden");
        loginError.classList.add("hidden");
      });

      tabRegister.addEventListener("click", () => {
        tabRegister.className = "flex-1 text-center py-2 text-sm font-medium border-b-2 border-white/70 text-white transition-all cursor-pointer";
        tabLogin.className = "flex-1 text-center py-2 text-sm font-medium border-b-2 border-transparent text-white/50 hover:text-white/80 transition-all cursor-pointer";
        formRegister.classList.remove("hidden");
        formLogin.classList.add("hidden");
        registerError.classList.add("hidden");
        registerSuccess.classList.add("hidden");
      });
    }

    if (formLogin) {
      formLogin.addEventListener("submit", (e) => {
        e.preventDefault();
        const username = document.getElementById("login-username").value.trim();
        const password = document.getElementById("login-password").value;

        loginError.classList.add("hidden");

        if (!username || !password) {
          loginError.innerText = "Operator credentials cannot be blank.";
          loginError.classList.remove("hidden");
          return;
        }

        const storedPassword = localStorage.getItem(`edith_user_${username}`);
        if (storedPassword === password) {
          localStorage.setItem("edith_logged_in_user", username);
          const hasKeys = localStorage.getItem("edith_key_groq") || localStorage.getItem("edith_key_mistral");
          window.location.href = hasKeys ? "dashboard.html" : "setup.html";
        } else {
          loginError.innerText = "Access denied. Invalid operator credentials.";
          loginError.classList.remove("hidden");
        }
      });
    }

    if (formRegister) {
      formRegister.addEventListener("submit", (e) => {
        e.preventDefault();
        const username = document.getElementById("register-username").value.trim();
        const password = document.getElementById("register-password").value;
        const confirm = document.getElementById("register-confirm").value;

        registerError.classList.add("hidden");
        registerSuccess.classList.add("hidden");

        if (!username || !password || !confirm) {
          registerError.innerText = "Please fill out all registration fields.";
          registerError.classList.remove("hidden");
          return;
        }

        if (password !== confirm) {
          registerError.innerText = "Security passwords do not match.";
          registerError.classList.remove("hidden");
          return;
        }

        if (localStorage.getItem(`edith_user_${username}`)) {
          registerError.innerText = "Operator username is already registered.";
          registerError.classList.remove("hidden");
          return;
        }

        localStorage.setItem(`edith_user_${username}`, password);
        registerSuccess.classList.remove("hidden");
        formRegister.reset();
      });
    }
  }

  if (isSetup) {
    const activeUser = localStorage.getItem("edith_logged_in_user");
    if (!activeUser) {
      window.location.href = "index.html";
      return;
    }

    const alreadyHasKeys = localStorage.getItem("edith_key_groq") || localStorage.getItem("edith_key_mistral");
    if (alreadyHasKeys) {
      window.location.href = "dashboard.html";
      return;
    }

    const formSetup = document.getElementById("form-setup");
    const skipBtn = document.getElementById("setup-skip");

    const groqKey = document.getElementById("setup-groq");
    const mistralKey = document.getElementById("setup-mistral");
    const safeKey = document.getElementById("setup-safebrowsing");
    const vtKey = document.getElementById("setup-virustotal");

    if (groqKey) groqKey.value = localStorage.getItem("edith_key_groq") || "";
    if (mistralKey) mistralKey.value = localStorage.getItem("edith_key_mistral") || "";
    if (safeKey) safeKey.value = localStorage.getItem("edith_key_safebrowsing") || "";
    if (vtKey) vtKey.value = localStorage.getItem("edith_key_virustotal") || "";

    if (formSetup) {
      formSetup.addEventListener("submit", (e) => {
        e.preventDefault();
        localStorage.setItem("edith_key_groq", groqKey.value.trim());
        localStorage.setItem("edith_key_mistral", mistralKey.value.trim());
        localStorage.setItem("edith_key_safebrowsing", safeKey.value.trim());
        localStorage.setItem("edith_key_virustotal", vtKey.value.trim());
        window.location.href = "dashboard.html";
      });
    }


    if (skipBtn) {
      skipBtn.addEventListener("click", () => {
        window.location.href = "dashboard.html";
      });
    }
  }

  if (isDashboard) {
    const activeUser = localStorage.getItem("edith_logged_in_user");
    if (!activeUser) {
      window.location.href = "index.html";
      return;
    }

    
    const swapperDashboard = document.getElementById("swapper-dashboard");
    const swapperTools = document.getElementById("swapper-tools");
    const activePill = document.getElementById("swapper-active-pill");
    const aiSection = document.getElementById("ai-section");
    const toolsSection = document.getElementById("tools-section");

    const updateSwapperPosition = (activeBtn, inactiveBtn) => {
      activeBtn.classList.add("text-slate-850");
      activeBtn.classList.remove("text-slate-500");
      inactiveBtn.classList.remove("text-slate-850");
      inactiveBtn.classList.add("text-slate-500");

      if (activePill) {
        activePill.style.left = `${activeBtn.offsetLeft}px`;
        activePill.style.width = `${activeBtn.offsetWidth}px`;
      }
    };

    if (swapperDashboard && swapperTools) {
      setTimeout(() => {
        updateSwapperPosition(swapperDashboard, swapperTools);
      }, 80);

      swapperDashboard.addEventListener("click", () => {
        aiSection.classList.remove("hidden");
        toolsSection.classList.add("hidden");
        updateSwapperPosition(swapperDashboard, swapperTools);
      });

      swapperTools.addEventListener("click", () => {
        aiSection.classList.add("hidden");
        toolsSection.classList.remove("hidden");
        updateSwapperPosition(swapperTools, swapperDashboard);
      });

      window.addEventListener("resize", () => {
        if (!toolsSection.classList.contains("hidden")) {
          updateSwapperPosition(swapperTools, swapperDashboard);
        } else {
          updateSwapperPosition(swapperDashboard, swapperTools);
        }
      });
    }

    const bgUserName = document.getElementById("bg-user-name");
    if (bgUserName) bgUserName.innerText = activeUser;

    const logoutBtn = document.getElementById("btn-logout");
    if (logoutBtn) {
      logoutBtn.addEventListener("click", () => {
        localStorage.removeItem("edith_logged_in_user");
        window.location.href = "index.html";
      });
    }

    const updateModelBadge = () => {
      const groqActive = !!localStorage.getItem("edith_key_groq");
      const mistralActive = !!localStorage.getItem("edith_key_mistral");
      const modelStatus = document.getElementById("ai-model-status");
      if (modelStatus) {
        if (groqActive && mistralActive) {
          modelStatus.innerText = "GROQ & MISTRAL KEY DIRECTIVE ACTIVE";
          modelStatus.className = "text-[10px] mono-display text-emerald-450";
        } else if (groqActive) {
          modelStatus.innerText = "GROQ INTEL VECTOR ACTIVE";
          modelStatus.className = "text-[10px] mono-display text-emerald-450";
        } else if (mistralActive) {
          modelStatus.innerText = "MISTRAL MODEL DIRECTIVE ACTIVE";
          modelStatus.className = "text-[10px] mono-display text-emerald-450";
        } else {
          modelStatus.innerText = "MODEL OFFLINE (DEMO ANALYTICS)";
          modelStatus.className = "text-[10px] mono-display text-white/30";
        }
      }
    };
    updateModelBadge();

    const btnAnalyze = document.getElementById("btn-analyze");
    const aiInput = document.getElementById("ai-input");
    const aiResult = document.getElementById("ai-result");
    const aiLoader = document.getElementById("ai-loader");

    const formatResult = (text) => {
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/^# (.*?)$/gm, '<h1 class="text-xl font-bold mt-4 mb-2 text-slate-800">🛡️ $1</h1>')
    .replace(/^## (.*?)$/gm, '<h2 class="text-lg font-bold mt-4 mb-1 text-slate-800">🔍 $1</h2>')
    .replace(/^### (.*?)$/gm, '<h3 class="text-base font-bold mt-3 mb-1 text-slate-800">📌 $1</h3>')
    .replace(/\bcritical\b/gi, '🔴 <strong>CRITICAL</strong>')
    .replace(/\bhigh\b/gi, '🟠 <strong>HIGH</strong>')
    .replace(/\bmedium\b/gi, '🟡 <strong>MEDIUM</strong>')
    .replace(/\blow\b/gi, '🟢 <strong>LOW</strong>')
    .replace(/\bwarning\b/gi, '⚠️ WARNING')
    .replace(/\berror\b/gi, '❌ ERROR')
    .replace(/\bsuccess\b/gi, '✅ SUCCESS')
    .replace(/\brecommendation\b/gi, '💡 Recommendation')
    .replace(/^\* (.*?)$/gm, '<li class="ml-4 list-disc text-slate-700">$1</li>')
    .replace(/^- (.*?)$/gm, '<li class="ml-4 list-disc text-slate-700">$1</li>')
    .replace(/\n/g, '<br>');
};
    const runAiAnalysis = async () => {
      const query = aiInput.value.trim();
      if (!query) {
        aiResult.innerText = "System: Waiting for input framework. Please paste logs or security threat incident data.";
        return;
      }

      aiLoader.classList.remove("opacity-0", "pointer-events-none");
      aiLoader.classList.add("opacity-100", "pointer-events-auto");

      try {
        const response = await fetch("http://127.0.0.1:8000/analyze", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: query })
        });

        if (!response.ok) throw new Error("API Connection Faulted");
        const data = await response.json();
        aiResult.innerHTML = formatResult(data.result || "");
      } catch (err) {
        aiResult.textContent = "Something went wrong. Please try again.";
      } finally {
        aiLoader.classList.add("opacity-0", "pointer-events-none");
        aiLoader.classList.remove("opacity-100", "pointer-events-auto");
      }
    };

    if (btnAnalyze) {
      btnAnalyze.addEventListener("click", runAiAnalysis);
    }

    if (aiInput) {
      aiInput.addEventListener("keydown", (e) => {
        if (e.ctrlKey && e.key === "Enter") {
          e.preventDefault();
          runAiAnalysis();
        }
      });
    }

    const toolModal = document.getElementById("tool-modal");
    const toolModalBody = document.getElementById("tool-modal-body");
    const btnCloseTool = document.getElementById("btn-close-tool-modal");

    const toolIconContainer = document.getElementById("tool-modal-icon-container");
    const toolModalName = document.getElementById("tool-modal-name");
    const toolModalDesc = document.getElementById("tool-modal-desc");
    const toolModalLabel = document.getElementById("tool-modal-label");
    const toolModalInput = document.getElementById("tool-modal-input");
    const btnToolExecute = document.getElementById("btn-tool-execute");
    const toolModalResult = document.getElementById("tool-modal-result");
    const toolModalLoader = document.getElementById("tool-modal-loader");

    let currentTool = "";

    const toolsConfig = {
      safebrowsing: {
        name: "Google Safe Browsing Search",
        desc: "Check target URLs against Google global database of unsafe pages.",
        label: "Target Threat URL to Scan",
        placeholder: "https://dangerous-site-example.com",
        icon: `<svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.57-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z"/></svg>`,
        queryParam: "url",
        endpointUrl: (param) => `http://127.0.0.1:8000/tools/safe-browsing?url=${encodeURIComponent(param)}`
      },
      virustotal: {
        name: "VirusTotal Scan Hub",
        desc: "Scan targets using 70+ antivirus and blacklisting scanners.",
        label: "URL Endpoint to Query",
        placeholder: "http://malicious-server.net",
        icon: `<svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.604 10.604z"/></svg>`,
        queryParam: "url",
        endpointUrl: (param) => `http://127.0.0.1:8000/tools/virustotal?url=${encodeURIComponent(param)}`
      },
      ipinfo: {
        name: "IP Address Information Geo-Scanner",
        desc: "Query IP network provider geolocation, routing, and WHOIS entries.",
        label: "IP Address (IPv4 / IPv6)",
        placeholder: "8.8.8.8",
        icon: `<svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25s-7.5-4.108-7.5-11.25a7.5 7.5 0 1115 0z"/></svg>`,
        queryParam: "ip",
        endpointUrl: (param) => `http://127.0.0.1:8000/tools/ipinfo?ip=${encodeURIComponent(param)}`
      },
      dnslookup: {
        name: "DNS Namespace Registrar Query",
        desc: "Query active NS parameters, digital certificates, MX and A record bindings.",
        label: "Target Domain Name",
        placeholder: "microsoft.com",
        icon: `<svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 017.843 4.582M12 3a8.997 8.997 0 00-7.843 4.582m15.686 0A11.953 11.953 0 0112 10.5c-2.998 0-5.74-.154-8.243-.466M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>`,
        queryParam: "domain",
        endpointUrl: (param) => `http://127.0.0.1:8000/tools/dns-lookup?domain=${encodeURIComponent(param)}`
      }
    };

    const formatToolResult = (text) => {
    return text
    .replace(/DANGEROUS/g, '🔴 <strong>DANGEROUS</strong>')
    .replace(/SAFE/g, '✅ <strong>SAFE</strong>')
    .replace(/MALWARE/g, '☣️ <strong>MALWARE</strong>')
    .replace(/SOCIAL_ENGINEERING/g, '🎭 <strong>SOCIAL ENGINEERING</strong>')
    .replace(/UNWANTED_SOFTWARE/g, '⚠️ <strong>UNWANTED SOFTWARE</strong>')
    .replace(/Malicious Engine\s*:/g, '🔴 Malicious Engines :')
    .replace(/Suspicious Engine\s*:/g, '🟡 Suspicious Engines :')
    .replace(/Harmless Engine\s*:/g, '✅ Harmless Engines :')
    .replace(/Flagged by\s*:/g, '🚩 Flagged by :')
    .replace(/IP\s*:/g, '🌐 IP :')
    .replace(/Hostname\s*:/g, '💻 Hostname :')
    .replace(/ORG\/ISP\s*:/g, '🏢 ORG/ISP :')
    .replace(/City\s*:/g, '🏙️ City :')
    .replace(/Region\s*:/g, '📍 Region :')
    .replace(/Country\s*:/g, '🌍 Country :')
    .replace(/Timezone\s*:/g, '🕐 Timezone :')
    .replace(/Domain\s*:/g, '🌐 Domain :')
    .replace(/IPv4\s*:/g, '4️⃣ IPv4 :')
    .replace(/IPv6\s*:/g, '6️⃣ IPv6 :')
    .replace(/Status\s*:/g, '📡 Status :')
    .replace(/Reachable/g, '✅ Reachable')
    .replace(/UnReachable/g, '🔴 Unreachable')
    .replace(/LookUp Time\s*:/g, '⚡ Lookup Time :')
    .replace(/\n/g, '<br>');
    };
    
    const openToolModal = (toolId) => {
      currentTool = toolId;
      const conf = toolsConfig[toolId];

      if (!conf) return;

      toolIconContainer.innerHTML = conf.icon;
      toolModalName.innerText = conf.name;
      toolModalDesc.innerText = conf.desc;
      toolModalLabel.innerText = conf.label;
      toolModalInput.value = "";
      toolModalInput.placeholder = conf.placeholder;
      toolModalResult.textContent = `Awaiting threat directive scan parameters... (${toolId})`;

      toolModal.classList.remove("hidden");
    };

    const closeToolModal = () => {
      toolModal.classList.add("hidden");
      currentTool = "";
    };

    if (btnCloseTool) btnCloseTool.addEventListener("click", closeToolModal);

    const tileS = document.getElementById("tile-safebrowsing");
    const tileV = document.getElementById("tile-virustotal");
    const tileI = document.getElementById("tile-ipinfo");
    const tileD = document.getElementById("tile-dnslookup");

    if (tileS) tileS.addEventListener("click", () => openToolModal("safebrowsing"));
    if (tileV) tileV.addEventListener("click", () => openToolModal("virustotal"));
    if (tileI) tileI.addEventListener("click", () => openToolModal("ipinfo"));
    if (tileD) tileD.addEventListener("click", () => openToolModal("dnslookup"));

    if (btnToolExecute) {
      btnToolExecute.addEventListener("click", async () => {
        const val = toolModalInput.value.trim();
        if (!val) {
          toolModalResult.textContent = "Error: Input query payload parameter cannot be empty.";
          return;
        }

        const conf = toolsConfig[currentTool];
        if (!conf) return;

        toolModalLoader.classList.remove("opacity-0", "pointer-events-none");
        toolModalLoader.classList.add("opacity-100", "pointer-events-auto");

        try {
          const fetchUrl = conf.endpointUrl(val);
          const res = await fetch(fetchUrl);
          if (!res.ok) throw new Error("Tool invocation failed");

          const data = await res.json();
          toolModalResult.innerHTML = formatToolResult(data.result || "");
        } catch (err) {
          toolModalResult.textContent = "Something went wrong. Please try again.";
        } finally {
          toolModalLoader.classList.add("opacity-0", "pointer-events-none");
          toolModalLoader.classList.remove("opacity-100", "pointer-events-auto");
        }
      });
    }

    toolModal.addEventListener("click", (e) => {
      if (e.target === toolModal) closeToolModal();
    });

    const settingsModal = document.getElementById("settings-modal");
    const btnOpenSettings = document.getElementById("btn-modal-settings");
    const btnCloseSettings = document.getElementById("btn-close-settings-modal");
    const formSettings = document.getElementById("form-modal-settings");

    const modalGroq = document.getElementById("modal-setup-groq");
    const modalMistral = document.getElementById("modal-setup-mistral");
    const modalSafebrowsing = document.getElementById("modal-setup-safebrowsing");
    const modalVirustotal = document.getElementById("modal-setup-virustotal");

    if (btnOpenSettings) {
      btnOpenSettings.addEventListener("click", () => {
        if (modalGroq) modalGroq.value = localStorage.getItem("edith_key_groq") || "";
        if (modalMistral) modalMistral.value = localStorage.getItem("edith_key_mistral") || "";
        if (modalSafebrowsing) modalSafebrowsing.value = localStorage.getItem("edith_key_safebrowsing") || "";
        if (modalVirustotal) modalVirustotal.value = localStorage.getItem("edith_key_virustotal") || "";

        settingsModal.classList.remove("hidden");
      });
    }

    const closeSettingsModal = () => {
      settingsModal.classList.add("hidden");
    };

    if (btnCloseSettings) btnCloseSettings.addEventListener("click", closeSettingsModal);

    if (formSettings) {
      formSettings.addEventListener("submit", (e) => {
        e.preventDefault();
        localStorage.setItem("edith_key_groq", modalGroq.value.trim());
        localStorage.setItem("edith_key_mistral", modalMistral.value.trim());
        localStorage.setItem("edith_key_safebrowsing", modalSafebrowsing.value.trim());
        localStorage.setItem("edith_key_virustotal", modalVirustotal.value.trim());

        updateModelBadge();
        closeSettingsModal();
      });
    }

    settingsModal.addEventListener("click", (e) => {
      if (e.target === settingsModal) closeSettingsModal();
    });

    const profileModal = document.getElementById("profile-modal");
    const btnOpenProfile = document.getElementById("btn-modal-profile");
    const btnCloseProfile = document.getElementById("btn-close-profile-modal");
    const formProfile = document.getElementById("form-modal-profile");
    const modalProfileName = document.getElementById("modal-profile-name");

    if (btnOpenProfile) {
      btnOpenProfile.addEventListener("click", () => {
        if (modalProfileName) {
          modalProfileName.value = localStorage.getItem("edith_logged_in_user") || "";
        }
        profileModal.classList.remove("hidden");
      });
    }

    const closeProfileModal = () => {
      profileModal.classList.add("hidden");
    };

    if (btnCloseProfile) btnCloseProfile.addEventListener("click", closeProfileModal);

    if (formProfile) {
      formProfile.addEventListener("submit", (e) => {
        e.preventDefault();
        const newName = modalProfileName.value.trim();
        if (newName) {
          const oldName = localStorage.getItem("edith_logged_in_user");
          const oldPass = localStorage.getItem(`edith_user_${oldName}`);

          localStorage.removeItem(`edith_user_${oldName}`);
          localStorage.setItem(`edith_user_${newName}`, oldPass || "admin");
          localStorage.setItem("edith_logged_in_user", newName);

          if (bgUserName) bgUserName.innerText = newName;

          closeProfileModal();
        }
      });
    }

    profileModal.addEventListener("click", (e) => {
      if (e.target === profileModal) closeProfileModal();
    });
  }
});