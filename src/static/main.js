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
display:block;
}
.audio-controls{
  display:block !important;
}
.speaker-icon {
  font-size: 42px;
  margin:auto;
  background:none;
  color:inherit;
  padding:0;
  height:42px;
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

function textFormat() {
  // Get the modal
  var modal = document.getElementById("myModal");

  // Get the button that opens the modal
  var btn = document.getElementById("openModal");

  // Get the <span> element that closes the modal
  var span = document.getElementsByClassName("close")[0];

  // When the user clicks on the button, open the modal
  btn.onclick = function () {
    modal.style.display = "block";
  };

  // When the user clicks on <span> (x), close the modal
  span.onclick = function () {
    modal.style.display = "none";
  };

  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function (event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  };

  // When the user clicks on apply changes, update the text style
  document.getElementById("applyChanges").onclick = function () {
    var body = document.getElementsByTagName("body")[0];
    var backgroundColor = document.getElementById("backgroundColor").value;
    var foregroundColor = document.getElementById("foregroundColor").value;
    var lineSpacing = document.getElementById("lineSpacing").value;
    var fontStyle = document.getElementById("fontStyle").value;
    // Get the font style selected
    if (fontStyle=="sans-serif"){
      selectedFontStyle = `"Gill Sans", "Gill Sans MT", Calibri, "Trebuchet MS", sans-serif`;
    }else{
      selectedFontStyle = `Georgia, 'Times New Roman', Times, serif`
    }

    // Update the body style
    body.style.backgroundColor = backgroundColor;
    body.style.color = foregroundColor;
    body.style.lineHeight = lineSpacing;
    body.style.fontFamily = selectedFontStyle;
    document.getElementById("formatCSS").innerText = `p,
dl,
ol,
ul {
  line-height: unset;
}`
  };

  // When the user clicks on reset changes, reset the text style to default
  document.getElementById("resetChanges").onclick = function () {
    var body = document.getElementsByTagName("body")[0];

    // Reset the body style to default
    body.style.backgroundColor = "";
    body.style.color = "";
    body.style.lineHeight = "";
    body.style.fontFamily = "";

    // Reset the form values to default
    document.getElementById("backgroundColor").value = "#151515";
    document.getElementById("foregroundColor").value = "#dddddd";
    document.getElementById("lineSpacing").value = 1;
    document.getElementById("fontStyle").value = `sans-serif`;
    document.getElementById("formatCSS").innerText = `p,
dl,
ol,
ul {
  line-height: 2rem;
}`
  };
}
window.onload = function () {
  Prism.highlightAll();
  audioPlayer();
  textFormat();
};
