/* ============================================
   HeartMula Showcase Page - Audio Player & Lyrics
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {
    // DOM 元素
    const audioPlayer = document.getElementById('audioPlayer');
    const playBtn = document.getElementById('playBtn');
    const playerCard = document.querySelector('.player-card');
    const progressBar = document.getElementById('progressBar');
    const progressFill = document.getElementById('progressFill');
    const progressThumb = document.getElementById('progressThumb');
    const currentTimeEl = document.getElementById('currentTime');
    const totalTimeEl = document.getElementById('totalTime');
    const volumeSlider = document.getElementById('volumeSlider');
    const lyricsContent = document.getElementById('lyricsContent');

    // 格式化时间
    function formatTime(seconds) {
        if (isNaN(seconds) || seconds < 0) return '0:00';
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    }

    // 播放/暂停切换
    function togglePlay() {
        if (audioPlayer.paused) {
            audioPlayer.play();
            playerCard.classList.add('playing');
        } else {
            audioPlayer.pause();
            playerCard.classList.remove('playing');
        }
    }

    // 更新进度条
    function updateProgress() {
        const { currentTime, duration } = audioPlayer;
        const percent = (currentTime / duration) * 100 || 0;
        progressFill.style.width = `${percent}%`;
        progressThumb.style.left = `${percent}%`;
        currentTimeEl.textContent = formatTime(currentTime);
    }

    // 进度条点击跳转
    function seekTo(e) {
        const rect = progressBar.getBoundingClientRect();
        const percent = (e.clientX - rect.left) / rect.width;
        audioPlayer.currentTime = percent * audioPlayer.duration;
    }

    // 设置音量
    function setVolume(e) {
        audioPlayer.volume = e.target.value / 100;
    }

    // 音频加载完成
    function onLoadedMetadata() {
        totalTimeEl.textContent = formatTime(audioPlayer.duration);
    }

    // 音频播放结束
    function onEnded() {
        playerCard.classList.remove('playing');
        progressFill.style.width = '0%';
        progressThumb.style.left = '0%';
        currentTimeEl.textContent = '0:00';
    }

    // 加载歌词
    async function loadLyrics() {
        try {
            const response = await fetch('/example/lyrics.txt');
            if (!response.ok) throw new Error('Failed to load lyrics');
            const text = await response.text();
            lyricsContent.textContent = text;
        } catch (error) {
            console.error('Failed to load lyrics:', error);
            lyricsContent.textContent = '歌词加载失败';
        }
    }

    // 事件绑定
    playBtn.addEventListener('click', togglePlay);
    progressBar.addEventListener('click', seekTo);
    volumeSlider.addEventListener('input', setVolume);
    audioPlayer.addEventListener('timeupdate', updateProgress);
    audioPlayer.addEventListener('loadedmetadata', onLoadedMetadata);
    audioPlayer.addEventListener('ended', onEnded);

    // 初始化
    audioPlayer.volume = volumeSlider.value / 100;
    loadLyrics();
});