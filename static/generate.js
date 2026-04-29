// ============================================
// HeartMula Generate Page - Music Generation
// ============================================

const lyricsInput = document.getElementById('lyricsInput');
const tagCategories = document.getElementById('tagCategories');
const selectionSummary = document.getElementById('selectionSummary');
const summaryText = document.getElementById('summaryText');
const generateBtn = document.getElementById('generateBtn');
const progressContainer = document.getElementById('progressContainer');
const progressPercent = document.getElementById('progressPercent');
const progressFill = document.getElementById('progressFill');
const progressHint = document.getElementById('progressHint');
const progressLabel = document.getElementById('progressLabel');
const successContainer = document.getElementById('successContainer');
const errorContainer = document.getElementById('errorContainer');
const errorMessage = document.getElementById('errorMessage');
const retryBtn = document.getElementById('retryBtn');
const resetBtn = document.getElementById('resetBtn');

// 用户标签选择
const selectedTags = {};

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    loadTags();
    setupEventListeners();
});

function setupEventListeners() {
    lyricsInput.addEventListener('input', updateGenerateButton);
    retryBtn.addEventListener('click', resetUI);
    resetBtn.addEventListener('click', resetUI);
}

// 加载标签分类
async function loadTags() {
    try {
        const response = await fetch('/api/v1/tags');
        if (!response.ok) {
            throw new Error(`获取标签失败 (${response.status})`);
        }
        const data = await response.json();
        renderTagCategories(data.categories);
    } catch (error) {
        showError('加载标签选项失败，请刷新页面重试');
    }
}

// 渲染标签分类
function renderTagCategories(categories) {
    tagCategories.innerHTML = categories.map(category => `
        <div class="tag-category" data-category="${category.name}">
            <div class="category-name">${category.display_name}</div>
            <div class="category-tags">
                ${category.tags.map(tag => `
                    <button
                        class="tag-pill"
                        data-value="${tag.value}"
                        data-display="${tag.display_name}"
                        onclick="selectTag('${category.name}', '${tag.value}', '${tag.display_name}')"
                    >
                        ${tag.display_name}
                    </button>
                `).join('')}
            </div>
        </div>
    `).join('');
}

// 选择标签
function selectTag(category, value, displayName) {
    const categoryEl = document.querySelector(`[data-category="${category}"]`);
    const pills = categoryEl.querySelectorAll('.tag-pill');

    // 互斥选择：同类标签只能选一个
    if (selectedTags[category] === value) {
        // 取消选择
        delete selectedTags[category];
        pills.forEach(pill => pill.classList.remove('selected'));
    } else {
        // 选中新标签
        selectedTags[category] = value;
        pills.forEach(pill => {
            if (pill.dataset.value === value) {
                pill.classList.add('selected');
            } else {
                pill.classList.remove('selected');
            }
        });
    }

    updateSummary();
    updateGenerateButton();
}

// 更新选择摘要
function updateSummary() {
    const selections = Object.entries(selectedTags);
    if (selections.length === 0) {
        summaryText.textContent = '未选择任何标签';
        summaryText.classList.add('empty');
    } else {
        summaryText.textContent = selections.map(([_, v]) => v).join(' + ');
        summaryText.classList.remove('empty');
    }
}

// 更新生成按钮状态
function updateGenerateButton() {
    const hasLyrics = lyricsInput.value.trim().length > 0;
    generateBtn.disabled = !hasLyrics;
}

// 处理生成
async function handleGenerate() {
    const lyrics = lyricsInput.value.trim();
    if (!lyrics) {
        showError('请输入歌词内容');
        return;
    }

    showProgress();

    try {
        // 第一步：验证标签
        updateProgress(10, '验证标签选择...');
        await delay(300);

        const selectResponse = await fetch('/api/v1/tags/select', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ selections: selectedTags }),
        });

        if (!selectResponse.ok) {
            const errorData = await selectResponse.json().catch(() => ({}));
            throw new Error(errorData.detail || '标签验证失败');
        }

        const selectData = await selectResponse.json();
        const tagsString = selectData.tags;

        // 第二步：生成音乐
        updateProgress(30, '正在生成音乐...');
        await simulateProgress(30, 80, 1500);

        updateProgress(80, '服务器处理中...');
        await delay(500);

        const generateResponse = await fetch('/api/v1/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ lyrics, tags: tagsString }),
        });

        if (!generateResponse.ok) {
            const errorData = await generateResponse.json().catch(() => ({}));
            throw new Error(errorData.detail || '音乐生成失败');
        }

        updateProgress(95, '下载音频文件...');
        await delay(200);

        // 下载文件
        const blob = await generateResponse.blob();
        const contentDisposition = generateResponse.headers.get('Content-Disposition');
        let filename = 'generated_music.mp3';
        if (contentDisposition) {
            const match = contentDisposition.match(/filename="?(.+)"?/);
            if (match) filename = match[1];
        }
        downloadBlob(blob, filename);

        updateProgress(100, '生成完成');
        await delay(300);
        showSuccess();

    } catch (error) {
        showError(error.message || '生成失败，请重试');
    }
}

// 进度模拟
function simulateProgress(start, end, duration) {
    return new Promise(resolve => {
        const steps = 10;
        const stepDuration = duration / steps;
        let step = 0;

        const interval = setInterval(() => {
            step++;
            const progress = start + (end - start) * (step / steps);
            updateProgress(progress, `生成中... ${Math.round(progress)}%`);

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

// 下载 blob
function downloadBlob(blob, filename) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// UI 状态管理
function showProgress() {
    generateBtn.hidden = true;
    successContainer.hidden = true;
    errorContainer.hidden = true;
    progressContainer.hidden = false;
    progressFill.style.width = '0%';
}

function showSuccess() {
    progressContainer.hidden = true;
    errorContainer.hidden = true;
    generateBtn.hidden = true;
    successContainer.hidden = false;
}

function showError(message) {
    progressContainer.hidden = true;
    successContainer.hidden = true;
    generateBtn.hidden = true;
    errorContainer.hidden = false;
    errorMessage.textContent = message;
}

function resetUI() {
    progressContainer.hidden = true;
    successContainer.hidden = true;
    errorContainer.hidden = true;
    generateBtn.hidden = false;
    lyricsInput.value = '';
    Object.keys(selectedTags).forEach(key => delete selectedTags[key]);
    document.querySelectorAll('.tag-pill').forEach(pill => pill.classList.remove('selected'));
    updateSummary();
    updateGenerateButton();
}

// 绑定生成按钮
generateBtn.addEventListener('click', handleGenerate);
