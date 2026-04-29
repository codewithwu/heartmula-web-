// ============================================
// HeartMula Lyrics Page - Upload & Transcribe
// ============================================

const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const progressContainer = document.getElementById('progressContainer');
const progressPercent = document.getElementById('progressPercent');
const progressFill = document.getElementById('progressFill');
const progressHint = document.getElementById('progressHint');
const fileName = document.getElementById('fileName');
const resultContainer = document.getElementById('resultContainer');
const lyricsContent = document.getElementById('lyricsContent');
const errorContainer = document.getElementById('errorContainer');
const errorMessage = document.getElementById('errorMessage');
const downloadBtn = document.getElementById('downloadBtn');
const retryBtn = document.getElementById('retryBtn');
const resetBtn = document.getElementById('resetBtn');

let currentLyrics = '';
let currentFilename = 'lyrics';

// Event Listeners
uploadArea.addEventListener('click', () => fileInput.click());

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('drag-over');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFile(e.target.files[0]);
    }
});

retryBtn.addEventListener('click', resetUI);
resetBtn.addEventListener('click', resetUI);
downloadBtn.addEventListener('click', downloadLyrics);

// File Handler
function handleFile(file) {
    const validTypes = ['audio/mpeg', 'audio/wav', 'audio/mp4', 'audio/x-m4a', 'audio/m4a'];
    const extension = file.name.split('.').pop().toLowerCase();
    const validExtensions = ['mp3', 'wav', 'm4a'];

    if (!validTypes.includes(file.type) && !validExtensions.includes(extension)) {
        showError('请上传有效的音频文件 (MP3, WAV, M4A)');
        return;
    }

    currentFilename = file.name.replace(/\.[^/.]+$/, '');
    fileName.textContent = file.name;
    uploadFile(file);
}

// Upload & Transcribe
async function uploadFile(file) {
    showProgress();

    const formData = new FormData();
    formData.append('file', file);

    try {
        updateProgress(5, '正在连接服务器...');
        await delay(300);

        updateProgress(10, '正在上传音频文件...');
        await simulateProgress(10, 25, 600);

        updateProgress(25, '服务器接收文件...');
        await delay(400);

        updateProgress(30, '正在处理音频...');
        await simulateProgress(30, 50, 800);

        updateProgress(50, '正在识别歌词...');
        await simulateProgress(50, 75, 1000);

        updateProgress(75, '正在进行语音识别...');
        await simulateProgress(75, 90, 800);

        updateProgress(90, '正在生成歌词结果...');

        const response = await fetch('/api/v1/transcribe', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `请求失败 (${response.status})`);
        }

        const data = await response.json();
        currentLyrics = data.lyrics || '未检测到歌词内容';

        updateProgress(100, '处理完成');
        await delay(300);
        showResult();

    } catch (error) {
        showError(error.message || '上传失败，请重试');
    }
}

// Progress Helpers
function simulateProgress(start, end, duration) {
    return new Promise(resolve => {
        const steps = 8;
        const stepDuration = duration / steps;
        let step = 0;

        const interval = setInterval(() => {
            step++;
            const progress = start + (end - start) * (step / steps);
            updateProgress(progress, `处理中... ${Math.round(progress)}%`);

            if (step >= steps) {
                clearInterval(interval);
                resolve();
            }
        }, stepDuration);
    });
}

function updateProgress(percent, hint) {
    progressPercent.textContent = `${Math.round(percent)}%`;
    progressFill.style.width = `${percent}%`;
    progressHint.textContent = hint;
}

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// UI State Management
function showProgress() {
    uploadArea.hidden = true;
    resultContainer.hidden = true;
    errorContainer.hidden = true;
    progressContainer.hidden = false;
    progressFill.style.width = '0%';
}

function showResult() {
    progressContainer.hidden = true;
    errorContainer.hidden = true;
    resultContainer.hidden = false;
    lyricsContent.textContent = currentLyrics;
}

function showError(message) {
    progressContainer.hidden = true;
    resultContainer.hidden = true;
    errorContainer.hidden = false;
    errorMessage.textContent = message;
}

function resetUI() {
    progressContainer.hidden = true;
    resultContainer.hidden = true;
    errorContainer.hidden = true;
    uploadArea.hidden = false;
    fileInput.value = '';
}

// Download
function downloadLyrics() {
    const blob = new Blob([currentLyrics], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${currentFilename}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}
