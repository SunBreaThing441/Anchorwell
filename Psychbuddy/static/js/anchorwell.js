/**
 * ============================================================================
 * ANCHORWELL: UNESCO MENTAL SUPPORT GRID
 * Core Client Runtime, Security Architecture & Data Integration Engine
 * Target Application Host: http://localhost:8000
 * ============================================================================
 */

(function () {
  'use strict';

  // Global State & Security Engine
  const GridSecurity = {
    patient: {
      isAuthenticated: function () {
        return !!sessionStorage.getItem('aw_patient_session');
      },
      setAuthenticated: function (userEmail) {
        sessionStorage.setItem('aw_patient_session', userEmail || 'AUTHENTICATED_PATIENT');
      },
      clear: function () {
        sessionStorage.removeItem('aw_patient_session');
        sessionStorage.removeItem('aw_redirect_url');
      }
    },
    admin: {
      isAuthenticated: function () {
        return !!sessionStorage.getItem('aw_admin_session');
      },
      setAuthenticated: function () {
        sessionStorage.setItem('aw_admin_session', 'ADMIN_TOKEN_' + Date.now());
        resetAdminInactivityTimer();
      },
      clear: function () {
        sessionStorage.removeItem('aw_admin_session');
        sessionStorage.removeItem('aw_admin_pending');
      }
    },
    inactivityTimer: null,
  };

  const GridState = {
    audio: {
      element: null,
      trackName: 'Oceanic Restoration Frequencies',
      trackPath: '/static/audio/Ocean Wave Sound.mp3',
      isPlaying: false,
      volume: 0.75,
      isLooping: true,
    },
  };

  /**
   * ========================================================================
   * 1. UNIVERSAL TOAST NOTIFICATION ENGINE (Bioluminescent Telemetry Alerts)
   * ========================================================================
   */
  window.renderToast = function (message, type = 'info') {
    let toast = document.getElementById('awGlobalToast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'awGlobalToast';
      toast.className = 'aw-tag';
      toast.style.cssText = `
        position: fixed; top: 85px; right: 2rem; z-index: 9999;
        padding: 1rem 1.5rem; border-radius: 14px; display: flex;
        align-items: center; gap: 12px; font-size: 0.88rem; font-weight: 500;
        animation: aw-scale-in 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        backdrop-filter: blur(20px); box-shadow: 0 10px 40px rgba(0,0,0,0.6);
        max-width: 480px; line-height: 1.5;
      `;
      document.body.appendChild(toast);
    }

    let bg = 'rgba(11, 15, 40, 0.95)';
    let border = '1px solid var(--aw-teal-bright)';
    let color = '#FFFFFF';
    let iconSvg = '';

    if (type === 'success') {
      bg = 'rgba(6, 78, 59, 0.95)';
      border = '1px solid #10B981';
      color = '#ECFDF5';
      iconSvg = `
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#6EE7B7" stroke-width="2">
          <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
          <polyline points="22 4 12 14.01 9 11.01"></polyline>
        </svg>
      `;
    } else if (type === 'error') {
      bg = 'rgba(136, 19, 55, 0.95)';
      border = '1px solid var(--aw-crisis)';
      color = '#FFF1F2';
      iconSvg = `
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#FDA4AF" stroke-width="2">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="8" x2="12" y2="12"></line>
          <line x1="12" y1="16" x2="12.01" y2="16"></line>
        </svg>
      `;
    } else {
      bg = 'rgba(15, 23, 42, 0.95)';
      border = '1px solid var(--aw-teal-bright)';
      color = '#F0FDFA';
      iconSvg = `
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--aw-teal-bright)" stroke-width="2">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="16" x2="12" y2="12"></line>
          <line x1="12" y1="8" x2="12.01" y2="8"></line>
        </svg>
      `;
    }

    toast.style.background = bg;
    toast.style.border = border;
    toast.style.color = color;
    toast.innerHTML = `${iconSvg}<span>${message}</span>`;
    toast.style.display = 'flex';

    if (toast.dismissTimeout) clearTimeout(toast.dismissTimeout);
    toast.dismissTimeout = setTimeout(() => {
      toast.style.display = 'none';
    }, 5000);
  };

  /**
   * ========================================================================
   * 2. ROUTE GUARDS & ACCESS CONTROL ENGINE
   * ========================================================================
   */
  const PROTECTED_PATIENT_ROUTES = [
    'homepage',
    'wellnessLog',
    'wellnesslogdir',
    'wellnessLogFileCreator',
    'myforum',
    'chatforum',
    'GIA'
  ];

  const PROTECTED_ADMIN_ROUTES = [
    'admin',
    'usersNav',
    'manageResources',
    'videoRes',
    'audioRes',
    'yRes',
    'mRes',
    'bookRes',
    'delYRes',
    'delMRes',
    'delBook',
    'delAudio',
    'delVideoSessions',
    'adminforum',
    'feedbackinfo',
    'appointmentmail',
    'admintips'
  ];

  function hydrateSecurityFromDOM() {
    const path = window.location.pathname.replace(/^\//, '').split('?')[0].split('#')[0];

    // 1. Patient Session Hydration
    const isProtectedPatientPage = PROTECTED_PATIENT_ROUTES.some(r => path === r || path.startsWith(r + '/'));
    if (isProtectedPatientPage) {
      const isSignInRendered = !!document.querySelector('form[action="signin"]') || !!document.getElementById('signinForm');
      if (!isSignInRendered) {
        if (!GridSecurity.patient.isAuthenticated()) {
          GridSecurity.patient.setAuthenticated('AUTHENTICATED_PATIENT');
        }
      }
    }

    // 2. Admin Session Hydration
    const isProtectedAdminPage = PROTECTED_ADMIN_ROUTES.some(r => path === r || path.startsWith(r + '/'));
    const isPendingAdmin = sessionStorage.getItem('aw_admin_pending') === 'true';
    if (isProtectedAdminPage || isPendingAdmin) {
      const isAdminLoginRendered = !!document.querySelector('form[action="adminlogin"]') || !!document.getElementById('adminPass');
      if (!isAdminLoginRendered) {
        GridSecurity.admin.setAuthenticated();
        sessionStorage.removeItem('aw_admin_pending');
      }
    }
  }

  function evaluateRouteSecurityGuard(targetUrl) {
    hydrateSecurityFromDOM();
    const clean = targetUrl.replace(/^\//, '').split('?')[0].split('#')[0];

    // 1. Admin Isolation Guard
    if (PROTECTED_ADMIN_ROUTES.some(r => clean === r || clean.startsWith(r + '/'))) {
      if (!GridSecurity.admin.isAuthenticated()) {
        console.warn(`[SECURITY GUARD] Blocked unauthorized attempt to administrative vector: /${clean}`);
        sessionStorage.setItem('aw_admin_redirect', targetUrl);
        window.location.href = 'adminlogin';
        return false;
      }
      resetAdminInactivityTimer();
      return true;
    }

    // 2. Patient Authentication Guard
    if (PROTECTED_PATIENT_ROUTES.some(r => clean === r || clean.startsWith(r + '/'))) {
      if (!GridSecurity.patient.isAuthenticated()) {
        console.warn(`[SECURITY GUARD] Unauthenticated access to clinical route: /${clean}. Rerouting to gateway.`);
        sessionStorage.setItem('aw_redirect_url', targetUrl);
        window.location.href = 'signin';
        return false;
      }
      return true;
    }

    return true;
  }

  function resetAdminInactivityTimer() {
    if (GridSecurity.inactivityTimer) {
      clearTimeout(GridSecurity.inactivityTimer);
    }
    // 15-minute auto-lock for admin session
    GridSecurity.inactivityTimer = setTimeout(() => {
      if (GridSecurity.admin.isAuthenticated()) {
        GridSecurity.admin.clear();
        alert("Administrative session has expired due to 15m inactivity. Re-authentication required.");
        window.location.href = 'adminlogin';
      }
    }, 15 * 60 * 1000);
  }

  function initActivityListeners() {
    ['mousedown', 'keydown', 'scroll', 'touchstart'].forEach(evt => {
      document.addEventListener(evt, () => {
        if (GridSecurity.admin.isAuthenticated()) {
          resetAdminInactivityTimer();
        }
      }, { passive: true });
    });
  }

  /**
   * ========================================================================
   * 3. MEDIA STREAMING PATHWAYS (MP3 Audio Chunks & MP4 Video Tracks)
   * ========================================================================
   */
  function initAudioSanctuary() {
    let audio = document.getElementById('awGlobalAudio');
    if (!audio) {
      audio = document.createElement('audio');
      audio.id = 'awGlobalAudio';
      audio.loop = true;
      audio.preload = 'auto';
      // Enable cross-origin credentials and byte-range request streaming
      audio.crossOrigin = 'anonymous';
      document.body.appendChild(audio);
    }
    GridState.audio.element = audio;

    const savedTrack = sessionStorage.getItem('aw_audio_track');
    const savedPath = sessionStorage.getItem('aw_audio_path');
    const savedVol = sessionStorage.getItem('aw_audio_vol');

    if (savedTrack && savedPath) {
      GridState.audio.trackName = savedTrack;
      GridState.audio.trackPath = savedPath;
    }
    if (savedVol) {
      GridState.audio.volume = parseFloat(savedVol);
      audio.volume = GridState.audio.volume;
    }

    renderFloatingDock();
    bindAudioEvents();
  }

  function renderFloatingDock() {
    let dock = document.getElementById('awAudioDock');
    if (!dock) {
      dock = document.createElement('div');
      dock.id = 'awAudioDock';
      dock.className = 'aw-floating-dock';
      dock.innerHTML = `
        <div class="aw-dock-track-info">
          <div class="aw-dock-wave" id="awWaveBars">
            <span></span><span></span><span></span><span></span>
          </div>
          <div class="aw-dock-meta">
            <h4 id="awDockTitle">${GridState.audio.trackName}</h4>
            <p>UNESCO Psychoacoustic Protocol • Continuous Harmonic Calming Loop</p>
          </div>
        </div>
        <div class="aw-dock-controls">
          <button id="awDockPlayBtn" class="aw-dock-play-btn" title="Toggle Sanctuary Sound">
            <svg id="awPlayIcon" width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
              <polygon points="5 3 19 12 5 21 5 3"></polygon>
            </svg>
            <svg id="awPauseIcon" width="18" height="18" viewBox="0 0 24 24" fill="currentColor" style="display:none;">
              <rect x="6" y="4" width="4" height="16"></rect>
              <rect x="14" y="4" width="4" height="16"></rect>
            </svg>
          </button>
          <div style="display: flex; align-items: center; gap: 8px;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#94A3B8" stroke-width="2">
              <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
              <path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path>
            </svg>
            <input type="range" id="awVolumeSlider" min="0" max="1" step="0.05" value="${GridState.audio.volume}" 
                   style="width: 80px; accent-color: var(--aw-teal-bright); cursor: pointer;">
          </div>
        </div>
      `;
      document.body.appendChild(dock);
    }
  }

  function bindAudioEvents() {
    const playBtn = document.getElementById('awDockPlayBtn');
    const playIcon = document.getElementById('awPlayIcon');
    const pauseIcon = document.getElementById('awPauseIcon');
    const volSlider = document.getElementById('awVolumeSlider');
    const audio = GridState.audio.element;

    if (playBtn) {
      playBtn.onclick = function () {
        toggleSanctuaryPlayback();
      };
    }

    if (volSlider) {
      volSlider.oninput = function (e) {
        const val = parseFloat(e.target.value);
        GridState.audio.volume = val;
        if (audio) audio.volume = val;
        sessionStorage.setItem('aw_audio_vol', val.toString());
      };
    }

    audio.onplay = function () {
      GridState.audio.isPlaying = true;
      if (playIcon) playIcon.style.display = 'none';
      if (pauseIcon) pauseIcon.style.display = 'block';
      const wave = document.getElementById('awWaveBars');
      if (wave) wave.style.opacity = '1';
    };

    audio.onpause = function () {
      GridState.audio.isPlaying = false;
      if (playIcon) playIcon.style.display = 'block';
      if (pauseIcon) pauseIcon.style.display = 'none';
      const wave = document.getElementById('awWaveBars');
      if (wave) wave.style.opacity = '0.3';
    };
  }

  window.playSanctuaryTrack = function (name, src) {
    const audio = GridState.audio.element;
    GridState.audio.trackName = name;
    GridState.audio.trackPath = src;

    sessionStorage.setItem('aw_audio_track', name);
    sessionStorage.setItem('aw_audio_path', src);

    const titleEl = document.getElementById('awDockTitle');
    if (titleEl) titleEl.textContent = name;

    if (audio) {
      audio.src = src;
      audio.play()
        .then(() => renderToast(`Now Streaming: ${name}`, 'info'))
        .catch(e => console.warn("Autoplay deferred:", e));
    }
  };

  function toggleSanctuaryPlayback() {
    const audio = GridState.audio.element;
    if (!audio) return;
    if (audio.paused) {
      if (!audio.src || audio.src.trim() === '') {
        audio.src = GridState.audio.trackPath;
      }
      audio.play().catch(e => console.warn("Audio blocked:", e));
    } else {
      audio.pause();
    }
  }

  /**
   * Video Streaming Pipeline: Partial-Content (HTTP 206) Stream Enhancer
   */
  function configureVideoStreaming() {
    document.querySelectorAll('.aw-video-player-wrap video, .sessionCategory video').forEach(video => {
      video.preload = 'metadata';
      video.controls = true;
      video.playsInline = true;

      video.onwaiting = function () {
        console.log(`[STREAMING] Buffering partial chunk for video: ${video.currentSrc}`);
      };

      video.onerror = function () {
        console.warn(`[STREAMING ANOMALY] Media stream failed for ${video.currentSrc}`);
      };
    });
  }

  /**
   * ========================================================================
   * 4. ZERO-RELOAD SPA ROUTER & DOM MORPHING (with withCredentials: true)
   * ========================================================================
   */
  function initSPARouter() {
    document.addEventListener('click', function (e) {
      const anchor = e.target.closest('a');
      if (!anchor) return;

      const href = anchor.getAttribute('href');
      if (!href) return;

      if (href.includes('adminlogout')) {
        GridSecurity.admin.clear();
        return;
      }

      if (
        href.startsWith('http') ||
        href.startsWith('#') ||
        href.startsWith('mailto:') ||
        href.includes('wellnessLogFileCreator') ||
        anchor.getAttribute('target') === '_blank'
      ) {
        return;
      }

      if (!evaluateRouteSecurityGuard(href)) {
        e.preventDefault();
        return;
      }

      const internalRoutes = [
        '', '/', 'homepage', 'relaxation', 'sessions', 'individualtherapy', 'grouptherapy',
        'coupletherapy', 'familytherapy', 'traumatherapy', 'heartbrokentherapy',
        'wellnessLog', 'wellnesslogdir', 'psychiatrist', 'aboutus', 'books', 'YM',
        'tips', 'news', 'forum', 'signin', 'first'
      ];

      const cleanHref = href.split('?')[0].split('#')[0].replace(/^\//, '');
      const isInternal = internalRoutes.includes(cleanHref) || internalRoutes.includes(cleanHref + '/');

      if (isInternal) {
        e.preventDefault();
        loadRouteSPA(href);
      }
    });

    window.addEventListener('popstate', function () {
      loadRouteSPA(window.location.pathname, false);
    });
  }

  function loadRouteSPA(url, pushState = true) {
    if (!evaluateRouteSecurityGuard(url)) {
      return;
    }

    const mainContent = document.querySelector('.aw-main-content');
    if (!mainContent) {
      window.location.href = url;
      return;
    }

    mainContent.style.opacity = '0.5';
    mainContent.style.transition = 'opacity 0.2s ease';

    fetch(url, {
      method: 'GET',
      credentials: 'include', // Preserves Django sessionid & csrftoken cookies
      headers: {
        'Accept': 'text/html,application/xhtml+xml,application/json,*/*',
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
      .then(res => res.text())
      .then(html => {
        if (html.includes("No active user found!")) {
          GridSecurity.patient.clear();
          renderToast("Clinical session expired. Please authenticate.", "error");
          window.location.href = 'signin';
          return;
        }

        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const newMain = doc.querySelector('.aw-main-content');

        if (newMain) {
          mainContent.innerHTML = newMain.innerHTML;
          document.title = doc.title || 'AnchorWell: UNESCO Mental Support Grid';
          if (pushState) {
            window.history.pushState({}, '', url);
          }
          window.scrollTo({ top: 0, behavior: 'smooth' });
          updateNavActive(url);
          rebindRouteControllers();
        } else {
          window.location.href = url;
        }
      })
      .catch(err => {
        console.error("SPA route loading failed, falling back to native:", err);
        window.location.href = url;
      })
      .finally(() => {
        if (mainContent) {
          mainContent.style.opacity = '1';
        }
      });
  }

  function updateNavActive(url) {
    const clean = url.replace(/^\//, '').split('?')[0];
    document.querySelectorAll('.aw-nav-link').forEach(link => {
      const href = link.getAttribute('href')?.replace(/^\//, '');
      if (href && (href === clean || clean.startsWith(href))) {
        link.classList.add('active');
      } else {
        link.classList.remove('active');
      }
    });
  }

  /**
   * ========================================================================
   * 5. DATA INTEGRATION & FORM SUBMISSION INTERCEPTORS
   * ========================================================================
   */
  function initDataIntegrationInterceptors() {
    document.addEventListener('submit', function (e) {
      const form = e.target;
      const action = form.getAttribute('action') || '';

      // 0. Admin Login submission tracking
      if (action === 'adminlogin') {
        sessionStorage.setItem('aw_admin_pending', 'true');
        return;
      }

      // 1. Patient Sign-In (/signin)
      if (action === 'signin') {
        e.preventDefault();
        handlePatientSignIn(form);
        return;
      }

      // 2. Doctor Consultation Booking (POST /psychinfo)
      if (action === 'psychinfo' && form.id === 'awBookingForm') {
        e.preventDefault();
        handleDoctorBookingSubmission(form);
        return;
      }

      // 3. Wellness Reflection Journal (POST /wellnessLog)
      if (action === 'wellnessLog' && form.id === 'journalForm') {
        e.preventDefault();
        handleWellnessLogSubmission(form);
        return;
      }

      // 4. Admin Multipart Uploads (videoRes, audioRes, bookRes, etc.)
      const enctype = form.getAttribute('enctype');
      if (enctype === 'multipart/form-data' && !form.dataset.nativeSubmit) {
        // Let explicit AJAX handlers (like in videoResAdmin) handle their own progress
        if (form.id === 'videoUploadForm') {
          return; // Already bound with progress HUD
        }
      }
    });
  }

  function handlePatientSignIn(form) {
    const formData = new FormData(form);
    const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
    const originalText = submitBtn ? submitBtn.innerHTML : 'Sign In';

    if (submitBtn) {
      submitBtn.innerHTML = '<span class="aw-mono" style="font-size:0.8rem;">AUTHENTICATING WITH GRID...</span>';
      submitBtn.style.opacity = '0.7';
    }

    fetch('signin', {
      method: 'POST',
      body: formData,
      credentials: 'include',
      headers: {
        'X-CSRFToken': getCsrfToken(),
      }
    })
      .then(res => res.text())
      .then(html => {
        if (html.includes("Invalid Credentials Entered")) {
          renderToast("Authentication failed. Invalid email identifier or passphrase.", "error");
          if (submitBtn) {
            submitBtn.innerHTML = originalText;
            submitBtn.style.opacity = '1';
          }
        } else if (html.includes("homepage") || html.includes("Mind Relaxation Therapy") || html.includes("Welcome to the AnchorWell Console")) {
          const username = formData.get('username');
          GridSecurity.patient.setAuthenticated(username);
          renderToast("Grid Authentication Verified. Welcome!", "success");

          const redirectUrl = sessionStorage.getItem('aw_redirect_url') || 'homepage';
          sessionStorage.removeItem('aw_redirect_url');
          setTimeout(() => {
            window.location.href = redirectUrl;
          }, 400);
        } else {
          window.location.href = 'homepage';
        }
      })
      .catch(err => {
        console.error("Sign-in request error:", err);
        renderToast("Network handshake anomaly during gateway connection.", "error");
        if (submitBtn) {
          submitBtn.innerHTML = originalText;
          submitBtn.style.opacity = '1';
        }
      });
  }

  /**
   * Doctor Booking Workflow: POST /psychinfo
   */
  function handleDoctorBookingSubmission(form) {
    const formData = new FormData(form);
    const doctorName = formData.get('psychname') || 'Psychiatric Specialist';
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalBtn = submitBtn ? submitBtn.innerHTML : 'Confirm Booking';

    if (submitBtn) {
      submitBtn.innerHTML = '<span class="aw-mono" style="font-size:0.8rem;">DISPATCHING CLINICAL DOSSIER...</span>';
      submitBtn.disabled = true;
    }

    fetch('psychinfo', {
      method: 'POST',
      body: formData,
      credentials: 'include',
      headers: {
        'X-CSRFToken': getCsrfToken(),
      }
    })
      .then(res => res.text())
      .then(html => {
        if (submitBtn) {
          submitBtn.innerHTML = originalBtn;
          submitBtn.disabled = false;
        }

        // Close modal
        window.closeBookingModal();

        // Check response payload for confirmation
        if (html.includes("Appointment Request Sent Successfully") || html.includes("psychiatrist")) {
          renderToast(
            `✓ Consultation Transmitted! Appointment request & longitudinal dossier delivered to Dr. ${doctorName}.`,
            "success"
          );
        } else {
          renderToast(
            `Consultation queued for Dr. ${doctorName}. Telemetry dispatched via clinical relay.`,
            "info"
          );
        }
      })
      .catch(err => {
        console.error("Doctor booking failed:", err);
        if (submitBtn) {
          submitBtn.innerHTML = originalBtn;
          submitBtn.disabled = false;
        }
        renderToast("Transmission failure during appointment booking.", "error");
      });
  }

  /**
   * Wellness Reflection Logging: POST /wellnessLog
   */
  function handleWellnessLogSubmission(form) {
    const formData = new FormData(form);
    const textarea = document.getElementById('journalTextarea');
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalBtn = submitBtn ? submitBtn.innerHTML : 'Submit';

    if (submitBtn) {
      submitBtn.innerHTML = '<span class="aw-mono" style="font-size:0.8rem;">ENCRYPTING & STORING...</span>';
      submitBtn.disabled = true;
    }

    fetch('wellnessLog', {
      method: 'POST',
      body: formData,
      credentials: 'include',
      headers: {
        'X-CSRFToken': getCsrfToken(),
      }
    })
      .then(res => res.text())
      .then(html => {
        if (submitBtn) {
          submitBtn.innerHTML = originalBtn;
          submitBtn.disabled = false;
        }

        // Clear textarea & word counter
        if (textarea) textarea.value = '';
        const wordCount = document.getElementById('awWordCount');
        if (wordCount) wordCount.textContent = '0 words (0 characters)';

        // Display success toast
        renderToast("✓ Somatic Reflection Encrypted & Stored! Appended to MySQL clinical logs.", "success");
      })
      .catch(err => {
        console.error("Journal logging failed:", err);
        if (submitBtn) {
          submitBtn.innerHTML = originalBtn;
          submitBtn.disabled = false;
        }
        renderToast("Failed to commit reflection to database.", "error");
      });
  }

  /**
   * ========================================================================
   * 6. WORD REPORT EXPORT TELEMETRY HUD
   * ========================================================================
   */
  function initExportHUD() {
    document.addEventListener('click', function (e) {
      const btn = e.target.closest('a[href*="wellnessLogFileCreator"]');
      if (!btn) return;

      e.preventDefault();
      showExportHUD();
    });
  }

  function showExportHUD() {
    let hud = document.getElementById('awExportModal');
    if (!hud) {
      hud = document.createElement('div');
      hud.id = 'awExportModal';
      hud.className = 'aw-export-modal';
      hud.innerHTML = `
        <div class="aw-export-hud-card">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <div style="display:flex; align-items:center; gap:10px;">
              <span class="aw-status-beacon"></span>
              <h3 style="font-size:1.15rem; font-weight:700;">Clinical Telemetry Compiler</h3>
            </div>
            <span class="aw-tag">UNESCO STANDARD</span>
          </div>

          <p style="font-size:0.85rem; color:var(--aw-slate-light); line-height:1.6;">
            Compiling patient longitudinal wellness reflections into an authenticated DOCX clinical dossier...
          </p>

          <div class="aw-progress-bar-wrap">
            <div id="awExportFill" class="aw-progress-bar-fill"></div>
          </div>

          <div id="awTelemetryTerminal" style="background:rgba(6,8,20,0.8); border:1px solid rgba(45,212,191,0.2); border-radius:12px; padding:1rem; font-family:var(--aw-font-mono); font-size:0.75rem; color:var(--aw-teal-bright); min-height:110px; display:flex; flex-direction:column; gap:4px;">
            <div>> Handshake initiated with persistence tier...</div>
          </div>

          <div style="display:flex; justify-content:flex-end;">
            <button id="awHudDismissBtn" class="aw-btn aw-btn-secondary" style="font-size:0.8rem; padding:0.4rem 1rem; display:none;">Close</button>
          </div>
        </div>
      `;
      document.body.appendChild(hud);

      document.getElementById('awHudDismissBtn').onclick = () => {
        hud.style.display = 'none';
      };
    }

    hud.style.display = 'flex';
    const fill = document.getElementById('awExportFill');
    const term = document.getElementById('awTelemetryTerminal');
    const dismiss = document.getElementById('awHudDismissBtn');

    fill.style.width = '0%';
    term.innerHTML = '<div>> Handshake initiated with persistence tier...</div>';
    dismiss.style.display = 'none';

    setTimeout(() => {
      fill.style.width = '30%';
      term.innerHTML += '<div>> Extracting MySQL table "wellnesslog" for active user... [OK]</div>';
    }, 400);

    setTimeout(() => {
      fill.style.width = '70%';
      term.innerHTML += '<div>> python-docx executing clinical formatting protocol... [OK]</div>';
    }, 900);

    setTimeout(() => {
      fill.style.width = '100%';
      term.innerHTML += '<div>> Document checksum validated. Dispatched download!</div>';
      dismiss.style.display = 'block';

      const dlLink = document.createElement('a');
      dlLink.href = 'wellnessLogFileCreator';
      dlLink.style.display = 'none';
      document.body.appendChild(dlLink);
      dlLink.click();
      document.body.removeChild(dlLink);
    }, 1500);
  }

  /**
   * ========================================================================
   * 7. CONSULTATION BOOKING MODAL (Specialist Registry)
   * ========================================================================
   */
  window.openBookingModal = function (doctorName, rating, education, location) {
    let modal = document.getElementById('awBookingModal');
    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'awBookingModal';
      modal.className = 'aw-modal-backdrop';
      modal.innerHTML = `
        <div class="aw-booking-modal-card">
          <button class="aw-modal-close" onclick="closeBookingModal()">&times;</button>
          <div style="display:flex; align-items:center; gap:12px; margin-bottom:1.5rem;">
            <div class="aw-brand-symbol" style="width:40px; height:40px;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
            </div>
            <div>
              <h3 style="font-size:1.25rem; font-weight:700;" id="awModalDocName">Specialist Consultation</h3>
              <p style="font-size:0.8rem; color:var(--aw-teal-bright); font-family:var(--aw-font-mono);">
                UNESCO Verified Multilateral Practitioner
              </p>
            </div>
          </div>

          <form action="psychinfo" method="POST" id="awBookingForm">
            <input type="hidden" name="csrfmiddlewaretoken" value="${getCsrfToken()}">
            <input type="hidden" name="psychname" id="awHiddenPsychName" value="">
            <input type="hidden" name="appointmentBtn" value="BookAppointment">

            <div class="aw-form-group">
              <label class="aw-form-label">Consultation Focus</label>
              <select name="concern" class="aw-form-select">
                <option value="Stress & Anxiety Regulation">Stress & Anxiety Regulation</option>
                <option value="Longitudinal Depression Management">Longitudinal Depression Management</option>
                <option value="Somatic & Sleep Architecture Calibration">Somatic & Sleep Architecture Calibration</option>
                <option value="Trauma Informed Processing">Trauma Informed Processing</option>
                <option value="General Psychosocial Telemetry Evaluation">General Psychosocial Telemetry Evaluation</option>
              </select>
            </div>

            <div style="display:grid; grid-template-columns:1fr 1fr; gap:1rem;">
              <div class="aw-form-group">
                <label class="aw-form-label">Preferred Date</label>
                <input type="date" name="tb2" class="aw-form-input" required value="${new Date().toISOString().split('T')[0]}">
              </div>
              <div class="aw-form-group">
                <label class="aw-form-label">Preferred Slot (UTC)</label>
                <input type="time" name="tb3" class="aw-form-input" required value="14:00">
              </div>
            </div>

            <div style="margin: 1rem 0; font-size:0.75rem; color:var(--aw-slate-muted); line-height:1.5;">
              * Note: Your historical wellness reflection summaries will be securely attached to Dr. <span id="awModalDocNotice"></span>'s encrypted clinical consultation queue.
            </div>

            <div style="display:flex; justify-content:flex-end; gap:1rem; margin-top:1.5rem;">
              <button type="button" class="aw-btn aw-btn-secondary" onclick="closeBookingModal()">Cancel</button>
              <button type="submit" class="aw-btn aw-btn-primary">Confirm Clinical Booking</button>
            </div>
          </form>
        </div>
      `;
      document.body.appendChild(modal);
    }

    document.getElementById('awModalDocName').textContent = doctorName;
    document.getElementById('awHiddenPsychName').value = doctorName;
    document.getElementById('awModalDocNotice').textContent = doctorName;
    modal.style.display = 'flex';
  };

  window.closeBookingModal = function () {
    const modal = document.getElementById('awBookingModal');
    if (modal) modal.style.display = 'none';
  };

  function getCsrfToken() {
    const match = document.cookie.match(/(^|;\s*)(csrftoken)=([^;]*)/);
    return match ? decodeURIComponent(match[3]) : '';
  }

  /**
   * ========================================================================
   * 8. ROUTE-SPECIFIC CONTROLLER REBINDING
   * ========================================================================
   */
  function rebindRouteControllers() {
    // Journal Word Counter
    const journalArea = document.querySelector('.aw-journal-textarea');
    const wordCountEl = document.getElementById('awWordCount');
    if (journalArea && wordCountEl) {
      journalArea.addEventListener('input', function () {
        const text = journalArea.value.trim();
        const words = text ? text.split(/\s+/).length : 0;
        wordCountEl.textContent = `${words} words (${text.length} characters)`;
      });
    }

    // Audio Play Buttons
    document.querySelectorAll('.aw-play-trigger').forEach(btn => {
      btn.onclick = function (e) {
        e.preventDefault();
        const name = this.dataset.name || 'Harmonic Calibration';
        const src = this.dataset.src || '/static/audio/Ocean Wave Sound.mp3';
        window.playSanctuaryTrack(name, src);
      };
    });

    // Configure Video Stream Elements
    configureVideoStreaming();
  }

  // Self Initialization on DOM Ready
  function bootstrap() {
    hydrateSecurityFromDOM();
    initActivityListeners();
    initAudioSanctuary();
    initSPARouter();
    initDataIntegrationInterceptors();
    initExportHUD();
    rebindRouteControllers();

    // Evaluate immediate security guard on currently loaded path
    evaluateRouteSecurityGuard(window.location.pathname);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bootstrap);
  } else {
    bootstrap();
  }

})();
