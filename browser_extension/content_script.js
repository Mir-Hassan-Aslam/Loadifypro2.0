function createQualityPopup() {
    // Remove existing popup if any
    const existingPopup = document.querySelector('.loadifypro-quality-popup');
    if (existingPopup) {
        existingPopup.remove();
    }

    const popup = document.createElement('div');
    popup.className = 'loadifypro-quality-popup';
    popup.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: white;
        border: 2px solid #ff0000;
        border-radius: 10px;
        padding: 20px;
        z-index: 10000;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        font-family: Arial, sans-serif;
        min-width: 300px;
        max-width: 400px;
    `;

    const title = document.createElement('h3');
    title.textContent = '📥 Download with LoadifyPro';
    title.style.cssText = `
        margin: 0 0 15px 0;
        color: #333;
        text-align: center;
        font-size: 16px;
    `;

    const qualityOptions = [
        { label: '🎬 Best Quality (Auto)', value: 'best', description: 'Highest available quality' },
        { label: '📺 4K (2160p)', value: '2160p', description: 'Ultra HD quality' },
        { label: '📺 1080p', value: '1080p', description: 'Full HD quality' },
        { label: '📺 720p', value: '720p', description: 'HD quality' },
        { label: '📺 480p', value: '480p', description: 'Standard quality' },
        { label: '📺 360p', value: '360p', description: 'Low quality' },
        { label: '🎵 Audio Only (MP3)', value: 'audio', description: 'Audio track only' },
        { label: '🎵 Audio Only (M4A)', value: 'audio_m4a', description: 'High quality audio' }
    ];

    const optionsContainer = document.createElement('div');
    optionsContainer.style.cssText = `
        margin-bottom: 20px;
        max-height: 300px;
        overflow-y: auto;
    `;

    qualityOptions.forEach(option => {
        const optionDiv = document.createElement('div');
        optionDiv.style.cssText = `
            padding: 10px;
            margin: 5px 0;
            border: 1px solid #ddd;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.2s;
        `;

        optionDiv.innerHTML = `
            <div style="font-weight: bold; color: #333;">${option.label}</div>
            <div style="font-size: 12px; color: #666; margin-top: 2px;">${option.description}</div>
        `;

        optionDiv.addEventListener('mouseenter', () => {
            optionDiv.style.backgroundColor = '#f0f0f0';
        });

        optionDiv.addEventListener('mouseleave', () => {
            optionDiv.style.backgroundColor = 'white';
        });

        optionDiv.addEventListener('click', () => {
            downloadWithQuality(option.value);
            popup.remove();
        });

        optionsContainer.appendChild(optionDiv);
    });

    const cancelButton = document.createElement('button');
    cancelButton.textContent = '❌ Cancel';
    cancelButton.style.cssText = `
        background: #666;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 5px;
        cursor: pointer;
        float: right;
    `;
    cancelButton.addEventListener('click', () => {
        popup.remove();
    });

    popup.appendChild(title);
    popup.appendChild(optionsContainer);
    popup.appendChild(cancelButton);

    // Add backdrop
    const backdrop = document.createElement('div');
    backdrop.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.5);
        z-index: 9999;
    `;
    backdrop.addEventListener('click', () => {
        popup.remove();
        backdrop.remove();
    });

    document.body.appendChild(backdrop);
    document.body.appendChild(popup);

    console.log('LoadifyPro: Quality selection popup created');
}

function downloadWithQuality(quality) {
    const videoUrl = window.location.href;
    console.log(`LoadifyPro: Downloading with quality: ${quality}, URL: ${videoUrl}`);
    
    // Always use direct HTTP method to avoid extension context issues
    console.log("LoadifyPro: Sending directly to HTTP server");
    fetch('http://localhost:8080/add_download', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            url: videoUrl,
            quality: quality
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log("LoadifyPro: Received response from HTTP server:", data);
        // Show success message to user
        showSuccessMessage(`Download started with ${quality} quality!`);
    })
    .catch(error => {
        console.error("LoadifyPro: Error sending to HTTP server:", error);
        // Show error message to user
        showErrorMessage(`Failed to start download: ${error.message}`);
    });
}

function showSuccessMessage(message) {
    // Create a temporary success notification
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #4CAF50;
        color: white;
        padding: 12px 20px;
        border-radius: 5px;
        z-index: 10001;
        font-family: Arial, sans-serif;
        font-size: 14px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    `;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 3000);
}

function showErrorMessage(message) {
    // Create a temporary error notification
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #f44336;
        color: white;
        padding: 12px 20px;
        border-radius: 5px;
        z-index: 10001;
        font-family: Arial, sans-serif;
        font-size: 14px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    `;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    // Remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 5000);
}

function addDownloadButton() {
    // Check if button already exists
    if (document.querySelector('.loadifypro-download-btn')) {
        return;
    }

    // Find the YouTube video player container
    const playerContainer = document.querySelector('#movie_player') || 
                           document.querySelector('.html5-video-player') ||
                           document.querySelector('video')?.closest('div');
    
    if (!playerContainer) {
        console.log('LoadifyPro: Video player container not found');
        return;
    }

    const button = document.createElement('button');
    button.className = 'loadifypro-download-btn';
    button.innerText = '📥 Download with LoadifyPro';
    button.style.position = 'absolute';
    button.style.top = '10px';
    button.style.right = '10px';
    button.style.zIndex = '9999';
    button.style.padding = '8px 12px';
    button.style.backgroundColor = '#ff0000';
    button.style.color = 'white';
    button.style.border = 'none';
    button.style.borderRadius = '5px';
    button.style.cursor = 'pointer';
    button.style.fontSize = '12px';
    button.style.fontWeight = 'bold';
    button.style.boxShadow = '0 2px 4px rgba(0,0,0,0.3)';
    
    // Make sure the container can hold a positioned element
    if (getComputedStyle(playerContainer).position === 'static') {
        playerContainer.style.position = 'relative';
    }

    button.onclick = (e) => {
        e.stopPropagation();
        e.preventDefault();
        createQualityPopup();
    };

    playerContainer.appendChild(button);
    console.log('LoadifyPro: Download button added');
}

function addDownloadButtonsToLinks() {
    // Find all download links on the page
    const downloadLinks = document.querySelectorAll('a[href*=".exe"], a[href*=".zip"], a[href*=".rar"], a[href*=".7z"], a[href*=".msi"], a[href*=".dmg"], a[href*=".pkg"], a[href*=".deb"], a[href*=".rpm"], a[href*=".tar.gz"], a[href*=".tar.bz2"], a[href*=".iso"], a[href*=".bin"], a[href*=".apk"], a[href*=".ipa"]');
    
    downloadLinks.forEach(link => {
        // Skip if already processed
        if (link.hasAttribute('data-loadify-processed')) {
            return;
        }
        
        link.setAttribute('data-loadify-processed', 'true');
        
        // Store original href
        const originalHref = link.href;
        link.setAttribute('data-original-href', originalHref);
        
        // Change href to prevent default download
        link.href = 'javascript:void(0)';
        link.style.cursor = 'pointer';
        
        // Create download button
        const button = document.createElement('button');
        button.className = 'loadifypro-file-download-btn';
        button.innerHTML = '📥 LoadifyPro';
        button.style.cssText = `
            position: relative;
            display: inline-block;
            margin-left: 10px;
            padding: 4px 8px;
            background: #ff0000;
            color: white;
            border: none;
            border-radius: 3px;
            cursor: pointer;
            font-size: 11px;
            font-weight: bold;
            z-index: 1000;
        `;
        
        // Insert button after the link
        link.parentNode.insertBefore(button, link.nextSibling);
        
        button.onclick = (e) => {
            e.preventDefault();
            e.stopPropagation();
            
            console.log('LoadifyPro: File download detected:', originalHref);
            downloadFile(originalHref);
        };
        
        // Intercept the original link click
        link.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            e.stopImmediatePropagation();
            
            console.log('LoadifyPro: Intercepted file download:', originalHref);
            downloadFile(originalHref);
            return false;
        }, true);
        
        console.log('LoadifyPro: Added download button for file:', originalHref);
    });
}

function downloadFile(fileUrl) {
    console.log('LoadifyPro: Downloading file:', fileUrl);
    
    fetch('http://localhost:8080/add_download', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            url: fileUrl,
            quality: 'best' // Files don't have quality options
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('LoadifyPro: File download started:', data);
        showSuccessMessage('File download started with LoadifyPro!');
    })
    .catch(error => {
        console.error('LoadifyPro: Error downloading file:', error);
        showErrorMessage(`Failed to start file download: ${error.message}`);
    });
}

// Function to check for video and add button
function checkAndAddButton() {
    // Check if we're on a video page
    if (window.location.hostname.includes('youtube.com') && 
        window.location.pathname.includes('/watch')) {
        addDownloadButton();
    }
    
    // Always check for file download links on any page
    addDownloadButtonsToLinks();
}

// Global download interceptor
function setupGlobalDownloadInterceptor() {
    console.log('LoadifyPro: Setting up download interceptor');
    
    // More aggressive interception - override the entire click event
    document.addEventListener('click', function(e) {
        console.log('LoadifyPro: Click detected on:', e.target);
        
        let downloadUrl = null;
        let target = e.target;
        
        // Check if clicked element or its parent is a download link
        while (target && target !== document) {
            if (target.tagName === 'A' && target.href) {
                const url = target.href;
                const isDownloadableFile = /\.(exe|zip|rar|7z|msi|dmg|pkg|deb|rpm|tar\.gz|tar\.bz2|iso|bin|apk|ipa|pdf|doc|docx|xls|xlsx|ppt|pptx|mp3|mp4|avi|mkv|mov|wmv|flv|webm|m4a|wav|flac|ogg)$/i.test(url);
                
                if (isDownloadableFile) {
                    downloadUrl = url;
                    break;
                }
            }
            target = target.parentElement;
        }
        
        if (downloadUrl) {
            console.log('LoadifyPro: Intercepted download attempt:', downloadUrl);
            e.preventDefault();
            e.stopPropagation();
            e.stopImmediatePropagation();
            
            // Use setTimeout to ensure our handler runs first
            setTimeout(() => {
                downloadFile(downloadUrl);
            }, 0);
            
            return false;
        }
    }, true); // Use capture phase to intercept before other handlers
    
    // Intercept programmatic downloads
    const originalOpen = window.open;
    window.open = function(url, ...args) {
        if (url && /\.(exe|zip|rar|7z|msi|dmg|pkg|deb|rpm|tar\.gz|tar\.bz2|iso|bin|apk|ipa|pdf|doc|docx|xls|xlsx|ppt|pptx|mp3|mp4|avi|mkv|mov|wmv|flv|webm|m4a|wav|flac|ogg)$/i.test(url)) {
            console.log('LoadifyPro: Intercepted programmatic download:', url);
            downloadFile(url);
            return null;
        }
        return originalOpen.call(this, url, ...args);
    };
    
    // Override fetch to intercept programmatic downloads
    const originalFetch = window.fetch;
    window.fetch = function(url, options) {
        if (typeof url === 'string' && /\.(exe|zip|rar|7z|msi|dmg|pkg|deb|rpm|tar\.gz|tar\.bz2|iso|bin|apk|ipa|pdf|doc|docx|xls|xlsx|ppt|pptx|mp3|mp4|avi|mkv|mov|wmv|flv|webm|m4a|wav|flac|ogg)$/i.test(url)) {
            console.log('LoadifyPro: Intercepted fetch download:', url);
            downloadFile(url);
            return Promise.resolve(new Response('Download intercepted by LoadifyPro', { status: 200 }));
        }
        return originalFetch.call(this, url, options);
    };
    
    // Override XMLHttpRequest to intercept AJAX downloads
    const originalXHROpen = XMLHttpRequest.prototype.open;
    XMLHttpRequest.prototype.open = function(method, url, ...args) {
        if (typeof url === 'string' && /\.(exe|zip|rar|7z|msi|dmg|pkg|deb|rpm|tar\.gz|tar\.bz2|iso|bin|apk|ipa|pdf|doc|docx|xls|xlsx|ppt|pptx|mp3|mp4|avi|mkv|mov|wmv|flv|webm|m4a|wav|flac|ogg)$/i.test(url)) {
            console.log('LoadifyPro: Intercepted XHR download:', url);
            downloadFile(url);
            return;
        }
        return originalXHROpen.call(this, method, url, ...args);
    };
}

// Initialize extension directly (no need to wait for Chrome runtime)
function initializeExtension() {
    console.log('LoadifyPro: Initializing extension');
    
    // Setup global download interceptor
    setupGlobalDownloadInterceptor();
    
    // Run when page loads
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', checkAndAddButton);
    } else {
        checkAndAddButton();
    }

    // Also check periodically for dynamic content
    setInterval(checkAndAddButton, 2000);

    // Listen for YouTube navigation (SPA)
    let lastUrl = location.href;
    new MutationObserver(() => {
        const url = location.href;
        if (url !== lastUrl) {
            lastUrl = url;
            setTimeout(checkAndAddButton, 1000); // Wait a bit for page to load
        }
    }).observe(document, { subtree: true, childList: true });
}

// Start the extension immediately
initializeExtension();