let played = false;
function audioPlayer() {
  const audioWrapper = document.querySelector(".audio-wrapper");
  const speakerIcon = document.querySelector(".speaker-icon");
  const audioPlayer = document.querySelector(".audio-player");
  const speedControl = document.querySelector(".audio-speed-control");
  const progressBar = document.querySelector(".progress-bar");
  const progressBarContainer = document.querySelector(
    ".progress-bar-container"
  );
  const fastForwardButton = document.querySelector(".fast-forward-button");
  const rewindButton = document.querySelector(".rewind-button");
  const css = document.getElementById("audioCSS");
  // Add event listener to speaker icon to show/hide audio player
  speakerIcon.addEventListener("click", () => {
    audioWrapper.classList.toggle("show-audio");
    if (audioWrapper.classList.contains("show-audio")) {
      audioPlayer.play();
      speakerIcon.innerText = "⏸";
      if (!played) {
        played = true;
        css.innerText = `
.audio-wrapper{
    max-width: 25vw;
  width:100%;
  left:calc(50% - 12.5vw);
  position:fixed;
  top:0;
  background-color:#222;
  padding:1rem;
  border-radius:0.3rem;
  z-index:1000;
}
.audio-controls{
  display:block !important;
}
`;
      }
    } else {
      audioPlayer.pause();
      speakerIcon.innerText = "▶";
    }
  });

  // Add event listener to speed control to update playback speed
  speedControl.addEventListener("input", () => {
    audioPlayer.playbackRate = speedControl.value;
  });

  // Add event listener to update progress bar
  audioPlayer.addEventListener("timeupdate", () => {
    const duration = audioPlayer.duration;
    const currentTime = audioPlayer.currentTime;
    const progress = (currentTime / duration) * 100;
    progressBar.style.width = `${progress}%`;
  });
  // Add event listener to progress bar container to update progress bar on drag
  progressBarContainer.addEventListener("mousedown", (event) => {
    const containerWidth = progressBarContainer.offsetWidth;
    const offsetX = event.offsetX;
    const percentage = (offsetX / containerWidth) * 100;
    progressBar.style.width = `${percentage}%`;
    const currentTime = (percentage / 100) * audioPlayer.duration;
    audioPlayer.currentTime = currentTime;
  });

  // Add event listener to fast forward button to skip ahead by 10 seconds
  fastForwardButton.addEventListener("click", () => {
    audioPlayer.currentTime += 10;
  });

  // Add event listener to rewind button to skip back by 10 seconds
  rewindButton.addEventListener("click", () => {
    audioPlayer.currentTime -= 10;
  });
}

window.onload = function () {
  Prism.highlightAll();
  audioPlayer();
};
