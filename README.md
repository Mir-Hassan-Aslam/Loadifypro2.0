# LoadifyPro 2.0 - Professional Download Manager

A powerful, feature-rich download manager built with Python and CustomTkinter, designed to rival commercial download managers like Internet Download Manager (IDM).

## 🚀 Features

### Core Download Features
- **Multi-format Support**: Download videos, files, documents, and more
- **YouTube Integration**: Download YouTube videos with quality selection (4K, 1080p, 720p, etc.)
- **Pause/Resume**: Full pause and resume functionality for all downloads
- **Speed Limiting**: Control download speed to manage bandwidth
- **Progress Tracking**: Real-time progress, speed, and ETA display
- **Queue Management**: Download multiple files simultaneously with queue system

### Browser Integration
- **Chrome Extension**: Seamless browser integration with custom extension
- **Download Interception**: Automatically captures download links from any website
- **Quality Selection**: IDM-like quality selection popup for videos
- **Universal Support**: Works with all file types (.exe, .zip, .pdf, .mp4, etc.)

### Security & Management
- **Antivirus Scanning**: Built-in Windows Defender and VirusTotal integration
- **Proxy Support**: HTTP/HTTPS proxy configuration
- **Authentication**: Support for HTTP authentication
- **Scheduling**: Time-based download scheduling
- **Drag & Drop**: Easy URL input via drag and drop

### User Interface
- **Modern UI**: Beautiful CustomTkinter interface with themes
- **Multilingual**: English and Spanish support
- **Dark/Light Themes**: Switch between appearance modes
- **Real-time Stats**: Global download statistics and monitoring

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Windows 10/11 (for antivirus integration)

### Setup
1. Clone the repository:
```bash
git clone https://github.com/yourusername/loadifypro-2.0.git
cd loadifypro-2.0
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run LoadifyPro:
```bash
python main_app.py
```

### Browser Extension Setup
1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked" and select the `browser_extension` folder
4. The extension will automatically detect download links

## 🎯 Usage

### Basic Download
1. Enter a URL in the URL field
2. Select destination folder
3. Click "Start Download"

### Browser Integration
1. Install the Chrome extension
2. Visit any website with download links
3. Click "📥 LoadifyPro" buttons that appear next to download links
4. For videos, select your preferred quality

### Pause/Resume
- Click ⏸️ to pause a download
- Click ▶️ to resume a paused download
- Click ❌ to cancel a download

## 🛠️ Technical Details

### Architecture
- **Main App**: `main_app.py` - Main application entry point
- **Download Core**: `download_core.py` - Core download logic and threading
- **UI Components**: `ui_components.py` - Custom UI widgets and windows
- **Managers**: Modular manager classes for different features
- **Browser Integration**: HTTP server + Chrome extension for browser integration

### Key Technologies
- **Python 3.8+**: Core language
- **CustomTkinter**: Modern UI framework
- **yt-dlp**: YouTube video downloading
- **requests**: HTTP file downloads
- **Flask**: HTTP server for browser integration
- **Chrome Extension**: JavaScript for browser integration

## 📁 Project Structure

```
LoadifyPro 2.0/
├── main_app.py              # Main application
├── download_core.py         # Download logic
├── ui_components.py         # UI components
├── requirements.txt         # Dependencies
├── browser_extension/       # Chrome extension
│   ├── manifest.json
│   ├── content_script.js
│   └── background.js
├── managers/                # Feature managers
│   ├── settings_manager.py
│   ├── antivirus_manager.py
│   ├── proxy_manager.py
│   └── ...
└── README.md
```

## 🔧 Configuration

### Settings
Access settings through the Settings button in the main interface:
- Download destination
- Speed limits
- Proxy settings
- Antivirus configuration
- Theme preferences
- Language settings

### Browser Extension
The extension automatically:
- Detects download links on any website
- Shows quality selection for videos
- Intercepts downloads to use LoadifyPro

## 🚀 Features Comparison

| Feature | LoadifyPro | IDM | Free Download Manager |
|---------|------------|-----|----------------------|
| YouTube Download | ✅ | ✅ | ✅ |
| Quality Selection | ✅ | ✅ | ❌ |
| Pause/Resume | ✅ | ✅ | ✅ |
| Browser Integration | ✅ | ✅ | ✅ |
| Antivirus Scanning | ✅ | ❌ | ❌ |
| Speed Limiting | ✅ | ✅ | ✅ |
| Proxy Support | ✅ | ✅ | ✅ |
| Modern UI | ✅ | ❌ | ❌ |
| Free | ✅ | ❌ | ✅ |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- CustomTkinter for the beautiful UI framework
- yt-dlp for YouTube downloading capabilities
- Chrome Extension API for browser integration
- Python community for excellent libraries

## 📞 Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/yourusername/loadifypro-2.0/issues) page
2. Create a new issue with detailed information
3. Include system information and error logs

---

**LoadifyPro 2.0** - Professional Download Management Made Simple! 🚀📥
